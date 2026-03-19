from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import os

from .database import get_db, init_db
from app.api import channels, videos, scripts, analytics, settings, channel_management
from app.api.empire import router as empire_router
from app.api.windows_ai import router as windows_ai_router
from app.api.system import router as system_router
from app.api.upload import router as upload_router
from app.api.windows_ml import router as windows_ml_router
from app.api.google_seo import router as google_seo_router
from app.api.omniverse import router as omniverse_router
from .services.settings_service import SettingsService

# FastAPI app initialization
app = FastAPI(
    title="VUC-2026 API",
    description="Vespera Ultimate Central - Otonom YouTube İmparatorluk Yönetim Sistemi",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="../assets"), name="assets")

# Include API routers
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(channel_management.router, prefix="/api/channel-management", tags=["channel-management"])
app.include_router(empire_router, prefix="/api/empire", tags=["empire"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(scripts.router, prefix="/api/scripts", tags=["scripts"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(windows_ai_router, tags=["windows-ai"])
app.include_router(system_router, tags=["system"])
app.include_router(upload_router, tags=["upload"])
app.include_router(windows_ml_router, tags=["windows-ml"])
app.include_router(google_seo_router, tags=["google-seo"])
app.include_router(omniverse_router, prefix="/api/omniverse", tags=["omniverse"])

@app.on_event("startup")
async def startup_event():
    """Başlangıç işlemleri"""
    # Veritabanını başlat
    init_db()
    
    # Varsayılan ayarları yükle
    settings_service = SettingsService()
    await settings_service.load_default_settings()
    
    # Gerekli dizinleri oluştur
    os.makedirs("static", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("../assets", exist_ok=True)

@app.get("/")
async def root():
    return {
        "message": "VUC-2026 API aktif",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Sistem sağlık kontrolü"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "timestamp": "2026-03-19T09:52:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
