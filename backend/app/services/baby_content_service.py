"""
VUC-2026 Baby Content Service
YouTube Kids için optimize edilmiş bebek video üretim servisi
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path
from app.services.ai_service import AIService
from app.services.youtube_upload_service import YouTubeUploadService
from app.core.ai_intelligence import AIIntelligence

class BabyContentService:
    """YouTube Kids bebek içeriği üretim servisi"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.youtube_service = YouTubeUploadService()
        self.ai_intelligence = AIIntelligence()
        
        # Baby content specific templates
        self.story_templates = {
            "uyku_hikayesi": {
                "duration": 900,  # 15 dakika
                "structure": ["giriş", "hikaye", "uyku_melodisi", "bitiş"],
                "tone": "sakin_ve_sevecen",
                "age_group": "0-2 yaş"
            },
            "oyun_öğren": {
                "duration": 1200,  # 20 dakika
                "structure": ["tanıtım", "oyun", "öğrenme", "tekrar", "bitiş"],
                "tone": "eğlenceli_ve_eğitici",
                "age_group": "2-4 yaş"
            },
            "şarkı_dans": {
                "duration": 600,  # 10 dakika
                "structure": ["şarkı", "dans", "tekrar", "bitiş"],
                "tone": "enerjik_ve_neşeli",
                "age_group": "1-3 yaş"
            }
        }
        
        # Baby content character library
        self.characters = {
            "pacan_kedi": "sevimli, meraklı kedi",
            "tatlı_panda": "uyumlu, neşeli panda", 
            "akilli_fare": "zeki, yardımsever fare",
            "mutlu_ayı": "dost canlısı, korumacı ayı",
            "renkli_kelebek": "hayalperest, neşeli kelebek"
        }
        
        # Educational themes
        self.educational_themes = {
            "renkler": ["kırmızı", "mavi", "sarı", "yeşil", "turuncu", "mor"],
            "sayılar": ["bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on"],
            "hayvanlar": ["kedi", "köpek", "kuş", "tavşan", "fil", "maymun"],
            "meyveler": ["elma", "armut", "muz", "portakal", "çilek", "üzüm"],
            "şekiller": ["daire", "kare", "üçgen", "dikdörtgen", "yıldız", "kalp"]
        }
        
        # Multilingual support
        self.languages = {
            "tr": {"name": "Türkçe", "voice": "tr-TR-AylinNeural"},
            "en": {"name": "English", "voice": "en-US-AriaNeural"},
            "de": {"name": "Deutsch", "voice": "de-DE-KatjaNeural"},
            "fr": {"name": "Français", "voice": "fr-FR-DeniseNeural"},
            "es": {"name": "Español", "voice": "es-ES-ElviraNeural"}
        }

    async def generate_baby_story(self, 
                                story_type: str,
                                character: str,
                                theme: str,
                                language: str = "tr",
                                target_duration: int = 900) -> Dict:
        """
        Bebek hikayesi oluştur
        
        Args:
            story_type: Hikaye türü (uyku_hikayesi, oyun_öğren, şarkı_dans)
            character: Karakter ismi
            theme: Eğitici tema
            language: Dil kodu
            target_duration: Hedef süre (saniye)
        """
        
        template = self.story_templates.get(story_type, self.story_templates["uyku_hikayesi"])
        character_info = self.characters.get(character, self.characters["pacan_kedi"])
        theme_items = self.educational_themes.get(theme, self.educational_themes["renkler"])
        lang_info = self.languages.get(language, self.languages["tr"])
        
        # AI ile hikaye senaryosu oluştur
        prompt = f"""
        YouTube Kids için {template['duration']} saniyelik bebek hikayesi oluştur.
        
        Kriterler:
        - Hikaye Türü: {story_type}
        - Karakter: {character_info} ({character})
        - Tema: {theme} - {', '.join(theme_items)}
        - Yaş Grubu: {template['age_group']}
        - Ton: {template['tone']}
        - Dil: {lang_info['name']}
        - Süre: {target_duration} saniye
        
        Yapı: {' → '.join(template['structure'])}
        
        Her bölüm için:
        1. Diyalog (basit, tekrarlı)
        2. Eylem açıklaması
        3. Görsel efekt önerisi
        4. Ses efekti önerisi
        
        YouTube Kids kurallarına uygun, eğitici ve eğlenceli içerik.
        """
        
        story_script = await self.ai_service.generate_script(prompt)
        
        return {
            "story_type": story_type,
            "character": character,
            "theme": theme,
            "language": language,
            "duration": target_duration,
            "script": story_script,
            "structure": template["structure"],
            "age_group": template["age_group"],
            "tone": template["tone"],
            "generated_at": datetime.now().isoformat()
        }

    async def generate_visual_assets(self, story_data: Dict) -> List[Dict]:
        """
        Hikaye için görsel varlıklar oluştur
        """
        visual_assets = []
        
        # Karakter görselleri
        character_prompt = f"""
        Çizgi film tarzı, bebek dostu {story_data['character']}
        Pastel renkler, yuvarlak hatlar, sevimli ve güvenli görünüm
        2D animasyon stili, yüksek çözünürlük
        """
        
        # Tema görselleri
        theme_items = self.educational_themes.get(story_data['theme'], [])
        
        for item in theme_items:
            item_prompt = f"""
            Çizgi film {item}, bebekler için
            Pastel renkler, basit ve anlaşılır
            Eğitici ve çekici tasarım
            """
            visual_assets.append({
                "type": "theme_item",
                "item": item,
                "prompt": item_prompt,
                "duration": 30  # saniye
            })
        
        return visual_assets

    async def generate_audio_assets(self, story_data: Dict) -> Dict:
        """
        Ses varlıkları oluştur (narration, müzik, efektler)
        """
        lang_info = self.languages.get(story_data['language'], self.languages['tr'])
        
        return {
            "narration": {
                "voice": lang_info['voice'],
                "style": "gentle_and_warm",
                "speed": "slow",
                "pitch": "high"
            },
            "background_music": {
                "type": "lullaby" if story_data['story_type'] == "uyku_hikayesi" else "playful",
                "volume": 0.3,
                "fade_in": True,
                "fade_out": True
            },
            "sound_effects": [
                "gentle_chimes",
                "soft_bells", 
                "baby_giggles",
                "nature_sounds"
            ]
        }

    async def produce_baby_video(self, 
                               story_type: str,
                               character: str,
                               theme: str,
                               language: str = "tr",
                               duration: int = 900) -> Dict:
        """
        Tam bebek video üretimi
        """
        
        # 1. Hikaye oluştur
        story_data = await self.generate_baby_story(
            story_type, character, theme, language, duration
        )
        
        # 2. Görsel varlıklar oluştur
        visual_assets = await self.generate_visual_assets(story_data)
        
        # 3. Ses varlıklar oluştur
        audio_assets = await self.generate_audio_assets(story_data)
        
        # 4. Video render planı
        render_plan = {
            "story_data": story_data,
            "visual_assets": visual_assets,
            "audio_assets": audio_assets,
            "render_settings": {
                "resolution": "1080p",
                "fps": 30,
                "quality": "high",
                "format": "mp4"
            },
            "youtube_settings": {
                "title": self._generate_youtube_title(story_data),
                "description": self._generate_youtube_description(story_data),
                "tags": self._generate_youtube_tags(story_data),
                "category": "Kids",
                "made_for_kids": True,
                "target_audience": "family_friendly"
            }
        }
        
        return render_plan

    def _generate_youtube_title(self, story_data: Dict) -> str:
        """YouTube başlığı oluştur"""
        titles = {
            "tr": [
                f"🌙 {story_data['character'].title()} - {story_data['theme'].title()} Hikayesi",
                f"🎨 {story_data['character'].title()} ile {story_data['theme'].title()} Öğreniyorum",
                f"🎵 {story_data['character'].title()} Şarkısı - {story_data['theme'].title()}"
            ],
            "en": [
                f"🌙 {story_data['character'].title()} - {story_data['theme'].title()} Story",
                f"🎨 Learning {story_data['theme'].title()} with {story_data['character'].title()}",
                f"🎵 {story_data['character'].title()} Song - {story_data['theme'].title()}"
            ]
        }
        
        lang_titles = titles.get(story_data['language'], titles["en"])
        return lang_titles[0]  # İlk başlığı kullan

    def _generate_youtube_description(self, story_data: Dict) -> str:
        """YouTube açıklaması oluştur"""
        age_group = story_data.get('age_group', '0-4 yaş')
        duration_minutes = story_data.get('duration', 900) // 60
        
        descriptions = {
            "tr": f"""
            👶 Bebekler için özel {story_data['character']} hikayesi!
            
            🎯 Bu videoda:
            • {story_data['theme'].title()} öğreniyoruz
            • {age_group} için uygun içerik
            • {duration_minutes} dakika eğlenceli zaman
            • Eğitici ve güvenli içerik
            
            📺 Abone olmayı unutmayın!
            👍 Beğen ve paylaşın!
            💬 Yorumlarınız bizim için değerli...
            
            #bebek #çocuk #hikaye #eğitim #YouTubeKids
            """,
            "en": f"""
            👶 Special {story_data['character']} story for babies!
            
            🎯 In this video:
            • Learning {story_data['theme'].title()}
            • Content for {age_group}
            • {duration_minutes} minutes of fun
            • Educational and safe content
            
            📺 Don't forget to subscribe!
            👍 Like and share!
            💬 Your comments are valuable...
            
            #baby #kids #story #education #YouTubeKids
            """
        }
        
        return descriptions.get(story_data['language'], descriptions["en"])

    def _generate_youtube_tags(self, story_data: Dict) -> List[str]:
        """YouTube etiketleri oluştur"""
        base_tags = [
            "baby videos",
            "kids content", 
            "educational",
            "family friendly",
            "YouTube Kids",
            story_data['character'],
            story_data['theme']
        ]
        
        # Dil spesifik etiketler
        if story_data['language'] == 'tr':
            base_tags.extend([
                "bebek videoları",
                "çocuk şarkıları", 
                "eğitici videolar",
                "yeni doğan",
                "ebeveynlik"
            ])
        
        return base_tags

    async def get_baby_content_ideas(self, limit: int = 20) -> List[Dict]:
        """
        Bebek içerik fikirleri oluştur
        """
        ideas = []
        
        for story_type in self.story_templates.keys():
            for character in self.characters.keys():
                for theme in self.educational_themes.keys():
                    for language in self.languages.keys():
                        if len(ideas) >= limit:
                            break
                            
                        ideas.append({
                            "story_type": story_type,
                            "character": character,
                            "theme": theme,
                            "language": language,
                            "estimated_duration": self.story_templates[story_type]["duration"],
                            "age_group": self.story_templates[story_type]["age_group"],
                            "priority_score": self._calculate_priority_score(story_type, character, theme)
                        })
        
        # Öncelik skoruna göre sırala
        ideas.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return ideas[:limit]

    def _calculate_priority_score(self, story_type: str, character: str, theme: str) -> float:
        """
        İçerik öncelik skoru hesapla
        """
        # Analytics verilerine göre skor
        base_scores = {
            "uyku_hikayesi": 0.9,
            "oyun_öğren": 0.85,
            "şarkı_dans": 0.8
        }
        
        character_scores = {
            "pacan_kedi": 0.95,
            "tatlı_panda": 0.9,
            "akilli_fare": 0.85,
            "mutlu_ayı": 0.8,
            "renkli_kelebek": 0.75
        }
        
        theme_scores = {
            "renkler": 0.9,
            "sayılar": 0.85,
            "hayvanlar": 0.95,
            "meyveler": 0.8,
            "şekiller": 0.75
        }
        
        return (
            base_scores.get(story_type, 0.5) * 0.4 +
            character_scores.get(character, 0.5) * 0.35 +
            theme_scores.get(theme, 0.5) * 0.25
        )

    async def schedule_baby_content(self, 
                                  daily_count: int = 3,
                                  upload_times: List[str] = None) -> List[Dict]:
        """
        Bebek içerik takvimi oluştur
        """
        if upload_times is None:
            upload_times = ["09:00", "15:00", "20:00"]
        
        content_ideas = await self.get_baby_content_ideas(daily_count * 7)  # 1 haftalık
        schedule = []
        
        for day in range(7):
            for time_slot in upload_times:
                if content_ideas:
                    idea = content_ideas.pop(0)
                    schedule.append({
                        "day": day,
                        "time": time_slot,
                        "content": idea,
                        "estimated_views": self._estimate_views(idea),
                        "estimated_revenue": self._estimate_revenue(idea)
                    })
        
        return schedule

    def _estimate_views(self, content_idea: Dict) -> int:
        """Görüntülenme tahmini"""
        base_views = 5000
        multiplier = content_idea.get('priority_score', 0.5) * 2
        
        return int(base_views * multiplier)

    def _estimate_revenue(self, content_idea: Dict) -> float:
        """Gelir tahmini"""
        views = self._estimate_views(content_idea)
        # Kids content genelde higher CPM
        cpm = 2.5  # $2.5 per 1000 views
        
        return (views / 1000) * cpm
