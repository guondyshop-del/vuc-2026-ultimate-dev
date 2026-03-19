"""
VUC-2026 Videos API
Video yönetimi için endpoint'ler - SWE 1.5 Staff Engineer Standards
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..database import get_db
from ..schemas.core import (
    VideoCreateRequest,
    VideoResponse,
    VideoListResponse,
    BaseResponse,
    ErrorResponse
)
from ..core.error_handler import VUCException, DatabaseError
from ..services.video_service import VideoService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=VideoListResponse)
async def get_videos(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    channel_id: Optional[int] = Query(None, ge=1, description="Filter by channel"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
) -> VideoListResponse:
    """Tüm videoları listele - Strict typing ile"""
    try:
        video_service = VideoService(db)
        videos, total = await video_service.get_videos(
            page=page,
            size=size,
            channel_id=channel_id,
            status=status
        )
        
        return VideoListResponse(
            success=True,
            message="Video listesi başarıyla alındı",
            videos=videos,
            total=total,
            page=page,
            size=size
        )
        
    except VUCException:
        raise
    except Exception as e:
        logger.error(f"Video listesi alma hatası: {e}")
        raise DatabaseError(f"Video listesi alınamadı: {str(e)}")

@router.post("/", response_model=VideoResponse)
async def create_video(
    video_data: VideoCreateRequest,
    db: Session = Depends(get_db)
) -> VideoResponse:
    """Yeni video oluştur - Pydantic v2 validation"""
    try:
        video_service = VideoService(db)
        video = await video_service.create_video(video_data)
        
        logger.info(f"Video oluşturuldu: {video.title} (ID: {video.id})")
        return video
        
    except VUCException:
        raise
    except Exception as e:
        logger.error(f"Video oluşturma hatası: {e}")
        raise DatabaseError(f"Video oluşturulamadı: {str(e)}")

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    db: Session = Depends(get_db)
) -> VideoResponse:
    """Video detaylarını al - Type safe"""
    try:
        if video_id <= 0:
            raise VUCException(
                message="Video ID pozitif bir sayı olmalıdır",
                error_code="INVALID_VIDEO_ID",
                severity="low"
            )
        
        video_service = VideoService(db)
        video = await video_service.get_video_by_id(video_id)
        
        if not video:
            raise VUCException(
                message=f"Video bulunamadı: {video_id}",
                error_code="VIDEO_NOT_FOUND",
                severity="medium"
            )
        
        return video
        
    except VUCException:
        raise
    except Exception as e:
        logger.error(f"Video detayları alma hatası: {e}")
        raise DatabaseError(f"Video detayları alınamadı: {str(e)}")

@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int,
    video_data: VideoCreateRequest,
    db: Session = Depends(get_db)
) -> VideoResponse:
    """Video güncelle - Strict validation"""
    try:
        video_service = VideoService(db)
        video = await video_service.update_video(video_id, video_data)
        
        if not video:
            raise VUCException(
                message=f"Güncellenecek video bulunamadı: {video_id}",
                error_code="VIDEO_NOT_FOUND",
                severity="medium"
            )
        
        logger.info(f"Video güncellendi: {video.title} (ID: {video.id})")
        return video
        
    except VUCException:
        raise
    except Exception as e:
        logger.error(f"Video güncelleme hatası: {e}")
        raise DatabaseError(f"Video güncellenemedi: {str(e)}")

@router.delete("/{video_id}", response_model=BaseResponse)
async def delete_video(
    video_id: int,
    db: Session = Depends(get_db)
) -> BaseResponse:
    """Video sil - Safe deletion"""
    try:
        if video_id <= 0:
            raise VUCException(
                message="Video ID pozitif bir sayı olmalıdır",
                error_code="INVALID_VIDEO_ID",
                severity="low"
            )
        
        video_service = VideoService(db)
        success = await video_service.delete_video(video_id)
        
        if not success:
            raise VUCException(
                message=f"Silinecek video bulunamadı: {video_id}",
                error_code="VIDEO_NOT_FOUND",
                severity="medium"
            )
        
        logger.info(f"Video silindi: ID {video_id}")
        return BaseResponse(
            success=True,
            message="Video başarıyla silindi"
        )
        
    except VUCException:
        raise
    except Exception as e:
        logger.error(f"Video silme hatası: {e}")
        raise DatabaseError(f"Video silinemedi: {str(e)}")
