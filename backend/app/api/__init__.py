"""
VUC-2026 API Package
API endpoint'leri için paket dosyası
"""

# API modüllerini import et
try:
    from . import channels
    from . import videos  
    from . import scripts
    from . import analytics
    from . import settings
    from . import family_kids_empire
except ImportError as e:
    print(f"API modülü import hatası: {e}")
    # Boş modüller oluştur
    channels = None
    videos = None
    scripts = None
    analytics = None
    settings = None
    family_kids_empire = None
