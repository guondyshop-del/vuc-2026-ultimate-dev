"""
VUC-2026 API Keys Management
Tüm API anahtarlarını güvenli bir şekilde yönetir
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class APIKeysManager:
    """API Anahtarları Yöneticisi"""
    
    def __init__(self):
        self.keys_file = "api_keys.enc"
        self.master_key = self._get_or_create_master_key()
        self.cipher = Fernet(self.master_key)
        self.keys = self._load_keys()
    
    def _get_or_create_master_key(self) -> bytes:
        """Ana anahtarı al veya oluştur"""
        master_key_file = "master.key"
        
        if os.path.exists(master_key_file):
            with open(master_key_file, 'rb') as f:
                return f.read()
        else:
            # Yeni anahtar oluştur
            master_key = Fernet.generate_key()
            with open(master_key_file, 'wb') as f:
                f.write(master_key)
            return master_key
    
    def _load_keys(self) -> Dict[str, Any]:
        """Şifreli anahtarları yükle"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            else:
                return self._get_default_keys()
        except Exception as e:
            logger.error(f"API anahtarları yüklenemedi: {e}")
            return self._get_default_keys()
    
    def _get_default_keys(self) -> Dict[str, Any]:
        """Varsayılan anahtarları al"""
        return {
            "google": {
                "gemini_api_key": "AIzaSyDjastAPrl4GcrgH-_t3FO3jJZtgOReHyc",
                "enabled": True,
                "last_updated": datetime.now().isoformat()
            },
            "youtube": {
                "api_key": os.getenv("YOUTUBE_API_KEY", ""),
                "client_id": os.getenv("YOUTUBE_CLIENT_ID", ""),
                "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET", ""),
                "enabled": bool(os.getenv("YOUTUBE_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "pexels": {
                "api_key": os.getenv("PEXELS_API_KEY", ""),
                "enabled": bool(os.getenv("PEXELS_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "pixabay": {
                "api_key": os.getenv("PIXABAY_API_KEY", ""),
                "enabled": bool(os.getenv("PIXABAY_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "redis": {
                "host": os.getenv("REDIS_HOST", "localhost"),
                "port": int(os.getenv("REDIS_PORT", 6379)),
                "password": os.getenv("REDIS_PASSWORD", ""),
                "db": int(os.getenv("REDIS_DB", 0)),
                "enabled": True,
                "last_updated": datetime.now().isoformat()
            },
            "database": {
                "url": os.getenv("DATABASE_URL", "sqlite:///./vuc2026.db"),
                "enabled": True,
                "last_updated": datetime.now().isoformat()
            },
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "enabled": bool(os.getenv("OPENAI_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "enabled": bool(os.getenv("ANTHROPIC_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "elevenlabs": {
                "api_key": os.getenv("ELEVENLABS_API_KEY", ""),
                "enabled": bool(os.getenv("ELEVENLABS_API_KEY")),
                "last_updated": datetime.now().isoformat()
            },
            "azure": {
                "speech_key": os.getenv("AZURE_SPEECH_KEY", ""),
                "speech_region": os.getenv("AZURE_SPEECH_REGION", ""),
                "computer_vision_key": os.getenv("AZURE_COMPUTER_VISION_KEY", ""),
                "computer_vision_endpoint": os.getenv("AZURE_COMPUTER_VISION_ENDPOINT", ""),
                "enabled": any([
                    os.getenv("AZURE_SPEECH_KEY"),
                    os.getenv("AZURE_COMPUTER_VISION_KEY")
                ]),
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def save_keys(self):
        """Anahtarları şifreli olarak kaydet"""
        try:
            keys_json = json.dumps(self.keys, indent=2)
            encrypted_data = self.cipher.encrypt(keys_json.encode())
            with open(self.keys_file, 'wb') as f:
                f.write(encrypted_data)
            logger.info("API anahtarları başarıyla kaydedildi")
        except Exception as e:
            logger.error(f"API anahtarları kaydedilemedi: {e}")
    
    def get_key(self, service: str, key_name: str = None) -> Optional[str]:
        """Belirli bir anahtarı al"""
        try:
            if key_name:
                return self.keys.get(service, {}).get(key_name)
            else:
                return self.keys.get(service)
        except Exception as e:
            logger.error(f"Anahtar alma hatası: {e}")
            return None
    
    def set_key(self, service: str, key_name: str, value: str):
        """Anahtar ayarla"""
        try:
            if service not in self.keys:
                self.keys[service] = {}
            
            self.keys[service][key_name] = value
            self.keys[service]["last_updated"] = datetime.now().isoformat()
            self.save_keys()
            logger.info(f"{service}.{key_name} anahtarı güncellendi")
        except Exception as e:
            logger.error(f"Anahtar ayarlama hatası: {e}")
    
    def enable_service(self, service: str, enabled: bool = True):
        """Servisi etkinleştir/devre dışı bırak"""
        try:
            if service in self.keys:
                self.keys[service]["enabled"] = enabled
                self.keys[service]["last_updated"] = datetime.now().isoformat()
                self.save_keys()
                logger.info(f"{service} servisi {'etkinleştirildi' if enabled else 'devre dışı bırakıldı'}")
        except Exception as e:
            logger.error(f"Servis durum değiştirme hatası: {e}")
    
    def get_all_keys(self) -> Dict[str, Any]:
        """Tüm anahtarları al (güvenli maskeli)"""
        try:
            safe_keys = {}
            for service, keys in self.keys.items():
                safe_keys[service] = {
                    "enabled": keys.get("enabled", False),
                    "last_updated": keys.get("last_updated"),
                    "configured": self._is_service_configured(keys)
                }
                
                # Anahtarları maskele
                for key, value in keys.items():
                    if key not in ["enabled", "last_updated"] and isinstance(value, str) and value:
                        safe_keys[service][f"{key}_masked"] = self._mask_key(value)
            
            return safe_keys
        except Exception as e:
            logger.error(f"Anahtar listesi alma hatası: {e}")
            return {}
    
    def _is_service_configured(self, keys: Dict[str, Any]) -> bool:
        """Servisin yapılandırılmış olup olmadığını kontrol et"""
        for key, value in keys.items():
            if key not in ["enabled", "last_updated"] and isinstance(value, str) and value:
                return True
        return False
    
    def _mask_key(self, key: str) -> str:
        """Anahtarı maskele"""
        if len(key) <= 8:
            return "*" * len(key)
        return key[:4] + "*" * (len(key) - 8) + key[-4:]
    
    def validate_keys(self) -> Dict[str, Any]:
        """Tüm anahtarların geçerliliğini kontrol et"""
        validation_results = {}
        
        # Google Gemini
        gemini_key = self.get_key("google", "gemini_api_key")
        validation_results["google"] = {
            "valid": bool(gemini_key and len(gemini_key) > 30),
            "message": "Geçerli" if gemini_key and len(gemini_key) > 30 else "Geçersiz veya eksik"
        }
        
        # YouTube
        youtube_key = self.get_key("youtube", "api_key")
        validation_results["youtube"] = {
            "valid": bool(youtube_key and len(youtube_key) > 20),
            "message": "Geçerli" if youtube_key and len(youtube_key) > 20 else "Geçersiz veya eksik"
        }
        
        # Redis
        redis_host = self.get_key("redis", "host")
        validation_results["redis"] = {
            "valid": bool(redis_host),
            "message": "Geçerli" if redis_host else "Geçersiz"
        }
        
        # Database
        db_url = self.get_key("database", "url")
        validation_results["database"] = {
            "valid": bool(db_url),
            "message": "Geçerli" if db_url else "Geçersiz"
        }
        
        # Diğer servisler
        for service in ["pexels", "pixabay", "openai", "anthropic", "elevenlabs", "azure"]:
            api_key = self.get_key(service, "api_key") or self.get_key(service, "speech_key")
            validation_results[service] = {
                "valid": bool(api_key),
                "message": "Geçerli" if api_key else "Eksik"
            }
        
        return validation_results
    
    def test_connections(self) -> Dict[str, Any]:
        """Tüm servis bağlantılarını test et"""
        test_results = {}
        
        # Google Gemini test
        try:
            from app.services.ai_service import AIService
            ai_service = AIService(self.get_key("google", "gemini_api_key") or "")
            test_results["google"] = {
                "status": "connected",
                "message": "Bağlantı başarılı"
            }
        except Exception as e:
            test_results["google"] = {
                "status": "error",
                "message": str(e)
            }
        
        # Redis test
        try:
            import redis
            redis_config = self.keys.get("redis", {})
            r = redis.Redis(
                host=redis_config.get("host", "localhost"),
                port=redis_config.get("port", 6379),
                password=redis_config.get("password"),
                db=redis_config.get("db", 0)
            )
            r.ping()
            test_results["redis"] = {
                "status": "connected",
                "message": "Redis bağlantısı başarılı"
            }
        except Exception as e:
            test_results["redis"] = {
                "status": "error",
                "message": f"Redis bağlantı hatası: {e}"
            }
        
        # Database test
        try:
            from app.database import engine
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            test_results["database"] = {
                "status": "connected",
                "message": "Veritabanı bağlantısı başarılı"
            }
        except Exception as e:
            test_results["database"] = {
                "status": "error",
                "message": f"Veritabanı bağlantı hatası: {e}"
            }
        
        # Windows AI test
        try:
            from app.services.windows_ai_service import windows_ai_service
            test_results["windows_ai"] = {
                "status": "connected" if windows_ai_service.is_available else "disconnected",
                "message": "Windows AI mevcut" if windows_ai_service.is_available else "Windows AI mevcut değil"
            }
        except Exception as e:
            test_results["windows_ai"] = {
                "status": "error",
                "message": f"Windows AI hatası: {e}"
            }
        
        # DirectML test
        try:
            from app.services.directml_accelerator import directml_accelerator
            test_results["directml"] = {
                "status": "connected" if directml_accelerator.is_available else "disconnected",
                "message": "DirectML mevcut" if directml_accelerator.is_available else "DirectML mevcut değil"
            }
        except Exception as e:
            test_results["directml"] = {
                "status": "error",
                "message": f"DirectML hatası: {e}"
            }
        
        return test_results

# Global instance
api_keys_manager = APIKeysManager()
