"""
VUC-2026 Database Initialization
Örnek kanallar ve verilerle veritabanını başlatma
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from ..database import SessionLocal, engine, Base
from ..models.channel import Channel
from ..models.video import Video
from ..models.script import Script

logger = logging.getLogger(__name__)

def create_sample_channels():
    """Örnek kanallar oluştur"""
    db = SessionLocal()
    
    try:
        # Örnek kanallar
        sample_channels = [
            {
                "name": "Kripto Analist",
                "channel_id": "cryptoanalist2026",
                "niche": "Crypto",
                "language": "TR",
                "target_audience": "Kripto yatırımcıları ve meraklıları",
                "description": "Kripto para piyasası analizleri, tahminleri ve yatırım stratejileri",
                "keywords": ["bitcoin", "altcoin", "blockchain", "kripto para", "yatırım", "değişim"],
                "is_active": True,
                "auto_upload": True,
                "upload_schedule": {
                    "monday": ["09:00", "14:00", "19:00"],
                    "tuesday": ["09:00", "14:00", "19:00"],
                    "wednesday": ["09:00", "14:00", "19:00"],
                    "thursday": ["09:00", "14:00", "19:00"],
                    "friday": ["09:00", "14:00", "19:00"],
                    "saturday": ["10:00", "15:00", "20:00"],
                    "sunday": ["10:00", "15:00", "20:00"]
                },
                "daily_upload_target": 3,
                "target_views_per_video": 15000,
                "competitor_analysis_enabled": True,
                "api_key": "AIzaSyDemoKey_CryptoAnalyst2026",
                "client_secret": "demo_client_secret_crypto"
            },
            {
                "name": "Bebek Gelişim Uzmanı",
                "channel_id": "bebekgelisim2026",
                "niche": "Babies",
                "language": "TR",
                "target_audience": "Yeni ebeveynler ve bebek bakımıyla ilgilenenler",
                "description": "Bebek bakımı, gelişim, ebeveynlik ipuçları ve güvenlik",
                "keywords": ["bebek bakımı", "yeni ebeveyn", "bebek gelişimi", "ebeveynlik", "bebek uyku", "bebek beslenme"],
                "is_active": True,
                "auto_upload": True,
                "upload_schedule": {
                    "monday": ["10:00", "15:00", "20:00"],
                    "tuesday": ["10:00", "15:00", "20:00"],
                    "wednesday": ["10:00", "15:00", "20:00"],
                    "thursday": ["10:00", "15:00", "20:00"],
                    "friday": ["10:00", "15:00", "20:00"],
                    "saturday": ["11:00", "16:00", "21:00"],
                    "sunday": ["11:00", "16:00", "21:00"]
                },
                "daily_upload_target": 2,
                "target_views_per_video": 8000,
                "competitor_analysis_enabled": True,
                "api_key": "AIzaSyDemoKey_BebekUzman2026",
                "client_secret": "demo_client_secret_bebek"
            },
            {
                "name": "Askeri Stratejist",
                "channel_id": "askeristratejist2026",
                "niche": "Military",
                "language": "TR",
                "target_audience": "Savunma sanayii meraklıları ve askeri personel",
                "description": "Askeri teknolojiler, savunma stratejileri ve ordular hakkında analizler",
                "keywords": ["askeri", "savunma", "ordu", "silah", "strateji", "çatışma", "savunma sanayii"],
                "is_active": True,
                "auto_upload": False,
                "upload_schedule": {
                    "monday": ["11:00", "16:00", "21:00"],
                    "wednesday": ["11:00", "16:00", "21:00"],
                    "friday": ["11:00", "16:00", "21:00"]
                },
                "daily_upload_target": 1,
                "target_views_per_video": 25000,
                "competitor_analysis_enabled": True,
                "api_key": "AIzaSyDemoKey_AskeriStratejist2026",
                "client_secret": "demo_client_secret_askeri"
            },
            {
                "name": "Tech İnovasyon Merkezi",
                "channel_id": "techinovasyon2026",
                "niche": "Tech",
                "language": "TR",
                "target_audience": "Teknoloji meraklıları ve profesyoneller",
                "description": "Yenilikçi teknolojiler, yapay zeka, yazılım ve donanım incelemeleri",
                "keywords": ["yapay zeka", "teknoloji", "yazılım", "donanım", "inovasyon", "startup", "teknik"],
                "is_active": True,
                "auto_upload": True,
                "upload_schedule": {
                    "monday": ["09:00", "14:00", "19:00"],
                    "tuesday": ["09:00", "14:00", "19:00"],
                    "wednesday": ["09:00", "14:00", "19:00"],
                    "thursday": ["09:00", "14:00", "19:00"],
                    "friday": ["09:00", "14:00", "19:00"]
                },
                "daily_upload_target": 4,
                "target_views_per_video": 12000,
                "competitor_analysis_enabled": True,
                "api_key": "AIzaSyDemoKey_TechInovasyon2026",
                "client_secret": "demo_client_secret_tech"
            },
            {
                "name": "Oyun Dünyası",
                "channel_id": "oyundunyasi2026",
                "niche": "Gaming",
                "language": "TR",
                "target_audience": "Oyuncular ve oyun geliştiricileri",
                "description": "Oyun incelemeleri, walkthrough'lar, e-spor haberleri ve oyun kültürü",
                "keywords": ["oyun", "gaming", "espor", "oyun incelemesi", "walkthrough", "oyun haberleri"],
                "is_active": False, # Pasif durumda
                "auto_upload": False,
                "upload_schedule": {},
                "daily_upload_target": 2,
                "target_views_per_video": 10000,
                "competitor_analysis_enabled": True,
                "api_key": "AIzaSyDemoKey_OyunDunyasi2026",
                "client_secret": "demo_client_secret_oyun"
            }
        ]
        
        # Kanalları veritabanına ekle
        for channel_data in sample_channels:
            # Kanal zaten var mı kontrol et
            existing = db.query(Channel).filter(Channel.channel_id == channel_data["channel_id"]).first()
            if not existing:
                new_channel = Channel(**channel_data)
                db.add(new_channel)
                logger.info(f"Örnek kanal oluşturuldu: {channel_data['name']}")
        
        db.commit()
        
        # Örnek videolar oluştur
        create_sample_videos(db)
        
        logger.info("Örnek kanallar ve videolar başarıyla oluşturuldu")
        
    except Exception as e:
        logger.error(f"Veritabanı başlatma hatası: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_videos(db: Session):
    """Örnek videolar oluştur"""
    channels = db.query(Channel).all()
    
    sample_videos = [
        {
            "channel_id": 1, # Kripto Analist
            "title": "🔥 2026'de KİPTO PARA FIRSATLARI!",
            "description": "2026 yılındaki en büyük kripto para yatırım fırsatları. Bitcoin, Ethereum ve altcoin'lerde neler bekliyor?",
            "tags": ["bitcoin", "ethereum", "altcoin", "kripto para", "yatırım 2026", "kripto fırsat"],
            "category": "22",
            "language": "TR",
            "duration": 420.0,
            "status": "published",
            "progress": 100,
            "views": 125000,
            "likes": 8500,
            "comments": 234,
            "youtube_id": "demo_video_001",
            "published_at": datetime.utcnow() - timedelta(days=5),
            "thumbnail_path": "/static/thumbnails/crypto_001.jpg",
            "file_path": "/static/videos/crypto_001.mp4",
            "file_size": 125829120
        },
        {
            "channel_id": 1, # Kripto Analist
            "title": "⚠️ BU ALTCOIN HAKKINDA BİLMENİZ GEREKENLER",
            "description": "Yatırımcıların bilmediği 5 kritik altcoin. Bu fırsatları kaçırmayın!",
            "tags": ["altcoin", "kripto para", "yatırım", "kripto analiz", "gizli fırsatlar"],
            "category": "22",
            "language": "TR",
            "duration": 380.0,
            "status": "published",
            "progress": 100,
            "views": 89000,
            "likes": 6200,
            "comments": 156,
            "youtube_id": "demo_video_002",
            "published_at": datetime.utcnow() - timedelta(days=3),
            "thumbnail_path": "/static/thumbnails/crypto_002.jpg",
            "file_path": "/static/videos/crypto_002.mp4",
            "file_size": 98304000
        },
        {
            "channel_id": 2, # Bebek Gelişim Uzmanı
            "title": "👶 BEBEK UYKUSU PROBLEMLERİ VE ÇÖZÜMLERİ",
            "description": "Yeni ebeveynlerin karşılaştığı 7 yayın uyku sorunu ve pratik çözümleri",
            "tags": ["bebek uyku", "ebeveynlik", "bebek bakımı", "uyku problemleri", "yeni ebeveyn"],
            "category": "22",
            "language": "TR",
            "duration": 480.0,
            "status": "published",
            "progress": 100,
            "views": 45000,
            "likes": 3200,
            "comments": 89,
            "youtube_id": "demo_video_003",
            "published_at": datetime.utcnow() - timedelta(days=2),
            "thumbnail_path": "/static/thumbnails/bebek_001.jpg",
            "file_path": "/static/videos/bebek_001.mp4",
            "file_size": 76800000
        },
        {
            "channel_id": 3, # Askeri Stratejist
            "title": "🎯 EN GELİMİŞ SAVUNMA TEKNOLOJİLERİ 2026",
            "description": "Dünyadaki en ileri savunma sistemleri ve askeri teknolojiler. Türkiye'nin savunma gücü",
            "tags": ["savunma", "askeri teknoloji", "ordu", "silah sistemleri", "savunma sanayii"],
            "category": "22",
            "language": "TR",
            "duration": 600.0,
            "status": "published",
            "progress": 100,
            "views": 156000,
            "likes": 9800,
            "comments": 445,
            "youtube_id": "demo_video_004",
            "published_at": datetime.utcnow() - timedelta(days=7),
            "thumbnail_path": "/static/thumbnails/askeri_001.jpg",
            "file_path": "/static/videos/askeri_001.mp4",
            "file_size": 187904000
        },
        {
            "channel_id": 4, # Tech İnovasyon Merkezi
            "title": "🚀 YAPAY ZEKA 2026'DE NELERİ DEĞİŞTİRECEK?",
            "description": "ChatGPT, Gemini ve yeni AI modellerinin 2026'deki etkileri. İş dünyası nasıl değişecek?",
            "tags": ["yapay zeka", "AI 2026", "ChatGPT", "Gemini", "teknoloji", "iş dünyası"],
            "category": "22",
            "language": "TR",
            "duration": 520.0,
            "status": "rendering", # İşlemde
            "progress": 65,
            "views": 0,
            "likes": 0,
            "comments": 0,
            "youtube_id": None,
            "published_at": None,
            "thumbnail_path": "/static/thumbnails/tech_001.jpg",
            "file_path": "/static/videos/tech_001.mp4",
            "file_size": 104857600
        }
    ]
    
    # Videoları veritabanına ekle
    for video_data in sample_videos:
        # Video zaten var mı kontrol et
        existing = db.query(Video).filter(Video.youtube_id == video_data["youtube_id"]).first()
        if not existing and video_data["youtube_id"]:
            new_video = Video(**video_data)
            db.add(new_video)
            logger.info(f"Örnek video oluşturuldu: {video_data['title']}")
    
    db.commit()

def init_database():
    """Veritabanını tam olarak başlat"""
    try:
        # Tüm tabloları oluştur
        Base.metadata.create_all(bind=engine)
        logger.info("Veritabanı tabloları oluşturuldu")
        
        # Örnek verileri ekle
        create_sample_channels()
        
        logger.info("VUC-2026 veritabanı başarıyla başlatıldı")
        
    except Exception as e:
        logger.error(f"Veritabanı başlatma hatası: {e}")
        raise

if __name__ == "__main__":
    init_database()
