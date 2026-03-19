"""
VUC-2026 Clickbait Optimization
YouTube Clickbait Policy uyumlu A/B test sistemi
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class ClickbaitType(Enum):
    """Clickbait türleri"""
    MISLEADING_PROMISE = "misleading_promise"
    SENSATIONALIZED = "sensationalized"
    CURIOSTIY_GAP = "curiosity_gap"
    EMOTIONAL_MANIPULATION = "emotional_manipulation"
    LEGITIMATE_HIGHLIGHT = "legitimate_highlight"

@dataclass
class TitleVariant:
    """Başlık variant'ı"""
    variant_id: str
    title_text: str
    clickbait_type: ClickbaitType
    relevance_score: float
    ctr_prediction: float
    compliance_score: float
    keywords: List[str]
    emotional_tone: str

@dataclass
class ABTest:
    """A/B test bilgileri"""
    test_id: str
    video_id: str
    original_title: str
    variants: List[TitleVariant]
    start_time: datetime
    duration_hours: int
    status: str
    results: Optional[Dict] = None

class ClickbaitAnalyzer:
    """Clickbait analiz sınıfı"""
    
    def __init__(self):
        self.misleading_patterns = [
            r" garanti(ed)?",
            r" %100",
            r"kesin(likle)?",
            r"asla",
            r"her zaman",
            r"mutlaka",
            r"hayatınızın şansı"
        ]
        
        self.sensationalized_words = [
            "şok", "inanılmaz", "müthik", "ağzı açık", "pes",
            "dehşet", "korkunç", "felaket", "skandal"
        ]
        
        self.curiosity_gap_patterns = [
            r"bu.*nedir",
            r"neden.*",
            r"nasıl.*",
            r".*\d+.*sır",
            r".*\d+.*yöntem"
        ]
    
    def analyze_clickbait_type(self, title: str) -> ClickbaitType:
        """Başlığın clickbait türünü analiz et"""
        title_lower = title.lower()
        
        # Yanıltıcı vaatler
        for pattern in self.misleading_patterns:
            if re.search(pattern, title_lower):
                return ClickbaitType.MISLEADING_PROMISE
        
        # Abartılı ifadeler
        sensational_count = sum(1 for word in self.sensationalized_words if word in title_lower)
        if sensational_count >= 2:
            return ClickbaitType.SENSATIONALIZED
        
        # Merak boşluğu
        for pattern in self.curiosity_gap_patterns:
            if re.search(pattern, title_lower):
                return ClickbaitType.CURIOSTIY_GAP
        
        # Duygusal manipülasyon
        emotional_words = ["üzücü", "mutluluk", "öfke", "korku", "sevgi"]
        if any(word in title_lower for word in emotional_words):
            return ClickbaitType.EMOTIONAL_MANIPULATION
        
        # Meşru vurgu
        return ClickbaitType.LEGITIMATE_HIGHLIGHT
    
    def calculate_compliance_score(self, title: str, clickbait_type: ClickbaitType) -> float:
        """YouTube uyumluluk skoru (0-100)"""
        base_score = 70
        
        # Clickbait türüne göre ceza puanları
        penalties = {
            ClickbaitType.MISLEADING_PROMISE: -50,
            ClickbaitType.SENSATIONALIZED: -30,
            ClickbaitType.CURIOSTIY_GAP: -10,
            ClickbaitType.EMOTIONAL_MANIPULATION: -20,
            ClickbaitType.LEGITIMATE_HIGHLIGHT: 0
        }
        
        base_score += penalties.get(clickbait_type, 0)
        
        # Başlık uzunluğu kontrolü
        if len(title) > 100:
            base_score -= 10
        elif len(title) < 20:
            base_score -= 5
        
        # Büyük harf kontrolü
        uppercase_ratio = sum(1 for c in title if c.isupper()) / len(title)
        if uppercase_ratio > 0.3:
            base_score -= 15
        
        # Noktalama işareti kontrolü
        punctuation_count = sum(1 for c in title if c in "!?.")
        if punctuation_count > 2:
            base_score -= 10
        
        return max(0, min(100, base_score))

class TitleOptimizer:
    """Başlık optimize edici"""
    
    def __init__(self, gemini_service):
        self.gemini_service = gemini_service
        self.clickbait_analyzer = ClickbaitAnalyzer()
    
    def generate_variants(self, original_title: str, video_keywords: List[str], target_audience: str) -> List[TitleVariant]:
        """Başlık variant'ları oluştur"""
        variants = []
        
        # 1. Meşru vurgu variant'ı
        variant1 = self._create_legitimate_highlight(original_title, video_keywords)
        variants.append(variant1)
        
        # 2. Merak boşluğu variant'ı (düşük riskli)
        variant2 = self._create_curiosity_gap(original_title, video_keywords)
        variants.append(variant2)
        
        # 3. Sayısal variant
        variant3 = self._create_numerical_variant(original_title, video_keywords)
        variants.append(variant3)
        
        # 4. Fayda odaklı variant
        variant4 = self._create_benefit_focused(original_title, video_keywords, target_audience)
        variants.append(variant4)
        
        # 5. Aciliyet variant'ı
        variant5 = self._create_urgency_variant(original_title, video_keywords)
        variants.append(variant5)
        
        return variants
    
    def _create_legitimate_highlight(self, original_title: str, keywords: List[str]) -> TitleVariant:
        """Meşru vurgu variant'ı"""
        prompt = f"""
        Orijinal başlık: {original_title}
        Anahtar kelimeler: {', '.join(keywords)}
        
        Bu başlığı, YouTube'un clickbait kurallarına uyumlu şekilde, içeriğin gerçek değerini vurgulayacak şekilde yeniden yaz.
        Kurallar:
        - Yanıltıcı vaatlerden KAÇIN
        - Abartılı ifadeler KULLANMA
        - İçerikle ilgili gerçek faydayı vurgula
        - 60-80 karakter arasında olmalı
        - Hedef kitle için ilgi çekici olmalı
        
        Sadece başlığı döndür.
        """
        
        try:
            optimized_title = self.gemini_service.generate_content(prompt)
        except:
            optimized_title = original_title
        
        return TitleVariant(
            variant_id=f"legitimate_{int(time.time())}",
            title_text=optimized_title.strip(),
            clickbait_type=ClickbaitType.LEGITIMATE_HIGHLIGHT,
            relevance_score=0.9,
            ctr_prediction=0.65,
            compliance_score=95,
            keywords=keywords,
            emotional_tone="informative"
        )
    
    def _create_curiosity_gap(self, original_title: str, keywords: List[str]) -> TitleVariant:
        """Merak boşluğu variant'ı (düşük riskli)"""
        prompt = f"""
        Orijinal başlık: {original_title}
        Anahtar kelimeler: {', '.join(keywords)}
        
        Bu başlığı, merak uyandıran ancak yanıltıcı olmayan şekilde yeniden yaz.
        Kurallar:
        - "Neden...", "Nasıl...", "Bu..." gibi formatlar kullanabilirsin
        - İçerikte cevaplanan bir soru sorun
        - Abartılı ifadelerden KAÇIN
        - 50-70 karakter arasında olmalı
        
        Sadece başlığı döndür.
        """
        
        try:
            curiosity_title = self.gemini_service.generate_content(prompt)
        except:
            curiosity_title = f"Neden {keywords[0] if keywords else 'bu'} önemli? {original_title[:30]}"
        
        return TitleVariant(
            variant_id=f"curiosity_{int(time.time())}",
            title_text=curiosity_title.strip(),
            clickbait_type=ClickbaitType.CURIOSTIY_GAP,
            relevance_score=0.8,
            ctr_prediction=0.75,
            compliance_score=85,
            keywords=keywords,
            emotional_tone="curious"
        )
    
    def _create_numerical_variant(self, original_title: str, keywords: List[str]) -> TitleVariant:
        """Sayısal variant"""
        prompt = f"""
        Orijinal başlık: {original_title}
        Anahtar kelimeler: {', '.join(keywords)}
        
        Bu başlığı, sayısal veriler içeren şekilde yeniden yaz.
        Kurallar:
        - "3 Yöntem", "5 Adım", "2026'da" gibi sayılar kullan
        - Gerçekçi ve içeriğe uygun sayılar kullan
        - 60-80 karakter arasında olmalı
        
        Sadece başlığı döndür.
        """
        
        try:
            numerical_title = self.gemini_service.generate_content(prompt)
        except:
            numerical_title = f"2026'da {keywords[0] if keywords else 'Bu Konu'}: 3 Önemli Nokta"
        
        return TitleVariant(
            variant_id=f"numerical_{int(time.time())}",
            title_text=numerical_title.strip(),
            clickbait_type=ClickbaitType.LEGITIMATE_HIGHLIGHT,
            relevance_score=0.85,
            ctr_prediction=0.70,
            compliance_score=90,
            keywords=keywords,
            emotional_tone="structured"
        )
    
    def _create_benefit_focused(self, original_title: str, keywords: List[str], target_audience: str) -> TitleVariant:
        """Fayda odaklı variant"""
        prompt = f"""
        Orijinal başlık: {original_title}
        Anahtar kelimeler: {', '.join(keywords)}
        Hedef kitle: {target_audience}
        
        Bu başlığı, hedef kitlenin faydalarına odaklanarak yeniden yaz.
        Kurallar:
        - İzleyiciye ne kazanacağını göster
        - Somut faydalar vurgula
        - 60-80 karakter arasında olmalı
        
        Sadece başlığı döndür.
        """
        
        try:
            benefit_title = self.gemini_service.generate_content(prompt)
        except:
            benefit_title = f"{target_audience} için {keywords[0] if keywords else 'Bu'}: Daha İyi Sonuçlar"
        
        return TitleVariant(
            variant_id=f"benefit_{int(time.time())}",
            title_text=benefit_title.strip(),
            clickbait_type=ClickbaitType.LEGITIMATE_HIGHLIGHT,
            relevance_score=0.88,
            ctr_prediction=0.72,
            compliance_score=92,
            keywords=keywords,
            emotional_tone="beneficial"
        )
    
    def _create_urgency_variant(self, original_title: str, keywords: List[str]) -> TitleVariant:
        """Aciliyet variant'ı"""
        prompt = f"""
        Orijinal başlık: {original_title}
        Anahtar kelimeler: {', '.join(keywords)}
        
        Bu başlığı, ılımlı bir aciliyet hissi yaratacak şekilde yeniden yaz.
        Kurallar:
        - "Şimdi", "Hemen", "Kaçırma" gibi ifadeler HAFİFÇE kullanabilirsin
        - Yanıltıcı zaman kısıtlamalarından KAÇIN
        - 60-80 karakter arasında olmalı
        
        Sadece başlığı döndür.
        """
        
        try:
            urgency_title = self.gemini_service.generate_content(prompt)
        except:
            urgency_title = f"{keywords[0] if keywords else 'Bu Konu'}: Şimdi Öğrenmeniz Gerekenler"
        
        return TitleVariant(
            variant_id=f"urgency_{int(time.time())}",
            title_text=urgency_title.strip(),
            clickbait_type=ClickbaitType.LEGITIMATE_HIGHLIGHT,
            relevance_score=0.82,
            ctr_prediction=0.68,
            compliance_score=88,
            keywords=keywords,
            emotional_tone="urgent"
        )

class ABTestManager:
    """A/B test yöneticisi"""
    
    def __init__(self, youtube_api_service):
        self.youtube_api = youtube_api_service
        self.active_tests = {}
        self.test_history = []
    
    def create_ab_test(self, video_id: str, original_title: str, variants: List[TitleVariant], duration_hours: int = 48) -> str:
        """A/B test oluştur"""
        test_id = f"ab_test_{video_id}_{int(time.time())}"
        
        # Sadece uyumlu variant'ları seç
        compliant_variants = [v for v in variants if v.compliance_score >= 70]
        
        if not compliant_variants:
            compliant_variants = variants[:1]  # En azından bir variant
        
        ab_test = ABTest(
            test_id=test_id,
            video_id=video_id,
            original_title=original_title,
            variants=compliant_variants,
            start_time=datetime.now(),
            duration_hours=duration_hours,
            status="initialized"
        )
        
        self.active_tests[test_id] = ab_test
        return test_id
    
    async def run_ab_test(self, test_id: str) -> Dict:
        """A/B testini çalıştır"""
        if test_id not in self.active_tests:
            return {"error": "Test not found"}
        
        test = self.active_tests[test_id]
        test.status = "running"
        
        try:
            # YouTube Analytics'ten veri çek
            analytics_data = await self._fetch_analytics_data(test.video_id, test.duration_hours)
            
            # Her variant için performans hesapla
            variant_results = []
            for variant in test.variants:
                # Simüle edilmiş CTR verisi
                simulated_ctr = variant.ctr_prediction + random.uniform(-0.1, 0.1)
                simulated_views = random.randint(1000, 10000)
                simulated_clicks = int(simulated_views * simulated_ctr)
                
                variant_result = {
                    "variant_id": variant.variant_id,
                    "title": variant.title_text,
                    "clickbait_type": variant.clickbait_type.value,
                    "compliance_score": variant.compliance_score,
                    "views": simulated_views,
                    "clicks": simulated_clicks,
                    "ctr": simulated_ctr,
                    "engagement_rate": random.uniform(0.02, 0.15),
                    "watch_time_avg": random.uniform(180, 600)
                }
                variant_results.append(variant_result)
            
            # Orijinal başlık için de veri ekle
            original_ctr = random.uniform(0.03, 0.08)
            original_views = random.randint(1000, 10000)
            original_result = {
                "variant_id": "original",
                "title": test.original_title,
                "clickbait_type": "original",
                "compliance_score": 100,
                "views": original_views,
                "clicks": int(original_views * original_ctr),
                "ctr": original_ctr,
                "engagement_rate": random.uniform(0.02, 0.12),
                "watch_time_avg": random.uniform(200, 550)
            }
            variant_results.append(original_result)
            
            # En iyi variant'ı belirle
            best_variant = max(variant_results, key=lambda x: x["ctr"] * x["compliance_score"] / 100)
            
            test.results = {
                "test_id": test_id,
                "video_id": test.video_id,
                "duration_hours": test.duration_hours,
                "variants": variant_results,
                "best_variant": best_variant,
                "improvement_vs_original": (best_variant["ctr"] - original_result["ctr"]) / original_result["ctr"] * 100,
                "test_completed_at": datetime.now().isoformat()
            }
            
            test.status = "completed"
            self.test_history.append(test)
            
            return test.results
            
        except Exception as e:
            print(f"AB test execution error: {e}")
            test.status = "failed"
            return {"error": str(e)}
    
    async def _fetch_analytics_data(self, video_id: str, duration_hours: int) -> Dict:
        """YouTube Analytics verisi çek"""
        # Simüle edilmiş analytics verisi
        await asyncio.sleep(2)  # API call simülasyonu
        
        return {
            "video_id": video_id,
            "views": random.randint(1000, 10000),
            "watch_time_minutes": random.randint(200, 2000),
            "subscribers_gained": random.randint(5, 50)
        }
    
    def get_test_recommendations(self, test_id: str) -> Dict:
        """Test önerileri"""
        if test_id not in self.active_tests:
            return {"error": "Test not found"}
        
        test = self.active_tests[test_id]
        
        if not test.results:
            return {"error": "Test not completed"}
        
        results = test.results
        best_variant = results["best_variant"]
        
        recommendations = []
        
        # Compliance kontrolü
        if best_variant["compliance_score"] < 80:
            recommendations.append("En iyi başlığın uyumluluk skoru düşük. Daha güvenli variant'ları tercih edin.")
        
        # CTR improvement kontrolü
        improvement = results["improvement_vs_original"]
        if improvement < 10:
            recommendations.append("CTR iyileştirmesi düşük. Başlık varyasyonlarını artırın.")
        elif improvement > 50:
            recommendations.append("CTR iyileştirmesi çok yüksek. Clickbait riskini kontrol edin.")
        
        # Clickbait türü analizi
        clickbait_types = [v["clickbait_type"] for v in results["variants"]]
        if "misleading_promise" in clickbait_types:
            recommendations.append("Yanıltıcı vaat içeren variant'ları kullanmaktan kaçının.")
        
        return {
            "test_id": test_id,
            "best_variant": best_variant,
            "recommendations": recommendations,
            "compliance_status": "COMPLIANT" if best_variant["compliance_score"] >= 80 else "NEEDS_REVIEW",
            "action_required": best_variant["compliance_score"] < 80
        }

class ClickbaitOptimization:
    """Ana Clickbait Optimization sınıfı"""
    
    def __init__(self, gemini_service, youtube_api_service):
        self.title_optimizer = TitleOptimizer(gemini_service)
        self.ab_test_manager = ABTestManager(youtube_api_service)
        self.clickbait_analyzer = ClickbaitAnalyzer()
    
    def optimize_title(self, video_id: str, original_title: str, video_keywords: List[str], target_audience: str) -> Dict:
        """Başlığı optimize et"""
        
        # 1. Orijinal başlığı analiz et
        original_clickbait_type = self.clickbait_analyzer.analyze_clickbait_type(original_title)
        original_compliance = self.clickbait_analyzer.calculate_compliance_score(original_title, original_clickbait_type)
        
        # 2. Variant'ları oluştur
        variants = self.title_optimizer.generate_variants(original_title, video_keywords, target_audience)
        
        # 3. Her variant'ın compliance'ini kontrol et
        for variant in variants:
            variant.compliance_score = self.clickbait_analyzer.calculate_compliance_score(
                variant.title_text, 
                variant.clickbait_type
            )
        
        # 4. A/B test oluştur
        test_id = self.ab_test_manager.create_ab_test(video_id, original_title, variants)
        
        return {
            "video_id": video_id,
            "original_title": original_title,
            "original_analysis": {
                "clickbait_type": original_clickbait_type.value,
                "compliance_score": original_compliance
            },
            "test_id": test_id,
            "variants": [
                {
                    "variant_id": v.variant_id,
                    "title": v.title_text,
                    "clickbait_type": v.clickbait_type.value,
                    "compliance_score": v.compliance_score,
                    "ctr_prediction": v.ctr_prediction
                }
                for v in variants
            ],
            "status": "test_created",
            "next_step": "run_ab_test"
        }
    
    async def run_optimization_test(self, test_id: str) -> Dict:
        """Optimizasyon testini çalıştır"""
        return await self.ab_test_manager.run_ab_test(test_id)
    
    def get_optimization_report(self, test_id: str) -> Dict:
        """Optimizasyon raporu"""
        return self.ab_test_manager.get_test_recommendations(test_id)
    
    def validate_title_compliance(self, title: str) -> Dict:
        """Başlık uyumluluğunu validate et"""
        clickbait_type = self.clickbait_analyzer.analyze_clickbait_type(title)
        compliance_score = self.clickbait_analyzer.calculate_compliance_score(title, clickbait_type)
        
        return {
            "title": title,
            "clickbait_type": clickbait_type.value,
            "compliance_score": compliance_score,
            "is_compliant": compliance_score >= 70,
            "risk_level": "LOW" if compliance_score >= 85 else "MEDIUM" if compliance_score >= 70 else "HIGH",
            "recommendations": self._generate_compliance_recommendations(title, clickbait_type, compliance_score)
        }
    
    def _generate_compliance_recommendations(self, title: str, clickbait_type: ClickbaitType, compliance_score: float) -> List[str]:
        """Uyumluluk önerileri"""
        recommendations = []
        
        if clickbait_type == ClickbaitType.MISLEADING_PROMISE:
            recommendations.append("Yanıltıcı vaatleri kaldırın")
            recommendations.append("Garanti ifadelerinden kaçının")
        
        if clickbait_type == ClickbaitType.SENSATIONALIZED:
            recommendations.append("Abartılı ifadeleri azaltın")
            recommendations.append("Daha dengeli bir dil kullanın")
        
        if compliance_score < 70:
            recommendations.append("Başlığı daha bilgilendirici hale getirin")
            recommendations.append("Gerçek içeriği yansıtın")
        
        if len(title) > 100:
            recommendations.append("Başlık uzunluğunu kısaltın")
        
        return recommendations
