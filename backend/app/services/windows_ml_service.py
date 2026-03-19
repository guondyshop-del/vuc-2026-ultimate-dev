"""
VUC-2026 Windows ML Service
Microsoft Windows ML API'leri için entegrasyon katmanı

Bu servis, Windows ML kullanarak ONNX modellerini yerel olarak çalıştırır
ve donanım hızlandırmasını optimize eder.
"""

import os
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path

# Windows ML için import'lar
try:
    # ONNX Runtime ile Windows ML entegrasyonu
    import onnxruntime as ort
    from onnxruntime import SessionOptions, InferenceSession
    WINDOWS_ML_AVAILABLE = True
except ImportError:
    logging.warning("ONNX Runtime mevcut değil. Windows ML özellikleri kullanılamayacak.")
    WINDOWS_ML_AVAILABLE = False

# DirectML için kontrol
try:
    # DirectML execution provider'ı kontrol et
    if WINDOWS_ML_AVAILABLE:
        providers = ort.get_available_providers()
        DIRECTML_AVAILABLE = 'DmlExecutionProvider' in providers
    else:
        DIRECTML_AVAILABLE = False
except:
    DIRECTML_AVAILABLE = False

logger = logging.getLogger(__name__)

class WindowsMLService:
    """Windows ML API'leri için servis katmanı"""
    
    def __init__(self):
        self.is_available = WINDOWS_ML_AVAILABLE
        self.directml_available = DIRECTML_AVAILABLE
        self.session_options = None
        self.loaded_models = {}
        self.model_cache = {}
        
        # Model yolları
        self.models_dir = Path("../models/windows_ml")
        self.models_dir.mkdir(exist_ok=True, parents=True)
        
        if self.is_available:
            self._initialize_windows_ml()
    
    def _initialize_windows_ml(self):
        """Windows ML bileşenlerini başlat"""
        try:
            # Session options ayarla
            self.session_options = SessionOptions()
            self.session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            self.session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            
            # Execution provider'ları ayarla
            if self.directml_available:
                self.providers = ['DmlExecutionProvider', 'CPUExecutionProvider']
                logger.info("Windows ML + DirectML başlatıldı")
            else:
                self.providers = ['CPUExecutionProvider']
                logger.info("Windows ML (CPU only) başlatıldı")
                
        except Exception as e:
            logger.error(f"Windows ML başlatma hatası: {e}")
            self.is_available = False
    
    def load_model(self, model_name: str, model_path: str = None) -> bool:
        """
        ONNX modelini yükle
        
        Args:
            model_name: Model adı
            model_path: Model dosya yolu (opsiyonel)
            
        Returns:
            Başarılı olup olmadığı
        """
        
        if not self.is_available:
            logger.warning("Windows ML mevcut değil")
            return False
        
        try:
            # Model yolunu belirle
            if model_path is None:
                model_path = self.models_dir / f"{model_name}.onnx"
            
            if not os.path.exists(model_path):
                logger.error(f"Model dosyası bulunamadı: {model_path}")
                return False
            
            # Modeli yükle
            session = InferenceSession(
                model_path,
                sess_options=self.session_options,
                providers=self.providers
            )
            
            # Model bilgilerini al
            input_details = session.get_inputs()
            output_details = session.get_outputs()
            
            self.loaded_models[model_name] = {
                'session': session,
                'input_details': input_details,
                'output_details': output_details,
                'model_path': str(model_path),
                'loaded_at': datetime.now().isoformat()
            }
            
            logger.info(f"Model yüklendi: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Model yükleme hatası ({model_name}): {e}")
            return False
    
    def run_inference(self, model_name: str, input_data: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """
        Model üzerinde inference çalıştır
        
        Args:
            model_name: Model adı
            input_data: Giriş verisi
            
        Returns:
            Inference sonuçları
        """
        
        if not self.is_available:
            return {"success": False, "error": "Windows ML mevcut değil"}
        
        if model_name not in self.loaded_models:
            return {"success": False, "error": f"Model yüklenmemiş: {model_name}"}
        
        try:
            model_info = self.loaded_models[model_name]
            session = model_info['session']
            
            # Giriş verilerini hazırla
            inputs = {}
            for input_detail in model_info['input_details']:
                input_name = input_detail.name
                if input_name in input_data:
                    inputs[input_name] = input_data[input_name]
                else:
                    logger.warning(f"Giriş verisi bulunamadı: {input_name}")
            
            # Inference çalıştır
            start_time = datetime.now()
            outputs = session.run(None, inputs)
            end_time = datetime.now()
            
            # Çıktıları hazırla
            output_data = {}
            for i, output_detail in enumerate(model_info['output_details']):
                output_name = output_detail.name
                output_data[output_name] = outputs[i]
            
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                "success": True,
                "outputs": output_data,
                "processing_time": processing_time,
                "model_name": model_name,
                "provider": self.providers[0] if self.providers else "CPU",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Inference hatası ({model_name}): {e}")
            return {"success": False, "error": str(e)}
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Model bilgilerini al"""
        
        if model_name not in self.loaded_models:
            return {"success": False, "error": f"Model yüklenmemiş: {model_name}"}
        
        model_info = self.loaded_models[model_name]
        
        return {
            "success": True,
            "model_name": model_name,
            "model_path": model_info['model_path'],
            "loaded_at": model_info['loaded_at'],
            "input_details": [
                {
                    "name": inp.name,
                    "type": str(inp.type),
                    "shape": inp.shape
                } for inp in model_info['input_details']
            ],
            "output_details": [
                {
                    "name": out.name,
                    "type": str(out.type),
                    "shape": out.shape
                } for out in model_info['output_details']
            ],
            "providers": self.providers
        }
    
    def list_loaded_models(self) -> List[str]:
        """Yüklenmiş modelleri listele"""
        return list(self.loaded_models.keys())
    
    def unload_model(self, model_name: str) -> bool:
        """Modeli hafızadan kaldır"""
        
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            logger.info(f"Model kaldırıldı: {model_name}")
            return True
        
        return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Cihaz ve donanım bilgilerini al"""
        
        if not self.is_available:
            return {"available": False, "error": "Windows ML mevcut değil"}
        
        try:
            device_info = {
                "available": True,
                "windows_ml": True,
                "directml": self.directml_available,
                "providers": self.providers,
                "onnx_runtime_version": ort.__version__,
                "execution_providers": ort.get_available_providers(),
                "device_info": self._get_device_capabilities()
            }
            
            return device_info
            
        except Exception as e:
            logger.error(f"Cihaz bilgileri alma hatası: {e}")
            return {"available": False, "error": str(e)}
    
    def _get_device_capabilities(self) -> Dict[str, Any]:
        """Cihaz yeteneklerini al"""
        capabilities = {
            "cpu_execution": True,
            "gpu_execution": self.directml_available,
            "npu_execution": False,  # NPU desteği kontrol edilebilir
            "memory_optimization": True,
            "parallel_execution": len(self.providers) > 1
        }
        
        # GPU bilgilerini al (varsa)
        if self.directml_available:
            try:
                # DirectML GPU bilgilerini kontrol et
                capabilities["gpu_info"] = {
                    "directml_version": "1.0",
                    "supported_formats": ["ONNX"],
                    "acceleration": True
                }
            except:
                capabilities["gpu_info"] = {"error": "GPU bilgileri alınamadı"}
        
        return capabilities
    
    def optimize_model(self, model_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Modeli optimize et (graph optimization)
        
        Args:
            model_path: Giriş model yolu
            output_path: Çıktı model yolu
            
        Returns:
            Optimizasyon sonuçları
        """
        
        if not self.is_available:
            return {"success": False, "error": "Windows ML mevcut değil"}
        
        try:
            if output_path is None:
                output_path = model_path.replace('.onnx', '_optimized.onnx')
            
            # Model optimizasyonu için session oluştur
            sess_options = SessionOptions()
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            sess_options.optimized_model_filepath = output_path
            
            # Geçici session oluştur (optimizasyon için)
            session = InferenceSession(
                model_path,
                sess_options=sess_options,
                providers=self.providers
            )
            
            return {
                "success": True,
                "input_model": model_path,
                "output_model": output_path,
                "optimization_level": "ORT_ENABLE_ALL",
                "providers_used": self.providers,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Model optimizasyonu hatası: {e}")
            return {"success": False, "error": str(e)}
    
    def benchmark_model(self, model_name: str, input_data: Dict[str, np.ndarray], 
                       iterations: int = 10) -> Dict[str, Any]:
        """
        Model performansını test et
        
        Args:
            model_name: Model adı
            input_data: Test verisi
            iterations: İterasyon sayısı
            
        Returns:
            Benchmark sonuçları
        """
        
        if not self.is_available:
            return {"success": False, "error": "Windows ML mevcut değil"}
        
        if model_name not in self.loaded_models:
            return {"success": False, "error": f"Model yüklenmemiş: {model_name}"}
        
        try:
            times = []
            
            for i in range(iterations):
                result = self.run_inference(model_name, input_data)
                if result["success"]:
                    times.append(result["processing_time"])
                else:
                    return {"success": False, "error": f"Inference hatası: {result['error']}"}
            
            # İstatistikleri hesapla
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            return {
                "success": True,
                "model_name": model_name,
                "iterations": iterations,
                "average_time": avg_time,
                "min_time": min_time,
                "max_time": max_time,
                "throughput": 1.0 / avg_time if avg_time > 0 else 0,
                "provider": self.providers[0] if self.providers else "CPU",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Benchmark hatası: {e}")
            return {"success": False, "error": str(e)}

# Global instance
windows_ml_service = WindowsMLService()
