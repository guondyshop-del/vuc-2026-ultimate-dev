"""
VUC-2026 YouTube OAuth Fix
Quick bypass for Google OAuth verification issues
"""

import os
import json
import webbrowser
from urllib.parse import urlencode, quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeOAuthBypass:
    """Quick OAuth bypass for development/testing"""
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        
    def get_oauth_url_testing(self):
        """Testing OAuth URL with verified app parameters"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:8080',
            'scope': 'https://www.googleapis.com/auth/youtube.readonly',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        oauth_url = f'{base_url}?{urlencode(params)}'
        
        return oauth_url
    
    def use_api_key_instead(self):
        """Use API Key instead of OAuth for basic operations"""
        print("🔑 API Key ile Devam Etme Seçeneği:")
        print(f"YouTube API Key: {self.api_key[:20]}...")
        print()
        print("✅ API Key ile yapabilecekleriniz:")
        print("- Video arama")
        print("- Video detayları")
        print("- Kanal bilgileri")
        print("- Trend videolar")
        print("- Kategori listesi")
        print()
        print("❌ API Key ile yapamayacaklarınız:")
        print("- Video upload")
        print("- Kanal yönetimi")
        print("- Yorum yapma")
        print("- Beğeni/like işlemleri")
        print()
        return self.api_key
    
    def create_test_credentials(self):
        """Create test credentials for development"""
        test_creds = {
            "token": "test_token",
            "refresh_token": "test_refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": ["https://www.googleapis.com/auth/youtube.readonly"]
        }
        
        # Save test credentials
        os.makedirs('credentials', exist_ok=True)
        with open('credentials/test_oauth.json', 'w') as f:
            json.dump(test_creds, f, indent=2)
        
        print("🧪 Test credentials oluşturuldu:")
        print("credentials/test_oauth.json")
        return test_creds

def main():
    """Main OAuth bypass function"""
    oauth_bypass = YouTubeOAuthBypass()
    
    print("🚀 VUC-2026 OAuth BYPASS SİSTEMİ")
    print("=" * 50)
    print()
    
    print("🔧 SEÇENEKLER:")
    print("1. API Key ile devam et (Önerilen)")
    print("2. Test credentials oluştur")
    print("3. Google Cloud Console'da app doğrula")
    print()
    
    choice = input("Seçiminiz (1-3): ").strip()
    
    if choice == "1":
        print("\n✅ API Key modu aktif:")
        oauth_bypass.use_api_key_instead()
        
    elif choice == "2":
        print("\n🧪 Test credentials oluşturuluyor:")
        oauth_bypass.create_test_credentials()
        
    elif choice == "3":
        print("\n📋 Google Cloud Console DOĞRULAMA ADIMLARI:")
        print("1. https://console.cloud.google.com/ adresine gidin")
        print("2. 'karacocuk' projesini seçin")
        print("3. APIs & Services > OAuth consent screen'e gidin")
        print("4. 'Publishing app' olarak ayarlayın")
        print("5. Gerekli alanları doldurun:")
        print("   - App name: VUC-2026 YouTube Manager")
        print("   - User support email: onurkarcck@gmail.com")
        print("   - Developer contact: onurkarcck@gmail.com")
        print("6. Scopes ekleyin:")
        print("   - ../auth/youtube.readonly")
        print("   - ../auth/youtube.upload")
        print("7. Test users ekleyin:")
        print("   - onurkarcck@gmail.com")
        print("8. Save ve Publish edin")
        print()
        print("⏳ Doğrulama 3-5 gün sürebilir!")
        
    else:
        print("❌ Geçersiz seçenek!")

if __name__ == "__main__":
    main()
