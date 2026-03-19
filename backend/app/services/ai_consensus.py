"""
VUC-2026 AI Consensus System
AI Agent'ları arasındaki consensus mekanizması

Bu sistem, SEO_Agent ve Creative_Agent çıktılarını karşılaştırır,
consensus skorunu hesaplar ve gerekirse otomatik revizyon tetikler.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json

from app.services.scoring_engine import scoring_engine

logger = logging.getLogger(__name__)

class AIConsensusSystem:
    """AI Consensus Sistemi"""
    
    def __init__(self):
        self.consensus_history = []
        self.agent_configs = {
            "seo_agent": {
                "focus": ["keyword_optimization", "seo_compliance", "ranking_potential"],
                "weight": 0.6,
                "threshold": 75
            },
            "creative_agent": {
                "focus": ["engagement", "creativity", "viral_potential"],
                "weight": 0.4,
                "threshold": 70
            }
        }
        self.revision_triggers = {
            "score_difference": 15,
            "low_consensus": 75,
            "high_risk_count": 3,
            "spam_indicators": True
        }
    
    async def run_consensus_analysis(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI consensus analizini çalıştır
        
        Args:
            content_data: Analiz edilecek içerik verileri
            
        Returns:
            Consensus analizi sonuçları
        """
        
        try:
            # İki agent'ı paralel çalıştır
            seo_task = self._run_seo_agent(content_data)
            creative_task = self._run_creative_agent(content_data)
            
            # Sonuçları bekle
            seo_result, creative_result = await asyncio.gather(seo_task, creative_task)
            
            # Consensus hesapla
            consensus_data = self._calculate_consensus(seo_result, creative_result, content_data)
            
            # Revizyon kararını al
            revision_decision = self._make_revision_decision(consensus_data)
            
            # Sonucu kaydet
            consensus_record = {
                "content_id": content_data.get("id"),
                "timestamp": datetime.now().isoformat(),
                "seo_agent_score": seo_result["score"],
                "creative_agent_score": creative_result["score"],
                "consensus_score": consensus_data["consensus_score"],
                "score_difference": consensus_data["score_difference"],
                "needs_revision": revision_decision["needs_revision"],
                "revision_reason": revision_decision["reason"],
                "agent_disagreements": consensus_data["disagreements"],
                "recommendations": consensus_data["recommendations"]
            }
            
            self.consensus_history.append(consensus_record)
            
            return {
                "success": True,
                "consensus_data": consensus_data,
                "revision_decision": revision_decision,
                "agent_results": {
                    "seo_agent": seo_result,
                    "creative_agent": creative_result
                },
                "record": consensus_record
            }
            
        except Exception as e:
            logger.error(f"Consensus analizi hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _run_seo_agent(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """SEO Agent'ını çalıştır"""
        try:
            # SEO odaklı analiz
            seo_data = content_data.get("seo", {})
            script_data = content_data.get("script", {})
            
            score = 0
            analysis = {}
            
            # Anahtar kelime optimizasyonu (40 puan)
            if seo_data.get("has_primary_keyword", False):
                score += 20
            if seo_data.get("description_has_keywords", False):
                score += 20
            
            # SEO uyumluluğu (30 puan)
            title_length = len(seo_data.get("title", ""))
            if 30 <= title_length <= 60:
                score += 15
            if 5 <= len(seo_data.get("tags", [])) <= 15:
                score += 15
            
            # Senaryo SEO'si (20 puan)
            keyword_density = script_data.get("keyword_density", 0)
            if 1.0 <= keyword_density <= 3.0:
                score += 20
            
            # Meta veri optimizasyonu (10 puan)
            if seo_data.get("thumbnail_optimized", False):
                score += 10
            
            analysis = {
                "keyword_optimization": seo_data.get("has_primary_keyword", False),
                "title_optimization": 30 <= title_length <= 60,
                "description_optimization": seo_data.get("description_has_keywords", False),
                "tag_optimization": 5 <= len(seo_data.get("tags", [])) <= 15,
                "keyword_density": keyword_density,
                "meta_optimization": seo_data.get("thumbnail_optimized", False)
            }
            
            return {
                "agent": "seo_agent",
                "score": min(score, 100),
                "analysis": analysis,
                "recommendations": self._get_seo_recommendations(analysis),
                "confidence": 0.85
            }
            
        except Exception as e:
            logger.error(f"SEO Agent hatası: {e}")
            return {
                "agent": "seo_agent",
                "score": 0,
                "analysis": {"error": str(e)},
                "recommendations": ["Hata: SEO analizi yapılamadı"],
                "confidence": 0
            }
    
    async def _run_creative_agent(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creative Agent'ını çalıştır"""
        try:
            # Yaratıcılık odaklı analiz
            script_data = content_data.get("script", {})
            audio_data = content_data.get("audio", {})
            video_data = content_data.get("video", {})
            
            score = 0
            analysis = {}
            
            # Etkileşim potansiyeli (35 puan)
            hooks = script_data.get("engagement_hooks", [])
            if len(hooks) >= 3:
                score += 20
            elif len(hooks) >= 1:
                score += len(hooks) * 7
            
            # Duygusal ifade (25 puan)
            emotional_range = audio_data.get("emotional_range", 0)
            if emotional_range >= 80:
                score += 25
            elif emotional_range >= 60:
                score += emotional_range * 0.42
            
            # Görsel yaratıcılık (20 puan)
            hormozi_elements = video_data.get("hormozi_elements", {})
            if hormozi_elements.get("colorful_text", False):
                score += 10
            if hormozi_elements.get("dynamic_captions", False):
                score += 10
            
            # İnovatif unsurlar (15 puan)
            if video_data.get("shadowban_shield_applied", False):
                score += 15
            
            # Viral potansiyeli (5 puan)
            if script_data.get("viral_hooks", 0) >= 2:
                score += 5
            
            analysis = {
                "engagement_potential": len(hooks),
                "emotional_impact": emotional_range,
                "visual_creativity": {
                    "colorful_text": hormozi_elements.get("colorful_text", False),
                    "dynamic_captions": hormozi_elements.get("dynamic_captions", False)
                },
                "innovation_score": video_data.get("shadowban_shield_applied", False),
                "viral_potential": script_data.get("viral_hooks", 0)
            }
            
            return {
                "agent": "creative_agent",
                "score": min(score, 100),
                "analysis": analysis,
                "recommendations": self._get_creative_recommendations(analysis),
                "confidence": 0.75
            }
            
        except Exception as e:
            logger.error(f"Creative Agent hatası: {e}")
            return {
                "agent": "creative_agent",
                "score": 0,
                "analysis": {"error": str(e)},
                "recommendations": ["Hata: Yaratıcılık analizi yapılamadı"],
                "confidence": 0
            }
    
    def _calculate_consensus(self, seo_result: Dict[str, Any], 
                           creative_result: Dict[str, Any], 
                           content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Consensus skorunu hesapla"""
        
        seo_score = seo_result["score"]
        creative_score = creative_result["score"]
        
        # Ağırlıklı consensus skorunu hesapla
        consensus_score = (
            seo_score * self.agent_configs["seo_agent"]["weight"] +
            creative_score * self.agent_configs["creative_agent"]["weight"]
        )
        
        # Uyuşmazlığı belirle
        score_difference = abs(seo_score - creative_score)
        
        # Anlaşmazlık noktalarını belirle
        disagreements = self._identify_disagreements(
            seo_result["analysis"], 
            creative_result["analysis"]
        )
        
        # Önerileri oluştur
        recommendations = self._generate_consensus_recommendations(
            consensus_score, score_difference, disagreements
        )
        
        return {
            "consensus_score": round(consensus_score, 1),
            "score_difference": round(score_difference, 1),
            "agreement_level": self._get_agreement_level(score_difference),
            "disagreements": disagreements,
            "recommendations": recommendations,
            "needs_human_review": self._should_require_human_review(
                consensus_score, score_difference, disagreements
            )
        }
    
    def _identify_disagreements(self, seo_analysis: Dict[str, Any], 
                              creative_analysis: Dict[str, Any]) -> List[str]:
        """Agent'lar arasındaki anlaşmazlıkları belirle"""
        disagreements = []
        
        # Anahtar kelime stratejisi
        if seo_analysis.get("keyword_optimization") != creative_analysis.get("engagement_potential", 0) >= 3:
            disagreements.append("Anahtar kelime vs Etkileşim odaklılık")
        
        # Görsel yaklaşım
        if seo_analysis.get("title_optimization") and not creative_analysis.get("visual_creativity", {}).get("colorful_text"):
            disagreements.append("SEO optimizasyonu vs Yaratıcılık")
        
        # Risk toleransı
        if not creative_analysis.get("innovation_score"):
            disagreements.append("Güvenli yaklaşım vs İnovatif yaklaşım")
        
        return disagreements
    
    def _get_agreement_level(self, score_difference: float) -> str:
        """Anlaşma seviyesini belirle"""
        if score_difference <= 5:
            return "Yüksek Anlaşma"
        elif score_difference <= 10:
            return "Orta Anlaşma"
        elif score_difference <= 20:
            return "Düşük Anlaşma"
        else:
            return "Anlaşmazlık"
    
    def _generate_consensus_recommendations(self, consensus_score: float, 
                                       score_difference: float, 
                                       disagreements: List[str]) -> List[str]:
        """Consensus önerileri oluştur"""
        recommendations = []
        
        if consensus_score < self.revision_triggers["low_consensus"]:
            recommendations.append("Düşük consensus - Agent'lar yeniden çalıştırılmalı")
        
        if score_difference > self.revision_triggers["score_difference"]:
            recommendations.append(f"Yüksek uyuşmazlık ({score_difference} puan) - İnsan müdahalesi önerilir")
        
        if len(disagreements) > 2:
            recommendations.append("Çok sayıda anlaşmazlık - Stratejik yaklaşım gözden geçirilmeli")
        
        if consensus_score >= 85:
            recommendations.append("Yüksek consensus - İçerik yayın için hazır")
        
        return recommendations
    
    def _should_require_human_review(self, consensus_score: float, 
                                  score_difference: float, 
                                  disagreements: List[str]) -> bool:
        """İnsan incelemesi gerekip gerekmediğini belirle"""
        return (
            consensus_score < 75 or
            score_difference > 20 or
            len(disagreements) > 3
        )
    
    def _make_revision_decision(self, consensus_data: Dict[str, Any]) -> Dict[str, Any]:
        """Revizyon kararı al"""
        needs_revision = (
            consensus_data["consensus_score"] < self.revision_triggers["low_consensus"] or
            consensus_data["score_difference"] > self.revision_triggers["score_difference"] or
            consensus_data["needs_human_review"]
        )
        
        if needs_revision:
            return {
                "needs_revision": True,
                "reason": self._get_revision_reason(consensus_data),
                "auto_revision_possible": consensus_data["consensus_score"] > 60,
                "recommended_actions": self._get_revision_actions(consensus_data)
            }
        else:
            return {
                "needs_revision": False,
                "reason": "Yüksek consensus - Revizyon gerekmez",
                "auto_revision_possible": False,
                "recommended_actions": ["İçeriği yayına hazırla"]
            }
    
    def _get_revision_reason(self, consensus_data: Dict[str, Any]) -> str:
        """Revizyon sebebini belirle"""
        if consensus_data["consensus_score"] < 50:
            return "Çok düşük consensus - Tam yeniden üretim"
        elif consensus_data["score_difference"] > 30:
            return "Yüksek uyuşmazlık - Strateji yeniden değerlendirme"
        elif len(consensus_data["disagreements"]) > 4:
            return "Temel anlaşmazlık - İnsan müdahalesi zorunlu"
        else:
            return "Orta seviye sorunlar - Otomatik revizyon mümkün"
    
    def _get_revision_actions(self, consensus_data: Dict[str, Any]) -> List[str]:
        """Revizyon eylemlerini belirle"""
        actions = []
        
        if consensus_data["consensus_score"] < 60:
            actions.extend([
                "İçeriği tamamen yeniden üret",
                "Farklı AI modellerini kullan",
                "Strateji yaklaşımını değiştir"
            ])
        else:
            actions.extend([
                "Anahtar kelime yoğunluğunu ayarla",
                "Etkileşim kancalarını güçlendir",
                "Görsel unsurları ekle"
            ])
        
        return actions
    
    def _get_seo_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """SEO Agent önerileri"""
        recommendations = []
        
        if not analysis.get("keyword_optimization"):
            recommendations.append("Anahtar kelime optimizasyonunu güçlendir")
        
        if not analysis.get("title_optimization"):
            recommendations.append("Başlık uzunluğunu 30-60 karakter arasına getir")
        
        if not analysis.get("meta_optimization"):
            recommendations.append("Thumbnail ve meta verileri optimize et")
        
        return recommendations
    
    def _get_creative_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Creative Agent önerileri"""
        recommendations = []
        
        if analysis.get("engagement_potential", 0) < 3:
            recommendations.append("Daha fazla etkileşim kancası ekle")
        
        if not analysis.get("visual_creativity", {}).get("colorful_text"):
            recommendations.append("Hormozi stili dinamik altyazılar ekle")
        
        if not analysis.get("innovation_score"):
            recommendations.append("Shadowban shield ve inovatif unsurlar ekle")
        
        return recommendations
    
    def get_consensus_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Consensus geçmişini al"""
        return self.consensus_history[-limit:] if self.consensus_history else []
    
    def get_consensus_stats(self) -> Dict[str, Any]:
        """Consensus istatistiklerini al"""
        if not self.consensus_history:
            return {}
        
        total_analyses = len(self.consensus_history)
        revisions_needed = len([r for r in self.consensus_history if r.get("needs_revision", False)])
        
        avg_consensus_score = sum(r.get("consensus_score", 0) for r in self.consensus_history) / total_analyses
        avg_score_difference = sum(r.get("score_difference", 0) for r in self.consensus_history) / total_analyses
        
        return {
            "total_analyses": total_analyses,
            "revisions_needed": revisions_needed,
            "revision_rate": round((revisions_needed / total_analyses) * 100, 1),
            "average_consensus_score": round(avg_consensus_score, 1),
            "average_score_difference": round(avg_score_difference, 1),
            "most_common_disagreements": self._get_most_common_disagreements(),
            "trend": self._get_consensus_trend()
        }
    
    def _get_most_common_disagreements(self) -> List[str]:
        """En sık anlaşmazlık türlerini al"""
        all_disagreements = []
        for record in self.consensus_history:
            all_disagreements.extend(record.get("agent_disagreements", []))
        
        from collections import Counter
        disagreement_counts = Counter(all_disagreements)
        return [disagreement for disagreement, count in disagreement_counts.most_common(3)]
    
    def _get_consensus_trend(self) -> str:
        """Consensus trendini belirle"""
        if len(self.consensus_history) < 5:
            return "Yetersiz veri"
        
        recent_scores = [r.get("consensus_score", 0) for r in self.consensus_history[-5:]]
        if all(score >= 80 for score in recent_scores):
            return "İyileşiyor"
        elif all(score >= 60 for score in recent_scores):
            return "Stabil"
        else:
            return "Düşüyor"

# Global instance
ai_consensus = AIConsensusSystem()
