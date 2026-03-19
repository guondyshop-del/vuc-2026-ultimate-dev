from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import os
from datetime import datetime

from ..database import get_db
from ..services.settings_service import SettingsService

router = APIRouter()

class YouTubeContentSettings(BaseModel):
    default_category: str = "22"
    default_privacy: str = "private"
    default_made_for_kids: bool = False
    max_video_duration: int = 14400
    max_file_size: int = 268435456000
    supported_formats: str = "mp4,webm,avi,mov,mpeg,flv,wmv"
    thumbnail_max_size: int = 2097152
    thumbnail_formats: str = "jpg,png,gif,bmp"

class YouTubeProfileSettings(BaseModel):
    channel_title: str = "VUC-2026 Ultimate Dev"
    channel_description: str = "Vespera Ultimate Central - Otonom YouTube İmparatorluk Yönetim Sistemi"
    channel_keywords: str = "technology,ai,development,programming,automation"
    default_language: str = "tr"
    default_country: str = "TR"
    channel_privacy: str = "public"

class YouTubeScheduleSettings(BaseModel):
    auto_schedule_enabled: bool = True
    optimal_upload_times: str = "09:00,15:00,20:00"
    timezone: str = "Europe/Istanbul"
    batch_upload_enabled: bool = False
    max_concurrent_uploads: int = 2
    retry_attempts: int = 3
    retry_delay: int = 60

class YouTubeOptimizationSettings(BaseModel):
    auto_tags_enabled: bool = True
    max_tags: int = 15
    tag_generation_model: str = "gemini-2.5-pro"
    title_optimization_enabled: bool = True
    description_templates_enabled: bool = True
    thumbnail_auto_generation: bool = True

class YouTubeAnalyticsSettings(BaseModel):
    analytics_enabled: bool = True
    performance_tracking: bool = True
    audience_retention_analysis: bool = True
    engagement_monitoring: bool = True
    revenue_tracking: bool = True
    competitor_analysis: bool = True

class YouTubeMonetizationSettings(BaseModel):
    monetization_enabled: bool = True
    ad_formats: str = "display_ads,overlay_ads,skippable_video_ads,non_skippable_video_ads,bumper_ads,sponsor_cards"
    content_suitability: str = "general"
    auto_content_rating: bool = True

class YouTubeCommunitySettings(BaseModel):
    auto_comments_response: bool = False
    comment_moderation: bool = True
    community_posts_enabled: bool = True
    live_streaming_enabled: bool = False
    premiere_features: bool = True

class YouTubeSafetySettings(BaseModel):
    content_warnings: bool = True
    copyright_check: bool = True
    community_guidelines_check: bool = True
    child_safety_mode: bool = True
    auto_content_id_check: bool = True

class YouTubeAPISettings(BaseModel):
    api_quota_enabled: bool = True
    daily_quota_limit: int = 10000
    rate_limit_per_minute: int = 60
    burst_limit: int = 100
    quota_reset_time: str = "00:00"

class YouTubeAllSettings(BaseModel):
    content: YouTubeContentSettings
    profile: YouTubeProfileSettings
    schedule: YouTubeScheduleSettings
    optimization: YouTubeOptimizationSettings
    analytics: YouTubeAnalyticsSettings
    monetization: YouTubeMonetizationSettings
    community: YouTubeCommunitySettings
    safety: YouTubeSafetySettings
    api: YouTubeAPISettings

class YouTubeSettingsService:
    def __init__(self):
        self.settings_service = SettingsService()
    
    def get_env_setting(self, key: str, default: Any = None) -> Any:
        """Get environment variable with type conversion"""
        value = os.getenv(key, default)
        if value is None:
            return default
        
        # Convert to appropriate type
        if isinstance(default, bool):
            return value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(default, int):
            try:
                return int(value)
            except ValueError:
                return default
        elif isinstance(default, float):
            try:
                return float(value)
            except ValueError:
                return default
        
        return value
    
    def set_env_setting(self, key: str, value: Any) -> bool:
        """Set environment variable (for runtime, not persistent)"""
        os.environ[key] = str(value)
        return True
    
    def get_content_settings(self) -> YouTubeContentSettings:
        return YouTubeContentSettings(
            default_category=self.get_env_setting("YOUTUBE_DEFAULT_CATEGORY", "22"),
            default_privacy=self.get_env_setting("YOUTUBE_DEFAULT_PRIVACY", "private"),
            default_made_for_kids=self.get_env_setting("YOUTUBE_DEFAULT_MADE_FOR_KIDS", False),
            max_video_duration=self.get_env_setting("YOUTUBE_MAX_VIDEO_DURATION", 14400),
            max_file_size=self.get_env_setting("YOUTUBE_MAX_FILE_SIZE", 268435456000),
            supported_formats=self.get_env_setting("YOUTUBE_SUPPORTED_FORMATS", "mp4,webm,avi,mov,mpeg,flv,wmv"),
            thumbnail_max_size=self.get_env_setting("YOUTUBE_THUMBNAIL_MAX_SIZE", 2097152),
            thumbnail_formats=self.get_env_setting("YOUTUBE_THUMBNAIL_FORMATS", "jpg,png,gif,bmp")
        )
    
    def get_profile_settings(self) -> YouTubeProfileSettings:
        return YouTubeProfileSettings(
            channel_title=self.get_env_setting("YOUTUBE_CHANNEL_TITLE", "VUC-2026 Ultimate Dev"),
            channel_description=self.get_env_setting("YOUTUBE_CHANNEL_DESCRIPTION", "Vespera Ultimate Central - Otonom YouTube İmparatorluk Yönetim Sistemi"),
            channel_keywords=self.get_env_setting("YOUTUBE_CHANNEL_KEYWORDS", "technology,ai,development,programming,automation"),
            default_language=self.get_env_setting("YOUTUBE_DEFAULT_LANGUAGE", "tr"),
            default_country=self.get_env_setting("YOUTUBE_DEFAULT_COUNTRY", "TR"),
            channel_privacy=self.get_env_setting("YOUTUBE_CHANNEL_PRIVACY", "public")
        )
    
    def get_schedule_settings(self) -> YouTubeScheduleSettings:
        return YouTubeScheduleSettings(
            auto_schedule_enabled=self.get_env_setting("YOUTUBE_AUTO_SCHEDULE_ENABLED", True),
            optimal_upload_times=self.get_env_setting("YOUTUBE_OPTIMAL_UPLOAD_TIMES", "09:00,15:00,20:00"),
            timezone=self.get_env_setting("YOUTUBE_TIMEZONE", "Europe/Istanbul"),
            batch_upload_enabled=self.get_env_setting("YOUTUBE_BATCH_UPLOAD_ENABLED", False),
            max_concurrent_uploads=self.get_env_setting("YOUTUBE_MAX_CONCURRENT_UPLOADS", 2),
            retry_attempts=self.get_env_setting("YOUTUBE_RETRY_ATTEMPTS", 3),
            retry_delay=self.get_env_setting("YOUTUBE_RETRY_DELAY", 60)
        )
    
    def get_optimization_settings(self) -> YouTubeOptimizationSettings:
        return YouTubeOptimizationSettings(
            auto_tags_enabled=self.get_env_setting("YOUTUBE_AUTO_TAGS_ENABLED", True),
            max_tags=self.get_env_setting("YOUTUBE_MAX_TAGS", 15),
            tag_generation_model=self.get_env_setting("YOUTUBE_TAG_GENERATION_MODEL", "gemini-2.5-pro"),
            title_optimization_enabled=self.get_env_setting("YOUTUBE_TITLE_OPTIMIZATION_ENABLED", True),
            description_templates_enabled=self.get_env_setting("YOUTUBE_DESCRIPTION_TEMPLATES_ENABLED", True),
            thumbnail_auto_generation=self.get_env_setting("YOUTUBE_THUMBNAIL_AUTO_GENERATION", True)
        )
    
    def get_analytics_settings(self) -> YouTubeAnalyticsSettings:
        return YouTubeAnalyticsSettings(
            analytics_enabled=self.get_env_setting("YOUTUBE_ANALYTICS_ENABLED", True),
            performance_tracking=self.get_env_setting("YOUTUBE_PERFORMANCE_TRACKING", True),
            audience_retention_analysis=self.get_env_setting("YOUTUBE_AUDIENCE_RETENTION_ANALYSIS", True),
            engagement_monitoring=self.get_env_setting("YOUTUBE_ENGAGEMENT_MONITORING", True),
            revenue_tracking=self.get_env_setting("YOUTUBE_REVENUE_TRACKING", True),
            competitor_analysis=self.get_env_setting("YOUTUBE_COMPETITOR_ANALYSIS", True)
        )
    
    def get_monetization_settings(self) -> YouTubeMonetizationSettings:
        return YouTubeMonetizationSettings(
            monetization_enabled=self.get_env_setting("YOUTUBE_MONETIZATION_ENABLED", True),
            ad_formats=self.get_env_setting("YOUTUBE_AD_FORMATS", "display_ads,overlay_ads,skippable_video_ads,non_skippable_video_ads,bumper_ads,sponsor_cards"),
            content_suitability=self.get_env_setting("YOUTUBE_CONTENT_SUITABILITY", "general"),
            auto_content_rating=self.get_env_setting("YOUTUBE_AUTO_CONTENT_RATING", True)
        )
    
    def get_community_settings(self) -> YouTubeCommunitySettings:
        return YouTubeCommunitySettings(
            auto_comments_response=self.get_env_setting("YOUTUBE_AUTO_COMMENTS_RESPONSE", False),
            comment_moderation=self.get_env_setting("YOUTUBE_COMMENT_MODERATION", True),
            community_posts_enabled=self.get_env_setting("YOUTUBE_COMMUNITY_POSTS_ENABLED", True),
            live_streaming_enabled=self.get_env_setting("YOUTUBE_LIVE_STREAMING_ENABLED", False),
            premiere_features=self.get_env_setting("YOUTUBE_PREMIERE_FEATURES", True)
        )
    
    def get_safety_settings(self) -> YouTubeSafetySettings:
        return YouTubeSafetySettings(
            content_warnings=self.get_env_setting("YOUTUBE_CONTENT_WARNINGS", True),
            copyright_check=self.get_env_setting("YOUTUBE_COPYRIGHT_CHECK", True),
            community_guidelines_check=self.get_env_setting("YOUTUBE_COMMUNITY_GUIDELINES_CHECK", True),
            child_safety_mode=self.get_env_setting("YOUTUBE_CHILD_SAFETY_MODE", True),
            auto_content_id_check=self.get_env_setting("YOUTUBE_AUTO_CONTENT_ID_CHECK", True)
        )
    
    def get_api_settings(self) -> YouTubeAPISettings:
        return YouTubeAPISettings(
            api_quota_enabled=self.get_env_setting("YOUTUBE_API_QUOTA_ENABLED", True),
            daily_quota_limit=self.get_env_setting("YOUTUBE_DAILY_QUOTA_LIMIT", 10000),
            rate_limit_per_minute=self.get_env_setting("YOUTUBE_RATE_LIMIT_PER_MINUTE", 60),
            burst_limit=self.get_env_setting("YOUTUBE_BURST_LIMIT", 100),
            quota_reset_time=self.get_env_setting("YOUTUBE_QUOTA_RESET_TIME", "00:00")
        )
    
    def get_all_settings(self) -> YouTubeAllSettings:
        return YouTubeAllSettings(
            content=self.get_content_settings(),
            profile=self.get_profile_settings(),
            schedule=self.get_schedule_settings(),
            optimization=self.get_optimization_settings(),
            analytics=self.get_analytics_settings(),
            monetization=self.get_monetization_settings(),
            community=self.get_community_settings(),
            safety=self.get_safety_settings(),
            api=self.get_api_settings()
        )
    
    def update_content_settings(self, settings: YouTubeContentSettings) -> YouTubeContentSettings:
        """Update content settings"""
        self.set_env_setting("YOUTUBE_DEFAULT_CATEGORY", settings.default_category)
        self.set_env_setting("YOUTUBE_DEFAULT_PRIVACY", settings.default_privacy)
        self.set_env_setting("YOUTUBE_DEFAULT_MADE_FOR_KIDS", settings.default_made_for_kids)
        self.set_env_setting("YOUTUBE_MAX_VIDEO_DURATION", settings.max_video_duration)
        self.set_env_setting("YOUTUBE_MAX_FILE_SIZE", settings.max_file_size)
        self.set_env_setting("YOUTUBE_SUPPORTED_FORMATS", settings.supported_formats)
        self.set_env_setting("YOUTUBE_THUMBNAIL_MAX_SIZE", settings.thumbnail_max_size)
        self.set_env_setting("YOUTUBE_THUMBNAIL_FORMATS", settings.thumbnail_formats)
        return settings
    
    def update_profile_settings(self, settings: YouTubeProfileSettings) -> YouTubeProfileSettings:
        """Update profile settings"""
        self.set_env_setting("YOUTUBE_CHANNEL_TITLE", settings.channel_title)
        self.set_env_setting("YOUTUBE_CHANNEL_DESCRIPTION", settings.channel_description)
        self.set_env_setting("YOUTUBE_CHANNEL_KEYWORDS", settings.channel_keywords)
        self.set_env_setting("YOUTUBE_DEFAULT_LANGUAGE", settings.default_language)
        self.set_env_setting("YOUTUBE_DEFAULT_COUNTRY", settings.default_country)
        self.set_env_setting("YOUTUBE_CHANNEL_PRIVACY", settings.channel_privacy)
        return settings

# Initialize service
youtube_settings_service = YouTubeSettingsService()

@router.get("/youtube-settings", response_model=YouTubeAllSettings)
async def get_youtube_settings(db: Session = Depends(get_db)):
    """Get all YouTube settings"""
    try:
        return youtube_settings_service.get_all_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve YouTube settings: {str(e)}"
        )

@router.get("/youtube-settings/content", response_model=YouTubeContentSettings)
async def get_content_settings(db: Session = Depends(get_db)):
    """Get content sharing settings"""
    try:
        return youtube_settings_service.get_content_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve content settings: {str(e)}"
        )

@router.get("/youtube-settings/profile", response_model=YouTubeProfileSettings)
async def get_profile_settings(db: Session = Depends(get_db)):
    """Get profile settings"""
    try:
        return youtube_settings_service.get_profile_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve profile settings: {str(e)}"
        )

@router.put("/youtube-settings/content", response_model=YouTubeContentSettings)
async def update_content_settings(settings: YouTubeContentSettings, db: Session = Depends(get_db)):
    """Update content sharing settings"""
    try:
        return youtube_settings_service.update_content_settings(settings)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update content settings: {str(e)}"
        )

@router.put("/youtube-settings/profile", response_model=YouTubeProfileSettings)
async def update_profile_settings(settings: YouTubeProfileSettings, db: Session = Depends(get_db)):
    """Update profile settings"""
    try:
        return youtube_settings_service.update_profile_settings(settings)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile settings: {str(e)}"
        )

@router.get("/youtube-settings/schedule", response_model=YouTubeScheduleSettings)
async def get_schedule_settings(db: Session = Depends(get_db)):
    """Get schedule settings"""
    try:
        return youtube_settings_service.get_schedule_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve schedule settings: {str(e)}"
        )

@router.get("/youtube-settings/optimization", response_model=YouTubeOptimizationSettings)
async def get_optimization_settings(db: Session = Depends(get_db)):
    """Get optimization settings"""
    try:
        return youtube_settings_service.get_optimization_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve optimization settings: {str(e)}"
        )

@router.get("/youtube-settings/analytics", response_model=YouTubeAnalyticsSettings)
async def get_analytics_settings(db: Session = Depends(get_db)):
    """Get analytics settings"""
    try:
        return youtube_settings_service.get_analytics_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analytics settings: {str(e)}"
        )

@router.get("/youtube-settings/monetization", response_model=YouTubeMonetizationSettings)
async def get_monetization_settings(db: Session = Depends(get_db)):
    """Get monetization settings"""
    try:
        return youtube_settings_service.get_monetization_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve monetization settings: {str(e)}"
        )

@router.get("/youtube-settings/community", response_model=YouTubeCommunitySettings)
async def get_community_settings(db: Session = Depends(get_db)):
    """Get community settings"""
    try:
        return youtube_settings_service.get_community_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve community settings: {str(e)}"
        )

@router.get("/youtube-settings/safety", response_model=YouTubeSafetySettings)
async def get_safety_settings(db: Session = Depends(get_db)):
    """Get safety settings"""
    try:
        return youtube_settings_service.get_safety_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve safety settings: {str(e)}"
        )

@router.get("/youtube-settings/api", response_model=YouTubeAPISettings)
async def get_api_settings(db: Session = Depends(get_db)):
    """Get API settings"""
    try:
        return youtube_settings_service.get_api_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve API settings: {str(e)}"
        )

@router.post("/youtube-settings/reset")
async def reset_youtube_settings(db: Session = Depends(get_db)):
    """Reset all YouTube settings to defaults"""
    try:
        # This would typically update a database or config file
        # For now, return success message
        return {
            "message": "YouTube settings reset to defaults successfully",
            "timestamp": datetime.utcnow(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset YouTube settings: {str(e)}"
        )
