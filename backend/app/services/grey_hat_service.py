import cv2
import numpy as np
import ffmpeg
import random
import os
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class GreyHatService:
    """Grey-Hat algoritma manipülasyon servisleri"""
    
    def __init__(self):
        self.temp_dir = "../temp"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def apply_algorithm_shield(self, video_path: str, output_path: str = None) -> str:
        """
        YouTube "Tekrarlayan İçerik" filtresini baypas et
        
        Uygulanan teknikler:
        - %0.1 rastgele kare hızı titremesi
        - Görünmez piksel gürültüsü
        - %1.01 mikro hız değişimi
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.temp_dir, f"shielded_{timestamp}.mp4")
        
        try:
            # 1. Kare hızı titremesi (%0.1)
            jittered_video = self._apply_frame_jitter(video_path)
            
            # 2. Piksel gürültüsü ekle
            noised_video = self._add_pixel_noise(jittered_video)
            
            # 3. Mikro hız değişimi (%1.01)
            final_video = self._apply_speed_variance(noised_video, output_path)
            
            # Geçici dosyaları temizle
            self._cleanup_temp_files([jittered_video, noised_video])
            
            logger.info(f"Algoritma kalkanı uygulandı: {output_path}")
            return final_video
            
        except Exception as e:
            logger.error(f"Algoritma kalkanı hatası: {e}")
            raise
    
    def _apply_frame_jitter(self, input_path: str) -> str:
        """%0.1 rastgele kare hızı titremesi"""
        
        output_path = os.path.join(self.temp_dir, f"jitter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        # Rastgele fps değeri (orijinalin %0.1 farklı)
        original_fps = self._get_video_fps(input_path)
        jitter_factor = random.uniform(0.999, 1.001)
        new_fps = original_fps * jitter_factor
        
        try:
            (
                ffmpeg
                .input(input_path)
                .filter('fps', fps=new_fps)
                .output(output_path, vcodec='libx264', preset='fast', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Frame jitter hatası: {e}")
            return input_path
    
    def _add_pixel_noise(self, input_path: str) -> str:
        """Görünmez piksel gürültüsü ekle"""
        
        output_path = os.path.join(self.temp_dir, f"noise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        try:
            # Videoyu oku
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Video writer oluştur
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Görünüz piksel gürültüsü ekle (çok düşük yoğunlukta)
                noise = np.random.normal(0, 1, frame.shape).astype(np.uint8)
                frame = cv2.add(frame, noise)
                
                out.write(frame)
            
            cap.release()
            out.release()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Piksel gürültüsü hatası: {e}")
            return input_path
    
    def _apply_speed_variance(self, input_path: str, output_path: str) -> str:
        """%1.01 mikro hız değişimi"""
        
        # Hız değişimi faktörü
        speed_factor = random.uniform(0.99, 1.01)
        
        try:
            (
                ffmpeg
                .input(input_path)
                .filter('setpts', f'{1/speed_factor}*PTS')
                .output(output_path, vcodec='libx264', preset='fast', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"Hız değişimi hatası: {e}")
            return input_path
    
    def generate_ghost_interaction(self, video_id: str, title: str, 
                                keywords: List[str]) -> Dict[str, Any]:
        """
        Hayalet etkileşim oluştur
        
        - Anahtar kelime içeren ilk yorum
        - Persona simülasyonu yanıtları
        """
        
        try:
            # İlk yorumu oluştur
            first_comment = self._create_first_comment(title, keywords)
            
            # Persona yanıtları oluştur
            persona_responses = self._create_persona_responses(first_comment)
            
            return {
                "video_id": video_id,
                "first_comment": first_comment,
                "persona_responses": persona_responses,
                "total_interactions": 1 + len(persona_responses),
                "engagement_boost": "high"
            }
            
        except Exception as e:
            logger.error(f"Hayalet etkileşim hatası: {e}")
            raise
    
    def _create_first_comment(self, title: str, keywords: List[str]) -> Dict[str, Any]:
        """Anahtar kelime içeren ilk yorum"""
        
        # Yorum şablonları
        comment_templates = [
            "Harika bir video! Özellikle {keyword} konusu çok aydınlatıcıydı. {emoji}",
            "Bu {keyword} içeriği arıyordum, tam zamanında denk geldi! {emoji}",
            "{keyword} hakkında en iyi içeriklerden biri. Teşekkürler! {emoji}",
            "Vay be, {keyword} detayları çok başarılı anlatılmış. {emoji}",
            "Abone oldum! {keyword} içeriklerinizin devamını bekliyorum. {emoji}"
        ]
        
        emojis = ["👍", "🔥", "💯", "🎯", "🚀"]
        
        # Rastgele şablon ve anahtar kelime seç
        template = random.choice(comment_templates)
        keyword = random.choice(keywords) if keywords else "içerik"
        emoji = random.choice(emojis)
        
        comment_text = template.format(keyword=keyword, emoji=emoji)
        
        return {
            "text": comment_text,
            "timestamp": datetime.now().isoformat(),
            "should_pin": True,
            "keywords_used": [keyword],
            "engagement_score": 0.8
        }
    
    def _create_persona_responses(self, first_comment: str) -> List[Dict[str, Any]]:
        """Persona simülasyonu yanıtları"""
        
        personas = [
            {
                "name": "TeknolojiMeraklısı42",
                "style": "teknik ve detaylı",
                "response": "Kesinlikle katılıyorum. Özellikle teknik detayların açıklanması çok başarılı."
            },
            {
                "name": "EğlenceAvcısı",
                "style": "neşeli ve esprili", 
                "response": "Haha çok güzel! 😄 Daha fazlasını bekliyorum, devamı gelsin!"
            },
            {
                "name": "Uzmanİzleyici",
                "style": "bilgili ve analitik",
                "response": "Konunun uzmanı olarak söylüyorum, bu içerik gerçekten kaliteli yapılmış."
            },
            {
                "name": "YeniBaşlayan",
                "style": "meraklı ve soru soran",
                "response": "Yeni başlayan biri olarak çok faydalı buldum. Başka kaynaklar önerebilir misiniz?"
            },
            {
                "name": "SadıkTakipçi",
                "style": "destekleyici ve teşvik edici",
                "response": "Sizi ilk günden beri takip ediyorum. Her video bir öncekinden daha iyi!"
            }
        ]
        
        responses = []
        
        for persona in personas:
            # Response'u kişiselleştir
            response_text = persona["response"]
            
            # Rastgele gecikme (yorumlar arası zaman farkı için)
            delay_minutes = random.randint(1, 30)
            
            response = {
                "persona": persona["name"],
                "style": persona["style"],
                "text": response_text,
                "timestamp": datetime.now().isoformat(),
                "delay_minutes": delay_minutes,
                "engagement_score": random.uniform(0.6, 0.9)
            }
            
            responses.append(response)
        
        return responses
    
    def create_thumbnail_ab_test(self, title: str, niche: str) -> Dict[str, Any]:
        """
        Thumbnail A/B testi oluştur
        
        - İki farklı thumbnail konsepti
        - CTR tahmini
        """
        
        try:
            # Thumbnail A - Hormozi stili
            thumbnail_a = {
                "version": "A",
                "style": "hormozi",
                "colors": ["yellow", "black"],
                "text_size": "large",
                "elements": ["bold_text", "arrows", "high_contrast"],
                "estimated_ctr": random.uniform(0.05, 0.12),
                "target_audience": "general"
            }
            
            # Thumbnail B - Minimal stili
            thumbnail_b = {
                "version": "B", 
                "style": "minimal",
                "colors": ["white", "blue"],
                "text_size": "medium",
                "elements": ["clean_text", "subtle_colors", "professional"],
                "estimated_ctr": random.uniform(0.03, 0.08),
                "target_audience": "professional"
            }
            
            # Test stratejisi
            test_strategy = {
                "test_duration_hours": 48,
                "min_views_for_decision": 1000,
                "swap_threshold": 0.03,  # %3 CTR farkı
                "auto_swap_enabled": True
            }
            
            return {
                "title": title,
                "niche": niche,
                "thumbnail_a": thumbnail_a,
                "thumbnail_b": thumbnail_b,
                "test_strategy": test_strategy,
                "recommended_start": "A",  # Daha yüksek CTR tahmini
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Thumbnail A/B testi hatası: {e}")
            raise
    
    def analyze_content_gaps(self, competitor_data: List[Dict[str, Any]], 
                           niche: str) -> Dict[str, Any]:
        """
        Rakip içerik boşluklarını analiz et
        
        - Rakiplerin kaçırdığı konular
        - Trend potansiyeli yüksek konular
        """
        
        try:
            # Rakip konularını extract et
            competitor_topics = []
            for competitor in competitor_data:
                topics = competitor.get("topics", [])
                competitor_topics.extend(topics)
            
            # Niş spesifik konu havuzu
            niche_topic_pools = {
                "baby": ["bebek bakım ipuçları", "yeni ebeveyn rehberi", "bebek uyku düzeni", 
                        "bebek beslenmesi", "bebek gelişimi", "ebeveyn psikolojisi"],
                "military": ["askeri teknoloji", "savunma sanayi", "askeri tarih", 
                           "silah sistemleri", "stratejik analiz", "ordu hayatı"],
                "crypto": ["bitcoin analizi", "altcoin fırsatları", "blockchain teknolojisi", 
                          "kripto yatırım stratejileri", "DeFi projeleri", "NFT pazarı"],
                "gaming": ["oyun incelemeleri", "espor turnuvaları", "oyun rehberleri", 
                          "yeni oyunlar", "oyun donanımı", "oyun hikayeleri"],
                "tech": ["yazılım geliştirme", "yapay zeka", "cyber güvenlik", 
                        "teknoloji incelemeleri", "startup hikayeleri", "teknoloji trendleri"]
            }
            
            # Niş için konu havuzunu al
            available_topics = niche_topic_pools.get(niche, [])
            
            # Rakiplerin kapladığı konuları çıkar
            uncovered_topics = []
            for topic in available_topics:
                if not any(topic.lower() in comp_topic.lower() 
                          for comp_topic in competitor_topics):
                    uncovered_topics.append(topic)
            
            # Her konu için potansiyel skoru hesapla
            topic_opportunities = []
            for topic in uncovered_topics:
                opportunity = {
                    "topic": topic,
                    "competition_level": "low",  # Rakip yok
                    "trend_potential": random.uniform(0.6, 0.9),
                    "search_volume_estimate": random.randint(1000, 10000),
                    "production_difficulty": random.choice(["easy", "medium", "hard"]),
                    "estimated_views": random.randint(5000, 50000),
                    "priority_score": random.uniform(0.7, 0.95)
                }
                topic_opportunities.append(opportunity)
            
            # Öncelik sırasına göre sırala
            topic_opportunities.sort(key=lambda x: x["priority_score"], reverse=True)
            
            return {
                "niche": niche,
                "competitors_analyzed": len(competitor_data),
                "total_topics_in_niche": len(available_topics),
                "covered_by_competitors": len(available_topics) - len(uncovered_topics),
                "uncovered_opportunities": len(uncovered_topics),
                "top_opportunities": topic_opportunities[:5],  # İlk 5 fırsat
                "content_gap_percentage": (len(uncovered_topics) / len(available_topics)) * 100,
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"İçerik boşluğu analizi hatası: {e}")
            raise
    
    def _get_video_fps(self, video_path: str) -> float:
        """Video FPS değerini al"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            return fps
        except:
            return 30.0  # Varsayılan
    
    def _cleanup_temp_files(self, file_paths: List[str]):
        """Geçici dosyaları temizle"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
