"""
VUC-2026 Settings Service
Ayarlar yönetimi servis katmanı
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

class SettingsService:
    """Ayarlar Servisi"""
    
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = self._get_default_settings()
        self.settings = self._load_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Varsayılan ayarları al"""
        return {
            "general": {
                "app_name": "VUC-2026",
                "version": "1.0.0",
                "debug": False,
                "log_level": "INFO"
            },
            "ai": {
                "provider": "google",
                "model": "gemini-2.0-pro",
                "temperature": 0.7,
                "max_tokens": 4000
            },
            "video": {
                "default_duration": 300,
                "resolution": "1920x1080",
                "fps": 30,
                "codec": "h264"
            },
            "upload": {
                "auto_upload": False,
                "privacy": "public",
                "category": "22"
            },
            "windows_ai": {
                "enabled": True,
                "use_directml": True,
                "ocr_language": "tr",
                "speech_language": "tr-TR"
            },
            "notifications": {
                "email_enabled": False,
                "push_enabled": True,
                "success_notifications": True,
                "error_notifications": True
            }
        }
    
    def _load_settings(self) -> Dict[str, Any]:
        """Ayarları dosyadan yükle"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                # Varsayılan ayarlarla birleştir
                return {**self.default_settings, **loaded_settings}
            else:
                return self.default_settings.copy()
        except Exception as e:
            logger.error(f"Ayarlar yüklenemedi: {e}")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Ayarları dosyaya kaydet"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.info("Ayarlar başarıyla kaydedildi")
        except Exception as e:
            logger.error(f"Ayarlar kaydedilemedi: {e}")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Belirli bir ayarı al"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_setting(self, key: str, value: Any):
        """Belirli bir ayarı ayarla"""
        keys = key.split('.')
        settings = self.settings
        
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        settings[keys[-1]] = value
        self.save_settings()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Tüm ayarları al"""
        return self.settings.copy()
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Ayarları güncelle"""
        self.settings.update(new_settings)
        self.save_settings()
    
    async def load_default_settings(self):
        """Varsayılan ayarları yükle"""
        self.settings = self.default_settings.copy()
        self.save_settings()
        logger.info("Varsayılan ayarlar yüklendi")

# Global instance
settings_service = SettingsService()
