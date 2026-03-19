"""
VUC-2026 Core Schemas
Pydantic v2 strict validation for all data models
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class BaseResponse(BaseModel):
    """Base response model with strict typing"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    success: bool = True
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class VideoStatus(str, Enum):
    """Video pipeline status with strict enumeration"""
    PLANNING = "planning"
    SCRIPTING = "scripting"
    ASSETS = "assets"
    RENDERING = "rendering"
    UPLOADING = "uploading"
    PUBLISHED = "published"
    FAILED = "failed"


class UploadStatus(str, Enum):
    """YouTube upload status"""
    DRAFT = "draft"
    UPLOADED = "uploaded"
    PUBLISHED = "published"
    FAILED = "failed"


class VideoCreateRequest(BaseModel):
    """Strict video creation schema"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    channel_id: int = Field(..., gt=0, description="Channel ID must be positive")
    title: str = Field(..., min_length=1, max_length=500, description="Video title")
    description: Optional[str] = Field(None, max_length=5000, description="Video description")
    tags: Optional[List[str]] = Field(default_factory=list, description="Video tags")
    category: Optional[str] = Field(None, max_length=100, description="Video category")
    language: str = Field(default="TR", pattern="^[A-Z]{2}$", description="ISO language code")
    script_id: Optional[int] = Field(None, gt=0, description="Associated script ID")
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValueError("All tags must be non-empty strings")
                if len(tag) > 50:
                    raise ValueError("Each tag must be max 50 characters")
        return v


class VideoResponse(BaseModel):
    """Strict video response schema"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid',
        from_attributes=True
    )
    
    id: int
    channel_id: int
    title: str
    description: Optional[str]
    tags: Optional[List[str]]
    category: Optional[str]
    language: str
    
    # Video metadata
    duration: Optional[float] = Field(None, ge=0, description="Duration in seconds")
    file_path: Optional[str]
    thumbnail_path: Optional[str]
    file_size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    
    # YouTube metadata
    youtube_id: Optional[str] = Field(None, pattern="^[A-Za-z0-9_-]{11}$", description="YouTube video ID")
    upload_status: UploadStatus
    published_at: Optional[datetime]
    
    # Analytics
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    watch_time_minutes: float = Field(default=0.0, ge=0)
    ctr: float = Field(default=0.0, ge=0, le=1)
    retention_rate: float = Field(default=0.0, ge=0, le=1)
    
    # Grey-hat features
    is_reused_content: bool = False
    frame_jitter_applied: bool = False
    pixel_noise_applied: bool = False
    speed_variance_applied: bool = False
    
    # A/B Testing
    thumbnail_version: str = Field(default="A", pattern="^[A-Z]$", description="Thumbnail version")
    thumbnail_a_ctr: float = Field(default=0.0, ge=0, le=1)
    thumbnail_b_ctr: float = Field(default=0.0, ge=0, le=1)
    
    # Production pipeline
    script_id: Optional[int]
    status: VideoStatus
    progress: int = Field(default=0, ge=0, le=100, description="Progress percentage")
    
    created_at: datetime
    updated_at: Optional[datetime]


class VideoListResponse(BaseResponse):
    """Video list response with pagination"""
    videos: List[VideoResponse]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)


class ErrorResponse(BaseModel):
    """Standardized error response"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    success: bool = False
    error_code: str
    error_message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheckResponse(BaseModel):
    """System health check response"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    status: Literal["healthy", "degraded", "unhealthy"]
    database: Literal["connected", "disconnected", "error"]
    redis: Literal["connected", "disconnected", "error"]
    celery: Literal["running", "stopped", "error"]
    version: str
    uptime_seconds: float = Field(..., ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EmpireAuditLog(BaseModel):
    """Empire Auditor log entry"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    id: Optional[int] = None
    event_type: str = Field(..., min_length=1, max_length=100)
    severity: Literal["low", "medium", "high", "critical"]
    component: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1, max_length=1000)
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ProcessingTask(BaseModel):
    """Video processing task schema"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    task_id: str
    video_id: int
    task_type: Literal["render", "upload", "thumbnail", "metadata"]
    status: Literal["pending", "running", "completed", "failed"]
    progress: int = Field(default=0, ge=0, le=100)
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=1, le=10)
