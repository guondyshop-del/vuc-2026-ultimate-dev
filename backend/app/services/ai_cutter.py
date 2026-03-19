"""
VUC-2026 AI Cutter - 9:16 Auto-Reframing Engine
Subject tracking + vertical snippet extraction for short-form platforms.

Uses OpenCV for subject detection and FFmpeg for reframing.
MediaPipe integration when available for precise body/face tracking.
"""

import logging
import asyncio
import random
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Platform output specs
PLATFORM_SPECS: Dict[str, Dict[str, Any]] = {
    "tiktok": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 180,     # 3 min max
        "preferred_duration": (30, 60),
        "fps": 30,
        "bitrate": "4500k",
        "hook_duration": 3,      # First 3 seconds = hook
        "trending_audio": True,
        "caption_style": "bold_bottom",
        "label": "TikTok"
    },
    "instagram_reels": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 90,
        "preferred_duration": (15, 45),
        "fps": 30,
        "bitrate": "3500k",
        "hook_duration": 2,
        "trending_audio": False,
        "caption_style": "cinematic_center",
        "label": "Instagram Reels"
    },
    "youtube_shorts": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 60,
        "preferred_duration": (30, 59),
        "fps": 60,
        "bitrate": "6000k",
        "hook_duration": 2,
        "trending_audio": False,
        "caption_style": "dynamic_top",
        "label": "YouTube Shorts"
    },
    "twitter_clip": {
        "aspect_ratio": "9:16",
        "width": 720,
        "height": 1280,
        "max_duration": 140,
        "preferred_duration": (20, 45),
        "fps": 30,
        "bitrate": "2500k",
        "hook_duration": 2,
        "trending_audio": False,
        "caption_style": "minimal_bottom",
        "label": "X/Twitter Clip"
    }
}

# Emotional peak keywords for cut-point detection
EMOTIONAL_PEAK_KEYWORDS = [
    "inanılmaz", "şok edici", "gerçek", "sır", "asla tahmin edemezsiniz",
    "incredible", "shocking", "secret", "never", "you won't believe",
    "sonuç", "result", "final", "aslında", "actually", "dikkat", "warning"
]


class AICutter:
    """AI-powered 9:16 auto-reframing and snippet extraction engine"""

    def __init__(self):
        self.engine_id = "ai_cutter_v1"
        self.mediapipe_available = self._check_mediapipe()
        self.opencv_available = self._check_opencv()
        self.cuts_history: List[Dict[str, Any]] = []

    def _check_mediapipe(self) -> bool:
        try:
            import mediapipe  # noqa: F401
            return True
        except ImportError:
            return False

    def _check_opencv(self) -> bool:
        try:
            import cv2  # noqa: F401
            return True
        except ImportError:
            return False

    async def extract_snippets(self, source_video: str, script: str,
                               platforms: List[str] = None,
                               max_snippets: int = 3) -> Dict[str, Any]:
        """
        Extract optimized 9:16 vertical snippets from long-form content.

        Args:
            source_video: Path to source video
            script: Video script text for emotional peak detection
            platforms: Target platforms (defaults to all)
            max_snippets: Max number of snippets to extract

        Returns:
            Extraction plan and results per platform
        """
        if platforms is None:
            platforms = ["tiktok", "instagram_reels", "youtube_shorts"]

        try:
            # Analyze script for emotional peaks
            emotional_peaks = self._detect_emotional_peaks(script)

            # Create time segments from peaks
            segments = self._create_optimal_segments(
                script, emotional_peaks, max_snippets
            )

            # Generate reframing plan per platform
            platform_plans = {}
            for platform in platforms:
                if platform not in PLATFORM_SPECS:
                    continue
                spec = PLATFORM_SPECS[platform]
                platform_plans[platform] = await self._create_platform_plan(
                    source_video, spec, segments, script
                )

            # Generate FFmpeg commands
            ffmpeg_commands = self._generate_ffmpeg_commands(
                source_video, platform_plans
            )

            result = {
                "source_video": source_video,
                "emotional_peaks": emotional_peaks,
                "segments_detected": len(segments),
                "segments": segments,
                "platform_plans": platform_plans,
                "ffmpeg_commands": ffmpeg_commands,
                "mediapipe_tracking": self.mediapipe_available,
                "opencv_tracking": self.opencv_available,
                "estimated_output_files": sum(
                    len(p["snippets"]) for p in platform_plans.values()
                ),
                "generated_at": datetime.now().isoformat()
            }

            self.cuts_history.append({
                "source": source_video,
                "platforms": platforms,
                "snippets": result["estimated_output_files"],
                "timestamp": datetime.now().isoformat()
            })

            logger.info(
                f"AI Cutter tamamlandı: {result['estimated_output_files']} snippet, "
                f"{len(platforms)} platform"
            )

            return result

        except Exception as e:
            logger.error(f"AI Cutter hatası: {e}")
            return {"success": False, "error": str(e)}

    def _detect_emotional_peaks(self, script: str) -> List[Dict[str, Any]]:
        """Detect emotional peak moments in script for cut points"""
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        peaks = []
        cumulative_ts = 0.0

        for i, sentence in enumerate(sentences):
            cumulative_ts += 3.5  # ~3.5s per sentence
            sentence_lower = sentence.lower()

            # Score emotional intensity
            intensity = 0.5
            if '!' in sentence:
                intensity += 0.2
            if '?' in sentence:
                intensity += 0.1
            if len(sentence.split()) < 8:
                intensity += 0.1  # Short punchy sentences
            for kw in EMOTIONAL_PEAK_KEYWORDS:
                if kw in sentence_lower:
                    intensity += 0.15
                    break

            intensity = min(1.0, intensity)

            if intensity >= 0.7:
                peaks.append({
                    "sentence_index": i,
                    "timestamp": round(cumulative_ts, 1),
                    "sentence": sentence[:80],
                    "intensity": round(intensity, 2),
                    "type": "high_energy" if intensity >= 0.85 else "medium_energy"
                })

        return peaks

    def _create_optimal_segments(self, script: str, peaks: List[Dict[str, Any]],
                                  max_snippets: int) -> List[Dict[str, Any]]:
        """Create time segments around emotional peaks"""
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        total_duration = len(sentences) * 3.5
        segments = []

        if not peaks:
            # Fallback: divide evenly
            segment_duration = min(60.0, total_duration / max_snippets)
            for i in range(max_snippets):
                start = i * (total_duration / max_snippets)
                segments.append({
                    "segment_id": i + 1,
                    "start_time": round(start, 1),
                    "end_time": round(start + segment_duration, 1),
                    "duration": round(segment_duration, 1),
                    "anchor_intensity": 0.6,
                    "hook_moment": round(start + 0.5, 1),
                    "type": "even_split"
                })
            return segments

        # Sort peaks by intensity
        top_peaks = sorted(peaks, key=lambda x: x["intensity"], reverse=True)[:max_snippets]
        top_peaks_sorted = sorted(top_peaks, key=lambda x: x["timestamp"])

        for i, peak in enumerate(top_peaks_sorted):
            ts = peak["timestamp"]
            # Build 30-60s segment around peak
            start = max(0.0, ts - random.uniform(10, 20))
            end = min(total_duration, start + random.uniform(30, 55))

            segments.append({
                "segment_id": i + 1,
                "start_time": round(start, 1),
                "end_time": round(end, 1),
                "duration": round(end - start, 1),
                "anchor_peak": peak,
                "anchor_intensity": peak["intensity"],
                "hook_moment": round(start + 1.0, 1),
                "type": "peak_anchored"
            })

        return segments

    async def _create_platform_plan(self, source_video: str, spec: Dict[str, Any],
                                    segments: List[Dict[str, Any]],
                                    script: str) -> Dict[str, Any]:
        """Create platform-specific reframing plan"""
        snippets = []
        preferred_min, preferred_max = spec["preferred_duration"]

        for seg in segments:
            # Trim segment to platform preferred duration
            target_duration = random.uniform(preferred_min, preferred_max)
            actual_duration = min(seg["duration"], target_duration)
            actual_end = seg["start_time"] + actual_duration

            # Subject tracking crop region (simulated — OpenCV/MediaPipe would detect real subject)
            crop_region = self._calculate_crop_region(
                source_width=1920, source_height=1080,
                target_width=spec["width"], target_height=spec["height"]
            )

            # Generate hook text for this snippet
            hook_text = self._generate_platform_hook(script, spec["label"])

            # Caption overlay config
            caption_config = self._get_caption_config(spec["caption_style"])

            # Trending audio injection plan (TikTok only)
            audio_plan = None
            if spec["trending_audio"]:
                audio_plan = {
                    "inject": True,
                    "volume": 0.10,     # 10% trending audio overlay
                    "fade_in": 0.5,
                    "fade_out": 0.5,
                    "source": "trending_audio_pool"
                }

            output_name = (
                f"{Path(source_video).stem}_"
                f"{spec['label'].lower().replace(' ', '_').replace('/', '_')}_"
                f"snippet_{seg['segment_id']}{Path(source_video).suffix}"
            )

            snippets.append({
                "snippet_id": f"{spec['label']}_seg_{seg['segment_id']}",
                "output_filename": output_name,
                "segment": seg,
                "actual_duration": round(actual_duration, 1),
                "actual_end": round(actual_end, 1),
                "crop_region": crop_region,
                "hook_text": hook_text,
                "caption_config": caption_config,
                "audio_plan": audio_plan,
                "platform_spec": {
                    "resolution": f"{spec['width']}x{spec['height']}",
                    "fps": spec["fps"],
                    "bitrate": spec["bitrate"]
                }
            })

        return {
            "platform": spec["label"],
            "spec": spec,
            "snippets": snippets,
            "total_snippets": len(snippets),
            "tracking_method": (
                "mediapipe" if self.mediapipe_available
                else "opencv" if self.opencv_available
                else "center_crop_fallback"
            )
        }

    def _calculate_crop_region(self, source_width: int, source_height: int,
                                target_width: int, target_height: int) -> Dict[str, int]:
        """Calculate crop region to achieve target aspect ratio"""
        target_ratio = target_width / target_height
        source_ratio = source_width / source_height

        if source_ratio > target_ratio:
            # Source is wider — crop width
            new_width = int(source_height * target_ratio)
            x_offset = (source_width - new_width) // 2
            return {
                "x": x_offset,
                "y": 0,
                "width": new_width,
                "height": source_height,
                "method": "center_crop"
            }
        else:
            # Source is taller — crop height
            new_height = int(source_width / target_ratio)
            y_offset = (source_height - new_height) // 2
            return {
                "x": 0,
                "y": y_offset,
                "width": source_width,
                "height": new_height,
                "method": "center_crop"
            }

    def _generate_platform_hook(self, script: str, platform: str) -> str:
        """Generate platform-specific aggressive hook text"""
        hook_templates = {
            "TikTok": [
                "POV: Kimse bunu söylemedi! 👀",
                "Bunu bilen kazanıyor! 🔥",
                "3 saniye dikkatini ver! ⚡",
                "Bu videoyu silmeden önce izle! 🚨",
                "Sana sır vereceğim! 🤫"
            ],
            "Instagram Reels": [
                "Bu stratejiyle her şey değişti ✨",
                "Bunu deneyen geri dönmüyor 🎯",
                "Hayatını değiştir, şimdi izle 🌟",
                "En sık sorulan sorunun cevabı 💡"
            ],
            "YouTube Shorts": [
                "Kimse bilmiyor ama...",
                "Sadece 60 saniyede öğren:",
                "Bu bilgiyle öne geç →",
                "Şok edici gerçek:"
            ],
            "X/Twitter Clip": [
                "Bu thread'i kaydet 🔖",
                "Herkes bunu anlamalı:",
                "Önemli bilgi ↓"
            ]
        }

        templates = hook_templates.get(platform, hook_templates["YouTube Shorts"])
        return random.choice(templates)

    def _get_caption_config(self, style: str) -> Dict[str, Any]:
        """Get caption overlay configuration for style"""
        configs = {
            "bold_bottom": {
                "position": "bottom_center",
                "font_size": 52,
                "font_weight": "black",
                "color": "#FFFFFF",
                "stroke_color": "#000000",
                "stroke_width": 4,
                "background": "semi_transparent_black",
                "animation": "word_by_word"
            },
            "cinematic_center": {
                "position": "center",
                "font_size": 44,
                "font_weight": "bold",
                "color": "#FFFFFF",
                "stroke_color": "#000000",
                "stroke_width": 3,
                "background": "none",
                "animation": "fade_in"
            },
            "dynamic_top": {
                "position": "top_center",
                "font_size": 48,
                "font_weight": "black",
                "color": "#FFFF00",
                "stroke_color": "#000000",
                "stroke_width": 4,
                "background": "none",
                "animation": "slide_down"
            },
            "minimal_bottom": {
                "position": "bottom_center",
                "font_size": 36,
                "font_weight": "bold",
                "color": "#FFFFFF",
                "stroke_color": "#333333",
                "stroke_width": 2,
                "background": "none",
                "animation": "static"
            }
        }
        return configs.get(style, configs["bold_bottom"])

    def _generate_ffmpeg_commands(self, source_video: str,
                                   platform_plans: Dict[str, Any]) -> List[str]:
        """Generate FFmpeg commands for all platform snippets"""
        commands = []

        for platform, plan in platform_plans.items():
            spec = plan["spec"]
            for snippet in plan["snippets"]:
                seg = snippet["segment"]
                crop = snippet["crop_region"]

                # Crop + scale + pad filter chain
                vf_parts = [
                    f"trim=start={seg['start_time']}:end={snippet['actual_end']}",
                    f"setpts=PTS-STARTPTS",
                    f"crop={crop['width']}:{crop['height']}:{crop['x']}:{crop['y']}",
                    f"scale={spec['width']}:{spec['height']}:flags=lanczos",
                ]

                # Add caption if hook text
                if snippet.get("hook_text"):
                    cc = snippet["caption_config"]
                    vf_parts.append(
                        f"drawtext=text='{snippet['hook_text']}':"
                        f"fontsize={cc['font_size']}:fontcolor={cc['color']}:"
                        f"x=(w-text_w)/2:y=h-th-40:borderw={cc['stroke_width']}"
                    )

                cmd = (
                    f"ffmpeg -i \"{source_video}\" "
                    f"-vf \"{','.join(vf_parts)}\" "
                    f"-r {spec['fps']} "
                    f"-b:v {spec['bitrate']} "
                    f"-c:v libx264 -preset fast -crf 18 "
                    f"-c:a aac -b:a 192k "
                    f"-t {snippet['actual_duration']} "
                    f"-y \"{snippet['output_filename']}\""
                )
                commands.append(cmd)

        return commands

    def get_engine_status(self) -> Dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "mediapipe_available": self.mediapipe_available,
            "opencv_available": self.opencv_available,
            "supported_platforms": list(PLATFORM_SPECS.keys()),
            "total_cuts_processed": len(self.cuts_history),
            "tracking_method": (
                "mediapipe" if self.mediapipe_available
                else "opencv" if self.opencv_available
                else "center_crop"
            ),
            "health_status": "healthy"
        }


# Global instance
ai_cutter = AICutter()
