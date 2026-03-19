#!/usr/bin/env python3
"""
VUC-2026 YouTube Kanal Bağlantı Sistemi
OAuth 2.0 kimlik doğrulama ile kanal yönetimi
"""

import os
import json
import asyncio
import webbrowser
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs
import http.server
import socketserver
import threading
import time
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeChannelConnector:
    """YouTube kanalına OAuth 2.0 ile bağlanma sistemi"""
    
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        # OAuth scopes
        self.scopes = [
            'https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/youtubepartner',
            'https://www.googleapis.com/auth/youtube.force-ssl'
        ]
        
        # Credentials storage
        self.credentials_path = "credentials/youtube_credentials.json"
        self.credentials = None
        
        # Local server for callback
        self.redirect_uri = "http://localhost:8080"
        self.auth_code = None
        
    def create_oauth_flow(self) -> Flow:
        """OAuth 2.0 flow oluştur"""
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
        )
        return flow
    
    def start_local_server(self):
        """OAuth callback için local server başlat"""
        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def __init__(self, connector, *args, **kwargs):
                self.connector = connector
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path.startswith('/?code='):
                    # Authorization code al
                    query = parse_qs(self.path[2:])
                    self.connector.auth_code = query.get('code', [None])[0]
                    
                    # Success response
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    success_html = """
                        <html><body>
                        <h1>VUC-2026 Baglanti Basarili!</h1>
                        <p>YouTube kanaliniza basariyla baglanildi.</p>
                        <p>Bu pencereyi kapatabilirsiniz.</p>
                        </body></html>
                    """.encode('utf-8')
                    self.wfile.write(success_html)
                else:
                    self.send_response(400)
                    self.end_headers()
        
        # Server başlat
        with socketserver.TCPServer(("", 8080), 
                                   lambda *args: CallbackHandler(self, *args)) as httpd:
            print("🌐 OAuth callback server başlatıldı: http://localhost:8080")
            httpd.timeout = 120  # 2 dakika timeout
            
            # Server'ı ayrı thread'de çalıştır
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            return httpd
    
    async def authenticate(self) -> bool:
        """OAuth 2.0 kimlik doğrulama sürecini başlat"""
        print("🚀 VUC-2026 YouTube Kanal Bağlantı Sistemi")
        print("=" * 50)
        
        if not all([self.client_id, self.client_secret]):
            print("❌ Google OAuth kimlik bilgileri eksik!")
            print("Lütfen .env dosyasını kontrol edin:")
            print("- GOOGLE_CLIENT_ID")
            print("- GOOGLE_CLIENT_SECRET")
            return False
        
        # Mevcut credentials kontrol et
        if os.path.exists(self.credentials_path):
            try:
                with open(self.credentials_path, 'r') as f:
                    creds_data = json.load(f)
                self.credentials = Credentials.from_authorized_user_info(creds_data, self.scopes)
                
                # Credentials geçerli mi kontrol et
                if self.credentials.valid:
                    print("✅ Mevcut credentials geçerli!")
                    return await self.test_connection()
                elif self.credentials.expired and self.credentials.refresh_token:
                    print("🔄 Credentials yenileniyor...")
                    self.credentials.refresh(None)
                    await self.save_credentials()
                    return await self.test_connection()
                    
            except Exception as e:
                print(f"⚠️ Mevcut credentials hatalı: {str(e)}")
        
        # Yeni OAuth flow başlat
        print("🔗 Yeni OAuth kimlik doğrulama başlatılıyor...")
        
        # Local server başlat
        httpd = self.start_local_server()
        
        # OAuth flow oluştur
        flow = self.create_oauth_flow()
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        print(f"🌐 Tarayıcı açılıyor: {auth_url}")
        print("Lütfen Google hesabınızla giriş yapın ve VUC-2026'a izin verin.")
        
        # Tarayıcıda aç
        webbrowser.open(auth_url)
        
        # Authorization code bekle
        print("⏳ Kimlik doğrulama kodu bekleniyor...")
        timeout = 120  # 2 dakika
        start_time = time.time()
        
        while self.auth_code is None and (time.time() - start_time) < timeout:
            await asyncio.sleep(1)
        
        if self.auth_code:
            print("✅ Authorization code alındı!")
            
            # Token al
            try:
                flow.fetch_token(code=self.auth_code)
                self.credentials = flow.credentials
                await self.save_credentials()
                
                # Server'ı durdur
                httpd.shutdown()
                
                return await self.test_connection()
                
            except Exception as e:
                print(f"❌ Token alma hatası: {str(e)}")
                return False
        else:
            print("❌ Kimlik doğrulama timeout!")
            httpd.shutdown()
            return False
    
    async def save_credentials(self):
        """Credentials'ı dosyaya kaydet"""
        os.makedirs("credentials", exist_ok=True)
        
        creds_data = {
            'token': self.credentials.token,
            'refresh_token': self.credentials.refresh_token,
            'token_uri': self.credentials.token_uri,
            'client_id': self.credentials.client_id,
            'client_secret': self.credentials.client_secret,
            'scopes': self.credentials.scopes,
            'expiry': self.credentials.expiry.isoformat() if self.credentials.expiry else None
        }
        
        with open(self.credentials_path, 'w') as f:
            json.dump(creds_data, f, indent=2)
        
        print(f"💾 Credentials kaydedildi: {self.credentials_path}")
    
    async def test_connection(self) -> bool:
        """YouTube API bağlantısını test et"""
        try:
            youtube = build('youtube', 'v3', credentials=self.credentials)
            
            # Channel bilgilerini al
            response = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                mine=True
            ).execute()
            
            if 'items' in response and response['items']:
                channel = response['items'][0]
                print(f"✅ YouTube kanalına bağlanıldı!")
                print(f"📺 Kanal: {channel['snippet']['title']}")
                print(f"👥 Aboneler: {channel['statistics'].get('subscriberCount', 'N/A')}")
                print(f"📹 Videolar: {channel['statistics'].get('videoCount', 'N/A')}")
                print(f"👀 Görüntülenme: {channel['statistics'].get('viewCount', 'N/A')}")
                
                # Kanal bilgisini kaydet
                await self.save_channel_info(channel)
                return True
            else:
                print("❌ Kanal bulunamadı!")
                return False
                
        except HttpError as e:
            print(f"❌ YouTube API hatası: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Bağlantı hatası: {str(e)}")
            return False
    
    async def save_channel_info(self, channel_data: Dict[str, Any]):
        """Kanal bilgilerini kaydet"""
        channel_info = {
            'channel_id': channel_data['id'],
            'title': channel_data['snippet']['title'],
            'description': channel_data['snippet']['description'],
            'created_at': channel_data['snippet']['publishedAt'],
            'subscriber_count': int(channel_data['statistics'].get('subscriberCount', 0)),
            'video_count': int(channel_data['statistics'].get('videoCount', 0)),
            'view_count': int(channel_data['statistics'].get('viewCount', 0)),
            'thumbnail_url': channel_data['snippet']['thumbnails']['high']['url']
        }
        
        # Kanal bilgisini VUC memory'e kaydet
        with open('vuc_memory/channel_info.json', 'w') as f:
            json.dump(channel_info, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Kanal bilgileri kaydedildi: vuc_memory/channel_info.json")
    
    async def get_authenticated_service(self):
        """Authenticated YouTube service döndür"""
        if not self.credentials or not self.credentials.valid:
            if not await self.authenticate():
                return None
        
        return build('youtube', 'v3', credentials=self.credentials)

async def main():
    """Ana bağlantı fonksiyonu"""
    connector = YouTubeChannelConnector()
    
    success = await connector.authenticate()
    
    if success:
        print("\n🎉 VUC-2026 YouTube kanal bağlantısı başarılı!")
        print("🚀 Artık video yükleyebilir ve kanalınızı yönetebilirsiniz!")
        
        # Test için service al
        youtube = await connector.get_authenticated_service()
        if youtube:
            print("✅ YouTube API service hazır!")
    else:
        print("\n❌ Kanal bağlantısı başarısız!")
        print("Lütfen OAuth kimlik bilgilerini kontrol edin.")

if __name__ == "__main__":
    asyncio.run(main())
