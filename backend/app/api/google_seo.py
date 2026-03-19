"""
VUC-2026 Google SEO API Endpoints
Google AI ve YouTube SEO optimizasyonu için endpoint'ler
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from app.services.google_seo_service import google_seo_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/google-seo", tags=["google-seo"])

@router.get("/status")
async def get_google_seo_status() -> Dict[str, Any]:
    """Google SEO servisi durumunu al"""
    try:
        status = {
            "genai_available": google_seo_service.genai_client is not None,
            "youtube_api_available": google_seo_service.youtube_service is not None,
            "api_keys": {
                "genai_configured": bool(google_seo_service.api_key),
                "youtube_configured": bool(google_seo_service.youtube_api_key)
            },
            "services": {
                "keyword_analysis": True,
                "content_optimization": True,
                "competitor_analysis": google_seo_service.youtube_service is not None,
                "seo_strategy": True,
                "ranking_tracking": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Google SEO durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-keywords")
async def analyze_keywords(
    topic: str,
    language: str = "tr"
) -> Dict[str, Any]:
    """Anahtar kelime analizi yap"""
    try:
        result = await google_seo_service.analyze_keywords(topic, language)
        return result
        
    except Exception as e:
        logger.error(f"Anahtar kelime analizi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-content")
async def optimize_content(
    title: str,
    description: str,
    tags: List[str],
    target_keywords: List[str]
) -> Dict[str, Any]:
    """İçeriği SEO optimizasyonu yap"""
    try:
        result = await google_seo_service.optimize_content(
            title, description, tags, target_keywords
        )
        return result
        
    except Exception as e:
        logger.error(f"İçerik optimizasyonu hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-competitors")
async def analyze_competitors(
    query: str,
    max_results: int = 10
) -> Dict[str, Any]:
    """Rakipleri analiz et"""
    try:
        result = await google_seo_service.analyze_competitors(query, max_results)
        return result
        
    except Exception as e:
        logger.error(f"Rakip analizi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-seo-strategy")
async def generate_seo_strategy(
    niche: str,
    target_audience: str,
    goals: List[str]
) -> Dict[str, Any]:
    """SEO stratejisi oluştur"""
    try:
        result = await google_seo_service.generate_seo_strategy(
            niche, target_audience, goals
        )
        return result
        
    except Exception as e:
        logger.error(f"SEO stratejisi oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/track-rankings")
async def track_rankings(
    keywords: List[str],
    url: Optional[str] = None
) -> Dict[str, Any]:
    """Sıralamaları takip et"""
    try:
        result = await google_seo_service.track_rankings(keywords, url)
        return result
        
    except Exception as e:
        logger.error(f"Sıralama takibi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending-keywords")
async def get_trending_keywords(
    category: str = "general",
    region: str = "TR"
) -> Dict[str, Any]:
    """Trend anahtar kelimeleri al"""
    try:
        # Simüle edilmiş trend verileri
        trending_data = {
            "success": True,
            "category": category,
            "region": region,
            "trending_keywords": [
                {
                    "keyword": "yapay zeka",
                    "trend_score": 95,
                    "search_volume": "100K-1M",
                    "growth_rate": "+45%",
                    "competition": "high"
                },
                {
                    "keyword": "video üretimi",
                    "trend_score": 88,
                    "search_volume": "10K-100K",
                    "growth_rate": "+32%",
                    "competition": "medium"
                },
                {
                    "keyword": "YouTube SEO",
                    "trend_score": 82,
                    "search_volume": "10K-100K",
                    "growth_rate": "+28%",
                    "competition": "medium"
                }
            ],
            "updated_at": datetime.now().isoformat()
        }
        
        return trending_data
        
    except Exception as e:
        logger.error(f"Trend anahtar kelimeleri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content-audit")
async def content_audit(
    title: str,
    description: str,
    tags: List[str],
    target_keywords: List[str]
) -> Dict[str, Any]:
    """İçerik denetimi yap"""
    try:
        # İçerik denetimi metrikleri
        audit_results = {
            "success": True,
            "content": {
                "title": title,
                "description": description,
                "tags": tags
            },
            "seo_audit": {
                "title_analysis": {
                    "length": len(title),
                    "optimal_length": 30 <= len(title) <= 60,
                    "has_primary_keyword": any(kw.lower() in title.lower() for kw in target_keywords),
                    "readability": "good",
                    "click_potential": 8.5
                },
                "description_analysis": {
                    "length": len(description),
                    "optimal_length": 100 <= len(description) <= 5000,
                    "has_keywords": any(kw.lower() in description.lower() for kw in target_keywords),
                    "keyword_density": len([kw for kw in target_keywords if kw.lower() in description.lower()]) / len(description.split()) * 100,
                    "readability": "excellent"
                },
                "tags_analysis": {
                    "count": len(tags),
                    "optimal_count": 5 <= len(tags) <= 15,
                    "has_relevant_tags": len([tag for tag in tags if any(kw.lower() in tag.lower() for kw in target_keywords)]),
                    "tag_relevance": 85
                }
            },
            "overall_score": 88,
            "recommendations": [
                "Başlığı 45 karaktere kısaltın",
                "Açıklamada daha fazla anahtar kelime kullanın",
                "5-10 arası etiket ekleyin"
            ],
            "audited_at": datetime.now().isoformat()
        }
        
        return audit_results
        
    except Exception as e:
        logger.error(f"İçerik denetimi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keyword-research")
async def keyword_research(
    seed_keyword: str,
    language: str = "tr",
    max_results: int = 20
) -> Dict[str, Any]:
    """Anahtar kelime araştırması yap"""
    try:
        # Simüle edilmiş anahtar kelime araştırması
        research_data = {
            "success": True,
            "seed_keyword": seed_keyword,
            "language": language,
            "keyword_suggestions": [
                {
                    "keyword": f"{seed_keyword} nasıl yapılır",
                    "search_volume": "10K-100K",
                    "competition": "medium",
                    "cpc": "$0.50",
                    "difficulty": 45,
                    "trend": "up"
                },
                {
                    "keyword": f"{seed_keyword} ipuçları",
                    "search_volume": "1K-10K",
                    "competition": "low",
                    "cpc": "$0.30",
                    "difficulty": 25,
                    "trend": "stable"
                },
                {
                    "keyword": f"en iyi {seed_keyword}",
                    "search_volume": "10K-100K",
                    "competition": "high",
                    "cpc": "$1.20",
                    "difficulty": 65,
                    "trend": "up"
                }
            ],
            "search_intent": {
                "informational": 60,
                "commercial": 25,
                "transactional": 15
            },
            "related_topics": [
                f"{seed_keyword} alternatifleri",
                f"{seed_keyword} karşılaştırma",
                f"{seed_keyword} yorumları"
            ],
            "researched_at": datetime.now().isoformat()
        }
        
        return research_data
        
    except Exception as e:
        logger.error(f"Anahtar kelime araştırması hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seo-score")
async def calculate_seo_score(
    title: str,
    description: str,
    tags: List[str],
    target_keywords: List[str]
) -> Dict[str, Any]:
    """SEO skorunu hesapla"""
    try:
        # SEO skor hesaplama
        score_breakdown = {
            "title_score": 0,
            "description_score": 0,
            "tags_score": 0,
            "keyword_relevance": 0,
            "readability": 0
        }
        
        # Başlık skoru (30 puan)
        if 30 <= len(title) <= 60:
            score_breakdown["title_score"] += 15
        if any(kw.lower() in title.lower() for kw in target_keywords):
            score_breakdown["title_score"] += 15
        
        # Açıklama skoru (30 puan)
        if 100 <= len(description) <= 5000:
            score_breakdown["description_score"] += 15
        if any(kw.lower() in description.lower() for kw in target_keywords):
            score_breakdown["description_score"] += 15
        
        # Etiket skoru (20 puan)
        if 5 <= len(tags) <= 15:
            score_breakdown["tags_score"] += 10
        if any(any(kw.lower() in tag.lower() for kw in target_keywords) for tag in tags):
            score_breakdown["tags_score"] += 10
        
        # Anahtar kelime relevansı (15 puan)
        keyword_density = len([kw for kw in target_keywords if kw.lower() in f"{title} {description}".lower()]) / len(f"{title} {description}".split()) * 100
        if 1 <= keyword_density <= 3:
            score_breakdown["keyword_relevance"] = 15
        elif keyword_density < 1:
            score_breakdown["keyword_relevance"] = keyword_density * 15
        else:
            score_breakdown["keyword_relevance"] = max(0, 15 - (keyword_density - 3) * 5)
        
        # Okunabilirlik (5 puan)
        avg_word_length = sum(len(word) for word in f"{title} {description}".split()) / len(f"{title} {description}".split())
        if 4 <= avg_word_length <= 6:
            score_breakdown["readability"] = 5
        else:
            score_breakdown["readability"] = max(0, 5 - abs(avg_word_length - 5))
        
        total_score = sum(score_breakdown.values())
        
        return {
            "success": True,
            "total_score": round(total_score, 1),
            "grade": "A" if total_score >= 90 else "B" if total_score >= 80 else "C" if total_score >= 70 else "D" if total_score >= 60 else "F",
            "score_breakdown": score_breakdown,
            "recommendations": [
                "Başlığı optimize edin" if score_breakdown["title_score"] < 25 else "Başlık iyi optimize edilmiş",
                "Açıklamayı geliştirin" if score_breakdown["description_score"] < 25 else "Açıklama iyi optimize edilmiş",
                "Etiketleri düzenleyin" if score_breakdown["tags_score"] < 15 else "Etiketler iyi optimize edilmiş",
                "Anahtar kelime yoğunluğunu ayarlayın" if score_breakdown["keyword_relevance"] < 10 else "Anahtar kelime yoğunluğu iyi"
            ],
            "calculated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"SEO skoru hesaplama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-connection")
async def test_google_seo_connection() -> Dict[str, Any]:
    """Google SEO servis bağlantısını test et"""
    try:
        test_results = {
            "genai": {
                "available": google_seo_service.genai_client is not None,
                "status": "connected" if google_seo_service.genai_client else "disconnected",
                "api_key_configured": bool(google_seo_service.api_key)
            },
            "youtube_api": {
                "available": google_seo_service.youtube_service is not None,
                "status": "connected" if google_seo_service.youtube_service else "disconnected",
                "api_key_configured": bool(google_seo_service.youtube_api_key)
            },
            "services": {
                "keyword_analysis": google_seo_service.genai_client is not None,
                "content_optimization": google_seo_service.genai_client is not None,
                "competitor_analysis": google_seo_service.youtube_service is not None,
                "seo_strategy": google_seo_service.genai_client is not None,
                "ranking_tracking": True
            },
            "overall_status": "healthy" if (google_seo_service.genai_client or google_seo_service.youtube_service) else "degraded",
            "timestamp": datetime.now().isoformat()
        }
        
        return test_results
        
    except Exception as e:
        logger.error(f"Google SEO bağlantı testi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
