"""
VUC-2026 YouTube Upload Service
Complete video upload, metadata, and thumbnail management
"""

import os
import asyncio
import json
import logging
import aiohttp
import aiofiles
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import mimetypes
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tempfile

from .youtube_auth_service import youtube_auth_service

logger = logging.getLogger(__name__)

@dataclass
class VideoMetadata:
    """Video metadata structure"""
    title: str
    description: str
    tags: List[str]
    category_id: str
    language: str = "en"
    privacy_status: str = "private"
    made_for_kids: bool = False
    age_restricted: bool = False
    publish_at: Optional[datetime] = None

@dataclass
class UploadProgress:
    """Upload progress tracking"""
    video_id: str
    status: str
    bytes_uploaded: int
    total_bytes: int
    progress_percent: float
    error_message: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

@dataclass
class ThumbnailOptions:
    """Thumbnail generation options"""
    text: str = ""
    font_size: int = 48
    text_color: str = "#FFFFFF"
    background_color: str = "#000000"
    quality: int = 90
    size: tuple = (1280, 720)

class YouTubeUploadService:
    """
    Complete YouTube video upload service for VUC-2026
    Handles video uploads, metadata, thumbnails, and optimization
    """
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.thumbnail_dir = Path("thumbnails")
        self.temp_dir = Path("temp")
        
        # Create directories
        for directory in [self.upload_dir, self.thumbnail_dir, self.temp_dir]:
            directory.mkdir(exist_ok=True)
        
        # Supported video formats
        self.supported_formats = [
            "video/mp4", "video/quicktime", "video/x-msvideo",
            "video/x-ms-wmv", "video/webm", "video/3gpp"
        ]
        
        # Upload tracking
        self.active_uploads = {}
        
        # Initialize upload service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize upload service"""
        try:
            logger.info("YouTube Upload Service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize upload service: {str(e)}")
    
    async def upload_video(self, 
                          video_path: str,
                          metadata: VideoMetadata,
                          thumbnail_path: str = None,
                          state: str = None) -> Dict[str, Any]:
        """
        Upload video to YouTube with metadata and thumbnail
        
        Args:
            video_path: Path to video file
            metadata: Video metadata
            thumbnail_path: Path to thumbnail file (optional)
            state: OAuth session state
            
        Returns:
            Upload result with video ID and status
        """
        try:
            # Validate video file
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Get OAuth credentials
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid or expired OAuth credentials")
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Prepare video metadata
            body = {
                "snippet": {
                    "title": metadata.title,
                    "description": metadata.description,
                    "tags": metadata.tags,
                    "categoryId": metadata.category_id,
                    "defaultLanguage": metadata.language,
                    "defaultAudioLanguage": metadata.language
                },
                "status": {
                    "privacyStatus": metadata.privacy_status,
                    "madeForKids": metadata.made_for_kids,
                    "selfDeclaredMadeForKids": metadata.made_for_kids
                }
            }
            
            # Add scheduled publish time if specified
            if metadata.publish_at:
                body["status"]["publishAt"] = metadata.publish_at.isoformat() + "Z"
            
            # Prepare media upload
            media = MediaIoBaseUpload(
                open(video_path, 'rb'),
                mimetype=self._get_mime_type(video_path),
                chunksize=1024*1024,  # 1MB chunks
                resumable=True
            )
            
            # Start upload
            logger.info(f"Starting upload for video: {metadata.title}")
            
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            # Execute upload with progress tracking
            video_id = await self._execute_upload_with_progress(request, video_path)
            
            if video_id:
                # Upload thumbnail if provided
                if thumbnail_path and os.path.exists(thumbnail_path):
                    await self._upload_thumbnail(youtube, video_id, thumbnail_path)
                
                # Generate thumbnail if not provided
                elif not thumbnail_path:
                    thumbnail_path = await self._generate_thumbnail(video_path, metadata.title)
                    if thumbnail_path:
                        await self._upload_thumbnail(youtube, video_id, thumbnail_path)
                
                logger.info(f"Video uploaded successfully: {video_id}")
                
                return {
                    "success": True,
                    "video_id": video_id,
                    "title": metadata.title,
                    "status": "uploaded",
                    "upload_time": datetime.utcnow().isoformat(),
                    "thumbnail_uploaded": bool(thumbnail_path)
                }
            else:
                raise Exception("Upload failed")
                
        except Exception as e:
            logger.error(f"Error uploading video: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status": "failed"
            }
    
    async def _execute_upload_with_progress(self, request, video_path: str) -> Optional[str]:
        """Execute upload with progress tracking"""
        try:
            file_size = os.path.getsize(video_path)
            upload_progress = UploadProgress(
                video_id="pending",
                status="uploading",
                bytes_uploaded=0,
                total_bytes=file_size,
                progress_percent=0.0
            )
            
            # Track upload progress
            upload_id = f"upload_{datetime.utcnow().timestamp()}"
            self.active_uploads[upload_id] = upload_progress
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    upload_progress.bytes_uploaded = status.resumable_progress
                    upload_progress.progress_percent = (status.resumable_progress / file_size) * 100
                    
                    logger.info(f"Upload progress: {upload_progress.progress_percent:.1f}%")
            
            # Get video ID from response
            video_id = response.get("id")
            upload_progress.video_id = video_id
            upload_progress.status = "completed"
            upload_progress.completed_at = datetime.utcnow()
            
            return video_id
            
        except Exception as e:
            logger.error(f"Error in upload execution: {str(e)}")
            return None
    
    async def _upload_thumbnail(self, youtube, video_id: str, thumbnail_path: str) -> bool:
        """Upload thumbnail for video"""
        try:
            with open(thumbnail_path, 'rb') as thumbnail_file:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=thumbnail_file
                ).execute()
            
            logger.info(f"Thumbnail uploaded for video: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading thumbnail: {str(e)}")
            return False
    
    async def _generate_thumbnail(self, video_path: str, title: str) -> Optional[str]:
        """Generate thumbnail from video"""
        try:
            # Extract frame from video
            cap = cv2.VideoCapture(video_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Extract frame at 10% of video
            target_frame = int(total_frames * 0.1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None
            
            # Convert to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Resize to thumbnail dimensions
            pil_image = pil_image.resize((1280, 720), Image.Resampling.LANCZOS)
            
            # Add text overlay
            draw = ImageDraw.Draw(pil_image)
            
            # Try to load font
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Add title text
            text_lines = self._wrap_text(title, 40)
            y_position = 50
            
            for line in text_lines:
                # Add text shadow for better visibility
                draw.text((52, y_position + 2), line, fill="black", font=font)
                draw.text((48, y_position + 2), line, fill="black", font=font)
                draw.text((52, y_position - 2), line, fill="black", font=font)
                draw.text((48, y_position - 2), line, fill="black", font=font)
                draw.text((50, y_position), line, fill="white", font=font)
                
                y_position += 60
            
            # Save thumbnail
            thumbnail_path = self.thumbnail_dir / f"thumb_{datetime.utcnow().timestamp()}.jpg"
            pil_image.save(thumbnail_path, "JPEG", quality=90)
            
            logger.info(f"Generated thumbnail: {thumbnail_path}")
            
            return str(thumbnail_path)
            
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            return None
    
    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Wrap text for thumbnail"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines[:3]  # Max 3 lines
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type for file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"
    
    async def update_video_metadata(self, 
                                   video_id: str,
                                   metadata: VideoMetadata,
                                   state: str = None) -> Dict[str, Any]:
        """Update video metadata"""
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Prepare update body
            body = {
                "id": video_id,
                "snippet": {
                    "title": metadata.title,
                    "description": metadata.description,
                    "tags": metadata.tags,
                    "categoryId": metadata.category_id
                },
                "status": {
                    "privacyStatus": metadata.privacy_status
                }
            }
            
            # Update video
            response = youtube.videos().update(
                part="snippet,status",
                body=body
            ).execute()
            
            logger.info(f"Updated metadata for video: {video_id}")
            
            return {
                "success": True,
                "video_id": video_id,
                "updated_fields": ["title", "description", "tags", "privacy_status"]
            }
            
        except Exception as e:
            logger.error(f"Error updating video metadata: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_upload_status(self, upload_id: str) -> Optional[UploadProgress]:
        """Get upload progress status"""
        return self.active_uploads.get(upload_id)
    
    async def cancel_upload(self, upload_id: str) -> bool:
        """Cancel active upload"""
        try:
            if upload_id in self.active_uploads:
                upload_progress = self.active_uploads[upload_id]
                upload_progress.status = "cancelled"
                del self.active_uploads[upload_id]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error cancelling upload: {str(e)}")
            return False
    
    async def get_video_categories(self) -> List[Dict[str, Any]]:
        """Get available video categories"""
        try:
            # This would use the YouTube API service
            # For now, return common categories
            return [
                {"id": "1", "title": "Film & Animation"},
                {"id": "2", "title": "Autos & Vehicles"},
                {"id": "10", "title": "Music"},
                {"id": "15", "title": "Pets & Animals"},
                {"id": "17", "title": "Sports"},
                {"id": "19", "title": "Travel & Events"},
                {"id": "20", "title": "Gaming"},
                {"id": "22", "title": "People & Blogs"},
                {"id": "23", "title": "Comedy"},
                {"id": "24", "title": "Entertainment"},
                {"id": "25", "title": "News & Politics"},
                {"id": "26", "title": "Howto & Style"},
                {"id": "27", "title": "Education"},
                {"id": "28", "title": "Science & Technology"},
                {"id": "29", "title": "Nonprofits & Activism"}
            ]
            
        except Exception as e:
            logger.error(f"Error getting video categories: {str(e)}")
            return []
    
    async def validate_video_file(self, video_path: str) -> Dict[str, Any]:
        """Validate video file for upload"""
        try:
            if not os.path.exists(video_path):
                return {"valid": False, "error": "File not found"}
            
            # Check file size (max 256GB for YouTube)
            file_size = os.path.getsize(video_path)
            max_size = 256 * 1024 * 1024 * 1024  # 256GB
            
            if file_size > max_size:
                return {"valid": False, "error": "File too large (max 256GB)"}
            
            # Check MIME type
            mime_type = self._get_mime_type(video_path)
            if mime_type not in self.supported_formats:
                return {"valid": False, "error": f"Unsupported format: {mime_type}"}
            
            # Check video duration
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            # Max 12 hours
            if duration > 12 * 3600:
                return {"valid": False, "error": "Video too long (max 12 hours)"}
            
            return {
                "valid": True,
                "file_size": file_size,
                "duration": duration,
                "mime_type": mime_type
            }
            
        except Exception as e:
            logger.error(f"Error validating video file: {str(e)}")
            return {"valid": False, "error": str(e)}
    
    async def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            # Clean up files older than 24 hours
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            for temp_file in self.temp_dir.glob("*"):
                if temp_file.stat().st_mtime < cutoff_time.timestamp():
                    temp_file.unlink()
                    logger.info(f"Cleaned up temp file: {temp_file}")
            
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")

# Global instance
youtube_upload_service = YouTubeUploadService()
