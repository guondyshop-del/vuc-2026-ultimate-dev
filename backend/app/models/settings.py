from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from ..database import Base

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(JSON)
    description = Column(Text)
    category = Column(String(50))  # api, rendering, upload, ai, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Default settings
DEFAULT_SETTINGS = {
    "gemini_api_key": {
        "value": "AIzaSyDjastAPrl4GcrgH-_t3FO3jJZtgOReHyc",
        "description": "Google Gemini 2.0 Pro API Anahtarı",
        "category": "api"
    },
    "youtube_api_key": {
        "value": "",
        "description": "YouTube Data API v3 Anahtarı",
        "category": "api"
    },
    "pexels_api_key": {
        "value": "",
        "description": "Pexels Stock Video API Anahtarı",
        "category": "api"
    },
    "pixabay_api_key": {
        "value": "",
        "description": "Pixabay API Anahtarı",
        "category": "api"
    },
    "render_quality": {
        "value": "high",
        "description": "Video render kalitesi (low, medium, high, ultra)",
        "category": "rendering"
    },
    "auto_upload_enabled": {
        "value": False,
        "description": "Otomatik video yükleme aktif",
        "category": "upload"
    },
    "ghost_interaction_enabled": {
        "value": True,
        "description": "Hayalet etkileşim özellikleri aktif",
        "category": "growth"
    },
    "algorithm_shield_enabled": {
        "value": True,
        "description": "Algoritma koruma kalkanı aktif",
        "category": "growth"
    },
    "daily_upload_limit": {
        "value": 5,
        "description": "Günlük maksimum video yükleme limiti",
        "category": "upload"
    },
    "default_language": {
        "value": "TR",
        "description": "Varsayılan içerik dili",
        "category": "content"
    },
    "default_voice": {
        "value": "tr-TR-AhmetNeural",
        "description": "Varsayılan TTS sesi",
        "category": "content"
    },
    "thumbnail_style": {
        "value": "hormozi",
        "description": "Thumbnail stili (hormozi, minimal, bold)",
        "category": "content"
    },
    "auto_thumbnail_ab_test": {
        "value": True,
        "description": "Otomatik thumbnail A/B testi",
        "category": "growth"
    },
    "competitor_analysis_interval": {
        "value": 24,
        "description": "Rakip analizi aralığı (saat)",
        "category": "analytics"
    },
    "retry_failed_uploads": {
        "value": True,
        "description": "Başarısız yüklemeleri otomatik yeniden dene",
        "category": "upload"
    },
    "max_render_concurrent": {
        "value": 2,
        "description": "Maksimum eş zamanlı render işlemi",
        "category": "rendering"
    }
}
