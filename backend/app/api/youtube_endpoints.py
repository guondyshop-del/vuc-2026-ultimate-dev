"""
VUC-2026 YouTube API Endpoints
Complete REST API endpoints for YouTube integration
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import asyncio
import json

from ..services.youtube_api_service import youtube_service, YouTubeVideo, YouTubeChannel, YouTubePlaylist
from ..services.youtube_auth_service import youtube_auth_service, UserProfile
from ..services.youtube_upload_service import youtube_upload_service, VideoMetadata, ThumbnailOptions
from ..services.youtube_analytics_service import youtube_analytics_service, VideoAnalytics, ChannelAnalytics
from ..services.vuc_youtube_neural_core import vuc_youtube_neural_core, ContentStrategy, TrendingPattern, CompetitiveInsight

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/youtube", tags=["youtube"])

# === AUTHENTICATION ENDPOINTS ===

@router.get("/auth/url")
async def get_auth_url():
    """Get OAuth 2.0 authorization URL"""
    try:
        auth_data = youtube_auth_service.get_authorization_url()
        return {
            "success": True,
            "data": auth_data
        }
    except Exception as e:
        logger.error(f"Error getting auth URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/callback")
async def auth_callback(code: str, state: str):
    """Handle OAuth 2.0 callback"""
    try:
        token = await youtube_auth_service.exchange_code_for_tokens(code, state)
        if token:
            return {
                "success": True,
                "message": "Authentication successful",
                "state": state
            }
        else:
            raise HTTPException(status_code=400, detail="Authentication failed")
    except Exception as e:
        logger.error(f"Error in auth callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auth/profile/{state}")
async def get_user_profile(state: str):
    """Get authenticated user profile"""
    try:
        profile = await youtube_auth_service.get_user_profile(state)
        if profile:
            return {
                "success": True,
                "data": {
                    "channel_id": profile.channel_id,
                    "channel_title": profile.channel_title,
                    "thumbnail_url": profile.thumbnail_url,
                    "subscriber_count": profile.subscriber_count
                }
            }
        else:
            raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/revoke/{state}")
async def revoke_token(state: str):
    """Revoke OAuth token"""
    try:
        success = await youtube_auth_service.revoke_token(state)
        return {
            "success": success,
            "message": "Token revoked" if success else "Token revocation failed"
        }
    except Exception as e:
        logger.error(f"Error revoking token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === SEARCH ENDPOINTS ===

@router.get("/search")
async def search_videos(
    q: str,
    max_results: int = 25,
    order: str = "relevance",
    duration: Optional[str] = None,
    published_after: Optional[datetime] = None,
    published_before: Optional[datetime] = None
):
    """Search for YouTube videos"""
    try:
        videos = await youtube_service.search_videos(
            query=q,
            max_results=max_results,
            order=order,
            duration=duration,
            published_after=published_after,
            published_before=published_before
        )
        
        return {
            "success": True,
            "data": {
                "videos": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "channel_title": video.channel_title,
                        "published_at": video.published_at.isoformat(),
                        "duration": video.duration,
                        "view_count": video.view_count,
                        "like_count": video.like_count,
                        "comment_count": video.comment_count,
                        "tags": video.tags,
                        "thumbnail_url": video.thumbnail_url,
                        "embed_url": video.embed_url
                    }
                    for video in videos
                ],
                "total_results": len(videos)
            }
        }
    except Exception as e:
        logger.error(f"Error searching videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos/{video_id}")
async def get_video_details(video_id: str):
    """Get detailed video information"""
    try:
        videos = await youtube_service.get_video_details([video_id])
        if not videos:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video = videos[0]
        return {
            "success": True,
            "data": {
                "video_id": video.video_id,
                "title": video.title,
                "description": video.description,
                "channel_id": video.channel_id,
                "channel_title": video.channel_title,
                "published_at": video.published_at.isoformat(),
                "duration": video.duration,
                "view_count": video.view_count,
                "like_count": video.like_count,
                "comment_count": video.comment_count,
                "tags": video.tags,
                "category_id": video.category_id,
                "thumbnail_url": video.thumbnail_url,
                "embed_url": video.embed_url
            }
        }
    except Exception as e:
        logger.error(f"Error getting video details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels/{channel_id}")
async def get_channel_details(channel_id: str):
    """Get detailed channel information"""
    try:
        channel = await youtube_service.get_channel_details(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        return {
            "success": True,
            "data": {
                "channel_id": channel.channel_id,
                "title": channel.title,
                "description": channel.description,
                "subscriber_count": channel.subscriber_count,
                "video_count": channel.video_count,
                "view_count": channel.view_count,
                "thumbnail_url": channel.thumbnail_url,
                "country": channel.country,
                "published_at": channel.published_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting channel details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels/{channel_id}/videos")
async def get_channel_videos(channel_id: str, max_results: int = 25):
    """Get videos from a channel"""
    try:
        videos = await youtube_service.get_channel_videos(channel_id, max_results)
        
        return {
            "success": True,
            "data": {
                "videos": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "published_at": video.published_at.isoformat(),
                        "duration": video.duration,
                        "view_count": video.view_count,
                        "like_count": video.like_count,
                        "comment_count": video.comment_count,
                        "thumbnail_url": video.thumbnail_url
                    }
                    for video in videos
                ],
                "total_results": len(videos)
            }
        }
    except Exception as e:
        logger.error(f"Error getting channel videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/playlists/{playlist_id}")
async def get_playlist_details(playlist_id: str):
    """Get detailed playlist information"""
    try:
        playlist = await youtube_service.get_playlist_details(playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        
        return {
            "success": True,
            "data": {
                "playlist_id": playlist.playlist_id,
                "title": playlist.title,
                "description": playlist.description,
                "channel_id": playlist.channel_id,
                "channel_title": playlist.channel_title,
                "video_count": playlist.video_count,
                "thumbnail_url": playlist.thumbnail_url,
                "published_at": playlist.published_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting playlist details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/playlists/{playlist_id}/videos")
async def get_playlist_videos(playlist_id: str, max_results: int = 25):
    """Get videos from a playlist"""
    try:
        videos = await youtube_service.get_playlist_videos(playlist_id, max_results)
        
        return {
            "success": True,
            "data": {
                "videos": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "published_at": video.published_at.isoformat(),
                        "duration": video.duration,
                        "view_count": video.view_count,
                        "like_count": video.like_count,
                        "comment_count": video.comment_count,
                        "thumbnail_url": video.thumbnail_url
                    }
                    for video in videos
                ],
                "total_results": len(videos)
            }
        }
    except Exception as e:
        logger.error(f"Error getting playlist videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending_videos(region_code: str = "US", category_id: Optional[str] = None):
    """Get trending videos"""
    try:
        videos = await youtube_service.get_trending_videos(region_code, category_id)
        
        return {
            "success": True,
            "data": {
                "videos": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "channel_title": video.channel_title,
                        "published_at": video.published_at.isoformat(),
                        "duration": video.duration,
                        "view_count": video.view_count,
                        "like_count": video.like_count,
                        "comment_count": video.comment_count,
                        "tags": video.tags,
                        "thumbnail_url": video.thumbnail_url
                    }
                    for video in videos
                ],
                "total_results": len(videos)
            }
        }
    except Exception as e:
        logger.error(f"Error getting trending videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_video_categories(region_code: str = "US"):
    """Get available video categories"""
    try:
        categories = await youtube_service.get_video_categories(region_code)
        
        return {
            "success": True,
            "data": {
                "categories": categories
            }
        }
    except Exception as e:
        logger.error(f"Error getting video categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === UPLOAD ENDPOINTS ===

@router.post("/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    category_id: str = Form("22"),
    privacy_status: str = Form("private"),
    made_for_kids: bool = Form(False),
    thumbnail_file: Optional[UploadFile] = File(None),
    state: Optional[str] = Form(None)
):
    """Upload video to YouTube"""
    try:
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        
        # Create metadata
        metadata = VideoMetadata(
            title=title,
            description=description,
            tags=tag_list,
            category_id=category_id,
            privacy_status=privacy_status,
            made_for_kids=made_for_kids
        )
        
        # Save uploaded files
        video_path = f"uploads/{video_file.filename}"
        with open(video_path, "wb") as buffer:
            content = await video_file.read()
            buffer.write(content)
        
        thumbnail_path = None
        if thumbnail_file:
            thumbnail_path = f"thumbnails/{thumbnail_file.filename}"
            with open(thumbnail_path, "wb") as buffer:
                content = await thumbnail_file.read()
                buffer.write(content)
        
        # Upload video
        result = await youtube_upload_service.upload_video(
            video_path=video_path,
            metadata=metadata,
            thumbnail_path=thumbnail_path,
            state=state
        )
        
        # Add cleanup task
        background_tasks.add_task(youtube_upload_service.cleanup_temp_files)
        
        return {
            "success": result["success"],
            "data": result if result["success"] else {"error": result.get("error")}
        }
        
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/videos/{video_id}/metadata")
async def update_video_metadata(
    video_id: str,
    title: str,
    description: str = "",
    tags: str = "",
    category_id: str = "22",
    privacy_status: str = "private",
    state: Optional[str] = None
):
    """Update video metadata"""
    try:
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        
        # Create metadata
        metadata = VideoMetadata(
            title=title,
            description=description,
            tags=tag_list,
            category_id=category_id,
            privacy_status=privacy_status
        )
        
        # Update metadata
        result = await youtube_upload_service.update_video_metadata(video_id, metadata, state)
        
        return {
            "success": result["success"],
            "data": result if result["success"] else {"error": result.get("error")}
        }
        
    except Exception as e:
        logger.error(f"Error updating video metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/upload/categories")
async def get_upload_categories():
    """Get available video categories for upload"""
    try:
        categories = await youtube_upload_service.get_video_categories()
        
        return {
            "success": True,
            "data": {
                "categories": categories
            }
        }
    except Exception as e:
        logger.error(f"Error getting upload categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate/video")
async def validate_video_file(video_file: UploadFile = File(...)):
    """Validate video file for upload"""
    try:
        # Save temporary file
        temp_path = f"temp/{video_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await video_file.read()
            buffer.write(content)
        
        # Validate file
        validation = await youtube_upload_service.validate_video_file(temp_path)
        
        # Clean up
        import os
        os.remove(temp_path)
        
        return {
            "success": validation["valid"],
            "data": validation
        }
        
    except Exception as e:
        logger.error(f"Error validating video file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === ANALYTICS ENDPOINTS ===

@router.get("/analytics/channel/{channel_id}")
async def get_channel_analytics(
    channel_id: str,
    start_date: datetime,
    end_date: datetime,
    state: Optional[str] = None
):
    """Get channel analytics"""
    try:
        analytics = await youtube_analytics_service.get_channel_analytics(
            channel_id, start_date, end_date, state
        )
        
        if not analytics:
            raise HTTPException(status_code=404, detail="Analytics not found")
        
        return {
            "success": True,
            "data": {
                "channel_id": analytics.channel_id,
                "channel_title": analytics.channel_title,
                "total_views": analytics.total_views,
                "total_subscribers": analytics.total_subscribers,
                "total_videos": analytics.total_videos,
                "watch_time_hours": analytics.watch_time_hours,
                "average_view_duration": analytics.average_view_duration,
                "subscriber_growth": analytics.subscriber_growth,
                "revenue_total": analytics.revenue_total,
                "top_videos": analytics.top_videos,
                "demographics": analytics.demographics
            }
        }
    except Exception as e:
        logger.error(f"Error getting channel analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analytics/videos")
async def get_video_analytics(
    video_ids: List[str],
    start_date: datetime,
    end_date: datetime,
    state: Optional[str] = None
):
    """Get analytics for specific videos"""
    try:
        analytics = await youtube_analytics_service.get_video_analytics(
            video_ids, start_date, end_date, state
        )
        
        return {
            "success": True,
            "data": {
                "videos": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "views": video.views,
                        "likes": video.likes,
                        "dislikes": video.dislikes,
                        "comments": video.comments,
                        "shares": video.shares,
                        "watch_time_minutes": video.watch_time_minutes,
                        "average_view_duration": video.average_view_duration,
                        "audience_retention": video.audience_retention,
                        "click_through_rate": video.click_through_rate,
                        "impressions": video.impressions,
                        "unique_viewers": video.unique_viewers,
                        "revenue": video.revenue,
                        "published_at": video.published_at.isoformat()
                    }
                    for video in analytics
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error getting video analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/channel/{channel_id}/realtime")
async def get_real_time_metrics(channel_id: str, state: Optional[str] = None):
    """Get real-time channel metrics"""
    try:
        metrics = await youtube_analytics_service.get_real_time_metrics(channel_id, state)
        
        return {
            "success": True,
            "data": metrics
        }
    except Exception as e:
        logger.error(f"Error getting real-time metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/channel/{channel_id}/top-videos")
async def get_top_performing_videos(
    channel_id: str,
    days: int = 30,
    metric: str = "views",
    state: Optional[str] = None
):
    """Get top performing videos"""
    try:
        top_videos = await youtube_analytics_service.get_top_performing_videos(
            channel_id, days, metric, state
        )
        
        return {
            "success": True,
            "data": {
                "top_videos": top_videos
            }
        }
    except Exception as e:
        logger.error(f"Error getting top performing videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analytics/videos/engagement")
async def get_engagement_metrics(
    video_ids: List[str],
    state: Optional[str] = None
):
    """Get engagement metrics for videos"""
    try:
        engagement = await youtube_analytics_service.get_engagement_metrics(video_ids, state)
        
        return {
            "success": True,
            "data": engagement
        }
    except Exception as e:
        logger.error(f"Error getting engagement metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/channel/{channel_id}/trends")
async def get_growth_trends(
    channel_id: str,
    days: int = 30,
    state: Optional[str] = None
):
    """Get growth trends"""
    try:
        trends = await youtube_analytics_service.get_growth_trends(channel_id, days, state)
        
        return {
            "success": True,
            "data": trends
        }
    except Exception as e:
        logger.error(f"Error getting growth trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/export")
async def export_analytics_report(
    channel_id: str,
    start_date: datetime,
    end_date: datetime,
    format: str = "csv",
    state: Optional[str] = None
):
    """Export analytics report"""
    try:
        report_path = await youtube_analytics_service.export_analytics_report(
            channel_id, start_date, end_date, format, state
        )
        
        if not report_path:
            raise HTTPException(status_code=500, detail="Failed to generate report")
        
        return {
            "success": True,
            "data": {
                "report_path": report_path,
                "format": format
            }
        }
    except Exception as e:
        logger.error(f"Error exporting analytics report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === NEURAL CORE ENDPOINTS ===

@router.post("/neural/strategy")
async def generate_content_strategy(
    video_topic: str,
    target_audience: Dict[str, Any],
    competitor_analysis: bool = True
):
    """Generate AI-optimized content strategy"""
    try:
        strategy = await vuc_youtube_neural_core.generate_content_strategy(
            video_topic, target_audience, competitor_analysis
        )
        
        return {
            "success": True,
            "data": {
                "title_optimization": strategy.title_optimization,
                "description_optimization": strategy.description_optimization,
                "tags_optimization": strategy.tags_optimization,
                "thumbnail_suggestions": strategy.thumbnail_suggestions,
                "publish_timing": strategy.publish_timing.isoformat(),
                "target_audience": strategy.target_audience,
                "predicted_performance": strategy.predicted_performance,
                "confidence_score": strategy.confidence_score
            }
        }
    except Exception as e:
        logger.error(f"Error generating content strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/neural/trends")
async def analyze_trending_patterns(region: str = "US", category: Optional[str] = None):
    """Analyze current trending patterns"""
    try:
        patterns = await vuc_youtube_neural_core.analyze_trending_patterns(region, category)
        
        return {
            "success": True,
            "data": {
                "patterns": [
                    {
                        "pattern_type": pattern.pattern_type,
                        "keywords": pattern.keywords,
                        "topics": pattern.topics,
                        "duration_trend": pattern.duration_trend,
                        "style_preferences": pattern.style_preferences,
                        "engagement_factors": pattern.engagement_factors,
                        "virality_score": pattern.virality_score,
                        "time_sensitivity": pattern.time_sensitivity
                    }
                    for pattern in patterns
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error analyzing trending patterns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/neural/competition/{channel_id}")
async def competitive_analysis(channel_id: str):
    """Analyze competitive landscape"""
    try:
        insights = await vuc_youtube_neural_core.competitive_analysis(channel_id)
        
        return {
            "success": True,
            "data": {
                "insights": [
                    {
                        "competitor_channel": insight.competitor_channel,
                        "top_performing_content": insight.top_performing_content,
                        "content_gaps": insight.content_gaps,
                        "engagement_strategies": insight.engagement_strategies,
                        "market_position": insight.market_position,
                        "opportunity_score": insight.opportunity_score
                    }
                    for insight in insights
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error in competitive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === HEALTH AND STATUS ENDPOINTS ===

@router.get("/health")
async def get_api_health():
    """Get YouTube API health status"""
    try:
        health = await youtube_service.get_api_health()
        
        return {
            "success": True,
            "data": health
        }
    except Exception as e:
        logger.error(f"Error getting API health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_service_status():
    """Get overall YouTube service status"""
    try:
        status = {
            "api_service": "running",
            "auth_service": "running",
            "upload_service": "running",
            "analytics_service": "running",
            "neural_core": "running",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "data": status
        }
    except Exception as e:
        logger.error(f"Error getting service status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === UTILITY ENDPOINTS ===

@router.post("/neural/save-state")
async def save_neural_state():
    """Save neural network state"""
    try:
        await vuc_youtube_neural_core.save_neural_state()
        
        return {
            "success": True,
            "message": "Neural state saved successfully"
        }
    except Exception as e:
        logger.error(f"Error saving neural state: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
