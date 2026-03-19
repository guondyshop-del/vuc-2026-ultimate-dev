#!/usr/bin/env python3
"""
VUC-2026 Production API Key Setup Script
External servisler için API anahtarlarını yapılandırır
"""

import os
import sys
from pathlib import Path

def setup_production_keys():
    """Production API anahtarlarını kur"""
    
    print("🚀 VUC-2026 Production API Key Setup")
    print("=" * 50)
    
    # Gerekli API anahtarları listesi
    required_keys = {
        "GOOGLE_API_KEY": "Google Cloud / Gemini API anahtarı",
        "ELEVENLABS_API_KEY": "ElevenLabs ses sentezi API anahtarı",
        "YOUTUBE_API_KEY": "YouTube Data API v3 anahtarı",
        "AMAZON_ACCESS_KEY_ID": "Amazon Affiliate Access Key ID",
        "AMAZON_SECRET_ACCESS_KEY": "Amazon Affiliate Secret Access Key",
        "AHREFS_API_TOKEN": "Ahrefs SEO analiz API token'ı",
        "SECRET_KEY": "Uygulama gizli anahtarı",
        "DATABASE_URL": "PostgreSQL veritabanı bağlantı URL"
    }
    
    # .env.production dosyasını kontrol et
    env_file = Path(".env.production")
    
    if not env_file.exists():
        print("❌ .env.production dosyası bulunamadı!")
        print("Önce .env.production dosyasını oluşturun.")
        return False
    
    # Mevcut anahtarları kontrol et
    print("\n📋 Gerekli API Anahtarları:")
    print("-" * 30)
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    missing_keys = []
    placeholder_keys = []
    
    for key, description in required_keys.items():
        if key not in content:
            missing_keys.append(key)
        elif "Buraya_" in content or "AIzaSyBuraya_" in content:
            placeholder_keys.append(key)
        else:
            print(f"✅ {key}: {description}")
    
    if missing_keys:
        print(f"\n❌ Eksik API anahtarları ({len(missing_keys)}):")
        for key in missing_keys:
            print(f"   - {key}: {required_keys[key]}")
    
    if placeholder_keys:
        print(f"\n⚠️  Placeholder anahtarlar ({len(placeholder_keys)}):")
        for key in placeholder_keys:
            print(f"   - {key}: {required_keys[key]}")
    
    if not missing_keys and not placeholder_keys:
        print("\n🎉 Tüm API anahtarları yapılandırılmış!")
        return True
    
    # Yapılandırma talimatları
    print("\n🔧 Yapılandırma Talimatları:")
    print("-" * 30)
    
    print("\n1. **Google Cloud / Gemini API**:")
    print("   - https://console.cloud.google.com/apis/credentials")
    print("   - Gemini API'yi etkinleştirin")
    print("   - API anahtarı oluşturun")
    
    print("\n2. **ElevenLabs API**:")
    print("   - https://elevenlabs.io/app/settings/api-keys")
    print("   - API anahtarı oluşturun")
    print("   - Voice ID'leri kontrol edin")
    
    print("\n3. **YouTube Data API v3**:")
    print("   - https://console.cloud.google.com/apis/credentials")
    print("   - YouTube Data API v3'ü etkinleştirin")
    print("   - OAuth 2.0 credentials oluşturun")
    
    print("\n4. **Amazon Affiliate API**:")
    print("   - https://affiliate-program.amazon.com/")
    print("   - Product Advertising API'ye başvurun")
    print("   - Access Key ve Secret Key alın")
    
    print("\n5. **Ahrefs API**:")
    print("   - https://ahrefs.com/api/documentation")
    print("   - API token'ı alın")
    
    print("\n6. **Database Setup**:")
    print("   - PostgreSQL veritabanı kurun")
    print("   - DATABASE_URL format: postgresql://user:password@host:port/database")
    
    # Test connection script
    print("\n🧪 API Test Script:")
    print("-" * 20)
    print("python test_api_connections.py")
    
    return False

def create_env_from_template():
    """Template'den .env.production oluştur"""
    template_content = """# VUC-2026 Production API Configuration
# Gerçek API anahtarlarınızı buraya ekleyin

# === GOOGLE CLOUD / GEMINI API ===
GOOGLE_API_KEY=AIzaSyBuraya_Gercek_Gemini_API_Anahatari
GOOGLE_PROJECT_ID=vuc-2026-production

# === ELEVENLABS API ===
ELEVENLABS_API_KEY=sk-elevenlabs_Buraya_Gercek_API_Anahatari

# === YOUTUBE DATA API v3 ===
YOUTUBE_API_KEY=AIzaSyBuraya_Gercek_YouTube_Data_API_Anahatari

# === AMAZON AFFILIATE API ===
AMAZON_ACCESS_KEY_ID=AKIABuraya_Amazon_Access_Key
AMAZON_SECRET_ACCESS_KEY=Buraya_Amazon_Secret_Key
AMAZON_ASSOCIATE_TAG=vuc2026-20

# === AHREFS API ===
AHREFS_API_TOKEN=ahrefs-token-Buraya_Gercek_Ahrefs_Token

# === SECURITY KEYS ===
SECRET_KEY=Buraya_Cok_Gizli_Uretim_Anahatari_2024
JWT_SECRET_KEY=Buraya_JWT_Signature_Anahatari

# === DATABASE ===
DATABASE_URL=postgresql://vuc2026:password@localhost:5432/vuc2026_production
REDIS_URL=redis://localhost:6379/0
"""
    
    with open(".env.production", "w") as f:
        f.write(template_content)
    
    print("✅ .env.production dosyası oluşturuldu!")

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    if not Path(".env.production").exists():
        print("📝 .env.production dosyası oluşturuluyor...")
        create_env_from_template()
    
    setup_production_keys()
