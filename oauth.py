#!/usr/bin/env python3
"""
VUC-2026 OAuth Helper
Akılda kalıcı OAuth yönetimi - "oauth" komutu ile çalışır
"""

import os
import sys
import asyncio
from datetime import datetime

# Backend path ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from permanent_oauth_manager import PermanentOAuthManager, ensure_youtube_connection

async def main():
    """Ana OAuth helper fonksiyonu"""
    
    # Komut satır argümanlarını kontrol et
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "status"  # Default
    
    manager = PermanentOAuthManager()
    
    print("🚀 VUC-2026 OAuth Helper")
    print("=" * 40)
    
    if command == "setup":
        print("🔧 OAuth kurulumu başlatılıyor...")
        if await manager.initialize():
            print("✅ OAuth başarıyla kuruldu!")
            manager.print_connection_summary()
        else:
            print("❌ OAuth kurulumu başarısız!")
    
    elif command == "test":
        print("🧪 Bağlantı test ediliyor...")
        service = await manager.get_youtube_service()
        if service:
            print("✅ YouTube bağlantısı başarılı!")
            status = await manager.check_connection_status()
            print(f"📊 Durum: {'Authenticated ✅' if status['authenticated'] else 'Not authenticated ❌'}")
        else:
            print("❌ YouTube bağlantısı başarısız!")
    
    elif command == "status":
        print("📊 Bağlantı durumu:")
        status = await manager.check_connection_status()
        
        print(f"🔐 Authenticated: {'✅' if status['authenticated'] else '❌'}")
        print(f"📄 Credentials: {'✅' if status['credentials_exist'] else '❌'}")
        print(f"📺 Channel: {'✅' if status['channel_connected'] else '❌'}")
        
        if status['authenticated']:
            print(f"⏰ Expires soon: {'⚠️' if status['expires_soon'] else '✅'}")
            print(f"🔄 Needs refresh: {'⚠️' if status['needs_refresh'] else '✅'}")
        
        manager.print_connection_summary()
    
    elif command == "connect":
        print("🔗 YouTube bağlantısı sağlanıyor...")
        service = await ensure_youtube_connection()
        if service:
            print("✅ YouTube service hazır!")
            print("🚀 VUC-2026 sistemi kullanıma hazır!")
        else:
            print("❌ YouTube bağlantısı sağlanamadı!")
    
    elif command == "reset":
        print("🔄 Credentials sıfırlanıyor...")
        files = [
            "credentials/youtube_credentials.json",
            "vuc_memory/oauth_session.json",
            "vuc_memory/channel_info.json"
        ]
        
        removed = 0
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ {file_path}")
                removed += 1
        
        if removed > 0:
            print(f"✅ {removed} dosya silindi")
            print("📝 'python oauth.py setup' ile yeniden kurun")
        else:
            print("ℹ️ Silinecek dosya bulunamadı")
    
    else:
        print("📋 Kullanım:")
        print("  python oauth.py setup    - Yeni OAuth kurulumu")
        print("  python oauth.py test     - Bağlantıyı test et")
        print("  python oauth.py status   - Durumu göster")
        print("  python oauth.py connect  - Bağlantı sağla")
        print("  python oauth.py reset    - Credentials'ı sıfırla")
        print("\n🎯 Hızlı başlangıç:")
        print("  python oauth.py          - Durumu göster (default)")

if __name__ == "__main__":
    asyncio.run(main())
