"""
VUC-2026 OAuth Token Generator
Authorization code'dan access token oluştur
"""

import os
import json
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OAuthTokenGenerator:
    """OAuth token oluşturma sınıfı"""
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = 'http://localhost:8080'
        
    def get_access_token(self, authorization_code):
        """Authorization code'dan access token al"""
        
        token_url = 'https://oauth2.googleapis.com/token'
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Token'ı kaydet
                self.save_token(token_data)
                
                print("✅ OAuth Token Başarıyla Oluşturuldu!")
                print("=" * 50)
                print(f"Access Token: {token_data.get('access_token', '')[:30]}...")
                print(f"Refresh Token: {token_data.get('refresh_token', '')[:30]}...")
                print(f"Expires In: {token_data.get('expires_in', 0)} saniye")
                print(f"Token Type: {token_data.get('token_type', 'unknown')}")
                print()
                print("📁 Token kaydedildi: credentials/oauth_token.json")
                
                return token_data
                
            else:
                print(f"❌ Token alma hatası: {response.status_code}")
                print(f"Hata mesajı: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {str(e)}")
            return None
    
    def save_token(self, token_data):
        """Token'ı dosyaya kaydet"""
        os.makedirs('credentials', exist_ok=True)
        
        with open('credentials/oauth_token.json', 'w') as f:
            json.dump(token_data, f, indent=2)
    
    def refresh_access_token(self, refresh_token):
        """Refresh token ile yeni access token al"""
        
        token_url = 'https://oauth2.googleapis.com/token'
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        try:
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.save_token(token_data)
                print("✅ Token başarıyla yenilendi!")
                return token_data
            else:
                print(f"❌ Token yenileme hatası: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {str(e)}")
            return None

def main():
    """Main token generator function"""
    
    # Authorization code'u URL'den çıkar
    auth_url = "http://localhost:8080/?iss=https://accounts.google.com&code=4/0AfrIepDqvNZXxuKdKClOS488GMdoTYBuUvX1jLTtzrAh9VnLIYRO4BvEAESuTqS-eU699A&scope=https://www.googleapis.com/auth/youtube.readonly"
    
    # Code parametresini al
    code_start = auth_url.find('code=') + 5
    code_end = auth_url.find('&', code_start)
    if code_end == -1:
        code_end = len(auth_url)
    
    authorization_code = auth_url[code_start:code_end]
    
    print("🔑 VUC-2026 OAUTH TOKEN GENERATOR")
    print("=" * 50)
    print(f"Authorization Code: {authorization_code[:30]}...")
    print()
    
    # Token generator oluştur
    generator = OAuthTokenGenerator()
    
    # Access token al
    token_data = generator.get_access_token(authorization_code)
    
    if token_data:
        print("\n🚀 VUC-2026 OAuth BAŞARILI!")
        print("Artık YouTube API ile tam entegre!")
        
        # Test et
        print("\n🧪 YouTube API Test:")
        try:
            from backend.app.services.youtube_api_service import YouTubeAPIService
            import asyncio
            
            async def test_oauth():
                service = YouTubeAPIService()
                results = await service.search_videos('bebek gelişimi', max_results=3)
                print(f"✅ OAuth ile video arama: {len(results)} sonuç")
            
            asyncio.run(test_oauth())
            
        except Exception as e:
            print(f"⚠️ API test hatası: {str(e)}")
    else:
        print("\n❌ OAuth başarısız!")

if __name__ == "__main__":
    main()
