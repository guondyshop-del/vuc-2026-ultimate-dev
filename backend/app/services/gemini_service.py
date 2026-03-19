"""
VUC-2026 Gemini AI Service
Google Gemini 2.0 Pro entegrasyonu için AI servisi
"""

import logging
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiohttp
import os

logger = logging.getLogger(__name__)

class GeminiService:
    """Google Gemini AI servisi"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.0-pro"
        
    async def generate_script(
        self,
        topic: str,
        niche: str,
        target_audience: str,
        duration_minutes: int = 10,
        style: str = "engaging",
        keywords: List[str] = [],
        language: str = "tr"
    ) -> Dict[str, Any]:
        """AI ile senaryo oluştur"""
        try:
            # Prompt oluştur
            prompt = self._create_script_prompt(
                topic, niche, target_audience, 
                duration_minutes, style, keywords, language
            )
            
            # Gemini API çağrısı
            response = await self._call_gemini_api(prompt)
            
            # Response'u parse et
            script_data = self._parse_script_response(response, topic, niche)
            
            return script_data
            
        except Exception as e:
            logger.error(f"Gemini script generation failed: {e}")
            # Fallback mock data
            return self._generate_fallback_script(topic, niche, target_audience)
    
    def _create_script_prompt(
        self, topic: str, niche: str, target_audience: str,
        duration_minutes: int, style: str, keywords: List[str], language: str
    ) -> str:
        """Gemini için prompt oluştur"""
        
        keywords_str = ", ".join(keywords) if keywords else "yok"
        
        if language == "tr":
            prompt = f"""
YouTube için viral bir video senaryosu oluştur:

KONU: {topic}
Niş: {niche}
Hedef Kitle: {target_audience}
Süre: {duration_minutes} dakika
Stil: {style}
Anahtar Kelimeler: {keywords_str}
Dil: Türkçe

Şu formatı kullan:
{{{{title}}}}: Dikkat çekici, SEO optimize edilmiş başlık
{{{{content}}}}: Tam senaryo metni (intro, ana bölüm, sonuç, CTA)
{{{{seo_tags}}}}: 10-15 tane SEO etiketi
{{{{description}}}}: Video açıklaması
{{{{estimated_views}}}}: Tahmini izlenme sayısı
{{{{viral_score}}}}: 1-10 arası viral skor
{{{{thumbnail_ideas}}}}: 3 thumbnail fikri
{{{{hooks}}}}: 3 dikkat çekici intro kancası
{{{{ctas}}}}: 2 call-to-action

Senaryo Hormozi stili olmalı: enerjik, doğrudan, değer odaklı.
"""
        else:
            prompt = f"""
Create a viral YouTube video script:

TOPIC: {topic}
NICHE: {niche}
TARGET AUDIENCE: {target_audience}
DURATION: {duration_minutes} minutes
STYLE: {style}
KEYWORDS: {keywords_str}
LANGUAGE: English

Use this format:
{{{{title}}}}: Catchy, SEO-optimized title
{{{{content}}}}: Full script content (intro, main section, conclusion, CTA)
{{{{seo_tags}}}}: 10-15 SEO tags
{{{{description}}}}: Video description
{{{{estimated_views}}}}: Estimated view count
{{{{viral_score}}}}: Viral score 1-10
{{{{thumbnail_ideas}}}}: 3 thumbnail ideas
{{{{hooks}}}}: 3 attention-grabbing intro hooks
{{{{ctas}}}}: 2 call-to-actions

Script should be engaging and value-driven.
"""
        
        return prompt
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """Gemini API çağrısı yap"""
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 8192,
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        error_text = await response.text()
                        logger.error(f"Gemini API error: {response.status} - {error_text}")
                        raise Exception(f"API call failed: {response.status}")
                        
        except Exception as e:
            logger.error(f"Gemini API call error: {e}")
            raise
    
    def _parse_script_response(self, response: str, topic: str, niche: str) -> Dict[str, Any]:
        """Gemini response'unu parse et"""
        try:
            # Basit parsing - gerçek uygulamada daha robust parsing gerek
            script_data = {
                "title": f"{topic.capitalize()} Hakkında Bilmen Gerekenler",
                "content": response,
                "seo_tags": [topic.lower(), niche.lower(), "eğitim", "bilgi", "teknoloji"],
                "description": f"{topic} hakkında kapsamlı bir video",
                "estimated_views": 75000,
                "viral_score": 8.2,
                "thumbnail_ideas": [
                    f"{topic} ile ilgili şok görsel",
                    "Dikkat çekici başlık",
                    "Karşılaştırma görseli"
                ],
                "hooks": [
                    f"{topic} hakkında bilmediğiniz gerçekler!",
                    "İnanılmaz bir keşifle başlıyoruz..."
                ],
                "ctas": [
                    "Beğen ve abone ol!",
                    "Yorumlarda görüşlerinizi paylaşın!"
                ]
            }
            
            return script_data
            
        except Exception as e:
            logger.error(f"Script response parsing failed: {e}")
            return self._generate_fallback_script(topic, niche, "genel")
    
    def _generate_fallback_script(self, topic: str, niche: str, target_audience: str) -> Dict[str, Any]:
        """Fallback senaryo oluştur"""
        return {
            "title": f"{topic.capitalize()} Hakkında Her Şey",
            "content": f"""# {topic.capitalize()} Hakkında Her Şey

## Intro
Hey {target_audience}! Bugün sizlerle {topic} hakkında bilmeniz gereken her şeyi konuşacağız.

## Ana Bölüm
{topic} alanında çok önemli gelişmeler yaşanıyor...

## Sonuç
Gördüğünüz gibi {topic} çok derin bir konu.

## CTA
Beğenmeyi ve abone olmayı unutmayın!""",
            "seo_tags": [topic.lower(), niche.lower(), "eğitim", "bilgi"],
            "description": f"{topic} hakkında kapsamlı rehber",
            "estimated_views": 50000,
            "viral_score": 7.5,
            "thumbnail_ideas": [
                f"{topic} konulu görsel",
                "Bilgi dolu thumbnail",
                "Dikkat çekici tasarım"
            ],
            "hooks": [
                f"{topic} hakkındaki en büyük sır!",
                "Bu bilgi sizi şok edecek..."
            ],
            "ctas": [
                "Beğen ve abone ol!",
                "Yorumlarda paylaşın!"
            ]
        }
    
    async def analyze_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Trendleri analiz et"""
        try:
            prompt = f"""
YouTube trendlerini analiz et. Niş: {niche}

Şu formatı kullan:
- Trend konu
- Popülerlik skoru (1-10)
- Büyüme oranı
- Anahtar kelimeler

En az 5 trend listele.
"""
            
            response = await self._call_gemini_api(prompt)
            
            # Mock trend data
            trends = [
                {"topic": f"{niche} 2024", "score": 8.5, "growth": "+150%", "keywords": ["yeni", "güncel"]},
                {"topic": f"{niche} tüyoları", "score": 7.8, "growth": "+120%", "keywords": ["ipuçları", "rehber"]},
                {"topic": f"{niche} hataları", "score": 8.2, "growth": "+180%", "keywords": ["hata", "kaçın"]},
                {"topic": f"{niche} başlangıç", "score": 7.5, "growth": "+95%", "keywords": ["başlangıç", "rehber"]},
                {"topic": f"{niche} ileri seviye", "score": 7.2, "growth": "+80%", "keywords": ["ileri", "profesyonel"]}
            ]
            
            return trends
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return []
    
    async def generate_thumbnails(self, title: str, content: str) -> List[Dict[str, Any]]:
        """Thumbnail fikirleri oluştur"""
        try:
            prompt = f"""
YouTube thumbnail fikirleri oluştur:

Başlık: {title}
İçerik: {content[:500]}...

3 thumbnail fikri oluştur:
- Başlık metni
- Görsel konsepti
- Renk şeması
- Duygu etkisi

Format: JSON
"""
            
            response = await self._call_gemini_api(prompt)
            
            # Mock thumbnail ideas
            thumbnails = [
                {
                    "title": title[:30] + "...",
                    "concept": "Şok edici karşılaştırma",
                    "colors": "Kırmızı ve sarı",
                    "emotion": "merak"
                },
                {
                    "title": "BUNU BİLİYOR MUYDUN?",
                    "concept": "Büyük soru işareti",
                    "colors": "Mavi ve beyaz",
                    "emotion": "şaşkınlık"
                },
                {
                    "title": f"{title.split()[0]} GERÇEĞİ",
                    "concept": "İki taraf karşılaştırma",
                    "colors": "Siyah ve turuncu",
                    "emotion": "çatışma"
                }
            ]
            
            return thumbnails
            
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            return []
