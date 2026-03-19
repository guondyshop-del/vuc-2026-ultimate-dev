from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from ..database import Base

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    channel_id = Column(String(100), unique=True, nullable=False)
    niche = Column(String(100), nullable=False)  # Babies, Military, Crypto, etc.
    language = Column(String(10), default="TR")  # TR, EN, DE, FR, ES
    target_audience = Column(Text)
    description = Column(Text)
    keywords = Column(JSON)  # Anahtar kelimeler listesi
    is_active = Column(Boolean, default=True)
    auto_upload = Column(Boolean, default=False)
    upload_schedule = Column(JSON)  # JSON formatında takvim
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # YouTube API credentials
    api_key = Column(String(500))
    client_secret = Column(Text)
    
    # Growth settings
    daily_upload_target = Column(Integer, default=3)
    target_views_per_video = Column(Integer, default=10000)
    competitor_analysis_enabled = Column(Boolean, default=True)
