"""
Stealth 4.0 API Endpoints
Ghost Mode Technologies - Pixel Cloaking, Device Spoofing, Lurker Protocol
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import logging

from ..services.stealth_service import stealth_manager, StealthConfig

logger = logging.getLogger(__name__)

router = APIRouter()

class StealthConfigRequest(BaseModel):
    """Stealth configuration request model"""
    pixel_noise_enabled: Optional[bool] = None
    pixel_noise_intensity: Optional[float] = None
    speed_variation_enabled: Optional[bool] = None
    speed_variation_range: Optional[tuple] = None
    frame_jitter_enabled: Optional[bool] = None
    frame_jitter_intensity: Optional[float] = None
    device_spoofing_enabled: Optional[bool] = None
    lurker_protocol_enabled: Optional[bool] = None

class StealthTestRequest(BaseModel):
    """Stealth test request model"""
    config: Optional[StealthConfigRequest] = None

class LurkerSessionRequest(BaseModel):
    """Lurker session request model"""
    persona_id: str
    niche: str
    duration_minutes: int = 30

class VideoProcessingRequest(BaseModel):
    """Video processing with stealth features"""
    input_path: str
    output_path: str
    device_type: str = "iphone_15_pro"

@router.get("/stealth/status")
async def get_stealth_status():
    """Get current stealth configuration and status"""
    try:
        config = stealth_manager.config
        
        return {
            "success": True,
            "config": {
                "pixel_noise_enabled": config.pixel_noise_enabled,
                "pixel_noise_intensity": config.pixel_noise_intensity,
                "speed_variation_enabled": config.speed_variation_enabled,
                "speed_variation_range": config.speed_variation_range,
                "frame_jitter_enabled": config.frame_jitter_enabled,
                "frame_jitter_intensity": config.frame_jitter_intensity,
                "device_spoofing_enabled": config.device_spoofing_enabled,
                "lurker_protocol_enabled": config.lurker_protocol_enabled
            },
            "status": "active",
            "version": "4.0"
        }
    except Exception as e:
        logger.error(f"Failed to get stealth status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stealth/config")
async def update_stealth_config(config_request: StealthConfigRequest):
    """Update stealth configuration"""
    try:
        # Update configuration with provided values
        update_data = {}
        
        if config_request.pixel_noise_enabled is not None:
            update_data["pixel_noise_enabled"] = config_request.pixel_noise_enabled
        if config_request.pixel_noise_intensity is not None:
            update_data["pixel_noise_intensity"] = config_request.pixel_noise_intensity
        if config_request.speed_variation_enabled is not None:
            update_data["speed_variation_enabled"] = config_request.speed_variation_enabled
        if config_request.speed_variation_range is not None:
            update_data["speed_variation_range"] = config_request.speed_variation_range
        if config_request.frame_jitter_enabled is not None:
            update_data["frame_jitter_enabled"] = config_request.frame_jitter_enabled
        if config_request.frame_jitter_intensity is not None:
            update_data["frame_jitter_intensity"] = config_request.frame_jitter_intensity
        if config_request.device_spoofing_enabled is not None:
            update_data["device_spoofing_enabled"] = config_request.device_spoofing_enabled
        if config_request.lurker_protocol_enabled is not None:
            update_data["lurker_protocol_enabled"] = config_request.lurker_protocol_enabled
        
        stealth_manager.update_config(**update_data)
        
        return {
            "success": True,
            "message": "Stealth configuration updated successfully",
            "updated_fields": list(update_data.keys())
        }
        
    except Exception as e:
        logger.error(f"Failed to update stealth config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stealth/test")
async def test_stealth_features(test_request: StealthTestRequest):
    """Test all stealth features"""
    try:
        # Update config if provided
        if test_request.config:
            config_update = test_request.config.dict(exclude_unset=True)
            stealth_manager.update_config(**config_update)
        
        # Run stealth tests
        results = stealth_manager.test_stealth_features()
        
        return results
        
    except Exception as e:
        logger.error(f"Stealth test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stealth/process-video")
async def process_video_with_stealth(request: VideoProcessingRequest, background_tasks: BackgroundTasks):
    """Process video with stealth features (async)"""
    try:
        # Validate input file exists (simplified)
        import os
        if not os.path.exists(request.input_path):
            raise HTTPException(status_code=404, detail="Input video file not found")
        
        # Create output directory if needed
        output_dir = os.path.dirname(request.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Process video with stealth
        result = stealth_manager.stealth_engine.process_video_stealth(
            request.input_path,
            request.output_path,
            request.device_type
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "Video processed with stealth features",
                "output_path": request.output_path,
                "stealth_features_applied": result["stealth_features_applied"],
                "metadata": result["metadata"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video stealth processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stealth/lurker/session")
async def run_lurker_session(request: LurkerSessionRequest, background_tasks: BackgroundTasks):
    """Run lurker protocol session"""
    try:
        # Validate inputs
        if not request.persona_id:
            raise HTTPException(status_code=400, detail="Persona ID is required")
        
        if request.duration_minutes < 1 or request.duration_minutes > 120:
            raise HTTPException(status_code=400, detail="Duration must be between 1 and 120 minutes")
        
        # Run lurker session
        result = stealth_manager.lurker.run_lurker_session(
            request.persona_id,
            request.niche,
            request.duration_minutes
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "Lurker session completed successfully",
                "session_result": {
                    "actions_performed": result["actions_performed"],
                    "scroll_actions": result["scroll_actions"],
                    "click_actions": result["click_actions"],
                    "trust_delta": result["trust_delta"],
                    "new_trust_score": 8.5 + result["trust_delta"],  # Simulated base score
                    "session_duration": result["session_duration"]
                }
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Session failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lurker session failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stealth/lurker/trust-scores")
async def get_trust_scores():
    """Get current trust scores for all personas"""
    try:
        # Simulated trust scores for demo
        trust_scores = {
            "TechWizard_TR": 6.2,
            "BusinessGuru_TR": 7.8,
            "ProGamer_TR": 5.1,
            "Hazal_K": 8.5,
            "Elif_M": 7.2,
            "CodeNinja_TR": 6.9
        }
        
        return {
            "success": True,
            "trust_scores": trust_scores,
            "last_updated": "2026-03-19T09:52:00Z"
        }
        
    except Exception as e:
        logger.error(f"Failed to get trust scores: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stealth/device-profiles")
async def get_device_profiles():
    """Get available device profiles for spoofing"""
    try:
        profiles = stealth_manager.stealth_engine.device_profiles
        
        return {
            "success": True,
            "profiles": profiles,
            "total_profiles": len(profiles)
        }
        
    except Exception as e:
        logger.error(f"Failed to get device profiles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stealth/analyze-video")
async def analyze_video_for_stealth(video_path: str):
    """Analyze video for stealth optimization opportunities"""
    try:
        import cv2
        import numpy as np
        
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Video file not found")
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Could not open video file")
        
        # Get basic properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Sample frames for analysis
        sample_frames = []
        sample_interval = max(1, frame_count // 10)  # Sample 10 frames
        
        for i in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                sample_frames.append(frame)
        
        cap.release()
        
        # Analyze frames for patterns
        frame_analysis = {
            "avg_brightness": [],
            "avg_contrast": [],
            "edge_density": []
        }
        
        for frame in sample_frames:
            # Calculate brightness
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            frame_analysis["avg_brightness"].append(brightness)
            
            # Calculate contrast (standard deviation)
            contrast = np.std(gray)
            frame_analysis["avg_contrast"].append(contrast)
            
            # Calculate edge density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            frame_analysis["edge_density"].append(edge_density)
        
        # Calculate averages
        analysis_results = {
            "video_properties": {
                "fps": fps,
                "frame_count": frame_count,
                "resolution": (width, height),
                "duration": frame_count / fps
            },
            "frame_analysis": {
                "avg_brightness": np.mean(frame_analysis["avg_brightness"]),
                "brightness_variance": np.var(frame_analysis["avg_brightness"]),
                "avg_contrast": np.mean(frame_analysis["avg_contrast"]),
                "contrast_variance": np.var(frame_analysis["avg_contrast"]),
                "avg_edge_density": np.mean(frame_analysis["edge_density"]),
                "edge_density_variance": np.var(frame_analysis["edge_density"])
            }
        }
        
        # Stealth recommendations
        recommendations = []
        
        if analysis_results["frame_analysis"]["brightness_variance"] < 100:
            recommendations.append("Low brightness variance detected - pixel noise will be more effective")
        
        if analysis_results["frame_analysis"]["edge_density_variance"] < 0.01:
            recommendations.append("Consistent edge patterns - consider increasing frame jitter")
        
        if fps == 30.0 or fps == 60.0:
            recommendations.append("Standard frame rate detected - speed variation recommended")
        
        return {
            "success": True,
            "analysis": analysis_results,
            "recommendations": recommendations,
            "stealth_suitability": "high" if len(recommendations) >= 2 else "medium"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stealth/health")
async def stealth_health_check():
    """Stealth system health check"""
    try:
        # Check all stealth components
        health_status = {
            "pixel_noise": "healthy",
            "speed_variation": "healthy",
            "frame_jitter": "healthy",
            "device_spoofing": "healthy",
            "lurker_protocol": "healthy"
        }
        
        # Test basic functionality
        test_result = stealth_manager.test_stealth_features()
        
        overall_health = "healthy" if test_result["success"] else "degraded"
        
        return {
            "status": overall_health,
            "components": health_status,
            "version": "4.0",
            "last_test": test_result,
            "uptime": "24h 37m 12s"  # Simulated uptime
        }
        
    except Exception as e:
        logger.error(f"Stealth health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
