"""
Turkish Character Normalization Test
VUC-2026 Ultimate Dev++ Standards
"""

import pytest
from app.utils.turkish_normalizer import TurkishNormalizer, apply_turkish_standards

def test_normalize_district_name():
    """İlçe adı normalizasyon testi"""
    # Test cases
    test_cases = [
        ("ataşehir", "Ataşehir"),
        ("kadikoy", "Kadıköy"),
        ("uskudar", "Üsküdar"),
        ("besiktas", "Beşiktaş"),
        ("sisli", "Şişli"),
        ("fatih", "Fatih"),
        ("eyup", "Eyüp")
    ]
    
    for input_name, expected in test_cases:
        result = TurkishNormalizer.normalize_district_name(input_name)
        assert result == expected, f"Expected {expected}, got {result}"

def test_normalize_content_type():
    """İçerik türü normalizasyon testi"""
    test_cases = [
        ("family", "family"),
        ("cocuk", "çocuk"),
        ("egitim", "eğitim"),
        ("bebek", "bebek"),
        ("kids", "kids")
    ]
    
    for input_type, expected in test_cases:
        result = TurkishNormalizer.normalize_content_type(input_type)
        assert result == expected, f"Expected {expected}, got {result}"

def test_normalize_json_response():
    """JSON response normalizasyon testi"""
    test_data = {
        "district_name": "ataşehir",
        "content_type": "cocuk",
        "description": "ataşehir'de çocuk içerikleri",
        "nested": {
            "title": "ataşehir egitim videolari"
        }
    }
    
    result = apply_turkish_standards(test_data)
    
    assert result["district_name"] == "Ataşehir"
    assert result["content_type"] == "çocuk"
    assert "Ataşehir" in result["description"]
    assert "Eğitim" in result["nested"]["title"]

def test_validate_turkish_characters():
    """Türkçe karakter validasyon testi"""
    turkish_text = "Ataşehir'de yaşayan çocuklar"
    english_text = "Atasehirde yasanan cocuklar"
    
    assert TurkishNormalizer.validate_turkish_characters(turkish_text) == True
    assert TurkishNormalizer.validate_turkish_characters(english_text) == False

def test_fix_common_turkish_errors():
    """Yaygın Türkçe karakter hata düzeltme testi"""
    test_cases = [
        ("atasehir", "Ataşehir"),
        ("egitim", "Eğitim"),
        ("cocuk", "Çocuk"),
        ("sehit", "Şehit")
    ]
    
    for input_text, expected in test_cases:
        result = TurkishNormalizer.fix_common_turkish_errors(input_text)
        assert result == expected, f"Expected {expected}, got {result}"

if __name__ == "__main__":
    # Run tests
    test_normalize_district_name()
    test_normalize_content_type()
    test_normalize_json_response()
    test_validate_turkish_characters()
    test_fix_common_turkish_errors()
    
    print("✅ All Turkish normalization tests passed!")
