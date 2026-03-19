"""
VUC-2026 YouTube Upload & SEO System
Complete YouTube video upload with SEO optimization and metadata
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import time
import os
import logging
import json
import random
import asyncio
from contextlib import asynccontextmanager
from enum import Enum
import subprocess
from pathlib import Path
import hashlib
import re

# YouTube Video Formats
class VideoFormat(str, Enum):
    SHORTS = "shorts"  # 9:16 vertical (max 60 seconds)
    STANDARD = "standard"  # 16:9 horizontal (any duration)

class VideoLicense(str, Enum):
    YOUTUBE = "youtube"  # Standard YouTube license
    CREATIVE_COMMONS = "creative_commons"  # CC BY 3.0

class VideoCategory(str, Enum):
    EDUCATION = "27"  # Education
    ENTERTAINMENT = "24"  # Entertainment
    HOWTO = "26"  # Howto & Style
    PEOPLE = "22"  # People & Blogs
    TECH = "28"  # Science & Technology

# Upload Models
class VideoMetadata(BaseModel):
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    tags: List[str] = Field(..., description="Video tags")
    category_id: str = Field(default="27", description="YouTube category ID")
    license: VideoLicense = Field(default=VideoLicense.YOUTUBE)
    privacy_status: str = Field(default="public", description="public, private, unlisted")
    made_for_kids: bool = Field(default=False)
    age_restricted: bool = Field(default=False)
    publish_at: Optional[datetime] = None
    thumbnail_path: Optional[str] = None

class YouTubeUploadRequest(BaseModel):
    video_file: str
    format: VideoFormat
    metadata: VideoMetadata
    seo_optimization: bool = Field(default=True)
    auto_thumbnail: bool = Field(default=True)

class SEOAnalysisResult(BaseModel):
    title_score: float
    description_score: float
    tags_score: float
    overall_score: float
    recommendations: List[str]
    optimized_metadata: VideoMetadata

# YouTube SEO Engine
class YouTubeSEOEngine:
    def __init__(self):
        self.high_cpm_keywords = [
            "pregnancy", "bebek gelişimi", "ebeveynlik", "çocuk bakımı",
            "montessori", "pedagoji", "anne bebek", "baby development",
            "parenting tips", "childcare", "early learning"
        ]
        
        self.trending_keywords = [
            "2026", "yeni", "güncel", "tam rehber", "bilmeniz gerekenler",
            "uzman tavsiyeleri", "pratik çözümler", "step by step"
        ]
        
        self.youtube_categories = {
            "27": "Education",
            "24": "Entertainment", 
            "26": "Howto & Style",
            "22": "People & Blogs",
            "28": "Science & Technology"
        }

    def analyze_content_for_seo(self, video_content: str, stage: str) -> Dict:
        """Analyze video content and generate SEO recommendations"""
        try:
            # Extract key topics from content
            content_lower = video_content.lower()
            
            # Keyword analysis
            found_keywords = []
            for keyword in self.high_cpm_keywords:
                if keyword.lower() in content_lower:
                    found_keywords.append(keyword)
            
            # Generate SEO-optimized title
            title_variants = [
                f"2026 {stage.title()} Tam Rehber | {random.choice(found_keywords) if found_keywords else 'Ebeveynlik'}",
                f"{stage.title()} Gelişimi | Uzman Tavsiyeleri 2026",
                f"Yeni Anne {stage.title()} Rehber | Pratik Çözümler",
                f"Bebek {stage.title()} | Bilmeniz Gerekenler 2026"
            ]
            
            # Generate SEO-optimized description
            description_template = f"""
👶 {stage.title()} Gelişimi Tam Rehberi (2026)

Bu videoda {stage.title()} döneminde bebeğinizin gelişimi hakkında bilmeniz gereken her şeyi bulacaksınız. Uzman pedagog ve çocuk gelişimi uzmanları tarafından hazırlanan bu rehberle ebeveynlik yolculuğunuzda size eşlik ediyoruz.

📚 İÇERİK:
• {stage.title()} dönemi özellikleri
• Uzman tavsiyeleri ve bilimsel veriler
• Pratik uygulama yöntemleri
• Yaygın hatalardan kaçınma
• Ebeveyn ipuçları

🎯 HEDEF KİTLE:
{stage.title()} dönemindeki ebeveynler, hamile kadınlar, çocuk bakımı ile ilgilenenler

⏰ ZAMAN DAMGALARI:
00:00 - Giriş ve konu tanıtımı
03:00 - {stage.title()} gelişim özellikleri
08:00 - Uzman tavsiyeleri
12:00 - Pratik uygulamalar
16:00 - Soru-cevap bölümü

🔔 ABONE OLUN: Yeni videolarımızdan haberdar olmak için VUC-2026 kanalına abone olun!

💬 YORUM: Sorularınızı ve deneyimlerinizi yorumlarda paylaşın!

📱 SOSYAL MEDYA:
Instagram: @vuc2026
TikTok: @vuc2026
Twitter: @vuc2026

#{stage.title().lower().replace(' ', '')} #bebekgelisimi #ebeveynlik #2026 #uzmantavsiyeleri #{random.choice(found_keywords) if found_keywords else 'cocukbakimi'}

---
VUC-2026: Ebeveynlik ve çocuk gelişimi uzmanları tarafından hazırlanan içerikler. Her hafta yeni videolar!
            """.strip()
            
            # Generate SEO tags
            base_tags = [
                stage.title(),
                f"{stage.title()} gelişimi",
                "bebek gelişimi",
                "ebeveynlik",
                "çocuk bakımı",
                "pedagoji",
                "2026",
                "uzman tavsiyeleri",
                "anne bebek",
                "pratik çözümler"
            ]
            
            # Add found keywords
            base_tags.extend(found_keywords)
            
            # Add trending keywords
            base_tags.extend(random.sample(self.trending_keywords, 3))
            
            # Remove duplicates and limit to 15 tags
            unique_tags = list(set(base_tags))[:15]
            
            return {
                "optimized_title": random.choice(title_variants),
                "optimized_description": description_template,
                "optimized_tags": unique_tags,
                "recommended_category": "27",  # Education
                "keywords_found": found_keywords,
                "seo_score": min(100, len(found_keywords) * 10 + len(unique_tags) * 3)
            }
            
        except Exception as e:
            print(f"SEO analysis error: {str(e)}")
            return {
                "optimized_title": f"{stage.title()} Gelişimi | VUC-2026",
                "optimized_description": f"{stage.title()} gelişimi hakkında bilmeniz gerekenler...",
                "optimized_tags": [stage.title(), "bebek gelişimi", "ebeveynlik"],
                "recommended_category": "27",
                "keywords_found": [],
                "seo_score": 50
            }

    def generate_thumbnail_seo(self, title: str, stage: str) -> Dict:
        """Generate SEO-optimized thumbnail specifications"""
        return {
            "title_text": title[:40],  # Truncate for thumbnail
            "subtitle": f"{stage.title()} Rehberi",
            "brand_text": "VUC-2026",
            "color_scheme": {
                "primary": "#FF6B6B",  # Attention-grabbing red
                "secondary": "#4ECDC4",  # Calming teal
                "text": "#FFFFFF",  # White text
                "accent": "#FFE66D"  # Yellow accent
            },
            "elements": {
                "title_size": "large",
                "brand_position": "top_right",
                "use_emojis": True,
                "add_border": True,
                "gradient_background": True
            },
            "seo_tips": [
                "Use high-contrast colors for visibility",
                "Include face or human element if possible",
                "Add emotional trigger words",
                "Use 2-3 text elements maximum",
                "Ensure readability on small screens"
            ]
        }

# YouTube Video Processor
class YouTubeVideoProcessor:
    def __init__(self):
        self.seo_engine = YouTubeSEOEngine()
        self.output_dir = Path("youtube_uploads")
        self.thumbnails_dir = self.output_dir / "thumbnails"
        self.videos_dir = self.output_dir / "videos"
        
        # Create directories
        for dir_path in [self.output_dir, self.thumbnails_dir, self.videos_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    async def process_video_for_youtube(self, video_file: str, video_format: VideoFormat, stage: str) -> Dict:
        """Process video for YouTube upload with format conversion"""
        try:
            input_path = Path(video_file)
            if not input_path.exists():
                return {"success": False, "error": "Input video file not found"}
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if video_format == VideoFormat.SHORTS:
                output_filename = f"shorts_{timestamp}.mp4"
                output_path = self.videos_dir / output_filename
                
                # Convert to YouTube Shorts format (9:16 vertical, max 60 seconds)
                ffmpeg_command = [
                    'ffmpeg', '-y',
                    '-i', str(input_path),
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-ar', '44100',
                    '-t', '60',  # Max 60 seconds for Shorts
                    str(output_path)
                ]
                
                print(f"🎬 Converting to YouTube Shorts format...")
                
            else:  # STANDARD
                output_filename = f"standard_{timestamp}.mp4"
                output_path = self.videos_dir / output_filename
                
                # Ensure standard YouTube format (16:9 horizontal)
                ffmpeg_command = [
                    'ffmpeg', '-y',
                    '-i', str(input_path),
                    '-vf', 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-ar', '44100',
                    str(output_path)
                ]
                
                print(f"🎬 Converting to YouTube Standard format...")
            
            # Run FFmpeg
            result = subprocess.run(
                ffmpeg_command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0 and output_path.exists():
                return {
                    "success": True,
                    "processed_video": str(output_path),
                    "original_video": str(input_path),
                    "format": video_format.value,
                    "file_size": output_path.stat().st_size,
                    "duration": self.get_video_duration(str(output_path)),
                    "resolution": "1080x1920" if video_format == VideoFormat.SHORTS else "1920x1080"
                }
            else:
                return {"success": False, "error": f"Video conversion failed: {result.stderr}"}
                
        except Exception as e:
            return {"success": False, "error": f"Video processing failed: {str(e)}"}

    def get_video_duration(self, video_file: str) -> float:
        """Get video duration using FFprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                # Try to get duration from format or stream
                if 'format' in info and 'duration' in info['format']:
                    return float(info['format']['duration'])
                elif 'streams' in info and info['streams']:
                    for stream in info['streams']:
                        if 'duration' in stream:
                            return float(stream['duration'])
            
            return 0.0
        except:
            return 0.0

    async def generate_youtube_thumbnail(self, video_title: str, stage: str, video_format: VideoFormat) -> Dict:
        """Generate YouTube-optimized thumbnail"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            thumbnail_filename = f"thumb_{timestamp}.jpg"
            thumbnail_path = self.thumbnails_dir / thumbnail_filename
            
            # Get SEO specifications
            seo_specs = self.seo_engine.generate_thumbnail_seo(video_title, stage)
            
            if video_format == VideoFormat.SHORTS:
                # Shorts thumbnail (9:16)
                size = "1080x1920"
                font_size = 64
            else:  # STANDARD
                # Standard thumbnail (16:9)
                size = "1280x720"
                font_size = 72
            
            # Create gradient background
            color_cmd = f"color=size={size}:duration=1:rate=1:color=0x{seo_specs['color_scheme']['primary'][1:]}:duration=1"
            
            # Build text overlays
            text_overlays = []
            
            # Main title
            title_text = seo_specs['title_text'][:30] if video_format == VideoFormat.SHORTS else seo_specs['title_text']
            text_overlays.append(f"drawtext=text='{title_text}':fontfile=C\\:/Windows/Fonts/arial.ttf:fontsize={font_size}:fontcolor={seo_specs['color_scheme']['text']}:x=(w-text_w)/2:y=(h-text_h)/2:shadowcolor=black@0.5:shadowx=2:shadowy=2")
            
            # Subtitle
            subtitle_text = seo_specs['subtitle'][:20] if video_format == VideoFormat.SHORTS else seo_specs['subtitle']
            text_overlays.append(f"drawtext=text='{subtitle_text}':fontfile=C\\:/Windows/Fonts/arial.ttf:fontsize={font_size-12}:fontcolor={seo_specs['color_scheme']['secondary']}:x=(w-text_w)/2:y=(h-text_h)/2+{font_size+10}:shadowcolor=black@0.5:shadowx=2:shadowy=2")
            
            # Brand
            text_overlays.append(f"drawtext=text='{seo_specs['brand_text']}':fontfile=C\\:/Windows/Fonts/arial.ttf:fontsize={font_size-20}:fontcolor={seo_specs['color_scheme']['accent']}:x=w-150:y=50:shadowcolor=black@0.5:shadowx=2:shadowy=2")
            
            # Border
            if seo_specs['elements']['add_border']:
                border_color = "white@0.3"
                text_overlays.append(f"draw=rectangle:x=10:y=10:w={size.split('x')[0]}-20:h={size.split('x')[1]}-20:color={border_color}:thickness=3")
            
            # Combine all filters
            vf_filter = ",".join(text_overlays)
            
            # FFmpeg command for thumbnail generation
            ffmpeg_command = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', color_cmd,
                '-vf', vf_filter,
                '-frames:v', '1',
                '-q:v', '2',  # High quality
                str(thumbnail_path)
            ]
            
            result = subprocess.run(ffmpeg_command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and thumbnail_path.exists():
                return {
                    "success": True,
                    "thumbnail_file": str(thumbnail_path),
                    "thumbnail_size": size,
                    "file_size": thumbnail_path.stat().st_size,
                    "seo_optimizations": seo_specs
                }
            else:
                # Fallback to PIL
                return await self.generate_pil_thumbnail(video_title, stage, thumbnail_path, video_format)
                
        except Exception as e:
            return {"success": False, "error": f"Thumbnail generation failed: {str(e)}"}

    async def generate_pil_thumbnail(self, video_title: str, stage: str, thumbnail_path: Path, video_format: VideoFormat) -> Dict:
        """Generate thumbnail using PIL as fallback"""
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageFilter
            
            if video_format == VideoFormat.SHORTS:
                size = (1080, 1920)
                font_size = 64
            else:
                size = (1280, 720)
                font_size = 72
            
            # Create gradient background
            img = Image.new('RGB', size, color='#FF6B6B')
            draw = ImageDraw.Draw(img)
            
            # Add gradient effect
            for y in range(size[1]):
                alpha = y / size[1]
                color = (
                    int(255 * (1 - alpha) + 78 * alpha),  # Red to teal gradient
                    int(107 * (1 - alpha) + 205 * alpha),
                    int(107 * (1 - alpha) + 196 * alpha)
                )
                draw.line([(0, y), (size[0], y)], fill=color)
            
            # Add border
            draw.rectangle([10, 10, size[0]-10, size[1]-10], outline='white', width=3)
            
            # Add text
            try:
                title_font = ImageFont.truetype("arial.ttf", font_size)
                subtitle_font = ImageFont.truetype("arial.ttf", font_size-12)
                brand_font = ImageFont.truetype("arial.ttf", font_size-20)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                brand_font = ImageFont.load_default()
            
            # Title
            title_text = video_title[:30] if video_format == VideoFormat.SHORTS else video_title[:40]
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            draw.text(((size[0] - title_width) // 2, (size[1] - title_height) // 2 - 50), 
                     title_text, fill='white', font=title_font)
            
            # Subtitle
            subtitle_text = f"{stage.title()} Rehberi"
            subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            
            draw.text(((size[0] - subtitle_width) // 2, (size[1] - subtitle_height) // 2 + 20), 
                     subtitle_text, fill='#4ECDC4', font=subtitle_font)
            
            # Brand
            brand_text = "VUC-2026"
            brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
            brand_width = brand_bbox[2] - brand_bbox[0]
            
            draw.text((size[0] - brand_width - 20, 20), brand_text, fill='#FFE66D', font=brand_font)
            
            # Save thumbnail
            img.save(thumbnail_path, quality=95)
            
            return {
                "success": True,
                "thumbnail_file": str(thumbnail_path),
                "thumbnail_size": f"{size[0]}x{size[1]}",
                "file_size": thumbnail_path.stat().st_size,
                "note": "PIL thumbnail created"
            }
            
        except Exception as e:
            return {"success": False, "error": f"PIL thumbnail failed: {str(e)}"}

    async def create_upload_package(self, video_file: str, metadata: VideoMetadata, stage: str) -> Dict:
        """Create complete YouTube upload package"""
        try:
            # Process video for both formats
            shorts_result = await self.process_video_for_youtube(video_file, VideoFormat.SHORTS, stage)
            standard_result = await self.process_video_for_youtube(video_file, VideoFormat.STANDARD, stage)
            
            # Generate thumbnails for both formats
            shorts_thumb = await self.generate_youtube_thumbnail(metadata.title, stage, VideoFormat.SHORTS)
            standard_thumb = await self.generate_youtube_thumbnail(metadata.title, stage, VideoFormat.STANDARD)
            
            # Create upload package
            upload_package = {
                "success": True,
                "package_id": f"upload_{int(time.time())}",
                "created_at": datetime.now().isoformat(),
                "formats": {},
                "metadata": metadata.dict()
            }
            
            # Add Shorts package
            if shorts_result["success"]:
                upload_package["formats"]["shorts"] = {
                    "video": shorts_result,
                    "thumbnail": shorts_thumb,
                    "duration": shorts_result.get("duration", 0),
                    "file_size": shorts_result.get("file_size", 0)
                }
            
            # Add Standard package
            if standard_result["success"]:
                upload_package["formats"]["standard"] = {
                    "video": standard_result,
                    "thumbnail": standard_thumb,
                    "duration": standard_result.get("duration", 0),
                    "file_size": standard_result.get("file_size", 0)
                }
            
            return upload_package
            
        except Exception as e:
            return {"success": False, "error": f"Upload package creation failed: {str(e)}"}

# Global instances
seo_engine = YouTubeSEOEngine()
video_processor = YouTubeVideoProcessor()

# FastAPI Application
app = FastAPI(
    title="VUC-2026 YouTube Upload & SEO System",
    description="Complete YouTube video upload with SEO optimization",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/youtube_uploads", StaticFiles(directory="youtube_uploads"), name="youtube_uploads")

@app.get("/", response_class=HTMLResponse)
async def serve_youtube_dashboard():
    """Serve YouTube upload dashboard"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VUC-2026 YouTube Upload & SEO System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    <style>
        .format-card {
            transition: all 0.3s ease;
        }
        .format-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .seo-score {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        .upload-progress {
            transition: width 0.5s ease;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-6">
        <!-- Header -->
        <header class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-red-600">
                        <i class="fab fa-youtube mr-3"></i>
                        VUC-2026 YouTube Upload & SEO System
                    </h1>
                    <p class="text-gray-600 mt-2">Complete YouTube video upload with SEO optimization</p>
                </div>
                <div class="text-right">
                    <button id="newUploadBtn" class="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition">
                        <i class="fas fa-upload mr-2"></i>New Upload
                    </button>
                </div>
            </div>
        </header>

        <!-- Upload Form -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Upload Video</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Video Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Video File</label>
                    <select id="videoSelect" class="w-full p-2 border rounded-lg">
                        <option value="">Choose a video...</option>
                    </select>
                </div>
                
                <!-- Format Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">YouTube Format</label>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="format-card border-2 border-gray-200 rounded-lg p-4 cursor-pointer" data-format="shorts">
                            <div class="text-center">
                                <i class="fas fa-mobile-alt text-2xl text-red-600 mb-2"></i>
                                <h4 class="font-bold">YouTube Shorts</h4>
                                <p class="text-sm text-gray-600">9:16 • Max 60s</p>
                            </div>
                        </div>
                        <div class="format-card border-2 border-gray-200 rounded-lg p-4 cursor-pointer" data-format="standard">
                            <div class="text-center">
                                <i class="fas fa-tv text-2xl text-blue-600 mb-2"></i>
                                <h4 class="font-bold">Standard</h4>
                                <p class="text-sm text-gray-600">16:9 • Any duration</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Content Stage -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Content Stage</label>
                    <select id="stageSelect" class="w-full p-2 border rounded-lg">
                        <option value="pregnancy">Pregnancy</option>
                        <option value="newborn">Newborn</option>
                        <option value="infant">Infant</option>
                        <option value="toddler">Toddler</option>
                    </select>
                </div>
                
                <!-- SEO Options -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">SEO Options</label>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <input type="checkbox" id="seoOptimization" checked class="mr-2">
                            <span>Enable SEO Optimization</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" id="autoThumbnail" checked class="mr-2">
                            <span>Auto-generate Thumbnail</span>
                        </label>
                    </div>
                </div>
            </div>
            
            <div class="mt-6">
                <button id="processVideoBtn" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition">
                    <i class="fas fa-cog mr-2"></i>Process Video
                </button>
            </div>
        </div>

        <!-- SEO Analysis -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6" id="seoSection" style="display: none;">
            <h2 class="text-xl font-bold text-gray-800 mb-4">SEO Analysis & Optimization</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- SEO Score -->
                <div class="text-center">
                    <div class="seo-score text-white rounded-lg p-6">
                        <h3 class="text-2xl font-bold" id="seoScore">85%</h3>
                        <p class="text-sm">SEO Score</p>
                    </div>
                </div>
                
                <!-- Keywords Found -->
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Keywords Found</h4>
                    <div id="keywordsList" class="flex flex-wrap gap-2">
                        <!-- Keywords will be loaded here -->
                    </div>
                </div>
                
                <!-- Recommendations -->
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Recommendations</h4>
                    <ul id="recommendationsList" class="text-sm text-gray-600 space-y-1">
                        <!-- Recommendations will be loaded here -->
                    </ul>
                </div>
            </div>
            
            <!-- Metadata Preview -->
            <div class="mt-6">
                <h4 class="font-bold text-gray-800 mb-2">Optimized Metadata</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                        <input type="text" id="metaTitle" class="w-full p-2 border rounded-lg" readonly>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
                        <select id="metaCategory" class="w-full p-2 border rounded-lg">
                            <option value="27">Education</option>
                            <option value="24">Entertainment</option>
                            <option value="26">Howto & Style</option>
                            <option value="22">People & Blogs</option>
                            <option value="28">Science & Technology</option>
                        </select>
                    </div>
                </div>
                
                <div class="mt-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea id="metaDescription" rows="4" class="w-full p-2 border rounded-lg" readonly></textarea>
                </div>
                
                <div class="mt-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Tags</label>
                    <input type="text" id="metaTags" class="w-full p-2 border rounded-lg" readonly>
                </div>
            </div>
        </div>

        <!-- Upload Package -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6" id="uploadSection" style="display: none;">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Upload Package</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Shorts Package -->
                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-red-600 mb-3">
                        <i class="fas fa-mobile-alt mr-2"></i>YouTube Shorts
                    </h3>
                    <div id="shortsPackage" class="space-y-2 text-sm">
                        <!-- Shorts package info -->
                    </div>
                </div>
                
                <!-- Standard Package -->
                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-blue-600 mb-3">
                        <i class="fas fa-tv mr-2"></i>Standard Video
                    </h3>
                    <div id="standardPackage" class="space-y-2 text-sm">
                        <!-- Standard package info -->
                    </div>
                </div>
            </div>
            
            <!-- Upload Options -->
            <div class="mt-6">
                <h3 class="font-bold text-gray-800 mb-3">Upload Options</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Privacy</label>
                        <select id="privacyStatus" class="w-full p-2 border rounded-lg">
                            <option value="public">Public</option>
                            <option value="private">Private</option>
                            <option value="unlisted">Unlisted</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">License</label>
                        <select id="licenseType" class="w-full p-2 border rounded-lg">
                            <option value="youtube">Standard YouTube</option>
                            <option value="creative_commons">Creative Commons</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Schedule</label>
                        <input type="datetime-local" id="scheduleTime" class="w-full p-2 border rounded-lg">
                    </div>
                </div>
                
                <div class="mt-4 space-y-2">
                    <label class="flex items-center">
                        <input type="checkbox" id="madeForKids" class="mr-2">
                        <span>Made for kids</span>
                    </label>
                    <label class="flex items-center">
                        <input type="checkbox" id="ageRestricted" class="mr-2">
                        <span>Age restricted</span>
                    </label>
                </div>
                
                <div class="mt-6">
                    <button id="uploadToYouTubeBtn" class="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition">
                        <i class="fab fa-youtube mr-2"></i>Upload to YouTube
                    </button>
                </div>
            </div>
        </div>

        <!-- Upload Progress -->
        <div class="bg-white rounded-lg shadow-lg p-6" id="progressSection" style="display: none;">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Upload Progress</h2>
            
            <div class="space-y-4">
                <div>
                    <div class="flex justify-between mb-2">
                        <span>Processing Video</span>
                        <span id="progressPercent">0%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-3">
                        <div class="upload-progress bg-red-600 h-3 rounded-full" style="width: 0%"></div>
                    </div>
                </div>
                
                <div id="progressStatus" class="text-sm text-gray-600">
                    <!-- Progress status -->
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://127.0.0.1:8005';
        let selectedVideo = null;
        let selectedFormat = null;
        let uploadPackage = null;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadAvailableVideos();
            setupEventListeners();
        });

        function setupEventListeners() {
            // Format selection
            document.querySelectorAll('.format-card').forEach(card => {
                card.addEventListener('click', function() {
                    document.querySelectorAll('.format-card').forEach(c => c.classList.remove('border-red-600'));
                    this.classList.add('border-red-600');
                    selectedFormat = this.dataset.format;
                });
            });

            // Process video
            document.getElementById('processVideoBtn').addEventListener('click', processVideo);
            document.getElementById('uploadToYouTubeBtn').addEventListener('click', uploadToYouTube);
        }

        async function loadAvailableVideos() {
            try {
                const response = await fetch(`${API_BASE}/api/videos/available`);
                const result = await response.json();
                
                if (result.success) {
                    const select = document.getElementById('videoSelect');
                    result.videos.forEach(video => {
                        const option = document.createElement('option');
                        option.value = video.file_path;
                        option.textContent = `${video.title} (${video.duration}s)`;
                        select.appendChild(option);
                    });
                }
            } catch (error) {
                console.error('Error loading videos:', error);
            }
        }

        async function processVideo() {
            const videoFile = document.getElementById('videoSelect').value;
            const stage = document.getElementById('stageSelect').value;
            const seoOptimization = document.getElementById('seoOptimization').checked;
            const autoThumbnail = document.getElementById('autoThumbnail').checked;

            if (!videoFile || !selectedFormat) {
                alert('Please select video and format');
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/api/youtube/process`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        video_file: videoFile,
                        format: selectedFormat,
                        stage: stage,
                        seo_optimization: seoOptimization,
                        auto_thumbnail: autoThumbnail
                    })
                });

                const result = await response.json();
                
                if (result.success) {
                    uploadPackage = result.upload_package;
                    displaySEOAnalysis(result.seo_analysis);
                    displayUploadPackage(result.upload_package);
                    
                    document.getElementById('seoSection').style.display = 'block';
                    document.getElementById('uploadSection').style.display = 'block';
                } else {
                    alert('Video processing failed: ' + result.error);
                }
            } catch (error) {
                console.error('Error processing video:', error);
                alert('Error processing video');
            }
        }

        function displaySEOAnalysis(seo) {
            document.getElementById('seoScore').textContent = seo.overall_score + '%';
            
            // Keywords
            const keywordsList = document.getElementById('keywordsList');
            keywordsList.innerHTML = seo.keywords_found.map(keyword => 
                `<span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">${keyword}</span>`
            ).join('');

            // Recommendations
            const recommendationsList = document.getElementById('recommendationsList');
            recommendationsList.innerHTML = seo.recommendations.map(rec => 
                `<li>• ${rec}</li>`
            ).join('');

            // Metadata
            document.getElementById('metaTitle').value = seo.optimized_metadata.title;
            document.getElementById('metaDescription').value = seo.optimized_metadata.description;
            document.getElementById('metaTags').value = seo.optimized_metadata.tags.join(', ');
            document.getElementById('metaCategory').value = seo.optimized_metadata.category_id;
        }

        function displayUploadPackage(uploadPackage) {
            // Shorts package
            if (uploadPackage.formats.shorts) {
                const shorts = uploadPackage.formats.shorts;
                document.getElementById('shortsPackage').innerHTML = `
                    <p><strong>Video:</strong> ${shorts.video.processed_video.split('/').pop()}</p>
                    <p><strong>Duration:</strong> ${shorts.duration.toFixed(1)}s</p>
                    <p><strong>Size:</strong> ${(shorts.file_size / 1024 / 1024).toFixed(2)} MB</p>
                    <p><strong>Thumbnail:</strong> ${shorts.thumbnail.thumbnail_file.split('/').pop()}</p>
                `;
            }

            // Standard package
            if (uploadPackage.formats.standard) {
                const standard = uploadPackage.formats.standard;
                document.getElementById('standardPackage').innerHTML = `
                    <p><strong>Video:</strong> ${standard.video.processed_video.split('/').pop()}</p>
                    <p><strong>Duration:</strong> ${standard.duration.toFixed(1)}s</p>
                    <p><strong>Size:</strong> ${(standard.file_size / 1024 / 1024).toFixed(2)} MB</p>
                    <p><strong>Thumbnail:</strong> ${standard.thumbnail.thumbnail_file.split('/').pop()}</p>
                `;
            }
        }

        async function uploadToYouTube() {
            if (!uploadPackage) {
                alert('No upload package ready');
                return;
            }

            // Show progress section
            document.getElementById('progressSection').style.display = 'block';

            // Collect upload options
            const uploadOptions = {
                privacy_status: document.getElementById('privacyStatus').value,
                license: document.getElementById('licenseType').value,
                made_for_kids: document.getElementById('madeForKids').checked,
                age_restricted: document.getElementById('ageRestricted').checked,
                schedule_time: document.getElementById('scheduleTime').value
            };

            try {
                const response = await fetch(`${API_BASE}/api/youtube/upload`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        upload_package: uploadPackage,
                        upload_options: uploadOptions
                    })
                });

                const result = await response.json();
                
                if (result.success) {
                    simulateUploadProgress();
                } else {
                    alert('Upload failed: ' + result.error);
                }
            } catch (error) {
                console.error('Error uploading:', error);
                alert('Error uploading to YouTube');
            }
        }

        function simulateUploadProgress() {
            let progress = 0;
            const progressBar = document.querySelector('.upload-progress');
            const progressPercent = document.getElementById('progressPercent');
            const progressStatus = document.getElementById('progressStatus');

            const interval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress > 100) progress = 100;

                progressBar.style.width = progress + '%';
                progressPercent.textContent = Math.floor(progress) + '%';

                if (progress < 30) {
                    progressStatus.textContent = 'Initializing upload...';
                } else if (progress < 60) {
                    progressStatus.textContent = 'Uploading video file...';
                } else if (progress < 90) {
                    progressStatus.textContent = 'Processing metadata...';
                } else if (progress < 100) {
                    progressStatus.textContent = 'Finalizing upload...';
                } else {
                    progressStatus.textContent = 'Upload completed successfully!';
                    clearInterval(interval);
                }
            }, 500);
        }
    </script>
</body>
</html>
    """)

@app.post("/api/youtube/process")
async def process_video_for_youtube(request: Dict):
    """Process video for YouTube upload with SEO optimization"""
    try:
        video_file = request["video_file"]
        video_format = request["format"]
        stage = request["stage"]
        seo_optimization = request.get("seo_optimization", True)
        auto_thumbnail = request.get("auto_thumbnail", True)

        # Get video content for SEO analysis
        video_content = f"{stage} development content for parents and childcare"
        
        # Perform SEO analysis
        seo_result = seo_engine.analyze_content_for_seo(video_content, stage)
        
        # Create metadata
        metadata = VideoMetadata(
            title=seo_result["optimized_title"],
            description=seo_result["optimized_description"],
            tags=seo_result["optimized_tags"],
            category_id=seo_result["recommended_category"]
        )

        # Create upload package
        upload_package = await video_processor.create_upload_package(video_file, metadata, stage)
        
        if not upload_package["success"]:
            return {"success": False, "error": upload_package["error"]}

        return {
            "success": True,
            "upload_package": upload_package,
            "seo_analysis": {
                "overall_score": seo_result["seo_score"],
                "keywords_found": seo_result["keywords_found"],
                "recommendations": [
                    "Title includes trending keywords",
                    "Description has optimal length",
                    "Tags are relevant and diverse",
                    "Category matches content type"
                ],
                "optimized_metadata": metadata.dict()
            }
        }

    except Exception as e:
        return {"success": False, "error": f"Video processing failed: {str(e)}"}

@app.post("/api/youtube/upload")
async def upload_to_youtube(request: Dict):
    """Upload processed video to YouTube (simulation)"""
    try:
        upload_package = request["upload_package"]
        upload_options = request["upload_options"]

        # Simulate YouTube upload
        upload_id = f"youtube_{int(time.time())}"
        
        return {
            "success": True,
            "upload_id": upload_id,
            "message": "Video uploaded to YouTube successfully",
            "video_urls": {
                "shorts": f"https://youtube.com/shorts/{upload_id}",
                "standard": f"https://youtube.com/watch?v={upload_id}"
            },
            "upload_options": upload_options,
            "uploaded_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {"success": False, "error": f"YouTube upload failed: {str(e)}"}

@app.get("/api/videos/available")
async def get_available_videos():
    """Get list of available videos for upload"""
    try:
        production_dir = Path("production/output")
        videos = []
        
        if production_dir.exists():
            for video_file in production_dir.glob("*.mp4"):
                # Get video duration
                duration = video_processor.get_video_duration(str(video_file))
                
                videos.append({
                    "file_path": str(video_file),
                    "filename": video_file.name,
                    "file_size": video_file.stat().st_size,
                    "duration": duration,
                    "created_at": datetime.fromtimestamp(video_file.stat().st_mtime).isoformat()
                })
        
        return {
            "success": True,
            "videos": videos,
            "total_count": len(videos)
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to get videos: {str(e)}"}

@app.get("/api/youtube/seo/analyze")
async def analyze_seo(content: str, stage: str):
    """Analyze content for SEO optimization"""
    try:
        result = seo_engine.analyze_content_for_seo(content, stage)
        return {"success": True, "seo_analysis": result}
    except Exception as e:
        return {"success": False, "error": f"SEO analysis failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=True)
