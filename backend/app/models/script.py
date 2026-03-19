from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Script(Base):
    __tablename__ = "scripts"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    
    # Script content
    title = Column(String(500), nullable=False)
    hook = Column(Text)  # 3 saniyelik kancı
    main_content = Column(Text, nullable=False)
    cta = Column(Text)  # Call to Action
    language = Column(String(10), default="TR")
    
    # AI generation metadata
    ai_model = Column(String(100), default="gemini-2.0-pro")
    generation_prompt = Column(Text)
    generation_temperature = Column(Float, default=0.7)
    
    # Script structure
    scenes = Column(JSON)  # Sahne bazında breakdown
    keywords = Column(JSON)  # Hedeflenen anahtar kelimeler
    emotional_arc = Column(JSON)  # Duygusal yol haritası
    
    # Performance metrics
    estimated_retention_rate = Column(Float, default=0)
    estimated_watch_time = Column(Float, default=0)
    hook_strength_score = Column(Float, default=0)
    
    # TTS metadata
    voice_profile = Column(String(100))  # edge-tts voice
    speech_rate = Column(Float, default=1.0)
    pitch = Column(Float, default=0)
    ssml_content = Column(Text)  # SSML formatında içerik
    
    # Status
    status = Column(String(50), default="draft")  # draft, approved, recorded, used
    is_approved = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    channel = relationship("Channel", backref="scripts")
