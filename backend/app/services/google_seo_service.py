"""
VUC-2026 Google SEO Service
Google AI ve YouTube API'leri ile SEO optimizasyonu

Bu servis, Google Generative AI ve YouTube Data API kullanarak
içerik SEO optimizasyonu, anahtar kelime analizi ve sıralama takibi yapar.
"""

import os
import logging
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
from urllib.parse import urlencode, urlparse, parse_qs

# Google API'leri için import'lar
try:
    from google import genai
    from google.genai import types
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    logging.warning("Google API'leri mevcut değil")
    GOOGLE_APIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class GoogleSEOService:
    """Google SEO optimizasyon servisi"""
    
    def __init__(self, api_key: str = None, youtube_api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_AI_API_KEY")
        self.youtube_api_key = youtube_api_key or os.getenv("YOUTUBE_API_KEY")
        self.genai_client = None
        self.youtube_service = None
        self.seo_cache = {}
        
        if self.api_key:
            self._initialize_genai()
        
        if self.youtube_api_key:
            self._initialize_youtube()
    
    def _initialize_genai(self):
        """Google Generative AI client'ını başlat"""
        try:
            self.genai_client = genai.Client(api_key=self.api_key)
            logger.info("Google Generative AI client başlatıldı")
        except Exception as e:
            logger.error(f"Google GenAI başlatma hatası: {e}")
            self.genai_client = None
    
    def _initialize_youtube(self):
        """YouTube Data API client'ını başlat"""
        try:
            self.youtube_service = build('youtube', 'v3', developerKey=self.youtube_api_key)
            logger.info("YouTube Data API client başlatıldı")
        except Exception as e:
            logger.error(f"YouTube API başlatma hatası: {e}")
            self.youtube_service = None
    
    async def analyze_keywords(self, topic: str, language: str = "tr") -> Dict[str, Any]:
        """
        Konu için anahtar kelime analizi yap
        
        Args:
            topic: Analiz edilecek konu
            language: Dil kodu
            
        Returns:
            Anahtar kelime analizi sonuçları
        """
        
        if not self.genai_client:
            return {"success": False, "error": "Google GenAI mevcut değil"}
        
        try:
            prompt = f"""
            SEO uzmanı olarak "{topic}" konusu için kapsamlı anahtar kelime analizi yap.
            
            Aşağıdaki formatta JSON yanıt ver:
            {{
                "primary_keywords": ["anahtar kelime 1", "anahtar kelime 2"],
                "secondary_keywords": ["ikincil kelime 1", "ikincil kelime 2"],
                "long_tail_keywords": ["uzun kuyruklu kelime 1", "uzun kuyruklu kelime 2"],
                "lsi_keywords": ["LSI kelime 1", "LSI kelime 2"],
                "trending_keywords": ["trend kelime 1", "trend kelime 2"],
                "search_volume_analysis": {{
                    "high_volume": ["yüksek hacimli kelime"],
                    "medium_volume": ["orta hacimli kelime"],
                    "low_volume": ["düşük hacimli kelime"]
                }},
                "competition_analysis": {{
                    "low_competition": ["düşük rekabetli kelime"],
                    "medium_competition": ["orta rekabetli kelime"],
                    "high_competition": ["yüksek rekabetli kelime"]
                }},
                "intent_analysis": {{
                    "informational": ["bilgisel amaçlı"],
                    "commercial": ["ticari amaçlı"],
                    "transactional": ["işlemsel amaçlı"],
                    "navigational": ["navigasyon amaçlı"]
                }}
            }}
            
            Dil: {language}
            """
            
            response = await self.genai_client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            # JSON yanıtını parse et
            try:
                analysis_data = json.loads(response.text)
                return {
                    "success": True,
                    "topic": topic,
                    "language": language,
                    "analysis": analysis_data,
                    "generated_at": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "JSON parse hatası",
                    "raw_response": response.text
                }
                
        except Exception as e:
            logger.error(f"Anahtar kelime analizi hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def optimize_content(self, title: str, description: str, tags: List[str], 
                              target_keywords: List[str]) -> Dict[str, Any]:
        """
        İçeriği SEO optimizasyonu yap
        
        Args:
            title: Mevcut başlık
            description: Mevcut açıklama
            tags: Mevcut etiketler
            target_keywords: Hedef anahtar kelimeler
            
        Returns:
            SEO optimize edilmiş içerik
        """
        
        if not self.genai_client:
            return {"success": False, "error": "Google GenAI mevcut değil"}
        
        try:
            prompt = f"""
            YouTube SEO uzmanı olarak aşağıdaki içeriği optimize et:
            
            Mevcut Başlık: {title}
            Mevcut Açıklama: {description}
            Mevcut Etiketler: {', '.join(tags)}
            Hedef Anahtar Kelimeler: {', '.join(target_keywords)}
            
            Aşağıdaki formatta JSON yanıt ver:
            {{
                "optimized_title": "SEO optimize edilmiş başlık (max 60 karakter)",
                "optimized_description": "SEO optimize edilmiş açıklama (max 5000 karakter)",
                "optimized_tags": ["etiket1", "etiket2", "etiket3", ...],
                "seo_score": 85,
                "improvements": [
                    "Başlık iyileştirmesi 1",
                    "Açıklama iyileştirmesi 1"
                ],
                "keyword_density": {{
                    "primary": 2.5,
                    "secondary": 1.8,
                    "overall": 4.3
                }},
                "readability_score": 75,
                "engagement_prediction": 8.5
            }}
            
            YouTube SEO en iyi uygulamalarına uy:
            - Başlık 60 karakteri geçmemeli
            - Açıklama 5000 karakteri geçmemeli
            - En az 5 etiket olmalı
            - Anahtar kelimeler doğal olarak kullanılmalı
            - İzleyici dikkatini çekecek
            """
            
            response = await self.genai_client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    top_p=0.9,
                    top_k=32
                )
            )
            
            try:
                optimization_data = json.loads(response.text)
                return {
                    "success": True,
                    "original": {
                        "title": title,
                        "description": description,
                        "tags": tags
                    },
                    "optimized": optimization_data,
                    "target_keywords": target_keywords,
                    "optimized_at": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "JSON parse hatası",
                    "raw_response": response.text
                }
                
        except Exception as e:
            logger.error(f"İçerik optimizasyonu hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def analyze_competitors(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Rakipleri analiz et
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
            
        Returns:
            Rakip analizi sonuçları
        """
        
        if not self.youtube_service:
            return {"success": False, "error": "YouTube API mevcut değil"}
        
        try:
            # YouTube'da ara
            search_response = self.youtube_service.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                order='relevance'
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            # Video detaylarını al
            videos_response = self.youtube_service.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            competitor_analysis = []
            
            for video in videos_response['items']:
                snippet = video['snippet']
                stats = video['statistics']
                
                # SEO metriklerini hesapla
                title = snippet.get('title', '')
                description = snippet.get('description', '')
                tags = snippet.get('tags', [])
                
                # Başlık analizi
                title_length = len(title)
                title_has_keywords = any(keyword.lower() in title.lower() 
                                      for keyword in query.split())
                
                # Açıklama analizi
                desc_length = len(description)
                desc_has_keywords = any(keyword.lower() in description.lower() 
                                      for keyword in query.split())
                
                # Etiket analizi
                tag_count = len(tags)
                tags_have_keywords = any(any(keyword.lower() in tag.lower() 
                                           for keyword in query.split()) 
                                       for tag in tags)
                
                competitor_data = {
                    "video_id": video['id'],
                    "title": title,
                    "description": description[:200] + "..." if len(description) > 200 else description,
                    "channel": snippet.get('channelTitle', ''),
                    "published_at": snippet.get('publishedAt', ''),
                    "metrics": {
                        "views": int(stats.get('viewCount', 0)),
                        "likes": int(stats.get('likeCount', 0)),
                        "comments": int(stats.get('commentCount', 0)),
                        "duration": video['contentDetails'].get('duration', ''),
                        "engagement_rate": self._calculate_engagement_rate(stats)
                    },
                    "seo_analysis": {
                        "title_length": title_length,
                        "title_optimal": 30 <= title_length <= 60,
                        "title_has_keywords": title_has_keywords,
                        "description_length": desc_length,
                        "description_optimal": 100 <= desc_length <= 5000,
                        "description_has_keywords": desc_has_keywords,
                        "tag_count": tag_count,
                        "tags_optimal": 5 <= tag_count <= 15,
                        "tags_have_keywords": tags_have_keywords,
                        "seo_score": self._calculate_seo_score(title, description, tags, query)
                    }
                }
                
                competitor_analysis.append(competitor_data)
            
            # Sıralama analizini yap
            sorted_by_views = sorted(competitor_analysis, 
                                   key=lambda x: x['metrics']['views'], 
                                   reverse=True)
            
            sorted_by_seo = sorted(competitor_analysis, 
                                 key=lambda x: x['seo_analysis']['seo_score'], 
                                 reverse=True)
            
            return {
                "success": True,
                "query": query,
                "total_results": len(competitor_analysis),
                "competitors": competitor_analysis,
                "top_performers": sorted_by_views[:5],
                "best_seo": sorted_by_seo[:5],
                "analysis_summary": self._generate_competitor_summary(competitor_analysis),
                "analyzed_at": datetime.now().isoformat()
            }
            
        except HttpError as e:
            logger.error(f"YouTube API hatası: {e}")
            return {"success": False, "error": f"YouTube API hatası: {e}"}
        except Exception as e:
            logger.error(f"Rakip analizi hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_seo_strategy(self, niche: str, target_audience: str, 
                                  goals: List[str]) -> Dict[str, Any]:
        """
        SEO stratejisi oluştur
        
        Args:
            niche: Niş alan
            target_audience: Hedef kitle
            goals: Hedefler
            
        Returns:
            SEO stratejisi
        """
        
        if not self.genai_client:
            return {"success": False, "error": "Google GenAI mevcut değil"}
        
        try:
            prompt = f"""
            SEO stratejisti olarak "{niche}" nişi için kapsamlı strateji oluştur.
            
            Hedef Kitle: {target_audience}
            Hedefler: {', '.join(goals)}
            
            Aşağıdaki formatta JSON yanıt ver:
            {{
                "content_strategy": {{
                    "primary_topics": ["konu 1", "konu 2"],
                    "content_pillars": ["temel konu 1", "temel konu 2"],
                    "content_calendar": {{
                        "weekly": [
                            {{
                                "day": "Pazartesi",
                                "topic": "haftalık konu",
                                "content_type": "video/blog"
                            }}
                        ]
                    }}
                }},
                "keyword_strategy": {{
                    "primary_keywords": ["anahtar kelime 1"],
                    "secondary_keywords": ["ikincil kelime 1"],
                    "long_tail_opportunities": ["uzun kuyruk fırsat 1"],
                    "local_seo": ["yerel seo kelime 1"],
                    "seasonal_keywords": ["mevsimsel kelime 1"]
                }},
                "technical_seo": {{
                    "video_optimization": [
                        "video optimizasyon ipucu 1"
                    ],
                    "metadata_optimization": [
                        "metadata optimizasyon ipucu 1"
                    ],
                    "structured_data": [
                        "yapısal veri ipucu 1"
                    ]
                }},
                "promotion_strategy": {{
                    "social_media": ["sosyal medya stratejisi"],
                    "backlink_building": ["backlink stratejisi"],
                    "collaboration": ["işbirliği stratejisi"]
                }},
                "kpi_tracking": {{
                    "primary_metrics": ["izlenme", "abone artışı"],
                    "secondary_metrics": ["etkileşim oranı"],
                    "tools": ["Google Analytics", "YouTube Studio"]
                }},
                "timeline": {{
                    "month_1": ["ilk ay hedefleri"],
                    "month_3": ["3 ay hedefleri"],
                    "month_6": ["6 ay hedefleri"]
                }}
            }}
            
            """
            
            response = await self.genai_client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    top_p=0.9,
                    top_k=40
                )
            )
            
            try:
                strategy_data = json.loads(response.text)
                return {
                    "success": True,
                    "niche": niche,
                    "target_audience": target_audience,
                    "goals": goals,
                    "strategy": strategy_data,
                    "generated_at": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "JSON parse hatası",
                    "raw_response": response.text
                }
                
        except Exception as e:
            logger.error(f"SEO stratejisi oluşturma hatası: {e}")
            return {"success": False, "error": str(e)}
    
    async def track_rankings(self, keywords: List[str], url: str = None) -> Dict[str, Any]:
        """
        Sıralamaları takip et
        
        Args:
            keywords: Takip edilecek anahtar kelimeler
            url: İzlenecek URL
            
        Returns:
            Sıralama takip sonuçları
        """
        
        # Bu metod Google Search API kullanarak sıralamaları takip eder
        # Şimdilik simüle edilmiş sonuçlar
        
        try:
            ranking_data = {}
            
            for keyword in keywords:
                # Simüle edilmiş sıralama verisi
                ranking_data[keyword] = {
                    "current_rank": 15,
                    "previous_rank": 18,
                    "change": "+3",
                    "url": url or f"https://example.com/{keyword.replace(' ', '-')}",
                    "search_volume": "1000-10000",
                    "competition": "medium",
                    "difficulty": 45,
                    "opportunity": 78,
                    "last_checked": datetime.now().isoformat()
                }
            
            return {
                "success": True,
                "keywords": keywords,
                "rankings": ranking_data,
                "summary": {
                    "average_rank": sum(data["current_rank"] for data in ranking_data.values()) / len(ranking_data),
                    "improving_keywords": len([data for data in ranking_data.values() if data["change"].startswith("+")]),
                    "declining_keywords": len([data for data in ranking_data.values() if data["change"].startswith("-")])
                },
                "tracked_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Sıralama takibi hatası: {e}")
            return {"success": False, "error": str(e)}
    
    def _calculate_engagement_rate(self, stats: Dict[str, str]) -> float:
        """Etkileşim oranını hesapla"""
        try:
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            
            if views == 0:
                return 0.0
            
            engagement = ((likes + comments) / views) * 100
            return round(engagement, 2)
        except:
            return 0.0
    
    def _calculate_seo_score(self, title: str, description: str, 
                           tags: List[str], query: str) -> int:
        """SEO skorunu hesapla"""
        score = 0
        
        # Başlık optimizasyonu (30 puan)
        if 30 <= len(title) <= 60:
            score += 15
        if any(keyword.lower() in title.lower() for keyword in query.split()):
            score += 15
        
        # Açıklama optimizasyonu (25 puan)
        if 100 <= len(description) <= 5000:
            score += 10
        if any(keyword.lower() in description.lower() for keyword in query.split()):
            score += 15
        
        # Etiket optimizasyonu (25 puan)
        if 5 <= len(tags) <= 15:
            score += 10
        if any(any(keyword.lower() in tag.lower() for keyword in query.split()) for tag in tags):
            score += 15
        
        # Genel optimizasyon (20 puan)
        if title and description and tags:
            score += 20
        
        return min(score, 100)
    
    def _generate_competitor_summary(self, competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rakip analizi özeti oluştur"""
        if not competitors:
            return {}
        
        total_views = sum(c['metrics']['views'] for c in competitors)
        avg_seo_score = sum(c['seo_analysis']['seo_score'] for c in competitors) / len(competitors)
        
        optimal_titles = len([c for c in competitors if c['seo_analysis']['title_optimal']])
        optimal_descriptions = len([c for c in competitors if c['seo_analysis']['description_optimal']])
        optimal_tags = len([c for c in competitors if c['seo_analysis']['tags_optimal']])
        
        return {
            "total_views": total_views,
            "average_views": total_views // len(competitors),
            "average_seo_score": round(avg_seo_score, 1),
            "optimization_rates": {
                "title_optimal": round((optimal_titles / len(competitors)) * 100, 1),
                "description_optimal": round((optimal_descriptions / len(competitors)) * 100, 1),
                "tags_optimal": round((optimal_tags / len(competitors)) * 100, 1)
            },
            "top_performer": max(competitors, key=lambda x: x['metrics']['views'])['title'],
            "best_seo": max(competitors, key=lambda x: x['seo_analysis']['seo_score'])['title']
        }

# Global instance
google_seo_service = GoogleSEOService()
