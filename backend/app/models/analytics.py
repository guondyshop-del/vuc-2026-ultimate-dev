from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    
    # Analytics period
    date = Column(DateTime(timezone=True), nullable=False)
    period_type = Column(String(20), default="daily")  # hourly, daily, weekly, monthly
    
    # Channel metrics
    total_subscribers = Column(Integer, default=0)
    new_subscribers = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_watch_time_minutes = Column(Float, default=0)
    
    # Video metrics (if video_id is provided)
    video_views = Column(Integer, default=0)
    video_likes = Column(Integer, default=0)
    video_comments = Column(Integer, default=0)
    video_shares = Column(Integer, default=0)
    video_watch_time_minutes = Column(Float, default=0)
    
    # Engagement metrics
    engagement_rate = Column(Float, default=0)
    click_through_rate = Column(Float, default=0)
    audience_retention = Column(Float, default=0)
    
    # Revenue metrics
    estimated_revenue = Column(Float, default=0)
    rpm = Column(Float, default=0)  # Revenue per mille
    
    # Traffic sources
    traffic_sources = Column(JSON)  # YouTube search, suggested, external, etc.
    device_types = Column(JSON)  # Desktop, mobile, tablet, TV
    geographic_data = Column(JSON)  # Top countries
    
    # Algorithm insights
    algorithm_score = Column(Float, default=0)  # YouTube algorithm favorability
    trending_score = Column(Float, default=0)  # Trending potential
    viral_coefficient = Column(Float, default=0)  # Share-to-view ratio
    
    # Ghost interaction metrics
    auto_comments_posted = Column(Integer, default=0)
    persona_responses_generated = Column(Integer, default=0)
    engagement_boost_score = Column(Float, default=0)
    
    # A/B Test results
    thumbnail_test_results = Column(JSON)
    title_test_results = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    channel = relationship("Channel", backref="analytics")
    video = relationship("Video", backref="analytics")

class TrendingTopic(Base):
    __tablename__ = "trending_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    niche = Column(String(100), nullable=False)
    language = Column(String(10), default="TR")
    
    # Topic data
    topic = Column(String(500), nullable=False)
    keywords = Column(JSON)
    category = Column(String(100))
    
    # Trend metrics
    search_volume = Column(Integer, default=0)
    trend_score = Column(Float, default=0)
    competition_level = Column(String(20))  # low, medium, high
    opportunity_score = Column(Float, default=0)
    
    # Time data
    trending_since = Column(DateTime(timezone=True))
    peak_period = Column(JSON)  # When this topic trends most
    estimated_lifespan = Column(Integer)  # Days
    
    # Content potential
    video_potential_score = Column(Float, default=0)
    estimated_views = Column(Integer, default=0)
    suggested_angles = Column(JSON)  # Different content approaches
    
    # Competitor activity
    competitor_coverage = Column(JSON)  # Which competitors covered this
    content_gap_opportunity = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SystemPerformance(Base):
    __tablename__ = "system_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # System metrics
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    cpu_usage = Column(Float, default=0)
    memory_usage = Column(Float, default=0)
    gpu_usage = Column(Float, default=0)
    disk_usage = Column(Float, default=0)
    
    # Application metrics
    active_rendering_tasks = Column(Integer, default=0)
    queued_videos = Column(Integer, default=0)
    api_calls_remaining = Column(JSON)  # Per API service
    error_count = Column(Integer, default=0)
    
    # Performance
    avg_render_time = Column(Float, default=0)  # minutes
    avg_upload_speed = Column(Float, default=0)  # Mbps
    success_rate = Column(Float, default=0)
    
    # Queue status
    redis_queue_size = Column(Integer, default=0)
    celery_worker_count = Column(Integer, default=0)
    
    # Alerts
    alerts = Column(JSON)  # System warnings and errors
