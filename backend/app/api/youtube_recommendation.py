"""
VUC-2026 YouTube Recommendation API
Önerilenler Algoritması ve Conversion Optimizasyon API Endpoint'leri
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from backend.app.services.youtube_recommendation_engine import youtube_recommendation_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/youtube-recommendation", tags=["youtube-recommendation"])

class RecommendationStrategyRequest(BaseModel):
    video_metadata: Dict[str, Any] = Field(..., description="Video meta verileri")
    target_audience: Dict[str, Any] = Field(..., description="Hedef kitle verileri")

class ConversionFunnelRequest(BaseModel):
    video_data: Dict[str, Any] = Field(..., description="Video verileri")
    conversion_goals: List[str] = Field(..., description="Conversion hedefleri")

class AdTeaserRequest(BaseModel):
    product_info: Dict[str, Any] = Field(..., description="Ürün bilgisi")
    placement_timing: str = Field(..., description="Yerleşim zamanlaması")

class PerformanceAnalysisRequest(BaseModel):
    video_id: str = Field(..., description="Video ID")
    performance_data: Dict[str, Any] = Field(..., description="Performans verileri")

@router.post("/strategy/generate", response_model=Dict[str, Any])
async def generate_recommendation_strategy(request: RecommendationStrategyRequest):
    """
    YouTube önerilenler stratejisi oluştur
    
    - **video_metadata**: Video meta verileri (başlık, süre, kategori vb.)
    - **target_audience**: Hedef kitle demografik ve psikografik verileri
    """
    try:
        strategy = youtube_recommendation_engine.generate_recommendation_strategy(
            video_metadata=request.video_metadata,
            target_audience=request.target_audience
        )
        
        if "error" in strategy:
            raise HTTPException(status_code=500, detail=strategy["error"])
        
        return {
            "success": True,
            "strategy": strategy,
            "message": "Recommendation strategy generated successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendation strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversion/optimize", response_model=Dict[str, Any])
async def optimize_conversion_funnels(request: ConversionFunnelRequest):
    """
    Conversion hunileri için optimizasyon
    
    - **video_data**: Video verileri
    - **conversion_goals**: Conversion hedefleri (subscribe, like, comment, share, purchase)
    """
    try:
        optimization = youtube_recommendation_engine.optimize_for_conversion_funnels(
            video_data=request.video_data,
            conversion_goals=request.conversion_goals
        )
        
        if "error" in optimization:
            raise HTTPException(status_code=500, detail=optimization["error"])
        
        return {
            "success": True,
            "optimization": optimization,
            "message": "Conversion funnel optimization completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing conversion funnels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ad-teaser/generate", response_model=Dict[str, Any])
async def generate_ad_teaser_content(request: AdTeaserRequest):
    """
    Reklam teaser içeriği oluştur
    
    - **product_info**: Ürün bilgisi (isim, fiyat, şirket, kategori)
    - **placement_timing**: Yerleşim zamanlaması (early_section, middle_section, climax_section)
    """
    try:
        teaser = youtube_recommendation_engine.generate_ad_teaser_content(
            product_info=request.product_info,
            placement_timing=request.placement_timing
        )
        
        if "error" in teaser:
            raise HTTPException(status_code=500, detail=teaser["error"])
        
        return {
            "success": True,
            "teaser": teaser,
            "message": "Ad teaser content generated",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating ad teaser content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/triggers/available", response_model=Dict[str, Any])
async def get_available_triggers():
    """
    Mevcut psikolojik trigger'ları getir
    """
    try:
        triggers = youtube_recommendation_engine.psychological_triggers
        
        trigger_list = []
        for key, trigger in triggers.items():
            trigger_list.append({
                "name": trigger.name,
                "trigger_type": trigger.trigger_type,
                "effectiveness_score": trigger.effectiveness_score,
                "placement_timing": trigger.placement_timing,
                "emotional_weight": trigger.emotional_weight,
                "conversion_potential": trigger.conversion_potential
            })
        
        return {
            "success": True,
            "triggers": trigger_list,
            "total_triggers": len(trigger_list),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting available triggers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hooks/templates", response_model=Dict[str, Any])
async def get_hook_templates():
    """
    Hook şablonlarını getir
    """
    try:
        templates = youtube_recommendation_engine.hook_templates
        
        return {
            "success": True,
            "templates": templates,
            "total_categories": len(templates),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting hook templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/curiosity-gaps/patterns", response_model=Dict[str, Any])
async def get_curiosity_gap_patterns():
    """
    Merak aralığı pattern'lerini getir
    """
    try:
        patterns = youtube_recommendation_engine.curiosity_gaps
        
        return {
            "success": True,
            "patterns": patterns,
            "total_patterns": len(patterns),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting curiosity gap patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ad-teaser/patterns", response_model=Dict[str, Any])
async def get_ad_teaser_patterns():
    """
    Reklam teaser pattern'lerini getir
    """
    try:
        patterns = youtube_recommendation_engine.ad_teaser_patterns
        
        return {
            "success": True,
            "patterns": patterns,
            "total_patterns": len(patterns),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting ad teaser patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/analyze", response_model=Dict[str, Any])
async def analyze_content_for_recommendations(video_metadata: Dict[str, Any]):
    """
    Video içeriğini önerilenler için analiz et
    
    - **video_metadata**: Video meta verileri
    """
    try:
        content_analysis = youtube_recommendation_engine._analyze_content_for_recommendations(video_metadata)
        
        return {
            "success": True,
            "analysis": content_analysis,
            "message": "Content analysis completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audience/analyze", response_model=Dict[str, Any])
async def analyze_audience_for_conversion(target_audience: Dict[str, Any]):
    """
    Hedef kitleyi conversion için analiz et
    
    - **target_audience**: Hedef kitle verileri
    """
    try:
        audience_analysis = youtube_recommendation_engine._analyze_audience_for_conversion(target_audience)
        
        return {
            "success": True,
            "analysis": audience_analysis,
            "message": "Audience analysis completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing audience: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/engagement/timeline", response_model=Dict[str, Any])
async def create_engagement_timeline(video_metadata: Dict[str, Any]):
    """
    Etkileşim zaman çizelgesi oluştur
    
    - **video_metadata**: Video meta verileri
    """
    try:
        timeline = youtube_recommendation_engine._create_engagement_timeline(video_metadata)
        
        return {
            "success": True,
            "timeline": timeline,
            "message": "Engagement timeline created",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating engagement timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/predict", response_model=Dict[str, Any])
async def predict_video_performance(video_metadata: Dict[str, Any], target_audience: Dict[str, Any]):
    """
    Video performansını tahmin et
    
    - **video_metadata**: Video meta verileri
    - **target_audience**: Hedef kitle verileri
    """
    try:
        content_analysis = youtube_recommendation_engine._analyze_content_for_recommendations(video_metadata)
        audience_analysis = youtube_recommendation_engine._analyze_audience_for_conversion(target_audience)
        
        performance = youtube_recommendation_engine._predict_performance(content_analysis, audience_analysis)
        
        return {
            "success": True,
            "performance": performance,
            "message": "Performance prediction completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error predicting performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversion/factors", response_model=Dict[str, Any])
async def get_conversion_factors():
    """
    Conversion faktörlerini getir
    """
    try:
        factors = {
            "psychological_triggers": list(youtube_recommendation_engine.psychological_triggers.keys()),
            "conversion_patterns": list(youtube_recommendation_engine.conversion_patterns.keys()),
            "hook_categories": list(youtube_recommendation_engine.hook_templates.keys()),
            "teaser_patterns": len(youtube_recommendation_engine.ad_teaser_patterns),
            "engagement_algorithms": list(youtube_recommendation_engine.engagement_algorithms.keys())
        }
        
        return {
            "success": True,
            "factors": factors,
            "message": "Conversion factors retrieved",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting conversion factors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/algorithm/signals", response_model=Dict[str, Any])
async def generate_algorithm_signals(video_metadata: Dict[str, Any], target_audience: Dict[str, Any]):
    """
    Algoritma sinyalleri oluştur
    
    - **video_metadata**: Video meta verileri
    - **target_audience**: Hedef kitle verileri
    """
    try:
        content_analysis = youtube_recommendation_engine._analyze_content_for_recommendations(video_metadata)
        audience_analysis = youtube_recommendation_engine._analyze_audience_for_conversion(target_audience)
        
        signals = youtube_recommendation_engine._generate_algorithm_signals(content_analysis, audience_analysis)
        
        return {
            "success": True,
            "signals": signals,
            "message": "Algorithm signals generated",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating algorithm signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/optimize", response_model=Dict[str, Any])
async def optimize_content_for_recommendations(video_metadata: Dict[str, Any]):
    """
    İçeriği önerilenler için optimize et
    
    - **video_metadata**: Video meta verileri
    """
    try:
        content_analysis = youtube_recommendation_engine._analyze_content_for_recommendations(video_metadata)
        optimization = youtube_recommendation_engine._optimize_content_for_recommendations(content_analysis)
        
        return {
            "success": True,
            "optimization": optimization,
            "message": "Content optimization completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error optimizing content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendation/factors", response_model=Dict[str, Any])
async def get_recommendation_factors():
    """
    Önerilenler algoritması faktörlerini getir
    """
    try:
        factors = youtube_recommendation_engine.recommendation_factors
        
        return {
            "success": True,
            "factors": factors,
            "total_factors": len(factors),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendation factors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch/analyze", response_model=Dict[str, Any])
async def batch_analyze_videos(videos: List[Dict[str, Any]]):
    """
    Çoklu video analizi
    
    - **videos**: Video listesi
    """
    try:
        results = []
        
        for video in videos:
            try:
                content_analysis = youtube_recommendation_engine._analyze_content_for_recommendations(video)
                performance = youtube_recommendation_engine._predict_performance(content_analysis, {})
                
                results.append({
                    "video_id": video.get("id", "unknown"),
                    "analysis": content_analysis,
                    "performance": performance,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "video_id": video.get("id", "unknown"),
                    "error": str(e),
                    "success": False
                })
        
        successful_analyses = [r for r in results if r["success"]]
        
        return {
            "success": True,
            "results": results,
            "summary": {
                "total_videos": len(videos),
                "successful_analyses": len(successful_analyses),
                "failed_analyses": len(videos) - len(successful_analyses),
                "success_rate": (len(successful_analyses) / len(videos) * 100) if videos else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/overview", response_model=Dict[str, Any])
async def get_analytics_overview():
    """
    Analitik genel bakış
    """
    try:
        overview = {
            "total_triggers": len(youtube_recommendation_engine.psychological_triggers),
            "hook_categories": len(youtube_recommendation_engine.hook_templates),
            "curiosity_patterns": len(youtube_recommendation_engine.curiosity_gaps),
            "ad_teaser_patterns": len(youtube_recommendation_engine.ad_teaser_patterns),
            "recommendation_factors": len(youtube_recommendation_engine.recommendation_factors),
            "conversion_patterns": len(youtube_recommendation_engine.conversion_patterns),
            "engagement_algorithms": len(youtube_recommendation_engine.engagement_algorithms),
            "performance_history": len(youtube_recommendation_engine.performance_history)
        }
        
        return {
            "success": True,
            "overview": overview,
            "message": "Analytics overview retrieved",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))
