#!/usr/bin/env python3
"""
VUC-2026 OAuth Quick Setup
Hızlı ve akılda kalıcı OAuth kurulumu
"""

import os
import json
import asyncio
from pathlib import Path

from permanent_oauth_manager import PermanentOAuthManager

class OAuthQuickSetup:
    """Hızlı OAuth kurulum sihirbazı"""
    
    def __init__(self):
        self.manager = PermanentOAuthManager()
    
    async def run_setup(self):
        """OAuth kurulum sihirbazını çalıştır"""
        print("🚀 VUC-2026 OAuth Hızlı Kurulum Sihirbazı")
        print("=" * 60)
        print("📋 Bu sihirbaz size kalıcı OAuth bağlantısı kuracaktır.")
        print("🔄 Sadece bir kez yapılacak, sonrasında otomatik bağlanılacak!")
        print()
        
        # 1. Durum kontrolü
        await self._check_current_status()
        
        # 2. Kurulum seçimi
        choice = input("\n🔧 Ne yapmak istersiniz?\n"
                       "1. Yeni OAuth kurulumu\n"
                       "2. Mevcut bağlantıyı test et\n"
                       "3. Bağlantı durumunu göster\n"
                       "4. Credentials'ı sıfırla\n"
                       "Seçiminiz (1-4): ").strip()
        
        if choice == "1":
            await self._setup_new_oauth()
        elif choice == "2":
            await self._test_connection()
        elif choice == "3":
            await self._show_status()
        elif choice == "4":
            await self._reset_credentials()
        else:
            print("❌ Geçersiz seçim!")
    
    async def _check_current_status(self):
        """Mevcut durumu kontrol et"""
        print("🔍 Mevcut durum kontrol ediliyor...")
        
        # Credentials dosyası
        creds_exist = os.path.exists(self.manager.credentials_path)
        session_exist = os.path.exists(self.manager.session_path)
        channel_exist = os.path.exists(self.manager.channel_path)
        
        print(f"📄 Credentials dosyası: {'✅' if creds_exist else '❌'}")
        print(f"📋 Session bilgisi: {'✅' if session_exist else '❌'}")
        print(f"📺 Kanal bilgisi: {'✅' if channel_exist else '❌'}")
        
        if creds_exist and session_exist:
            try:
                with open(self.manager.session_path, 'r') as f:
                    session = json.load(f)
                
                status = session.get('status', 'unknown')
                last_auth = session.get('last_authenticated', 'Bilinmiyor')
                
                print(f"🔐 Durum: {status}")
                print(f"📅 Son authentication: {last_auth}")
                
                if status == 'authenticated':
                    print("✅ OAuth bağlantısı hazır!")
                else:
                    print("⚠️ OAuth bağlantısı kurulum gerektiriyor")
                    
            except:
                print("⚠️ Session dosyası okunamadı")
        else:
            print("📝 OAuth kurulumu gerekli")
    
    async def _setup_new_oauth(self):
        """Yeni OAuth kurulumu"""
        print("\n🔗 Yeni OAuth kurulumu başlatılıyor...")
        
        # Environment kontrol
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            print("\n❌ Google OAuth kimlik bilgileri eksik!")
            print("📋 Lütfen aşağıdaki bilgileri girin:")
            
            if not client_id:
                client_id = input("🔑 Google Client ID: ").strip()
                os.environ["GOOGLE_CLIENT_ID"] = client_id
            
            if not client_secret:
                client_secret = input("🔒 Google Client Secret: ").strip()
                os.environ["GOOGLE_CLIENT_SECRET"] = client_secret
            
            # .env dosyasına kaydet
            await self._save_env_file(client_id, client_secret)
        
        # Manager'ı güncelle
        self.manager.client_id = client_id
        self.manager.client_secret = client_secret
        
        # Authentication yap
        if await self.manager.initialize():
            print("\n🎉 OAuth kurulumu başarıyla tamamlandı!")
            self.manager.print_connection_summary()
        else:
            print("\n❌ OAuth kurulumu başarısız!")
    
    async def _save_env_file(self, client_id: str, client_secret: str):
        """Environment bilgilerini .env dosyasına kaydet"""
        env_content = f"""# VUC-2026 Google OAuth Configuration
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}
GOOGLE_CLOUD_PROJECT=karacocuk
YOUTUBE_API_KEY=AIzaSyDBiY-TjMaXQZw2Mfb9iNB2ld44YmHZBJc
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("💾 Environment bilgileri .env dosyasına kaydedildi")
    
    async def _test_connection(self):
        """Bağlantıyı test et"""
        print("\n🧪 YouTube bağlantısı test ediliyor...")
        
        service = await self.manager.get_youtube_service()
        
        if service:
            try:
                # Channel test
                response = service.channels().list(
                    part='snippet,statistics',
                    mine=True
                ).execute()
                
                if 'items' in response:
                    channel = response['items'][0]
                    print(f"✅ Bağlantı başarılı!")
                    print(f"📺 Kanal: {channel['snippet']['title']}")
                    print(f"👥 Aboneler: {channel['statistics'].get('subscriberCount', 0):,}")
                else:
                    print("❌ Kanal bulunamadı!")
                    
            except Exception as e:
                print(f"❌ Bağlantı test hatası: {str(e)}")
        else:
            print("❌ YouTube service oluşturulamadı!")
    
    async def _show_status(self):
        """Bağlantı durumunu göster"""
        print("\n📊 OAuth Bağlantı Durumu")
        print("=" * 40)
        
        status = await self.manager.check_connection_status()
        
        print(f"🔐 Authenticated: {'✅' if status['authenticated'] else '❌'}")
        print(f"📄 Credentials exist: {'✅' if status['credentials_exist'] else '❌'}")
        print(f"📺 Channel connected: {'✅' if status['channel_connected'] else '❌'}")
        print(f"⏰ Expires soon: {'⚠️' if status['expires_soon'] else '✅'}")
        print(f"🔄 Needs refresh: {'⚠️' if status['needs_refresh'] else '✅'}")
        
        self.manager.print_connection_summary()
    
    async def _reset_credentials(self):
        """Credentials'ı sıfırla"""
        print("\n🔄 Credentials sıfırlanıyor...")
        
        # Dosyaları sil
        files_to_remove = [
            self.manager.credentials_path,
            self.manager.session_path,
            self.manager.channel_path
        ]
        
        removed_count = 0
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ {file_path} silindi")
                removed_count += 1
        
        if removed_count > 0:
            print(f"✅ {removed_count} dosya silindi")
            print("📝 Yeni OAuth kurulumu yapmanız gerekecek")
        else:
            print("ℹ️ Silinecek credentials dosyası bulunamadı")

async def main():
    """Ana fonksiyon"""
    setup = OAuthQuickSetup()
    await setup.run_setup()

if __name__ == "__main__":
    asyncio.run(main())
