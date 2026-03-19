"""
VUC-2026 ElevenLabs Voice Configuration Service
Family & Kids Empire için optimize edilmiş ses yönetimi
"""

import os
from typing import Dict, Optional
from enum import Enum

class VoiceType(str, Enum):
    RACHEL = "rachel"      # Bebek içerikleri için sıcak, anneane tonu
    BELLA = "bella"        # Çocuklar için enerjik, arkadaşça ton
    DOMI = "domi"          # Eğitici içerik için net, profesyonel ton
    SAM = "sam"            # Erkek, authoritative ton
    ADAM = "adam"          # Erkek, sakin ton

class ContentType(str, Enum):
    PREGNANCY = "pregnancy"
    NEWBORN = "newborn"
    INFANT = "infant"
    TODDLER = "toddler"

class ElevenLabsVoiceConfig:
    """ElevenLabs ses yapılandırma servisi"""
    
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_mappings = self._initialize_voice_mappings()
        self.voice_settings = self._initialize_voice_settings()
    
    def _initialize_voice_mappings(self) -> Dict[ContentType, VoiceType]:
        """İçerik türüne göre ses eşleştirmesi"""
        return {
            ContentType.PREGNANCY: VoiceType.RACHEL,  # Sıcak, anneane tonu
            ContentType.NEWBORN: VoiceType.BELLA,      # Enerjik, arkadaşça ton
            ContentType.INFANT: VoiceType.BELLA,      # Enerjik, arkadaşça ton
            ContentType.TODDLER: VoiceType.DOMI       # Eğitici, profesyonel ton
        }
    
    def _initialize_voice_settings(self) -> Dict[VoiceType, Dict]:
        """Ses tipine göre özel ayarlar"""
        return {
            VoiceType.RACHEL: {
                "stability": 0.75,        # Kararlı, sakin ton
                "similarity_boost": 0.85, # Yüksek benzerlik
                "style": 0.5,            # Dengeli stil
                "use_speaker_boost": True,
                "speed": 0.95            # Biraz yavaş, sakin anlatım
            },
            VoiceType.BELLA: {
                "stability": 0.65,        # Daha dinamik
                "similarity_boost": 0.90, # Yüksek enerji
                "style": 0.7,            # Enerjik stil
                "use_speaker_boost": True,
                "speed": 1.05            # Biraz hızlı, enerjik
            },
            VoiceType.DOMI: {
                "stability": 0.80,        # Çok kararlı
                "similarity_boost": 0.88, # Net anlatım
                "style": 0.4,            # Profesyonel stil
                "use_speaker_boost": True,
                "speed": 1.0             # Normal hız
            },
            VoiceType.SAM: {
                "stability": 0.85,
                "similarity_boost": 0.87,
                "style": 0.3,
                "use_speaker_boost": True,
                "speed": 0.98
            },
            VoiceType.ADAM: {
                "stability": 0.82,
                "similarity_boost": 0.86,
                "style": 0.35,
                "use_speaker_boost": True,
                "speed": 0.95
            }
        }
    
    def get_voice_for_content(self, content_type: ContentType) -> VoiceType:
        """İçerik türüne uygun sesi getir"""
        return self.voice_mappings.get(content_type, VoiceType.RACHEL)
    
    def get_voice_settings(self, voice_type: VoiceType) -> Dict:
        """Ses tipine göre ayarları getir"""
        return self.voice_settings.get(voice_type, self.voice_settings[VoiceType.RACHEL])
    
    def get_voice_payload(self, content_type: ContentType, text: str, **kwargs) -> Dict:
        """ElevenLabs API için payload oluştur"""
        voice_type = self.get_voice_for_content(content_type)
        settings = self.get_voice_settings(voice_type)
        
        return {
            "text": text,
            "voice_id": voice_type.value,
            "emotion": kwargs.get("emotion", "warm"),
            "speed": kwargs.get("speed", settings["speed"]),
            "stability": settings["stability"],
            "similarity_boost": settings["similarity_boost"],
            "style": settings["style"],
            "use_speaker_boost": settings["use_speaker_boost"]
        }
    
    def get_api_key(self) -> str:
        """API key'i güvenli şekilde getir"""
        return self.api_key
    
    def validate_voice_id(self, voice_id: str) -> bool:
        """Voice ID'nin geçerli olup olmadığını kontrol et"""
        valid_voices = [voice.value for voice in VoiceType]
        return voice_id in valid_voices
    
    def get_available_voices(self) -> Dict[str, Dict]:
        """Mevcut sesleri ve özelliklerini listele"""
        return {
            voice.value: {
                "type": voice.name,
                "description": self._get_voice_description(voice),
                "best_for": self._get_best_content_type(voice)
            }
            for voice in VoiceType
        }
    
    def _get_voice_description(self, voice_type: VoiceType) -> str:
        """Ses açıklamaları"""
        descriptions = {
            VoiceType.RACHEL: "Bebek içerikleri için sıcak, anneane tonu",
            VoiceType.BELLA: "Çocuklar için enerjik, arkadaşça ton",
            VoiceType.DOMI: "Eğitici içerik için net, profesyonel ton",
            VoiceType.SAM: "Erkek, authoritative ton",
            VoiceType.ADAM: "Erkek, sakin ton"
        }
        return descriptions.get(voice_type, "Genel amaçlı ses")
    
    def _get_best_content_type(self, voice_type: VoiceType) -> str:
        """Sesin en uygun olduğu içerik türü"""
        best_for = {
            VoiceType.RACHEL: "Pregnancy (Hamilelik)",
            VoiceType.BELLA: "Newborn/Infant (Yenidoğan/Bebek)",
            VoiceType.DOMI: "Toddler (Küçük Çocuk)",
            VoiceType.SAM: "Educational (Eğitici)",
            VoiceType.ADAM: "Narration (Anlatım)"
        }
        return best_for.get(voice_type, "General (Genel)")

# Global instance
elevenlabs_voice_config = ElevenLabsVoiceConfig()
