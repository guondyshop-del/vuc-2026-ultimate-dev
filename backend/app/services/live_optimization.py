"""
VUC-2026 Live Optimization System
Yayındaki videoları gerçek zamanlı optimize eder

Bu sistem, yayındaki videonun performansını izler,
düşük performans durumunda otomatik optimizasyon önerileri sunar
ve kullanıcı onayı ile anında güncelleme yapar.
"""

import logging
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

class LiveOptimizationSystem:
    """Canlı Optimizasyon Sistemi"""
    
    def __init__(self):
        self.active_optimizations = {}
        self.optimization_history = []
        self.performance_thresholds = {
            "ctr_min": 2.0,          # Minimum CTR %
            "retention_min": 30.0,    # Minimum izlenme süresi %
            "engagement_min": 5.0,    # Minimum etkileşim oranı %
            "views_per_hour_min": 100   # Minimum saat başına izlenme
        }
        self.optimization_strategies = {
            "title_optimization": {
                "priority": "high",
                "impact": "ctr",
                "test_variants": 3
            },
            "thumbnail_a_b": {
                "priority": "high", 
                "impact": "ctr",
                "test_variants": 2
            },
            "description_optimization": {
                "priority": "medium",
                "impact": "retention",
                "test_variants": 2
            },
            "tags_optimization": {
                "priority": "low",
                "impact": "discovery",
                "test_variants": 5
            }
        }
    
    async def start_monitoring(self, video_id: str, initial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Video izlemeyi başlat
        
        Args:
            video_id: Video ID'si
            initial_metrics: Başlangıç metrikleri
            
        Returns:
            İzleme başlatma sonuçları
        """
        
        try:
            monitoring_session = {
                "video_id": video_id,
                "started_at": datetime.now().isoformat(),
                "initial_metrics": initial_metrics,
                "current_metrics": initial_metrics.copy(),
                "optimizations_applied": [],
                "alerts_triggered": [],
                "status": "monitoring"
            }
            
            self.active_optimizations[video_id] = monitoring_session
            
            logger.info(f"{video_id} için canlı izleme başlatıldı")
            
            return {
                "success": True,
                "session_id": f"session_{video_id}_{int(time.time())}",
                "monitoring": monitoring_session,
                "thresholds": self.performance_thresholds
            }
            
        except Exception as e:
            logger.error(f"İzleme başlatma hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_id": video_id
            }
    
    async def analyze_performance(self, video_id: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Video performansını analiz et
        
        Args:
            video_id: Video ID'si
            current_metrics: Güncel metrikler
            
        Returns:
            Performans analizi sonuçları
        """
        
        if video_id not in self.active_optimizations:
            return {
                "success": False,
                "error": "Video izlenmiyor",
                "video_id": video_id
            }
        
        try:
            session = self.active_optimizations[video_id]
            session["current_metrics"] = current_metrics
            
            # Performans düşüşlerini analiz et
            performance_analysis = self._analyze_performance_trends(
                session["initial_metrics"], 
                current_metrics
            )
            
            # Optimizasyon ihtiyaçlarını belirle
            optimization_needs = self._identify_optimization_needs(
                performance_analysis, 
                current_metrics
            )
            
            # Alert'leri kontrol et
            alerts = self._check_performance_alerts(
                performance_analysis, 
                optimization_needs
            )
            
            session["performance_analysis"] = performance_analysis
            session["optimization_needs"] = optimization_needs
            session["alerts_triggered"] = alerts
            
            return {
                "success": True,
                "video_id": video_id,
                "performance_analysis": performance_analysis,
                "optimization_needs": optimization_needs,
                "alerts": alerts,
                "session_status": session["status"]
            }
            
        except Exception as e:
            logger.error(f"Performans analizi hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_id": video_id
            }
    
    async def suggest_optimization(self, video_id: str, optimization_type: str, 
                                user_approval: bool = False) -> Dict[str, Any]:
        """
        Optimizasyon önerisi sun
        
        Args:
            video_id: Video ID'si
            optimization_type: Optimizasyon türü
            user_approval: Kullanıcı onayı gerekli mi
            
        Returns:
            Optimizasyon önerisi
        """
        
        if video_id not in self.active_optimizations:
            return {
                "success": False,
                "error": "Video izlenmiyor",
                "video_id": video_id
            }
        
        try:
            session = self.active_optimizations[video_id]
            current_metrics = session["current_metrics"]
            
            # Optimizasyon stratejisi oluştur
            optimization_strategy = self.optimization_strategies.get(optimization_type)
            
            if not optimization_strategy:
                return {
                    "success": False,
                    "error": f"Bilinmeyen optimizasyon türü: {optimization_type}",
                    "video_id": video_id
                }
            
            # Optimizasyon varyasyonları oluştur
            variants = await self._generate_optimization_variants(
                optimization_type, 
                current_metrics, 
                optimization_strategy["test_variants"]
            )
            
            # Öneri oluştur
            suggestion = {
                "video_id": video_id,
                "optimization_type": optimization_type,
                "priority": optimization_strategy["priority"],
                "expected_impact": optimization_strategy["impact"],
                "variants": variants,
                "recommended_variant": variants[0] if variants else None,
                "requires_approval": user_approval,
                "implementation_time": datetime.now().isoformat(),
                "estimated_improvement": self._estimate_improvement(
                    optimization_type, 
                    current_metrics, 
                    variants[0] if variants else None
                ),
                "confidence": self._calculate_optimization_confidence(
                    optimization_type, 
                    current_metrics
                )
            }
            
            return {
                "success": True,
                "suggestion": suggestion,
                "video_id": video_id
            }
            
        except Exception as e:
            logger.error(f"Optimizasyon önerisi hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_id": video_id
            }
    
    async def apply_optimization(self, video_id: str, variant_id: str, 
                              user_approved: bool = True) -> Dict[str, Any]:
        """
        Optimizasyon uygula
        
        Args:
            video_id: Video ID'si
            variant_id: Varyant ID'si
            user_approved: Kullanıcı onayı
            
        Returns:
            Optimizasyon uygulama sonuçları
        """
        
        if video_id not in self.active_optimizations:
            return {
                "success": False,
                "error": "Video izlenmiyor",
                "video_id": video_id
            }
        
        try:
            session = self.active_optimizations[video_id]
            
            # Optimizasyon kaydı oluştur
            optimization_record = {
                "video_id": video_id,
                "variant_id": variant_id,
                "applied_at": datetime.now().isoformat(),
                "user_approved": user_approved,
                "previous_metrics": session["current_metrics"].copy(),
                "optimization_type": self._identify_optimization_type(variant_id),
                "status": "applied"
            }
            
            # Session'ı güncelle
            session["optimizations_applied"].append(optimization_record)
            
            # Optimizasyon geçmişine ekle
            self.optimization_history.append(optimization_record)
            
            logger.info(f"{video_id} için optimizasyon uygulandı: {variant_id}")
            
            return {
                "success": True,
                "optimization_applied": optimization_record,
                "video_id": video_id,
                "session_status": session["status"]
            }
            
        except Exception as e:
            logger.error(f"Optimizasyon uygulama hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_id": video_id
            }
    
    def _analyze_performance_trends(self, initial_metrics: Dict[str, Any], 
                                current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Performans trendlerini analiz et"""
        
        try:
            # Metrik değişimlerini hesapla
            trends = {}
            
            for metric_name, initial_value in initial_metrics.items():
                if metric_name in current_metrics:
                    current_value = current_metrics[metric_name]
                    
                    if isinstance(initial_value, (int, float)) and isinstance(current_value, (int, float)):
                        change = current_value - initial_value
                        percent_change = (change / initial_value * 100) if initial_value != 0 else 0
                        
                        trends[metric_name] = {
                            "initial_value": initial_value,
                            "current_value": current_value,
                            "absolute_change": change,
                            "percent_change": round(percent_change, 2),
                            "trend": self._determine_trend(change, percent_change),
                            "concern_level": self._assess_concern_level(
                                metric_name, change, percent_change
                            )
                        }
            
            return {
                "trends": trends,
                "overall_performance": self._calculate_overall_performance(trends),
                "key_insights": self._extract_key_insights(trends),
                "analysis_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Performans trend analizi hatası: {e}")
            return {"trends": {}, "error": str(e)}
    
    def _identify_optimization_needs(self, performance_analysis: Dict[str, Any], 
                                   current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimizasyon ihtiyaçlarını belirle"""
        
        needs = []
        trends = performance_analysis.get("trends", {})
        
        # CTR analizi
        if "ctr" in trends:
            ctr_trend = trends["ctr"]
            if ctr_trend["trend"] == "declining" or ctr_trend["percent_change"] < -20:
                needs.append({
                    "type": "title_optimization",
                    "urgency": "high",
                    "reason": f"CTR %{ctr_trend['percent_change']}% düştü",
                    "expected_impact": "click_through_rate",
                    "confidence": 0.85
                })
        
        # İzlenme süresi analizi
        if "retention" in trends:
            retention_trend = trends["retention"]
            if retention_trend["trend"] == "declining" or retention_trend["percent_change"] < -15:
                needs.append({
                    "type": "description_optimization",
                    "urgency": "medium",
                    "reason": f"İzlenme süresi %{retention_trend['percent_change']}% düştü",
                    "expected_impact": "watch_time",
                    "confidence": 0.75
                })
        
        # Etkileşim analizi
        if "engagement" in trends:
            engagement_trend = trends["engagement"]
            if engagement_trend["trend"] == "declining" or engagement_trend["percent_change"] < -25:
                needs.append({
                    "type": "thumbnail_a_b",
                    "urgency": "high",
                    "reason": f"Etkileşim %{engagement_trend['percent_change']}% düştü",
                    "expected_impact": "engagement_rate",
                    "confidence": 0.80
                })
        
        # Keşif analizi
        views_per_hour = current_metrics.get("views_per_hour", 0)
        if views_per_hour < self.performance_thresholds["views_per_hour_min"]:
            needs.append({
                "type": "tags_optimization",
                "urgency": "low",
                "reason": f"Düşük keşif oranı: {views_per_hour}/saat",
                "expected_impact": "discovery",
                "confidence": 0.70
            })
        
        return sorted(needs, key=lambda x: (x["urgency"] == "high" and 0 or x["urgency"] == "medium" and 1 or 2))
    
    def _check_performance_alerts(self, performance_analysis: Dict[str, Any], 
                               optimization_needs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Performans alert'lerini kontrol et"""
        
        alerts = []
        trends = performance_analysis.get("trends", {})
        
        # Kritik alert'ler
        high_urgency_needs = [need for need in optimization_needs if need["urgency"] == "high"]
        
        if high_urgency_needs:
            alerts.append({
                "level": "critical",
                "title": "Yüksek Öncelikli Optimizasyon Gerekli",
                "message": f"{len(high_urgency_needs)} kritik optimizasyon ihtiyacı var",
                "needs_immediate_attention": True,
                "recommended_actions": [need["type"] for need in high_urgency_needs],
                "timestamp": datetime.now().isoformat()
            })
        
        # Trend uyarıları
        declining_metrics = [trend for trend in trends.values() if trend.get("trend") == "declining"]
        
        if len(declining_metrics) >= 2:
            alerts.append({
                "level": "warning",
                "title": "Birden Fazla Metrik Düşüyor",
                "message": f"{len(declining_metrics)} metrik düşüş trendinde",
                "needs_immediate_attention": False,
                "affected_metrics": [metric for metric in trends.keys() if trends[metric]["trend"] == "declining"],
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    async def _generate_optimization_variants(self, optimization_type: str, 
                                           current_metrics: Dict[str, Any], 
                                           variant_count: int) -> List[Dict[str, Any]]:
        """Optimizasyon varyasyonları oluştur"""
        
        variants = []
        
        if optimization_type == "title_optimization":
            # Başlık varyasyonları
            current_title = current_metrics.get("title", "")
            base_keywords = self._extract_keywords(current_title)
            
            for i in range(variant_count):
                if i == 0:
                    # Mevcut başlık (kontrol)
                    variant = {
                        "id": f"control_{i}",
                        "title": current_title,
                        "type": "control",
                        "expected_ctr": current_metrics.get("ctr", 2.0)
                    }
                elif i == 1:
                    # Soru formatı
                    variant = {
                        "id": f"question_{i}",
                        "title": f"{base_keywords[0]} nasıl yapılır?",
                        "type": "question",
                        "expected_ctr": current_metrics.get("ctr", 2.0) * 1.3
                    }
                elif i == 2:
                    # Şaşırtıcı format
                    variant = {
                        "id": f"shocking_{i}",
                        "title": f"ASIL BİLİNMENEN {base_keywords[0]} SIRRI!",
                        "type": "shocking",
                        "expected_ctr": current_metrics.get("ctr", 2.0) * 1.5
                    }
                
                variants.append(variant)
        
        elif optimization_type == "thumbnail_a_b":
            # Thumbnail A/B test varyasyonları
            for i in range(variant_count):
                if i == 0:
                    variant = {
                        "id": f"thumbnail_a_{i}",
                        "type": "professional",
                        "description": "Profesyonel thumbnail",
                        "expected_ctr": current_metrics.get("ctr", 2.0)
                    }
                elif i == 1:
                    variant = {
                        "id": f"thumbnail_b_{i}",
                        "type": "emotional",
                        "description": "Duygusal thumbnail",
                        "expected_ctr": current_metrics.get("ctr", 2.0) * 1.4
                    }
                
                variants.append(variant)
        
        elif optimization_type == "description_optimization":
            # Açıklama varyasyonları
            current_description = current_metrics.get("description", "")
            
            for i in range(variant_count):
                if i == 0:
                    variant = {
                        "id": f"desc_a_{i}",
                        "description": current_description,
                        "type": "control",
                        "expected_retention": current_metrics.get("retention", 30.0)
                    }
                elif i == 1:
                    # Daha kısa ve etkili açıklama
                    shortened_desc = current_description[:len(current_description)//2] + "\n\n🔥 Abone olmayı unutmayın!"
                    variant = {
                        "id": f"desc_b_{i}",
                        "description": shortened_desc,
                        "type": "optimized",
                        "expected_retention": current_metrics.get("retention", 30.0) * 1.2
                    }
                
                variants.append(variant)
        
        return variants
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Metinden anahtar kelimeleri çıkar"""
        import re
        # Basit anahtar kelime çıkarma
        words = re.findall(r'\b\w+\b', text.lower())
        # En sık geçen 3 kelimeyi al
        from collections import Counter
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(3)]
    
    def _determine_trend(self, change: float, percent_change: float) -> str:
        """Trend yönünü belirle"""
        if percent_change < -10:
            return "declining"
        elif percent_change < -2:
            return "slightly_declining"
        elif percent_change < 2:
            return "stable"
        elif percent_change < 10:
            return "improving"
        else:
            return "rapidly_improving"
    
    def _assess_concern_level(self, metric_name: str, change: float, percent_change: float) -> str:
        """Endişe seviyesini belirle"""
        if metric_name in ["ctr", "engagement"]:
            if percent_change < -30:
                return "critical"
            elif percent_change < -15:
                return "high"
            elif percent_change < -5:
                return "medium"
            else:
                return "low"
        elif metric_name in ["retention", "views_per_hour"]:
            if percent_change < -25:
                return "critical"
            elif percent_change < -10:
                return "high"
            elif percent_change < -3:
                return "medium"
            else:
                return "low"
        else:
            return "low"
    
    def _calculate_overall_performance(self, trends: Dict[str, Any]) -> Dict[str, Any]:
        """Genel performansı hesapla"""
        if not trends:
            return {"score": 0, "grade": "F"}
        
        # Trend skorlarını hesapla
        trend_scores = []
        for metric_name, trend_data in trends.items():
            if trend_data["trend"] == "improving":
                trend_scores.append(2)
            elif trend_data["trend"] == "stable":
                trend_scores.append(1)
            elif trend_data["trend"] == "declining":
                trend_scores.append(0)
            else:
                trend_scores.append(1)
        
        overall_score = sum(trend_scores) / len(trend_scores) * 33.3
        
        # Not belirle
        if overall_score >= 80:
            grade = "A (Mükemmel)"
        elif overall_score >= 60:
            grade = "B (İyi)"
        elif overall_score >= 40:
            grade = "C (Orta)"
        elif overall_score >= 20:
            grade = "D (Zayıf)"
        else:
            grade = "F (Kötü)"
        
        return {
            "score": round(overall_score, 1),
            "grade": grade,
            "trend_summary": self._summarize_trends(trends)
        }
    
    def _extract_key_insights(self, trends: Dict[str, Any]) -> List[str]:
        """Anahtar içgörüleri çıkar"""
        insights = []
        
        declining_metrics = [name for name, trend in trends.items() if trend["trend"] == "declining"]
        improving_metrics = [name for name, trend in trends.items() if trend["trend"] == "improving"]
        
        if declining_metrics:
            insights.append(f"{len(declining_metrics)} metrik düşüş trendinde: {', '.join(declining_metrics)}")
        
        if improving_metrics:
            insights.append(f"{len(improving_metrics)} metrik iyileşme trendinde: {', '.join(improving_metrics)}")
        
        # En büyük değişim
        if trends:
            largest_change = max(trends.values(), key=lambda x: abs(x.get("percent_change", 0)))
            insights.append(f"En büyük değişim: {largest_change.get('metric_name', 'bilinmeyen')} %{largest_change.get('percent_change', 0)}%")
        
        return insights
    
    def _summarize_trends(self, trends: Dict[str, Any]) -> str:
        """Trend özeti oluştur"""
        if not trends:
            return "Yetersiz veri"
        
        declining_count = sum(1 for trend in trends.values() if trend["trend"] == "declining")
        improving_count = sum(1 for trend in trends.values() if trend["trend"] == "improving")
        stable_count = sum(1 for trend in trends.values() if trend["trend"] == "stable")
        
        if declining_count > improving_count:
            return "Genel olarak düşüş trendi"
        elif improving_count > declining_count:
            return "Genel olarak iyileşme trendi"
        else:
            return "Genel olarak stabilitrendi"
    
    def _estimate_improvement(self, optimization_type: str, current_metrics: Dict[str, Any], 
                            variant: Dict[str, Any]) -> Dict[str, float]:
        """İyileştirme tahmini yap"""
        
        improvements = {
            "title_optimization": {
                "ctr": 15.0,      # %15 CTR artışı
                "views": 20.0      # %20 izlenme artışı
            },
            "thumbnail_a_b": {
                "ctr": 25.0,      # %25 CTR artışı
                "engagement": 30.0  # %30 etkileşim artışı
            },
            "description_optimization": {
                "retention": 18.0,  # %18 izlenme süresi artışı
                "watch_time": 25.0   # %25 izlenme süresi artışı
            },
            "tags_optimization": {
                "discovery": 10.0,   # %10 keşif artışı
                "suggested_views": 15.0  # %15 önerilen izlenme
            }
        }
        
        return improvements.get(optimization_type, {"ctr": 5.0, "views": 10.0})
    
    def _calculate_optimization_confidence(self, optimization_type: str, 
                                     current_metrics: Dict[str, Any]) -> float:
        """Optimizasyon güven seviyesini hesapla"""
        
        base_confidence = 0.75
        
        # Metrik kalitesine göre güven ayarla
        if current_metrics.get("sample_size", 0) > 1000:
            base_confidence += 0.15
        
        if current_metrics.get("time_published", 0):
            hours_since_publish = (datetime.now() - datetime.fromisoformat(
                current_metrics["time_published"].replace("Z", "+00:00")
            )).total_seconds() / 3600
            
            if hours_since_publish > 24:
                base_confidence += 0.10
        
        return min(base_confidence, 0.95)
    
    def _identify_optimization_type(self, variant_id: str) -> str:
        """Varyant ID'sinden optimizasyon türünü belirle"""
        if "title" in variant_id:
            return "title_optimization"
        elif "thumbnail" in variant_id:
            return "thumbnail_a_b"
        elif "desc" in variant_id:
            return "description_optimization"
        elif "tags" in variant_id:
            return "tags_optimization"
        else:
            return "unknown"
    
    def get_optimization_history(self, video_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Optimizasyon geçmişini al"""
        history = self.optimization_history
        
        if video_id:
            history = [opt for opt in history if opt.get("video_id") == video_id]
        else:
            history = history
        
        return sorted(history, key=lambda x: x.get("applied_at", ""), reverse=True)[:limit]
    
    def get_active_monitoring_sessions(self) -> Dict[str, Any]:
        """Aktif izleme oturumlarını al"""
        return {
            "total_sessions": len(self.active_optimizations),
            "sessions": self.active_optimizations,
            "summary": {
                "total_alerts": sum(len(session.get("alerts_triggered", [])) for session in self.active_optimizations.values()),
                "optimizations_applied": sum(len(session.get("optimizations_applied", [])) for session in self.active_optimizations.values()),
                "average_performance": self._calculate_average_performance()
            }
        }
    
    def _calculate_average_performance(self) -> Dict[str, float]:
        """Ortalama performansı hesapla"""
        if not self.active_optimizations:
            return {}
        
        all_metrics = []
        for session in self.active_optimizations.values():
            current = session.get("current_metrics", {})
            if current:
                all_metrics.append(current)
        
        if not all_metrics:
            return {}
        
        # Ortalama metrikleri
        avg_metrics = {}
        metric_names = set()
        for metrics in all_metrics:
            metric_names.update(metrics.keys())
        
        for metric_name in metric_names:
            values = [m.get(metric_name, 0) for m in all_metrics if metric_name in m]
            if values:
                avg_metrics[metric_name] = sum(values) / len(values)
        
        return avg_metrics

# Global instance
live_optimization = LiveOptimizationSystem()
