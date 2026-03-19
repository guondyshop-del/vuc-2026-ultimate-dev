"""
VUC-2026 Baby Content API Routes
YouTube Kids bebek içeriği yönetimi için API endpoint'leri
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.baby_content_service import BabyContentService
from app.core.ai_intelligence import AIIntelligence

router = APIRouter(prefix="/api/baby-content", tags=["baby-content"])
baby_service = BabyContentService()
ai_intelligence = AIIntelligence()

class BabyContentRequest(BaseModel):
    story_type: str
    character: str
    theme: str
    language: str = "tr"
    duration: int = 900  # 15 dakika

class BabyContentResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str
    timestamp: datetime

@router.post("/generate", response_model=BabyContentResponse)
async def generate_baby_content(request: BabyContentRequest):
    """
    Yeni bebek içeriği oluştur
    """
    try:
        # İçerik üretim planı oluştur
        content_plan = await baby_service.produce_baby_video(
            story_type=request.story_type,
            character=request.character,
            theme=request.theme,
            language=request.language,
            duration=request.duration
        )
        
        # Analytics'e kaydet
        await ai_intelligence.log_content_generation(
            content_type="baby_video",
            parameters=request.dict(),
            result=content_plan
        )
        
        return BabyContentResponse(
            success=True,
            data=content_plan,
            message="Bebek içeriği başarıyla oluşturuldu",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"İçerik oluşturulamadı: {str(e)}"
        )

@router.get("/ideas", response_model=BabyContentResponse)
async def get_baby_content_ideas(limit: int = 20):
    """
    Bebek içerik fikirleri getir
    """
    try:
        ideas = await baby_service.get_baby_content_ideas(limit)
        
        return BabyContentResponse(
            success=True,
            data={"ideas": ideas, "total": len(ideas)},
            message=f"{len(ideas)} içerik fikri bulundu",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fikirler getirilemedi: {str(e)}"
        )

@router.get("/templates", response_model=BabyContentResponse)
async def get_content_templates():
    """
    Mevcut içerik şablonlarını getir
    """
    try:
        templates = {
            "story_types": baby_service.story_templates,
            "characters": baby_service.characters,
            "themes": baby_service.educational_themes,
            "languages": baby_service.languages
        }
        
        return BabyContentResponse(
            success=True,
            data=templates,
            message="İçerik şablonları getirildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Şablonlar getirilemedi: {str(e)}"
        )

@router.post("/schedule", response_model=BabyContentResponse)
async def create_content_schedule(
    daily_count: int = 3,
    upload_times: Optional[List[str]] = None
):
    """
    Bebek içerik takvimi oluştur
    """
    try:
        if upload_times is None:
            upload_times = ["09:00", "15:00", "20:00"]
            
        schedule = await baby_service.schedule_baby_content(
            daily_count=daily_count,
            upload_times=upload_times
        )
        
        # Analytics'e kaydet
        await ai_intelligence.log_schedule_creation(
            content_type="baby_content",
            schedule=schedule
        )
        
        return BabyContentResponse(
            success=True,
            data={"schedule": schedule, "total_videos": len(schedule)},
            message=f"{len(schedule)} videoluk takvim oluşturuldu",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Takvim oluşturulamadı: {str(e)}"
        )

@router.get("/analytics", response_model=BabyContentResponse)
async def get_baby_content_analytics():
    """
    Bebek içeriği analitik verileri
    """
    try:
        # Analytics Vault'tan bebek içerik verilerini çek
        analytics_data = await ai_intelligence.get_niche_analytics("baby")
        
        return BabyContentResponse(
            success=True,
            data=analytics_data,
            message="Bebek içeriği analitik verileri getirildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analitik veriler getirilemedi: {str(e)}"
        )

@router.post("/optimize", response_model=BabyContentResponse)
async def optimize_baby_content():
    """
    Bebek içeriği stratejilerini optimize et
    """
    try:
        # AI ile optimizasyon önerileri oluştur
        optimization_report = await ai_intelligence.optimize_content_strategy(
            niche="baby",
            target_metrics=["views", "engagement", "revenue"]
        )
        
        return BabyContentResponse(
            success=True,
            data=optimization_report,
            message="İçerik stratejisi optimize edildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimizasyon yapılamadı: {str(e)}"
        )

@router.get("/characters", response_model=BabyContentResponse)
async def get_characters():
    """
    Mevcut karakterleri getir
    """
    try:
        return BabyContentResponse(
            success=True,
            data=baby_service.characters,
            message="Karakterler getirildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Karakterler getirilemedi: {str(e)}"
        )

@router.get("/themes", response_model=BabyContentResponse)
async def get_themes():
    """
    Mevcut temaları getir
    """
    try:
        return BabyContentResponse(
            success=True,
            data=baby_service.educational_themes,
            message="Temalar getirildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Temalar getirilemedi: {str(e)}"
        )

@router.post("/batch-generate", response_model=BabyContentResponse)
async def batch_generate_baby_content(
    background_tasks: BackgroundTasks,
    count: int = 10,
    auto_schedule: bool = True
):
    """
    Toplu bebek içeriği oluştur
    """
    try:
        # Fikirleri getir
        ideas = await baby_service.get_baby_content_ideas(count)
        
        generated_content = []
        
        for idea in ideas:
            try:
                content_plan = await baby_service.produce_baby_video(
                    story_type=idea["story_type"],
                    character=idea["character"],
                    theme=idea["theme"],
                    language=idea["language"],
                    duration=idea["estimated_duration"]
                )
                generated_content.append(content_plan)
                
            except Exception as e:
                # Hatalı içeriği logla ama devam et
                print(f"İçerik oluşturma hatası: {e}")
                continue
        
        # Otomatik takvim oluştur
        if auto_schedule and generated_content:
            background_tasks.add_task(
                baby_service.schedule_baby_content,
                daily_count=3,
                upload_times=["09:00", "15:00", "20:00"]
            )
        
        return BabyContentResponse(
            success=True,
            data={
                "generated_count": len(generated_content),
                "content": generated_content,
                "auto_scheduled": auto_schedule
            },
            message=f"{len(generated_content)} içerik toplu olarak oluşturuldu",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Toplu oluşturulamadı: {str(e)}"
        )

@router.get("/performance", response_model=BabyContentResponse)
async def get_baby_content_performance():
    """
    Bebek içeriği performans metrikleri
    """
    try:
        # Performans verilerini Analytics Vault'tan çek
        performance_data = await ai_intelligence.get_performance_metrics(
            content_type="baby",
            time_range="30_days"
        )
        
        return BabyContentResponse(
            success=True,
            data=performance_data,
            message="Performans verileri getirildi",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Performans verileri getirilemedi: {str(e)}"
        )
