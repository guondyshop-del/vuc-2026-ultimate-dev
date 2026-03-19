from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Competitor(Base):
    __tablename__ = "competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    
    # Competitor info
    competitor_channel_id = Column(String(100), nullable=False)
    competitor_name = Column(String(255))
    subscriber_count = Column(Integer, default=0)
    total_videos = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    
    # Analysis data
    niche = Column(String(100))
    content_style = Column(String(100))  # educational, entertainment, news, etc.
    upload_frequency = Column(Float)  # videos per week
    average_video_length = Column(Float)  # minutes
    
    # Performance metrics
    avg_views_per_video = Column(Float, default=0)
    avg_engagement_rate = Column(Float, default=0)
    vph_trend = Column(JSON)  # View-per-Hour trend data
    best_upload_times = Column(JSON)  # Optimal upload times
    
    # Content analysis
    top_keywords = Column(JSON)  # Most used keywords
    trending_topics = Column(JSON)  # Currently trending in their niche
    content_gaps = Column(JSON)  # Topics they're missing
    
    # Thumbnail analysis
    thumbnail_styles = Column(JSON)  # Common thumbnail patterns
    color_schemes = Column(JSON)  # Dominant colors used
    
    # Last analysis
    last_analyzed_at = Column(DateTime(timezone=True))
    analysis_version = Column(String(20), default="1.0")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    channel = relationship("Channel", backref="competitors")

class CompetitorVideo(Base):
    __tablename__ = "competitor_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    
    # Video metadata
    youtube_id = Column(String(20), nullable=False)
    title = Column(String(500))
    description = Column(Text)
    tags = Column(JSON)
    duration = Column(Float)
    published_at = Column(DateTime(timezone=True))
    
    # Performance data
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # View-per-Hour tracking
    vph_data = Column(JSON)  # Hourly view progression
    peak_view_hours = Column(JSON)  # When views peaked
    
    # Content analysis
    hook_detected = Column(Text)  # First 3 seconds analysis
    cta_detected = Column(Boolean, default=False)
    emotional_elements = Column(JSON)  # Anger, joy, surprise, etc.
    
    # Thumbnail data
    thumbnail_url = Column(String(1000))
    thumbnail_analysis = Column(JSON)  # AI analysis of thumbnail
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    competitor = relationship("Competitor", backref="videos")
