"""
VUC-2026 Transcription SEO Service
LSI keyword injection at strategic audio timestamps

Injects high-value LSI keywords at specific audio timestamps
to manipulate YouTube's Speech-to-Text indexing bot.
"""

import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TranscriptionSEO:
    """Transcription SEO with strategic LSI keyword injection"""

    def __init__(self):
        self.lsi_databases: Dict[str, List[str]] = {
            "technology": [
                "yapay zeka uygulamaları", "makine öğrenmesi algoritmaları",
                "derin öğrenme modelleri", "nöral ağ eğitimi", "veri bilimi araçları",
                "büyük veri analizi", "bulut bilişim hizmetleri", "API entegrasyonu",
                "yazılım geliştirme süreçleri", "DevOps pratikleri"
            ],
            "business": [
                "gelir artırma stratejileri", "maliyet optimizasyonu", "pazar analizi",
                "müşteri kazanım stratejileri", "satış hunisi optimizasyonu",
                "dijital pazarlama taktikleri", "marka bilinirliği artırma",
                "e-ticaret büyüme hackler", "dönüşüm oranı optimizasyonu", "ROI hesaplama"
            ],
            "education": [
                "öğrenme metodolojileri", "eğitim teknolojileri", "aktif öğrenme teknikleri",
                "bellek güçlendirme yöntemleri", "uzaktan eğitim platformları",
                "interaktif öğrenme araçları", "başarı motivasyonu", "sınav stratejileri",
                "not alma sistemleri", "zihin haritaları oluşturma"
            ],
            "gaming": [
                "oyun geliştirme temelleri", "e-spor profesyonelleşme", "oyun stratejileri",
                "karakter geliştirme ipuçları", "oyun içi ekonomi yönetimi",
                "multiplayer taktikleri", "stream kurulum rehberi", "yayıncılık teknikleri",
                "gaming donanım seçimi", "performans optimizasyonu"
            ],
            "general": [
                "verimlilik artırma yöntemleri", "zaman yönetimi teknikleri",
                "kişisel gelişim adımları", "hedef belirleme stratejileri",
                "motivasyon kaynakları", "alışkanlık oluşturma", "stres yönetimi",
                "sağlıklı yaşam ipuçları", "finansal okuryazarlık", "iletişim becerileri"
            ]
        }

        self.stt_optimization_rules = {
            "keyword_frequency": "high_value_keywords_first_30_seconds",
            "repetition_strategy": "natural_variation_not_exact",
            "sentence_position": "hook_midpoint_conclusion",
            "pronunciation_clarity": "slow_emphasis_on_key_terms",
            "question_format": "include_search_queries_verbatim"
        }

    def inject_lsi_keywords(self, script: str, keywords: List[str],
                             niche: str = "general") -> Dict[str, Any]:
        """
        Inject LSI keywords at strategic timestamps within the script.

        Args:
            script: Original script text
            keywords: Primary keywords to optimize for
            niche: Content niche for LSI database selection

        Returns:
            Optimized script with injection report
        """

        sentences = self._split_sentences(script)
        lsi_pool = self._get_lsi_pool(niche, keywords)
        injection_plan = self._create_injection_plan(sentences, keywords, lsi_pool)
        optimized_script = self._apply_injections(sentences, injection_plan)
        keyword_density = self._calculate_keyword_density(optimized_script, keywords)
        stt_score = self._calculate_stt_score(optimized_script, keywords, lsi_pool)
        timestamp_map = self._generate_timestamp_map(sentences, injection_plan)

        logger.info(f"LSI enjeksiyonu tamamlandı: {len(injection_plan)} enjeksiyon, STT skoru: {stt_score:.1f}")

        return {
            "optimized_script": optimized_script,
            "original_word_count": len(script.split()),
            "optimized_word_count": len(optimized_script.split()),
            "injection_count": len(injection_plan),
            "keyword_density": keyword_density,
            "stt_score": stt_score,
            "timestamp_map": timestamp_map,
            "lsi_keywords_used": [inj["lsi_keyword"] for inj in injection_plan],
            "optimization_rules_applied": list(self.stt_optimization_rules.keys()),
            "generated_at": datetime.now().isoformat()
        }

    def analyze_transcript_seo(self, transcript: str, target_keywords: List[str],
                                niche: str = "general") -> Dict[str, Any]:
        """
        Analyze an existing transcript for SEO optimization opportunities.

        Args:
            transcript: Existing transcript or script
            target_keywords: Keywords to optimize for
            niche: Content niche

        Returns:
            SEO analysis with recommendations
        """

        sentences = self._split_sentences(transcript)
        lsi_pool = self._get_lsi_pool(niche, target_keywords)
        current_density = self._calculate_keyword_density(transcript, target_keywords)
        current_stt_score = self._calculate_stt_score(transcript, target_keywords, lsi_pool)
        missing_lsi = self._find_missing_lsi(transcript, lsi_pool)
        keyword_distribution = self._analyze_keyword_distribution(sentences, target_keywords)
        timestamp_opportunities = self._find_timestamp_opportunities(sentences, target_keywords)

        return {
            "current_stt_score": current_stt_score,
            "target_stt_score": 85.0,
            "improvement_needed": max(0.0, 85.0 - current_stt_score),
            "keyword_density": current_density,
            "missing_lsi_keywords": missing_lsi[:10],
            "keyword_distribution": keyword_distribution,
            "timestamp_opportunities": timestamp_opportunities,
            "recommendations": self._generate_recommendations(
                current_stt_score, current_density, missing_lsi, keyword_distribution
            ),
            "analyzed_at": datetime.now().isoformat()
        }

    def generate_stt_optimized_captions(self, script: str, keywords: List[str],
                                         timing_seconds_per_word: float = 0.5) -> List[Dict[str, Any]]:
        """
        Generate SRT-style caption entries with strategic keyword placement.

        Args:
            script: Script text
            keywords: Keywords to emphasize
            timing_seconds_per_word: Average word duration in seconds

        Returns:
            List of caption entries with timestamps
        """

        words = script.split()
        captions = []
        current_time = 0.0
        words_per_caption = 10
        caption_index = 1

        for i in range(0, len(words), words_per_caption):
            caption_words = words[i:i + words_per_caption]
            caption_text = ' '.join(caption_words)
            duration = len(caption_words) * timing_seconds_per_word

            # Check if this caption contains target keywords
            contains_keyword = any(k.lower() in caption_text.lower() for k in keywords)

            captions.append({
                "index": caption_index,
                "start_time": round(current_time, 2),
                "end_time": round(current_time + duration, 2),
                "start_srt": self._seconds_to_srt(current_time),
                "end_srt": self._seconds_to_srt(current_time + duration),
                "text": caption_text,
                "contains_keyword": contains_keyword,
                "stt_priority": "high" if contains_keyword else "normal"
            })

            current_time += duration
            caption_index += 1

        return captions

    def _get_lsi_pool(self, niche: str, keywords: List[str]) -> List[str]:
        """Get LSI keywords combining niche database and primary keywords"""
        base_lsi = self.lsi_databases.get(niche, self.lsi_databases["general"])
        # Add variations of primary keywords
        variations = []
        for keyword in keywords[:3]:
            variations.extend([
                f"{keyword} nedir",
                f"{keyword} nasıl yapılır",
                f"{keyword} rehberi",
                f"en iyi {keyword}",
                f"{keyword} 2026"
            ])
        return base_lsi + variations

    def _create_injection_plan(self, sentences: List[str], keywords: List[str],
                                lsi_pool: List[str]) -> List[Dict[str, Any]]:
        """Create strategic injection plan"""
        plan = []
        total = len(sentences)

        # Target positions: ~15%, ~30%, ~50%, ~70%, ~90%
        target_positions = [
            int(total * 0.15),
            int(total * 0.30),
            int(total * 0.50),
            int(total * 0.70),
            int(total * 0.90)
        ]

        # Avoid duplicates
        used_lsi = set()
        lsi_idx = 0

        for pos in target_positions:
            if lsi_idx >= len(lsi_pool):
                break
            lsi_kw = lsi_pool[lsi_idx]
            if lsi_kw not in used_lsi:
                plan.append({
                    "sentence_index": min(pos, total - 1),
                    "lsi_keyword": lsi_kw,
                    "injection_type": "natural_mention",
                    "position_pct": round(pos / max(total, 1) * 100, 1)
                })
                used_lsi.add(lsi_kw)
                lsi_idx += 1

        return plan

    def _apply_injections(self, sentences: List[str], injection_plan: List[Dict[str, Any]]) -> str:
        """Apply LSI keyword injections to sentences"""
        modified = list(sentences)

        for injection in injection_plan:
            idx = injection["sentence_index"]
            lsi = injection["lsi_keyword"]
            if idx < len(modified):
                # Natural insertion templates
                templates = [
                    f"{modified[idx]} Bu konuda {lsi} konusuna da değinmek istiyorum.",
                    f"{modified[idx]} Ayrıca {lsi} hakkında bilmeniz gerekenler var.",
                    f"{modified[idx]} {lsi} açısından bakıldığında bu çok önemli.",
                ]
                # Pick template that fits
                import random
                modified[idx] = random.choice(templates)

        return ' '.join(modified)

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density for each keyword"""
        text_lower = text.lower()
        word_count = max(len(text.split()), 1)
        density = {}
        for kw in keywords:
            count = text_lower.count(kw.lower())
            density[kw] = round((count / word_count) * 100, 2)
        return density

    def _calculate_stt_score(self, text: str, keywords: List[str], lsi_pool: List[str]) -> float:
        """Calculate YouTube STT optimization score (0-100)"""
        score = 50.0
        text_lower = text.lower()

        # Primary keyword presence
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 8.0

        # LSI keyword presence
        lsi_found = sum(1 for lsi in lsi_pool if lsi.lower() in text_lower)
        score += min(lsi_found * 3.0, 20.0)

        # Opening hook (first 30 words should have keywords)
        first_30 = ' '.join(text.split()[:30]).lower()
        for kw in keywords:
            if kw.lower() in first_30:
                score += 5.0
                break

        # Question phrases (YouTube indexes questions)
        question_count = text.count('?')
        score += min(question_count * 2.0, 8.0)

        # Natural repetition
        if keywords:
            main_kw_count = text_lower.count(keywords[0].lower())
            if 3 <= main_kw_count <= 7:
                score += 5.0

        return min(100.0, round(score, 1))

    def _generate_timestamp_map(self, sentences: List[str],
                                 injection_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate timestamp map for STT injection points"""
        timestamp_map = []
        cumulative_time = 0.0

        for inj in injection_plan:
            idx = inj["sentence_index"]
            # Estimate time: ~3.5s per sentence
            cumulative_time = idx * 3.5
            timestamp_map.append({
                "timestamp": round(cumulative_time, 1),
                "timestamp_formatted": self._seconds_to_srt(cumulative_time),
                "lsi_keyword": inj["lsi_keyword"],
                "sentence_index": idx,
                "position_pct": inj["position_pct"],
                "stt_priority": "high"
            })

        return timestamp_map

    def _find_missing_lsi(self, transcript: str, lsi_pool: List[str]) -> List[str]:
        """Find LSI keywords not present in transcript"""
        text_lower = transcript.lower()
        return [lsi for lsi in lsi_pool if lsi.lower() not in text_lower]

    def _analyze_keyword_distribution(self, sentences: List[str],
                                       keywords: List[str]) -> Dict[str, Any]:
        """Analyze how keywords are distributed across the script"""
        if not keywords:
            return {}

        kw = keywords[0].lower()
        keyword_positions = [i for i, s in enumerate(sentences) if kw in s.lower()]
        total = max(len(sentences), 1)

        return {
            "total_occurrences": len(keyword_positions),
            "position_percentages": [round(p / total * 100, 1) for p in keyword_positions],
            "well_distributed": len(keyword_positions) >= 3,
            "first_appearance_pct": round(keyword_positions[0] / total * 100, 1) if keyword_positions else 0,
            "last_appearance_pct": round(keyword_positions[-1] / total * 100, 1) if keyword_positions else 0
        }

    def _find_timestamp_opportunities(self, sentences: List[str],
                                       keywords: List[str]) -> List[Dict[str, Any]]:
        """Find timestamp positions where keywords can be naturally added"""
        opportunities = []
        cumulative_ts = 0.0
        for i, sentence in enumerate(sentences):
            cumulative_ts += 3.5
            # Sentences without keywords near high-engagement points
            has_kw = any(k.lower() in sentence.lower() for k in keywords)
            if not has_kw and len(sentence.split()) > 8:
                opportunities.append({
                    "sentence_index": i,
                    "timestamp": round(cumulative_ts, 1),
                    "sentence_preview": sentence[:80],
                    "suggested_lsi_insertion": True
                })
        return opportunities[:10]

    def _generate_recommendations(self, stt_score: float, density: Dict[str, float],
                                   missing_lsi: List[str],
                                   distribution: Dict[str, Any]) -> List[str]:
        """Generate actionable optimization recommendations"""
        recs = []

        if stt_score < 70:
            recs.append("Ana anahtar kelimeyi ilk 30 kelimede kullan")
        if stt_score < 80:
            recs.append(f"{len(missing_lsi)} LSI anahtar kelimesi eksik — enjeksiyon önerilir")
        if not distribution.get("well_distributed"):
            recs.append("Anahtar kelime dağılımını videonun tamamına yay")
        for kw, d in density.items():
            if d < 0.5:
                recs.append(f"'{kw}' yoğunluğu düşük (%{d}) — 2-3 ek kullanım ekle")
            elif d > 3.0:
                recs.append(f"'{kw}' çok sık kullanılmış (%{d}) — doğal azaltma yapılmalı")

        if not recs:
            recs.append("STT optimizasyonu iyi durumda — yayına hazır")

        return recs

    def _seconds_to_srt(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format HH:MM:SS,mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# Global instance
transcription_seo = TranscriptionSEO()
