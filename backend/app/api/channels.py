"""
VUC-2026 Channels API
Kanal yönetimi için endpoint'ler
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from ..database import get_db
from ..models.channel import Channel
from ..models.video import Video

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def get_channels(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Tüm kanalları listele"""
    try:
        channels = db.query(Channel).all()
        
        # Mock analytics data for each channel
        channels_data = []
        for channel in channels:
            # Get video count for this channel
            video_count = db.query(Video).filter(Video.channel_id == channel.id).count()
            
            channels_data.append({
                "id": channel.id,
                "name": channel.name,
                "channel_id": channel.channel_id,
                "niche": channel.niche,
                "language": channel.language,
                "target_audience": channel.target_audience,
                "description": channel.description,
                "keywords": channel.keywords or [],
                "is_active": channel.is_active,
                "auto_upload": channel.auto_upload,
                "upload_schedule": channel.upload_schedule,
                "created_at": channel.created_at.isoformat() if channel.created_at else None,
                "updated_at": channel.updated_at.isoformat() if channel.updated_at else None,
                "api_key": channel.api_key[:20] + "..." if channel.api_key else None,
                "client_secret": channel.client_secret[:20] + "..." if channel.client_secret else None,
                "daily_upload_target": channel.daily_upload_target,
                "target_views_per_video": channel.target_views_per_video,
                "competitor_analysis_enabled": channel.competitor_analysis_enabled,
                # Analytics (mock data for now)
                "subscribers": 125000 if channel.id == 1 else 45000,
                "total_views": 2500000 if channel.id == 1 else 890000,
                "total_videos": video_count,
                "monthly_revenue": 12500 if channel.id == 1 else 3200,
                "engagement_rate": 8.7 if channel.id == 1 else 6.2,
                # Status
                "last_sync": (datetime.now() - timedelta(hours=2)).isoformat(),
                "health_score": 92 if channel.id == 1 else 78,
                "quota_usage": 67 if channel.id == 1 else 45,
                # Logs
                "recent_activities": [
                    {
                        "id": 1,
                        "type": "upload",
                        "message": "Video başarıyla yüklendi: 'Kripto Fırsatları 2026'",
                        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
                        "details": {"video_id": "abc123", "views": 12500}
                    },
                    {
                        "id": 2,
                        "type": "sync",
                        "message": "YouTube API ile senkronizasyon tamamlandı",
                        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                        "details": {"synced_items": 45}
                    },
                    {
                        "id": 3,
                        "type": "error",
                        "message": "API kota sınırı aşıldı",
                        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
                        "details": {"quota_used": "98%", "reset_time": "2 saat"}
                    }
                ]
            })
        
        return {
            "success": True,
            "channels": channels_data,
            "total": len(channels_data)
        }
    except Exception as e:
        logger.error(f"Kanal listesi alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_channel(channel_data: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Yeni kanal oluştur"""
    try:
        # Validate required fields
        required_fields = ["name", "channel_id", "niche"]
        for field in required_fields:
            if field not in channel_data:
                raise HTTPException(status_code=400, detail=f"{field} alanı zorunludur")
        
        # Check if channel_id already exists
        existing = db.query(Channel).filter(Channel.channel_id == channel_data["channel_id"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Bu channel_id zaten mevcut")
        
        # Create new channel
        new_channel = Channel(
            name=channel_data["name"],
            channel_id=channel_data["channel_id"],
            niche=channel_data["niche"],
            language=channel_data.get("language", "TR"),
            target_audience=channel_data.get("target_audience"),
            description=channel_data.get("description"),
            keywords=channel_data.get("keywords", []),
            is_active=channel_data.get("is_active", True),
            auto_upload=channel_data.get("auto_upload", False),
            upload_schedule=channel_data.get("upload_schedule"),
            api_key=channel_data.get("api_key"),
            client_secret=channel_data.get("client_secret"),
            daily_upload_target=channel_data.get("daily_upload_target", 3),
            target_views_per_video=channel_data.get("target_views_per_video", 10000),
            competitor_analysis_enabled=channel_data.get("competitor_analysis_enabled", True)
        )
        
        db.add(new_channel)
        db.commit()
        db.refresh(new_channel)
        
        logger.info(f"Yeni kanal oluşturuldu: {new_channel.name} (ID: {new_channel.id})")
        
        return {
            "success": True,
            "channel": {
                "id": new_channel.id,
                "name": new_channel.name,
                "channel_id": new_channel.channel_id,
                "niche": new_channel.niche,
                "language": new_channel.language,
                "is_active": new_channel.is_active,
                "auto_upload": new_channel.auto_upload,
                "created_at": new_channel.created_at.isoformat()
            },
            "message": "Kanal başarıyla oluşturuldu"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal oluşturma hatası: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{channel_id}")
async def get_channel(channel_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Kanal detaylarını al"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Kanal bulunamadı")
        
        # Get videos for this channel
        videos = db.query(Video).filter(Video.channel_id == channel_id).all()
        
        return {
            "success": True,
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "channel_id": channel.channel_id,
                "niche": channel.niche,
                "language": channel.language,
                "target_audience": channel.target_audience,
                "description": channel.description,
                "keywords": channel.keywords or [],
                "is_active": channel.is_active,
                "auto_upload": channel.auto_upload,
                "upload_schedule": channel.upload_schedule,
                "created_at": channel.created_at.isoformat() if channel.created_at else None,
                "updated_at": channel.updated_at.isoformat() if channel.updated_at else None,
                "daily_upload_target": channel.daily_upload_target,
                "target_views_per_video": channel.target_views_per_video,
                "competitor_analysis_enabled": channel.competitor_analysis_enabled,
                "videos": [
                    {
                        "id": video.id,
                        "title": video.title,
                        "status": video.status,
                        "views": video.views,
                        "likes": video.likes,
                        "comments": video.comments,
                        "published_at": video.published_at.isoformat() if video.published_at else None
                    }
                    for video in videos
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal detayları alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{channel_id}")
async def update_channel(channel_id: int, channel_data: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Kanal güncelle"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Kanal bulunamadı")
        
        # Update channel fields
        updateable_fields = [
            "name", "niche", "language", "target_audience", "description",
            "keywords", "is_active", "auto_upload", "upload_schedule",
            "api_key", "client_secret", "daily_upload_target",
            "target_views_per_video", "competitor_analysis_enabled"
        ]
        
        for field in updateable_fields:
            if field in channel_data:
                setattr(channel, field, channel_data[field])
        
        channel.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Kanal güncellendi: {channel.name} (ID: {channel.id})")
        
        return {
            "success": True,
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "channel_id": channel.channel_id,
                "niche": channel.niche,
                "language": channel.language,
                "updated_at": channel.updated_at.isoformat()
            },
            "message": "Kanal başarıyla güncellendi"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal güncelleme hatası: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{channel_id}")
async def delete_channel(channel_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Kanal sil"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Kanal bulunamadı")
        
        # Check if channel has videos
        video_count = db.query(Video).filter(Video.channel_id == channel_id).count()
        if video_count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Kanala ait {video_count} video olduğu için silinemez"
            )
        
        db.delete(channel)
        db.commit()
        
        logger.info(f"Kanal silindi: {channel.name} (ID: {channel.id})")
        
        return {
            "success": True,
            "channel_id": channel_id,
            "message": "Kanal başarıyla silindi"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal silme hatası: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{channel_id}/sync")
async def sync_channel(channel_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Kanal senkronizasyonu"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Kanal bulunamadı")
        
        # Mock sync process - in real implementation, this would sync with YouTube API
        sync_data = {
            "subscribers": 125000 + (channel_id * 1000),
            "total_views": 2500000 + (channel_id * 50000),
            "last_sync": datetime.utcnow().isoformat(),
            "health_score": min(95, 85 + (channel_id * 5))
        }
        
        logger.info(f"Kanal senkronize edildi: {channel.name} (ID: {channel.id})")
        
        return {
            "success": True,
            "channel_id": channel_id,
            "sync_data": sync_data,
            "message": "Kanal başarıyla senkronize edildi"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal senkronizasyon hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{channel_id}/analytics")
async def get_channel_analytics(channel_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Kanal analitikleri"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Kanal bulunamadı")
        
        # Mock analytics data - in real implementation, this would come from YouTube Analytics API
        analytics = {
            "overview": {
                "subscribers": 125000 + (channel_id * 1000),
                "total_views": 2500000 + (channel_id * 50000),
                "total_videos": db.query(Video).filter(Video.channel_id == channel_id).count(),
                "monthly_revenue": 12500 + (channel_id * 500),
                "engagement_rate": 8.7 + (channel_id * 0.5)
            },
            "growth": {
                "subscribers_growth_30d": 12.5,
                "views_growth_30d": 18.3,
                "revenue_growth_30d": 15.7
            },
            "top_videos": [
                {
                    "title": "Kripto Fırsatları 2026",
                    "views": 125000,
                    "likes": 8500,
                    "comments": 234
                },
                {
                    "title": "Bitcoin Tahminleri",
                    "views": 89000,
                    "likes": 6200,
                    "comments": 156
                }
            ],
            "audience_demographics": {
                "age_groups": {"18-24": 25, "25-34": 35, "35-44": 25, "45+": 15},
                "gender": {"male": 65, "female": 35},
                "countries": {"TR": 45, "US": 20, "DE": 15, "other": 20}
            }
        }
        
        return {
            "success": True,
            "channel_id": channel_id,
            "analytics": analytics
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Kanal analitikleri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
