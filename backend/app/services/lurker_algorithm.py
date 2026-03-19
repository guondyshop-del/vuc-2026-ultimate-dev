"""
VUC-2026 Lurker Algorithm
Behavioral humanization for ghost personas

This service simulates organic human session behavior:
searching, watching, liking, and commenting with realistic
timing patterns before uploading to build trust scores.
"""

import logging
import asyncio
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class LurkerAlgorithm:
    """Simulates organic human browsing sessions for trust building"""

    def __init__(self):
        self.session_patterns = {
            "morning":   {"start": 7,  "end": 10, "weight": 0.20},
            "afternoon": {"start": 12, "end": 15, "weight": 0.30},
            "evening":   {"start": 18, "end": 22, "weight": 0.40},
            "night":     {"start": 22, "end": 24, "weight": 0.10},
        }
        self.human_delays = {
            "page_scroll": (0.8, 3.5),       # seconds
            "video_pause": (2.0, 8.0),
            "typing_speed": (0.06, 0.18),    # seconds per character
            "search_pause": (1.5, 4.0),
            "reaction_time": (0.3, 1.2),
            "between_videos": (5.0, 25.0),
            "comment_read": (3.0, 12.0),
        }
        self.trust_metrics: Dict[str, float] = {}
        self.session_history: List[Dict[str, Any]] = []

    async def run_lurker_session(self, persona_id: str, niche: str,
                                  duration_minutes: int = 20) -> Dict[str, Any]:
        """
        Simulate a full organic browsing session for a persona.

        Args:
            persona_id: Ghost persona identifier
            niche: Content niche to browse
            duration_minutes: Total session duration in minutes

        Returns:
            Session results with trust score delta
        """
        session_id = f"lurk_{persona_id}_{int(datetime.now().timestamp())}"
        start_time = datetime.now()
        actions_performed = []
        trust_delta = 0.0

        logger.info(f"Lurker oturumu başlatıldı: {persona_id} — Niş: {niche}")

        try:
            # 1. Initial search behavior
            search_actions = await self._simulate_search_session(niche)
            actions_performed.extend(search_actions)
            trust_delta += len(search_actions) * 0.5

            # 2. Watch competitor videos
            watch_actions = await self._simulate_watch_session(niche, duration_minutes // 3)
            actions_performed.extend(watch_actions)
            trust_delta += sum(a.get("watch_percentage", 0) for a in watch_actions) * 0.1

            # 3. Engagement (likes, comments on competitors)
            engagement_actions = await self._simulate_engagement(niche)
            actions_performed.extend(engagement_actions)
            trust_delta += len(engagement_actions) * 1.2

            # 4. Scroll homepage / trending
            scroll_actions = await self._simulate_homepage_scroll()
            actions_performed.extend(scroll_actions)
            trust_delta += len(scroll_actions) * 0.3

            # Update trust score
            prev_score = self.trust_metrics.get(persona_id, 0.0)
            new_score = min(10.0, prev_score + trust_delta * 0.1)
            self.trust_metrics[persona_id] = new_score

            session_result = {
                "session_id": session_id,
                "persona_id": persona_id,
                "niche": niche,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
                "actions_performed": len(actions_performed),
                "trust_delta": round(trust_delta, 2),
                "new_trust_score": round(new_score, 2),
                "action_breakdown": self._summarize_actions(actions_performed),
                "status": "completed"
            }

            self.session_history.append(session_result)
            logger.info(f"Lurker oturumu tamamlandı: {persona_id} — Güven: +{trust_delta:.1f}")

            return session_result

        except Exception as e:
            logger.error(f"Lurker oturumu hatası: {e}")
            return {
                "session_id": session_id,
                "persona_id": persona_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _simulate_search_session(self, niche: str) -> List[Dict[str, Any]]:
        """Simulate search queries with human-like timing"""
        actions = []
        search_queries = self._generate_search_queries(niche)

        for query in search_queries[:random.randint(2, 4)]:
            # Typing delay
            type_delay = len(query) * random.uniform(*self.human_delays["typing_speed"])
            await asyncio.sleep(min(type_delay, 0.5))  # Capped for simulation speed

            actions.append({
                "type": "search",
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "typing_duration_ms": int(type_delay * 1000)
            })

            # Pause after search results load
            await asyncio.sleep(random.uniform(*self.human_delays["search_pause"]) * 0.1)

        return actions

    async def _simulate_watch_session(self, niche: str,
                                       max_minutes: int) -> List[Dict[str, Any]]:
        """Simulate watching videos with realistic retention"""
        actions = []
        video_topics = self._generate_video_topics(niche)
        watch_budget_seconds = max_minutes * 60

        for topic in video_topics[:random.randint(2, 5)]:
            if watch_budget_seconds <= 0:
                break

            # Random video length (2-15 mins)
            video_duration = random.randint(120, 900)

            # Human retention: watch 40-85% of video
            watch_pct = random.uniform(0.40, 0.85)
            watched_seconds = int(video_duration * watch_pct)
            watched_seconds = min(watched_seconds, watch_budget_seconds)

            await asyncio.sleep(0.05)  # Simulation speed-up

            action = {
                "type": "watch",
                "video_topic": topic,
                "video_duration": video_duration,
                "watched_seconds": watched_seconds,
                "watch_percentage": round(watch_pct * 100, 1),
                "paused": random.random() < 0.3,
                "scrubbed": random.random() < 0.2,
                "timestamp": datetime.now().isoformat()
            }
            actions.append(action)
            watch_budget_seconds -= watched_seconds

            # Gap between videos
            await asyncio.sleep(random.uniform(1, 3) * 0.02)

        return actions

    async def _simulate_engagement(self, niche: str) -> List[Dict[str, Any]]:
        """Simulate likes and comments on competitor content"""
        actions = []

        # Like some videos (30% chance per viewed video)
        for _ in range(random.randint(1, 4)):
            if random.random() < 0.30:
                await asyncio.sleep(random.uniform(*self.human_delays["reaction_time"]) * 0.05)
                actions.append({
                    "type": "like",
                    "niche": niche,
                    "timestamp": datetime.now().isoformat()
                })

        # Leave a comment (20% chance)
        if random.random() < 0.20:
            comment_templates = [
                f"Çok güzel içerik, teşekkürler! 👍",
                f"Bu {niche} konusunu çok iyi anlattınız",
                f"Devamını bekliyorum!",
                f"Bilgilendirici video, abone oldum"
            ]
            await asyncio.sleep(random.uniform(*self.human_delays["comment_read"]) * 0.05)
            actions.append({
                "type": "comment",
                "content": random.choice(comment_templates),
                "niche": niche,
                "timestamp": datetime.now().isoformat()
            })

        # Subscribe to 1-2 channels (10% chance)
        if random.random() < 0.10:
            actions.append({
                "type": "subscribe",
                "niche": niche,
                "timestamp": datetime.now().isoformat()
            })

        return actions

    async def _simulate_homepage_scroll(self) -> List[Dict[str, Any]]:
        """Simulate homepage browsing and scroll behavior"""
        actions = []
        scroll_count = random.randint(3, 8)

        for i in range(scroll_count):
            await asyncio.sleep(random.uniform(*self.human_delays["page_scroll"]) * 0.02)
            actions.append({
                "type": "scroll",
                "scroll_depth": random.randint(20, 90),
                "dwell_time_ms": random.randint(800, 4000),
                "timestamp": datetime.now().isoformat()
            })

        return actions

    def _generate_search_queries(self, niche: str) -> List[str]:
        """Generate realistic search queries for niche"""
        query_pools = {
            "technology": [
                "yapay zeka ile para kazanma 2026",
                "python öğrenme rehberi",
                "chatgpt kullanım ipuçları",
                "AI araçları 2026",
                "programlama nasıl öğrenilir"
            ],
            "business": [
                "pasif gelir yolları",
                "dropshipping başlangıç rehberi",
                "e-ticaret 2026",
                "freelance iş bulma",
                "online iş kurma"
            ],
            "education": [
                "verimli ders çalışma teknikleri",
                "not alma yöntemleri",
                "sınav hazırlık ipuçları",
                "öğrenme psikolojisi",
                "hafıza güçlendirme"
            ],
            "gaming": [
                "en iyi oyunlar 2026",
                "gaming setup kurma",
                "e-spor kariyeri nasıl yapılır",
                "fps artırma yöntemleri",
                "oyun içi para kazanma"
            ],
            "general": [
                "youtube izleme",
                "trending videolar",
                "gündem haberleri",
                "eğlenceli videolar",
                "viral içerikler"
            ]
        }
        return query_pools.get(niche, query_pools["general"])

    def _generate_video_topics(self, niche: str) -> List[str]:
        """Generate realistic video topic list for niche"""
        topic_pools = {
            "technology": ["Yapay Zeka Rehberi", "Python İpuçları", "ChatGPT Hacks", "AI Araçları", "Kodlama Eğitimi"],
            "business": ["Pasif Gelir", "E-Ticaret", "Dropshipping", "Yatırım Stratejileri", "Freelance"],
            "education": ["Verimli Ders", "Hafıza Teknikleri", "Sınav Hazırlık", "Öğrenme Psikolojisi"],
            "gaming": ["En İyi Oyunlar", "Gaming Setup", "E-Spor", "FPS Artırma", "Oyun Rehberi"],
            "general": ["Trending Video 1", "Viral İçerik 2", "Eğlenceli Video 3"]
        }
        return topic_pools.get(niche, topic_pools["general"])

    def _summarize_actions(self, actions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Summarize action types"""
        summary: Dict[str, int] = {}
        for action in actions:
            action_type = action.get("type", "unknown")
            summary[action_type] = summary.get(action_type, 0) + 1
        return summary

    def get_trust_score(self, persona_id: str) -> float:
        """Get current trust score for persona"""
        return round(self.trust_metrics.get(persona_id, 0.0), 2)

    def get_all_trust_scores(self) -> Dict[str, float]:
        """Get all persona trust scores"""
        return {k: round(v, 2) for k, v in self.trust_metrics.items()}

    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of all lurker sessions"""
        if not self.session_history:
            return {"total_sessions": 0, "sessions": []}

        completed = [s for s in self.session_history if s.get("status") == "completed"]
        return {
            "total_sessions": len(self.session_history),
            "completed_sessions": len(completed),
            "failed_sessions": len(self.session_history) - len(completed),
            "total_actions": sum(s.get("actions_performed", 0) for s in completed),
            "avg_trust_delta": round(
                sum(s.get("trust_delta", 0) for s in completed) / max(len(completed), 1), 2
            ),
            "active_personas": len(self.trust_metrics),
            "top_trust_personas": sorted(
                self.trust_metrics.items(), key=lambda x: x[1], reverse=True
            )[:5],
            "last_session": self.session_history[-1] if self.session_history else None
        }


# Global instance
lurker_algorithm = LurkerAlgorithm()
