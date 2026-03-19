from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    tags = Column(JSON)
    category = Column(String(100))
    language = Column(String(10), default="TR")
    
    # Video metadata
    duration = Column(Float)  # saniye cinsinden
    file_path = Column(String(1000))
    thumbnail_path = Column(String(1000))
    file_size = Column(Integer)  # byte cinsinden
    
    # YouTube metadata
    youtube_id = Column(String(20), unique=True)
    upload_status = Column(String(50), default="draft")  # draft, uploaded, published, failed
    published_at = Column(DateTime(timezone=True))
    
    # Analytics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    watch_time_minutes = Column(Float, default=0)
    ctr = Column(Float, default=0)  # Click Through Rate
    retention_rate = Column(Float, default=0)
    
    # Grey-hat features
    is_reused_content = Column(Boolean, default=False)
    frame_jitter_applied = Column(Boolean, default=False)
    pixel_noise_applied = Column(Boolean, default=False)
    speed_variance_applied = Column(Boolean, default=False)
    
    # A/B Testing
    thumbnail_version = Column(String(10), default="A")
    thumbnail_a_ctr = Column(Float, default=0)
    thumbnail_b_ctr = Column(Float, default=0)
    
    # Production pipeline
    script_id = Column(Integer, ForeignKey("scripts.id"))
    status = Column(String(50), default="planning")  # planning, scripting, assets, rendering, uploading, published
    progress = Column(Integer, default=0)  # 0-100
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    channel = relationship("Channel", backref="videos")
    script = relationship("Script", backref="videos")
