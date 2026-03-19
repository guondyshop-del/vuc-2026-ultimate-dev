"""
VUC-2026 Ghost Personas System
Otonom etkileşim için AI karakterleri yönetimi

Bu sistem, her kanalın nişine özel 5 farklı AI karakteri yaratır
ve videoları bu karakterlerle otomatik olarak yönetir.
"""

import logging
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class GhostPersona:
    """Ghost Karakteri sınıfı"""
    
    def __init__(self, name: str, niche: str, personality: Dict[str, Any], 
                 avatar: str, background: str):
        self.name = name
        self.niche = niche
        self.personality = personality
        self.avatar = avatar
        self.background = background
        self.comment_history = []
        self.engagement_stats = {
            "comments_posted": 0,
            "replies_given": 0,
            "likes_received": 0,
            "conversations_started": 0
        }
        self.last_activity = datetime.now()
    
    def generate_comment(self, video_context: Dict[str, Any]) -> Dict[str, Any]:
        """Video için yorum oluştur"""
        try:
            # Kişilik özelliklerine göre yorum oluştur
            comment_style = self.personality.get("comment_style", "supportive")
            tone = self.personality.get("tone", "friendly")
            expertise_level = self.personality.get("expertise_level", "intermediate")
            
            # Video bağlamını analiz et
            video_title = video_context.get("title", "")
            video_description = video_context.get("description", "")
            target_keywords = video_context.get("target_keywords", [])
            
            # Yorum şablonları
            templates = self._get_comment_templates(comment_style, tone)
            
            # Uygun şablon seç ve özelleştir
            template = random.choice(templates)
            
            comment = template.format(
                video_title=video_title,
                personal_touch=self.personality.get("personal_touch", ""),
                expertise_note=self._get_expertise_note(expertise_level, video_context),
                question=self._get_contextual_question(target_keywords, expertise_level),
                encouragement=self._get_encouragement(tone)
            )
            
            # Anahtar kelime ekle
            if target_keywords and random.random() > 0.3:
                keyword = random.choice(target_keywords)
                comment += f" #{keyword}"
            
            return {
                "persona": self.name,
                "comment": comment,
                "style": comment_style,
                "tone": tone,
                "expertise_level": expertise_level,
                "includes_keywords": bool(target_keywords and random.random() > 0.3),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Yorum oluşturma hatası ({self.name}): {e}")
            return {
                "persona": self.name,
                "comment": "Harika video!",
                "style": "simple",
                "error": str(e)
            }
    
    def _get_comment_templates(self, style: str, tone: str) -> List[str]:
        """Yorum şablonları"""
        templates = {
            "supportive": {
                "friendly": [
                    "Harika işçivmi {video_title}! {personal_touch} {expertise_note}",
                    "Bu konuda emek harcamışsınız {encouragement}",
                    "Çok faydalı içerik {personal_touch} {question}"
                ],
                "professional": [
                    "Teknik olarak çok başarılı bir çalışma {video_title}. {expertise_note}",
                    "Değerli katkı sağlıyorsunuz {encouragement}",
                    "Bu alanda daha fazla içeriğinizı bekleriz {question}"
                ]
            },
            "analytical": {
                "neutral": [
                    "İlginç analiz {video_title}. {expertise_note}",
                    "Veri noktasından bakıldığında {personal_touch}",
                    "Ek perspektifler {question}"
                ],
                "detailed": [
                    "Derinlemesine güzel {video_title}. {expertise_note}",
                    "İstatistiklerinizı paylaşırmısınız mı? {personal_touch}",
                    "Karşılaştırmalı analiz {question}"
                ]
            },
            "enthusiastic": {
                "energetic": [
                    "MÜKEMMEL! 🎉 {video_title} {personal_touch}",
                    "Bu harikaydı! {expertise_note} {encouragement}",
                    "DAHA FAZLASI! 🔥 {question}"
                ],
                "casual": [
                    "Vay bea! {video_title} {personal_touch}",
                    "Super içerik! {expertise_note} {encouragement}",
                    "Ne düşünüyorsun? {question}"
                ]
            },
            "controversial": {
                "challenging": [
                    "Farklı bir bakış açısı {video_title}. {personal_touch}",
                    "Peki ya bu noktayı düşündünüz mü? {expertise_note}",
                    "Tartışmaya açık {question}"
                ],
                "provocative": [
                    "Bu gerçekten doğru mu? {video_title} {personal_touch}",
                    "Kanıtlarınızı paylaşır mısınız? {expertise_note}",
                    "Alternatif teoriler {question}"
                ]
            }
        }
        
        return templates.get(style, {}).get(tone, ["Harika video!"])
    
    def _get_expertise_note(self, level: str, context: Dict[str, Any]) -> str:
        """Uzmanlık notu oluştur"""
        notes = {
            "beginner": "Bu alanda yeniyseniz çok iyi ilerliyorsunuz.",
            "intermediate": "Uzmanlığını konuşturuyorsunuz.",
            "advanced": "Derin bilgileriniz paylaşımda değerli.",
            "expert": "Sektör lideri olarak öncülük ediyorsunuz."
        }
        
        # Nişe özel notlar
        niche_notes = {
            "technology": "Teknik detaylarınız çok doğru.",
            "business": "İş dünyası içgörüleriniz değerli.",
            "education": "Eğitim yaklaşımınız etkili.",
            "entertainment": "Eğlence sektöründe fark yaratıyorsunuz.",
            "gaming": "Oyun stratejileriniz orijinal."
        }
        
        base_note = notes.get(level, "")
        niche_note = niche_notes.get(context.get("niche", ""), "")
        
        return f"{base_note} {niche_note}" if niche_note else base_note
    
    def _get_contextual_question(self, keywords: List[str], level: str) -> str:
        """Bağlamsal soru oluştur"""
        if not keywords:
            return ""
        
        questions = {
            "beginner": [
                f"Bu konuda daha fazla öğrenmek ister misiniz?",
                "Başlangıç için ne önerirsiniz?",
                "En çok zorlandığınız nokta neydi?"
            ],
            "intermediate": [
                f"Bu yaklaşımı nasıl geliştirebiliriz?",
                f"#{random.choice(keywords)} hakkında ne düşünüyorsunuz?",
                "Karşılaştığınız zorluklar neler?"
            ],
            "advanced": [
                f"İleri seviye teknikleri paylaşır mısınız?",
                f"Bu alandaki yenilikleri takip ediyor musunuz?",
                "Sektör trendlerini nasıl değerlendiriyorsunuz?"
            ],
            "expert": [
                f"Bu alandaki geleceği nasıl görüyorsunuz?",
                f"Yeni girişimciler için ne tavsiye edersiniz?",
                f"Endüstri standartlarını nasıl etkiliyorsunuz?"
            ]
        }
        
        level_questions = questions.get(level, ["Ne düşünüyorsunuz?"])
        return random.choice(level_questions)
    
    def _get_encouragement(self, tone: str) -> str:
        """Teşvik mesajı oluştur"""
        encouragements = {
            "friendly": "Başarılar dilerim!",
            "professional": "Değerli katkılarınız için teşekkürler.",
            "neutral": "İlerlemeye devam.",
            "energetic": "DEVAM ET! 🔥",
            "casual": "Harika gidiyor!",
            "challenging": "Düşünmeye devam.",
            "provocative": "Tartışmaya devam."
        }
        
        return encouragements.get(tone, "Başarılar!")
    
    def start_conversation(self, other_persona: str, initial_message: str) -> Dict[str, Any]:
        """Diğer karakterle sohbet başlat"""
        conversation = {
            "participants": [self.name, other_persona],
            "started_by": self.name,
            "initial_message": initial_message,
            "messages": [
                {
                    "sender": self.name,
                    "message": initial_message,
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "status": "active",
            "started_at": datetime.now().isoformat()
        }
        
        self.engagement_stats["conversations_started"] += 1
        self.last_activity = datetime.now()
        
        return conversation
    
    def reply_to_conversation(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Sohbete yanıt ver"""
        reply = {
            "conversation_id": conversation_id,
            "sender": self.name,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "reply_style": self.personality.get("reply_style", "constructive")
        }
        
        self.engagement_stats["replies_given"] += 1
        self.last_activity = datetime.now()
        
        return reply

class GhostPersonaManager:
    """Ghost Karakterleri Yöneticisi"""
    
    def __init__(self):
        self.personas = {}
        self.niche_personas = {
            "technology": [
                {
                    "name": "TechWizard",
                    "personality": {
                        "comment_style": "analytical",
                        "tone": "professional",
                        "expertise_level": "advanced",
                        "personal_touch": "Teknik detaylarınız çok doğru.",
                        "reply_style": "constructive"
                    },
                    "avatar": "🧙‍♂️",
                    "background": "10+ yıl yazılım geliştirme deneyimi, AI/ML uzmanı"
                },
                {
                    "name": "CodeNinja",
                    "personality": {
                        "comment_style": "supportive",
                        "tone": "friendly",
                        "expertise_level": "expert",
                        "personal_touch": "Kod sanatı gibi!",
                        "reply_style": "helpful"
                    },
                    "avatar": "🥷",
                    "background": "Full-stack developer, open source katkıcısı"
                }
            ],
            "business": [
                {
                    "name": "BusinessGuru",
                    "personality": {
                        "comment_style": "analytical",
                        "tone": "professional",
                        "expertise_level": "expert",
                        "personal_touch": "İş dünyası içgörüleriniz değerli.",
                        "reply_style": "strategic"
                    },
                    "avatar": "👨‍💼",
                    "background": "MBA, 15+ yıl iş deneyimi, startup kurucusu"
                },
                {
                    "name": "StartupMentor",
                    "personality": {
                        "comment_style": "supportive",
                        "tone": "friendly",
                        "expertise_level": "advanced",
                        "personal_touch": "Girişimci ruhunu anlıyorum!",
                        "reply_style": "encouraging"
                    },
                    "avatar": "🚀",
                    "background": "Venture Capitalist, startup danışmanı"
                }
            ],
            "education": [
                {
                    "name": "ProfWisdom",
                    "personality": {
                        "comment_style": "analytical",
                        "tone": "professional",
                        "expertise_level": "expert",
                        "personal_touch": "Eğitim yaklaşımınız etkili.",
                        "reply_style": "educational"
                    },
                    "avatar": "👨‍🏫",
                    "background": "PhD, 20+ yıl akademik deneyim"
                },
                {
                    "name": "StudyBuddy",
                    "personality": {
                        "comment_style": "supportive",
                        "tone": "friendly",
                        "expertise_level": "intermediate",
                        "personal_touch": "Birlikte öğrenelim!",
                        "reply_style": "collaborative"
                    },
                    "avatar": "📚",
                    "background": "Öğrenci, öğrenme meraklısı"
                }
            ],
            "entertainment": [
                {
                    "name": "MemeLord",
                    "personality": {
                        "comment_style": "enthusiastic",
                        "tone": "casual",
                        "expertise_level": "advanced",
                        "personal_touch": "Viral content! 😂",
                        "reply_style": "humorous"
                    },
                    "avatar": "😎",
                    "background": "İnternet kültürü uzmanı, meme kralı"
                },
                {
                    "name": "FunExpert",
                    "personality": {
                        "comment_style": "supportive",
                        "tone": "energetic",
                        "expertise_level": "intermediate",
                        "personal_touch": "Eğlence her zaman! 🎉",
                        "reply_style": "engaging"
                    },
                    "avatar": "🎭",
                    "background": "Eğlence sektörü analisti, trend avcısı"
                }
            ],
            "gaming": [
                {
                    "name": "ProGamer",
                    "personality": {
                        "comment_style": "analytical",
                        "tone": "competitive",
                        "expertise_level": "expert",
                        "personal_touch": "GG WP!",
                        "reply_style": "strategic"
                    },
                    "avatar": "🎮",
                    "background": "E-spor oyuncusu, 10+ yıl profesyonel gaming"
                },
                {
                    "name": "GameStrategist",
                    "personality": {
                        "comment_style": "supportive",
                        "tone": "friendly",
                        "expertise_level": "advanced",
                        "personal_touch": "Meta build harikası!",
                        "reply_style": "helpful"
                    },
                    "avatar": "🎯",
                    "background": "Oyun teoristi, strateji uzmanı"
                }
            ]
        }
        
        self.active_conversations = {}
        self.engagement_analytics = {}
    
    def initialize_personas(self, channel_niche: str) -> Dict[str, GhostPersona]:
        """Kanal nişine göre karakterleri başlat"""
        if channel_niche not in self.niche_personas:
            # Varsayılan karakterleri kullan
            channel_niche = "technology"
        
        niche_configs = self.niche_personas[channel_niche]
        
        for config in niche_configs:
            persona = GhostPersona(
                name=config["name"],
                niche=channel_niche,
                personality=config["personality"],
                avatar=config["avatar"],
                background=config["background"]
            )
            
            self.personas[config["name"]] = persona
        
        logger.info(f"{channel_niche} nişi için {len(self.personas)} karakter başlatıldı")
        return self.personas
    
    async def deploy_personas_to_video(self, video_id: str, video_context: Dict[str, Any]) -> Dict[str, Any]:
        """Video için karakterleri konuşlandır"""
        try:
            deployment_results = {
                "video_id": video_id,
                "deployment_time": datetime.now().isoformat(),
                "personas_deployed": list(self.personas.keys()),
                "comment_strategy": self._get_commenting_strategy(video_context),
                "comments": [],
                "conversations": [],
                "engagement_plan": self._create_engagement_plan(video_context)
            }
            
            # İlk yorumları oluştur (ilk 15 dakika içinde)
            for persona_name, persona in self.personas.items():
                # Her karakterin yorumlama zamanlaması
                delay = self._get_commenting_delay(persona.personality)
                
                # Yorum oluştur
                comment = persona.generate_comment(video_context)
                comment["scheduled_time"] = (datetime.now() + timedelta(minutes=delay)).isoformat()
                comment["status"] = "scheduled"
                
                deployment_results["comments"].append(comment)
            
            # Konuşma planları oluştur
            conversation_plan = self._plan_conversations(video_context)
            deployment_results["conversations"] = conversation_plan
            
            return {
                "success": True,
                "deployment": deployment_results,
                "analytics": {
                    "total_personas": len(self.personas),
                    "expected_comments": len(deployment_results["comments"]),
                    "conversation_pairs": len(conversation_plan),
                    "engagement_potential": self._calculate_engagement_potential(video_context)
                }
            }
            
        except Exception as e:
            logger.error(f"Karakter konuşlandırma hatası: {e}")
            return {
                "success": False,
                "error": str(e),
                "video_id": video_id
            }
    
    def _get_commenting_strategy(self, video_context: Dict[str, Any]) -> Dict[str, Any]:
        """Yorumlama stratejisi belirle"""
        video_type = video_context.get("content_type", "educational")
        
        strategies = {
            "educational": {
                "initial_burst": 3,  # İlk 3 yorum
                "spacing_minutes": 5,  # Aralık 5 dakika
                "persona_rotation": True,  # Karakter rotasyonu
                "keyword_inclusion": 0.8,  # %80 anahtar kelime
                "conversation_trigger": 10  # 10 yorumdan sonra sohbet
            },
            "entertainment": {
                "initial_burst": 5,
                "spacing_minutes": 2,
                "persona_rotation": True,
                "keyword_inclusion": 0.6,
                "conversation_trigger": 8
            },
            "business": {
                "initial_burst": 2,
                "spacing_minutes": 10,
                "persona_rotation": False,
                "keyword_inclusion": 0.9,
                "conversation_trigger": 15
            },
            "gaming": {
                "initial_burst": 4,
                "spacing_minutes": 3,
                "persona_rotation": True,
                "keyword_inclusion": 0.7,
                "conversation_trigger": 12
            }
        }
        
        return strategies.get(video_type, strategies["educational"])
    
    def _get_commenting_delay(self, personality: Dict[str, Any]) -> int:
        """Karaktere özel yorumlama gecikmesi"""
        style = personality.get("comment_style", "supportive")
        expertise = personality.get("expertise_level", "intermediate")
        
        # Uzmanlık seviyesine göre gecikme
        base_delays = {
            "beginner": 8,    # Başlangıç seviyesi
            "intermediate": 5,  # Orta seviye
            "advanced": 3,     # İleri seviye
            "expert": 1          # Uzman seviyesi
        }
        
        # Yorum stiline göre ek gecikme
        style_delays = {
            "analytical": 2,    # Analitik yorumlar daha uzun sürer
            "supportive": 0,     # Destekleyici yorumlar hızlı
            "enthusiastic": -1, # Hevesli yorumlar daha hızlı
            "controversial": 3    # Tartışmalı yorumlar daha yavaş
        }
        
        base_delay = base_delays.get(expertise, 5)
        style_delay = style_delays.get(style, 0)
        
        return max(1, base_delay + style_delay)
    
    def _create_engagement_plan(self, video_context: Dict[str, Any]) -> Dict[str, Any]:
        """Etkileşim planı oluştur"""
        return {
            "phase_1": {
                "duration_minutes": 30,
                "goal": "İlk etkileşim dalgası oluştur",
                "actions": ["initial_comments", "like_strategic_comments"],
                "target_engagement": 50
            },
            "phase_2": {
                "duration_minutes": 60,
                "goal": "Sohbetleri başlat",
                "actions": ["start_conversations", "reply_to_comments"],
                "target_engagement": 100
            },
            "phase_3": {
                "duration_minutes": 120,
                "goal": "Session Time sinyali gönder",
                "actions": ["sustain_conversations", "create_threads"],
                "target_engagement": 200
            }
        }
    
    def _plan_conversations(self, video_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sohbet planları oluştur"""
        conversations = []
        persona_names = list(self.personas.keys())
        
        # Farklı karakterler arasında sohbetler oluştur
        for i in range(0, len(persona_names), 2):
            if i + 1 < len(persona_names):
                persona1 = self.personas[persona_names[i]]
                persona2 = self.personas[persona_names[i + 1]]
                
                # Sohbet başlatma mesajı
                initial_message = persona1.generate_comment(video_context)["comment"]
                
                conversation = {
                    "participants": [persona1.name, persona2.name],
                    "initiator": persona1.name,
                    "scheduled_time": (datetime.now() + timedelta(minutes=15 * (i + 1))).isoformat(),
                    "initial_message": initial_message,
                    "expected_duration_minutes": 20,
                    "goal": "Session Time sinyali oluştur"
                }
                
                conversations.append(conversation)
        
        return conversations
    
    def _calculate_engagement_potential(self, video_context: Dict[str, Any]) -> int:
        """Etkileşim potansiyelini hesapla"""
        base_potential = 100
        
        # Video türüne göre çarpan
        content_type = video_context.get("content_type", "educational")
        type_multipliers = {
            "educational": 1.2,
            "entertainment": 1.5,
            "business": 0.8,
            "gaming": 1.8
        }
        
        multiplier = type_multipliers.get(content_type, 1.0)
        return int(base_potential * multiplier)
    
    def get_persona_analytics(self, persona_name: str = None) -> Dict[str, Any]:
        """Karakter analitiğini al"""
        if persona_name:
            # Tekil karakter analitiği
            if persona_name in self.personas:
                persona = self.personas[persona_name]
                return {
                    "persona": persona_name,
                    "niche": persona.niche,
                    "engagement_stats": persona.engagement_stats,
                    "last_activity": persona.last_activity,
                    "comment_history": persona.comment_history[-10:]  # Son 10 yorum
                }
        else:
            # Tüm karakterlerin analitiği
            return {
                "total_personas": len(self.personas),
                "active_conversations": len(self.active_conversations),
                "total_engagement": {
                    "comments_posted": sum(p.engagement_stats["comments_posted"] for p in self.personas.values()),
                    "replies_given": sum(p.engagement_stats["replies_given"] for p in self.personas.values()),
                    "conversations_started": sum(p.engagement_stats["conversations_started"] for p in self.personas.values())
                },
                "persona_performance": {
                    name: {
                        "engagement_rate": p.engagement_stats["comments_posted"] / max(1, (datetime.now() - p.last_activity).total_seconds() / 3600),
                        "last_activity": p.last_activity
                    }
                    for name, p in self.personas.items()
                }
            }

# Global instance
ghost_persona_manager = GhostPersonaManager()
