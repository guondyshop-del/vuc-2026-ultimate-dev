"""
VUC-2026 Video Rendering API
Otomatik video render için endpoint'ler
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import os
from datetime import datetime

from ..database import get_db
from ..services.video_rendering_service import VideoRenderingService

logger = logging.getLogger(__name__)
router = APIRouter()

class VideoRenderRequest(BaseModel):
    script_data: Dict[str, Any]
    video_config: Dict[str, Any]
    media_assets: Optional[Dict[str, Any]] = None
    apply_shadowban_protection: bool = True
    generate_thumbnail: bool = True
    render_quality: str = "high"  # low, medium, high, ultra

class VideoRenderResponse(BaseModel):
    success: bool
    render_id: Optional[str] = None
    video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    duration: Optional[int] = None
    resolution: Optional[str] = None
    file_size: Optional[int] = None
    processing_time: Optional[float] = None
    message: str

class ThumbnailRequest(BaseModel):
    video_path: str
    title: str
    style: str = "default"
    text_overlay: bool = True

@router.post("/render", response_model=VideoRenderResponse)
async def render_video(
    request: VideoRenderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> VideoRenderResponse:
    """Video render et"""
    try:
        start_time = datetime.now()
        
        # Render servisini başlat
        render_service = VideoRenderingService()
        
        # Video konfigürasyonunu ayarla
        video_config = request.video_config.copy()
        
        # Kalite ayarları
        quality_settings = {
            "low": {"resolution": "854x480", "fps": 24, "crf": 28},
            "medium": {"resolution": "1280x720", "fps": 30, "crf": 25},
            "high": {"resolution": "1920x1080", "fps": 30, "crf": 23},
            "ultra": {"resolution": "3840x2160", "fps": 60, "crf": 20}
        }
        
        quality = quality_settings.get(request.render_quality, quality_settings["high"])
        video_config.update(quality)
        
        # Video render et
        render_result = await render_service.render_video(
            script_data=request.script_data,
            video_config=video_config,
            media_assets=request.media_assets
        )
        
        if not render_result.get("success"):
            raise HTTPException(status_code=500, detail=render_result.get("error", "Render başarısız"))
        
        # Thumbnail oluştur
        thumbnail_path = None
        if request.generate_thumbnail:
            try:
                title = request.script_data.get("title", "Video")
                thumbnail_path = await render_service.create_thumbnail(
                    video_path=render_result["video_path"],
                    title=title,
                    style="hormozi"
                )
            except Exception as e:
                logger.error(f"Thumbnail creation failed: {e}")
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Temizlik task'ı ekle
        render_id = render_result.get("render_id")
        if render_id:
            background_tasks.add_task(render_service.cleanup_temp_files, render_id)
        
        return VideoRenderResponse(
            success=True,
            render_id=render_result.get("render_id"),
            video_path=render_result.get("video_path"),
            thumbnail_path=thumbnail_path,
            duration=render_result.get("duration"),
            resolution=render_result.get("resolution"),
            file_size=render_result.get("file_size"),
            processing_time=processing_time,
            message="Video başarıyla render edildi"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video render error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thumbnail")
async def create_thumbnail(
    request: ThumbnailRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Thumbnail oluştur"""
    try:
        render_service = VideoRenderingService()
        
        # Video path kontrolü
        if not os.path.exists(request.video_path):
            raise HTTPException(status_code=404, detail="Video dosyası bulunamadı")
        
        # Thumbnail oluştur
        thumbnail_path = await render_service.create_thumbnail(
            video_path=request.video_path,
            title=request.title,
            style=request.style
        )
        
        return {
            "success": True,
            "thumbnail_path": thumbnail_path,
            "title": request.title,
            "style": request.style,
            "created_at": datetime.utcnow().isoformat(),
            "message": "Thumbnail başarıyla oluşturuldu"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Thumbnail creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_video_templates() -> Dict[str, Any]:
    """Video şablonlarını getir"""
    try:
        templates = {
            "hormozi_style": {
                "name": "Hormozi Stili",
                "description": "Enerjik, hızlı kesimler, bold metinler",
                "duration_range": [8, 15],
                "features": [
                    "Hızlı kesimler",
                    "Bold altyazılar",
                    "Enerjik müzik",
                    "Dikkat çekici thumbnail'lar"
                ],
                "best_for": ["eğitim", "listicle", "nasıl yapılır"],
                "config": {
                    "resolution": "1920x1080",
                    "fps": 30,
                    "text_style": "bold_hormozi",
                    "music_energy": "high"
                }
            },
            "documentary_style": {
                "name": "Belgesel Stili",
                "description": "Profesyonel, yavaş tempo, derinlemesine analiz",
                "duration_range": [15, 30],
                "features": [
                    "Sinematik çekimler",
                    "Profesyonel ses",
                    "Araştırma odaklı",
                    "Uzman görüşleri"
                ],
                "best_for": ["belgesel", "analiz", "derinlemesine"],
                "config": {
                    "resolution": "1920x1080",
                    "fps": 24,
                    "text_style": "professional",
                    "music_energy": "medium"
                }
            },
            "viral_style": {
                "name": "Viral Stili",
                "description": "Trend odaklı, sosyal medya uyumlu",
                "duration_range": [30, 60],
                "features": [
                    "Trend müzikler",
                    "Hızlı montaj",
                    "Sosyal medya formatı",
                    "Paylaşım odaklı"
                ],
                "best_for": ["shorts", "tiktok", "viral"],
                "config": {
                    "resolution": "1080x1920",  # Vertical
                    "fps": 30,
                    "text_style": "viral",
                    "music_energy": "very_high"
                }
            },
            "educational_style": {
                "name": "Eğitim Stili",
                "description": "Bilgi odaklı, anlaşılır, öğretici",
                "duration_range": [10, 20],
                "features": [
                    "Ekran kayıtları",
                    "Adım adım anlatım",
                    "Bilgi grafikleri",
                    "Örnekler"
                ],
                "best_for": ["eğitim", "nasıl yapılır", "rehber"],
                "config": {
                    "resolution": "1920x1080",
                    "fps": 30,
                    "text_style": "educational",
                    "music_energy": "low"
                }
            }
        }
        
        return {
            "success": True,
            "templates": templates,
            "total_templates": len(templates),
            "message": "Video şablonları başarıyla alındı"
        }
        
    except Exception as e:
        logger.error(f"Video templates error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/render-status/{render_id}")
async def get_render_status(render_id: str) -> Dict[str, Any]:
    """Render durumunu kontrol et"""
    try:
        # Mock render status
        status_data = {
            "render_id": render_id,
            "status": "completed",
            "progress": 100,
            "current_stage": "completed",
            "estimated_time_remaining": 0,
            "processing_time": 45.2,
            "stages": {
                "script_parsing": {"completed": True, "duration": 2.1},
                "media_preparation": {"completed": True, "duration": 8.5},
                "video_segments": {"completed": True, "duration": 15.3},
                "merging": {"completed": True, "duration": 12.8},
                "audio_addition": {"completed": True, "duration": 3.2},
                "subtitles": {"completed": True, "duration": 2.1},
                "shadowban_protection": {"completed": True, "duration": 1.2}
            },
            "output_files": {
                "video": f"outputs/videos/protected_{render_id}.mp4",
                "thumbnail": f"outputs/videos/thumbnail_{render_id}.jpg"
            },
            "created_at": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "render_status": status_data,
            "message": "Render durumu başarıyla alındı"
        }
        
    except Exception as e:
        logger.error(f"Render status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queue")
async def get_render_queue() -> Dict[str, Any]:
    """Render kuyruğunu getir"""
    try:
        # Mock queue data
        queue_data = {
            "active_jobs": [
                {
                    "render_id": "render_1640000000",
                    "status": "processing",
                    "progress": 65,
                    "started_at": "2024-01-15T14:30:00Z",
                    "estimated_completion": "2024-01-15T14:35:00Z",
                    "script_title": "10 Teknoloji Mitleri"
                }
            ],
            "queued_jobs": [
                {
                    "render_id": "render_1640000001",
                    "status": "queued",
                    "queue_position": 1,
                    "estimated_start": "2024-01-15T14:35:00Z",
                    "script_title": "Yapay Zeka Analizi"
                },
                {
                    "render_id": "render_1640000002",
                    "status": "queued",
                    "queue_position": 2,
                    "estimated_start": "2024-01-15T14:40:00Z",
                    "script_title": "5 En İyi Telefon"
                }
            ],
            "completed_jobs": [
                {
                    "render_id": "render_1639999900",
                    "status": "completed",
                    "completed_at": "2024-01-15T14:25:00Z",
                    "processing_time": 42.1,
                    "script_title": "Siber Güvenlik İpuçları"
                }
            ],
            "queue_stats": {
                "total_jobs": 3,
                "active_jobs": 1,
                "queued_jobs": 2,
                "completed_today": 5,
                "average_processing_time": 38.5
            }
        }
        
        return {
            "success": True,
            "queue": queue_data,
            "message": "Render kuyruğu başarıyla alındı"
        }
        
    except Exception as e:
        logger.error(f"Render queue error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup/{render_id}")
async def cleanup_render_files(render_id: str) -> Dict[str, Any]:
        """Render dosyalarını temizle"""
        try:
            render_service = VideoRenderingService()
            
            # Temizlik yap
            await render_service.cleanup_temp_files(render_id)
            
            return {
                "success": True,
                "render_id": render_id,
                "cleaned_at": datetime.utcnow().isoformat(),
                "message": "Render dosyaları başarıyla temizlendi"
            }
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/media-library")
async def get_media_library() -> Dict[str, Any]:
    """Medya kütüphanesini getir"""
    try:
        # Mock media library
        media_library = {
            "video_clips": [
                {
                    "id": "clip_1",
                    "name": "Teknoloji Background 1",
                    "duration": 30,
                    "resolution": "1920x1080",
                    "file_size": 15728640,
                    "tags": ["teknoloji", "background", "abstract"],
                    "thumbnail": "assets/media/clips/clip_1_thumb.jpg"
                },
                {
                    "id": "clip_2",
                    "name": "Abstract Animation",
                    "duration": 15,
                    "resolution": "1920x1080",
                    "file_size": 7864320,
                    "tags": ["abstract", "animation", "colorful"],
                    "thumbnail": "assets/media/clips/clip_2_thumb.jpg"
                }
            ],
            "images": [
                {
                    "id": "img_1",
                    "name": "Teknoloji Görsel 1",
                    "resolution": "1920x1080",
                    "file_size": 1048576,
                    "tags": ["teknoloji", "blue", "digital"],
                    "thumbnail": "assets/media/images/img_1_thumb.jpg"
                }
            ],
            "audio": [
                {
                    "id": "audio_1",
                    "name": "Enerjik Background Müzik",
                    "duration": 120,
                    "file_size": 2097152,
                    "tags": ["enerjik", "background", "upbeat"],
                    "waveform": "assets/media/audio/audio_1_wave.png"
                }
            ],
            "sound_effects": [
                {
                    "id": "sfx_1",
                    "name": "Whoosh Sesi",
                    "duration": 2,
                    "file_size": 524288,
                    "tags": ["whoosh", "transition", "swoosh"]
                }
            ],
            "total_files": {
                "video_clips": 2,
                "images": 1,
                "audio": 1,
                "sound_effects": 1,
                "total_size": 26214400
            }
        }
        
        return {
            "success": True,
            "media_library": media_library,
            "message": "Medya kütüphanesi başarıyla alındı"
        }
        
    except Exception as e:
        logger.error(f"Media library error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-render")
async def batch_render_videos(
    requests: List[VideoRenderRequest],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Çoklu video render"""
    try:
        if len(requests) > 10:
            raise HTTPException(status_code=400, detail="En fazla 10 video aynı anda render edilebilir")
        
        render_results = []
        render_service = VideoRenderingService()
        
        for i, request in enumerate(requests):
            try:
                # Render işlemini başlat
                render_result = await render_service.render_video(
                    script_data=request.script_data,
                    video_config=request.video_config,
                    media_assets=request.media_assets
                )
                
                if render_result.get("success"):
                    render_results.append({
                        "index": i,
                        "render_id": render_result.get("render_id"),
                        "status": "completed",
                        "video_path": render_result.get("video_path")
                    })
                else:
                    render_results.append({
                        "index": i,
                        "status": "failed",
                        "error": render_result.get("error", "Render başarısız")
                    })
                    
            except Exception as e:
                render_results.append({
                    "index": i,
                    "status": "failed",
                    "error": str(e)
                })
        
        successful_renders = [r for r in render_results if r.get("status") == "completed"]
        
        return {
            "success": True,
            "batch_results": render_results,
            "total_requested": len(requests),
            "successful_renders": len(successful_renders),
            "failed_renders": len(requests) - len(successful_renders),
            "message": f"Batch render tamamlandı: {len(successful_renders)}/{len(requests)} başarılı"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch render error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
