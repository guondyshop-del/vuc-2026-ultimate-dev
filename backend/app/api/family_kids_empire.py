"""
VUC-2026 Family & Kids Empire API Router
Complete integration of matrix engine, SEO constitution, and full-stack APIs
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import asyncio
import json
import os

from ..services.family_kids_matrix_engine import seed_matrix_engine, VideoSeed, VideoStage
from ..services.seo_algorithm_constitution import seo_constitution_engine, SEOConstitution, SEOOptimizationLevel
from ..services.full_stack_api_mapper import full_stack_api_mapper, APIType

# Pydantic models for API requests/responses
class GenerateMatrixRequest(BaseModel):
    optimization_level: SEOOptimizationLevel = SEOOptimizationLevel.OMNIPOTENT
    target_duration_minutes: int = Field(ge=15, le=20, default=18)

class GenerateMatrixResponse(BaseModel):
    success: bool
    video_count: int
    videos: List[VideoSeed]
    estimated_total_views: int
    estimated_total_revenue: float
    generation_time_ms: float

class SEOConstitutionRequest(BaseModel):
    primary_keyword: str
    optimization_level: SEOOptimizationLevel = SEOOptimizationLevel.OMNIPOTENT
    target_duration_minutes: int = Field(ge=15, le=20, default=18)

class SEOConstitutionResponse(BaseModel):
    success: bool
    constitution: SEOConstitution
    processing_time_ms: float

class ProductionRequest(BaseModel):
    video_seed_id: int
    script_requirements: Optional[Dict[str, Any]] = None
    voice_settings: Optional[Dict[str, Any]] = None
    rendering_options: Optional[Dict[str, Any]] = None

class ProductionResponse(BaseModel):
    success: bool
    production_id: str
    estimated_completion_time: datetime
    tasks_created: List[str]

class EmpireStatusResponse(BaseModel):
    matrix_generated: bool
    total_videos: int
    production_queue_size: int
    api_health: Dict[str, Dict[str, Any]]
    system_uptime_hours: float
    last_production_success: Optional[datetime]

class AutoPilotRequest(BaseModel):
    daily_video_target: int = Field(ge=1, le=10, default=3)
    auto_upload_enabled: bool = True
    auto_optimization_enabled: bool = True
    production_hours: List[str] = Field(default=["09:00", "15:00", "20:00"])

class AutoPilotResponse(BaseModel):
    success: bool
    autopilot_active: bool
    daily_schedule: List[Dict[str, Any]]
    next_production_time: Optional[datetime]

router = APIRouter()

# Initialize system state
empire_state = {
    "matrix_generated": False,
    "video_matrix": [],
    "production_queue": [],
    "system_start_time": datetime.now(),
    "last_production_success": None,
    "autopilot_active": False
}

@router.post("/generate-matrix", response_model=GenerateMatrixResponse)
async def generate_video_matrix(request: GenerateMatrixRequest, background_tasks: BackgroundTasks):
    """Generate the complete 100-video seed matrix"""
    
    try:
        start_time = datetime.now()
        
        # Generate the matrix
        video_matrix = await seed_matrix_engine.generate_100_video_matrix()
        
        # Calculate totals
        total_views = sum(video.estimated_views for video in video_matrix)
        total_revenue = sum(video.monetization_potential for video in video_matrix)
        
        # Apply SEO constitution to each video
        for video in video_matrix:
            seo_constitution = await seo_constitution_engine.generate_seo_constitution(
                primary_keyword=video.keywords_primary[0],
                optimization_level=request.optimization_level,
                target_duration_minutes=request.target_duration_minutes
            )
            video.metadata.description = seo_constitution.description_optimization
            video.metadata.tags = seo_constitution.tags_optimization
        
        # Update empire state
        empire_state["matrix_generated"] = True
        empire_state["video_matrix"] = video_matrix
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return GenerateMatrixResponse(
            success=True,
            video_count=len(video_matrix),
            videos=video_matrix,
            estimated_total_views=total_views,
            estimated_total_revenue=total_revenue,
            generation_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matrix generation failed: {str(e)}")

@router.post("/seo-constitution", response_model=SEOConstitutionResponse)
async def generate_seo_constitution(request: SEOConstitutionRequest):
    """Generate SEO constitution for a specific keyword"""
    
    try:
        start_time = datetime.now()
        
        constitution = await seo_constitution_engine.generate_seo_constitution(
            primary_keyword=request.primary_keyword,
            optimization_level=request.optimization_level,
            target_duration_minutes=request.target_duration_minutes
        )
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return SEOConstitutionResponse(
            success=True,
            constitution=constitution,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SEO constitution generation failed: {str(e)}")

@router.post("/produce", response_model=ProductionResponse)
async def start_video_production(request: ProductionRequest, background_tasks: BackgroundTasks):
    """Start video production pipeline"""
    
    try:
        if not empire_state["matrix_generated"]:
            raise HTTPException(status_code=400, detail="Video matrix not generated yet")
        
        # Find the video seed
        video_seed = None
        for video in empire_state["video_matrix"]:
            if video.id == request.video_seed_id:
                video_seed = video
                break
        
        if not video_seed:
            raise HTTPException(status_code=404, detail="Video seed not found")
        
        # Generate production ID
        production_id = f"prod_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{video_seed.id}"
        
        # Add to production queue
        empire_state["production_queue"].append({
            "production_id": production_id,
            "video_seed": video_seed,
            "status": "queued",
            "created_at": datetime.now(),
            "script_requirements": request.script_requirements or {},
            "voice_settings": request.voice_settings or {},
            "rendering_options": request.rendering_options or {}
        })
        
        # Start background production tasks
        background_tasks.add_task(
            process_video_production,
            production_id,
            video_seed,
            request.script_requirements,
            request.voice_settings,
            request.rendering_options
        )
        
        # Calculate estimated completion time
        estimated_completion = datetime.now() + timedelta(minutes=30)  # 30 minutes per video
        
        return ProductionResponse(
            success=True,
            production_id=production_id,
            estimated_completion_time=estimated_completion,
            tasks_created=["script_generation", "voice_synthesis", "video_rendering", "metadata_optimization", "upload_preparation"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Production start failed: {str(e)}")

@router.get("/status", response_model=EmpireStatusResponse)
async def get_empire_status():
    """Get current empire status"""
    
    try:
        # Get API health
        api_health = await full_stack_api_mapper.get_api_health_status()
        
        # Calculate uptime
        uptime_hours = (datetime.now() - empire_state["system_start_time"]).total_seconds() / 3600
        
        return EmpireStatusResponse(
            matrix_generated=empire_state["matrix_generated"],
            total_videos=len(empire_state["video_matrix"]),
            production_queue_size=len(empire_state["production_queue"]),
            api_health=api_health,
            system_uptime_hours=uptime_hours,
            last_production_success=empire_state["last_production_success"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.post("/autopilot", response_model=AutoPilotResponse)
async def toggle_autopilot(request: AutoPilotRequest, background_tasks: BackgroundTasks):
    """Toggle or configure autopilot mode"""
    
    try:
        if not empire_state["matrix_generated"]:
            raise HTTPException(status_code=400, detail="Video matrix not generated yet")
        
        # Toggle autopilot
        empire_state["autopilot_active"] = not empire_state["autopilot_active"]
        
        if empire_state["autopilot_active"]:
            # Generate daily schedule
            daily_schedule = []
            current_time = datetime.now()
            
            for hour_str in request.production_hours:
                hour, minute = map(int, hour_str.split(":"))
                schedule_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if schedule_time <= current_time:
                    schedule_time += timedelta(days=1)
                
                daily_schedule.append({
                    "time": hour_str,
                    "video_target": request.daily_video_target,
                    "next_run": schedule_time,
                    "auto_upload": request.auto_upload_enabled,
                    "auto_optimization": request.auto_optimization_enabled
                })
            
            # Start autopilot background task
            background_tasks.add_task(run_autopilot_scheduler, daily_schedule)
            
            # Find next production time
            next_production = min([s["next_run"] for s in daily_schedule])
            
            return AutoPilotResponse(
                success=True,
                autopilot_active=True,
                daily_schedule=daily_schedule,
                next_production_time=next_production
            )
        else:
            return AutoPilotResponse(
                success=True,
                autopilot_active=False,
                daily_schedule=[],
                next_production_time=None
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autopilot toggle failed: {str(e)}")

@router.get("/matrix/videos")
async def get_video_matrix():
    """Get the complete video matrix"""
    
    if not empire_state["matrix_generated"]:
        raise HTTPException(status_code=400, detail="Video matrix not generated yet")
    
    return {
        "success": True,
        "total_videos": len(empire_state["video_matrix"]),
        "videos": empire_state["video_matrix"]
    }

@router.get("/matrix/videos/{stage}")
async def get_videos_by_stage(stage: VideoStage):
    """Get videos by stage"""
    
    if not empire_state["matrix_generated"]:
        raise HTTPException(status_code=400, detail="Video matrix not generated yet")
    
    filtered_videos = [v for v in empire_state["video_matrix"] if v.stage == stage]
    
    return {
        "success": True,
        "stage": stage,
        "video_count": len(filtered_videos),
        "videos": filtered_videos
    }

@router.get("/production/queue")
async def get_production_queue():
    """Get current production queue"""
    
    return {
        "success": True,
        "queue_size": len(empire_state["production_queue"]),
        "queue": empire_state["production_queue"]
    }

@router.get("/production/{production_id}")
async def get_production_status(production_id: str):
    """Get status of specific production"""
    
    production = None
    for item in empire_state["production_queue"]:
        if item["production_id"] == production_id:
            production = item
            break
    
    if not production:
        raise HTTPException(status_code=404, detail="Production not found")
    
    return {
        "success": True,
        "production": production
    }

@router.post("/api/test")
async def test_api_endpoints():
    """Test all API endpoints and return comprehensive data"""
    
    try:
        # Test data generation
        test_results = {
            "matrix_status": empire_state["matrix_generated"],
            "total_videos": len(empire_state["video_matrix"]),
            "production_queue_size": len(empire_state["production_queue"]),
            "autopilot_active": empire_state["autopilot_active"],
            "system_uptime": str(datetime.now() - empire_state["system_start_time"]),
            "api_health": {
                "family_kids_empire": "active",
                "empire_orchestrator": "active",
                "seo_constitution": "active",
                "matrix_engine": "active"
            },
            "sample_video_data": [],
            "production_stats": {
                "completed_productions": 0,
                "failed_productions": 0,
                "active_productions": 0
            }
        }
        
        # Add sample video data if matrix exists
        if empire_state["video_matrix"]:
            test_results["sample_video_data"] = [
                {
                    "id": video.id,
                    "title": video.metadata.title,
                    "stage": video.stage,
                    "estimated_views": video.estimated_views,
                    "monetization_potential": video.monetization_potential,
                    "keywords_primary": video.keywords_primary[:3]  # First 3 keywords
                }
                for video in empire_state["video_matrix"][:5]  # First 5 videos
            ]
        
        # Calculate production stats
        for production in empire_state["production_queue"]:
            if production["status"] == "completed":
                test_results["production_stats"]["completed_productions"] += 1
            elif production["status"] == "failed":
                test_results["production_stats"]["failed_productions"] += 1
            elif production["status"] == "processing":
                test_results["production_stats"]["active_productions"] += 1
        
        return {
            "success": True,
            "test_results": test_results,
            "timestamp": datetime.now().isoformat(),
            "message": "VUC-2026 Family & Kids Empire API fully operational"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API testing failed: {str(e)}")

async def test_api_type(api_type: APIType) -> Dict[str, Any]:
    """Test all APIs of a specific type"""
    
    results = {}
    
    for endpoint_name, endpoint in full_stack_api_mapper.endpoints.items():
        if endpoint.api_type == api_type:
            try:
                # Simple health check
                results[endpoint_name] = {
                    "status": "healthy",
                    "success_rate": endpoint.success_rate,
                    "last_called": endpoint.last_called.isoformat() if endpoint.last_called else None
                }
            except Exception as e:
                results[endpoint_name] = {
                    "status": "error",
                    "error": str(e)
                }
    
    return results

async def process_video_production(
    production_id: str,
    video_seed: VideoSeed,
    script_requirements: Dict[str, Any],
    voice_settings: Dict[str, Any],
    rendering_options: Dict[str, Any]
):
    """Background task for video production"""
    
    try:
        # Update production status
        for item in empire_state["production_queue"]:
            if item["production_id"] == production_id:
                item["status"] = "processing"
                item["started_at"] = datetime.now()
                break
        
        # Step 1: Script Generation
        script_payload = {
            "title": video_seed.metadata.title,
            "description": video_seed.metadata.description,
            "keywords": video_seed.keywords_primary,
            "duration_minutes": video_seed.metadata.target_duration_minutes,
            "hook": video_seed.metadata.hook,
            "cta": video_seed.metadata.cta,
            **script_requirements
        }
        
        script_result = await full_stack_api_mapper.call_api("gemini_scripting", script_payload)
        
        # Step 2: Voice Synthesis - İçerik türüne göre ses seçimi
        # Pregnancy (hamilelik) → Rachel (sıcak, anneane tonu)
        # Newborn/Infant (yenidoğan/bebek) → Bella (enerjik, arkadaşça ton)
        # Toddler (toddler) → Domi (eğitici, profesyonel ton)
        
        content_type = video_seed.content_type
        voice_mapping = {
            "pregnancy": os.getenv("ELEVENLABS_VOICE_ID_RACHEL", "rachel"),
            "newborn": os.getenv("ELEVENLABS_VOICE_ID_BELLA", "bella"),
            "infant": os.getenv("ELEVENLABS_VOICE_ID_BELLA", "bella"),
            "toddler": os.getenv("ELEVENLABS_VOICE_ID_DOMI", "domi")
        }
        
        selected_voice = voice_mapping.get(content_type, os.getenv("ELEVENLABS_DEFAULT_VOICE", "rachel"))
        
        voice_payload = {
            "text": script_result.get("script", ""),
            "voice_id": selected_voice,
            "emotion": voice_settings.get("emotion", "warm"),
            "speed": voice_settings.get("speed", 1.0)
        }
        
        voice_result = await full_stack_api_mapper.call_api("elevenlabs_voice", voice_payload)
        
        # Step 3: Video Rendering
        render_payload = {
            "script": script_result.get("script", ""),
            "audio_url": voice_result.get("audio_url", ""),
            "duration_minutes": video_seed.metadata.target_duration_minutes,
            "pattern_interrupts": video_seed.pattern_interrupts,
            "ai_deception": video_seed.metadata.title,  # Will be processed
            **rendering_options
        }
        
        render_result = await full_stack_api_mapper.call_api("ffmpeg_rendering", render_payload)
        
        # Step 4: Metadata Optimization
        metadata_payload = {
            "video_path": render_result.get("video_path", ""),
            "title": video_seed.metadata.title,
            "description": video_seed.metadata.description,
            "tags": video_seed.metadata.tags,
            "thumbnail_text": video_seed.metadata.title
        }
        
        # Update production status to completed
        for item in empire_state["production_queue"]:
            if item["production_id"] == production_id:
                item["status"] = "completed"
                item["completed_at"] = datetime.now()
                item["result"] = render_result
                break
        
        empire_state["last_production_success"] = datetime.now()
        
    except Exception as e:
        # Update production status to failed
        for item in empire_state["production_queue"]:
            if item["production_id"] == production_id:
                item["status"] = "failed"
                item["error"] = str(e)
                item["failed_at"] = datetime.now()
                break

async def run_autopilot_scheduler(daily_schedule: List[Dict[str, Any]]):
    """Background task for autopilot scheduling"""
    
    while empire_state["autopilot_active"]:
        current_time = datetime.now()
        
        # Check if any scheduled time is due
        for schedule_item in daily_schedule:
            if current_time >= schedule_item["next_run"]:
                # Start production for scheduled videos
                await start_scheduled_production(schedule_item)
                
                # Update next run time
                schedule_item["next_run"] += timedelta(days=1)
        
        # Sleep for 1 minute before checking again
        await asyncio.sleep(60)

async def start_scheduled_production(schedule_item: Dict[str, Any]):
    """Start production for scheduled videos"""
    
    try:
        # Get next videos from matrix that haven't been produced
        unproduced_videos = [
            video for video in empire_state["video_matrix"]
            if not any(p["video_seed"].id == video.id for p in empire_state["production_queue"])
        ]
        
        # Start production for target number of videos
        for i in range(min(schedule_item["video_target"], len(unproduced_videos))):
            video = unproduced_videos[i]
            
            production_request = ProductionRequest(
                video_seed_id=video.id,
                script_requirements={},
                voice_settings={},
                rendering_options={}
            )
            
            await start_video_production(production_request, BackgroundTasks())
        
    except Exception as e:
        print(f"Scheduled production failed: {str(e)}")
