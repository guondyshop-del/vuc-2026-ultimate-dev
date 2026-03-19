"""
VUC-2026 Thumbnail Color Gap Analyzer
Competitor palette analysis + opposite-spectrum generation

Scrapes competitor thumbnails, extracts dominant color palettes,
then generates high-contrast complementary color schemes to dominate
the Explore page through visual differentiation.
"""

import logging
import asyncio
import random
import colorsys
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))  # type: ignore


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex string"""
    return f"#{r:02X}{g:02X}{b:02X}"


def _rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB (0-255) to HSV (0-1 range)"""
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert HSV (0-1) to RGB (0-255)"""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def _complementary_color(hex_color: str) -> str:
    """Generate complementary (opposite) color on color wheel"""
    r, g, b = _hex_to_rgb(hex_color)
    h, s, v = _rgb_to_hsv(r, g, b)
    # Rotate 180° on hue wheel
    h_comp = (h + 0.5) % 1.0
    # Maximize contrast: flip value
    v_comp = 1.0 - v * 0.3
    s_comp = min(1.0, s * 1.2)
    cr, cg, cb = _hsv_to_rgb(h_comp, s_comp, v_comp)
    return _rgb_to_hex(cr, cg, cb)


def _contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG contrast ratio between two colors"""
    def relative_luminance(r, g, b):
        vals = [c / 255 for c in (r, g, b)]
        return sum(
            v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
            for v, w in zip(vals, [0.2126, 0.7152, 0.0722])
        )

    def rl(hex_c):
        r, g, b = _hex_to_rgb(hex_c)
        return relative_luminance(r, g, b)

    L1, L2 = rl(hex1), rl(hex2)
    lighter, darker = max(L1, L2), min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)


class ThumbnailAnalyzer:
    """Competitor thumbnail color gap analyzer and dominant palette generator"""

    def __init__(self):
        self.analyzer_id = "thumbnail_analyzer_v1"
        self.analysis_history: List[Dict[str, Any]] = []

        # Simulated color palettes for common YouTube niches
        self._niche_palette_db: Dict[str, List[List[str]]] = {
            "technology": [
                ["#0066FF", "#1A1A2E", "#FFFFFF", "#00D4FF"],
                ["#6C63FF", "#282828", "#FFFFFF", "#FF6584"],
                ["#00FF41", "#0D0208", "#FFFFFF", "#008F11"],
            ],
            "business": [
                ["#2C3E50", "#E74C3C", "#FFFFFF", "#3498DB"],
                ["#1ABC9C", "#2C3E50", "#FFFFFF", "#E74C3C"],
                ["#F39C12", "#2C3E50", "#FFFFFF", "#1ABC9C"],
            ],
            "education": [
                ["#3498DB", "#FFFFFF", "#2C3E50", "#E74C3C"],
                ["#9B59B6", "#FFFFFF", "#2C3E50", "#1ABC9C"],
                ["#E67E22", "#FFFFFF", "#2C3E50", "#3498DB"],
            ],
            "gaming": [
                ["#9B59B6", "#1A1A2E", "#00FF41", "#FFFFFF"],
                ["#E74C3C", "#1A1A2E", "#FFFFFF", "#F39C12"],
                ["#00BCD4", "#1A1A2E", "#FF4081", "#FFFFFF"],
            ],
            "entertainment": [
                ["#FF4081", "#1A1A2E", "#FFFFFF", "#FFD700"],
                ["#FF6B6B", "#292929", "#FFFFFF", "#4ECDC4"],
                ["#F7DC6F", "#1A1A2E", "#E74C3C", "#FFFFFF"],
            ],
        }

    async def analyze_competitor_thumbnails(self, niche: str,
                                             competitor_channels: List[str] = None,
                                             sample_count: int = 20) -> Dict[str, Any]:
        """
        Analyze competitor thumbnails to find color gaps.

        Args:
            niche: Content niche
            competitor_channels: List of competitor channel IDs
            sample_count: Number of thumbnails to analyze

        Returns:
            Color gap analysis with gap colors and palette recommendations
        """
        try:
            # Extract competitor dominant palettes (simulated — real: use YouTube Data API + PIL)
            competitor_palettes = await self._extract_competitor_palettes(
                niche, competitor_channels, sample_count
            )

            # Identify dominant colors in the competitive landscape
            dominant_colors = self._identify_dominant_colors(competitor_palettes)

            # Find color gaps (underutilized spectrum areas)
            color_gaps = self._find_color_gaps(dominant_colors)

            # Generate winning thumbnail palette
            winning_palette = self._generate_winning_palette(
                dominant_colors, color_gaps
            )

            # Calculate contrast scores
            contrast_analysis = self._analyze_contrast(
                winning_palette, dominant_colors
            )

            # Generate design recommendations
            design_recommendations = self._generate_design_recommendations(
                winning_palette, color_gaps, niche
            )

            result = {
                "niche": niche,
                "thumbnails_analyzed": sample_count,
                "competitor_palette_summary": self._summarize_palettes(competitor_palettes),
                "dominant_competitor_colors": dominant_colors,
                "color_gaps": color_gaps,
                "winning_palette": winning_palette,
                "contrast_analysis": contrast_analysis,
                "design_recommendations": design_recommendations,
                "visual_dominance_score": self._calculate_dominance_score(
                    winning_palette, dominant_colors
                ),
                "analyzed_at": datetime.now().isoformat()
            }

            self.analysis_history.append({
                "niche": niche,
                "dominance_score": result["visual_dominance_score"],
                "timestamp": result["analyzed_at"]
            })

            logger.info(
                f"Thumbnail analizi: {niche} — "
                f"Hakimiyet skoru: {result['visual_dominance_score']:.1f}/10"
            )

            return result

        except Exception as e:
            logger.error(f"Thumbnail analiz hatası: {e}")
            return {"success": False, "error": str(e)}

    async def _extract_competitor_palettes(self, niche: str,
                                            competitor_channels: Optional[List[str]],
                                            sample_count: int) -> List[Dict[str, Any]]:
        """Extract dominant palettes from competitor thumbnails"""
        await asyncio.sleep(0.1)  # Simulate API/scraping delay

        palettes_db = self._niche_palette_db.get(niche, self._niche_palette_db["entertainment"])
        results = []

        for i in range(min(sample_count, 15)):
            palette = random.choice(palettes_db)
            # Add slight variation
            varied_palette = []
            for color in palette:
                r, g, b = _hex_to_rgb(color)
                # ±15 variation
                r = max(0, min(255, r + random.randint(-15, 15)))
                g = max(0, min(255, g + random.randint(-15, 15)))
                b = max(0, min(255, b + random.randint(-15, 15)))
                varied_palette.append(_rgb_to_hex(r, g, b))

            results.append({
                "thumbnail_index": i + 1,
                "channel": f"competitor_{i+1}",
                "dominant_colors": varied_palette,
                "views": random.randint(10000, 2000000),
                "ctr": random.uniform(2.0, 12.0)
            })

        return results

    def _identify_dominant_colors(self, palettes: List[Dict]) -> List[Dict[str, Any]]:
        """Identify most frequently used colors across competitors"""
        color_freq: Dict[str, Dict[str, Any]] = {}

        for palette_data in palettes:
            for color in palette_data["dominant_colors"]:
                r, g, b = _hex_to_rgb(color)
                h, s, v = _rgb_to_hsv(r, g, b)

                # Quantize hue to 30° buckets (12 segments)
                hue_bucket = int(h * 12) / 12
                bucket_key = f"hue_{int(hue_bucket * 360)}"

                if bucket_key not in color_freq:
                    color_freq[bucket_key] = {
                        "representative_color": color,
                        "hue_degrees": int(hue_bucket * 360),
                        "count": 0,
                        "avg_saturation": 0,
                        "avg_value": 0,
                        "colors": []
                    }

                color_freq[bucket_key]["count"] += 1
                color_freq[bucket_key]["avg_saturation"] += s
                color_freq[bucket_key]["avg_value"] += v
                color_freq[bucket_key]["colors"].append(color)

        # Normalize averages
        for data in color_freq.values():
            n = max(data["count"], 1)
            data["avg_saturation"] = round(data["avg_saturation"] / n, 2)
            data["avg_value"] = round(data["avg_value"] / n, 2)
            data["frequency_pct"] = round(data["count"] / max(len(palettes), 1) * 100, 1)

        return sorted(color_freq.values(), key=lambda x: x["count"], reverse=True)[:6]

    def _find_color_gaps(self, dominant_colors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find underutilized hue regions on the color wheel"""
        occupied_hues = set(d["hue_degrees"] for d in dominant_colors)

        # Check all 12 hue buckets (30° each)
        all_buckets = set(range(0, 360, 30))
        empty_buckets = all_buckets - occupied_hues

        gaps = []
        for hue_deg in sorted(empty_buckets):
            h = hue_deg / 360
            # Generate vivid representative color for this gap
            r, g, b = _hsv_to_rgb(h, 0.85, 0.95)
            gap_color = _rgb_to_hex(r, g, b)
            gaps.append({
                "hue_degrees": hue_deg,
                "gap_color": gap_color,
                "opportunity_level": "high" if hue_deg not in {h+15 for h in occupied_hues} else "medium",
                "description": self._describe_hue(hue_deg)
            })

        return gaps[:5]  # Top 5 gaps

    def _describe_hue(self, hue_deg: int) -> str:
        """Describe a hue bucket in plain language"""
        descriptions = {
            0: "Kırmızı tonu", 30: "Turuncu tonu", 60: "Sarı tonu",
            90: "Sarı-yeşil tonu", 120: "Yeşil tonu", 150: "Açık yeşil tonu",
            180: "Cyan tonu", 210: "Açık mavi tonu", 240: "Mavi tonu",
            270: "Mor-mavi tonu", 300: "Mor tonu", 330: "Pembe-kırmızı tonu"
        }
        return descriptions.get(hue_deg, f"{hue_deg}° tonu")

    def _generate_winning_palette(self, dominant_colors: List[Dict],
                                   color_gaps: List[Dict]) -> Dict[str, Any]:
        """Generate a thumbnail palette that stands out from competitors"""
        if not color_gaps:
            # No gaps — use complementary of most dominant
            most_dominant = dominant_colors[0]["representative_color"] if dominant_colors else "#3498DB"
            primary = _complementary_color(most_dominant)
        else:
            # Use the highest opportunity gap color
            primary = color_gaps[0]["gap_color"]

        r, g, b = _hex_to_rgb(primary)
        h, s, v = _rgb_to_hsv(r, g, b)

        # Secondary: complementary
        secondary = _complementary_color(primary)

        # Accent: triadic (120° offset)
        h_accent = (h + 1/3) % 1.0
        ar, ag, ab = _hsv_to_rgb(h_accent, min(1.0, s * 1.1), v)
        accent = _rgb_to_hex(ar, ag, ab)

        # Background: deep dark for contrast
        bg = "#0D0D0D" if v > 0.5 else "#F5F5F5"

        # Text: maximum contrast to primary
        text = "#FFFFFF" if v > 0.4 else "#1A1A1A"

        return {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "background": bg,
            "text": text,
            "palette_name": f"Gap-Dominant-{color_gaps[0]['hue_degrees'] if color_gaps else 'Complementary'}",
            "contrast_with_background": round(_contrast_ratio(primary, bg), 2)
        }

    def _analyze_contrast(self, winning_palette: Dict,
                           dominant_colors: List[Dict]) -> Dict[str, Any]:
        """Analyze how winning palette contrasts with competitive landscape"""
        competitor_rep_colors = [d["representative_color"] for d in dominant_colors[:3]]

        contrast_scores = []
        for comp_color in competitor_rep_colors:
            score = _contrast_ratio(winning_palette["primary"], comp_color)
            contrast_scores.append(round(score, 2))

        avg_contrast = sum(contrast_scores) / max(len(contrast_scores), 1)

        return {
            "avg_contrast_vs_competitors": round(avg_contrast, 2),
            "min_contrast": min(contrast_scores) if contrast_scores else 0,
            "max_contrast": max(contrast_scores) if contrast_scores else 0,
            "contrast_scores": contrast_scores,
            "stands_out": avg_contrast >= 3.0,
            "wcag_passes": avg_contrast >= 4.5
        }

    def _generate_design_recommendations(self, palette: Dict, gaps: List[Dict],
                                          niche: str) -> List[str]:
        """Generate actionable thumbnail design recommendations"""
        recs = [
            f"Ana renk: {palette['primary']} — rakiplerde yok, öne çıkacaksın",
            f"Arka plan: {palette['background']} — maksimum kontrast",
            f"Metin rengi: {palette['text']}",
            f"Vurgu rengi: {palette['accent']} — CTA elementler için",
        ]

        if gaps:
            recs.append(f"Kullanılmamış renk boşluğu: {gaps[0]['description']}")

        niche_tips = {
            "technology": "Minimal tasarım, tek bold element, 3 kelimeden az metin",
            "business": "Profesyonel yüz + büyük rakam/başarı metriği",
            "education": "Adım numarası + meraklı soru formatı",
            "gaming": "Aksiyon karesi + neon renk glow efekti",
            "entertainment": "Abartılı yüz ifadesi + kontrast arka plan"
        }
        if niche in niche_tips:
            recs.append(f"Niş önerisi: {niche_tips[niche]}")

        contrast_ratio = palette.get("contrast_with_background", 0)
        if contrast_ratio < 4.5:
            recs.append(f"⚠️ Kontrast oranı {contrast_ratio:.1f} — 4.5+ hedefle")
        else:
            recs.append(f"✅ Kontrast oranı {contrast_ratio:.1f} — Mükemmel görünürlük")

        return recs

    def _summarize_palettes(self, palettes: List[Dict]) -> Dict[str, Any]:
        """Summarize competitor palette data"""
        avg_ctr = sum(p["ctr"] for p in palettes) / max(len(palettes), 1)
        top_performers = sorted(palettes, key=lambda x: x["ctr"], reverse=True)[:3]

        return {
            "total_analyzed": len(palettes),
            "avg_competitor_ctr": round(avg_ctr, 2),
            "top_performer_ctr": round(top_performers[0]["ctr"], 2) if top_performers else 0,
            "top_performer_colors": top_performers[0]["dominant_colors"] if top_performers else []
        }

    def _calculate_dominance_score(self, palette: Dict,
                                    dominant_colors: List[Dict]) -> float:
        """Score how dominant the generated palette will be (0-10)"""
        score = 5.0

        contrast = palette.get("contrast_with_background", 1.0)
        if contrast >= 7.0:
            score += 2.5
        elif contrast >= 4.5:
            score += 1.5
        elif contrast >= 3.0:
            score += 0.5

        # Check if primary color is truly unique vs competitors
        primary = palette.get("primary", "#000000")
        pr, pg, pb = _hex_to_rgb(primary)
        ph, _, _ = _rgb_to_hsv(pr, pg, pb)

        comp_hues = []
        for dc in dominant_colors:
            cr, cg, cb = _hex_to_rgb(dc["representative_color"])
            ch, _, _ = _rgb_to_hsv(cr, cg, cb)
            comp_hues.append(ch)

        min_hue_diff = min(abs(ph - ch) for ch in comp_hues) if comp_hues else 0.5
        if min_hue_diff > 0.3:
            score += 2.5
        elif min_hue_diff > 0.15:
            score += 1.5

        return min(10.0, round(score, 1))

    def get_analyzer_status(self) -> Dict[str, Any]:
        return {
            "analyzer_id": self.analyzer_id,
            "supported_niches": list(self._niche_palette_db.keys()),
            "analyses_completed": len(self.analysis_history),
            "health_status": "healthy"
        }


# Global instance
thumbnail_analyzer = ThumbnailAnalyzer()
