"""
VUC-2026 YouTube Compliance Orchestrator
Tüm compliance modüllerini koordine eden ana orchestrator
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..services.anti_spam_protocol import AntiSpamProtocol
from ..services.ai_disclosure_compliance import AIDisclosureCompliance
from ..services.engagement_authenticity import EngagementAuthenticity
from ..services.clickbait_optimization import ClickbaitOptimization

class ComplianceStage(Enum):
    """Compliance aşamaları"""
    INITIALIZED = "initialized"
    ANTI_SPAM_PROCESSING = "anti_spam_processing"
    AI_DISCLOSURE_PENDING = "ai_disclosure_pending"
    HUMAN_REVIEW_PENDING = "human_review_pending"
    TITLE_OPTIMIZATION = "title_optimization"
    ENGAGEMENT_CAMPAIGN = "engagement_campaign"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ComplianceTask:
    """Compliance görevi"""
    task_id: str
    video_id: str
    video_path: str
    video_metadata: Dict
    stage: ComplianceStage
    created_at: datetime
    updated_at: datetime
    results: Dict
    errors: List[str]

class YouTubeComplianceOrchestrator:
    """YouTube Compliance Orchestrator"""
    
    def __init__(self, gemini_service, youtube_api_service):
        self.gemini_service = gemini_service
        self.youtube_api = youtube_api_service
        
        # Servisleri başlat
        self.anti_spam = AntiSpamProtocol(gemini_service)
        self.ai_disclosure = AIDisclosureCompliance(youtube_api_service)
        self.engagement_auth = EngagementAuthenticity(gemini_service, youtube_api_service)
        self.clickbait_opt = ClickbaitOptimization(gemini_service, youtube_api_service)
        
        # Task yönetimi
        self.active_tasks = {}
        self.completed_tasks = []
    
    def create_compliance_task(self, video_id: str, video_path: str, video_metadata: Dict) -> str:
        """Yeni compliance görevi oluştur"""
        task_id = f"compliance_{video_id}_{int(datetime.now().timestamp())}"
        
        task = ComplianceTask(
            task_id=task_id,
            video_id=video_id,
            video_path=video_path,
            video_metadata=video_metadata,
            stage=ComplianceStage.INITIALIZED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            results={},
            errors=[]
        )
        
        self.active_tasks[task_id] = task
        return task_id
    
    async def execute_compliance_pipeline(self, task_id: str, config: Dict = None) -> Dict:
        """Compliance pipeline'ını çalıştır"""
        if task_id not in self.active_tasks:
            return {"error": "Task not found"}
        
        task = self.active_tasks[task_id]
        config = config or {}
        
        try:
            # Stage 1: Anti-Spam Processing
            await self._execute_anti_spam_stage(task)
            
            # Stage 2: AI Disclosure
            await self._execute_ai_disclosure_stage(task)
            
            # Stage 3: Human Review (gerekirse)
            if task.stage == ComplianceStage.HUMAN_REVIEW_PENDING:
                return {"status": "human_review_required", "task_id": task_id}
            
            # Stage 4: Title Optimization
            await self._execute_title_optimization_stage(task)
            
            # Stage 5: Engagement Campaign (isteğe bağlı)
            if config.get("run_engagement_campaign", False):
                await self._execute_engagement_stage(task)
            
            # Stage 6: Complete
            task.stage = ComplianceStage.COMPLETED
            task.updated_at = datetime.now()
            
            # Task'i completed'e taşı
            self.completed_tasks.append(task)
            del self.active_tasks[task_id]
            
            return {
                "success": True,
                "task_id": task_id,
                "stage": task.stage.value,
                "results": task.results,
                "compliance_score": self._calculate_overall_compliance_score(task)
            }
            
        except Exception as e:
            task.stage = ComplianceStage.FAILED
            task.errors.append(str(e))
            task.updated_at = datetime.now()
            
            return {
                "success": False,
                "task_id": task_id,
                "error": str(e),
                "stage": task.stage.value
            }
    
    async def _execute_anti_spam_stage(self, task: ComplianceTask):
        """Anti-spam aşamasını çalıştır"""
        task.stage = ComplianceStage.ANTI_SPAM_PROCESSING
        task.updated_at = datetime.now()
        
        try:
            # Videoyu benzersizleştir
            base_content = task.video_metadata.get("script_content", "")
            competitor_analysis = task.video_metadata.get("competitor_analysis", {})
            
            processed_video, metadata = self.anti_spam.process_video(
                task.video_path, 
                base_content, 
                competitor_analysis
            )
            
            # Compliance raporu
            compliance_report = self.anti_spam.get_compliance_report(metadata)
            
            task.results["anti_spam"] = {
                "processed_video_path": processed_video,
                "unique_metadata": metadata,
                "compliance_report": compliance_report,
                "stage_completed_at": datetime.now().isoformat()
            }
            
            task.video_path = processed_video  # Güncellenmiş video path
            
        except Exception as e:
            task.errors.append(f"Anti-spam processing failed: {str(e)}")
            raise
    
    async def _execute_ai_disclosure_stage(self, task: ComplianceTask):
        """AI disclosure aşamasını çalıştır"""
        task.stage = ComplianceStage.AI_DISCLOSURE_PENDING
        task.updated_at = datetime.now()
        
        try:
            # AI disclosure işle
            disclosure_result = self.ai_disclosure.process_video(
                task.video_id,
                task.video_path,
                task.video_metadata
            )
            
            task.results["ai_disclosure"] = {
                "disclosure_result": disclosure_result,
                "stage_completed_at": datetime.now().isoformat()
            }
            
            # İnsan denetimi gerekiyorsa bekle
            if disclosure_result.get("next_step") == "human_approval_required":
                task.stage = ComplianceStage.HUMAN_REVIEW_PENDING
                return
            
            # Otomatik onay varsa YouTube'a uygula
            if disclosure_result.get("compliance_status") == "compliant":
                success = self.ai_disclosure.apply_disclosure_to_youtube(
                    task.video_id,
                    disclosure_result["ai_disclosure"]
                )
                
                task.results["ai_disclosure"]["youtube_applied"] = success
            
        except Exception as e:
            task.errors.append(f"AI disclosure processing failed: {str(e)}")
            raise
    
    async def _execute_title_optimization_stage(self, task: ComplianceTask):
        """Title optimization aşamasını çalıştır"""
        task.stage = ComplianceStage.TITLE_OPTIMIZATION
        task.updated_at = datetime.now()
        
        try:
            original_title = task.video_metadata.get("title", "")
            video_keywords = task.video_metadata.get("keywords", [])
            target_audience = task.video_metadata.get("target_audience", "general")
            
            # Başlığı optimize et
            optimization_result = self.clickbait_opt.optimize_title(
                task.video_id,
                original_title,
                video_keywords,
                target_audience
            )
            
            # A/B testini çalıştır
            test_results = await self.clickbait_opt.run_optimization_test(
                optimization_result["test_id"]
            )
            
            # En iyi başlığı seç
            best_title = test_results.get("best_variant", {}).get("title", original_title)
            
            task.results["title_optimization"] = {
                "optimization_result": optimization_result,
                "test_results": test_results,
                "selected_title": best_title,
                "stage_completed_at": datetime.now().isoformat()
            }
            
            # Video metadata'sını güncelle
            task.video_metadata["optimized_title"] = best_title
            
        except Exception as e:
            task.errors.append(f"Title optimization failed: {str(e)}")
            raise
    
    async def _execute_engagement_stage(self, task: ComplianceTask):
        """Engagement campaign aşamasını çalıştır"""
        task.stage = ComplianceStage.ENGAGEMENT_CAMPAIGN
        task.updated_at = datetime.now()
        
        try:
            video_topic = task.video_metadata.get("topic", "")
            persona_types_str = task.video_metadata.get("persona_types", ["tech_wizard", "business_guru"])
            
            # String'i enum'a çevir
            from ..services.engagement_authenticity import PersonaType
            persona_types = []
            for p_type in persona_types_str:
                try:
                    persona_types.append(PersonaType(p_type))
                except ValueError:
                    continue
            
            # Kampanya oluştur ve çalıştır
            campaign_id = self.engagement_auth.create_engagement_campaign(
                task.video_id,
                video_topic,
                persona_types
            )
            
            campaign_results = await self.engagement_auth.execute_campaign(campaign_id)
            
            # Otantiklik raporu
            authenticity_report = self.engagement_auth.get_authenticity_report(campaign_id)
            
            task.results["engagement_campaign"] = {
                "campaign_id": campaign_id,
                "campaign_results": campaign_results,
                "authenticity_report": authenticity_report,
                "stage_completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            task.errors.append(f"Engagement campaign failed: {str(e)}")
            raise
    
    def submit_human_review(self, task_id: str, review_data: Dict) -> Dict:
        """İnsan denetimini gönder"""
        if task_id not in self.active_tasks:
            return {"error": "Task not found"}
        
        task = self.active_tasks[task_id]
        
        if task.stage != ComplianceStage.HUMAN_REVIEW_PENDING:
            return {"error": "Task not in human review stage"}
        
        try:
            # AI disclosure'a gönder
            review_id = task.results["ai_disclosure"]["disclosure_result"]["review_id"]
            review_result = self.ai_disclosure.human_loop.submit_review(review_id, review_data)
            
            # YouTube'a disclosure uygula
            if review_result.get("approval_status", False):
                ai_disclosure = task.results["ai_disclosure"]["disclosure_result"]["ai_disclosure"]
                success = self.ai_disclosure.apply_disclosure_to_youtube(task.video_id, ai_disclosure)
                
                task.results["ai_disclosure"]["youtube_applied"] = success
                task.results["ai_disclosure"]["human_review_result"] = review_result
                
                # Pipeline'a devam et
                asyncio.create_task(self._continue_pipeline_after_review(task_id))
                
                return {
                    "success": True,
                    "review_result": review_result,
                    "pipeline_continued": True
                }
            else:
                task.results["ai_disclosure"]["human_review_result"] = review_result
                task.stage = ComplianceStage.FAILED
                task.errors.append("Human review rejected")
                
                return {
                    "success": False,
                    "review_result": review_result,
                    "pipeline_stopped": True
                }
                
        except Exception as e:
            task.errors.append(f"Human review submission failed: {str(e)}")
            return {"error": str(e)}
    
    async def _continue_pipeline_after_review(self, task_id: str):
        """İnsan denetiminden sonra pipeline'a devam et"""
        if task_id not in self.active_tasks:
            return
        
        task = self.active_tasks[task_id]
        
        try:
            # Title optimization ve sonraki aşamalar
            await self._execute_title_optimization_stage(task)
            
            # Engagement campaign (config'e bağlı)
            config = {"run_engagement_campaign": False}  # Varsayılan olarak kapalı
            if config.get("run_engagement_campaign", False):
                await self._execute_engagement_stage(task)
            
            # Complete
            task.stage = ComplianceStage.COMPLETED
            task.updated_at = datetime.now()
            
            # Task'i completed'e taşı
            self.completed_tasks.append(task)
            del self.active_tasks[task_id]
            
        except Exception as e:
            task.stage = ComplianceStage.FAILED
            task.errors.append(f"Post-review pipeline failed: {str(e)}")
            task.updated_at = datetime.now()
    
    def _calculate_overall_compliance_score(self, task: ComplianceTask) -> float:
        """Genel uyumluluk skoru hesapla"""
        scores = []
        
        # Anti-spam skoru
        if "anti_spam" in task.results:
            anti_spam_score = task.results["anti_spam"]["compliance_report"]["compliance_score"]
            scores.append(anti_spam_score)
        
        # AI disclosure skoru
        if "ai_disclosure" in task.results:
            compliance_report = self.ai_disclosure.get_compliance_report(task.video_id)
            ai_disclosure_score = compliance_report.get("compliance_score", 0)
            scores.append(ai_disclosure_score)
        
        # Title optimization skoru
        if "title_optimization" in task.results:
            best_variant = task.results["title_optimization"]["test_results"].get("best_variant", {})
            title_score = best_variant.get("compliance_score", 70)
            scores.append(title_score)
        
        # Engagement authenticity skoru
        if "engagement_campaign" in task.results:
            authenticity_report = task.results["engagement_campaign"]["authenticity_report"]
            engagement_score = authenticity_report.get("authenticity_score", 70)
            scores.append(engagement_score)
        
        # Ortalama skoru hesapla
        if scores:
            return sum(scores) / len(scores)
        
        return 0.0
    
    def get_task_status(self, task_id: str) -> Dict:
        """Task durumunu getir"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
        elif any(t.task_id == task_id for t in self.completed_tasks):
            task = next(t for t in self.completed_tasks if t.task_id == task_id)
        else:
            return {"error": "Task not found"}
        
        return {
            "task_id": task.task_id,
            "video_id": task.video_id,
            "stage": task.stage.value,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
            "results": task.results,
            "errors": task.errors,
            "compliance_score": self._calculate_overall_compliance_score(task) if task.stage == ComplianceStage.COMPLETED else None
        }
    
    def get_compliance_dashboard(self) -> Dict:
        """Compliance dashboard'ı"""
        total_tasks = len(self.active_tasks) + len(self.completed_tasks)
        completed_count = len(self.completed_tasks)
        
        # Stage bazında sayım
        stage_counts = {}
        for task in self.active_tasks.values():
            stage_counts[task.stage.value] = stage_counts.get(task.stage.value, 0) + 1
        
        # Ortalama compliance skorları
        if self.completed_tasks:
            avg_scores = [self._calculate_overall_compliance_score(task) for task in self.completed_tasks]
            avg_compliance = sum(avg_scores) / len(avg_scores)
        else:
            avg_compliance = 0.0
        
        return {
            "overview": {
                "total_tasks": total_tasks,
                "active_tasks": len(self.active_tasks),
                "completed_tasks": completed_count,
                "success_rate": (completed_count / total_tasks * 100) if total_tasks > 0 else 0,
                "average_compliance_score": avg_compliance
            },
            "active_stages": stage_counts,
            "recent_tasks": [
                {
                    "task_id": task.task_id,
                    "video_id": task.video_id,
                    "stage": task.stage.value,
                    "updated_at": task.updated_at.isoformat()
                }
                for task in list(self.active_tasks.values())[:5]
            ],
            "service_health": {
                "anti_spam_protocol": "healthy",
                "ai_disclosure_compliance": "healthy",
                "engagement_authenticity": "healthy",
                "clickbait_optimization": "healthy"
            }
        }
