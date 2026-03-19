"""
Turkish Character Normalization Utility
VUC-2026 Ultimate Dev++ Standards
Türkçe harf kurallarına uygun string işlemleri
"""

import turkish_string
import re
from typing import Dict, Any

class TurkishNormalizer:
    """Türkçe karakter normalizasyon sınıfı"""
    
    # Custom Turkish character mapping
    TURKISH_MAPPING = {
        'c': 'ç',
        'g': 'ğ', 
        'o': 'ö',
        's': 'ş',
        'u': 'ü',
        'C': 'Ç',
        'G': 'Ğ',
        'I': 'İ',
        'O': 'Ö',
        'S': 'Ş',
        'U': 'Ü'
    }
    
    @staticmethod
    def apply_turkish_chars(text: str) -> str:
        """Custom Turkish character conversion"""
        if not text:
            return text
            
        # Specific word mappings for common Turkish words
        word_mappings = {
            'atasehir': 'ataşehir',
            'kadikoy': 'kadıköy',
            'uskudar': 'üsküdar',
            'besiktas': 'beşiktaş',
            'sisli': 'şişli',
            'fatih': 'fatih',
            'eyup': 'eyüp',
            'egitim': 'eğitim',
            'cocuk': 'çocuk',
            'sehit': 'şehit',
            'guzel': 'güzel',
            'ogrenci': 'öğrenci',
            'baba': 'baba',
            'anne': 'anne',
            'videolari': 'videoları'
        }
        
        # Split text into words and apply mappings
        words = text.split()
        result_words = []
        
        for word in words:
            # Check for exact word matches first
            if word in word_mappings:
                result_words.append(word_mappings[word])
            else:
                # Apply character mapping to each character
                mapped_word = ""
                for char in word:
                    if char in TurkishNormalizer.TURKISH_MAPPING:
                        mapped_word += TurkishNormalizer.TURKISH_MAPPING[char]
                    else:
                        mapped_word += char
                result_words.append(mapped_word)
        
        return " ".join(result_words)
    
    @staticmethod
    def normalize_district_name(district_name: str) -> str:
        """
        İlçe adını Türkçe harf kurallarına göre normalize eder
        Örnek: atasehir -> Ataşehir
        """
        if not district_name:
            return district_name
            
        # Apply custom Turkish character mapping and title case
        normalized = TurkishNormalizer.apply_turkish_chars(district_name.lower())
        return turkish_string.title_tr(normalized)
    
    @staticmethod
    def normalize_content_type(content_type: str) -> str:
        """
        İçerik türünü normalize eder
        """
        if not content_type:
            return content_type
            
        mapping = {
            "family": "family",
            "kids": "kids", 
            "bebek": "bebek",
            "cocuk": "çocuk",
            "eğitim": "eğitim",
            "egitim": "eğitim"
        }
        
        return mapping.get(content_type.lower(), content_type.lower())
    
    @staticmethod
    def normalize_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        JSON response içindeki Türkçe karakterleri normalize eder
        """
        if not isinstance(data, dict):
            return data
            
        normalized_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                if key == "district_name":
                    normalized_data[key] = TurkishNormalizer.normalize_district_name(value)
                elif key == "content_type":
                    normalized_data[key] = TurkishNormalizer.normalize_content_type(value)
                else:
                    # General string normalization
                    normalized = TurkishNormalizer.apply_turkish_chars(value.lower())
                    normalized_data[key] = turkish_string.title_tr(normalized)
            elif isinstance(value, dict):
                normalized_data[key] = TurkishNormalizer.normalize_json_response(value)
            elif isinstance(value, list):
                normalized_data[key] = [
                    TurkishNormalizer.normalize_json_response(item) if isinstance(item, dict) 
                    else (
                        turkish_string.title_tr(TurkishNormalizer.apply_turkish_chars(item.lower())) 
                        if isinstance(item, str) else item
                    )
                    for item in value
                ]
            else:
                normalized_data[key] = value
                
        return normalized_data
    
    @staticmethod
    def validate_turkish_characters(text: str) -> bool:
        """
        Metnin geçerli Türkçe karakterler içerdiğini kontrol eder
        """
        turkish_chars = set("çğıöşüÇĞİÖŞÜ")
        return any(char in turkish_chars for char in text)
    
    @staticmethod
    def fix_common_turkish_errors(text: str) -> str:
        """
        Yaygın Türkçe karakter hatalarını düzeltir
        """
        if not text:
            return text
            
        # Apply custom Turkish character mapping and title case
        normalized = TurkishNormalizer.apply_turkish_chars(text.lower())
        return turkish_string.title_tr(normalized)

# VUC-2026 Integration
def apply_turkish_standards(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    VUC-2026 standartlarına göre Türkçe karakter düzenlemesi uygular
    """
    return TurkishNormalizer.normalize_json_response(data)

if __name__ == "__main__":
    # Test cases
    test_data = {
        "district_name": "ataşehir",
        "content_type": "family",
        "description": "ataşehir'de family içerik üretimi"
    }
    
    normalized = apply_turkish_standards(test_data)
    print("Normalized data:", normalized)
