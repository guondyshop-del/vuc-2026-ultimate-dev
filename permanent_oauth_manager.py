#!/usr/bin/env python3
"""
VUC-2026 Permanent OAuth Manager
Sürekli OAuth problemlerini çözen kalıcı çözüm
"""

import os
import json
import asyncio
import webbrowser
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class PermanentOAuthManager:
    """Kalıcı OAuth yönetimi - sürekli bağlantı sağlar"""
    
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        # OAuth scopes
        self.scopes = [
            'https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/youtubepartner',
            'https://www.googleapis.com/auth/youtube.force-ssl'
        ]
        
        # File paths
        self.credentials_path = "credentials/youtube_credentials.json"
        self.session_path = "vuc_memory/oauth_session.json"
        self.channel_path = "vuc_memory/channel_info.json"
        
        # Redirect URI
        self.redirect_uri = "http://127.0.0.1:8002/auth/callback"
        
        # Session state
        self.credentials = None
        self.youtube_service = None
        self.channel_info = None
        
    async def initialize(self) -> bool:
        """OAuth sistemini başlat ve bağlantıyı sağla"""
        print("🚀 VUC-2026 Permanent OAuth Manager")
        print("=" * 60)
        print("🔄 Sürekli OAuth bağlantısı başlatılıyor...")
        
        # 1. Environment kontrol
        if not await self._check_environment():
            return False
        
        # 2. Mevcut credentials kontrol ve yükle
        if await self._load_existing_credentials():
            return True
        
        # 3. Yeni authentication gerekirse
        return await self._perform_authentication()
    
    async def _check_environment(self) -> bool:
        """Environment variables kontrol et"""
        if not all([self.client_id, self.client_secret]):
            print("❌ OAuth kimlik bilgileri eksik!")
            print("📋 Gerekli environment variables:")
            print("   - GOOGLE_CLIENT_ID")
            print("   - GOOGLE_CLIENT_SECRET")
            print("\n🔧 .env dosyasını kontrol edin veya:")
            print("   set GOOGLE_CLIENT_ID=your_client_id")
            print("   set GOOGLE_CLIENT_SECRET=your_client_secret")
            return False
        
        print("✅ Environment variables kontrol edildi")
        return True
    
    async def _load_existing_credentials(self) -> bool:
        """Mevcut credentials'ı yükle ve doğrula"""
        # Credentials dosyası var mı?
        if not os.path.exists(self.credentials_path):
            print("📄 Credentials dosyası bulunamadı")
            return False
        
        try:
            # Credentials yükle
            with open(self.credentials_path, 'r') as f:
                creds_data = json.load(f)
            
            self.credentials = Credentials.from_authorized_user_info(creds_data, self.scopes)
            
            # Session bilgisini kaydet
            await self._save_session_info()
            
            # Credentials geçerli mi?
            if self.credentials.valid:
                print("✅ Mevcut credentials geçerli")
                return await self._test_connection()
            
            # Credentials expired ama refresh token var mı?
            elif self.credentials.expired and self.credentials.refresh_token:
                print("🔄 Credentials expired, yenileniyor...")
                return await self._refresh_credentials()
            
            else:
                print("⚠️ Credentials geçersiz, yeni authentication gerekli")
                return False
                
        except Exception as e:
            print(f"❌ Credentials yükleme hatası: {str(e)}")
            return False
    
    async def _refresh_credentials(self) -> bool:
        """Credentials'ı yenile"""
        try:
            self.credentials.refresh(None)
            await self._save_credentials()
            print("✅ Credentials başarıyla yenilendi")
            return await self._test_connection()
        except Exception as e:
            print(f"❌ Credentials yenileme hatası: {str(e)}")
            print("🔄 Yeni authentication gerekli")
            return False
    
    async def _perform_authentication(self) -> bool:
        """Yeni OAuth authentication süreci"""
        print("\n🔗 Yeni OAuth authentication başlatılıyor...")
        print("📋 Bu işlem sadece bir kez yapılacak, sonrasında otomatik bağlanılacak")
        
        # OAuth flow oluştur
        flow = self._create_oauth_flow()
        
        # Authorization URL oluştur
        auth_url, state = flow.authorization_url(
            access_type='offline',  # Refresh token için
            include_granted_scopes='true',
            prompt='consent',  # Her zaman consent iste
            code_challenge=None,
            code_challenge_method=None
        )
        
        print(f"\n🌐 Lütfen aşağıdaki URL'yi açın:")
        print(f"🔗 {auth_url}")
        print(f"\n📋 State: {state}")
        
        # Tarayıcıda aç
        try:
            webbrowser.open(auth_url)
            print("🌐 Tarayıcı otomatik açıldı")
        except:
            print("⚠️ Tarayıcı açılamadı, URL'yi manuel kopyalayın")
        
        print("\n📝 Google hesabınızla giriş yapın ve izin verin")
        print("🔄 İzin verdikten sonra callback URL'ini kopyalayın")
        print("📤 Callback URL formatı: http://127.0.0.1:8002/auth/callback?code=...")
        
        # Manuel authorization code al
        callback_url = input("\n⌨️ Callback URL'ini yapıştırın: ").strip()
        
        if callback_url:
            return await self._handle_callback(callback_url, flow)
        else:
            print("❌ Callback URL girilmedi!")
            return False
    
    def _create_oauth_flow(self) -> Flow:
        """OAuth flow oluştur"""
        return Flow.from_client_config(
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
    
    async def _handle_callback(self, callback_url: str, flow: Flow) -> bool:
        """OAuth callback işle"""
        try:
            from urllib.parse import urlparse, parse_qs
            
            # URL'den code'i çıkar
            parsed_url = urlparse(callback_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'code' not in query_params:
                print("❌ Callback URL'de authorization code bulunamadı!")
                return False
            
            auth_code = query_params['code'][0]
            print(f"✅ Authorization code alındı")
            
            # Token al
            flow.fetch_token(code=auth_code)
            self.credentials = flow.credentials
            
            # Credentials kaydet
            await self._save_credentials()
            
            # Session kaydet
            await self._save_session_info()
            
            # Bağlantı test
            return await self._test_connection()
            
        except Exception as e:
            print(f"❌ Callback işleme hatası: {str(e)}")
            return False
    
    async def _save_credentials(self):
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
    
    async def _save_session_info(self):
        """Session bilgisini kaydet"""
        os.makedirs("vuc_memory", exist_ok=True)
        
        session_info = {
            'last_authenticated': datetime.now().isoformat(),
            'expires_at': self.credentials.expiry.isoformat() if self.credentials.expiry else None,
            'has_refresh_token': bool(self.credentials.refresh_token),
            'client_id': self.client_id,
            'scopes': self.scopes,
            'status': 'authenticated' if self.credentials.valid else 'expired'
        }
        
        with open(self.session_path, 'w') as f:
            json.dump(session_info, f, indent=2)
    
    async def _test_connection(self) -> bool:
        """YouTube API bağlantısını test et"""
        try:
            # YouTube service oluştur
            self.youtube_service = build('youtube', 'v3', credentials=self.credentials)
            
            # Channel bilgilerini al
            response = self.youtube_service.channels().list(
                part='snippet,contentDetails,statistics',
                mine=True
            ).execute()
            
            if 'items' in response and response['items']:
                channel = response['items'][0]
                self.channel_info = channel
                
                # Channel bilgisini kaydet
                await self._save_channel_info(channel)
                
                print(f"\n✅ YouTube kanalına başarıyla bağlanıldı!")
                print(f"📺 Kanal: {channel['snippet']['title']}")
                print(f"👥 Aboneler: {channel['statistics'].get('subscriberCount', 'N/A')}")
                print(f"📹 Videolar: {channel['statistics'].get('videoCount', 'N/A')}")
                print(f"👀 Görüntülenme: {channel['statistics'].get('viewCount', 'N/A')}")
                
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
    
    async def _save_channel_info(self, channel_data: Dict[str, Any]):
        """Kanal bilgilerini kaydet"""
        channel_info = {
            'channel_id': channel_data['id'],
            'title': channel_data['snippet']['title'],
            'description': channel_data['snippet']['description'],
            'created_at': channel_data['snippet']['publishedAt'],
            'subscriber_count': int(channel_data['statistics'].get('subscriberCount', 0)),
            'video_count': int(channel_data['statistics'].get('videoCount', 0)),
            'view_count': int(channel_data['statistics'].get('viewCount', 0)),
            'thumbnail_url': channel_data['snippet']['thumbnails']['high']['url'],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.channel_path, 'w', encoding='utf-8') as f:
            json.dump(channel_info, f, indent=2, ensure_ascii=False)
    
    async def get_youtube_service(self):
        """Authenticated YouTube service döndür"""
        if not self.credentials or not self.credentials.valid:
            if not await self.initialize():
                return None
        
        if not self.youtube_service:
            self.youtube_service = build('youtube', 'v3', credentials=self.credentials)
        
        return self.youtube_service
    
    async def check_connection_status(self) -> Dict[str, Any]:
        """Bağlantı durumunu kontrol et"""
        status = {
            'authenticated': False,
            'credentials_exist': os.path.exists(self.credentials_path),
            'channel_connected': False,
            'expires_soon': False,
            'needs_refresh': False
        }
        
        if self.credentials and self.credentials.valid:
            status['authenticated'] = True
            status['channel_connected'] = bool(self.channel_info)
            
            # 24 saat içinde mi expire oluyor?
            if self.credentials.expiry:
                time_until_expiry = self.credentials.expiry - datetime.now()
                if time_until_expiry.total_seconds() < 86400:  # 24 saat
                    status['expires_soon'] = True
                
                if time_until_expiry.total_seconds() < 3600:  # 1 saat
                    status['needs_refresh'] = True
        
        return status
    
    def print_connection_summary(self):
        """Bağlantı özetini yazdır"""
        print("\n" + "="*60)
        print("📊 VUC-2026 OAuth Bağlantı Özeti")
        print("="*60)
        
        # Session bilgisi
        if os.path.exists(self.session_path):
            with open(self.session_path, 'r') as f:
                session = json.load(f)
            
            print(f"🔐 Son Authentication: {session.get('last_authenticated', 'Bilinmiyor')}")
            print(f"⏰ Expire Tarihi: {session.get('expires_at', 'Bilinmiyor')}")
            print(f"🔄 Refresh Token: {'✅' if session.get('has_refresh_token') else '❌'}")
        
        # Kanal bilgisi
        if os.path.exists(self.channel_path):
            with open(self.channel_path, 'r', encoding='utf-8') as f:
                channel = json.load(f)
            
            print(f"\n📺 Kanal: {channel.get('title', 'Bilinmiyor')}")
            print(f"👥 Aboneler: {channel.get('subscriber_count', 0):,}")
            print(f"📹 Videolar: {channel.get('video_count', 0):,}")
            print(f"👀 Görüntülenme: {channel.get('view_count', 0):,}")
        
        print("\n🎯 Not: Bu bağlantı kalıcıdır. Tekrar authentication gerekmez!")
        print("🚀 VUC-2026 sistemi artık otomatik olarak YouTube'a bağlanabilir.")

# Global instance
_oauth_manager = None

async def get_oauth_manager() -> PermanentOAuthManager:
    """Global OAuth manager instance döndür"""
    global _oauth_manager
    if _oauth_manager is None:
        _oauth_manager = PermanentOAuthManager()
    return _oauth_manager

async def ensure_youtube_connection():
    """YouTube bağlantısını guarantee et"""
    manager = await get_oauth_manager()
    service = await manager.get_youtube_service()
    if service:
        print("✅ YouTube bağlantısı hazır!")
        return service
    else:
        print("❌ YouTube bağlantısı kurulamadı!")
        return None

if __name__ == "__main__":
    async def main():
        manager = PermanentOAuthManager()
        
        if await manager.initialize():
            manager.print_connection_summary()
            print("\n🎉 VUC-2026 OAuth sistemi kalıcı olarak kuruldu!")
        else:
            print("\n❌ OAuth kurulumu başarısız!")
    
    asyncio.run(main())
