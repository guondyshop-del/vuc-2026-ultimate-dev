"""
VUC-2026 API Key Status Checker
Gerekli API key'lerin durumunu kontrol et
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIKeyChecker:
    """API key durum kontrolü"""
    
    def __init__(self):
        self.api_keys = {
            # ✅ MEVCUT VE ÇALIŞAN
            'google_ai_api_key': {
                'name': 'Google AI (Gemini)',
                'key': os.getenv('GOOGLE_AI_API_KEY'),
                'status': '✅ WORKING',
                'purpose': 'Script generation, AI content',
                'priority': 'HIGH'
            },
            'youtube_api_key': {
                'name': 'YouTube Data API v3',
                'key': os.getenv('YOUTUBE_API_KEY'),
                'status': '✅ WORKING',
                'purpose': 'Video search, channel data',
                'priority': 'HIGH'
            },
            'elevenlabs_api_key': {
                'name': 'ElevenLabs Voice',
                'key': os.getenv('ELEVENLABS_API_KEY'),
                'status': '✅ WORKING',
                'purpose': 'Voice synthesis, TTS',
                'priority': 'HIGH'
            },
            
            # 🔧 EKLENEBİLİR (OPSİYONEL)
            'openai_api_key': {
                'name': 'OpenAI GPT',
                'key': os.getenv('OPENAI_API_KEY'),
                'status': '❌ MISSING',
                'purpose': 'Alternative AI, backup content',
                'priority': 'MEDIUM'
            },
            'anthropic_api_key': {
                'name': 'Anthropic Claude',
                'key': os.getenv('ANTHROPIC_API_KEY'),
                'status': '❌ MISSING',
                'purpose': 'AI content alternative',
                'priority': 'MEDIUM'
            },
            'pexels_api_key': {
                'name': 'Pexels Images',
                'key': os.getenv('PEXELS_API_KEY'),
                'status': '❌ MISSING',
                'purpose': 'Stock images, thumbnails',
                'priority': 'LOW'
            },
            'pixabay_api_key': {
                'name': 'Pixabay Media',
                'key': os.getenv('PIXABAY_API_KEY'),
                'status': '❌ MISSING',
                'purpose': 'Stock videos, images',
                'priority': 'LOW'
            }
        }
    
    def check_status(self):
        """API key durumlarını kontrol et"""
        print("🔑 VUC-2026 API KEY DURUMU")
        print("=" * 60)
        
        working = []
        missing = []
        
        for key_id, info in self.api_keys.items():
            key = info['key']
            status = '✅ WORKING' if key and key.strip() else '❌ MISSING'
            info['status'] = status
            
            if key and key.strip():
                working.append(info)
            else:
                missing.append(info)
        
        # Working API keys
        print("\n✅ ÇALIŞAN API KEYS:")
        print("-" * 40)
        for info in working:
            print(f"🔹 {info['name']}")
            print(f"   Purpose: {info['purpose']}")
            print(f"   Priority: {info['priority']}")
            print(f"   Key: {info['key'][:15]}..." if info['key'] else "   Key: Missing")
            print()
        
        # Missing API keys
        print("\n❌ EKSİK API KEYS:")
        print("-" * 40)
        for info in missing:
            print(f"🔸 {info['name']}")
            print(f"   Purpose: {info['purpose']}")
            print(f"   Priority: {info['priority']}")
            print(f"   Status: Required for full features")
            print()
        
        return working, missing
    
    def get_recommendations(self, missing):
        """Öneriler oluştur"""
        print("\n🎯 API KEY ÖNERİLERİ:")
        print("=" * 40)
        
        high_priority = [info for info in missing if info['priority'] == 'HIGH']
        medium_priority = [info for info in missing if info['priority'] == 'MEDIUM']
        low_priority = [info for info in missing if info['priority'] == 'LOW']
        
        if high_priority:
            print("🚀 ÖNCELİKLİ (Hemen gerekli):")
            for info in high_priority:
                print(f"   - {info['name']}: {info['purpose']}")
        
        if medium_priority:
            print("\n⚡ ORTA ÖNCELİK (İyileştirme için):")
            for info in medium_priority:
                print(f"   - {info['name']}: {info['purpose']}")
        
        if low_priority:
            print("\n💡 DÜŞÜK ÖNCELİK (Ek özellikler):")
            for info in low_priority:
                print(f"   - {info['name']}: {info['purpose']}")
    
    def minimal_setup(self):
        """Minimal kurulum için gerekli olanlar"""
        print("\n🎯 MINIMAL KURULUM İÇİN GEREKLİLER:")
        print("=" * 40)
        
        minimal_required = [
            'Google AI (Gemini) - Script generation',
            'YouTube Data API v3 - Video operations',
            'ElevenLabs Voice - Voice synthesis'
        ]
        
        for item in minimal_required:
            print(f"✅ {item}")
        
        print("\n📊 Bu 3 API key ile VUC-2026 tam çalışır!")
        print("🚀 Diğer API'ler opsiyonel iyileştirmeler için.")

def main():
    """Main checker function"""
    checker = APIKeyChecker()
    
    # Durum kontrolü
    working, missing = checker.check_status()
    
    # Öneriler
    checker.get_recommendations(missing)
    
    # Minimal setup
    checker.minimal_setup()
    
    # Özet
    print(f"\n📈 ÖZET:")
    print(f"✅ Çalışan: {len(working)} API key")
    print(f"❌ Eksik: {len(missing)} API key")
    print(f"🎯 Sistem durumu: {'TAM ÇALIŞIR' if len(working) >= 3 else 'EKLEME GEREKLİ'}")

if __name__ == "__main__":
    main()
