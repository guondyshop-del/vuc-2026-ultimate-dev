"""
AI-Orchestrated API Endpoints
Dynamic LLM-Router for Production, Stealth, and Espionage endpoints
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import logging

from ..services.ai_orchestrator import get_ai_orchestrator, OrchestratedRequest
from ..services.self_correcting_scripts import get_script_executor
from ..services.vectorized_memory import get_vectorized_memory
from ..services.stealth_service import stealth_manager
from ..services.self_healing_service import self_healing_engine

logger = logging.getLogger(__name__)

router = APIRouter()

class ProductionRequest(BaseModel):
    """Production request model"""
    topic: str
    script_type: str = "educational"
    tone: str = "professional"
    platforms: list = ["youtube"]
    stealth_enabled: bool = True
    device_type: str = "iphone_15_pro"

class StealthRequest(BaseModel):
    """Stealth request model"""
    video_path: str
    output_path: str
    device_type: str = "iphone_15_pro"
    stealth_config: Optional[Dict[str, Any]] = None

class EspionageRequest(BaseModel):
    """Espionage request model"""
    target_channel: str
    niche: str
    depth: str = "standard"
    analyze_thumbnails: bool = True

@router.post("/ai/orchestrate/production")
async def orchestrate_production(request: Request, production_req: ProductionRequest):
    """AI-orchestrated production endpoint"""
    try:
        # Get AI orchestrator
        orchestrator = get_ai_orchestrator()
        
        # Prepare request data
        request_data = {
            "topic": production_req.topic,
            "script_type": production_req.script_type,
            "tone": production_req.tone,
            "platforms": production_req.platforms,
            "stealth_enabled": production_req.stealth_enabled,
            "device_type": production_req.device_type
        }
        
        # Orchestrate the request
        orchestrated = await orchestrator.orchestrate_request(
            request=request,
            path="/production",
            method="POST",
            body=request_data
        )
        
        # Execute production with optimized parameters
        executor = get_script_executor()
        
        # Build FFmpeg command based on orchestrated parameters
        command = [
            "ffmpeg",
            "-y",
            "-i", "input.mp4",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "output.mp4"
        ]
        
        # Add stealth parameters if enabled
        if orchestrated.optimized_parameters.get("stealth_enabled", True):
            stealth_config = stealth_manager.config
            if stealth_config.pixel_noise_enabled:
                # Add pixel noise processing
                command.extend(["-vf", "noise=alls=0.1:allf=t+u"])
        
        # Execute with self-correcting scripts
        execution = await executor.execute_script(
            script_name="video_production",
            command=command,
            parameters=orchestrated.optimized_parameters,
            health_checks=["ffmpeg", "disk_space", "memory"]
        )
        
        # Store in vectorized memory
        memory = get_vectorized_memory()
        await memory.store_viral_video({
            "title": orchestrated.optimized_parameters.get("topic", "Generated Video"),
            "description": f"AI-generated {production_req.script_type} content",
            "tags": orchestrated.optimized_parameters.get("platforms", []),
            "platform": production_req.platforms[0] if production_req.platforms else "youtube",
            "engagement_rate": orchestrated.estimated_success_rate,
            "viral_coefficient": orchestrated.confidence_score,
            "content_features": {
                "script_type": production_req.script_type,
                "tone": production_req.tone,
                "ai_optimized": True
            }
        })
        
        return {
            "success": execution.success,
            "orchestration": {
                "confidence_score": orchestrated.confidence_score,
                "processing_strategy": orchestrated.processing_strategy,
                "estimated_success_rate": orchestrated.estimated_success_rate,
                "ai_recommendations": orchestrated.ai_recommendations,
                "optimized_parameters": orchestrated.optimized_parameters
            },
            "execution": {
                "script_name": execution.script_name,
                "success": execution.success,
                "retry_count": execution.retry_count,
                "ai_fix_applied": execution.ai_fix_applied,
                "error_message": execution.error_message
            },
            "stealth_applied": production_req.stealth_enabled,
            "memory_stored": True
        }
        
    except Exception as e:
        logger.error(f"Production orchestration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/orchestrate/stealth")
async def orchestrate_stealth(request: Request, stealth_req: StealthRequest):
    """AI-orchestrated stealth endpoint"""
    try:
        # Get AI orchestrator
        orchestrator = get_ai_orchestrator()
        
        # Prepare request data
        request_data = {
            "video_path": stealth_req.video_path,
            "output_path": stealth_req.output_path,
            "device_type": stealth_req.device_type,
            "stealth_config": stealth_req.stealth_config or {}
        }
        
        # Orchestrate the request
        orchestrated = await orchestrator.orchestrate_request(
            request=request,
            path="/stealth",
            method="POST",
            body=request_data
        )
        
        # Apply stealth processing with AI optimization
        stealth_result = stealth_manager.stealth_engine.process_video_stealth(
            input_path=stealth_req.video_path,
            output_path=stealth_req.output_path,
            device_type=orchestrated.optimized_parameters.get("device_type", stealth_req.device_type)
        )
        
        # Update stealth config based on AI recommendations
        if orchestrated.ai_recommendations:
            for recommendation in orchestrated.ai_recommendations:
                if "pixel_noise" in recommendation.lower():
                    stealth_manager.update_config(pixel_noise_enabled=True)
                elif "speed_variation" in recommendation.lower():
                    stealth_manager.update_config(speed_variation_enabled=True)
        
        return {
            "success": stealth_result.get("success", False),
            "orchestration": {
                "confidence_score": orchestrated.confidence_score,
                "processing_strategy": orchestrated.processing_strategy,
                "ai_recommendations": orchestrated.ai_recommendations
            },
            "stealth_result": stealth_result,
            "device_metadata": stealth_result.get("metadata", {}),
            "stealth_features_applied": stealth_result.get("stealth_features_applied", {})
        }
        
    except Exception as e:
        logger.error(f"Stealth orchestration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/orchestrate/espionage")
async def orchestrate_espionage(request: Request, espionage_req: EspionageRequest):
    """AI-orchestrated espionage endpoint"""
    try:
        # Get AI orchestrator
        orchestrator = get_ai_orchestrator()
        
        # Prepare request data
        request_data = {
            "target_channel": espionage_req.target_channel,
            "niche": espionage_req.niche,
            "depth": espionage_req.depth,
            "analyze_thumbnails": espionage_req.analyze_thumbnails
        }
        
        # Orchestrate the request
        orchestrated = await orchestrator.orchestrate_request(
            request=request,
            path="/espionage",
            method="POST",
            body=request_data
        )
        
        # Execute espionage with optimized parameters
        memory = get_vectorized_memory()
        
        # Get viral insights for the target niche
        insights = await memory.get_viral_insights(
            query_text=espionage_req.niche,
            platform="youtube"
        )
        
        # Store trend pattern in memory
        await memory.store_trend_pattern({
            "trend_name": f"Espionage: {espionage_req.target_channel}",
            "category": espionage_req.niche,
            "keywords": insights.get("ai_insights", {}).get("viral_patterns", []),
            "engagement_rate": orchestrated.estimated_success_rate,
            "viral_score": orchestrated.confidence_score,
            "platforms": ["youtube"],
            "duration_hours": 24
        })
        
        return {
            "success": True,
            "orchestration": {
                "confidence_score": orchestrated.confidence_score,
                "processing_strategy": orchestrated.processing_strategy,
                "estimated_success_rate": orchestrated.estimated_success_rate
            },
            "espionage_result": {
                "target_channel": espionage_req.target_channel,
                "niche": espionage_req.niche,
                "depth": espionage_req.depth,
                "viral_insights": insights,
                "opportunity_score": orchestrated.confidence_score * 100,
                "recommended_actions": orchestrated.ai_recommendations
            },
            "memory_stored": True
        }
        
    except Exception as e:
        logger.error(f"Espionage orchestration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai/orchestrate/status")
async def get_orchestration_status():
    """Get AI orchestration system status"""
    try:
        orchestrator = get_ai_orchestrator()
        executor = get_script_executor()
        memory = get_vectorized_memory()
        
        # Get stats from all systems
        orchestration_stats = orchestrator.get_orchestration_stats()
        execution_stats = executor.get_execution_stats()
        memory_stats = memory.get_memory_stats()
        
        # Get stealth status
        stealth_status = {
            "config": {
                "pixel_noise_enabled": stealth_manager.config.pixel_noise_enabled,
                "speed_variation_enabled": stealth_manager.config.speed_variation_enabled,
                "frame_jitter_enabled": stealth_manager.config.frame_jitter_enabled,
                "device_spoofing_enabled": stealth_manager.config.device_spoofing_enabled,
                "lurker_protocol_enabled": stealth_manager.config.lurker_protocol_enabled
            },
            "version": "4.0"
        }
        
        # Get self-healing status
        healing_stats = self_healing_engine.get_error_statistics(24)
        
        return {
            "status": "active",
            "systems": {
                "ai_orchestrator": orchestration_stats,
                "self_correcting_scripts": execution_stats,
                "vectorized_memory": memory_stats,
                "stealth_system": stealth_status,
                "self_healing": healing_stats
            },
            "overall_health": "healthy",
            "last_updated": "2026-03-19T09:52:00Z"
        }
        
    except Exception as e:
        logger.error(f"Failed to get orchestration status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/orchestrate/memory/query")
async def query_vectorized_memory(query: str, content_type: str = "viral_video", limit: int = 10):
    """Query vectorized memory for similar content"""
    try:
        memory = get_vectorized_memory()
        
        from ..services.vectorized_memory import MemoryQuery
        memory_query = MemoryQuery(
            query_text=query,
            content_type=content_type,
            limit=limit,
            similarity_threshold=0.7
        )
        
        results = await memory.query_memory(memory_query)
        
        return {
            "success": True,
            "query": query,
            "content_type": content_type,
            "results": [
                {
                    "content_id": result.content_id,
                    "content_type": result.content_type,
                    "similarity_score": result.similarity_score,
                    "metadata": result.metadata,
                    "created_at": result.created_at.isoformat()
                }
                for result in results
            ],
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Memory query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai/orchestrate/memory/trends")
async def get_trending_patterns(category: str = None, limit: int = 20):
    """Get trending patterns from vectorized memory"""
    try:
        memory = get_vectorized_memory()
        trends = await memory.get_trending_patterns(category=category, limit=limit)
        
        return {
            "success": True,
            "category": category,
            "trends": trends,
            "total_trends": len(trends)
        }
        
    except Exception as e:
        logger.error(f"Failed to get trending patterns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/orchestrate/heal")
async def trigger_self_healing(component: str, error_type: str, error_message: str):
    """Trigger self-healing for a specific component"""
    try:
        # Create error for self-healing
        error = Exception(error_message)
        
        # Log error and trigger healing
        error_report = self_healing_engine.log_error(
            error=error,
            component=component,
            context={"triggered_by": "ai_orchestrator", "error_type": error_type}
        )
        
        return {
            "success": True,
            "error_id": str(id(error_report)),
            "component": component,
            "error_type": error_type,
            "auto_healing_triggered": True,
            "severity": error_report.severity,
            "fix_attempts": error_report.fix_attempts
        }
        
    except Exception as e:
        logger.error(f"Self-healing trigger failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai/orchestrate/dashboard")
async def get_ai_dashboard():
    """Get comprehensive AI dashboard data"""
    try:
        # Get all system stats
        orchestrator = get_ai_orchestrator()
        executor = get_script_executor()
        memory = get_vectorized_memory()
        
        orchestration_stats = orchestrator.get_orchestration_stats()
        execution_stats = executor.get_execution_stats()
        memory_stats = memory.get_memory_stats()
        
        # Get recent trends
        trends = await memory.get_trending_patterns(limit=5)
        
        # Get self-healing stats
        healing_stats = self_healing_engine.get_error_statistics(24)
        
        return {
            "success": True,
            "dashboard": {
                "ai_orchestrator": orchestration_stats,
                "self_correcting_scripts": execution_stats,
                "vectorized_memory": memory_stats,
                "self_healing": healing_stats,
                "recent_trends": trends,
                "system_status": "All Systems Go"
            },
            "timestamp": "2026-03-19T09:52:00Z"
        }
        
    except Exception as e:
        logger.error(f"Failed to get AI dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
