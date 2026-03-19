"""
VUC-2026 Scoring Engine
İçerik kalitesi ve güven skorunu hesaplayan motor

Bu motor, üretilen her içerik için 0-100 arası güven skoru hesaplar
ve AI consensus mekanizması çalıştırır.
"""

import logging
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ContentScore:
    """İçerik skor verisi"""
    overall_score: float
    script_score: float
    audio_score: float
    video_score: float
    seo_score: float
    confidence: float
    recommendations: List[str]
    risk_factors: List[str]
    calculated_at: str

class ScoringEngine:
    """İçerik skorlama motoru"""
    
    def __init__(self):
        self.weight_config = {
            "script": 0.35,      # Senaryo ağırlığı
            "audio": 0.25,       # Ses kalitesi ağırlığı
            "video": 0.25,       # Video kalitesi ağırlığı
            "seo": 0.15           # SEO ağırlığı
        }
        
        self.thresholds = {
            "excellent": 90,
            "good": 75,
            "acceptable": 60,
            "needs_improvement": 40
        }
    
    async def calculate_content_score(self, content_data: Dict[str, Any]) -> ContentScore:
        """
        İçerik için kapsamlı skor hesapla
        
        Args:
            content_data: İçerik verileri (script, audio, video, SEO)
            
        Returns:
            Detaylı skor bilgileri
        """
        
        try:
            # Bileşen skorlarını hesapla
            script_score = await self._score_script(content_data.get("script", {}))
            audio_score = await self._score_audio(content_data.get("audio", {}))
            video_score = await self._score_video(content_data.get("video", {}))
            seo_score = await self._score_seo(content_data.get("seo", {}))
            
            # Ağırlıklı genel skor
            overall_score = (
                script_score * self.weight_config["script"] +
                audio_score * self.weight_config["audio"] +
                video_score * self.weight_config["video"] +
                seo_score * self.weight_config["seo"]
            )
            
            # Güven seviyesini belirle
            confidence = self._calculate_confidence(content_data)
            
            # Risk faktörlerini belirle
            risk_factors = self._identify_risk_factors(content_data, overall_score)
            
            # Önerileri oluştur
            recommendations = self._generate_recommendations(
                script_score, audio_score, video_score, seo_score, overall_score
            )
            
            return ContentScore(
                overall_score=round(overall_score, 1),
                script_score=round(script_score, 1),
                audio_score=round(audio_score, 1),
                video_score=round(video_score, 1),
                seo_score=round(seo_score, 1),
                confidence=round(confidence, 1),
                recommendations=recommendations,
                risk_factors=risk_factors,
                calculated_at=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Skor hesaplama hatası: {e}")
            return ContentScore(
                overall_score=0.0,
                script_score=0.0,
                audio_score=0.0,
                video_score=0.0,
                seo_score=0.0,
                confidence=0.0,
                recommendations=["Hata: Skor hesaplanamadı"],
                risk_factors=["Sistem hatası"],
                calculated_at=datetime.now().isoformat()
            )
    
    async def _score_script(self, script_data: Dict[str, Any]) -> float:
        """Senaryo skorunu hesapla"""
        score = 0.0
        
        # Konu tutarlılığı (30 puan)
        if script_data.get("topic_consistency", False):
            score += 30
        
        # Yapısal bütünlük (25 puan)
        structure = script_data.get("structure", {})
        if structure.get("introduction") and structure.get("main_content") and structure.get("conclusion"):
            score += 25
        
        # Anahtar kelime yoğunluğu (20 puan)
        keyword_density = script_data.get("keyword_density", 0)
        if 1.0 <= keyword_density <= 3.0:
            score += 20
        elif keyword_density < 1.0:
            score += keyword_density * 20
        else:
            score += max(0, 20 - (keyword_density - 3.0) * 5)
        
        # Etkileşim kancaları (15 puan)
        hooks = script_data.get("engagement_hooks", [])
        if len(hooks) >= 3:
            score += 15
        elif len(hooks) >= 1:
            score += len(hooks) * 5
        
        # Okunabilirlik (10 puan)
        readability = script_data.get("readability_score", 0)
        if readability >= 80:
            score += 10
        elif readability >= 60:
            score += readability / 8
        
        return min(score, 100)
    
    async def _score_audio(self, audio_data: Dict[str, Any]) -> float:
        """Ses kalitesi skorunu hesapla"""
        score = 0.0
        
        # Ses netliği (25 puan)
        clarity = audio_data.get("clarity_score", 0)
        if clarity >= 90:
            score += 25
        elif clarity >= 75:
            score += clarity * 0.33
        
        # Arka plan gürültüsü (20 puan)
        noise_level = audio_data.get("noise_level", 100)
        if noise_level <= 10:
            score += 20
        elif noise_level <= 30:
            score += 20 - (noise_level - 10) * 0.5
        else:
            score += max(0, 10 - (noise_level - 30) * 0.2)
        
        # Ses seviyesi tutarlılığı (15 puan)
        volume_consistency = audio_data.get("volume_consistency", 0)
        if volume_consistency >= 85:
            score += 15
        elif volume_consistency >= 70:
            score += volume_consistency * 0.21
        
        # Duygusal ifade (20 puan)
        emotional_range = audio_data.get("emotional_range", 0)
        if emotional_range >= 80:
            score += 20
        elif emotional_range >= 60:
            score += emotional_range * 0.33
        
        # SSML optimizasyonu (10 puan)
        ssml_optimized = audio_data.get("ssml_optimized", False)
        if ssml_optimized:
            score += 10
        
        # Sidechain kullanımı (10 puan)
        sidechain_used = audio_data.get("sidechain_used", False)
        if sidechain_used:
            score += 10
        
        return min(score, 100)
    
    async def _score_video(self, video_data: Dict[str, Any]) -> float:
        """Video kalitesi skorunu hesapla"""
        score = 0.0
        
        # Görüntü çözünürlüğü (20 puan)
        resolution = video_data.get("resolution", "")
        if "1920x1080" in resolution or "1080p" in resolution:
            score += 20
        elif "1280x720" in resolution or "720p" in resolution:
            score += 15
        elif "1920x1080" in resolution or "4K" in resolution:
            score += 25
        
        # Frame rate (15 puan)
        fps = video_data.get("fps", 0)
        if fps >= 30:
            score += 15
        elif fps >= 24:
            score += fps * 0.6
        
        # Renk doygunluğu (15 puan)
        color_grading = video_data.get("color_grading_score", 0)
        if color_grading >= 85:
            score += 15
        elif color_grading >= 70:
            score += color_grading * 0.21
        
        # Stabilizasyon (15 puan)
        stabilization = video_data.get("stabilization_score", 0)
        if stabilization >= 90:
            score += 15
        elif stabilization >= 75:
            score += stabilization * 0.2
        
        # Hormozi stili (20 puan)
        hormozi_elements = video_data.get("hormozi_elements", {})
        if hormozi_elements.get("dynamic_captions", False):
            score += 10
        if hormozi_elements.get("colorful_text", False):
            score += 10
        
        # Shadowban shield (15 puan)
        shadowban_shield = video_data.get("shadowban_shield_applied", False)
        if shadowban_shield:
            score += 15
        
        return min(score, 100)
    
    async def _score_seo(self, seo_data: Dict[str, Any]) -> float:
        """SEO skorunu hesapla"""
        score = 0.0
        
        # Başlık optimizasyonu (30 puan)
        title = seo_data.get("title", "")
        title_length = len(title)
        if 30 <= title_length <= 60:
            score += 15
        if seo_data.get("has_primary_keyword", False):
            score += 15
        
        # Açıklama optimizasyonu (25 puan)
        description = seo_data.get("description", "")
        desc_length = len(description)
        if 100 <= desc_length <= 5000:
            score += 15
        if seo_data.get("description_has_keywords", False):
            score += 10
        
        # Etiket optimizasyonu (20 puan)
        tags = seo_data.get("tags", [])
        if 5 <= len(tags) <= 15:
            score += 10
        if seo_data.get("tags_have_keywords", False):
            score += 10
        
        # Anahtar kelime yoğunluğu (15 puan)
        keyword_density = seo_data.get("keyword_density", 0)
        if 1.0 <= keyword_density <= 3.0:
            score += 15
        elif keyword_density < 1.0:
            score += keyword_density * 15
        else:
            score += max(0, 15 - (keyword_density - 3.0) * 5)
        
        # Thumbnail optimizasyonu (10 puan)
        thumbnail_optimized = seo_data.get("thumbnail_optimized", False)
        if thumbnail_optimized:
            score += 10
        
        return min(score, 100)
    
    def _calculate_confidence(self, content_data: Dict[str, Any]) -> float:
        """Güven seviyesini hesapla"""
        confidence = 100.0
        
        # Veri eksikliklerine göre güven seviyesini düşür
        if not content_data.get("script"):
            confidence -= 25
        if not content_data.get("audio"):
            confidence -= 25
        if not content_data.get("video"):
            confidence -= 20
        if not content_data.get("seo"):
            confidence -= 15
        
        # AI kaynaklı verilerin kalitesine göre güven seviyesi
        ai_sources = content_data.get("ai_sources", {})
        for source, quality in ai_sources.items():
            if quality == "high":
                continue
            elif quality == "medium":
                confidence -= 5
            elif quality == "low":
                confidence -= 10
        
        return max(confidence, 0)
    
    def _identify_risk_factors(self, content_data: Dict[str, Any], overall_score: float) -> List[str]:
        """Risk faktörlerini belirle"""
        risk_factors = []
        
        if overall_score < self.thresholds["acceptable"]:
            risk_factors.append("Düşük genel skor - İçerik revize edilmeli")
        
        # Bileşen riskleri
        script_data = content_data.get("script", {})
        if script_data.get("keyword_density", 0) > 5.0:
            risk_factors.append("Anahtar kelime yoğunluğu çok yüksek - Spam riski")
        
        audio_data = content_data.get("audio", {})
        if audio_data.get("noise_level", 0) > 50:
            risk_factors.append("Yüksek arka plan gürültüsü - Dinleyici deneyimini etkiler")
        
        video_data = content_data.get("video", {})
        if "360p" in video_data.get("resolution", ""):
            risk_factors.append("Düşük video çözünürlüğü - İzlenme süresini etkiler")
        
        seo_data = content_data.get("seo", {})
        if len(seo_data.get("title", "")) > 100:
            risk_factors.append("Başlık çok uzun - SEO performansını düşürür")
        
        # Shadowban riskleri
        if not content_data.get("shadowban_shield_applied", False):
            risk_factors.append("Shadowban shield uygulanmadı - Algoritma riski")
        
        return risk_factors
    
    def _generate_recommendations(self, script_score: float, audio_score: float, 
                               video_score: float, seo_score: float, 
                               overall_score: float) -> List[str]:
        """Önerileri oluştur"""
        recommendations = []
        
        # Genel öneriler
        if overall_score < self.thresholds["acceptable"]:
            recommendations.append("İçerik kalitesi düşük - Tüm bileşenler revize edilmeli")
        elif overall_score < self.thresholds["good"]:
            recommendations.append("İçerik kalitesi orta - Bazı iyileştirmeler yapılabilir")
        
        # Senaryo önerileri
        if script_score < self.thresholds["good"]:
            recommendations.append("Senaryo yapısını güçlendirin - Daha fazla etkileşim kancaları ekleyin")
        if script_score < self.thresholds["acceptable"]:
            recommendations.append("Anahtar kelime yoğunluğunu ayarlayın - %1-3 arası olmalı")
        
        # Ses önerileri
        if audio_score < self.thresholds["good"]:
            recommendations.append("Ses kalitesini artırın - Arka plan gürültüsünü azaltın")
        if audio_score < self.thresholds["acceptable"]:
            recommendations.append("Duygusal ifade ekleyin - SSML ile vurgular kullanın")
        
        # Video önerileri
        if video_score < self.thresholds["good"]:
            recommendations.append("Video kalitesini artırın - Daha yüksek çözünürlük kullanın")
        if video_score < self.thresholds["acceptable"]:
            recommendations.append("Hormozi stili ekleyin - Dinamik altyazılar kullanın")
        
        # SEO önerileri
        if seo_score < self.thresholds["good"]:
            recommendations.append("SEO optimizasyonunu güçlendirin - Başlık ve açıklamayı iyileştirin")
        if seo_score < self.thresholds["acceptable"]:
            recommendations.append("Anahtar kelime stratejisi gözden geçirin - LSI keywords ekleyin")
        
        # Yüksek skor önerileri
        if overall_score >= self.thresholds["excellent"]:
            recommendations.append("Mükemmel içerik kalitesi - Yayın için hazır")
        
        return recommendations
    
    def get_score_grade(self, score: float) -> str:
        """Skor notunu belirle"""
        if score >= self.thresholds["excellent"]:
            return "A+ (Mükemmel)"
        elif score >= self.thresholds["good"]:
            return "B (İyi)"
        elif score >= self.thresholds["acceptable"]:
            return "C (Kabul Edilebilir)"
        elif score >= self.thresholds["needs_improvement"]:
            return "D (İyileştirme Gerekli)"
        else:
            return "F (Revize Gerekli)"
    
    def should_require_human_review(self, score: ContentScore) -> bool:
        """İnsan incelemesi gerekip gerekmediğini belirle"""
        return (
            score.overall_score < 75 or  # Düşük genel skor
            score.confidence < 70 or     # Düşük güven seviyesi
            len(score.risk_factors) > 3 or  # Çok sayıda risk faktörü
            any("spam" in risk.lower() for risk in score.risk_factors)  # Spam riski
        )
    
    async def run_ai_consensus(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI consensus mekanizması çalıştır
        SEO_Agent ve Creative_Agent çıktılarını denetle
        """
        
        try:
            # Simüle edilmiş AI agent çıktıları
            seo_agent_score = await self._simulate_seo_agent(content_data)
            creative_agent_score = await self._simulate_creative_agent(content_data)
            
            # Consensus hesapla
            consensus_score = (seo_agent_score + creative_agent_score) / 2
            
            # Uyuşmazlık kontrolü
            score_difference = abs(seo_agent_score - creative_agent_score)
            needs_revision = score_difference > 15 or consensus_score < 75
            
            return {
                "consensus_score": round(consensus_score, 1),
                "seo_agent_score": round(seo_agent_score, 1),
                "creative_agent_score": round(creative_agent_score, 1),
                "score_difference": round(score_difference, 1),
                "needs_revision": needs_revision,
                "recommendation": self._get_consensus_recommendation(
                    consensus_score, score_difference, needs_revision
                ),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI consensus hatası: {e}")
            return {
                "consensus_score": 0,
                "seo_agent_score": 0,
                "creative_agent_score": 0,
                "score_difference": 0,
                "needs_revision": True,
                "recommendation": "Hata: Consensus hesaplanamadı",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _simulate_seo_agent(self, content_data: Dict[str, Any]) -> float:
        """SEO Agent simülasyonu"""
        # SEO odaklı skorlama
        seo_data = content_data.get("seo", {})
        script_data = content_data.get("script", {})
        
        score = 0
        
        # Anahtar kelime optimizasyonu
        if seo_data.get("has_primary_keyword", False):
            score += 30
        if seo_data.get("description_has_keywords", False):
            score += 25
        
        # Senaryo SEO'si
        if script_data.get("keyword_density", 0) >= 1.0:
            score += 25
        
        # Meta veri optimizasyonu
        if seo_data.get("thumbnail_optimized", False):
            score += 20
        
        return min(score, 100)
    
    async def _simulate_creative_agent(self, content_data: Dict[str, Any]) -> float:
        """Creative Agent simülasyonu"""
        # Yaratıcılık odaklı skorlama
        script_data = content_data.get("script", {})
        audio_data = content_data.get("audio", {})
        video_data = content_data.get("video", {})
        
        score = 0
        
        # Yaratıcılık ve etkileşim
        if len(script_data.get("engagement_hooks", [])) >= 3:
            score += 30
        
        # Duygusal ifade
        if audio_data.get("emotional_range", 0) >= 70:
            score += 25
        
        # Görsel kalite
        if video_data.get("hormozi_elements", {}).get("colorful_text", False):
            score += 25
        
        # İnovatif unsurlar
        if video_data.get("shadowban_shield_applied", False):
            score += 20
        
        return min(score, 100)
    
    def _get_consensus_recommendation(self, consensus_score: float, 
                                   score_difference: float, 
                                   needs_revision: bool) -> str:
        """Consensus önerisi oluştur"""
        if needs_revision:
            if score_difference > 20:
                return "Büyük uyuşmazlık - İçerik tamamen revize edilmeli"
            elif consensus_score < 60:
                return "Düşük consensus - AI agent'ları yeniden çalıştırılmalı"
            else:
                return "Küçük uyuşmazlık - Minör iyileştirmeler yeterli"
        else:
            if consensus_score >= 85:
                return "Yüksek consensus - İçerik yayın için mükemmel"
            else:
                return "Orta consensus - İçerik uygun ama iyileştirilebilir"

# Global instance
scoring_engine = ScoringEngine()
