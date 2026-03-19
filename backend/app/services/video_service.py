"""
VUC-2026 Video Service
Business logic with strict typing and error handling
"""

from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
import logging

from ..models.video import Video
from ..schemas.core import VideoCreateRequest, VideoResponse, VideoStatus, UploadStatus
from ..core.error_handler import VUCException, DatabaseError


class VideoService:
    """Video business logic service - SWE 1.5 Standards"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    async def get_videos(
        self,
        page: int = 1,
        size: int = 10,
        channel_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> Tuple[List[VideoResponse], int]:
        """Get videos with pagination and filtering"""
        try:
            query = self.db.query(Video)
            
            # Apply filters
            if channel_id:
                query = query.filter(Video.channel_id == channel_id)
            
            if status:
                try:
                    status_enum = VideoStatus(status)
                    query = query.filter(Video.status == status_enum)
                except ValueError:
                    raise VUCException(
                        message=f"Geçersiz durum: {status}",
                        error_code="INVALID_STATUS",
                        severity="low"
                    )
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * size
            videos = query.order_by(desc(Video.created_at)).offset(offset).limit(size).all()
            
            # Convert to response models
            video_responses = [VideoResponse.model_validate(video) for video in videos]
            
            return video_responses, total
            
        except VUCException:
            raise
        except Exception as e:
            self.logger.error(f"Video listesi alma hatası: {e}")
            raise DatabaseError(f"Video listesi alınamadı: {str(e)}")
    
    async def create_video(self, video_data: VideoCreateRequest) -> VideoResponse:
        """Create new video with validation"""
        try:
            # Check if channel exists (simplified)
            from ..models.channel import Channel
            channel = self.db.query(Channel).filter(Channel.id == video_data.channel_id).first()
            if not channel:
                raise VUCException(
                    message=f"Kanal bulunamadı: {video_data.channel_id}",
                    error_code="CHANNEL_NOT_FOUND",
                    severity="medium"
                )
            
            # Create video record
            video = Video(
                channel_id=video_data.channel_id,
                title=video_data.title,
                description=video_data.description,
                tags=video_data.tags,
                category=video_data.category,
                language=video_data.language,
                script_id=video_data.script_id,
                status=VideoStatus.PLANNING,
                upload_status=UploadStatus.DRAFT
            )
            
            self.db.add(video)
            self.db.commit()
            self.db.refresh(video)
            
            return VideoResponse.model_validate(video)
            
        except VUCException:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Video oluşturma hatası: {e}")
            raise DatabaseError(f"Video oluşturulamadı: {str(e)}")
    
    async def get_video_by_id(self, video_id: int) -> Optional[VideoResponse]:
        """Get video by ID"""
        try:
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if video:
                return VideoResponse.model_validate(video)
            return None
            
        except Exception as e:
            self.logger.error(f"Video detayları alma hatası: {e}")
            raise DatabaseError(f"Video detayları alınamadı: {str(e)}")
    
    async def update_video(self, video_id: int, video_data: VideoCreateRequest) -> Optional[VideoResponse]:
        """Update video with validation"""
        try:
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if not video:
                return None
            
            # Update fields
            video.title = video_data.title
            video.description = video_data.description
            video.tags = video_data.tags
            video.category = video_data.category
            video.language = video_data.language
            video.script_id = video_data.script_id
            
            self.db.commit()
            self.db.refresh(video)
            
            return VideoResponse.model_validate(video)
            
        except VUCException:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Video güncelleme hatası: {e}")
            raise DatabaseError(f"Video güncellenemedi: {str(e)}")
    
    async def delete_video(self, video_id: int) -> bool:
        """Delete video safely"""
        try:
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if not video:
                return False
            
            # Check if video is published (prevent deletion of published videos)
            if video.upload_status == UploadStatus.PUBLISHED:
                raise VUCException(
                    message="Yayınlanmış videolar silinemez",
                    error_code="CANNOT_DELETE_PUBLISHED",
                    severity="medium"
                )
            
            self.db.delete(video)
            self.db.commit()
            
            return True
            
        except VUCException:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Video silme hatası: {e}")
            raise DatabaseError(f"Video silinemedi: {str(e)}")
    
    async def update_video_status(self, video_id: int, status: VideoStatus) -> Optional[VideoResponse]:
        """Update video status"""
        try:
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if not video:
                return None
            
            video.status = status
            self.db.commit()
            self.db.refresh(video)
            
            return VideoResponse.model_validate(video)
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Video durum güncelleme hatası: {e}")
            raise DatabaseError(f"Video durumu güncellenemedi: {str(e)}")
    
    async def get_videos_by_status(self, status: VideoStatus, limit: int = 50) -> List[VideoResponse]:
        """Get videos by status"""
        try:
            videos = self.db.query(Video).filter(
                Video.status == status
            ).order_by(desc(Video.created_at)).limit(limit).all()
            
            return [VideoResponse.model_validate(video) for video in videos]
            
        except Exception as e:
            self.logger.error(f"Duruma göre video listesi alma hatası: {e}")
            raise DatabaseError(f"Video listesi alınamadı: {str(e)}")
