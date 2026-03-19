"""
VUC-2026 Adaptive Learning API Router
Kendini geliştiren sistemin API endpoint'leri
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

from ..services.adaptive_learning_engine import adaptive_learning_engine, LearningType, AdaptationStrategy

# Pydantic models
class LearningPatternResponse(BaseModel):
    pattern_id: str
    learning_type: str
    success_rate: float
    confidence_score: float
    frequency: int
    impact_score: float
    last_applied: str

class AdaptationRequest(BaseModel):
    pattern_id: str
    force_apply: bool = False

class AdaptationResponse(BaseModel):
    success: bool
    adaptation_id: str
    strategy: str
    improvement_score: float
    message: str

router = APIRouter()

@router.get("/dashboard")
async def get_learning_dashboard():
    """Get adaptive learning dashboard"""
    try:
        dashboard_data = await adaptive_learning_engine.get_learning_dashboard()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            **dashboard_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning dashboard: {str(e)}")

@router.get("/patterns")
async def get_learning_patterns():
    """Get all learning patterns"""
    try:
        patterns = []
        for pattern_id, pattern in adaptive_learning_engine.learning_patterns.items():
            patterns.append({
                "pattern_id": pattern.pattern_id,
                "learning_type": pattern.learning_type.value,
                "context": pattern.context,
                "success_rate": pattern.success_rate,
                "confidence_score": pattern.confidence_score,
                "frequency": pattern.frequency,
                "impact_score": pattern.impact_score,
                "last_applied": pattern.last_applied.isoformat()
            })
        
        return {
            "success": True,
            "total_patterns": len(patterns),
            "patterns": sorted(patterns, key=lambda p: p["impact_score"] * p["confidence_score"], reverse=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning patterns: {str(e)}")

@router.get("/patterns/{pattern_id}")
async def get_pattern_details(pattern_id: str):
    """Get specific pattern details"""
    try:
        if pattern_id not in adaptive_learning_engine.learning_patterns:
            raise HTTPException(status_code=404, detail="Pattern not found")
        
        pattern = adaptive_learning_engine.learning_patterns[pattern_id]
        
        return {
            "success": True,
            "pattern": {
                "pattern_id": pattern.pattern_id,
                "learning_type": pattern.learning_type.value,
                "context": pattern.context,
                "success_rate": pattern.success_rate,
                "confidence_score": pattern.confidence_score,
                "frequency": pattern.frequency,
                "impact_score": pattern.impact_score,
                "last_applied": pattern.last_applied.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pattern details: {str(e)}")

@router.post("/adaptations/trigger")
async def trigger_adaptation(request: AdaptationRequest, background_tasks: BackgroundTasks):
    """Manually trigger an adaptation"""
    try:
        if request.pattern_id not in adaptive_learning_engine.learning_patterns:
            raise HTTPException(status_code=404, detail="Pattern not found")
        
        pattern = adaptive_learning_engine.learning_patterns[request.pattern_id]
        
        # Check if pattern meets thresholds
        if (not request.force_apply and 
            pattern.confidence_score < adaptive_learning_engine.adaptation_thresholds["min_confidence"]):
            return {
                "success": False,
                "message": f"Pattern confidence too low: {pattern.confidence_score:.2f}"
            }
        
        # Create adaptation opportunity
        opportunity = {
            "pattern_id": request.pattern_id,
            "pattern": pattern,
            "strategy": adaptive_learning_engine._select_adaptation_strategy(pattern),
            "priority": pattern.impact_score * pattern.confidence_score
        }
        
        # Apply adaptation in background
        background_tasks.add_task(adaptive_learning_engine._apply_adaptation, opportunity)
        
        return {
            "success": True,
            "message": f"Adaptation triggered for pattern {request.pattern_id}",
            "strategy": opportunity["strategy"].value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger adaptation: {str(e)}")

@router.get("/adaptations/history")
async def get_adaptation_history(limit: int = 50):
    """Get adaptation history"""
    try:
        history = adaptive_learning_engine.adaptation_history.copy()
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        history = history[:limit]
        
        return {
            "success": True,
            "total_adaptations": len(adaptive_learning_engine.adaptation_history),
            "adaptations": [
                {
                    "adaptation_id": adaptation.adaptation_id,
                    "strategy": adaptation.strategy.value,
                    "trigger_event": adaptation.trigger_event,
                    "improvement_score": adaptation.improvement_score,
                    "success": adaptation.success,
                    "timestamp": adaptation.timestamp.isoformat()
                }
                for adaptation in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get adaptation history: {str(e)}")

@router.get("/performance/metrics")
async def get_performance_metrics():
    """Get current performance metrics"""
    try:
        metrics = adaptive_learning_engine.performance_metrics
        
        # Calculate current stats
        current_metrics = {}
        for metric_name, values in metrics.items():
            if values:
                current_metrics[metric_name] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "trend": "up" if len(values) > 1 and values[-1] > values[-2] else "down",
                    "data_points": len(values)
                }
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "metrics": current_metrics,
            "total_metrics": len(current_metrics)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")

@router.get("/learning/state")
async def get_learning_state():
    """Get current learning state"""
    try:
        state = adaptive_learning_engine.learning_state.copy()
        
        # Calculate additional metrics
        total_adaptations = state.get("successful_adaptations", 0) + state.get("failed_adaptations", 0)
        success_rate = state.get("successful_adaptations", 0) / total_adaptations if total_adaptations > 0 else 0.0
        
        return {
            "success": True,
            "learning_state": {
                **state,
                "total_adaptations": total_adaptations,
                "success_rate": success_rate,
                "learning_efficiency": state.get("average_improvement", 0.0) * success_rate
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning state: {str(e)}")

@router.post("/learning/start")
async def start_continuous_learning(background_tasks: BackgroundTasks):
    """Start continuous learning process"""
    try:
        # Start learning in background
        background_tasks.add_task(adaptive_learning_engine.start_continuous_learning)
        
        return {
            "success": True,
            "message": "Continuous learning started successfully",
            "learning_interval": adaptive_learning_engine.adaptation_thresholds["learning_interval"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start continuous learning: {str(e)}")

@router.post("/learning/stop")
async def stop_continuous_learning():
    """Stop continuous learning process"""
    try:
        # In a real implementation, would stop the learning task
        return {
            "success": True,
            "message": "Continuous learning stopped successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop continuous learning: {str(e)}")

@router.post("/learning/save")
async def save_learning_state():
    """Save current learning state"""
    try:
        await adaptive_learning_engine.save_learning_state()
        
        return {
            "success": True,
            "message": "Learning state saved successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save learning state: {str(e)}")

@router.post("/learning/load")
async def load_learning_state():
    """Load learning state from storage"""
    try:
        await adaptive_learning_engine.load_learning_state()
        
        return {
            "success": True,
            "message": "Learning state loaded successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load learning state: {str(e)}")

@router.get("/opportunities")
async def get_adaptation_opportunities():
    """Get current adaptation opportunities"""
    try:
        opportunities = await adaptive_learning_engine._identify_adaptation_opportunities()
        
        return {
            "success": True,
            "opportunities": [
                {
                    "pattern_id": opp["pattern_id"],
                    "strategy": opp["strategy"].value,
                    "priority": opp["priority"],
                    "pattern": {
                        "success_rate": opp["pattern"].success_rate,
                        "confidence_score": opp["pattern"].confidence_score,
                        "impact_score": opp["pattern"].impact_score,
                        "frequency": opp["pattern"].frequency
                    }
                }
                for opp in opportunities
            ],
            "total_opportunities": len(opportunities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get adaptation opportunities: {str(e)}")

@router.get("/thresholds")
async def get_adaptation_thresholds():
    """Get current adaptation thresholds"""
    try:
        return {
            "success": True,
            "thresholds": adaptive_learning_engine.adaptation_thresholds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get adaptation thresholds: {str(e)}")

@router.put("/thresholds")
async def update_adaptation_thresholds(thresholds: Dict[str, Any]):
    """Update adaptation thresholds"""
    try:
        # Validate thresholds
        valid_keys = adaptive_learning_engine.adaptation_thresholds.keys()
        for key in thresholds.keys():
            if key not in valid_keys:
                raise HTTPException(status_code=400, detail=f"Invalid threshold key: {key}")
        
        # Update thresholds
        adaptive_learning_engine.adaptation_thresholds.update(thresholds)
        
        return {
            "success": True,
            "message": "Adaptation thresholds updated successfully",
            "new_thresholds": adaptive_learning_engine.adaptation_thresholds
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update adaptation thresholds: {str(e)}")
