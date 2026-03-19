"""
VUC-2026 Google Cloud Integration API
Comprehensive Google Cloud services integration for YouTube Empire Management
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, List, Optional, Any
import asyncio
import logging
import os

from ..services.vertex_ai_service import vertex_ai_service
from ..services.bigtable_service import bigtable_service
from ..services.bigquery_service import bigquery_service
from ..services.bigquery_transfer_service import bigquery_transfer_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/google-cloud", tags=["Google Cloud"])

@router.post("/vertex-ai/analyze-video")
async def analyze_youtube_video(
    video_url: str,
    analysis_type: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Analyze YouTube video using Vertex AI Gemini
    
    Args:
        video_url: YouTube video URL
        analysis_type: Type of analysis (comprehensive, summary, transcript, metadata)
    """
    try:
        result = await vertex_ai_service.analyze_youtube_video(video_url, analysis_type)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error in video analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vertex-ai/generate-content")
async def generate_content_from_video(
    video_url: str,
    content_type: str = "blog_post"
) -> Dict[str, Any]:
    """
    Generate new content based on YouTube video analysis
    
    Args:
        video_url: YouTube video URL
        content_type: Type of content to generate
    """
    try:
        result = await vertex_ai_service.generate_content_from_video(video_url, content_type)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vertex-ai/viral-analysis")
async def viral_content_analysis(video_url: str) -> Dict[str, Any]:
    """
    Specialized viral content analysis for YouTube optimization
    """
    try:
        result = await vertex_ai_service.viral_content_analysis(video_url)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error in viral analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vertex-ai/competitor-analysis")
async def competitor_analysis(competitor_videos: List[str]) -> Dict[str, Any]:
    """
    Analyze competitor videos for strategic insights
    """
    try:
        if len(competitor_videos) > 10:
            raise HTTPException(status_code=400, detail="Too many videos. Maximum 10 allowed.")
        
        result = await vertex_ai_service.competitor_analysis(competitor_videos)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error in competitor analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigtable/initialize")
async def initialize_bigtable() -> Dict[str, Any]:
    """Initialize Bigtable database and tables"""
    try:
        success = await bigtable_service.initialize_database()
        
        if success:
            return {
                "success": True,
                "message": "Bigtable database initialized successfully",
                "tables_created": list(bigtable_service.table_configs.keys())
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize Bigtable")
        
    except Exception as e:
        logger.error(f"Error initializing Bigtable: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigtable/store-video")
async def store_video_metadata(
    video_data: Dict[str, Any],
    track_changes: bool = True
) -> Dict[str, Any]:
    """
    Store video metadata with change tracking
    
    Args:
        video_data: Video metadata dictionary
        track_changes: Whether to track changes over time
    """
    try:
        success = await bigtable_service.store_video_metadata(video_data, track_changes)
        
        if success:
            return {
                "success": True,
                "message": "Video metadata stored successfully",
                "video_id": video_data.get("video_id")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store video metadata")
        
    except Exception as e:
        logger.error(f"Error storing video metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigtable/store-analytics-event")
async def store_analytics_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Store analytics events for real-time processing"""
    try:
        success = await bigtable_service.store_analytics_event(event_data)
        
        if success:
            return {
                "success": True,
                "message": "Analytics event stored successfully",
                "event_type": event_data.get("event_type")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store analytics event")
        
    except Exception as e:
        logger.error(f"Error storing analytics event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bigtable/video-analytics/{video_id}")
async def get_video_analytics(
    video_id: str,
    include_history: bool = False
) -> Dict[str, Any]:
    """
    Retrieve video analytics with optional historical data
    
    Args:
        video_id: YouTube video ID
        include_history: Whether to include change history
    """
    try:
        analytics = await bigtable_service.get_video_analytics(video_id, include_history)
        
        if analytics:
            return {
                "success": True,
                "video_id": video_id,
                "analytics": analytics,
                "include_history": include_history
            }
        else:
            return {
                "success": True,
                "video_id": video_id,
                "analytics": {},
                "include_history": include_history,
                "message": "No analytics data found"
            }
        
    except Exception as e:
        logger.error(f"Error retrieving video analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigquery/initialize")
async def initialize_bigquery() -> Dict[str, Any]:
    """Initialize BigQuery dataset and tables"""
    try:
        success = await bigquery_service.initialize_dataset()
        
        if success:
            return {
                "success": True,
                "message": "BigQuery dataset initialized successfully",
                "tables_created": list(bigquery_service.table_schemas.keys())
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize BigQuery")
        
    except Exception as e:
        logger.error(f"Error initializing BigQuery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigquery/setup-transfer")
async def setup_youtube_data_transfer(channel_ids: List[str]) -> Dict[str, Any]:
    """
    Setup YouTube Data Transfer Service for automated data collection
    
    Args:
        channel_ids: List of YouTube channel IDs to monitor
    """
    try:
        if len(channel_ids) > 50:
            raise HTTPException(status_code=400, detail="Too many channels. Maximum 50 allowed.")
        
        result = await bigquery_service.setup_youtube_data_transfer(channel_ids)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error setting up data transfer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigquery/channel-data")
async def insert_channel_data(channel_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert channel basic data into BigQuery"""
    try:
        success = await bigquery_service.insert_channel_data(channel_data)
        
        if success:
            return {
                "success": True,
                "message": "Channel data inserted successfully",
                "channel_id": channel_data.get("id")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to insert channel data")
        
    except Exception as e:
        logger.error(f"Error inserting channel data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigquery/video-data")
async def insert_video_performance(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert video performance data into BigQuery"""
    try:
        success = await bigquery_service.insert_video_performance(video_data)
        
        if success:
            return {
                "success": True,
                "message": "Video data inserted successfully",
                "video_id": video_data.get("id")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to insert video data")
        
    except Exception as e:
        logger.error(f"Error inserting video data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bigquery/top-videos/{channel_id}")
async def get_top_performing_videos(
    channel_id: str,
    days: int = 30,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Get top performing videos for a channel
    
    Args:
        channel_id: YouTube channel ID
        days: Number of days to analyze
        limit: Maximum number of videos to return
    """
    try:
        if days > 365:
            raise HTTPException(status_code=400, detail="Days parameter too large. Maximum 365 days.")
        
        if limit > 50:
            raise HTTPException(status_code=400, detail="Limit parameter too large. Maximum 50 videos.")
        
        videos = await bigquery_service.get_top_performing_videos(channel_id, days, limit)
        
        return {
            "success": True,
            "channel_id": channel_id,
            "period_days": days,
            "videos": videos,
            "count": len(videos)
        }
        
    except Exception as e:
        logger.error(f"Error getting top videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bigquery/growth-metrics/{channel_id}")
async def get_channel_growth_metrics(
    channel_id: str,
    days: int = 90
) -> Dict[str, Any]:
    """
    Get comprehensive channel growth metrics
    
    Args:
        channel_id: YouTube channel ID
        days: Number of days to analyze
    """
    try:
        if days > 365:
            raise HTTPException(status_code=400, detail="Days parameter too large. Maximum 365 days.")
        
        metrics = await bigquery_service.get_channel_growth_metrics(channel_id, days)
        
        if metrics:
            return {
                "success": True,
                "channel_id": channel_id,
                "period_days": days,
                "metrics": metrics
            }
        else:
            return {
                "success": True,
                "channel_id": channel_id,
                "period_days": days,
                "metrics": {},
                "message": "No data found for the specified period"
            }
        
    except Exception as e:
        logger.error(f"Error getting growth metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bigquery/custom-query")
async def execute_custom_query(query: str) -> Dict[str, Any]:
    """
    Execute custom analytics query
    
    Args:
        query: SQL query string
    """
    try:
        # Basic query validation (prevent dangerous operations)
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE"]
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                raise HTTPException(status_code=400, detail=f"Query contains forbidden keyword: {keyword}")
        
        if not query.strip().upper().startswith("SELECT"):
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
        
        results = await bigquery_service.execute_analytics_query(query)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error executing custom query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_google_cloud_status() -> Dict[str, Any]:
    """Get status of all Google Cloud services"""
    try:
        transfer_status = await bigquery_transfer_service.get_service_status()
        
        status = {
            "vertex_ai": "configured",
            "bigtable": "ready",
            "bigquery": "ready",
            "bigquery_transfer": transfer_status,
            "cloud_storage": "configured",
            "monitoring": "enabled",
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", "karacocuk"),
            "location": os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        }
        
        return {
            "success": True,
            "services": status,
            "message": "All Google Cloud services are configured and ready"
        }
        
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# BigQuery Data Transfer Service Endpoints
@router.post("/transfer/create-youtube-config")
async def create_youtube_transfer_config(channel_ids: List[str]) -> Dict[str, Any]:
    """
    Create YouTube Analytics data transfer configuration
    
    Args:
        channel_ids: List of YouTube channel IDs to monitor
    """
    try:
        if len(channel_ids) > 50:
            raise HTTPException(status_code=400, detail="Too many channels. Maximum 50 allowed.")
        
        result = await bigquery_transfer_service.create_youtube_transfer_config(channel_ids)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error creating YouTube transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transfer/configs")
async def list_transfer_configs() -> Dict[str, Any]:
    """List all transfer configurations in the project"""
    try:
        configs = await bigquery_transfer_service.list_transfer_configs()
        
        return {
            "success": True,
            "configurations": configs,
            "count": len(configs)
        }
        
    except Exception as e:
        logger.error(f"Error listing transfer configs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transfer/config/{config_name}")
async def get_transfer_config(config_name: str) -> Dict[str, Any]:
    """
    Get details of a specific transfer configuration
    
    Args:
        config_name: Name of the transfer configuration
    """
    try:
        result = await bigquery_transfer_service.get_transfer_config(config_name)
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/transfer/config/{config_name}")
async def update_transfer_config(config_name: str, channel_ids: List[str]) -> Dict[str, Any]:
    """
    Update transfer configuration with new channel IDs
    
    Args:
        config_name: Name of the transfer configuration
        channel_ids: Updated list of YouTube channel IDs
    """
    try:
        if len(channel_ids) > 50:
            raise HTTPException(status_code=400, detail="Too many channels. Maximum 50 allowed.")
        
        result = await bigquery_transfer_service.update_transfer_config(config_name, channel_ids)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error updating transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transfer/config/{config_name}/disable")
async def disable_transfer_config(config_name: str) -> Dict[str, Any]:
    """
    Disable a transfer configuration
    
    Args:
        config_name: Name of the transfer configuration
    """
    try:
        result = await bigquery_transfer_service.disable_transfer_config(config_name)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error disabling transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transfer/config/{config_name}/enable")
async def enable_transfer_config(config_name: str) -> Dict[str, Any]:
    """
    Enable a transfer configuration
    
    Args:
        config_name: Name of the transfer configuration
    """
    try:
        result = await bigquery_transfer_service.enable_transfer_config(config_name)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error enabling transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/transfer/config/{config_name}")
async def delete_transfer_config(config_name: str) -> Dict[str, Any]:
    """
    Delete a transfer configuration
    
    Args:
        config_name: Name of the transfer configuration
    """
    try:
        result = await bigquery_transfer_service.delete_transfer_config(config_name)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error deleting transfer config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transfer/config/{config_name}/runs")
async def get_transfer_runs(config_name: str, days: int = 7) -> Dict[str, Any]:
    """
    Get recent transfer runs for a configuration
    
    Args:
        config_name: Name of the transfer configuration
        days: Number of days to look back
    """
    try:
        if days > 30:
            raise HTTPException(status_code=400, detail="Days parameter too large. Maximum 30 days.")
        
        runs = await bigquery_transfer_service.get_transfer_runs(config_name, days)
        
        return {
            "success": True,
            "config_name": config_name,
            "period_days": days,
            "runs": runs,
            "count": len(runs)
        }
        
    except Exception as e:
        logger.error(f"Error getting transfer runs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transfer/status")
async def get_transfer_service_status() -> Dict[str, Any]:
    """Get BigQuery Data Transfer service status"""
    try:
        status = await bigquery_transfer_service.get_service_status()
        return status
        
    except Exception as e:
        logger.error(f"Error getting transfer service status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
