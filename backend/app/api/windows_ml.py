"""
VUC-2026 Windows ML API Endpoints
Windows ML ve ONNX model yönetimi için endpoint'ler
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List, Any, Optional
import logging
import os
import numpy as np
from datetime import datetime

from app.services.windows_ml_service import windows_ml_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/windows-ml", tags=["windows-ml"])

@router.get("/status")
async def get_windows_ml_status() -> Dict[str, Any]:
    """Windows ML durumunu al"""
    try:
        status = {
            "available": windows_ml_service.is_available,
            "directml": windows_ml_service.directml_available,
            "device_info": windows_ml_service.get_device_info(),
            "loaded_models": windows_ml_service.list_loaded_models(),
            "timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Windows ML durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_name}/load")
async def load_model(model_name: str, model_file: UploadFile = File(...)) -> Dict[str, Any]:
    """ONNX modelini yükle"""
    try:
        # Model dosyasını kaydet
        models_dir = "../models/windows_ml"
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, f"{model_name}.onnx")
        
        with open(model_path, "wb") as buffer:
            content = await model_file.read()
            buffer.write(content)
        
        # Modeli yükle
        success = windows_ml_service.load_model(model_name, model_path)
        
        if success:
            model_info = windows_ml_service.get_model_info(model_name)
            return {
                "success": True,
                "model_name": model_name,
                "model_info": model_info,
                "message": "Model başarıyla yüklendi"
            }
        else:
            return {
                "success": False,
                "error": "Model yüklenemedi"
            }
        
    except Exception as e:
        logger.error(f"Model yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_name}/inference")
async def run_inference(model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Model üzerinde inference çalıştır"""
    try:
        # Giriş verisini numpy array'e çevir
        processed_inputs = {}
        for key, value in input_data.items():
            if isinstance(value, list):
                processed_inputs[key] = np.array(value, dtype=np.float32)
            else:
                processed_inputs[key] = value
        
        # Inference çalıştır
        result = windows_ml_service.run_inference(model_name, processed_inputs)
        
        return result
        
    except Exception as e:
        logger.error(f"Inference hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_name}/info")
async def get_model_info(model_name: str) -> Dict[str, Any]:
    """Model bilgilerini al"""
    try:
        info = windows_ml_service.get_model_info(model_name)
        return info
        
    except Exception as e:
        logger.error(f"Model bilgileri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models() -> Dict[str, Any]:
    """Yüklenmiş modelleri listele"""
    try:
        models = windows_ml_service.list_loaded_models()
        model_details = {}
        
        for model_name in models:
            model_details[model_name] = windows_ml_service.get_model_info(model_name)
        
        return {
            "success": True,
            "models": models,
            "model_details": model_details,
            "total_loaded": len(models)
        }
        
    except Exception as e:
        logger.error(f"Model listesi alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/models/{model_name}")
async def unload_model(model_name: str) -> Dict[str, Any]:
    """Modeli hafızadan kaldır"""
    try:
        success = windows_ml_service.unload_model(model_name)
        
        return {
            "success": success,
            "model_name": model_name,
            "message": "Model kaldırıldı" if success else "Model bulunamadı"
        }
        
    except Exception as e:
        logger.error(f"Model kaldırma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_name}/benchmark")
async def benchmark_model(
    model_name: str, 
    input_data: Dict[str, Any],
    iterations: int = 10
) -> Dict[str, Any]:
    """Model performansını test et"""
    try:
        # Giriş verisini işle
        processed_inputs = {}
        for key, value in input_data.items():
            if isinstance(value, list):
                processed_inputs[key] = np.array(value, dtype=np.float32)
            else:
                processed_inputs[key] = value
        
        # Benchmark çalıştır
        result = windows_ml_service.benchmark_model(model_name, processed_inputs, iterations)
        
        return result
        
    except Exception as e:
        logger.error(f"Benchmark hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/optimize")
async def optimize_model(
    model_file: UploadFile = File(...),
    output_name: str = "optimized_model"
) -> Dict[str, Any]:
    """Modeli optimize et"""
    try:
        # Model dosyasını kaydet
        models_dir = "../models/windows_ml"
        os.makedirs(models_dir, exist_ok=True)
        
        input_path = os.path.join(models_dir, f"{output_name}_input.onnx")
        output_path = os.path.join(models_dir, f"{output_name}_optimized.onnx")
        
        with open(input_path, "wb") as buffer:
            content = await model_file.read()
            buffer.write(content)
        
        # Optimizasyon yap
        result = windows_ml_service.optimize_model(input_path, output_path)
        
        return result
        
    except Exception as e:
        logger.error(f"Model optimizasyonu hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/device")
async def get_device_info() -> Dict[str, Any]:
    """Cihaz ve donanım bilgilerini al"""
    try:
        device_info = windows_ml_service.get_device_info()
        return device_info
        
    except Exception as e:
        logger.error(f"Cihaz bilgileri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-connection")
async def test_windows_ml_connection() -> Dict[str, Any]:
    """Windows ML bağlantısını test et"""
    try:
        test_results = {
            "windows_ml": {
                "available": windows_ml_service.is_available,
                "status": "connected" if windows_ml_service.is_available else "disconnected"
            },
            "directml": {
                "available": windows_ml_service.directml_available,
                "status": "connected" if windows_ml_service.directml_available else "disconnected"
            },
            "onnx_runtime": {
                "available": windows_ml_service.is_available,
                "version": "1.24.4" if windows_ml_service.is_available else None
            },
            "loaded_models_count": len(windows_ml_service.list_loaded_models()),
            "device_capabilities": windows_ml_service._get_device_capabilities() if windows_ml_service.is_available else {},
            "overall_status": "healthy" if windows_ml_service.is_available else "degraded",
            "timestamp": datetime.now().isoformat()
        }
        
        return test_results
        
    except Exception as e:
        logger.error(f"Windows ML bağlantı testi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_execution_providers() -> Dict[str, Any]:
    """Mevcut execution provider'ları listele"""
    try:
        if not windows_ml_service.is_available:
            return {"available": False, "error": "Windows ML mevcut değil"}
        
        import onnxruntime as ort
        
        providers = ort.get_available_providers()
        active_providers = windows_ml_service.providers
        
        return {
            "available": True,
            "all_providers": providers,
            "active_providers": active_providers,
            "primary_provider": active_providers[0] if active_providers else None,
            "directml_available": 'DmlExecutionProvider' in providers,
            "cuda_available": 'CUDAExecutionProvider' in providers,
            "cpu_available": 'CPUExecutionProvider' in providers
        }
        
    except Exception as e:
        logger.error(f"Provider listesi alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
