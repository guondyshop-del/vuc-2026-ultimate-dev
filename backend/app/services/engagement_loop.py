"""
VUC-2026 Engagement Loop
Persona-driven debate injection to boost session time and velocity metrics.

Personas start meaningful comment debates that drag viewers into
conversation threads, increasing dwell time and engagement signals.
"""

import logging
import asyncio
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


DEBATE_SEEDS: Dict[str, List[Dict[str, str]]] = {
    "technology": [
        {
            "opener": "Açıkçası yapay zeka bu kadar hızlı gelişmeseydi daha iyi olurdu 🤔",
            "counter": "Katılmıyorum tamamen, hız inovasyon demek. Sormak istediğim...",
            "reply_1": "İkisinin de haklı yanları var ama asıl mesele şu:",
            "reply_2": "Bence buradaki asıl soru şu: bu değişim kimin lehine?"
        },
        {
            "opener": "Bu videodan önce tamamen farklı düşünüyordum 😮",
            "counter": "Hangi kısım sizi en çok etkiledi? Benim için 3. bölüm oyunun kurallarını değiştirdi",
            "reply_1": "Evet 3. bölüm harika ama ben 5. bölümü daha önemli buldum:",
            "reply_2": "İkisi de güçlüydü. Peki pratikte nasıl uygulayacaksınız?"
        }
    ],
    "business": [
        {
            "opener": "Bu stratejiyi 6 ay önce bilseydim çok farklı kararlar alırdım",
            "counter": "Hangi kısmını uyguladınız? Ben 2. maddeyi denedim, sonuçlar ilginç...",
            "reply_1": "2. madde gerçekten kritik. Ben üçüncüden başladım:",
            "reply_2": "Deneyimlerinizi merak ettim. Hangi sektörde kullandınız?"
        }
    ],
    "education": [
        {
            "opener": "Bu teknikleri öğrencilerime uygulamaya başladım, fark inanılmaz!",
            "counter": "Kaç yaş grubu için kullandınız? Üniversite öğrencileri için farklı sonuçlar veriyor mu?",
            "reply_1": "Üniversite için biraz modifiye etmek gerekiyor ama temeli aynı:",
            "reply_2": "Kesinlikle yaş grubuna göre adapte etmek şart. Ben şöyle yaklaştım:"
        }
    ],
    "gaming": [
        {
            "opener": "Bu strateji yanlış 😤 Üst seviyede işe yaramaz",
            "counter": "Hangi rank'ta oynadın? Gold'dan sonra gerçekten değişiyor mu?",
            "reply_1": "Diamond+ için şunu söyleyebilirim, meta çok farklı:",
            "reply_2": "Rank bağımlı kesinlikle. Hangi karakter/sınıfı kullanıyorsun?"
        }
    ],
    "general": [
        {
            "opener": "Herkes bu videoyu izlemeli! 🙌",
            "counter": "Hangi kısmı en çok etkiledi sizi? Özellikle merak ettim...",
            "reply_1": "Ben 3. bölümü gerçek hayatta uyguladım, sonuçları paylaşayım:",
            "reply_2": "Teori güzel ama pratikte nasıl işliyor? Deneyenler var mı?"
        }
    ]
}

TIMESTAMP_COMMENT_TEMPLATES = [
    "{ts} anını tekrar tekrar izledim 😮 Bu bilgiyi neden kimse söylemedi?",
    "Herkese {ts} bölümüne bakmasını tavsiye ederim 🔥",
    "{ts} - bu kısım her şeyi değiştiriyor!",
    "Not aldım: {ts} → bu altın bilgi",
    "{ts}'de söylenen şey gerçek mi? Araştırdım ve...",
]


class EngagementLoop:
    """Persona debate injector for session time manipulation"""

    def __init__(self):
        self.active_debates: Dict[str, List[Dict[str, Any]]] = {}
        self.debate_history: List[Dict[str, Any]] = []
        self.velocity_metrics: Dict[str, Dict[str, float]] = {}

    async def inject_debate(self, video_id: str, niche: str,
                            persona_ids: List[str],
                            video_duration_seconds: int = 600) -> Dict[str, Any]:
        """
        Inject a coordinated debate thread to a video.

        Args:
            video_id: Target video ID
            niche: Content niche
            persona_ids: Personas to use (at least 2)
            video_duration_seconds: Used to generate timestamp comments

        Returns:
            Debate plan with comment thread and timing strategy
        """
        try:
            if len(persona_ids) < 2:
                persona_ids = persona_ids + [f"auto_persona_{random.randint(1, 999)}"]

            seeds = DEBATE_SEEDS.get(niche, DEBATE_SEEDS["general"])
            seed = random.choice(seeds)

            # Build multi-persona comment thread
            thread = await self._build_debate_thread(seed, persona_ids, video_id)

            # Generate timestamp comments
            timestamp_comments = self._generate_timestamp_comments(
                video_duration_seconds, persona_ids
            )

            # Timing strategy (staggered to look organic)
            timing_plan = self._create_timing_plan(thread + timestamp_comments)

            # Predict session time impact
            session_impact = self._predict_session_time_impact(
                thread, timestamp_comments
            )

            debate_record = {
                "debate_id": f"debate_{video_id}_{int(datetime.now().timestamp())}",
                "video_id": video_id,
                "niche": niche,
                "personas_used": persona_ids,
                "thread": thread,
                "timestamp_comments": timestamp_comments,
                "timing_plan": timing_plan,
                "session_impact_prediction": session_impact,
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }

            self.active_debates.setdefault(video_id, []).append(debate_record)
            self.debate_history.append(debate_record)

            logger.info(
                f"Debate enjeksiyonu: {video_id} — {len(thread)} yorum, "
                f"tahmini +{session_impact['session_time_increase_pct']:.1f}% oturum süresi"
            )

            return debate_record

        except Exception as e:
            logger.error(f"Engagement Loop hatası: {e}")
            return {"success": False, "error": str(e), "video_id": video_id}

    async def _build_debate_thread(self, seed: Dict[str, str],
                                    personas: List[str],
                                    video_id: str) -> List[Dict[str, Any]]:
        """Build a coordinated multi-turn debate thread"""
        thread = []
        now = datetime.now()

        # Comment 1: Persona A opens with opinion
        thread.append({
            "comment_id": f"c_{video_id}_1",
            "persona": personas[0],
            "content": seed["opener"],
            "type": "opener",
            "reply_to": None,
            "scheduled_delay_minutes": random.randint(5, 20),
            "scheduled_at": (now + timedelta(minutes=random.randint(5, 20))).isoformat(),
            "likes_target": random.randint(8, 35),
            "is_pinnable": False
        })

        # Comment 2: Persona B counters
        thread.append({
            "comment_id": f"c_{video_id}_2",
            "persona": personas[1],
            "content": seed["counter"],
            "type": "counter",
            "reply_to": f"c_{video_id}_1",
            "scheduled_delay_minutes": random.randint(8, 25),
            "scheduled_at": (now + timedelta(minutes=random.randint(25, 45))).isoformat(),
            "likes_target": random.randint(5, 20),
            "is_pinnable": False
        })

        # Comment 3: Third persona adds nuance
        if len(personas) >= 3:
            third_persona = personas[2]
        else:
            third_persona = f"organic_user_{random.randint(100, 999)}"

        thread.append({
            "comment_id": f"c_{video_id}_3",
            "persona": third_persona,
            "content": seed.get("reply_1", "Bence ikisi de harika noktalara değindi 🤔"),
            "type": "nuance",
            "reply_to": f"c_{video_id}_1",
            "scheduled_delay_minutes": random.randint(30, 60),
            "scheduled_at": (now + timedelta(minutes=random.randint(60, 90))).isoformat(),
            "likes_target": random.randint(3, 15),
            "is_pinnable": False
        })

        # Comment 4: Creator-style engagement hook (pinnable)
        thread.append({
            "comment_id": f"c_{video_id}_4",
            "persona": personas[0],
            "content": seed.get("reply_2", "Bu tartışmayı görmek harika 💪 Ne düşünüyorsunuz?"),
            "type": "engagement_hook",
            "reply_to": None,
            "scheduled_delay_minutes": random.randint(90, 180),
            "scheduled_at": (now + timedelta(minutes=random.randint(120, 180))).isoformat(),
            "likes_target": random.randint(15, 50),
            "is_pinnable": True
        })

        return thread

    def _generate_timestamp_comments(self, video_duration: int,
                                      personas: List[str]) -> List[Dict[str, Any]]:
        """Generate timestamp-based comments to boost indexing"""
        comments = []
        now = datetime.now()

        # Pick 2-3 strategic timestamps
        strategic_points = [
            int(video_duration * 0.15),
            int(video_duration * 0.45),
            int(video_duration * 0.80)
        ]

        for i, ts_seconds in enumerate(strategic_points[:2]):
            mins, secs = divmod(ts_seconds, 60)
            ts_str = f"{mins}:{secs:02d}"
            template = random.choice(TIMESTAMP_COMMENT_TEMPLATES)
            content = template.format(ts=ts_str)

            comments.append({
                "comment_id": f"ts_comment_{i}",
                "persona": personas[i % len(personas)],
                "content": content,
                "type": "timestamp",
                "timestamp_seconds": ts_seconds,
                "timestamp_display": ts_str,
                "reply_to": None,
                "scheduled_delay_minutes": random.randint(10, 60),
                "scheduled_at": (now + timedelta(minutes=random.randint(10, 60))).isoformat(),
                "likes_target": random.randint(5, 25),
                "is_pinnable": False
            })

        return comments

    def _create_timing_plan(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create staggered timing plan to appear organic"""
        sorted_comments = sorted(comments, key=lambda x: x["scheduled_delay_minutes"])
        total_window = max(c["scheduled_delay_minutes"] for c in comments) if comments else 0

        return {
            "total_comments": len(comments),
            "deployment_window_minutes": total_window,
            "average_gap_minutes": total_window / max(len(comments), 1),
            "pinnable_comment": next(
                (c["comment_id"] for c in comments if c.get("is_pinnable")), None
            ),
            "schedule": [
                {
                    "comment_id": c["comment_id"],
                    "persona": c["persona"],
                    "delay_minutes": c["scheduled_delay_minutes"],
                    "type": c["type"]
                }
                for c in sorted_comments
            ]
        }

    def _predict_session_time_impact(self, thread: List[Dict],
                                      timestamp_comments: List[Dict]) -> Dict[str, Any]:
        """Predict impact on session time and engagement signals"""
        debate_length = len(thread)
        ts_count = len(timestamp_comments)
        pinnable_count = sum(1 for c in thread if c.get("is_pinnable"))

        # Empirical estimates
        session_increase = (debate_length * 3.5) + (ts_count * 5.0) + (pinnable_count * 8.0)
        velocity_boost = debate_length * 0.8 + ts_count * 0.5

        return {
            "session_time_increase_pct": round(min(session_increase, 45.0), 1),
            "comment_velocity_boost": round(velocity_boost, 1),
            "engagement_depth_score": round(debate_length * 1.2, 1),
            "timestamp_seo_impact": ts_count * 2,
            "estimated_thread_replies": random.randint(3, 15),
            "prediction_confidence": 0.72
        }

    async def boost_top_comments(self, video_id: str,
                                  target_comment_ids: List[str]) -> Dict[str, Any]:
        """
        Coordinate persona likes on specific comments to boost them to top.

        Args:
            video_id: Video ID
            target_comment_ids: Comment IDs to boost

        Returns:
            Boost plan
        """
        boost_actions = []

        for comment_id in target_comment_ids:
            likes_needed = random.randint(10, 30)
            for i in range(likes_needed):
                boost_actions.append({
                    "action": "like",
                    "comment_id": comment_id,
                    "persona": f"auto_liker_{random.randint(100, 999)}",
                    "delay_seconds": i * random.randint(30, 120),
                    "timestamp": datetime.now().isoformat()
                })

        logger.info(f"Comment boost planlandı: {len(boost_actions)} eylem")

        return {
            "video_id": video_id,
            "target_comments": target_comment_ids,
            "boost_actions": len(boost_actions),
            "execution_window_minutes": len(boost_actions) * 0.5,
            "status": "scheduled"
        }

    def get_engagement_summary(self) -> Dict[str, Any]:
        """Get engagement loop summary"""
        total_debates = len(self.debate_history)
        active_videos = len(self.active_debates)
        total_comments = sum(
            len(d.get("thread", [])) + len(d.get("timestamp_comments", []))
            for d in self.debate_history
        )

        return {
            "total_debates_injected": total_debates,
            "active_video_debates": active_videos,
            "total_comments_generated": total_comments,
            "avg_session_impact_pct": round(
                sum(
                    d.get("session_impact_prediction", {}).get("session_time_increase_pct", 0)
                    for d in self.debate_history
                ) / max(total_debates, 1),
                1
            ),
            "health_status": "healthy"
        }


# Global instance
engagement_loop = EngagementLoop()
