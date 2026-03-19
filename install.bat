@echo off
echo VUC-2026 Otomatik Kurulum Baslatiliyor...
echo.

:: Python kontrol ve kurulum
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.11+ bulunamadi. Kuruluyor...
    winget install Python.Python.3.11
    echo Python yuklendikten sonra bu dosyayi tekrar calistirin.
    pause
    exit
)

:: Node.js kontrol ve kurulum
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js bulunamadi. Kuruluyor...
    winget install OpenJS.NodeJS
    echo Node.js yuklendikten sonra bu dosyayi tekrar calistirin.
    pause
    exit
)

:: FFmpeg kontrol ve kurulum
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg bulunamadi. Kuruluyor...
    winget install Gyan.FFmpeg
    echo FFmpeg yuklendikten sonra bu dosyayi tekrar calistirin.
    pause
    exit
)

:: Redis kontrol ve kurulum
redis-cli --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Redis bulunamadi. Kuruluyor...
    winget install Redis.Redis
)

:: Backend kurulum
echo Backend kurulumu baslatiliyor...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install fastapi uvicorn celery redis sqlalchemy python-multipart python-jose[cryptography] passlib[bcrypt] python-decouple yt-dlp google-generativeai edge-tts ffmpeg-python pillow requests beautifulsoup4 selenium pandas numpy matplotlib opencv-python

:: Veritabani baslatma
echo Veritabani baslatiliyor...
python -c "from app.database import init_db; init_db()"

:: Frontend kurulum
echo Frontend kurulumu baslatiliyor...
cd ..\frontend
npm init -y
npm install next@14 react react-dom tailwindcss framer-motion @types/node @types/react @types/recharts axios lucide-react
npx tailwindcss init -p

:: Gerekli dosyalari olustur
echo Gerekli konfigurasyon dosyalari olusturuluyor...

:: Redis baslatma
echo Redis baslatiliyor...
start /B redis-server

echo.
echo =====================================
echo VUC-2026 Kurulum Tamamlandi!
echo =====================================
echo.
echo Sistemi baslatmak icin:
echo 1. Backend: cd backend && venv\Scripts\activate && uvicorn app.main:app --reload
echo 2. Frontend: cd frontend && npm run dev
echo 3. Redis: redis-server (arka planda calisiyor)
echo.
echo Tarayicinizda acin: http://localhost:3000
echo API Dokumantasyonu: http://localhost:8000/docs
echo.
pause
