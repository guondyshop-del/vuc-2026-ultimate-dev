#!/usr/bin/env python3
"""
VUC-2026 OAuth Callback Handler
Google OAuth callback URL'den authorization code'i işler
"""

import os
import json
import sys
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

def handle_oauth_callback(callback_url: str):
    """OAuth callback URL'ini işle ve credentials oluştur"""
    
    print("🚀 VUC-2026 OAuth Callback Handler")
    print("=" * 50)
    
    # Google OAuth bilgileri
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    if not all([client_id, client_secret]):
        print("❌ Google OAuth kimlik bilgileri eksik!")
        print("Lütfen .env dosyasını kontrol edin:")
        print("- GOOGLE_CLIENT_ID")
        print("- GOOGLE_CLIENT_SECRET")
        return False
    
    # OAuth scopes
    scopes = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtubepartner',
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ]
    
    # Redirect URI
    redirect_uri = "http://127.0.0.1:8002/auth/callback"
    
    try:
        # Callback URL'den authorization code'i çıkar
        parsed_url = urlparse(callback_url)
        query_params = parse_qs(parsed_url.query)
        
        # Authorization code'i al
        if 'code' in query_params:
            auth_code = query_params['code'][0]
            print(f"✅ Authorization code alındı: {auth_code[:50]}...")
        else:
            print("❌ Callback URL'de authorization code bulunamadı!")
            return False
        
        # OAuth flow oluştur
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=scopes,
            redirect_uri=redirect_uri
        )
        
        # Token al
        print("🔄 Access token alınıyor...")
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        
        # Credentials'ı kaydet
        os.makedirs("credentials", exist_ok=True)
        
        creds_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
        
        credentials_path = "credentials/youtube_credentials.json"
        with open(credentials_path, 'w') as f:
            json.dump(creds_data, f, indent=2)
        
        print(f"💾 Credentials kaydedildi: {credentials_path}")
        
        # Connection test
        print("🧪 YouTube API bağlantısı test ediliyor...")
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Channel bilgilerini al
        response = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            mine=True
        ).execute()
        
        if 'items' in response and response['items']:
            channel = response['items'][0]
            print(f"\n✅ YouTube kanalına başarıyla bağlanıldı!")
            print(f"📺 Kanal: {channel['snippet']['title']}")
            print(f"👥 Aboneler: {channel['statistics'].get('subscriberCount', 'N/A')}")
            print(f"📹 Videolar: {channel['statistics'].get('videoCount', 'N/A')}")
            print(f"👀 Görüntülenme: {channel['statistics'].get('viewCount', 'N/A')}")
            
            # Kanal bilgisini kaydet
            channel_info = {
                'channel_id': channel['id'],
                'title': channel['snippet']['title'],
                'description': channel['snippet']['description'],
                'created_at': channel['snippet']['publishedAt'],
                'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                'video_count': int(channel['statistics'].get('videoCount', 0)),
                'view_count': int(channel['statistics'].get('viewCount', 0)),
                'thumbnail_url': channel['snippet']['thumbnails']['high']['url']
            }
            
            os.makedirs("vuc_memory", exist_ok=True)
            with open('vuc_memory/channel_info.json', 'w', encoding='utf-8') as f:
                json.dump(channel_info, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Kanal bilgileri kaydedildi: vuc_memory/channel_info.json")
            
            print("\n🎉 VUC-2026 YouTube kanal bağlantısı tamamlandı!")
            print("🚀 Artık video yükleyebilir ve kanalınızı yönetebilirsiniz!")
            
            return True
        else:
            print("❌ Kanal bulunamadı!")
            return False
            
    except Exception as e:
        print(f"❌ OAuth callback işleme hatası: {str(e)}")
        return False

if __name__ == "__main__":
    # Komut satırından callback URL'ini al
    if len(sys.argv) > 1:
        callback_url = sys.argv[1]
    else:
        # Manuel giriş
        callback_url = input("📋 OAuth callback URL'ini yapıştırın: ").strip()
    
    if callback_url:
        handle_oauth_callback(callback_url)
    else:
        print("❌ Callback URL girilmedi!")
