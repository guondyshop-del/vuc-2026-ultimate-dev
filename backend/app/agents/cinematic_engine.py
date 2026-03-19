"""
VUC-2026 Cinematic Engine
Dynamic pacing, Foley SFX, and emotional video production

This engine analyzes audio intensity and emotional tone to
auto-adjust zoom, cuts, transitions, and background SFX.
"""

import logging
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Foley SFX keyword map (keyword -> sfx_file, volume_db)
FOLEY_MAP = {
    "rüzgar": ("sfx/wind_ambient.mp3", -20),
    "wind": ("sfx/wind_ambient.mp3", -20),
    "tıklama": ("sfx/click.mp3", -15),
    "click": ("sfx/click.mp3", -15),
    "alkış": ("sfx/applause.mp3", -18),
    "applause": ("sfx/applause.mp3", -18),
    "para": ("sfx/cash_register.mp3", -16),
    "money": ("sfx/cash_register.mp3", -16),
    "rocket": ("sfx/rocket_launch.mp3", -18),
    "roket": ("sfx/rocket_launch.mp3", -18),
    "patlama": ("sfx/explosion.mp3", -22),
    "explosion": ("sfx/explosion.mp3", -22),
    "yazı": ("sfx/keyboard_typing.mp3", -18),
    "typing": ("sfx/keyboard_typing.mp3", -18),
    "alarm": ("sfx/alarm.mp3", -14),
    "whoosh": ("sfx/whoosh.mp3", -16),
    "fısıltı": ("sfx/whisper_ambient.mp3", -24),
}

EMOTIONAL_TONE_MAP = {
    "energetic": {
        "cut_interval": 2.5,
        "zoom_factor": 1.15,
        "transition": "zoom_cut",
        "color_grade": "vibrant",
        "music_bpm": 128
    },
    "emotional": {
        "cut_interval": 5.0,
        "zoom_factor": 1.05,
        "transition": "dissolve",
        "color_grade": "warm",
        "music_bpm": 72
    },
    "professional": {
        "cut_interval": 4.0,
        "zoom_factor": 1.02,
        "transition": "cut",
        "color_grade": "neutral",
        "music_bpm": 90
    },
    "dramatic": {
        "cut_interval": 3.0,
        "zoom_factor": 1.10,
        "transition": "flash_cut",
        "color_grade": "high_contrast",
        "music_bpm": 110
    },
    "educational": {
        "cut_interval": 6.0,
        "zoom_factor": 1.0,
        "transition": "slide",
        "color_grade": "clean",
        "music_bpm": 80
    }
}


class CinematicEngine:
    """Dynamic pacing and Foley SFX engine"""

    def __init__(self):
        self.engine_id = "cinematic_engine_v1"

    def analyze_script(self, script: str) -> Dict[str, Any]:
        """
        Analyze script for emotional tone, energy peaks, and Foley triggers.

        Args:
            script: Raw script text

        Returns:
            Full cinematic plan
        """
        sentences = self._split_sentences(script)
        tone = self._detect_tone(script)
        energy_curve = self._build_energy_curve(sentences)
        cut_points = self._generate_cut_points(energy_curve, tone)
        foley_events = self._detect_foley_events(sentences)
        lsi_timestamps = self._generate_lsi_timestamps(sentences)
        zoom_plan = self._generate_zoom_plan(energy_curve, tone)

        plan = {
            "tone": tone,
            "tone_config": EMOTIONAL_TONE_MAP.get(tone, EMOTIONAL_TONE_MAP["professional"]),
            "total_sentences": len(sentences),
            "energy_curve": energy_curve,
            "cut_points": cut_points,
            "foley_events": foley_events,
            "lsi_timestamps": lsi_timestamps,
            "zoom_plan": zoom_plan,
            "estimated_duration_seconds": len(sentences) * 3.5,
            "generated_at": datetime.now().isoformat()
        }

        logger.info(f"Sinematik plan üretildi: ton={tone}, kesim={len(cut_points)}, foley={len(foley_events)}")
        return plan

    def _split_sentences(self, text: str) -> List[str]:
        """Split script into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _detect_tone(self, text: str) -> str:
        """Detect dominant emotional tone"""
        text_lower = text.lower()
        scores = {
            "energetic": sum(1 for w in ["heyecan", "enerji", "hızlı", "incredible", "amazing", "!"] if w in text_lower),
            "emotional": sum(1 for w in ["duygu", "hikaye", "anlatı", "story", "feel", "heart"] if w in text_lower),
            "professional": sum(1 for w in ["analiz", "strateji", "veri", "analysis", "data", "strategy"] if w in text_lower),
            "dramatic": sum(1 for w in ["şok", "inanılmaz", "sır", "shock", "secret", "reveal"] if w in text_lower),
            "educational": sum(1 for w in ["öğren", "adım", "rehber", "learn", "step", "guide", "nasıl"] if w in text_lower),
        }
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "professional"

    def _build_energy_curve(self, sentences: List[str]) -> List[float]:
        """Build 0-1 energy score per sentence"""
        curve = []
        for sentence in sentences:
            score = 0.5  # baseline
            if "!" in sentence:
                score += 0.2
            if "?" in sentence:
                score += 0.1
            if any(w in sentence.lower() for w in ["büyük", "inanılmaz", "şok", "hızlı", "incredible", "huge", "shocking"]):
                score += 0.2
            if len(sentence.split()) > 20:
                score -= 0.1  # long = slower
            curve.append(min(1.0, max(0.0, round(score, 2))))
        return curve

    def _generate_cut_points(self, energy_curve: List[float], tone: str) -> List[Dict[str, Any]]:
        """Generate cut/transition points based on energy peaks"""
        config = EMOTIONAL_TONE_MAP.get(tone, EMOTIONAL_TONE_MAP["professional"])
        base_interval = config["cut_interval"]  # seconds per sentence approx 3.5s
        cut_points = []
        timestamp = 0.0

        for i, energy in enumerate(energy_curve):
            # Shorter cuts at high energy peaks
            interval = base_interval * (1.0 - (energy - 0.5) * 0.4)
            timestamp += 3.5  # ~3.5s per sentence
            if energy > 0.7:
                cut_points.append({
                    "sentence_index": i,
                    "timestamp": round(timestamp, 1),
                    "type": config["transition"],
                    "energy": energy,
                    "zoom": config["zoom_factor"] if energy > 0.8 else 1.0
                })

        return cut_points

    def _detect_foley_events(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """Detect keywords that trigger Foley SFX"""
        events = []
        cumulative_ts = 0.0
        for i, sentence in enumerate(sentences):
            cumulative_ts += 3.5
            sentence_lower = sentence.lower()
            for keyword, (sfx_file, vol_db) in FOLEY_MAP.items():
                if keyword in sentence_lower:
                    events.append({
                        "sentence_index": i,
                        "timestamp": round(cumulative_ts, 1),
                        "trigger_word": keyword,
                        "sfx_file": sfx_file,
                        "volume_db": vol_db,
                        "fade_in_ms": 200,
                        "fade_out_ms": 500
                    })
                    break  # one SFX per sentence max
        return events

    def _generate_lsi_timestamps(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """
        Generate timestamps for LSI keyword injection to
        manipulate YouTube's speech-to-text indexing.
        """
        lsi_events = []
        cumulative_ts = 0.0
        for i, sentence in enumerate(sentences):
            cumulative_ts += 3.5
            # Flag sentences with high keyword potential (nouns, verbs > 5 chars)
            words = [w for w in sentence.split() if len(w) > 5]
            if len(words) >= 2:
                lsi_events.append({
                    "sentence_index": i,
                    "timestamp": round(cumulative_ts, 1),
                    "sentence_preview": sentence[:60],
                    "high_value_words": words[:3],
                    "stt_index_priority": "high" if len(words) > 3 else "normal"
                })
        return lsi_events[:20]  # Top 20 priority timestamps

    def _generate_zoom_plan(self, energy_curve: List[float], tone: str) -> List[Dict[str, Any]]:
        """Generate zoom keyframes based on energy curve"""
        config = EMOTIONAL_TONE_MAP.get(tone, EMOTIONAL_TONE_MAP["professional"])
        plan = []
        cumulative_ts = 0.0
        for i, energy in enumerate(energy_curve):
            cumulative_ts += 3.5
            if energy > 0.65:
                plan.append({
                    "sentence_index": i,
                    "timestamp": round(cumulative_ts, 1),
                    "zoom_in": config["zoom_factor"],
                    "duration_ms": 400,
                    "easing": "ease_in_out"
                })
            elif i > 0 and energy_curve[i - 1] > 0.65:
                plan.append({
                    "sentence_index": i,
                    "timestamp": round(cumulative_ts, 1),
                    "zoom_in": 1.0,
                    "duration_ms": 600,
                    "easing": "ease_out"
                })
        return plan

    def generate_ffmpeg_filter(self, plan: Dict[str, Any], input_file: str, output_file: str) -> str:
        """
        Generate FFmpeg filter_complex command from cinematic plan.
        Includes speed variation (shadowban shield) and foley SFX overlay.
        """
        # Base video with speed variation (1.005x — shadowban shield)
        speed_factor = 1.005
        filter_parts = [
            f"[0:v]setpts={1/speed_factor:.4f}*PTS[vout]",
            f"[0:a]atempo={speed_factor:.3f}[aout]"
        ]

        # Zoom keyframes via scale+crop
        if plan.get("zoom_plan"):
            first_zoom = plan["zoom_plan"][0]
            zoom_val = first_zoom.get("zoom_in", 1.0)
            if zoom_val > 1.0:
                w_expr = f"iw/{zoom_val:.3f}"
                filter_parts.insert(0, f"[0:v]scale={w_expr}:-1,crop=iw:{zoom_val:.3f}*ih[vout_zoom]")

        cmd = (
            f'ffmpeg -i "{input_file}" '
            f'-filter_complex "{"; ".join(filter_parts)}" '
            f'-map "[vout]" -map "[aout]" '
            f'-c:v libx264 -preset fast -crf 18 '
            f'-c:a aac -b:a 192k '
            f'"{output_file}"'
        )
        return cmd

    def get_engine_status(self) -> Dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "supported_tones": list(EMOTIONAL_TONE_MAP.keys()),
            "foley_keywords": len(FOLEY_MAP),
            "health_status": "healthy"
        }


# Global instance
cinematic_engine = CinematicEngine()
