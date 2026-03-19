#!/usr/bin/env python3
"""
Vespera-Omni Workspace Setup Script
Otonom video üretim motoru için çalışma ortamı kurulumu
"""

import os
import subprocess
import sys
import platform

def create_vespera_workspace():
    print("🚀 Vespera-Omni Workspace başlatılıyor...")

    # 1. Klasör Hiyerarşisi
    directories = [
        "assets/images",
        "assets/audio", 
        "assets/music",
        "output",
        "core",
        "services",
        "api"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Klasörlerin git'e boş da olsa eklenebilmesi için .gitkeep
        with open(os.path.join(directory, ".gitkeep"), "w") as f:
            pass
        print(f"📁 Oluşturuldu: {directory}")

    # 2. .env Şablonu (API Key'ler için)
    env_content = """# Vespera-Omni Environment Variables
GEMINI_API_KEY=buraya_gemini_api_key_gelecek
ELEVENLABS_API_KEY=buraya_elevenlabs_api_key_gelecek
YOUTUBE_API_KEY=buraya_youtube_api_key_gelecek
MIDJOURNEY_WEBHOOK_URL=opsiyonel_mj_otomasyon_linki
"""
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("⚙️ .env şablonu oluşturuldu.")

    # 3. Requirements Dosyası (Sıfır Hata Render ve API Bağımlılıkları)
    req_content = """# Core AI & API
google-generativeai
fastapi
uvicorn
python-dotenv
requests
pydantic

# Render Engine (Video Kurgu)
moviepy==1.0.3
Pillow
numpy

# Database (Gelecek fazlar için)
sqlalchemy
asyncpg
"""
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(req_content)
    print("📦 requirements.txt oluşturuldu.")

    # 4. Virtual Environment (Sanal Ortam) Kurulumu
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("🐍 Sanal ortam (venv) kuruluyor, lütfen bekleyin...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir])
        print("✅ Sanal ortam başarıyla kuruldu.")
    else:
        print("⚡ Sanal ortam zaten mevcut, atlanıyor.")

    # İşletim sistemine göre aktivasyon komutunu belirle
    is_windows = platform.system() == "Windows"
    activation_cmd = ".\\venv\\Scripts\\activate" if is_windows else "source venv/bin/activate"
    install_cmd = "pip install -r requirements.txt"

    print("\n" + "="*50)
    print("🎉 KURULUM TAMAMLANDI!")
    print("Sistemi ayağa kaldırmak için terminalde sırasıyla şu komutları çalıştırın:")
    print(f"1. {activation_cmd}")
    print(f"2. {install_cmd}")
    print("="*50)

if __name__ == "__main__":
    create_vespera_workspace()
