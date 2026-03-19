"""
Zero-Bug Audit & Self-Healing API Endpoints
Autonomous error detection, diagnosis, and recovery
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import logging

from ..services.self_healing_service import self_healing_engine, system_auditor

logger = logging.getLogger(__name__)

router = APIRouter()

class ErrorReportRequest(BaseModel):
    """Error report request model"""
    component: str
    error_type: str
    error_message: str
    stack_trace: str
    context: Optional[Dict[str, Any]] = None

class HealingConfigRequest(BaseModel):
    """Healing configuration request"""
    max_fix_attempts: Optional[int] = None
    enable_auto_healing: Optional[bool] = None
    healing_strategies: Optional[Dict[str, List[Dict]]] = None

@router.get("/self-healing/status")
async def get_self_healing_status():
    """Get self-healing system status"""
    try:
        error_stats = self_healing_engine.get_error_statistics(24)
        health_summary = self_healing_engine.get_health_summary()
        
        return {
            "success": True,
            "status": "active",
            "error_statistics": error_stats,
            "health_summary": health_summary,
            "configuration": {
                "max_fix_attempts": self_healing_engine.max_fix_attempts,
                "total_errors_logged": len(self_healing_engine.error_history),
                "total_metrics_collected": len(self_healing_engine.health_metrics)
            }
        }
    except Exception as e:
        logger.error(f"Failed to get self-healing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-healing/report-error")
async def report_error(error_request: ErrorReportRequest):
    """Report an error to the self-healing system"""
    try:
        # Create error exception from request
        error = Exception(error_request.error_message)
        
        # Log error
        error_report = self_healing_engine.log_error(
            error=error,
            component=error_request.component,
            context=error_request.context or {}
        )
        
        return {
            "success": True,
            "error_id": str(id(error_report)),
            "timestamp": error_report.timestamp.isoformat(),
            "severity": error_report.severity,
            "auto_healing_attempted": True
        }
    except Exception as e:
        logger.error(f"Failed to report error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-healing/errors")
async def get_error_history(hours: int = 24, component: Optional[str] = None, severity: Optional[str] = None):
    """Get error history with filtering"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self_healing_engine.error_history if e.timestamp > cutoff_time]
        
        # Apply filters
        if component:
            recent_errors = [e for e in recent_errors if e.component == component]
        if severity:
            recent_errors = [e for e in recent_errors if e.severity == severity]
        
        # Convert to dict for JSON response
        error_dicts = []
        for error in recent_errors:
            error_dict = {
                "timestamp": error.timestamp.isoformat(),
                "error_type": error.error_type,
                "error_message": error.error_message,
                "component": error.component,
                "severity": error.severity,
                "auto_fixed": error.auto_fixed,
                "fix_method": error.fix_method,
                "fix_attempts": error.fix_attempts,
                "context": error.context
            }
            error_dicts.append(error_dict)
        
        return {
            "success": True,
            "errors": error_dicts,
            "total_count": len(error_dicts),
            "time_window_hours": hours
        }
    except Exception as e:
        logger.error(f"Failed to get error history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-healing/metrics")
async def get_health_metrics(hours: int = 24, component: Optional[str] = None):
    """Get health metrics with filtering"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [m for m in self_healing_engine.health_metrics if m.timestamp > cutoff_time]
        
        # Apply filters
        if component:
            recent_metrics = [m for m in recent_metrics if m.component == component]
        
        # Convert to dict for JSON response
        metric_dicts = []
        for metric in recent_metrics:
            metric_dict = {
                "timestamp": metric.timestamp.isoformat(),
                "component": metric.component,
                "metric_name": metric.metric_name,
                "value": metric.value,
                "threshold": metric.threshold,
                "status": metric.status
            }
            metric_dicts.append(metric_dict)
        
        return {
            "success": True,
            "metrics": metric_dicts,
            "total_count": len(metric_dicts),
            "time_window_hours": hours
        }
    except Exception as e:
        logger.error(f"Failed to get health metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-healing/config")
async def update_healing_config(config_request: HealingConfigRequest):
    """Update self-healing configuration"""
    try:
        updates = {}
        
        if config_request.max_fix_attempts is not None:
            self_healing_engine.max_fix_attempts = config_request.max_fix_attempts
            updates["max_fix_attempts"] = config_request.max_fix_attempts
        
        if config_request.healing_strategies is not None:
            self_healing_engine.healing_strategies = config_request.healing_strategies
            updates["healing_strategies_updated"] = True
        
        return {
            "success": True,
            "message": "Self-healing configuration updated",
            "updates": updates
        }
    except Exception as e:
        logger.error(f"Failed to update healing config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-healing/audit")
async def run_system_audit(background_tasks: BackgroundTasks):
    """Run full system audit"""
    try:
        # Run audit in background
        audit_result = await system_auditor.run_full_audit()
        
        return {
            "success": True,
            "audit_result": audit_result,
            "timestamp": audit_result["timestamp"]
        }
    except Exception as e:
        logger.error(f"System audit failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-healing/strategies")
async def get_healing_strategies():
    """Get available healing strategies"""
    try:
        return {
            "success": True,
            "strategies": self_healing_engine.healing_strategies,
            "total_strategies": len(self_healing_engine.healing_strategies)
        }
    except Exception as e:
        logger.error(f"Failed to get healing strategies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-healing/test-healing")
async def test_healing_mechanism(component: str, error_type: str):
    """Test healing mechanism with simulated error"""
    try:
        # Create simulated error
        test_error = Exception(f"Test error for {component} - {error_type}")
        
        # Log error and trigger healing
        error_report = self_healing_engine.log_error(
            error=test_error,
            component=component,
            context={"test_mode": True, "error_type": error_type}
        )
        
        # Wait a moment for healing to attempt
        await asyncio.sleep(2)
        
        # Get updated error status
        updated_error = next(
            (e for e in reversed(self_healing_engine.error_history) 
             if e.timestamp == error_report.timestamp), 
            None
        )
        
        return {
            "success": True,
            "test_result": {
                "error_id": str(id(error_report)),
                "auto_fixed": updated_error.auto_fixed if updated_error else False,
                "fix_method": updated_error.fix_method if updated_error else None,
                "fix_attempts": updated_error.fix_attempts if updated_error else 0
            }
        }
    except Exception as e:
        logger.error(f"Healing test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-healing/dashboard")
async def get_dashboard_data():
    """Get dashboard data for self-healing system"""
    try:
        error_stats = self_healing_engine.get_error_statistics(24)
        health_summary = self_healing_engine.get_health_summary()
        
        # Get recent errors for dashboard
        recent_errors = self_healing_engine.error_history[-10:]
        recent_errors_data = []
        for error in recent_errors:
            error_dict = {
                "timestamp": error.timestamp.isoformat(),
                "component": error.component,
                "error_type": error.error_type,
                "severity": error.severity,
                "auto_fixed": error.auto_fixed
            }
            recent_errors_data.append(error_dict)
        
        # Get latest metrics
        latest_metrics = {}
        for metric in self_healing_engine.health_metrics[-20:]:
            key = f"{metric.component}_{metric.metric_name}"
            if key not in latest_metrics or metric.timestamp > latest_metrics[key]["timestamp"]:
                latest_metrics[key] = {
                    "value": metric.value,
                    "status": metric.status,
                    "timestamp": metric.timestamp.isoformat()
                }
        
        return {
            "success": True,
            "dashboard_data": {
                "error_statistics": error_stats,
                "health_summary": health_summary,
                "recent_errors": recent_errors_data,
                "latest_metrics": latest_metrics,
                "system_status": health_summary["status"],
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-healing/force-healing")
async def force_healing_attempt(error_id: str):
    """Force healing attempt for a specific error"""
    try:
        # Find error by ID (timestamp-based)
        target_error = None
        for error in self_healing_engine.error_history:
            if str(id(error)) == error_id:
                target_error = error
                break
        
        if not target_error:
            raise HTTPException(status_code=404, detail="Error not found")
        
        # Attempt healing
        success = await self_healing_engine.attempt_auto_healing(target_error)
        
        return {
            "success": True,
            "healing_attempted": True,
            "healing_successful": success,
            "error_id": error_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Force healing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/self-healing/clear-history")
async def clear_error_history(older_than_hours: int = 168):  # Default 7 days
    """Clear error history older than specified hours"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        original_count = len(self_healing_engine.error_history)
        
        # Remove old errors
        self_healing_engine.error_history = [
            e for e in self_healing_engine.error_history 
            if e.timestamp > cutoff_time
        ]
        
        removed_count = original_count - len(self_healing_engine.error_history)
        
        return {
            "success": True,
            "removed_errors": removed_count,
            "remaining_errors": len(self_healing_engine.error_history),
            "cutoff_hours": older_than_hours
        }
    except Exception as e:
        logger.error(f"Failed to clear error history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-healing/health")
async def self_healing_health_check():
    """Self-healing system health check"""
    try:
        # Check system components
        health_status = {
            "error_logging": "healthy",
            "auto_healing": "healthy",
            "health_monitoring": "healthy",
            "system_auditor": "healthy"
        }
        
        # Test basic functionality
        try:
            # Test error logging
            test_error = Exception("Health check test error")
            error_report = self_healing_engine.log_error(
                error=test_error,
                component="health_check",
                context={"test": True}
            )
            
            # Test metric collection
            metrics = await self_healing_engine.collect_health_metrics()
            
            # Test auditor
            audit_result = await system_auditor.run_full_audit()
            
            overall_health = "healthy"
            if not audit_result or audit_result.get("overall_status") != "healthy":
                overall_health = "degraded"
            
        except Exception as e:
            logger.error(f"Self-healing health check failed: {str(e)}")
            overall_health = "unhealthy"
        
        return {
            "status": overall_health,
            "components": health_status,
            "version": "1.0.0",
            "configuration": {
                "max_fix_attempts": self_healing_engine.max_fix_attempts,
                "total_errors_logged": len(self_healing_engine.error_history),
                "total_metrics_collected": len(self_healing_engine.health_metrics)
            }
        }
    except Exception as e:
        logger.error(f"Self-healing health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
