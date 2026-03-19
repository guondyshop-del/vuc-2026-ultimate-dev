from celery import current_task
from celery_app.celery import celery_app
import yt_dlp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

from backend.app.database import SessionLocal
from backend.app.models.competitor import Competitor, CompetitorVideo
from backend.app.models.channel import Channel

logger = logging.getLogger(__name__)

class CompetitorSpy:
    """Rakip casusluk servisi - The Reaper"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
        }
    
    def analyze_channel(self, channel_url: str) -> Dict[str, Any]:
        """Kanal analiz et"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                
                return {
                    'channel_id': info.get('id'),
                    'channel_name': info.get('uploader'),
                    'subscriber_count': info.get('subscriber_count', 0),
                    'total_videos': info.get('channel_follower_count', 0),
                    'total_views': info.get('view_count', 0),
                    'description': info.get('description', ''),
                    'upload_playlist': info.get('uploader_id', ''),
                    'niches': self._extract_niches(info.get('description', '')),
                    'content_style': self._analyze_content_style(info.get('description', '')),
                }
        except Exception as e:
            logger.error(f"Kanal analiz hatası: {e}")
            return {}
    
    def get_recent_videos(self, channel_id: str, limit: int = 20) -> List[Dict]:
        """Kanalın son videolarını getir"""
        try:
            videos = []
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                playlist_url = f"https://www.youtube.com/channel/{channel_id}/videos"
                info = ydl.extract_info(playlist_url, download=False)
                
                for entry in info.get('entries', [])[:limit]:
                    video_data = {
                        'youtube_id': entry.get('id'),
                        'title': entry.get('title'),
                        'description': entry.get('description'),
                        'duration': entry.get('duration'),
                        'published_at': entry.get('upload_date'),
                        'views': entry.get('view_count', 0),
                        'likes': entry.get('like_count', 0),
                        'comments': entry.get('comment_count', 0),
                        'tags': entry.get('tags', []),
                        'thumbnail_url': entry.get('thumbnail'),
                    }
                    
                    # Gelişmiş VPH (View-per-Hour) analizi
                    video_data['vph_data'] = self._calculate_advanced_vph(video_data)
                    video_data['hourly_trends'] = self._analyze_hourly_trends(entry.get('id'))
                    video_data['peak_performance'] = self._find_peak_performance_hours(video_data)
                    video_data['hook_detected'] = self._detect_hook(entry.get('description', ''))
                    video_data['cta_detected'] = self._detect_cta(entry.get('description', ''))
                    
                    videos.append(video_data)
            
            return videos
        except Exception as e:
            logger.error(f"Video getirme hatası: {e}")
            return []
    
    def _extract_niches(self, description: str) -> List[str]:
        """Açıklamadan nişleri çıkar"""
        niche_keywords = {
            'baby': ['bebek', 'baby', 'çocuk', 'kid', 'parenting'],
            'military': ['asker', 'military', 'savunma', 'defense', 'ordu'],
            'crypto': ['kripto', 'crypto', 'bitcoin', 'blockchain', 'altcoin'],
            'gaming': ['oyun', 'game', 'gaming', 'oyuncu', 'espor'],
            'tech': ['teknoloji', 'tech', 'yazılım', 'software', 'bilgisayar'],
            'finance': ['finans', 'finance', 'para', 'money', 'yatırım'],
        }
        
        found_niches = []
        description_lower = description.lower()
        
        for niche, keywords in niche_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                found_niches.append(niche)
        
        return found_niches
    
    def _analyze_content_style(self, description: str) -> str:
        """İçerik stilini analiz et"""
        educational_words = ['öğren', 'nasıl', 'how', 'tutorial', 'guide']
        entertainment_words = ['eğlence', 'komik', 'funny', 'meme', 'viral']
        news_words = ['haber', 'news', 'güncel', 'breaking', 'latest']
        
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in educational_words):
            return 'educational'
        elif any(word in desc_lower for word in entertainment_words):
            return 'entertainment'
        elif any(word in desc_lower for word in news_words):
            return 'news'
        else:
            return 'general'
    
    def _calculate_advanced_vph(self, video_data: Dict) -> Dict:
        """Gelişmiş View-per-Hour analizi"""
        if not video_data.get('published_at') or not video_data.get('views'):
            return {"vph": 0.0, "trend": "stable", "peak_hours": []}
        
        try:
            # Tarih formatını düzelt
            pub_date = datetime.strptime(video_data['published_at'], '%Y%m%d')
            hours_since_upload = (datetime.now() - pub_date).total_seconds() / 3600
            
            if hours_since_upload > 0:
                base_vph = video_data['views'] / hours_since_upload
                
                # VPH trend analizi
                trend = self._calculate_vph_trend(base_vph, video_data)
                
                # Peak performans saatleri
                peak_hours = self._estimate_peak_hours(base_vph)
                
                return {
                    "vph": base_vph,
                    "trend": trend,
                    "peak_hours": peak_hours,
                    "performance_score": self._calculate_performance_score(base_vph, trend),
                    "vph_category": self._categorize_vph(base_vph)
                }
            return {"vph": 0.0, "trend": "stable", "peak_hours": []}
        except Exception as e:
            logger.error(f"Gelişmiş VPH hesaplama hatası: {e}")
            return {"vph": 0.0, "trend": "error", "peak_hours": []}
    
    def _analyze_hourly_trends(self, video_id: str) -> Dict:
        """Saatlik trend analizi (simüle edilmiş)"""
        # Gerçek implementasyonda YouTube Analytics API kullanılacak
        import random
        
        hourly_data = {}
        base_views = random.randint(500, 5000)
        
        for hour in range(24):
            # Simüle edilmiş saatlik dağılım
            if hour in [9, 14, 19, 21]:  # Peak hours
                multiplier = random.uniform(1.5, 2.5)
            elif hour in [7, 12, 18, 22]:  # Good hours
                multiplier = random.uniform(1.0, 1.5)
            else:  # Low hours
                multiplier = random.uniform(0.3, 0.8)
            
            hourly_views = int(base_views * multiplier)
            hourly_data[str(hour)] = hourly_views
        
        return {
            "hourly_distribution": hourly_data,
            "peak_hour": max(hourly_data, key=hourly_data.get),
            "total_views": sum(hourly_data.values()),
            "view_velocity": self._calculate_view_velocity(hourly_data)
        }
    
    def _find_peak_performance_hours(self, video_data: Dict) -> List[int]:
        """Peak performans saatlerini bul"""
        vph_data = video_data.get('vph_data', {})
        hourly_trends = video_data.get('hourly_trends', {})
        
        peak_hours = []
        
        if hourly_trends:
            hourly_dist = hourly_trends.get('hourly_distribution', {})
            avg_views = sum(hourly_dist.values()) / len(hourly_dist) if hourly_dist else 0
            
            for hour, views in hourly_dist.items():
                if views > avg_views * 1.3:  # %30 above average
                    peak_hours.append(int(hour))
        
        return sorted(peak_hours)
    
    def _calculate_vph_trend(self, current_vph: float, video_data: Dict) -> str:
        """VPH trendini hesapla"""
        # Basit trend analizi - gerçek implementasyonda tarihsel veri kullanılacak
        if current_vph > 1000:
            return "rising_fast"
        elif current_vph > 500:
            return "rising"
        elif current_vph > 200:
            return "stable"
        elif current_vph > 100:
            return "declining"
        else:
            return "declining_fast"
    
    def _estimate_peak_hours(self, vph: float) -> List[int]:
        """Peak saatlerini tahmin et"""
        # VPH'e göre tahmin
        if vph > 1000:
            return [9, 14, 19, 21]  # High VPH = more peaks
        elif vph > 500:
            return [14, 19]  # Medium VPH = moderate peaks
        else:
            return [19]  # Low VPH = evening peak
    
    def _calculate_performance_score(self, vph: float, trend: str) -> float:
        """Performans skoru hesapla (0-100)"""
        base_score = min(vph / 20, 50)  # VPH score max 50
        
        trend_scores = {
            "rising_fast": 30,
            "rising": 20,
            "stable": 10,
            "declining": 5,
            "declining_fast": 0
        }
        
        trend_score = trend_scores.get(trend, 5)
        return min(base_score + trend_score, 100)
    
    def _categorize_vph(self, vph: float) -> str:
        """VPH kategorizasyonu"""
        if vph > 1000:
            return "viral"
        elif vph > 500:
            return "high"
        elif vph > 200:
            return "medium"
        elif vph > 50:
            return "low"
        else:
            return "very_low"
    
    def _calculate_view_velocity(self, hourly_data: Dict) -> float:
        """View hızı hesapla (views/hour acceleration)"""
        if len(hourly_data) < 2:
            return 0.0
        
        hours = sorted(hourly_data.keys())
        velocities = []
        
        for i in range(1, len(hours)):
            prev_hour = hours[i-1]
            curr_hour = hours[i]
            
            prev_views = hourly_data[prev_hour]
            curr_views = hourly_data[curr_hour]
            
            velocity = (curr_views - prev_views) / max(prev_views, 1)
            velocities.append(velocity)
        
        return sum(velocities) / len(velocities) if velocities else 0.0
    
    def _detect_hook(self, description: str) -> str:
        """3 saniyelik kancı tespit et"""
        # İlk cümledeki kancı kelimeler
        hook_patterns = [
            'izle', 'watch', 'gördünüz mü', 'did you see',
            'inanamayacaksınız', 'unbelievable', 'şok', 'shock',
            'sadece 3 saniye', 'only 3 seconds', 'hemen', 'now'
        ]
        
        first_sentence = description.split('.')[0] if description else ''
        first_sentence_lower = first_sentence.lower()
        
        for pattern in hook_patterns:
            if pattern in first_sentence_lower:
                return first_sentence[:100]  # İlk 100 karakter
        
        return first_sentence[:100] if first_sentence else ''
    
    def _detect_cta(self, description: str) -> bool:
        """Call-to-action tespit et"""
        cta_keywords = [
            'abone ol', 'subscribe', 'beğen', 'like', 'yorum yap', 'comment',
            'bildirimler', 'notifications', 'paylaş', 'share'
        ]
        
        desc_lower = description.lower()
        return any(keyword in desc_lower for keyword in cta_keywords)

@celery_app.task(bind=True)
def analyze_competitor(self, channel_id: int, competitor_url: str):
    """Rakip analizi görevi"""
    try:
        # Task progress güncelle
        self.update_state(state="PROGRESS", meta={"progress": 10})
        
        spy = CompetitorSpy()
        db = SessionLocal()
        
        # Rakip kanalını analiz et
        competitor_data = spy.analyze_channel(competitor_url)
        self.update_state(state="PROGRESS", meta={"progress": 30})
        
        if not competitor_data:
            raise Exception("Rakip kanalı analiz edilemedi")
        
        # Veritabanına kaydet/güncelle
        competitor = db.query(Competitor).filter_by(
            channel_id=channel_id,
            competitor_channel_id=competitor_data['channel_id']
        ).first()
        
        if not competitor:
            competitor = Competitor(
                channel_id=channel_id,
                competitor_channel_id=competitor_data['channel_id'],
                competitor_name=competitor_data['channel_name'],
                subscriber_count=competitor_data['subscriber_count'],
                total_videos=competitor_data['total_videos'],
                total_views=competitor_data['total_views'],
                niche=competitor_data.get('niches', ['general'])[0] if competitor_data.get('niches') else 'general',
                content_style=competitor_data['content_style'],
                last_analyzed_at=datetime.now()
            )
            db.add(competitor)
        else:
            # Mevcut kaydı güncelle
            competitor.subscriber_count = competitor_data['subscriber_count']
            competitor.total_videos = competitor_data['total_videos']
            competitor.total_views = competitor_data['total_views']
            competitor.last_analyzed_at = datetime.now()
        
        db.commit()
        self.update_state(state="PROGRESS", meta={"progress": 50})
        
        # Son videoları analiz et
        videos = spy.get_recent_videos(competitor_data['channel_id'])
        self.update_state(state="PROGRESS", meta={"progress": 70})
        
        # Video verilerini kaydet
        for video_data in videos:
            existing_video = db.query(CompetitorVideo).filter_by(
                competitor_id=competitor.id,
                youtube_id=video_data['youtube_id']
            ).first()
            
            if not existing_video:
                comp_video = CompetitorVideo(
                    competitor_id=competitor.id,
                    youtube_id=video_data['youtube_id'],
                    title=video_data['title'],
                    description=video_data['description'],
                    duration=video_data['duration'],
                    published_at=datetime.strptime(video_data['published_at'], '%Y%m%d'),
                    views=video_data['views'],
                    likes=video_data['likes'],
                    comments=video_data['comments'],
                    vph_data={'vph': video_data['vph']},
                    hook_detected=video_data['hook_detected'],
                    cta_detected=video_data['cta_detected'],
                    thumbnail_url=video_data['thumbnail_url']
                )
                db.add(comp_video)
        
        db.commit()
        self.update_state(state="PROGRESS", meta={"progress": 90})
        
        # İstatistikleri hesapla
        avg_views = sum(v['views'] for v in videos) / len(videos) if videos else 0
        avg_vph = sum(v['vph'] for v in videos) / len(videos) if videos else 0
        
        competitor.avg_views_per_video = avg_views
        competitor.vph_trend = {'current_avg_vph': avg_vph}
        
        db.commit()
        
        db.close()
        
        return {
            "status": "success",
            "competitor": competitor_data['channel_name'],
            "videos_analyzed": len(videos),
            "avg_views": avg_views,
            "avg_vph": avg_vph
        }
        
    except Exception as e:
        logger.error(f"Rakip analizi hatası: {e}")
        raise

@celery_app.task
def analyze_all_competitors():
    """Tüm rakipleri analiz et"""
    db = SessionLocal()
    try:
        channels = db.query(Channel).filter(Channel.is_active == True).all()
        
        for channel in channels:
            competitors = db.query(Competitor).filter_by(channel_id=channel.id).all()
            
            for competitor in competitors:
                # Rakip URL'ini oluştur
                competitor_url = f"https://www.youtube.com/channel/{competitor.competitor_channel_id}"
                
                # Analiz görevini başlat
                analyze_competitor.delay(channel.id, competitor_url)
        
        return {"status": "queued", "channels": len(channels)}
        
    except Exception as e:
        logger.error(f"Toplu rakip analizi hatası: {e}")
        raise
    finally:
        db.close()
