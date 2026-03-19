"""
VUC-2026 YouTube Ad-Slot Optimization API
Dynamic mid-roll placement and revenue optimization endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.ad_slot_optimization_service import AdSlotOptimizationService
from app.core.ai_intelligence import AIIntelligence

router = APIRouter(prefix="/api/yt/ad-slots", tags=["ad-slots"])
ad_service = AdSlotOptimizationService()
ai_intelligence = AIIntelligence()

class AdSlotRequest(BaseModel):
    script: str
    duration: int
    target_views: int = 10000
    is_kids_content: bool = False
    target_cpm: float = 2.5

class AdSlotResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str
    timestamp: datetime

class COPPARequest(BaseModel):
    video_metadata: Dict
    made_for_kids: bool = False

@router.post("/optimize", response_model=AdSlotResponse)
async def optimize_ad_slots(request: AdSlotRequest):
    """
    Optimize ad slot placement for maximum revenue
    """
    try:
        # Generate complete optimization
        optimization = await ad_service.optimize_for_maximum_revenue(
            script=request.script,
            duration=request.duration,
            target_views=request.target_views,
            is_kids_content=request.is_kids_content
        )
        
        # Log optimization for analytics
        await ai_intelligence.log_ad_optimization(
            script_length=len(request.script),
            duration=request.duration,
            target_views=request.target_views,
            is_kids_content=request.is_kids_content,
            result=optimization
        )
        
        return AdSlotResponse(
            success=True,
            data=optimization,
            message="Ad slot optimization completed successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ad slot optimization failed: {str(e)}"
        )

@router.post("/coppa-check", response_model=AdSlotResponse)
async def coppa_compliance_check(request: COPPARequest):
    """
    COPPA compliance checker and metadata adjustment
    """
    try:
        # Apply COPPA compliance
        compliant_metadata = await ad_service.coppa_compliance_check(
            video_metadata=request.video_metadata,
            made_for_kids=request.made_for_kids
        )
        
        return AdSlotResponse(
            success=True,
            data={"compliant_metadata": compliant_metadata},
            message="COPPA compliance check completed",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"COPPA compliance check failed: {str(e)}"
        )

@router.post("/analyze-engagement", response_model=AdSlotResponse)
async def analyze_script_engagement(
    script: str,
    duration: int
):
    """
    Analyze script engagement patterns
    """
    try:
        engagement = await ad_service.analyze_script_engagement(script, duration)
        
        return AdSlotResponse(
            success=True,
            data={"engagement_analysis": engagement.dict()},
            message="Script engagement analysis completed",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Engagement analysis failed: {str(e)}"
        )

@router.post("/revenue-projection", response_model=AdSlotResponse)
async def generate_revenue_projection(
    ad_slots: List[Dict],
    expected_views: int,
    duration: int
):
    """
    Generate revenue projection for ad slots
    """
    try:
        # Convert dict to AdSlot objects
        from app.services.ad_slot_optimization_service import AdSlot
        slot_objects = []
        
        for slot_data in ad_slots:
            slot = AdSlot(
                position_seconds=slot_data["position_seconds"],
                ad_type=slot_data["ad_type"],
                engagement_score=slot_data["engagement_score"],
                predicted_cpm=slot_data["predicted_cpm"],
                retention_impact=slot_data["retention_impact"]
            )
            slot_objects.append(slot)
        
        projection = await ad_service.generate_ad_revenue_projection(
            ad_slots=slot_objects,
            expected_views=expected_views,
            duration=duration
        )
        
        return AdSlotResponse(
            success=True,
            data={"revenue_projection": projection},
            message="Revenue projection generated successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Revenue projection failed: {str(e)}"
        )

@router.get("/analytics", response_model=AdSlotResponse)
async def get_ad_analytics():
    """
    Get ad slot performance analytics
    """
    try:
        analytics = await ai_intelligence.get_ad_performance_analytics()
        
        return AdSlotResponse(
            success=True,
            data=analytics,
            message="Ad analytics retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analytics retrieval failed: {str(e)}"
        )

@router.post("/batch-optimize", response_model=AdSlotResponse)
async def batch_optimize_videos(
    background_tasks: BackgroundTasks,
    video_requests: List[AdSlotRequest]
):
    """
    Batch optimize multiple videos
    """
    try:
        results = []
        
        for request in video_requests:
            try:
                optimization = await ad_service.optimize_for_maximum_revenue(
                    script=request.script,
                    duration=request.duration,
                    target_views=request.target_views,
                    is_kids_content=request.is_kids_content
                )
                results.append({
                    "success": True,
                    "optimization": optimization
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e)
                })
        
        successful_count = sum(1 for r in results if r["success"])
        
        return AdSlotResponse(
            success=True,
            data={
                "total_processed": len(video_requests),
                "successful": successful_count,
                "failed": len(video_requests) - successful_count,
                "results": results
            },
            message=f"Batch optimization completed: {successful_count}/{len(video_requests)} successful",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch optimization failed: {str(e)}"
        )

@router.get("/settings", response_model=AdSlotResponse)
async def get_ad_optimization_settings():
    """
    Get current ad optimization settings
    """
    try:
        settings = {
            "min_interval_between_ads": ad_service.min_interval_between_ads,
            "max_mid_rolls_per_10min": ad_service.max_mid_rolls_per_10min,
            "retention_threshold": ad_service.retention_threshold,
            "coppa_cpm_adjustment": ad_service.coppa_cpm_adjustment,
            "high_tension_keywords": ad_service.high_tension_keywords,
            "drop_off_indicators": ad_service.drop_off_indicators
        }
        
        return AdSlotResponse(
            success=True,
            data=settings,
            message="Ad optimization settings retrieved",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Settings retrieval failed: {str(e)}"
        )

@router.put("/settings", response_model=AdSlotResponse)
async def update_ad_optimization_settings(settings: Dict):
    """
    Update ad optimization settings
    """
    try:
        # Update service settings
        if "min_interval_between_ads" in settings:
            ad_service.min_interval_between_ads = settings["min_interval_between_ads"]
        if "max_mid_rolls_per_10min" in settings:
            ad_service.max_mid_rolls_per_10min = settings["max_mid_rolls_per_10min"]
        if "retention_threshold" in settings:
            ad_service.retention_threshold = settings["retention_threshold"]
        if "coppa_cpm_adjustment" in settings:
            ad_service.coppa_cpm_adjustment = settings["coppa_cpm_adjustment"]
        
        return AdSlotResponse(
            success=True,
            data=settings,
            message="Ad optimization settings updated",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Settings update failed: {str(e)}"
        )
