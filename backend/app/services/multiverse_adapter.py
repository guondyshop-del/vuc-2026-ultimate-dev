"""
VUC-2026 Multi-Verse Adapter
Cross-platform content morphing for TikTok, Instagram, X, Facebook

Adapts long-form YouTube content into platform-optimized versions
with aggressive hooks, cinematic LUTs, viral threads, and community posts.
"""

import logging
import asyncio
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Platform-specific LUT presets
INSTAGRAM_LUTS = {
    "golden_hour": {"contrast": 1.15, "saturation": 1.2, "warmth": 0.8, "vignette": 0.3},
    "clean_minimal": {"contrast": 1.05, "saturation": 0.9, "warmth": 0.0, "vignette": 0.0},
    "moody_dark": {"contrast": 1.3, "saturation": 0.8, "warmth": -0.3, "vignette": 0.5},
    "vibrant_pop": {"contrast": 1.2, "saturation": 1.4, "warmth": 0.2, "vignette": 0.1},
    "film_grain": {"contrast": 1.1, "saturation": 0.95, "warmth": 0.1, "vignette": 0.4, "grain": 0.15},
}

TIKTOK_HOOK_TEMPLATES = [
    "POV: {keyword} ile hayatını değiştirdin 👀",
    "Kimse söylemedi ama {keyword} hakkında...",
    "Bu {keyword} sırrını öğrenen kazanıyor 🔥",
    "{keyword} hakkında 30 saniyede bilmeniz gereken her şey",
    "Bunu yapmayana {keyword}'den faydalanamaz ⚡",
    "Strateji: {keyword} → viral sonuç 🚀",
    "İzlenmesi gereken bir video: {keyword}",
    "Sana {keyword} hakkında bir şey söyleyeyim 🤫",
]

X_THREAD_TEMPLATES = [
    "🧵 {title} hakkında {n} şey bilmeniz lazım:\n\n1/",
    "📌 {title} için ultimate rehber:\n\n{n} adım, {n} dakika → hepsi burada 🧵\n\n1/",
    "Bu kadar çalıştıktan sonra {title} hakkında bulduklarımı paylaşıyorum:\n\n🧵 Thread başlıyor →\n\n1/",
    "💡 {n} yıllık tecrübemi {n} tweet'e sığdırdım.\n\nKonu: {title}\n\n🧵 1/",
]


class MultiverseAdapter:
    """Cross-platform content morphing engine"""

    def __init__(self):
        self.adapter_id = "multiverse_adapter_v1"
        self.adaptations_history: List[Dict[str, Any]] = []

    async def adapt_for_all_platforms(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt content for all supported platforms simultaneously.

        Args:
            content: {title, script, description, keywords, niche, video_path}

        Returns:
            Per-platform adapted content
        """
        try:
            platforms = ["tiktok", "instagram", "twitter", "facebook", "youtube_community"]

            tasks = {
                platform: self._adapt_for_platform(content, platform)
                for platform in platforms
            }

            results = {}
            for platform, coro in tasks.items():
                results[platform] = await coro

            adaptation_record = {
                "original_title": content.get("title", ""),
                "platforms_adapted": len(results),
                "timestamp": datetime.now().isoformat()
            }
            self.adaptations_history.append(adaptation_record)

            logger.info(f"Multi-verse adaptasyon: {len(results)} platform")

            return {
                "success": True,
                "original_content": content,
                "adaptations": results,
                "platforms_count": len(results),
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Multi-verse adaptasyon hatası: {e}")
            return {"success": False, "error": str(e)}

    async def _adapt_for_platform(self, content: Dict[str, Any],
                                   platform: str) -> Dict[str, Any]:
        """Route to platform-specific adapter"""
        adapters = {
            "tiktok": self._adapt_tiktok,
            "instagram": self._adapt_instagram,
            "twitter": self._adapt_twitter,
            "facebook": self._adapt_facebook,
            "youtube_community": self._adapt_youtube_community,
        }
        adapter = adapters.get(platform, self._adapt_generic)
        return await adapter(content)

    async def _adapt_tiktok(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """TikTok: Aggressive hook + trending audio + fast cuts"""
        title = content.get("title", "")
        keywords = content.get("keywords", [])
        script = content.get("script", "")
        primary_kw = keywords[0] if keywords else title.split()[0] if title else "konu"

        # Generate aggressive hook
        hook_template = random.choice(TIKTOK_HOOK_TEMPLATES)
        hook = hook_template.format(keyword=primary_kw)

        # Script adaptation: keep only first 60 seconds (≈180 words)
        words = script.split()
        tiktok_script = ' '.join(words[:180]) if len(words) > 180 else script

        # Add trending audio recommendation
        trending_audios = [
            "Trending Sound #1 (TikTok Creator Marketplace)",
            "Viral Beat - Original Sound",
            "Lo-fi background - trending this week",
        ]

        # Generate 3 caption variations
        captions = self._generate_tiktok_captions(title, keywords)

        # Generate hashtag strategy
        hashtags = self._generate_platform_hashtags(keywords, "tiktok")

        return {
            "platform": "TikTok",
            "hook": hook,
            "adapted_script": tiktok_script,
            "target_duration_seconds": random.randint(30, 60),
            "trending_audio_recommendation": random.choice(trending_audios),
            "audio_volume": 0.10,
            "caption_variations": captions,
            "hashtags": hashtags,
            "cta": "Takip et, daha fazlası geliyor! 🔔",
            "production_notes": [
                "İlk 3 saniye hook kısmı — kesintisiz tutulacak",
                "Ses efekti: whoosh geçişleri",
                "Altyazı: büyük, renkli, kelime kelime",
                f"Trending audio: %10 ses seviyesi overlay"
            ]
        }

    async def _adapt_instagram(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Instagram: Cinematic LUT + engagement-focused captions"""
        title = content.get("title", "")
        keywords = content.get("keywords", [])
        script = content.get("script", "")
        niche = content.get("niche", "general")

        # Select LUT based on niche
        lut_map = {
            "technology": "clean_minimal",
            "business": "golden_hour",
            "education": "clean_minimal",
            "entertainment": "vibrant_pop",
            "gaming": "moody_dark",
        }
        lut_name = lut_map.get(niche, "golden_hour")
        lut_settings = INSTAGRAM_LUTS[lut_name]

        # Instagram caption (storytelling format)
        caption = self._generate_instagram_caption(title, script, keywords)

        # Carousel slide text (if applicable)
        carousel_slides = self._generate_carousel_slides(script, keywords)

        # Hashtag strategy (max 30)
        hashtags = self._generate_platform_hashtags(keywords, "instagram")

        return {
            "platform": "Instagram",
            "lut_preset": lut_name,
            "lut_settings": lut_settings,
            "caption": caption,
            "carousel_slides": carousel_slides,
            "hashtags": hashtags[:30],
            "reel_duration_seconds": random.randint(15, 45),
            "story_adaptation": self._generate_story_adaptation(title, keywords),
            "cta": "Profile'ı ziyaret et 👆 Daha fazla içerik için",
            "production_notes": [
                f"LUT: {lut_name} — cinematic görünüm",
                "Altyazı: Orta-bottom, beyaz, temiz font",
                "Muzik: Background instrumental, -18dB",
                "Cover: Manuel seç — en dikkat çekici kare"
            ]
        }

    async def _adapt_twitter(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """X/Twitter: Viral thread + deep-link CTAs"""
        title = content.get("title", "")
        keywords = content.get("keywords", [])
        script = content.get("script", "")
        youtube_url = content.get("youtube_url", "https://youtube.com/watch")

        # Generate thread
        thread = self._generate_twitter_thread(title, script, keywords, youtube_url)

        # Single tweet hook
        hook_tweet = f"🔥 {title}\n\nBir thread hazırladım — okumadan geçme!\n\n🧵 Devamı ↓"

        # Poll suggestion
        poll = {
            "question": f"{title.split()[:4]}... hakkında ne düşünüyorsunuz?",
            "options": ["Çok faydalı!", "Bunu bilmiyordum", "Daha fazla istiyorum", "Konuyu araştıracağım"]
        }

        return {
            "platform": "X/Twitter",
            "hook_tweet": hook_tweet,
            "thread": thread,
            "thread_length": len(thread),
            "poll_suggestion": poll,
            "hashtags": self._generate_platform_hashtags(keywords, "twitter")[:5],
            "deep_link_cta": f"Tam video: {youtube_url}",
            "best_posting_time": random.choice(["09:00", "12:00", "19:00", "21:00"]),
            "production_notes": [
                f"Thread {len(thread)} tweet — optimal engagement için 5-10 arası",
                "Her tweet bağımsız okunabilir olmalı",
                "Video klip: 2. veya 3. tweet'e ekle",
                "Pin thread to profile after posting"
            ]
        }

    async def _adapt_facebook(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Facebook: Long-form storytelling + community engagement"""
        title = content.get("title", "")
        keywords = content.get("keywords", [])
        script = content.get("script", "")
        youtube_url = content.get("youtube_url", "")

        post_text = self._generate_facebook_post(title, script, keywords, youtube_url)
        hashtags = self._generate_platform_hashtags(keywords, "facebook")[:10]

        return {
            "platform": "Facebook",
            "post_text": post_text,
            "hashtags": hashtags,
            "video_title": title,
            "video_description": f"Bu videoyu izlemeden geçme! 👇\n\n{youtube_url}",
            "cta": "Paylaş ve arkadaşlarını etiketle!",
            "best_posting_time": "19:00-21:00",
            "group_sharing_suggestion": True,
            "production_notes": [
                "Facebook Watch için yükle — ayrıca optimize et",
                "İlk yorum: video açıklaması + link",
                "Community Group'larda paylaş",
                "24 saat sonra boost düşün"
            ]
        }

    async def _adapt_youtube_community(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """YouTube Community Tab: Poll + announcement 2 hours before upload"""
        title = content.get("title", "")
        keywords = content.get("keywords", [])

        poll_options = self._generate_community_poll_options(keywords)
        announcement_text = self._generate_community_announcement(title)

        return {
            "platform": "YouTube Community",
            "pre_upload_post": {
                "text": announcement_text,
                "post_timing": "2 saat önce",
                "type": "announcement"
            },
            "poll_post": {
                "question": f"Bu {title.split()[0]} videosu hakkında ne düşünüyorsunuz?",
                "options": poll_options,
                "post_timing": "6 saat önce",
                "type": "poll"
            },
            "post_upload_post": {
                "text": f"🎬 YENİ VIDEO: {title} — Hemen izleyin!",
                "type": "announcement",
                "post_timing": "yükleme anında"
            },
            "production_notes": [
                "Yükleme 2 saat önce poll paylaş",
                "Yükleme 6 saat önce teaser paylaş",
                "İlk saatte pinned comment ekle"
            ]
        }

    async def _adapt_generic(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generic platform adaptation"""
        return {
            "platform": "Generic",
            "title": content.get("title", ""),
            "description": content.get("description", ""),
            "keywords": content.get("keywords", [])
        }

    # --- Content generation helpers ---

    def _generate_tiktok_captions(self, title: str, keywords: List[str]) -> List[str]:
        """Generate 3 TikTok caption variations"""
        pk = keywords[0] if keywords else title.split()[0] if title else "konu"
        return [
            f"Bu {pk} stratejisini kimse bilmiyordu! 🔥 #viral #{pk.replace(' ', '')}",
            f"{pk} hakkında her şey burada 👀 Kaydettiniz mi?",
            f"POV: {pk} ile işini büyütüyorsun ⚡ #fyp #{pk.replace(' ', '')}"
        ]

    def _generate_instagram_caption(self, title: str, script: str, keywords: List[str]) -> str:
        """Generate Instagram storytelling caption"""
        hook = f"✨ {title}"
        story_parts = script.split('.')[:3] if script else [title]
        body = ' '.join(s.strip() for s in story_parts if s.strip())[:400]
        cta = "👇 Düşüncelerinizi yorumda paylaşın!"
        return f"{hook}\n\n{body}\n\n{cta}"

    def _generate_carousel_slides(self, script: str, keywords: List[str]) -> List[str]:
        """Generate carousel slide texts"""
        sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 20][:8]
        slides = []
        for i, sentence in enumerate(sentences, 1):
            if i == 1:
                slides.append(f"💡 SLIDE {i}: {sentence[:100]}")
            elif i == len(sentences):
                slides.append(f"✅ SON: {sentence[:100]}\n\nKaydet & Paylaş 🔖")
            else:
                slides.append(f"→ {sentence[:100]}")
        return slides

    def _generate_story_adaptation(self, title: str, keywords: List[str]) -> Dict[str, str]:
        """Generate Instagram Story adaptation"""
        return {
            "slide_1": f"Yeni video geldi! 🎬\n{title}",
            "slide_2": f"Kaçırmayın 👆\nLink bio'da!",
            "poll_sticker": f"İzlediniz mi?\n✅ Evet  ❌ Hayır"
        }

    def _generate_twitter_thread(self, title: str, script: str, keywords: List[str],
                                   youtube_url: str) -> List[str]:
        """Generate viral Twitter thread"""
        template = random.choice(X_THREAD_TEMPLATES)
        sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 15]
        n = min(len(sentences), 8)

        tweets = []
        # Tweet 1: Hook
        tweets.append(template.format(title=title, n=n))

        # Tweets 2-N: Content
        for i, sentence in enumerate(sentences[:n-2], 2):
            tweets.append(f"{i}/{n+1}\n\n{sentence[:250]}")

        # Last tweet: CTA
        tweets.append(
            f"{n+1}/{n+1}\n\n"
            f"Daha fazlası için tam video:\n"
            f"👇 {youtube_url}\n\n"
            f"Bu thread faydalıysa RT eder misiniz? 🙏"
        )

        return tweets

    def _generate_facebook_post(self, title: str, script: str, keywords: List[str],
                                 youtube_url: str) -> str:
        """Generate Facebook long-form post"""
        sentences = [s.strip() for s in script.split('.') if s.strip()][:5]
        intro = ' '.join(sentences)[:600] if sentences else title
        return (
            f"📌 {title}\n\n"
            f"{intro}\n\n"
            f"Tüm detaylar için video:\n"
            f"▶️ {youtube_url}\n\n"
            f"Arkadaşlarınızı etiketleyin! 👇"
        )

    def _generate_community_poll_options(self, keywords: List[str]) -> List[str]:
        """Generate YouTube Community poll options"""
        if keywords:
            kw = keywords[0]
            return [
                f"Evet, {kw} konusunu biliyorum",
                f"Hayır, {kw} hakkında yeniyim",
                f"{kw} hakkında daha fazla video istiyorum",
                "Başka bir konu öner"
            ]
        return ["Çok faydalı!", "Daha fazlasını istiyorum!", "İlk defa duyuyorum", "Bunu araştıracağım"]

    def _generate_community_announcement(self, title: str) -> str:
        """Generate pre-upload community announcement"""
        return (
            f"🎬 2 saat sonra yeni video!\n\n"
            f"'{title}'\n\n"
            f"Hazır mısınız? 👀 Zil butonuna bastınız mı? 🔔"
        )

    def _generate_platform_hashtags(self, keywords: List[str], platform: str) -> List[str]:
        """Generate platform-optimized hashtags"""
        base_tags = [f"#{kw.replace(' ', '').lower()}" for kw in keywords[:5]]

        platform_tags = {
            "tiktok": ["#fyp", "#viral", "#keşfet", "#foryoupage", "#trending"],
            "instagram": ["#instagood", "#reels", "#explore", "#viral", "#türkiye"],
            "twitter": ["#trending", "#viral"],
            "facebook": ["#video", "#viral"],
        }

        extra = platform_tags.get(platform, [])
        return list(dict.fromkeys(base_tags + extra))  # Deduplicated

    def get_adapter_status(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "supported_platforms": ["tiktok", "instagram", "twitter", "facebook", "youtube_community"],
            "total_adaptations": len(self.adaptations_history),
            "instagram_luts": list(INSTAGRAM_LUTS.keys()),
            "health_status": "healthy"
        }


# Global instance
multiverse_adapter = MultiverseAdapter()
