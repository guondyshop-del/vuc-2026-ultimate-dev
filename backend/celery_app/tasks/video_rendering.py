"""
VUC-2026 Video Rendering Tasks with Self-Healing
Production-ready video rendering with auto-recovery mechanisms
"""

import os
import logging
from celery import Celery
from typing import Dict, Any, Optional
from datetime import datetime

from app.services.self_healing_service import self_healing_service, self_healing_retry
from app.services.media_engine import MediaEngine
from app.services.directml_accelerator import DirectMLAccelerator
from app.services.grey_hat_service import GreyHatService

logger = logging.getLogger(__name__)

# Celery app instance
celery_app = Celery('vuc2026')

# Render retry policy from .windsurfrules
RENDER_RETRY_POLICY = {
    "max_retries": 3,
    "retry_delay": 30,
    "exponential_backoff": True,
    "fallback_strategy": "reduce_quality"
}

@celery_app.task(bind=True, max_retries=None)
def render_video_task(self, script_data: Dict[str, Any], 
                     channel_config: Dict[str, Any],
                     quality_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Render video with self-healing capabilities
    
    Args:
        script_data: Script data with title, content, etc.
        channel_config: Channel configuration
        quality_settings: Optional quality settings for fallback
        
    Returns:
        Render result with success status and file paths
    """
    
    def _render_video_with_healing():
        """Internal render function with all logic"""
        try:
            logger.info(f"Starting video render: {script_data.get('title', 'Untitled')}")
            
            # Initialize services
            media_engine = MediaEngine()
            directml_accelerator = DirectMLAccelerator()
            grey_hat_service = GreyHatService()
            
            # Quality settings (with fallback support)
            if not quality_settings:
                quality_settings = {
                    "resolution": "1080p",
                    "fps": 30,
                    "bitrate": "5M",
                    "quality": "high"
                }
            
            # Step 1: Fetch stock media
            logger.info("Fetching stock media...")
            media_files = media_engine.fetch_stock_media(
                query=script_data.get("title", ""),
                media_type="video",
                count=3
            )
            
            if not media_files:
                raise Exception("No stock media files available")
            
            # Step 2: Optimize media with DirectML
            logger.info("Optimizing media files...")
            optimized_media = []
            
            for media_file in media_files:
                if directml_accelerator.is_available:
                    # Enhance media quality
                    enhanced_media = f"enhanced_{os.path.basename(media_file)}"
                    enhancement_result = directml_accelerator.accelerate_image_processing(
                        media_file, enhanced_media, "enhance"
                    )
                    
                    if enhancement_result.get("success"):
                        optimized_media.append(enhanced_media)
                        logger.info(f"Media enhanced with DirectML: {enhanced_media}")
                    else:
                        optimized_media.append(media_file)
                        logger.warning(f"DirectML enhancement failed, using original: {media_file}")
                else:
                    optimized_media.append(media_file)
            
            # Step 3: Create thumbnail
            logger.info("Creating thumbnail...")
            thumbnail_path = media_engine.create_thumbnail(
                title=script_data.get("title", ""),
                style="hormozi"
            )
            
            # Step 4: Render video
            logger.info(f"Rendering video at {quality_settings['resolution']}...")
            video_path = media_engine.render_video(
                script_data=script_data,
                media_files=optimized_media,
                quality_settings=quality_settings
            )
            
            if not video_path or not os.path.exists(video_path):
                raise Exception("Video render failed - no output file")
            
            # Step 5: Apply DirectML enhancement if available
            if directml_accelerator.is_available:
                logger.info("Applying DirectML video enhancement...")
                enhanced_video = f"enhanced_{os.path.basename(video_path)}"
                enhancement_result = directml_accelerator.accelerate_video_processing(
                    video_path, enhanced_video, "enhance"
                )
                
                if enhancement_result.get("success"):
                    video_path = enhanced_video
                    logger.info(f"Video enhanced with DirectML: {enhancement_result}")
                else:
                    logger.warning(f"DirectML video enhancement failed, using original")
            
            # Step 6: Apply Shadowban Shield
            logger.info("Applying Shadowban Shield...")
            shielded_video = grey_hat_service.apply_algorithm_shield(video_path)
            
            if not os.path.exists(shielded_video):
                raise Exception("Shadowban Shield application failed")
            
            # Success - return results
            render_result = {
                "success": True,
                "video_path": shielded_video,
                "thumbnail_path": thumbnail_path,
                "script_id": script_data.get("id"),
                "title": script_data.get("title", "Untitled"),
                "duration": script_data.get("estimated_duration", 300),
                "quality_settings": quality_settings,
                "directml_used": directml_accelerator.is_available,
                "shadowban_shield_applied": True,
                "file_size": os.path.getsize(shielded_video),
                "render_time": datetime.now().isoformat()
            }
            
            logger.info(f"Video render completed successfully: {shielded_video}")
            return render_result
            
        except Exception as e:
            logger.error(f"Video render failed: {str(e)}")
            raise e
    
    # Execute with self-healing
    healing_result = self_healing_service.retry_with_backoff(
        _render_video_with_healing,
        RENDER_RETRY_POLICY,
        "video_render"
    )
    
    # Log recovery event if fallback was applied
    if not healing_result.get("success") and healing_result.get("fallback_applied"):
        self_healing_service.log_recovery_event(
            operation_type="video_render",
            original_error=str(healing_result.get("error", "Unknown error")),
            recovery_action=healing_result.get("fallback_applied", "unknown"),
            success=False
        )
    
    return healing_result

@celery_app.task(bind=True)
def render_video_with_fallback_task(self, script_data: Dict[str, Any], 
                                  channel_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render video with automatic quality fallback
    
    This task automatically reduces quality if render fails
    """
    
    quality_levels = [
        {"resolution": "1080p", "fps": 30, "bitrate": "5M", "quality": "high"},
        {"resolution": "720p", "fps": 30, "bitrate": "3M", "quality": "medium"},
        {"resolution": "480p", "fps": 25, "bitrate": "2M", "quality": "low"},
        {"resolution": "360p", "fps": 24, "bitrate": "1M", "quality": "minimal"}
    ]
    
    for i, quality_settings in enumerate(quality_levels):
        logger.info(f"Attempting render with quality: {quality_settings['quality']} ({quality_settings['resolution']})")
        
        try:
            result = render_video_task.apply_async(
                args=[script_data, channel_config, quality_settings],
                queue='render_queue'
            ).get(timeout=1800)  # 30 minutes timeout
            
            if result.get("success"):
                logger.info(f"Render successful with quality: {quality_settings['quality']}")
                
                # Log successful fallback if not first attempt
                if i > 0:
                    self_healing_service.log_recovery_event(
                        operation_type="video_render_fallback",
                        original_error=f"High quality render failed, fell back to {quality_settings['quality']}",
                        recovery_action=f"quality_reduced_to_{quality_settings['quality']}",
                        success=True
                    )
                
                return result
            
        except Exception as e:
            logger.warning(f"Render failed with quality {quality_settings['quality']}: {str(e)}")
            
            # If this is the last quality level, give up
            if i == len(quality_levels) - 1:
                logger.error("All quality levels failed - render cannot be completed")
                
                # Log final failure
                self_healing_service.log_recovery_event(
                    operation_type="video_render_final_failure",
                    original_error=str(e),
                    recovery_action="all_quality_levels_failed",
                    success=False
                )
                
                return {
                    "success": False,
                    "error": f"All quality levels failed: {str(e)}",
                    "fallback_attempts": len(quality_levels),
                    "operation_type": "video_render"
                }
    
    # This should never be reached
    return {
        "success": False,
        "error": "Unexpected error in render fallback",
        "operation_type": "video_render"
    }

@celery_app.task
def cleanup_render_temp_files_task(video_path: str, thumbnail_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Clean up temporary render files
    
    Args:
        video_path: Path to video file
        thumbnail_path: Optional path to thumbnail file
        
    Returns:
        Cleanup result
    """
    
    try:
        cleaned_files = []
        
        # Clean up video file if it exists
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            cleaned_files.append(video_path)
            logger.info(f"Cleaned up video file: {video_path}")
        
        # Clean up thumbnail if provided
        if thumbnail_path and os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            cleaned_files.append(thumbnail_path)
            logger.info(f"Cleaned up thumbnail file: {thumbnail_path}")
        
        return {
            "success": True,
            "cleaned_files": cleaned_files,
            "cleanup_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "operation_type": "cleanup_temp_files"
        }

@celery_app.task
def optimize_video_for_upload_task(video_path: str, target_size_mb: int = 100) -> Dict[str, Any]:
    """
    Optimize video for upload by reducing file size if needed
    
    Args:
        video_path: Path to video file
        target_size_mb: Target file size in MB
        
    Returns:
        Optimization result
    """
    
    try:
        # Check current file size
        current_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        
        if current_size_mb <= target_size_mb:
            logger.info(f"Video size already optimal: {current_size_mb:.1f}MB")
            return {
                "success": True,
                "optimized": False,
                "original_size_mb": current_size_mb,
                "final_size_mb": current_size_mb,
                "video_path": video_path
            }
        
        logger.info(f"Optimizing video from {current_size_mb:.1f}MB to target {target_size_mb}MB")
        
        # Use MediaEngine to optimize
        media_engine = MediaEngine()
        optimized_path = media_engine.optimize_video_for_upload(
            video_path, target_size_mb
        )
        
        if optimized_path and os.path.exists(optimized_path):
            final_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
            
            logger.info(f"Video optimized: {current_size_mb:.1f}MB -> {final_size_mb:.1f}MB")
            
            return {
                "success": True,
                "optimized": True,
                "original_size_mb": current_size_mb,
                "final_size_mb": final_size_mb,
                "video_path": optimized_path,
                "compression_ratio": current_size_mb / final_size_mb
            }
        else:
            raise Exception("Video optimization failed - no output file")
            
    except Exception as e:
        logger.error(f"Video optimization failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "operation_type": "video_optimization"
        }
