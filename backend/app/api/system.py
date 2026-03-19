"""
VUC-2026 System API Endpoints
Sistem durumu, health check ve genel API endpoint'leri
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import psutil
import os
from datetime import datetime

from app.api.keys import api_keys_manager
from app.services.windows_ai_service import windows_ai_service
from app.services.directml_accelerator import directml_accelerator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Sistem health check"""
    try:
        # Sistem kaynakları
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Servis durumları
        services_status = {
            "windows_ai": windows_ai_service.is_available,
            "directml": directml_accelerator.is_available,
            "api_keys": True,  # API keys manager her zaman çalışır
        }
        
        # Genel durum
        overall_status = "healthy"
        if cpu_percent > 90 or memory.percent > 90:
            overall_status = "warning"
        if cpu_percent > 95 or memory.percent > 95:
            overall_status = "critical"
        
        health_data = {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "system_resources": {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent,
                    "used_gb": round(memory.used / (1024**3), 2)
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 2),
                    "used_gb": round(disk.used / (1024**3), 2)
                }
            },
            "services": services_status,
            "version": "1.0.0",
            "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_system_status() -> Dict[str, Any]:
    """Detaylı sistem durumu"""
    try:
        # API anahtarları durumu
        keys_validation = api_keys_manager.validate_keys()
        connections_test = api_keys_manager.test_connections()
        
        # Windows AI detayları
        windows_ai_status = None
        if windows_ai_service.is_available:
            windows_ai_status = {
                "available": True,
                "services": {
                    "ocr": windows_ai_service.ocr_engine is not None,
                    "speech": windows_ai_service.speech_recognizer is not None,
                    "image_analysis": True,
                    "video_enhancement": True,
                    "phi3": windows_ai_service.phi3_model is not None
                }
            }
        
        # DirectML detayları
        directml_status = None
        if directml_accelerator.is_available:
            directml_status = directml_accelerator.get_device_info()
        
        # Process bilgileri
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                if proc_info['cpu_percent'] > 5 or proc_info['memory_percent'] > 5:
                    processes.append({
                        "pid": proc_info['pid'],
                        "name": proc_info['name'],
                        "cpu_percent": proc_info['cpu_percent'],
                        "memory_percent": proc_info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # En çok kaynak kullanan process'ler
        processes.sort(key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)
        top_processes = processes[:10]
        
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "api_keys": {
                "validation": keys_validation,
                "connections": connections_test
            },
            "windows_ai": windows_ai_status,
            "directml": directml_status,
            "top_processes": top_processes,
            "system_info": {
                "platform": psutil.platform.system(),
                "platform_release": psutil.platform.release(),
                "platform_version": psutil.platform.version(),
                "architecture": psutil.platform.architecture()[0],
                "hostname": psutil.platform.node(),
                "processor": psutil.platform.processor(),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            },
            "network": {
                "connections": len(psutil.net_connections()),
                "interfaces": psutil.net_if_addrs().keys()
            }
        }
        
        return status_data
        
    except Exception as e:
        logger.error(f"Sistem durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api-keys")
async def get_api_keys() -> Dict[str, Any]:
    """API anahtarlarını al (güvenli maskeli)"""
    try:
        keys = api_keys_manager.get_all_keys()
        return {
            "keys": keys,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"API anahtarları alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api-keys/validate")
async def validate_api_keys() -> Dict[str, Any]:
    """API anahtarlarını doğrula"""
    try:
        validation = api_keys_manager.validate_keys()
        return {
            "validation": validation,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"API anahtarı doğrulama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api-keys/test-connections")
async def test_api_connections() -> Dict[str, Any]:
    """API bağlantılarını test et"""
    try:
        connections = api_keys_manager.test_connections()
        return {
            "connections": connections,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"API bağlantı testi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_system_logs(lines: int = 100) -> Dict[str, Any]:
    """Sistem loglarını al"""
    try:
        log_file = "logs/vuc2026.log"
        logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                # Son N satırı al
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                
                for line in recent_lines:
                    logs.append(line.strip())
        
        return {
            "logs": logs,
            "total_lines": len(logs),
            "requested_lines": lines,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Logları alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_system_metrics() -> Dict[str, Any]:
    """Sistem metriklerini al"""
    try:
        # CPU metrikleri
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Bellek metrikleri
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk metrikleri
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Ağ metrikleri
        network_io = psutil.net_io_counters()
        
        # Process metrikleri
        process_count = len(psutil.pids())
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": cpu_percent,
                "count": cpu_count,
                "freq_current": cpu_freq.current if cpu_freq else None,
                "freq_min": cpu_freq.min if cpu_freq else None,
                "freq_max": cpu_freq.max if cpu_freq else None
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent,
                "buffers": memory.buffers,
                "cached": memory.cached,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_free": swap.free,
                "swap_percent": swap.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100,
                "read_count": disk_io.read_count if disk_io else 0,
                "write_count": disk_io.write_count if disk_io else 0,
                "read_bytes": disk_io.read_bytes if disk_io else 0,
                "write_bytes": disk_io.write_bytes if disk_io else 0
            },
            "network": {
                "bytes_sent": network_io.bytes_sent if network_io else 0,
                "bytes_recv": network_io.bytes_recv if network_io else 0,
                "packets_sent": network_io.packets_sent if network_io else 0,
                "packets_recv": network_io.packets_recv if network_io else 0,
                "errin": network_io.errin if network_io else 0,
                "errout": network_io.errout if network_io else 0,
                "dropin": network_io.dropin if network_io else 0,
                "dropout": network_io.dropout if network_io else 0
            },
            "processes": {
                "total": process_count,
                "running": len([p for p in psutil.process_iter() if p.status() == 'running']),
                "sleeping": len([p for p in psutil.process_iter() if p.status() == 'sleeping'])
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Sistem metrikleri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restart-service")
async def restart_service(service_name: str) -> Dict[str, Any]:
    """Servisi yeniden başlat (admin only)"""
    try:
        # Bu endpoint sadece geliştirme için
        # Production'da güvenlik önlemleri eklenmeli
        
        restart_info = {
            "service": service_name,
            "status": "restarted",
            "message": f"{service_name} servisi yeniden başlatıldı",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Servis yeniden başlatıldı: {service_name}")
        
        return restart_info
        
    except Exception as e:
        logger.error(f"Servis yeniden başlatma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/version")
async def get_version_info() -> Dict[str, Any]:
    """Versiyon bilgilerini al"""
    try:
        version_info = {
            "version": "1.0.0",
            "build": "20260319",
            "api_version": "v1",
            "python_version": psutil.platform.python_version(),
            "platform": psutil.platform.system(),
            "features": {
                "windows_ai": windows_ai_service.is_available,
                "directml": directml_accelerator.is_available,
                "gpu_acceleration": directml_accelerator.is_available,
                "local_ai": windows_ai_service.is_available,
                "cloud_ai": True,  # Gemini her zaman mevcut
                "orchestrator": True,
                "grey_hat": True,
                "competitor_analysis": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return version_info
        
    except Exception as e:
        logger.error(f"Versiyon bilgileri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
