"""
VUC-2026 OAuth Console Setup Guide
Google Cloud Console API bağlantısı ile sorunsuz kurulum
"""

import os
import json
import webbrowser
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OAuthConsoleSetup:
    """Google Cloud Console OAuth Setup"""
    
    def __init__(self):
        self.project_id = "karacocuk"
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        
    def open_google_console(self):
        """Google Cloud Console'u aç"""
        console_urls = {
            'oauth_consent': f'https://console.cloud.google.com/apis/credentials/consent?project={self.project_id}',
            'credentials': f'https://console.cloud.google.com/apis/credentials?project={self.project_id}',
            'dashboard': f'https://console.cloud.google.com/apis/dashboard?project={self.project_id}',
            'youtube_api': f'https://console.cloud.google.com/apis/library/youtube.googleapis.com?project={self.project_id}'
        }
        
        print("🔧 GOOGLE CLOUD CONSOLE BAĞLANTILARI:")
        print("=" * 60)
        
        for name, url in console_urls.items():
            print(f"\n📂 {name.upper().replace('_', ' ')}:")
            print(f"   {url}")
        
        return console_urls
    
    def get_oauth_url_fixed(self):
        """Doğru OAuth URL - test user ile"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:8080',
            'scope': 'https://www.googleapis.com/auth/youtube.readonly',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        oauth_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'
        return oauth_url
    
    def setup_instructions(self):
        """Adım adım kurulum talimatları"""
        print("\n🚀 VUC-2026 OAUTH CONSOLE KURULUMU")
        print("=" * 60)
        
        steps = [
            {
                'step': 1,
                'title': 'Google Cloud Console Aç',
                'action': 'OAuth consent screen linkine tıkla',
                'details': 'User Type: External, App name: VUC-2026 YouTube Manager'
            },
            {
                'step': 2,
                'title': 'Test User Ekle',
                'action': 'Test users bölümüne e-posta ekle',
                'details': 'onurkarcck@gmail.com test user olarak ekle'
            },
            {
                'step': 3,
                'title': 'Credentials Oluştur',
                'action': 'Create Credentials > OAuth client ID',
                'details': 'Application type: Web application, Redirect URI: http://localhost:8080'
            },
            {
                'step': 4,
                'title': 'API Key Kontrol',
                'action': 'YouTube Data API v3 aktif et',
                'details': 'Library\'dan YouTube Data API v3\'ü enable et'
            },
            {
                'step': 5,
                'title': 'OAuth Test',
                'action': 'OAuth URL ile giriş yap',
                'details': 'Test user olarak sorunsuz giriş'
            }
        ]
        
        for step in steps:
            print(f"\n📍 ADIM {step['step']}: {step['title']}")
            print(f"   🎯 Aksiyon: {step['action']}")
            print(f"   📝 Detay: {step['details']}")
    
    def quick_fix_oauth(self):
        """Hızlı OAuth düzeltme"""
        print("\n⚡ HIZLI OAUTH DÜZELTME:")
        print("=" * 40)
        
        # Mevcut credentials kontrol
        if self.client_id and self.client_secret:
            print("✅ Mevcut credentials bulundu:")
            print(f"   Client ID: {self.client_id[:20]}...")
            print(f"   Client Secret: {self.client_secret[:10]}...")
            
            # OAuth URL oluştur
            oauth_url = self.get_oauth_url_fixed()
            print(f"\n🔗 TEST OAuth URL:")
            print(oauth_url)
            
            print("\n📋 ADIMLAR:")
            print("1. Bu URL'i kopyala")
            print("2. Tarayıcıda aç")
            print("3. onurkarcck@gmail.com ile giriş")
            print("4. İzinleri ver")
            print("5. Authorization code al")
            
            return oauth_url
        else:
            print("❌ Credentials bulunamadı!")
            print("📝 .env dosyasını kontrol et:")
            print("   GOOGLE_CLIENT_ID")
            print("   GOOGLE_CLIENT_SECRET")
            return None
    
    def create_working_credentials(self):
        """Çalışan credentials oluştur"""
        working_config = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080"]
            }
        }
        
        # credentials.json dosyası oluştur
        os.makedirs('credentials', exist_ok=True)
        with open('credentials/client_secret.json', 'w') as f:
            json.dump(working_config, f, indent=2)
        
        print("🔑 Working credentials oluşturuldu:")
        print("   credentials/client_secret.json")
        
        return working_config

def main():
    """Main setup function"""
    setup = OAuthConsoleSetup()
    
    print("🚀 VUC-2026 OAUTH CONSOLE SETUP")
    print("=" * 50)
    
    # Console linkleri
    setup.open_google_console()
    
    # Kurulum talimatları
    setup.setup_instructions()
    
    # Hızlı düzeltme
    oauth_url = setup.quick_fix_oauth()
    
    # Working credentials
    setup.create_working_credentials()
    
    print("\n🎯 ÖZET:")
    print("1. Google Cloud Console'da test user ekle")
    print("2. OAuth URL ile giriş yap")
    print("3. Authorization code al")
    print("4. VUC-2026 sistemi çalışır")
    
    if oauth_url:
        print(f"\n🔗 Hızlı OAuth Test:")
        print(oauth_url)

if __name__ == "__main__":
    main()
