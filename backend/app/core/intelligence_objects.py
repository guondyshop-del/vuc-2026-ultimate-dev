"""
VUC-2026 Intelligence Objects
Pydantic models for structured inter-agent communication

This module defines all intelligence objects used for communication
between agents in the neural network architecture.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid

class PriorityLevel(str, Enum):
    """Priority levels for intelligence objects"""
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"

class AgentType(str, Enum):
    """Agent types in the empire"""
    SCRIPT_AGENT = "script_agent"
    MEDIA_AGENT = "media_agent"
    SEO_AGENT = "seo_agent"
    UPLOAD_AGENT = "upload_agent"
    SPY_AGENT = "spy_agent"
    GHOST_AGENT = "ghost_agent"
    GROWTH_AGENT = "growth_agent"

class ConfidenceLevel(BaseModel):
    """Confidence scoring system"""
    score: float = Field(..., ge=0, le=100, description="Confidence score 0-100")
    level: str = Field(..., description="Confidence level description")
    requires_human_review: bool = Field(..., description="Requires human review")
    auto_execution: bool = Field(..., description="Can execute autonomously")
    
    @validator('level', pre=True, always=True)
    def set_level(cls, v, values):
        """Set confidence level based on score"""
        score = values.get('score', 0)
        if score >= 90:
            return "Yüksek Güven"
        elif score >= 75:
            return "Orta Güven"
        elif score >= 60:
            return "Düşük Güven"
        else:
            return "Çok Düşük Güven"
    
    @validator('requires_human_review', pre=True, always=True)
    def set_human_review(cls, v, values):
        """Set human review requirement"""
        score = values.get('score', 0)
        return score < 75
    
    @validator('auto_execution', pre=True, always=True)
    def set_auto_execution(cls, v, values):
        """Set auto execution capability"""
        score = values.get('score', 0)
        return score >= 90

class BaseIntelligenceObject(BaseModel):
    """Base intelligence object for all agent communications"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique object ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    agent: AgentType = Field(..., description="Creating agent type")
    confidence: ConfidenceLevel = Field(..., description="Confidence assessment")
    data: Dict[str, Any] = Field(..., description="Intelligence data payload")
    priority: PriorityLevel = Field(default=PriorityLevel.NORMAL, description="Priority level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    execution_status: Optional[str] = Field(None, description="Execution status")
    parent_id: Optional[str] = Field(None, description="Parent intelligence object ID")
    child_ids: List[str] = Field(default_factory=list, description="Child intelligence object IDs")

class ScriptIntelligence(BaseIntelligenceObject):
    """Script agent intelligence object"""
    script_type: str = Field(..., description="Type of script (educational, entertainment, etc.)")
    word_count: int = Field(..., ge=1, description="Word count of script")
    seo_keywords: List[str] = Field(default_factory=list, description="SEO keywords included")
    hook_strength: float = Field(..., ge=0, le=10, description="Hook strength score 0-10")
    viral_potential: float = Field(..., ge=0, le=10, description="Viral potential score 0-10")
    emotional_tone: str = Field(..., description="Emotional tone of script")
    target_audience: str = Field(..., description="Target audience demographic")
    content_pillar: str = Field(..., description="Content pillar category")
    estimated_duration: int = Field(..., ge=1, description="Estimated video duration in seconds")
    script_structure: Dict[str, Any] = Field(default_factory=dict, description="Script structure analysis")
    engagement_hooks: List[str] = Field(default_factory=list, description="Engagement hooks included")

class MediaIntelligence(BaseIntelligenceObject):
    """Media agent intelligence object"""
    resolution: str = Field(..., description="Video resolution (1920x1080, etc.)")
    fps: int = Field(..., ge=1, le=240, description="Frames per second")
    duration: int = Field(..., ge=1, description="Video duration in seconds")
    quality_score: float = Field(..., ge=0, le=10, description="Quality assessment score 0-10")
    shadowban_shield: bool = Field(default=True, description="Shadowban protection applied")
    file_size_mb: float = Field(..., ge=0, description="File size in MB")
    codec: str = Field(..., description="Video codec used")
    bitrate: Optional[int] = Field(None, description="Video bitrate")
    color_grading: Dict[str, Any] = Field(default_factory=dict, description="Color grading information")
    audio_quality: Dict[str, Any] = Field(default_factory=dict, description="Audio quality metrics")
    rendering_time: Optional[float] = Field(None, description="Rendering time in seconds")
    device_metadata: Dict[str, Any] = Field(default_factory=dict, description="Device spoofing metadata")

class SEOIntelligence(BaseIntelligenceObject):
    """SEO agent intelligence object"""
    title_score: float = Field(..., ge=0, le=10, description="Title optimization score 0-10")
    description_score: float = Field(..., ge=0, le=10, description="Description optimization score 0-10")
    tag_relevance: float = Field(..., ge=0, le=10, description="Tag relevance score 0-10")
    thumbnail_optimized: bool = Field(default=False, description="Thumbnail optimized flag")
    estimated_ctr: float = Field(..., ge=0, le=100, description="Estimated click-through rate %")
    keyword_density: float = Field(..., ge=0, le=10, description="Keyword density score 0-10")
    competition_analysis: Dict[str, Any] = Field(default_factory=dict, description="Competition analysis")
    trend_alignment: float = Field(..., ge=0, le=10, description="Trend alignment score 0-10")
    search_volume: Dict[str, Any] = Field(default_factory=dict, description="Search volume data")
    ranking_potential: float = Field(..., ge=0, le=10, description="Ranking potential score 0-10")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Optimization suggestions")

class UploadIntelligence(BaseIntelligenceObject):
    """Upload agent intelligence object"""
    upload_speed: float = Field(..., ge=0, description="Upload speed MB/s")
    success_rate: float = Field(..., ge=0, le=100, description="Upload success rate %")
    platform_compliance: bool = Field(default=True, description="Platform compliance check")
    metadata_integrity: bool = Field(default=True, description="Metadata integrity check")
    upload_method: str = Field(..., description="Upload method used")
    retry_count: int = Field(default=0, description="Number of upload retries")
    chunk_size: Optional[int] = Field(None, description="Upload chunk size in bytes")
    proxy_used: Optional[str] = Field(None, description="Proxy used for upload")
    user_agent: Optional[str] = Field(None, description="User agent used")
    upload_duration: Optional[float] = Field(None, description="Upload duration in seconds")
    error_codes: List[str] = Field(default_factory=list, description="Error codes encountered")

class SpyIntelligence(BaseIntelligenceObject):
    """Spy agent intelligence object"""
    target_channel: str = Field(..., description="Target channel ID or name")
    competitor_data: Dict[str, Any] = Field(..., description="Competitor analysis data")
    content_gaps: List[str] = Field(default_factory=list, description="Identified content gaps")
    audience_insights: Dict[str, Any] = Field(default_factory=dict, description="Audience insights")
    successful_strategies: List[str] = Field(default_factory=list, description="Successful competitor strategies")
    weakness_analysis: Dict[str, Any] = Field(default_factory=dict, description="Weakness analysis")
    opportunity_score: float = Field(..., ge=0, le=10, description="Opportunity score 0-10")
    espionage_method: str = Field(..., description="Method used for intelligence gathering")
    data_freshness: datetime = Field(..., description="Data freshness timestamp")
    risk_assessment: Dict[str, Any] = Field(default_factory=dict, description="Risk assessment")

class GhostIntelligence(BaseIntelligenceObject):
    """Ghost agent intelligence object"""
    persona_name: str = Field(..., description="Ghost persona name")
    target_video: str = Field(..., description="Target video ID")
    engagement_strategy: str = Field(..., description="Engagement strategy used")
    comment_content: str = Field(..., description="Generated comment content")
    timing_strategy: Dict[str, Any] = Field(..., description="Timing strategy")
    interaction_type: str = Field(..., description="Type of interaction (comment, like, share)")
    organic_trust_score: float = Field(..., ge=0, le=10, description="Organic trust score 0-10")
    stealth_level: str = Field(..., description="Stealth level achieved")
    detection_risk: float = Field(..., ge=0, le=10, description="Detection risk score 0-10")
    conversation_thread: Optional[str] = Field(None, description="Conversation thread ID")
    reply_chain: List[str] = Field(default_factory=list, description="Reply chain history")

class GrowthIntelligence(BaseIntelligenceObject):
    """Growth agent intelligence object"""
    campaign_type: str = Field(..., description="Type of growth campaign")
    target_metrics: Dict[str, Any] = Field(..., description="Target metrics for campaign")
    current_performance: Dict[str, Any] = Field(..., description="Current performance data")
    growth_rate: float = Field(..., ge=-100, le=1000, description="Growth rate %")
    viral_coefficient: float = Field(..., ge=0, le=10, description="Viral coefficient")
    engagement_velocity: float = Field(..., ge=0, description="Engagement velocity per hour")
    conversion_rate: float = Field(..., ge=0, le=100, description="Conversion rate %")
    roi_metrics: Dict[str, Any] = Field(default_factory=dict, description="ROI metrics")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Optimization suggestions")
    scaling_potential: float = Field(..., ge=0, le=10, description="Scaling potential score 0-10")

class DecisionObject(BaseModel):
    """Decision object for empire orchestrator"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique decision ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Decision timestamp")
    intelligence_id: str = Field(..., description="Related intelligence object ID")
    decision_type: str = Field(..., description="Type of decision made")
    action: str = Field(..., description="Action to be taken")
    confidence_threshold: float = Field(..., description="Confidence threshold used")
    reasoning: str = Field(..., description="Reasoning behind decision")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    execution_plan: Dict[str, Any] = Field(default_factory=dict, description="Execution plan")
    status: str = Field(default="pending", description="Decision status")
    co_founder_notified: bool = Field(default=False, description="Co-founder notified flag")
    execution_result: Optional[Dict[str, Any]] = Field(None, description="Execution result")

class ConsultationObject(BaseModel):
    """Consultation object for co-founder interaction"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique consultation ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Consultation timestamp")
    intelligence_id: str = Field(..., description="Related intelligence object ID")
    agent: AgentType = Field(..., description="Requesting agent")
    confidence_score: float = Field(..., description="Confidence score")
    data_summary: str = Field(..., description="Data summary for consultation")
    question: str = Field(..., description="Question for co-founder")
    options: List[Dict[str, str]] = Field(..., description="Response options")
    status: str = Field(default="awaiting_response", description="Consultation status")
    response: Optional[str] = Field(None, description="Co-founder response")
    response_timestamp: Optional[datetime] = Field(None, description="Response timestamp")
    timeout_minutes: int = Field(default=30, description="Timeout in minutes")

class PerformanceMetrics(BaseModel):
    """Performance metrics for empire monitoring"""
    timestamp: datetime = Field(default_factory=datetime.now, description="Metrics timestamp")
    total_intelligence_objects: int = Field(default=0, description="Total intelligence objects")
    active_campaigns: int = Field(default=0, description="Active campaigns")
    success_rate: float = Field(default=0, description="Overall success rate %")
    autonomous_decisions: int = Field(default=0, description="Autonomous decisions count")
    human_consultations: int = Field(default=0, description="Human consultations count")
    avg_confidence: float = Field(default=0, description="Average confidence score")
    processing_time_avg: float = Field(default=0, description="Average processing time")
    agent_performance: Dict[str, Any] = Field(default_factory=dict, description="Agent performance metrics")
    empire_health: str = Field(default="healthy", description="Empire health status")

class EmpireMetrics(BaseModel):
    """Empire-wide metrics"""
    total_channels: int = Field(default=0, description="Total channels managed")
    active_channels: int = Field(default=0, description="Active channels count")
    monthly_revenue: float = Field(default=0, description="Monthly revenue $")
    total_subscribers: int = Field(default=0, description="Total subscribers across channels")
    total_views: int = Field(default=0, description="Total views across channels")
    engagement_rate: float = Field(default=0, description="Average engagement rate %")
    viral_videos: int = Field(default=0, description="Number of viral videos")
    conversion_rate: float = Field(default=0, description="Average conversion rate %")
    roi: float = Field(default=0, description="Return on investment")
    growth_rate: float = Field(default=0, description="Monthly growth rate %")
    operational_efficiency: float = Field(default=0, description="Operational efficiency %")

# Type aliases for better readability
IntelligenceObject = Union[
    ScriptIntelligence,
    MediaIntelligence,
    SEOIntelligence,
    UploadIntelligence,
    SpyIntelligence,
    GhostIntelligence,
    GrowthIntelligence
]

# Factory functions for creating intelligence objects
def create_script_intelligence(
    agent: AgentType,
    confidence_score: float,
    script_data: Dict[str, Any],
    priority: PriorityLevel = PriorityLevel.NORMAL
) -> ScriptIntelligence:
    """Create script intelligence object"""
    
    confidence = ConfidenceLevel(score=confidence_score)
    
    return ScriptIntelligence(
        agent=agent,
        confidence=confidence,
        data=script_data,
        priority=priority,
        script_type=script_data.get("type", "educational"),
        word_count=script_data.get("word_count", 0),
        seo_keywords=script_data.get("seo_keywords", []),
        hook_strength=script_data.get("hook_strength", 5.0),
        viral_potential=script_data.get("viral_potential", 5.0),
        emotional_tone=script_data.get("emotional_tone", "neutral"),
        target_audience=script_data.get("target_audience", "general"),
        content_pillar=script_data.get("content_pillar", "general"),
        estimated_duration=script_data.get("estimated_duration", 300),
        script_structure=script_data.get("script_structure", {}),
        engagement_hooks=script_data.get("engagement_hooks", [])
    )

def create_media_intelligence(
    agent: AgentType,
    confidence_score: float,
    media_data: Dict[str, Any],
    priority: PriorityLevel = PriorityLevel.NORMAL
) -> MediaIntelligence:
    """Create media intelligence object"""
    
    confidence = ConfidenceLevel(score=confidence_score)
    
    return MediaIntelligence(
        agent=agent,
        confidence=confidence,
        data=media_data,
        priority=priority,
        resolution=media_data.get("resolution", "1920x1080"),
        fps=media_data.get("fps", 30),
        duration=media_data.get("duration", 0),
        quality_score=media_data.get("quality_score", 7.0),
        shadowban_shield=media_data.get("shadowban_shield", True),
        file_size_mb=media_data.get("file_size_mb", 0),
        codec=media_data.get("codec", "h264"),
        bitrate=media_data.get("bitrate"),
        color_grading=media_data.get("color_grading", {}),
        audio_quality=media_data.get("audio_quality", {}),
        rendering_time=media_data.get("rendering_time"),
        device_metadata=media_data.get("device_metadata", {})
    )

def create_seo_intelligence(
    agent: AgentType,
    confidence_score: float,
    seo_data: Dict[str, Any],
    priority: PriorityLevel = PriorityLevel.NORMAL
) -> SEOIntelligence:
    """Create SEO intelligence object"""
    
    confidence = ConfidenceLevel(score=confidence_score)
    
    return SEOIntelligence(
        agent=agent,
        confidence=confidence,
        data=seo_data,
        priority=priority,
        title_score=seo_data.get("title_score", 7.0),
        description_score=seo_data.get("description_score", 7.0),
        tag_relevance=seo_data.get("tag_relevance", 7.0),
        thumbnail_optimized=seo_data.get("thumbnail_optimized", False),
        estimated_ctr=seo_data.get("estimated_ctr", 5.0),
        keyword_density=seo_data.get("keyword_density", 5.0),
        competition_analysis=seo_data.get("competition_analysis", {}),
        trend_alignment=seo_data.get("trend_alignment", 5.0),
        search_volume=seo_data.get("search_volume", {}),
        ranking_potential=seo_data.get("ranking_potential", 5.0),
        optimization_suggestions=seo_data.get("optimization_suggestions", [])
    )

def create_upload_intelligence(
    agent: AgentType,
    confidence_score: float,
    upload_data: Dict[str, Any],
    priority: PriorityLevel = PriorityLevel.NORMAL
) -> UploadIntelligence:
    """Create upload intelligence object"""
    
    confidence = ConfidenceLevel(score=confidence_score)
    
    return UploadIntelligence(
        agent=agent,
        confidence=confidence,
        data=upload_data,
        priority=priority,
        upload_speed=upload_data.get("upload_speed", 10.0),
        success_rate=upload_data.get("success_rate", 95.0),
        platform_compliance=upload_data.get("platform_compliance", True),
        metadata_integrity=upload_data.get("metadata_integrity", True),
        upload_method=upload_data.get("upload_method", "api"),
        retry_count=upload_data.get("retry_count", 0),
        chunk_size=upload_data.get("chunk_size"),
        proxy_used=upload_data.get("proxy_used"),
        user_agent=upload_data.get("user_agent"),
        upload_duration=upload_data.get("upload_duration"),
        error_codes=upload_data.get("error_codes", [])
    )

def create_consultation_object(
    intelligence_id: str,
    agent: AgentType,
    confidence_score: float,
    data_summary: str,
    question: str,
    options: List[Dict[str, str]] = None
) -> ConsultationObject:
    """Create consultation object"""
    
    if options is None:
        options = [
            {"id": "approve", "label": "Otonom Yürüt"},
            {"id": "modify", "label": "Revize Et"},
            {"id": "reject", "label": "Reddet"}
        ]
    
    return ConsultationObject(
        intelligence_id=intelligence_id,
        agent=agent,
        confidence_score=confidence_score,
        data_summary=data_summary,
        question=question,
        options=options
    )
