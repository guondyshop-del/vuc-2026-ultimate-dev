"""
VUC-2026 AI Assistant API Router
Problem çözüm ve otomatik müdahale endpoint'leri
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio
import logging

from ..services.ai_problem_solver import ai_problem_solver, ProblemCategory, ProblemSeverity, SolutionType

router = APIRouter()
logger = logging.getLogger("vuc_ai_assistant_api")

class ProblemDetectionRequest(BaseModel):
    """Problem tespit isteği"""
    category: ProblemCategory
    severity: ProblemSeverity
    title: str
    description: str
    component: str
    symptoms: List[str]
    metrics: Dict[str, Any] = {}

class ManualSolutionRequest(BaseModel):
    """Manuel çözüm isteği"""
    problem_id: str
    solution_type: SolutionType
    custom_steps: List[str] = []

class SystemAnalysisRequest(BaseModel):
    """Sistem analizi isteği"""
    analysis_depth: str = Field(default="standard", description="basic, standard, deep")
    components: List[str] = Field(default=[], description="Analiz edilecek komponentler")

@router.get("/dashboard")
async def get_ai_assistant_dashboard():
    """AI asistan problem çözüm dashboard'ı"""
    try:
        dashboard_data = await ai_problem_solver.get_problem_solving_dashboard()
        return {
            "success": True,
            "data": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard alınamadı: {str(e)}")

@router.get("/problems")
async def get_active_problems():
    """Aktif problemleri listele"""
    try:
        problems = []
        for problem_id, problem in ai_problem_solver.detected_problems.items():
            problems.append({
                "id": problem.problem_id,
                "title": problem.title,
                "category": problem.category.value,
                "severity": problem.severity.value,
                "description": problem.description,
                "component": problem.component,
                "symptoms": problem.symptoms,
                "detected_at": problem.detected_at.isoformat(),
                "metrics": problem.metrics,
                "impact_assessment": problem.impact_assessment
            })
        
        return {
            "success": True,
            "count": len(problems),
            "problems": problems,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Get problems error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Problemler alınamadı: {str(e)}")

@router.get("/problems/{problem_id}")
async def get_problem_detail(problem_id: str):
    """Problem detayını al"""
    try:
        problem = ai_problem_solver.detected_problems.get(problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem bulunamadı")
        
        # Get solution history for this problem
        solution_history = [
            result for result in ai_problem_solver.solution_history
            if result.problem_id == problem_id
        ]
        
        return {
            "success": True,
            "problem": {
                "id": problem.problem_id,
                "title": problem.title,
                "category": problem.category.value,
                "severity": problem.severity.value,
                "description": problem.description,
                "component": problem.component,
                "symptoms": problem.symptoms,
                "detected_at": problem.detected_at.isoformat(),
                "metrics": problem.metrics,
                "impact_assessment": problem.impact_assessment
            },
            "solution_history": [
                {
                    "solution_applied": result.solution_applied.dict() if result.solution_applied else None,
                    "success": result.success,
                    "execution_time_seconds": result.execution_time_seconds,
                    "error_message": result.error_message,
                    "system_state_after": result.system_state_after,
                    "lessons_learned": result.lessons_learned
                }
                for result in solution_history
            ],
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get problem detail error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Problem detayı alınamadı: {str(e)}")

@router.post("/problems/detect")
async def detect_problem_manually(request: ProblemDetectionRequest):
    """Manuel problem tespiti"""
    try:
        from ..services.ai_problem_solver import DetectedProblem
        
        problem = DetectedProblem(
            problem_id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            category=request.category,
            severity=request.severity,
            title=request.title,
            description=request.description,
            component=request.component,
            symptoms=request.symptoms,
            detected_at=datetime.now(),
            metrics=request.metrics,
            impact_assessment={"manual_detection": True}
        )
        
        ai_problem_solver.detected_problems[problem.problem_id] = problem
        
        logger.info(f"🔍 Manual problem detected: {problem.title}")
        
        return {
            "success": True,
            "problem_id": problem.problem_id,
            "message": "Problem başarıyla tespit edildi",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Manual problem detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Problem tespit edilemedi: {str(e)}")

@router.post("/problems/{problem_id}/solve")
async def solve_problem_manually(problem_id: str, request: ManualSolutionRequest):
    """Manuel problem çözümü"""
    try:
        problem = ai_problem_solver.detected_problems.get(problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem bulunamadı")
        
        # Generate solution
        from ..services.ai_problem_solver import Solution
        
        solution = Solution(
            solution_id=f"manual_solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            problem_id=problem_id,
            solution_type=request.solution_type,
            title=f"Manuel Çözüm: {problem.title}",
            description="Kullanıcı tarafından talep edilen manuel çözüm",
            steps=request.custom_steps if request.custom_steps else ["Manuel müdahale uygulanıyor"],
            estimated_time="5-15 minutes",
            success_probability=0.8,
            risk_level="medium",
            prerequisites=[],
            rollback_plan="Manuel değişiklikler geri alınıyor"
        )
        
        # Execute solution
        result = await ai_problem_solver._execute_solution(problem, solution)
        ai_problem_solver.solution_history.append(result)
        
        if result.success:
            # Remove solved problem
            del ai_problem_solver.detected_problems[problem_id]
            logger.info(f"✅ Manual problem solved: {problem_id}")
        else:
            logger.warning(f"⚠️ Manual solution failed: {problem_id}")
        
        return {
            "success": result.success,
            "result": {
                "solution_applied": result.solution_applied.dict() if result.solution_applied else None,
                "execution_time_seconds": result.execution_time_seconds,
                "error_message": result.error_message,
                "system_state_after": result.system_state_after,
                "lessons_learned": result.lessons_learned
            },
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Manual problem solving error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Problem çözülemedi: {str(e)}")

@router.post("/system/analyze")
async def analyze_system(request: SystemAnalysisRequest):
    """Sistem analizi yap"""
    try:
        # Update system context
        await ai_problem_solver._update_system_context()
        
        analysis_result = {
            "analysis_depth": request.analysis_depth,
            "system_context": {
                "cpu_usage": ai_problem_solver.system_context.cpu_usage,
                "memory_usage": ai_problem_solver.system_context.memory_usage,
                "disk_usage": ai_problem_solver.system_context.disk_usage,
                "network_latency": ai_problem_solver.system_context.network_latency,
                "active_services": ai_problem_solver.system_context.active_services,
                "last_updated": ai_problem_solver.system_context.last_updated.isoformat()
            },
            "detected_issues": len(ai_problem_solver.detected_problems),
            "critical_issues": len([p for p in ai_problem_solver.detected_problems.values() if p.severity == ProblemSeverity.CRITICAL]),
            "recommendations": []
        }
        
        # Generate recommendations based on analysis depth
        if request.analysis_depth in ["standard", "deep"]:
            if ai_problem_solver.system_context.cpu_usage > 80:
                analysis_result["recommendations"].append("CPU kullanımı yüksek. Kaynak temizliği veya servis optimizasyonu önerilir.")
            
            if ai_problem_solver.system_context.memory_usage > 80:
                analysis_result["recommendations"].append("Bellek kullanımı yüksek. Memory leak taraması önerilir.")
            
            if len(ai_problem_solver.detected_problems) > 5:
                analysis_result["recommendations"].append("Çok sayıda aktif problem var. Otomatik çözüm sistemi aktive edilebilir.")
        
        if request.analysis_depth == "deep":
            # Add deep analysis recommendations
            analysis_result["recommendations"].extend([
                "Performans metrikleri izleme önerilir",
                "Otomatik problem çözüm sistemi optimize edilebilir",
                "Öğrenme sistemi güncellemeleri kontrol edilmeli"
            ])
        
        return {
            "success": True,
            "data": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"System analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sistem analizi yapılamadı: {str(e)}")

@router.post("/monitoring/start")
async def start_monitoring(background_tasks: BackgroundTasks):
    """AI asistan monitoring'ini başlat"""
    try:
        background_tasks.add_task(ai_problem_solver.start_continuous_monitoring)
        
        logger.info("🚀 AI Assistant monitoring started")
        
        return {
            "success": True,
            "message": "AI Assistant monitoring başlatıldı",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Start monitoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Monitoring başlatılamadı: {str(e)}")

@router.get("/learning/patterns")
async def get_learning_patterns():
    """Öğrenme sistemi pattern'larını al"""
    try:
        patterns = {
            "successful_patterns": {},
            "failed_attempts": {},
            "optimization_suggestions": ai_problem_solver.learning_system["optimization_suggestions"]
        }
        
        # Process successful patterns
        for category, results in ai_problem_solver.learning_system["successful_patterns"].items():
            patterns["successful_patterns"][category.value] = {
                "count": len(results),
                "most_common_solution": max(set([r.solution_applied.solution_type.value for r in results]), 
                                          key=lambda x: [r.solution_applied.solution_type.value for r in results].count(x)) if results else None,
                "avg_success_rate": sum(r.success for r in results) / len(results) if results else 0.0
            }
        
        # Process failed attempts
        for category, results in ai_problem_solver.learning_system["failed_attempts"].items():
            patterns["failed_attempts"][category.value] = {
                "count": len(results),
                "common_errors": list(set([r.error_message for r in results if r.error_message]))[:5]
            }
        
        return {
            "success": True,
            "data": patterns,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Get learning patterns error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Öğrenme pattern'ları alınamadı: {str(e)}")

@router.get("/solutions/history")
async def get_solution_history(limit: int = 50):
    """Çözüm geçmişini al"""
    try:
        # Get recent solutions
        recent_solutions = sorted(ai_problem_solver.solution_history, 
                                key=lambda x: x.execution_time_seconds, 
                                reverse=True)[:limit]
        
        history = []
        for result in recent_solutions:
            problem = ai_problem_solver.detected_problems.get(result.problem_id)
            history.append({
                "problem_id": result.problem_id,
                "problem_title": problem.title if problem else "Unknown Problem",
                "solution_applied": result.solution_applied.dict() if result.solution_applied else None,
                "success": result.success,
                "execution_time_seconds": result.execution_time_seconds,
                "error_message": result.error_message,
                "lessons_learned": result.lessons_learned,
                "timestamp": datetime.fromtimestamp(result.execution_time_seconds).isoformat()
            })
        
        return {
            "success": True,
            "count": len(history),
            "history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Get solution history error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Çözüm geçmişi alınamadı: {str(e)}")

@router.delete("/problems/{problem_id}")
async def dismiss_problem(problem_id: str):
    """Problem'i görmezden gel (çözülmeden kapat)"""
    try:
        if problem_id not in ai_problem_solver.detected_problems:
            raise HTTPException(status_code=404, detail="Problem bulunamadı")
        
        problem = ai_problem_solver.detected_problems[problem_id]
        del ai_problem_solver.detected_problems[problem_id]
        
        logger.info(f"🗑️ Problem dismissed: {problem_id}")
        
        return {
            "success": True,
            "message": f"Problem {problem_id} görmezden gelindi",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dismiss problem error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Problem görmezden gelinemedi: {str(e)}")

@router.get("/health")
async def get_ai_assistant_health():
    """AI asistan sağlık durumu"""
    try:
        health_status = {
            "status": "healthy",
            "monitoring_active": True,
            "total_problems": len(ai_problem_solver.detected_problems),
            "critical_problems": len([p for p in ai_problem_solver.detected_problems.values() if p.severity == ProblemSeverity.CRITICAL]),
            "solutions_applied": len(ai_problem_solver.solution_history),
            "success_rate": sum(1 for r in ai_problem_solver.solution_history if r.success) / len(ai_problem_solver.solution_history) if ai_problem_solver.solution_history else 1.0,
            "learning_system_active": True,
            "last_update": ai_problem_solver.system_context.last_updated.isoformat()
        }
        
        # Determine overall health
        if health_status["critical_problems"] > 0:
            health_status["status"] = "critical"
        elif health_status["total_problems"] > 10:
            health_status["status"] = "degraded"
        elif health_status["success_rate"] < 0.5:
            health_status["status"] = "degraded"
        
        return {
            "success": True,
            "data": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"AI assistant health check error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sağlık kontrolü yapılamadı: {str(e)}")
