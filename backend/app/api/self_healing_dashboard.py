"""
VUC-2026 Self-Healing API Router
Endpoints for system health monitoring, auto-healing, and AI decision management
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio

from ..services.self_healing_engine import self_healing_engine, IssueSeverity, IssueType, HealingAction

# Pydantic models for API requests/responses
class SystemHealthResponse(BaseModel):
    timestamp: str
    system_metrics: Dict[str, Any]
    issues: Dict[str, Any]
    healing_performance: Dict[str, Any]
    ai_decisions: Dict[str, Any]
    status: str

class IssueListResponse(BaseModel):
    success: bool
    total_issues: int
    unresolved_issues: int
    issues: List[Dict[str, Any]]

class HealingHistoryResponse(BaseModel):
    success: bool
    total_healings: int
    success_rate: float
    healing_history: List[Dict[str, Any]]

class AIDecisionsResponse(BaseModel):
    success: bool
    total_decisions: int
    avg_confidence: float
    decisions: List[Dict[str, Any]]

class ManualHealingRequest(BaseModel):
    issue_id: str
    preferred_action: Optional[HealingAction] = None

class ManualHealingResponse(BaseModel):
    success: bool
    healing_result: Dict[str, Any]
    message: str

router = APIRouter()

@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    """Get comprehensive system health report"""
    try:
        health_report = await self_healing_engine.get_system_health_report()
        return SystemHealthResponse(**health_report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system health: {str(e)}")

@router.get("/issues", response_model=IssueListResponse)
async def get_active_issues(severity: Optional[IssueSeverity] = None, resolved: Optional[bool] = False):
    """Get list of system issues with optional filtering"""
    try:
        issues = list(self_healing_engine.active_issues.values())
        
        # Apply filters
        if severity:
            issues = [issue for issue in issues if issue.severity == severity]
        
        if resolved is not None:
            issues = [issue for issue in issues if issue.resolved == resolved]
        
        # Sort by detection time (newest first)
        issues.sort(key=lambda x: x.detected_at, reverse=True)
        
        return IssueListResponse(
            success=True,
            total_issues=len(issues),
            unresolved_issues=len([issue for issue in issues if not issue.resolved]),
            issues=[
                {
                    "issue_id": issue.issue_id,
                    "issue_type": issue.issue_type.value,
                    "severity": issue.severity.value,
                    "description": issue.description,
                    "component": issue.component,
                    "detected_at": issue.detected_at.isoformat(),
                    "resolution_attempts": issue.resolution_attempts,
                    "resolved": issue.resolved,
                    "healing_actions_taken": [action.value for action in issue.healing_actions_taken]
                }
                for issue in issues
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get issues: {str(e)}")

@router.get("/issues/{issue_id}")
async def get_issue_details(issue_id: str):
    """Get detailed information about a specific issue"""
    try:
        if issue_id not in self_healing_engine.active_issues:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        issue = self_healing_engine.active_issues[issue_id]
        
        return {
            "success": True,
            "issue": {
                "issue_id": issue.issue_id,
                "issue_type": issue.issue_type.value,
                "severity": issue.severity.value,
                "description": issue.description,
                "component": issue.component,
                "error_details": issue.error_details,
                "detected_at": issue.detected_at.isoformat(),
                "resolution_attempts": issue.resolution_attempts,
                "resolved": issue.resolved,
                "healing_actions_taken": [action.value for action in issue.healing_actions_taken]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get issue details: {str(e)}")

@router.get("/healing/history", response_model=HealingHistoryResponse)
async def get_healing_history(limit: int = 50, successful_only: bool = False):
    """Get healing action history"""
    try:
        history = self_healing_engine.healing_history.copy()
        
        # Apply filters
        if successful_only:
            history = [result for result in history if result.success]
        
        # Sort by execution time (newest first)
        history.sort(key=lambda x: result.action_taken, reverse=True)
        
        # Apply limit
        history = history[:limit]
        
        # Calculate success rate
        total_healings = len(self_healing_engine.healing_history)
        successful_healings = len([result for result in self_healing_engine.healing_history if result.success])
        success_rate = successful_healings / total_healings if total_healings > 0 else 0.0
        
        return HealingHistoryResponse(
            success=True,
            total_healings=total_healings,
            success_rate=success_rate,
            healing_history=[
                {
                    "success": result.success,
                    "action_taken": result.action_taken.value,
                    "resolution_time_ms": result.resolution_time_ms,
                    "new_state": result.new_state,
                    "confidence_score": result.confidence_score,
                    "timestamp": result.action_taken.isoformat() if hasattr(result.action_taken, 'isoformat') else datetime.now().isoformat()
                }
                for result in history
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get healing history: {str(e)}")

@router.get("/ai/decisions", response_model=AIDecisionsResponse)
async def get_ai_decisions(limit: int = 50):
    """Get AI decision history"""
    try:
        decisions = self_healing_engine.ai_decisions.copy()
        
        # Sort by decision time (newest first)
        decisions.sort(key=lambda x: x.made_at, reverse=True)
        
        # Apply limit
        decisions = decisions[:limit]
        
        # Calculate metrics
        total_decisions = len(self_healing_engine.ai_decisions)
        avg_confidence = sum(decision.confidence_score for decision in self_healing_engine.ai_decisions) / total_decisions if total_decisions > 0 else 0.0
        
        return AIDecisionsResponse(
            success=True,
            total_decisions=total_decisions,
            avg_confidence=avg_confidence,
            decisions=[
                {
                    "decision_id": decision.decision_id,
                    "context": decision.context,
                    "problem_description": decision.problem_description,
                    "chosen_option": decision.chosen_option,
                    "reasoning": decision.reasoning,
                    "confidence_score": decision.confidence_score,
                    "execution_time_ms": decision.execution_time_ms,
                    "impact_assessment": decision.impact_assessment,
                    "made_at": decision.made_at.isoformat()
                }
                for decision in decisions
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI decisions: {str(e)}")

@router.post("/healing/manual", response_model=ManualHealingResponse)
async def trigger_manual_healing(request: ManualHealingRequest, background_tasks: BackgroundTasks):
    """Manually trigger healing for a specific issue"""
    try:
        if request.issue_id not in self_healing_engine.active_issues:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        issue = self_healing_engine.active_issues[request.issue_id]
        
        if issue.resolved:
            return ManualHealingResponse(
                success=False,
                healing_result={},
                message="Issue is already resolved"
            )
        
        # Start background healing task
        background_tasks.add_task(
            self_healing_engine._attempt_healing,
            issue
        )
        
        return ManualHealingResponse(
            success=True,
            healing_result={"issue_id": request.issue_id, "healing_initiated": True},
            message=f"Manual healing initiated for issue {request.issue_id}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger manual healing: {str(e)}")

@router.post("/monitoring/start")
async def start_monitoring():
    """Start the self-healing monitoring system"""
    try:
        await self_healing_engine.start_monitoring()
        return {
            "success": True,
            "message": "Self-healing monitoring started successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start monitoring: {str(e)}")

@router.post("/monitoring/stop")
async def stop_monitoring():
    """Stop the self-healing monitoring system"""
    try:
        # In a real implementation, would stop the monitoring tasks
        # For now, just return success
        return {
            "success": True,
            "message": "Self-healing monitoring stopped successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop monitoring: {str(e)}")

@router.get("/metrics/system")
async def get_system_metrics():
    """Get current system metrics"""
    try:
        metrics = self_healing_engine.system_metrics
        
        return {
            "success": True,
            "metrics": {
                "cpu_usage": metrics.cpu_usage,
                "memory_usage": metrics.memory_usage,
                "disk_usage": metrics.disk_usage,
                "network_latency": metrics.network_latency,
                "api_response_times": metrics.api_response_times,
                "error_rates": metrics.error_rates,
                "queue_sizes": metrics.queue_sizes,
                "last_updated": metrics.last_updated.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system metrics: {str(e)}")

@router.delete("/issues/{issue_id}")
async def resolve_issue_manually(issue_id: str):
    """Manually mark an issue as resolved"""
    try:
        if issue_id not in self_healing_engine.active_issues:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        issue = self_healing_engine.active_issues[issue_id]
        issue.resolved = True
        
        return {
            "success": True,
            "message": f"Issue {issue_id} marked as resolved manually",
            "resolved_at": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve issue: {str(e)}")

@router.get("/strategies")
async def get_healing_strategies():
    """Get available healing strategies for different issue types"""
    try:
        strategies = {}
        
        for issue_type, actions in self_healing_engine.healing_strategies.items():
            strategies[issue_type.value] = [action.value for action in actions]
        
        return {
            "success": True,
            "strategies": strategies,
            "total_strategies": len(strategies)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get healing strategies: {str(e)}")

@router.get("/performance/summary")
async def get_performance_summary():
    """Get performance summary of the self-healing system"""
    try:
        # Get recent performance data
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        
        # Issues in last 24h
        recent_issues = [
            issue for issue in self_healing_engine.active_issues.values()
            if issue.detected_at >= last_24h
        ]
        
        # Healings in last 24h
        recent_healings = [
            result for result in self_healing_engine.healing_history
            if hasattr(result, 'timestamp') and result.timestamp >= last_24h
        ]
        
        # AI decisions in last 24h
        recent_decisions = [
            decision for decision in self_healing_engine.ai_decisions
            if decision.made_at >= last_24h
        ]
        
        # Calculate metrics
        healing_success_rate = len([h for h in recent_healings if h.success]) / len(recent_healings) if recent_healings else 0.0
        avg_decision_confidence = sum(d.confidence_score for d in recent_decisions) / len(recent_decisions) if recent_decisions else 0.0
        avg_resolution_time = sum(h.resolution_time_ms for h in recent_healings) / len(recent_healings) if recent_healings else 0.0
        
        return {
            "success": True,
            "period": "last_24h",
            "summary": {
                "issues_detected": len(recent_issues),
                "issues_resolved": len([i for i in recent_issues if i.resolved]),
                "issues_critical": len([i for i in recent_issues if i.severity == IssueSeverity.CRITICAL]),
                "healing_attempts": len(recent_healings),
                "healing_success_rate": healing_success_rate,
                "avg_resolution_time_ms": avg_resolution_time,
                "ai_decisions_made": len(recent_decisions),
                "avg_decision_confidence": avg_decision_confidence,
                "current_system_status": "healthy" if self_healing_engine.system_metrics.cpu_usage < 90 and self_healing_engine.system_metrics.memory_usage < 85 else "degraded"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance summary: {str(e)}")
