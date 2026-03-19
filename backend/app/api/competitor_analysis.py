"""
VUC-2026 Competitor Analysis API
YouTube rakip analizi için endpoint'ler
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import os
from datetime import datetime

from ..database import get_db
from ..services.competitor_analysis_service import CompetitorAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()

class CompetitorAnalysisRequest(BaseModel):
    channel_url: str
    analysis_depth: str = "basic"  # basic, detailed, comprehensive
    include_video_analysis: bool = True
    include_thumbnail_analysis: bool = True

class ContentOpportunityRequest(BaseModel):
    niche: str
    competitor_channels: List[str] = []
    analysis_period_days: int = 30
    min_demand_score: float = 7.0

@router.post("/analyze")
async def analyze_competitor(
    request: CompetitorAnalysisRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Rakip kanal analiz et"""
    try:
        # YouTube API anahtarını al
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not youtube_api_key:
            youtube_api_key = os.getenv("GOOGLE_AI_API_KEY")  # Fallback
        
        if not youtube_api_key:
            raise HTTPException(status_code=500, detail="YouTube API anahtarı bulunamadı")
        
        # Analiz servisini başlat
        analysis_service = CompetitorAnalysisService(youtube_api_key)
        
        # Rakibi analiz et
        result = await analysis_service.analyze_competitor(request.channel_url)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Analiz başarısız"))
        
        return {
            "success": True,
            "analysis": result,
            "request_info": {
                "channel_url": request.channel_url,
                "analysis_depth": request.analysis_depth,
                "analyzed_at": datetime.utcnow().isoformat()
            },
            "message": "Rakip analizi başarıyla tamamlandı"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Competitor analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/opportunities")
async def find_content_opportunities(
    request: ContentOpportunityRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """İçerik fırsatlarını bul"""
    try:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_AI_API_KEY")
        
        if not youtube_api_key:
            raise HTTPException(status_code=500, detail="API anahtarı bulunamadı")
        
        analysis_service = CompetitorAnalysisService(youtube_api_key)
        
        # Fırsatları bul
        opportunities = await analysis_service.find_content_opportunities(
            request.niche, 
            request.competitor_channels
        )
        
        # Min skor filtrelemesi
        filtered_opportunities = [
            opp for opp in opportunities 
            if opp.demand_score >= request.min_demand_score
        ]
        
        return {
            "success": True,
            "opportunities": [
                {
                    "topic": opp.topic,
                    "demand_score": opp.demand_score,
                    "competition_level": opp.competition_level,
                    "estimated_views": opp.estimated_views,
                    "difficulty_score": opp.difficulty_score,
                    "content_angle": opp.content_angle,
                    "target_keywords": opp.target_keywords,
                    "best_upload_time": opp.best_upload_time,
                    "thumbnail_style": opp.thumbnail_style
                }
                for opp in filtered_opportunities
            ],
            "total_opportunities": len(filtered_opportunities),
            "niche": request.niche,
            "analysis_date": datetime.utcnow().isoformat(),
            "message": f"{request.niche} nişi için {len(filtered_opportunities)} içerik fırsatı bulundu"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content opportunities error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending/{niche}")
async def get_niche_trends(niche: str) -> Dict[str, Any]:
    """Niş trendlerini getir"""
    try:
        # Mock trend data
        trends = {
            "teknoloji": [
                {"topic": "Yapay Zeka", "score": 9.5, "growth": "+250%", "difficulty": 8.2},
                {"topic": "5G Teknolojisi", "score": 8.8, "growth": "+180%", "difficulty": 7.5},
                {"topic": "Siber Güvenlik", "score": 8.2, "growth": "+150%", "difficulty": 6.8},
                {"topic": "Blockchain", "score": 7.9, "growth": "+120%", "difficulty": 7.9},
                {"topic": "Oyun Teknolojileri", "score": 7.5, "growth": "+95%", "difficulty": 6.2}
            ],
            "eğitim": [
                {"topic": "Online Eğitim", "score": 9.2, "growth": "+200%", "difficulty": 7.8},
                {"topic": "Dil Öğrenme", "score": 8.5, "growth": "+160%", "difficulty": 6.5},
                {"topic": "Mesleki Gelişim", "score": 8.1, "growth": "+140%", "difficulty": 7.2},
                {"topic": "Sınav Taktikleri", "score": 7.8, "growth": "+110%", "difficulty": 5.9},
                {"topic": "Etüt Teknikleri", "score": 7.3, "growth": "+85%", "difficulty": 5.2}
            ],
            "finans": [
                {"topic": "Kripto Para", "score": 9.1, "growth": "+300%", "difficulty": 8.5},
                {"topic": "Yatırım Stratejileri", "score": 8.7, "growth": "+190%", "difficulty": 7.6},
                {"topic": "Kişisel Finans", "score": 8.3, "growth": "+170%", "difficulty": 6.8},
                {"topic": "Borsa Analizi", "score": 7.9, "growth": "+130%", "difficulty": 7.9},
                {"topic": "Girişimcilik", "score": 7.6, "growth": "+100%", "difficulty": 7.1}
            ]
        }
        
        niche_trends = trends.get(niche.lower(), [
            {"topic": f"{niche} Genel", "score": 7.0, "growth": "+50%", "difficulty": 6.0}
        ])
        
        return {
            "success": True,
            "niche": niche,
            "trends": niche_trends,
            "total_trends": len(niche_trends),
            "analysis_date": datetime.utcnow().isoformat(),
            "message": f"{niche} nişi trendleri başarıyla alındı"
        }
        
    except Exception as e:
        logger.error(f"Niche trends error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comparison")
async def compare_channels(channel_urls: List[str] = None) -> Dict[str, Any]:
    """Birden fazla kanalı karşılaştır"""
    try:
        if not channel_urls or len(channel_urls) < 2:
            raise HTTPException(status_code=400, detail="En az 2 kanal URL'i gerekli")
        
        # Mock comparison data
        comparison_data = []
        
        for i, url in enumerate(channel_urls):
            mock_channel = {
                "channel_url": url,
                "channel_name": f"Kanal {i+1}",
                "subscriber_count": 50000 * (i+1),
                "avg_views": 25000 * (i+1),
                "upload_frequency": 2.5 * (i+1),
                "engagement_rate": 0.05 * (i+1),
                "content_quality_score": 7.0 + (i * 0.5),
                "strengths": [f"Güçlü yön {i+1}", "Özellik 2"],
                "weaknesses": ["Zayıf yön 1", "Geliştirilebilir alan"],
                "rank": i + 1
            }
            comparison_data.append(mock_channel)
        
        # Sıralama yap
        comparison_data.sort(key=lambda x: x["subscriber_count"], reverse=True)
        
        # Rank güncelle
        for i, channel in enumerate(comparison_data):
            channel["rank"] = i + 1
        
        return {
            "success": True,
            "comparison": comparison_data,
            "total_channels": len(comparison_data),
            "analysis_date": datetime.utcnow().isoformat(),
            "message": f"{len(channel_urls)} kanal başarıla karşılaştırıldı"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Channel comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gap-analysis/{niche}")
async def analyze_content_gaps(niche: str) -> Dict[str, Any]:
    """İçerik boşluk analizi"""
    try:
        # Mock gap analysis
        content_gaps = {
            "untapped_topics": [
                {
                    "topic": f"{niche} için İleri Seviye İpuçları",
                    "demand_score": 8.5,
                    "competition_level": "düşük",
                    "estimated_views": 95000,
                    "content_angle": "Uzman seviye içerik"
                },
                {
                    "topic": f"{niche} Hataları ve Çözümleri",
                    "demand_score": 9.1,
                    "competition_level": "orta",
                    "estimated_views": 120000,
                    "content_angle": "Problem çözüm odaklı"
                },
                {
                    "topic": f"{niche} Trendleri 2024",
                    "demand_score": 8.8,
                    "competition_level": "yüksek",
                    "estimated_views": 150000,
                    "content_angle": "Gelecek odaklı analiz"
                }
            ],
            "oversaturated_topics": [
                {
                    "topic": f"{niche} Temel Bilgiler",
                    "saturation_level": 0.85,
                    "difficulty_score": 9.2,
                    "recommendation": "Kaçın veya çok özel bir açı bulun"
                },
                {
                    "topic": f"{niche} Genel Bakış",
                    "saturation_level": 0.78,
                    "difficulty_score": 8.5,
                    "recommendation": "Spesifik alt konulara odaklanın"
                }
            ],
            "seasonal_opportunities": [
                {
                    "topic": f"{niche} Yıl Sonu İncelemesi",
                    "best_time": "Aralık",
                    "demand_multiplier": 1.8,
                    "content_angle": "Özet ve gelecek tahminleri"
                },
                {
                    "topic": f"{niche} Yaz Trendleri",
                    "best_time": "Haziran-Temmuz",
                    "demand_multiplier": 1.4,
                    "content_angle": "Sezonluk özel içerik"
                }
            ]
        }
        
        return {
            "success": True,
            "niche": niche,
            "gap_analysis": content_gaps,
            "total_opportunities": len(content_gaps["untapped_topics"]),
            "analysis_date": datetime.utcnow().isoformat(),
            "message": f"{niche} için içerik boşluk analizi tamamlandı"
        }
        
    except Exception as e:
        logger.error(f"Content gap analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/thumbnail-analysis")
async def analyze_thumbnail_trends() -> Dict[str, Any]:
    """Thumbnail trendlerini analiz et"""
    try:
        # Mock thumbnail analysis
        thumbnail_trends = {
            "effective_styles": [
                {
                    "style": "Yüz Odaklı Şok İfadesi",
                    "effectiveness_score": 8.9,
                    "usage_percentage": 65,
                    "best_for": ["reaksiyon", "şok edici içerik"]
                },
                {
                    "style": "Büyük Kontrastlı Metin",
                    "effectiveness_score": 8.5,
                    "usage_percentage": 78,
                    "best_for": ["listicle", "nasıl yapılır"]
                },
                {
                    "style": "Karşılaştırma Split Screen",
                    "effectiveness_score": 8.2,
                    "usage_percentage": 45,
                    "best_for": ["karşılaştırma", "test"]
                }
            ],
            "color_trends": {
                "high_contrast": {"red_yellow": 0.85, "blue_white": 0.72},
                "emotional": {"orange_black": 0.78, "purple_pink": 0.68}
            },
            "text_patterns": [
                {"pattern": "Soru Formatı", "ctr_boost": "+25%"},
                {"pattern": "Sayı Kullanımı", "ctr_boost": "+18%"},
                {"pattern": "Şok Kelimeleri", "ctr_boost": "+32%"}
            ],
            "recommendations": [
                "Yüz ifadeleri ile duygusal bağ kurun",
                "Kontrast renkler kullanın",
                "Metin okunabilirliğini önceliklendirin",
                "Mobil görünürlüğü test edin"
            ]
        }
        
        return {
            "success": True,
            "thumbnail_trends": thumbnail_trends,
            "analysis_date": datetime.utcnow().isoformat(),
            "message": "Thumbnail trend analizi tamamlandı"
        }
        
    except Exception as e:
        logger.error(f"Thumbnail analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
