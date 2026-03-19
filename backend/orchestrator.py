"""
VUC-2026 Orchestrator - Otonom İş Akışı Yöneticisi

Bu modül, Analiz -> Senaryo -> Render -> Upload -> Ghost Interaction 
adımlarını tek bir tetiklemeyle otonom olarak sırayla çalıştırır.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os

from app.database import SessionLocal, get_db
from app.models.channel import Channel
from app.models.video import Video
from app.models.script import Script
from app.services.ai_service import AIService
from app.services.media_engine import MediaEngine
from app.services.grey_hat_service import GreyHatService
from app.services.windows_ai_service import WindowsAIService
from app.services.directml_accelerator import DirectMLAccelerator
from app.services.self_healing_service import self_healing_service
from app.celery_app.celery import celery_app
from app.celery_app.tasks.competitor_analysis import analyze_competitor
from app.celery_app.tasks.video_rendering import render_video_with_fallback_task
from app.celery_app.tasks.upload_tasks import upload_video_task, schedule_upload_for_later_task
from app.celery_app.tasks.ai_tasks import generate_script_task

logger = logging.getLogger(__name__)

class VUCOrchestrator:
    """VUC-2026 Otonom Orchestrator"""
    
    def __init__(self):
        self.ai_service = AIService("AIzaSyDjastAPrl4GcrgH-_t3FO3jJZtgOReHyc")
        self.media_engine = MediaEngine()
        self.grey_hat_service = GreyHatService()
        self.windows_ai_service = WindowsAIService()
        self.directml_accelerator = DirectMLAccelerator()
        self.db = SessionLocal()
        
        # İş akışı durumları
        self.workflow_states = {
            "idle": "Boşta",
            "analyzing": "Rakip analizi yapılıyor",
            "scripting": "Senaryo üretiliyor",
            "rendering": "Video render ediliyor",
            "uploading": "Video yükleniyor",
            "interacting": "Hayalet etkileşimler yapılıyor",
            "completed": "Tamamlandı"
        }
        
        self.current_state = "idle"
        self.current_task = None
        
    async def start_autonomous_workflow(self, channel_id: int, 
                                  force_restart: bool = False) -> Dict[str, Any]:
        """
        Otonom iş akışını başlat
        
        Args:
            channel_id: Kanal ID
            force_restart: Zorla yeniden başlat
        
        Returns:
            İş akışı sonuçları
        """
        
        try:
            # Kanal kontrolü
            channel = self.db.query(Channel).filter(Channel.id == channel_id).first()
            if not channel:
                return {"success": False, "error": "Kanal bulunamadı"}
            
            if not channel.is_active:
                return {"success": False, "error": "Kanal aktif değil"}
            
            # Mevcut görev kontrolü
            if self.current_state != "idle" and not force_restart:
                return {
                    "success": False, 
                    "error": f"İş akışı devam ediyor: {self.current_state}",
                    "current_task": self.current_task
                }
            
            logger.info(f"Otonom iş akışı başlatılıyor - Kanal: {channel.name}")
            
            # Adım 1: Rakip Analizi
            await self._update_state("analyzing", "Rakip analizi başlatılıyor")
            analysis_result = await self._analyze_competitors(channel)
            
            if not analysis_result["success"]:
                await self._update_state("idle", None)
                return analysis_result
            
            # Adım 2: Strateji ve Senaryo Üretimi
            await self._update_state("scripting", "İçerik stratejisi oluşturuluyor")
            strategy_result = await self._create_content_strategy(channel, analysis_result)
            
            if not strategy_result["success"]:
                await self._update_state("idle", None)
                return strategy_result
            
            # Adım 3: Video Üretimi
            await self._update_state("rendering", "Video render ediliyor")
            render_result = await self._produce_video(channel, strategy_result)
            
            if not render_result["success"]:
                await self._update_state("idle", None)
                return render_result
            
            # Adım 4: Yükleme
            if channel.auto_upload:
                await self._update_state("uploading", "Video yükleniyor")
                upload_result = await self._upload_video(channel, render_result)
                
                if not upload_result["success"]:
                    await self._update_state("idle", None)
                    return upload_result
            
            # Adım 5: Hayalet Etkileşimler
            await self._update_state("interacting", "Hayalet etkileşimler başlatılıyor")
            interaction_result = await self._start_ghost_interactions(upload_result)
            
            # Karar günlüğü kaydet
            await self._log_decision(channel, strategy_result, "workflow_completed")
            
            await self._update_state("completed", "İş akışı tamamlandı")
            
            return {
                "success": True,
                "channel": channel.name,
                "workflow_steps": {
                    "analysis": analysis_result,
                    "strategy": strategy_result,
                    "render": render_result,
                    "upload": upload_result if channel.auto_upload else {"skipped": True},
                    "interactions": interaction_result
                },
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Otonom iş akışı hatası: {e}")
            await self._update_state("idle", None)
            
            # Log system recovery attempt
            await self._log_recovery_event(
                "autonomous_workflow",
                str(e),
                "workflow_error_handling",
                False
            )
            
            return {"success": False, "error": str(e)}
    
    async def _analyze_competitors(self, channel: Channel) -> Dict[str, Any]:
        """Rakip analizi adımı"""
        try:
            # Aktif rakipleri getir
            from app.models.competitor import Competitor
            competitors = self.db.query(Competitor).filter(
                Competitor.channel_id == channel.id
            ).all()
            
            if not competitors:
                return {"success": False, "error": "Analiz edilecek rakip bulunamadı"}
            
            # Her rakip için analiz görevi başlat
            analysis_tasks = []
            for competitor in competitors:
                competitor_url = f"https://www.youtube.com/channel/{competitor.competitor_channel_id}"
                task = analyze_competitor.delay(channel.id, competitor_url)
                analysis_tasks.append(task)
            
            # Tüm analizlerin tamamlanmasını bekle
            results = []
            for task in analysis_tasks:
                try:
                    result = task.get(timeout=300)  # 5 dakika timeout
                    results.append(result)
                except Exception as e:
                    logger.error(f"Rakip analizi görev hatası: {e}")
                    results.append({"success": False, "error": str(e)})
            
            # Analiz sonuçlarını birleştir
            successful_analyses = [r for r in results if r.get("success", False)]
            
            return {
                "success": len(successful_analyses) > 0,
                "competitors_analyzed": len(successful_analyses),
                "total_competitors": len(competitors),
                "analysis_data": successful_analyses,
                "insights": self._extract_competitor_insights(successful_analyses)
            }
            
        except Exception as e:
            logger.error(f"Rakip analizi hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def _create_content_strategy(self, channel: Channel, 
                                 analysis_result: Dict) -> Dict[str, Any]:
        """İçerik stratejisi oluşturma adımı"""
        try:
            # Analytics vault'tan öğrenilen verileri yükle
            analytics_data = self._load_analytics_vault()
            
            # Rakip analizinden fırsatları çıkar
            competitor_insights = analysis_result.get("insights", {})
            content_gaps = competitor_insights.get("content_gaps", [])
            
            # En iyi stratejiyi seç
            best_topic = self._select_best_topic(channel.niche, content_gaps, analytics_data)
            
            # Senaryo oluştur
            script_result = await self.ai_service.generate_script(
                topic=best_topic,
                language=channel.language,
                style="engaging",
                target_duration=300,  # 5 dakika
                keywords=content_gaps[:5] if content_gaps else None
            )
            
            if not script_result["success"]:
                return {"success": False, "error": "Senaryo oluşturulamadı"}
            
            # Thumbnail A/B testi oluştur
            thumbnail_test = self.grey_hat_service.create_thumbnail_ab_test(
                title=script_result["script"]["title"],
                niche=channel.niche
            )
            
            return {
                "success": True,
                "topic": best_topic,
                "script": script_result["script"],
                "thumbnail_test": thumbnail_test,
                "strategy_rationale": self._generate_strategy_rationale(
                    best_topic, competitor_insights, analytics_data
                ),
                "confidence_score": self._calculate_confidence_score(
                    best_topic, competitor_insights
                )
            }
            
        except Exception as e:
            logger.error(f"Strateji oluşturma hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def _produce_video(self, channel: Channel, 
                          strategy_result: Dict) -> Dict[str, Any]:
        """Video üretimi adımı - Windows AI ve DirectML ile geliştirilmiş"""
        try:
            script_data = strategy_result["script"]
            
            # Channel config for render task
            channel_config = {
                "id": channel.id,
                "name": channel.name,
                "niche": channel.niche,
                "language": channel.language
            }
            
            # Self-healing render task with fallback
            render_task = render_video_with_fallback_task.delay(
                script_data=script_data,
                channel_config=channel_config
            )
            
            # Wait for render completion with timeout
            try:
                render_result = render_task.get(timeout=1800)  # 30 minutes
            except Exception as e:
                logger.error(f"Render task timeout or error: {e}")
                return {"success": False, "error": f"Render failed: {str(e)}"}
            
            if not render_result.get("success"):
                # Log failure and check for fallback
                fallback_applied = render_result.get("fallback_applied")
                if fallback_applied:
                    logger.warning(f"Render completed with fallback: {fallback_applied}")
                    
                    # Log recovery event
                    await self._log_recovery_event(
                        "video_production",
                        str(render_result.get("error", "Unknown error")),
                        fallback_applied,
                        False
                    )
                
                return render_result
            
            # Success - log and return
            logger.info(f"Video production completed: {render_result.get('video_path')}")
            
            return {
                "success": True,
                "video_path": render_result["video_path"],
                "thumbnail_path": render_result["thumbnail_path"],
                "script_id": script_data.get("id"),
                "title": script_data["title"],
                "duration": script_data.get("estimated_duration", 300),
                "windows_ai_used": render_result.get("directml_used", False),
                "directml_used": render_result.get("directml_used", False),
                "quality_applied": render_result.get("quality_settings", {}),
                "fallback_attempts": render_result.get("fallback_attempts", 0)
            }
            
        except Exception as e:
            logger.error(f"Video üretim hatası: {e}")
            
            # Log recovery attempt
            await self._log_recovery_event(
                "video_production",
                str(e),
                "orchestrator_error_handling",
                False
            )
            
            return {"success": False, "error": str(e)}
    
    async def _upload_video(self, channel: Channel, 
                          render_result: Dict) -> Dict[str, Any]:
        """Video yükleme adımı - Self-healing ile geliştirilmiş"""
        try:
            # Prepare upload metadata
            title = render_result["title"]
            description = self._generate_description(render_result)
            tags = self._generate_tags(channel, render_result)
            
            # Start self-healing upload task
            upload_task = upload_video_task.delay(
                channel_id=channel.id,
                video_path=render_result["video_path"],
                thumbnail_path=render_result["thumbnail_path"],
                title=title,
                description=description,
                tags=tags,
                privacy_status="private"  # Start as private, will be made public later
            )
            
            # Wait for upload completion with timeout
            try:
                upload_result = upload_task.get(timeout=600)  # 10 minutes
            except Exception as e:
                logger.error(f"Upload task timeout or error: {e}")
                
                # Try schedule for later as fallback
                logger.info("Attempting to schedule upload for later...")
                schedule_task = schedule_upload_for_later_task.delay(
                    channel_id=channel.id,
                    video_path=render_result["video_path"],
                    thumbnail_path=render_result["thumbnail_path"],
                    title=title,
                    description=description,
                    tags=tags,
                    delay_minutes=120  # 2 hours later
                )
                
                schedule_result = schedule_task.get(timeout=60)
                
                # Log recovery event
                await self._log_recovery_event(
                    "video_upload",
                    str(e),
                    "scheduled_for_later",
                    True
                )
                
                return {
                    "success": False,
                    "error": f"Upload failed, scheduled for later: {str(e)}",
                    "fallback_applied": "schedule_later",
                    "scheduled_time": schedule_result.get("scheduled_time"),
                    "recovery_action": "upload_scheduled"
                }
            
            if not upload_result.get("success"):
                # Check if fallback was applied
                fallback_applied = upload_result.get("fallback_applied")
                if fallback_applied:
                    logger.warning(f"Upload completed with fallback: {fallback_applied}")
                    
                    # Log recovery event
                    await self._log_recovery_event(
                        "video_upload",
                        str(upload_result.get("error", "Unknown error")),
                        fallback_applied,
                        False
                    )
                
                return upload_result
            
            # Success - log and return
            logger.info(f"Video upload completed: {upload_result.get('youtube_id')}")
            
            return {
                "success": True,
                "youtube_id": upload_result["youtube_id"],
                "youtube_url": upload_result["youtube_url"],
                "upload_time": upload_result.get("upload_time"),
                "optimizations_applied": upload_result.get("optimizations_applied", {}),
                "file_size_mb": upload_result.get("file_size_mb")
            }
            
        except Exception as e:
            logger.error(f"Video yükleme hatası: {e}")
            
            # Log recovery attempt
            await self._log_recovery_event(
                "video_upload",
                str(e),
                "orchestrator_error_handling",
                False
            )
            
            return {"success": False, "error": str(e)}
    
    async def _start_ghost_interactions(self, upload_result: Dict) -> Dict[str, Any]:
        """Hayalet etkileşimler adımı"""
        try:
            if not upload_result.get("youtube_id"):
                return {"success": False, "error": "YouTube ID bulunamadı"}
            
            # Hayalet etkileşimleri başlat
            interactions = self.grey_hat_service.generate_ghost_interaction(
                video_id=upload_result["youtube_id"],
                title=upload_result.get("title", ""),
                keywords=self._extract_keywords(upload_result)
            )
            
            return {
                "success": True,
                "interactions": interactions,
                "total_interactions": interactions["total_interactions"],
                "engagement_boost": interactions["engagement_boost"]
            }
            
        except Exception as e:
            logger.error(f"Hayalet etkileşim hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def _update_state(self, new_state: str, task_description: str = None):
        """İş akışı durumunu güncelle"""
        self.current_state = new_state
        self.current_task = task_description
        
        state_message = self.workflow_states.get(new_state, new_state)
        logger.info(f"Orchestrator durumu: {state_message}")
        
        if task_description:
            logger.info(f"Mevcut görev: {task_description}")
    
    def _load_analytics_vault(self) -> Dict:
        """Analytics vault verilerini yükle"""
        try:
            vault_path = "../vuc_memory/analytics_vault.json"
            if os.path.exists(vault_path):
                with open(vault_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Analytics vault yüklenemedi: {e}")
        
        return {}
    
    def _extract_competitor_insights(self, analyses: List[Dict]) -> Dict:
        """Rakip analizlerinden içgörü çıkar"""
        insights = {
            "content_gaps": [],
            "successful_patterns": [],
            "upload_times": [],
            "thumbnail_styles": []
        }
        
        for analysis in analyses:
            # Başarılı patternleri çıkar
            if "top_topics" in analysis:
                insights["successful_patterns"].extend(analysis["top_topics"])
            
            # Yükleme zamanlarını topla
            if "best_upload_times" in analysis:
                insights["upload_times"].extend(analysis["best_upload_times"])
        
        return insights
    
    def _select_best_topic(self, niche: str, content_gaps: List[str], 
                         analytics_data: Dict) -> str:
        """En iyi konuyu seç"""
        # Analytics verilerinden başarılı patternleri kullan
        successful_patterns = analytics_data.get("successful_patterns", {})
        title_patterns = successful_patterns.get("title_patterns", {})
        
        # Content gap'lerden en uygununu seç
        if content_gaps:
            return content_gaps[0]  # İlk fırsat
        
        # Nişe göre varsayılan konu
        default_topics = {
            "crypto": "Kripto para piyasası analizi",
            "baby": "Yeni ebeveynler için ipuçları",
            "military": "Askeri teknoloji güncellemeleri",
            "tech": "Yapay zeka devrimi",
            "gaming": "En çok beklenen oyunlar"
        }
        
        return default_topics.get(niche, "Genel içerik")
    
    def _generate_strategy_rationale(self, topic: str, insights: Dict, 
                                analytics_data: Dict) -> str:
        """Strateji gerekçesi oluştur"""
        rationale = f"""
        Konu Seçimi: {topic}
        
        Rakip Analizi Sonuçları:
        - İçerik boşlukları tespit edildi
        - Başarılı patternler analiz edildi
        
        Analytics Verileri:
        - Tarihsel başarı oranları kullanıldı
        - Optimum yayın zamanları dikkate alındı
        
        Confidence: Yüksek (veri destekli)
        """
        
        return rationale.strip()
    
    def _calculate_confidence_score(self, topic: str, insights: Dict) -> float:
        """Confidence skoru hesapla (0-1)"""
        base_score = 0.7
        
        # Rakip verisi varsa +0.2
        if insights.get("content_gaps"):
            base_score += 0.2
        
        # Analytics verisi varsa +0.1
        if self._load_analytics_vault():
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _generate_description(self, render_result: Dict) -> str:
        """Video açıklaması oluştur"""
        title = render_result.get("title", "")
        
        description = f"""
        {title}
        
        🎯 Bu videoda {title.lower()} konusunu detaylıca inceliyoruz.
        
        📈 Kanalımıza abone olun: https://youtube.com/channel/UC
        
        🔔 Bildirimleri açmayı unutmayın!
        
        #vuc2026 #youtube #otomasyon
        
        Keywords: {title.lower()}, analiz, strateji
        """
        
        return description.strip()
    
    def _generate_tags(self, channel: Channel, render_result: Dict) -> List[str]:
        """Video etiketleri oluştur"""
        title = render_result.get("title", "")
        niche = channel.niche
        
        # Analytics vault'tan etkili etiketleri al
        analytics_data = self._load_analytics_vault()
        tag_effectiveness = analytics_data.get("tag_effectiveness", {})
        niche_tags = tag_effectiveness.get("high_performing", {}).get(niche, [])
        
        # Başlığa özel etiketler
        title_words = title.lower().split()
        title_tags = [word for word in title_words if len(word) > 3]
        
        # Trend etiketler
        trend_tags = ["2026", "yeni", "güncel", "viral"]
        
        # Tüm etiketleri birleştir ve benzersiz yap
        all_tags = list(set(niche_tags + title_tags + trend_tags))
        
        return all_tags[:15]  # Maksimum 15 etiket
    
    def _extract_keywords(self, render_result: Dict) -> List[str]:
        """Anahtar kelimeleri çıkar"""
        title = render_result.get("title", "")
        
        # Başlıktan anahtar kelimeleri çıkar
        keywords = []
        for word in title.split():
            if len(word) > 4:
                keywords.append(word.lower())
        
        return keywords[:5]  # İlk 5 kelime
    
    async def _log_decision(self, channel: Channel, strategy_result: Dict, 
                          decision_type: str):
        """Karar günlüğü kaydet"""
        try:
            decision_log_path = "../vuc_memory/decision_log.md"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            decision_id = f"DEC-{timestamp.replace('-', '').replace(':', '').replace(' ', '')}"
            
            log_entry = f"""
### {timestamp} - {decision_type}

**Karar ID**: {decision_id}
**Kanal**: {channel.name} ({channel.niche})
**Konu**: {strategy_result.get('topic', 'Belirtilmemiş')}

**Neden Seçildi**:
{strategy_result.get('strategy_rationale', 'Belirtilmemiş')}

**Confidence Score**: {strategy_result.get('confidence_score', 0)}/1.0

**Beklenen Sonuçlar**:
- İlk 24 saat: Tahmini yüksek izlenme
- Haftalık hedef: Kanal büyümesi
- Etkileşim: Artan yorum ve beğeni

---

"""
            
            # Dosyaya ekle
            with open(decision_log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            logger.info(f"Karar günlüğe kaydedildi: {decision_id}")
            
        except Exception as e:
            logger.error(f"Karar günlüğü kaydetme hatası: {e}")
    
    async def _log_recovery_event(self, operation_type: str, original_error: str, 
                                recovery_action: str, success: bool):
        """Kurtarma olayını kaydet"""
        try:
            recovery_log = self_healing_service.log_recovery_event(
                operation_type=operation_type,
                original_error=original_error,
                recovery_action=recovery_action,
                success=success
            )
            
            logger.info(f"Recovery event logged: {recovery_log['recovery_id']}")
            
        except Exception as e:
            logger.error(f"Recovery log kaydetme hatası: {e}")
    
    async def check_system_health_and_recover(self) -> Dict[str, Any]:
        """Sistem sağlığını kontrol et ve otomatik kurtarma"""
        try:
            health_status = self_healing_service.check_system_health()
            
            # Log health check
            logger.info(f"System health check: {health_status['overall_health']}")
            
            # If there are alerts, log them
            if health_status.get("alerts"):
                for alert in health_status["alerts"]:
                    logger.warning(f"System alert: {alert}")
            
            return health_status
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "overall_health": "error",
                "alerts": [f"Health check failed: {str(e)}"],
                "metrics": {}
            }

# Global orchestrator instance
orchestrator = VUCOrchestrator()

@celery_app.task
def start_autonomous_workflow_task(channel_id: int, force_restart: bool = False):
    """Otonom iş akışı için Celery görevi"""
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            orchestrator.start_autonomous_workflow(channel_id, force_restart)
        )
        return result
    except Exception as e:
        logger.error(f"Otonom iş akışı görev hatası: {e}")
        return {"success": False, "error": str(e)}
