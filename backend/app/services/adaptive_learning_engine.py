"""
VUC-2026 Adaptive Learning Engine
Sürekli kendini geliştiren ve öğrenen sistem
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import json
import asyncio
import logging
from enum import Enum
import pickle
import os
from dataclasses import dataclass

class LearningType(str, Enum):
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ERROR_PATTERN_RECOGNITION = "error_pattern_recognition"
    SUCCESS_PATTERN_ANALYSIS = "success_pattern_analysis"
    USER_BEHAVIOR_LEARNING = "user_behavior_learning"
    CONTENT_STRATEGY_ADAPTATION = "content_strategy_adaptation"
    SYSTEM_RESOURCE_OPTIMIZATION = "system_resource_optimization"

class AdaptationStrategy(str, Enum):
    AUTOMATIC_TUNING = "automatic_tuning"
    PARAMETER_ADJUSTMENT = "parameter_adjustment"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    RESOURCE_REALLOCATION = "resource_reallocation"
    ALGORITHM_SWITCHING = "algorithm_switching"
    BEHAVIOR_MODIFICATION = "behavior_modification"

@dataclass
class LearningPattern:
    pattern_id: str
    learning_type: LearningType
    context: Dict[str, Any]
    success_rate: float
    confidence_score: float
    frequency: int
    last_applied: datetime
    impact_score: float

@dataclass
class AdaptationRecord:
    adaptation_id: str
    strategy: AdaptationStrategy
    trigger_event: str
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    improvement_score: float
    timestamp: datetime
    success: bool

class AdaptiveLearningEngine:
    """VUC-2026 Adaptive Learning Engine - Sürekli Kendini Geliştiren Sistem"""
    
    def __init__(self):
        self.logger = logging.getLogger("vuc_adaptive_learning")
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.adaptation_history: List[AdaptationRecord] = []
        self.performance_metrics: Dict[str, List[float]] = {}
        self.learning_state = {
            "total_learning_cycles": 0,
            "successful_adaptations": 0,
            "failed_adaptations": 0,
            "average_improvement": 0.0,
            "learning_velocity": 0.0
        }
        self.adaptation_thresholds = {
            "min_confidence": 0.7,
            "min_improvement": 0.05,
            "max_frequency": 100,
            "learning_interval": 300  # 5 minutes
        }
        self._initialize_base_patterns()
        
    def _initialize_base_patterns(self):
        """Temel öğrenme pattern'lerini başlat"""
        base_patterns = [
            LearningPattern(
                pattern_id="perf_cpu_optimization",
                learning_type=LearningType.PERFORMANCE_OPTIMIZATION,
                context={"metric": "cpu_usage", "threshold": 80},
                success_rate=0.85,
                confidence_score=0.8,
                frequency=15,
                last_applied=datetime.now() - timedelta(hours=2),
                impact_score=0.15
            ),
            LearningPattern(
                pattern_id="error_api_timeout",
                learning_type=LearningType.ERROR_PATTERN_RECOGNITION,
                context={"error_type": "timeout", "component": "api"},
                success_rate=0.92,
                confidence_score=0.9,
                frequency=8,
                last_applied=datetime.now() - timedelta(hours=1),
                impact_score=0.25
            ),
            LearningPattern(
                pattern_id="success_video_production",
                learning_type=LearningType.SUCCESS_PATTERN_ANALYSIS,
                context={"process": "video_production", "stage": "rendering"},
                success_rate=0.95,
                confidence_score=0.85,
                frequency=25,
                last_applied=datetime.now() - timedelta(minutes=30),
                impact_score=0.20
            ),
            LearningPattern(
                pattern_id="content_engagement_boost",
                learning_type=LearningType.CONTENT_STRATEGY_ADAPTATION,
                context={"content_type": "kids_video", "metric": "engagement"},
                success_rate=0.78,
                confidence_score=0.75,
                frequency=12,
                last_applied=datetime.now() - timedelta(hours=3),
                impact_score=0.30
            ),
            LearningPattern(
                pattern_id="resource_memory_cleanup",
                learning_type=LearningType.SYSTEM_RESOURCE_OPTIMIZATION,
                context={"resource": "memory", "action": "cleanup"},
                success_rate=0.88,
                confidence_score=0.82,
                frequency=20,
                last_applied=datetime.now() - timedelta(minutes=45),
                impact_score=0.12
            )
        ]
        
        for pattern in base_patterns:
            self.learning_patterns[pattern.pattern_id] = pattern
    
    async def start_continuous_learning(self):
        """Sürekli öğrenme döngüsünü başlat"""
        self.logger.info("🧠 VUC-2026 Adaptive Learning Engine starting...")
        
        while True:
            try:
                await self._learning_cycle()
                await asyncio.sleep(self.adaptation_thresholds["learning_interval"])
            except Exception as e:
                self.logger.error(f"Learning cycle error: {e}")
                await asyncio.sleep(60)
    
    async def _learning_cycle(self):
        """Ana öğrenme döngüsü"""
        self.learning_state["total_learning_cycles"] += 1
        
        # 1. Performans verilerini topla
        await self._collect_performance_metrics()
        
        # 2. Pattern'leri analiz et
        await self._analyze_patterns()
        
        # 3. Adaptasyon fırsatlarını tespit et
        adaptation_opportunities = await self._identify_adaptation_opportunities()
        
        # 4. Adaptasyonları uygula
        for opportunity in adaptation_opportunities:
            await self._apply_adaptation(opportunity)
        
        # 5. Sonuçları değerlendir
        await self._evaluate_adaptations()
        
        # 6. Learning state'i güncelle
        await self._update_learning_state()
        
        self.logger.info(f"🔄 Learning cycle {self.learning_state['total_learning_cycles']} completed")
    
    async def _collect_performance_metrics(self):
        """Performans metriklerini topla"""
        try:
            # CPU, Memory, Network metrikleri
            import psutil
            
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Metrikleri kaydet
            timestamp = datetime.now()
            
            if "cpu_usage" not in self.performance_metrics:
                self.performance_metrics["cpu_usage"] = []
            if "memory_usage" not in self.performance_metrics:
                self.performance_metrics["memory_usage"] = []
            if "disk_usage" not in self.performance_metrics:
                self.performance_metrics["disk_usage"] = []
            
            self.performance_metrics["cpu_usage"].append(cpu_usage)
            self.performance_metrics["memory_usage"].append(memory.percent)
            self.performance_metrics["disk_usage"].append(disk.percent)
            
            # Son 100 veriyi tut
            for metric in self.performance_metrics:
                if len(self.performance_metrics[metric]) > 100:
                    self.performance_metrics[metric] = self.performance_metrics[metric][-100:]
            
            # API response time'ları
            await self._collect_api_metrics()
            
        except Exception as e:
            self.logger.error(f"Failed to collect performance metrics: {e}")
    
    async def _collect_api_metrics(self):
        """API metriklerini topla"""
        try:
            import aiohttp
            
            endpoints = [
                "http://127.0.0.1:8002/health",
                "http://127.0.0.1:8003/api/production/dashboard",
                "http://127.0.0.1:8004/api/self-healing/health"
            ]
            
            for endpoint in endpoints:
                try:
                    start_time = datetime.now()
                    async with aiohttp.ClientSession() as session:
                        async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            response_time = (datetime.now() - start_time).total_seconds() * 1000
                            
                            endpoint_name = endpoint.split("/")[-2] + "_" + endpoint.split("/")[-1]
                            if endpoint_name not in self.performance_metrics:
                                self.performance_metrics[endpoint_name] = []
                            
                            self.performance_metrics[endpoint_name].append(response_time)
                            
                            if len(self.performance_metrics[endpoint_name]) > 50:
                                self.performance_metrics[endpoint_name] = self.performance_metrics[endpoint_name][-50:]
                
                except Exception:
                    # Endpoint unavailable - bu da bir öğrenme verisi
                    pass
                    
        except Exception as e:
            self.logger.error(f"Failed to collect API metrics: {e}")
    
    async def _analyze_patterns(self):
        """Pattern'leri analiz et"""
        for pattern_id, pattern in self.learning_patterns.items():
            try:
                # Pattern context'ini kontrol et
                if await self._pattern_context_matches(pattern):
                    # Pattern başarı skorunu güncelle
                    new_success_rate = await self._calculate_pattern_success_rate(pattern)
                    pattern.success_rate = (pattern.success_rate + new_success_rate) / 2
                    
                    # Confidence score'u güncelle
                    pattern.frequency += 1
                    if pattern.frequency > 10:
                        pattern.confidence_score = min(0.95, pattern.confidence_score + 0.01)
                    
                    # Impact score'u güncelle
                    pattern.impact_score = await self._calculate_pattern_impact(pattern)
                    
            except Exception as e:
                self.logger.error(f"Failed to analyze pattern {pattern_id}: {e}")
    
    async def _pattern_context_matches(self, pattern: LearningPattern) -> bool:
        """Pattern context'inin mevcut durumla eşleşip eşleşmediğini kontrol et"""
        context = pattern.context
        
        if "metric" in context:
            metric_name = context["metric"]
            if metric_name in self.performance_metrics:
                current_value = self.performance_metrics[metric_name][-1] if self.performance_metrics[metric_name] else 0
                threshold = context.get("threshold", 80)
                
                if context.get("condition", "greater_than") == "greater_than":
                    return current_value > threshold
                else:
                    return current_value < threshold
        
        return False
    
    async def _calculate_pattern_success_rate(self, pattern: LearningPattern) -> float:
        """Pattern başarı oranını hesapla"""
        # Basit başarı hesaplaması - gerçek sistemde daha karmaşık olur
        base_rate = pattern.success_rate
        
        # Son uygulamaların başarısını kontrol et
        recent_adaptations = [a for a in self.adaptation_history 
                            if a.timestamp > datetime.now() - timedelta(hours=24)]
        
        if recent_adaptations:
            success_count = len([a for a in recent_adaptations if a.success])
            recent_success_rate = success_count / len(recent_adaptations)
            
            # Weighted average
            return (base_rate * 0.7 + recent_success_rate * 0.3)
        
        return base_rate
    
    async def _calculate_pattern_impact(self, pattern: LearningPattern) -> float:
        """Pattern etki skorunu hesapla"""
        # Pattern'in sistem performansı üzerindeki etkisini ölç
        base_impact = pattern.impact_score
        
        # Frequency ve confidence'a göre ayarla
        frequency_factor = min(1.0, pattern.frequency / 50)
        confidence_factor = pattern.confidence_score
        
        return base_impact * frequency_factor * confidence_factor
    
    async def _identify_adaptation_opportunities(self) -> List[Dict[str, Any]]:
        """Adaptasyon fırsatlarını tespit et"""
        opportunities = []
        
        for pattern_id, pattern in self.learning_patterns.items():
            # Threshold kontrolü
            if (pattern.confidence_score >= self.adaptation_thresholds["min_confidence"] and
                pattern.impact_score >= self.adaptation_thresholds["min_improvement"] and
                pattern.frequency <= self.adaptation_thresholds["max_frequency"]):
                
                # Son uygulama zamanını kontrol et
                time_since_last = datetime.now() - pattern.last_applied
                if time_since_last.total_seconds() > 300:  # 5 minutes
                    
                    opportunities.append({
                        "pattern_id": pattern_id,
                        "pattern": pattern,
                        "strategy": self._select_adaptation_strategy(pattern),
                        "priority": pattern.impact_score * pattern.confidence_score
                    })
        
        # Priority'ye göre sırala
        opportunities.sort(key=lambda x: x["priority"], reverse=True)
        
        return opportunities[:3]  # En iyi 3 fırsat
    
    def _select_adaptation_strategy(self, pattern: LearningPattern) -> AdaptationStrategy:
        """Pattern için adaptasyon stratejisi seç"""
        strategy_mapping = {
            LearningType.PERFORMANCE_OPTIMIZATION: AdaptationStrategy.AUTOMATIC_TUNING,
            LearningType.ERROR_PATTERN_RECOGNITION: AdaptationStrategy.PARAMETER_ADJUSTMENT,
            LearningType.SUCCESS_PATTERN_ANALYSIS: AdaptationStrategy.WORKFLOW_OPTIMIZATION,
            LearningType.CONTENT_STRATEGY_ADAPTATION: AdaptationStrategy.BEHAVIOR_MODIFICATION,
            LearningType.SYSTEM_RESOURCE_OPTIMIZATION: AdaptationStrategy.RESOURCE_REALLOCATION
        }
        
        return strategy_mapping.get(pattern.learning_type, AdaptationStrategy.AUTOMATIC_TUNING)
    
    async def _apply_adaptation(self, opportunity: Dict[str, Any]):
        """Adaptasyon uygula"""
        pattern = opportunity["pattern"]
        strategy = opportunity["strategy"]
        
        try:
            # Önceki durumu kaydet
            before_state = await self._capture_system_state()
            
            # Adaptasyonu uygula
            success = await self._execute_adaptation(pattern, strategy)
            
            # Sonraki durumu kaydet
            after_state = await self._capture_system_state()
            
            # İyileşme skorunu hesapla
            improvement_score = await self._calculate_improvement(before_state, after_state)
            
            # Adaptasyon kaydı oluştur
            adaptation = AdaptationRecord(
                adaptation_id=f"adapt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.adaptation_history)}",
                strategy=strategy,
                trigger_event=pattern.pattern_id,
                before_state=before_state,
                after_state=after_state,
                improvement_score=improvement_score,
                timestamp=datetime.now(),
                success=success
            )
            
            self.adaptation_history.append(adaptation)
            
            # Pattern'i güncelle
            pattern.last_applied = datetime.now()
            
            # Learning state'i güncelle
            if success:
                self.learning_state["successful_adaptations"] += 1
            else:
                self.learning_state["failed_adaptations"] += 1
            
            self.logger.info(f"🎯 Applied adaptation: {strategy.value} for {pattern.pattern_id} (Success: {success}, Improvement: {improvement_score:.3f})")
            
        except Exception as e:
            self.logger.error(f"Failed to apply adaptation for {pattern.pattern_id}: {e}")
            self.learning_state["failed_adaptations"] += 1
    
    async def _capture_system_state(self) -> Dict[str, Any]:
        """Mevcut sistem durumunu yakala"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "performance_metrics": {}
        }
        
        # Performans metriklerini ekle
        for metric, values in self.performance_metrics.items():
            if values:
                state["performance_metrics"][metric] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "trend": "up" if len(values) > 1 and values[-1] > values[-2] else "down"
                }
        
        return state
    
    async def _execute_adaptation(self, pattern: LearningPattern, strategy: AdaptationStrategy) -> bool:
        """Adaptasyonu çalıştır"""
        try:
            if strategy == AdaptationStrategy.AUTOMATIC_TUNING:
                return await self._execute_automatic_tuning(pattern)
            elif strategy == AdaptationStrategy.RESOURCE_REALLOCATION:
                return await self._execute_resource_reallocation(pattern)
            elif strategy == AdaptationStrategy.PARAMETER_ADJUSTMENT:
                return await self._execute_parameter_adjustment(pattern)
            elif strategy == AdaptationStrategy.WORKFLOW_OPTIMIZATION:
                return await self._execute_workflow_optimization(pattern)
            else:
                return True  # Default success
                
        except Exception as e:
            self.logger.error(f"Adaptation execution failed: {e}")
            return False
    
    async def _execute_automatic_tuning(self, pattern: LearningPattern) -> bool:
        """Otomatik tuning uygula"""
        # Örnek: CPU kullanımı yüksekse process'leri optimize et
        if "cpu" in pattern.context.get("metric", ""):
            import gc
            gc.collect()  # Garbage collection
            return True
        
        return False
    
    async def _execute_resource_reallocation(self, pattern: LearningPattern) -> bool:
        """Kaynak yeniden tahsis"""
        # Örnek: Memory cleanup
        if "memory" in pattern.context.get("resource", ""):
            import gc
            gc.collect()
            return True
        
        return False
    
    async def _execute_parameter_adjustment(self, pattern: LearningPattern) -> bool:
        """Parametre ayarı"""
        # Örnek: Timeout değerlerini ayarla
        if "timeout" in pattern.context.get("error_type", ""):
            # Timeout'ları artır
            return True
        
        return False
    
    async def _execute_workflow_optimization(self, pattern: LearningPattern) -> bool:
        """Workflow optimizasyonu"""
        # Örnek: Video production workflow'unu optimize et
        if "video_production" in pattern.context.get("process", ""):
            # Production pipeline'ı optimize et
            return True
        
        return False
    
    async def _calculate_improvement(self, before_state: Dict[str, Any], after_state: Dict[str, Any]) -> float:
        """İyileşme skorunu hesapla"""
        try:
            before_metrics = before_state.get("performance_metrics", {})
            after_metrics = after_state.get("performance_metrics", {})
            
            improvements = []
            
            for metric_name in before_metrics:
                if metric_name in after_metrics:
                    before_val = before_metrics[metric_name].get("average", 0)
                    after_val = after_metrics[metric_name].get("average", 0)
                    
                    # CPU/Memory için düşük daha iyi, response time için düşük daha iyi
                    if "cpu" in metric_name or "memory" in metric_name or "time" in metric_name:
                        improvement = (before_val - after_val) / before_val if before_val > 0 else 0
                    else:
                        improvement = (after_val - before_val) / before_val if before_val > 0 else 0
                    
                    improvements.append(improvement)
            
            # Ortalama iyileşme
            return sum(improvements) / len(improvements) if improvements else 0.0
            
        except Exception:
            return 0.0
    
    async def _evaluate_adaptations(self):
        """Adaptasyonları değerlendir"""
        # Son 24 saatki adaptasyonları değerlendir
        recent_adaptations = [a for a in self.adaptation_history 
                            if a.timestamp > datetime.now() - timedelta(hours=24)]
        
        if recent_adaptations:
            successful = len([a for a in recent_adaptations if a.success])
            total = len(recent_adaptations)
            success_rate = successful / total
            
            avg_improvement = sum(a.improvement_score for a in recent_adaptations) / total
            
            # Learning state'i güncelle
            self.learning_state["average_improvement"] = avg_improvement
            self.learning_state["learning_velocity"] = success_rate
    
    async def _update_learning_state(self):
        """Learning state'i güncelle"""
        total = self.learning_state["successful_adaptations"] + self.learning_state["failed_adaptations"]
        if total > 0:
            success_rate = self.learning_state["successful_adaptations"] / total
            self.learning_state["success_rate"] = success_rate
    
    async def get_learning_dashboard(self) -> Dict[str, Any]:
        """Learning dashboard verilerini getir"""
        return {
            "learning_state": self.learning_state,
            "active_patterns": len(self.learning_patterns),
            "total_adaptations": len(self.adaptation_history),
            "performance_metrics": self.performance_metrics,
            "top_patterns": sorted(
                self.learning_patterns.values(),
                key=lambda p: p.impact_score * p.confidence_score,
                reverse=True
            )[:5],
            "recent_adaptations": self.adaptation_history[-10:],
            "learning_velocity": self.learning_state.get("learning_velocity", 0.0)
        }
    
    async def save_learning_state(self):
        """Learning durumunu kaydet"""
        try:
            state_data = {
                "learning_patterns": self.learning_patterns,
                "adaptation_history": self.adaptation_history,
                "performance_metrics": self.performance_metrics,
                "learning_state": self.learning_state
            }
            
            os.makedirs("vuc_memory", exist_ok=True)
            with open("vuc_memory/adaptive_learning_state.pkl", "wb") as f:
                pickle.dump(state_data, f)
                
            self.logger.info("💾 Learning state saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save learning state: {e}")
    
    async def load_learning_state(self):
        """Learning durumunu yükle"""
        try:
            file_path = "vuc_memory/adaptive_learning_state.pkl"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    state_data = pickle.load(f)
                
                self.learning_patterns = state_data.get("learning_patterns", {})
                self.adaptation_history = state_data.get("adaptation_history", [])
                self.performance_metrics = state_data.get("performance_metrics", {})
                self.learning_state = state_data.get("learning_state", {})
                
                self.logger.info("📂 Learning state loaded successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to load learning state: {e}")

# Global instance
adaptive_learning_engine = AdaptiveLearningEngine()
