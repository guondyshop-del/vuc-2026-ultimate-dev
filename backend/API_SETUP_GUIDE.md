# VUC-2026 External API Setup Guide

## 🚀 Production API Anahtarları Kurulum Rehberi

VUC-2026 sisteminin production modda çalışması için aşağıdaki external servislerin API anahtarlarını yapılandırmanız gerekmektedir.

## 📋 Gerekli API Anahtarları

### 1. Google Cloud / Gemini API
- **Amaç**: Video script'leri için AI içerik üretimi
- **URL**: https://console.cloud.google.com/apis/credentials
- **Adımlar**:
  1. Google Cloud Console'a gidin
  2. Yeni proje oluşturun: `vuc-2026-production`
  3. Gemini API'yi etkinleştirin
  4. API anahtarı oluşturun
  5. `.env.production` dosyasına ekleyin

### 2. ElevenLabs API
- **Amaç**: Video seslendirmesi (text-to-speech)
- **URL**: https://elevenlabs.io/app/settings/api-keys
- **Adımlar**:
  1. ElevenLabs hesabına giriş yapın
  2. Settings > API Keys bölümüne gidin
  3. Yeni API anahtarı oluşturun
  4. Voice ID'leri kontrol edin (rachel, adam, bella)

### 3. YouTube Data API v3
- **Amaç**: Video yükleme ve analiz
- **URL**: https://console.cloud.google.com/apis/credentials
- **Adımlar**:
  1. Google Cloud Console'da YouTube Data API v3'ü etkinleştirin
  2. OAuth 2.0 credentials oluşturun
  3. Client ID ve Client Secret alın
  4. YouTube kanalınızı bağlayın

### 4. Amazon Affiliate API
- **Amaç**: Ürün yerleştirme ve affiliate gelir
- **URL**: https://affiliate-program.amazon.com/
- **Adımlar**:
  1. Amazon Associates hesabı oluşturun
  2. Product Advertising API'ye başvurun
  3. Access Key ID ve Secret Access Key alın
  4. Associate tag oluşturun

### 5. Ahrefs API
- **Amaç**: SEO analizi ve competitor intelligence
- **URL**: https://ahrefs.com/api/documentation
- **Adımlar**:
  1. Ahrefs hesabına giriş yapın
  2. API access başvurusu yapın
  3. API token'ı alın

## 🔧 Kurulum Adımları

### 1. Environment Dosyasını Oluşturun
```bash
# Backend dizininde
cd backend
python setup_production_keys.py
```

### 2. API Anahtarlarını Yapılandırın
`.env.production` dosyasını düzenleyin ve placeholder'ları gerçek anahtarlarla değiştirin:

```bash
# Örnek yapılandırma
GOOGLE_API_KEY=AIzaSySyR8y8h8h8h8h8h8h8h8h8h8h8h8h8h8h
ELEVENLABS_API_KEY=sk-elevenlabs_1a2b3c4d5e6f7g8h9i0j
YOUTUBE_API_KEY=AIzaSyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6
AMAZON_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AMAZON_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AHREFS_API_TOKEN=ahrefs-token-1234567890abcdef
```

### 3. Bağlantıları Test Edin
```bash
python test_api_connections.py
```

### 4. Veritabanını Kurun
```bash
# PostgreSQL kurulumu
sudo apt-get install postgresql postgresql-contrib

# Veritabanı ve kullanıcı oluşturma
sudo -u postgres psql
CREATE DATABASE vuc2026_production;
CREATE USER vuc2026 WITH PASSWORD 'guvenli_sifre';
GRANT ALL PRIVILEGES ON DATABASE vuc2026_production TO vuc2026;
\q

# Redis kurulumu
sudo apt-get install redis-server
```

### 5. Production Server'ı Başlatın
```bash
# Production modda başlat
export ENVIRONMENT=production
python -m app.main
```

## 🧪 Test ve Doğrulama

### API Connection Test
```bash
python test_api_connections.py
```

### Health Check
```bash
curl http://localhost:8002/health
```

### API Endpoint Test
```bash
curl http://localhost:8002/api/family-kids-empire/status
```

## 📊 Monitoring

### Log Monitoring
```bash
# Real-time log izleme
tail -f logs/vuc2026.log

# Error log izleme
tail -f logs/errors.log
```

### Performance Monitoring
- CPU kullanımı: < 90%
- Memory kullanımı: < 85%
- API response time: < 5000ms
- Error rate: < 15%

## 🛡️ Güvenlik

### API Anahtarı Güvenliği
- Asla API anahtarlarını GitHub'a yüklemeyin
- `.env.production` dosyasını `.gitignore`'a ekleyin
- Düzenli olarak API anahtarlarını rotate edin
- IP whitelisting kullanın

### Environment Variables
```bash
# .gitignore dosyasına ekleyin
.env.production
.env.local
api_keys.json
```

## 🔄 Maintenance

### Günlük Kontroller
1. API health check
2. Veritabanı bağlantısı
3. Redis bağlantısı
4. Disk alanı
5. Memory kullanımı

### Haftalık Bakım
1. Log rotation
2. Cache temizleme
3. Backup kontrolü
4. API anahtarı güvenlik kontrolü

## 🚨 Troubleshooting

### Yaygın Sorunlar

#### 1. API Anahtarı Hataları
- **Sorun**: 401/403 hataları
- **Çözüm**: API anahtarlarını kontrol edin ve yenileyin

#### 2. Rate Limiting
- **Sorun**: 429 hataları
- **Çözüm**: Rate limit ayarlarını optimize edin

#### 3. Network Issues
- **Sorun**: Connection timeout
- **Çözüm**: Proxy ve firewall ayarlarını kontrol edin

#### 4. Database Issues
- **Sorun**: Connection refused
- **Çözüm**: PostgreSQL servisinin çalıştığını kontrol edin

## 📞 Destek

Sorun yaşarsanız:
1. Logları kontrol edin
2. API test script'ini çalıştırın
3. Configuration'ı doğrulayın
4. Documentation'ı inceleyin

---

**🎯 Hedef**: VUC-2026 sisteminin tam production kapasitesinde çalışması
**📈 Başarı Oranı**: %99+ uptime
**🔧 Destek**: 24/7 monitoring
