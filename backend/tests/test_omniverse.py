"""
VUC-2026 Omniverse Test Suite
Tests for Ghost Cloak, AI Cutter, Multi-Verse Adapter,
Ghost Auditor, Thumbnail Analyzer, and Engagement Loop

Run: pytest backend/tests/test_omniverse.py -v
"""

import asyncio
import pytest
import random
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# GHOST CLOAK TESTS
# ---------------------------------------------------------------------------

class TestGhostCloak:

    def test_hardware_profiles_loaded(self):
        from app.services.ghost_cloak import HARDWARE_PROFILES
        assert "youtube" in HARDWARE_PROFILES
        assert "instagram" in HARDWARE_PROFILES
        assert "tiktok" in HARDWARE_PROFILES
        assert "twitter" in HARDWARE_PROFILES

    def test_youtube_profile_sony(self):
        from app.services.ghost_cloak import HARDWARE_PROFILES
        yt = HARDWARE_PROFILES["youtube"]
        assert yt["make"] == "SONY"
        assert "ILCE-7SM3" in yt["model"]
        assert yt["fps_base"] == 29.97

    def test_instagram_profile_iphone(self):
        from app.services.ghost_cloak import HARDWARE_PROFILES
        ig = HARDWARE_PROFILES["instagram"]
        assert ig["make"] == "Apple"
        assert "iPhone 15 Pro Max" in ig["model"]
        assert ig["extension"] == ".mov"

    def test_tiktok_profile_pixel(self):
        from app.services.ghost_cloak import HARDWARE_PROFILES
        tt = HARDWARE_PROFILES["tiktok"]
        assert tt["make"] == "Google"
        assert "Pixel 8" in tt["model"]

    def test_gps_coordinates_turkey(self):
        from app.services.ghost_cloak import GPS_COORDINATES
        assert len(GPS_COORDINATES) >= 3
        for coord in GPS_COORDINATES:
            assert 36 <= coord["lat"] <= 42
            assert 26 <= coord["lng"] <= 45

    @pytest.mark.asyncio
    async def test_pixel_cloaking_applied(self):
        from app.services.ghost_cloak import GhostCloak, HARDWARE_PROFILES
        cloak = GhostCloak()
        profile = HARDWARE_PROFILES["youtube"]
        result = await cloak._apply_pixel_cloaking("nonexistent.mp4", "output.mp4", profile)
        assert result["applied"] is True
        assert result["fps_base"] == 29.97
        assert result["fps_jittered"] != result["fps_base"]
        assert abs(result["fps_delta"]) < 0.005
        assert 1000 <= result["noise_seed"] <= 9999
        assert 1.003 <= result["speed_factor"] <= 1.008

    @pytest.mark.asyncio
    async def test_hardware_metadata_injection(self):
        from app.services.ghost_cloak import GhostCloak, HARDWARE_PROFILES
        cloak = GhostCloak()
        profile = HARDWARE_PROFILES["instagram"]
        result = await cloak._inject_hardware_metadata("nonexistent.mov", profile)
        assert result["applied"] is True
        assert result["tags_injected"] >= 10
        assert result["hardware_profile"] == profile["device_fingerprint"]
        assert result["metadata_tags"]["Make"] == "Apple"
        assert "gps_city" in result
        assert "serial_number" in result

    @pytest.mark.asyncio
    async def test_full_cloak_pipeline(self):
        from app.services.ghost_cloak import GhostCloak
        cloak = GhostCloak()
        result = await cloak.cloak_video("nonexistent.mp4", "tiktok")
        assert "detection_risk" in result
        assert result["platform"] == "tiktok"
        assert result["hardware_profile"] == "Google Pixel 8"
        assert result["pixel_cloaking"]["applied"] is True
        assert result["metadata_injection"]["applied"] is True

    def test_cloaking_stats_tracked(self):
        from app.services.ghost_cloak import GhostCloak
        cloak = GhostCloak()
        cloak.cloaking_history = [
            {"success": True, "platform": "youtube", "detection_risk": "minimal"},
            {"success": True, "platform": "tiktok", "detection_risk": "low"},
            {"success": False, "platform": "instagram", "detection_risk": "medium"},
        ]
        stats = cloak.get_cloaking_stats()
        assert stats["total_cloaked"] == 3
        assert stats["successful"] == 2
        assert stats["success_rate"] == pytest.approx(66.7, abs=0.5)
        assert "youtube" in stats["platform_breakdown"]

    def test_detection_risk_calculation(self):
        from app.services.ghost_cloak import GhostCloak
        cloak = GhostCloak()
        ffmpeg_success = {"ffmpeg_success": True, "fps_delta": 0.002}
        metadata_success = {"exiftool_success": True}
        risk = cloak._estimate_detection_risk(ffmpeg_success, metadata_success)
        assert risk == "minimal"

    def test_detection_risk_high_on_failure(self):
        from app.services.ghost_cloak import GhostCloak
        cloak = GhostCloak()
        ffmpeg_fail = {"ffmpeg_success": False, "fps_delta": 0.0}
        metadata_fail = {"exiftool_success": False}
        risk = cloak._estimate_detection_risk(ffmpeg_fail, metadata_fail)
        assert risk in ["medium", "high"]


# ---------------------------------------------------------------------------
# AI CUTTER TESTS
# ---------------------------------------------------------------------------

class TestAICutter:

    def test_platform_specs_complete(self):
        from app.services.ai_cutter import PLATFORM_SPECS
        required = ["tiktok", "instagram_reels", "youtube_shorts", "twitter_clip"]
        for platform in required:
            assert platform in PLATFORM_SPECS
            spec = PLATFORM_SPECS[platform]
            assert spec["width"] > 0
            assert spec["height"] > spec["width"]  # Vertical
            assert spec["fps"] > 0

    def test_emotional_peak_detection(self):
        from app.services.ai_cutter import AICutter
        cutter = AICutter()
        script = (
            "Bu inanılmaz bir sonuç! Bakın ne kadar harika! "
            "Normal bir cümle buraya gidiyor. "
            "ŞOCK EDİCİ gerçek şimdi açıklanıyor! "
            "Başka normal bir cümle. "
        )
        peaks = cutter._detect_emotional_peaks(script)
        assert len(peaks) > 0
        for peak in peaks:
            assert peak["intensity"] >= 0.7
            assert "timestamp" in peak

    def test_tiktok_hook_generation(self):
        from app.services.ai_cutter import AICutter, PLATFORM_SPECS
        cutter = AICutter()
        spec = PLATFORM_SPECS["tiktok"]
        hook = cutter._generate_platform_hook("Bu video AI hakkında", "TikTok")
        assert isinstance(hook, str)
        assert len(hook) > 5

    def test_crop_region_16x9_to_9x16(self):
        from app.services.ai_cutter import AICutter
        cutter = AICutter()
        crop = cutter._calculate_crop_region(
            source_width=1920, source_height=1080,
            target_width=1080, target_height=1920
        )
        assert crop["width"] > 0
        assert crop["height"] > 0
        # Result should maintain 9:16 ratio
        ratio = crop["width"] / crop["height"]
        assert ratio == pytest.approx(9/16, abs=0.01)

    def test_caption_config_styles(self):
        from app.services.ai_cutter import AICutter
        cutter = AICutter()
        for style in ["bold_bottom", "cinematic_center", "dynamic_top", "minimal_bottom"]:
            config = cutter._get_caption_config(style)
            assert "position" in config
            assert "font_size" in config
            assert "color" in config

    @pytest.mark.asyncio
    async def test_snippet_extraction_pipeline(self):
        from app.services.ai_cutter import AICutter
        cutter = AICutter()
        script = """
        Merhaba! Bugün inanılmaz bir konuyu ele alacağız!
        Bu bilgi hayatınızı değiştirecek. Hazır mısınız?
        İşte en önemli kısım şimdi geliyor!
        Bu tekniği bilmek büyük avantaj sağlıyor.
        Normal bilgi aktarımı burada devam ediyor.
        Son olarak vurgulamak istediğim şok edici gerçek:
        Bu kadar basit olduğuna inanmak zor!
        """
        result = await cutter.extract_snippets(
            "test_video.mp4", script,
            platforms=["tiktok", "youtube_shorts"],
            max_snippets=2
        )
        assert "platform_plans" in result
        assert "tiktok" in result["platform_plans"]
        assert result["estimated_output_files"] >= 1
        assert result["segments_detected"] >= 1

    def test_ffmpeg_commands_generated(self):
        from app.services.ai_cutter import AICutter, PLATFORM_SPECS
        cutter = AICutter()
        plan = {
            "tiktok": {
                "spec": PLATFORM_SPECS["tiktok"],
                "snippets": [
                    {
                        "segment": {"start_time": 5.0, "end_time": 45.0},
                        "actual_end": 45.0,
                        "actual_duration": 40.0,
                        "crop_region": {"width": 607, "height": 1080, "x": 656, "y": 0},
                        "hook_text": "Bunu kimse bilmiyordu!",
                        "caption_config": cutter._get_caption_config("bold_bottom"),
                        "output_filename": "test_tiktok_snippet_1.mp4"
                    }
                ]
            }
        }
        commands = cutter._generate_ffmpeg_commands("source.mp4", plan)
        assert len(commands) >= 1
        assert "ffmpeg" in commands[0]
        assert "tiktok" in commands[0].lower() or "snippet" in commands[0].lower()


# ---------------------------------------------------------------------------
# MULTI-VERSE ADAPTER TESTS
# ---------------------------------------------------------------------------

class TestMultiverseAdapter:

    @pytest.mark.asyncio
    async def test_tiktok_adaptation(self):
        from app.services.multiverse_adapter import MultiverseAdapter
        adapter = MultiverseAdapter()
        content = {
            "title": "Yapay Zeka ile Para Kazanma",
            "script": "Bu videoda yapay zeka araçlarını ele alıyoruz. İnanılmaz sonuçlar!",
            "keywords": ["yapay zeka", "AI", "para kazanma"],
            "niche": "technology"
        }
        result = await adapter._adapt_tiktok(content)
        assert result["platform"] == "TikTok"
        assert "hook" in result
        assert "hashtags" in result
        assert "caption_variations" in result
        assert len(result["caption_variations"]) >= 1
        assert result["audio_volume"] == 0.10

    @pytest.mark.asyncio
    async def test_instagram_adaptation(self):
        from app.services.multiverse_adapter import MultiverseAdapter, INSTAGRAM_LUTS
        adapter = MultiverseAdapter()
        content = {
            "title": "Business Rehberi",
            "script": "İş dünyasında başarı için stratejiler.",
            "keywords": ["iş", "strateji"],
            "niche": "business"
        }
        result = await adapter._adapt_instagram(content)
        assert result["platform"] == "Instagram"
        assert result["lut_preset"] in INSTAGRAM_LUTS
        assert "caption" in result
        assert "carousel_slides" in result

    @pytest.mark.asyncio
    async def test_twitter_thread_generation(self):
        from app.services.multiverse_adapter import MultiverseAdapter
        adapter = MultiverseAdapter()
        content = {
            "title": "AI Rehberi",
            "script": "Yapay zeka çok önemli bir konudur. Her gün yeni gelişmeler var. Bu alanda uzmanlaşmak gerekiyor. Adım adım öğrenmek mümkün.",
            "keywords": ["AI"],
            "youtube_url": "https://youtube.com/watch?v=test"
        }
        result = await adapter._adapt_twitter(content)
        assert result["platform"] == "X/Twitter"
        assert len(result["thread"]) >= 3
        assert "youtube.com" in result["deep_link_cta"]
        assert "1/" in result["thread"][0]

    @pytest.mark.asyncio
    async def test_all_platforms_adaptation(self):
        from app.services.multiverse_adapter import MultiverseAdapter
        adapter = MultiverseAdapter()
        content = {
            "title": "Test Video",
            "script": "Bu test içeriğidir.",
            "keywords": ["test"],
            "niche": "general"
        }
        result = await adapter.adapt_for_all_platforms(content)
        assert result["success"] is True
        assert result["platforms_count"] == 5
        assert "tiktok" in result["adaptations"]
        assert "instagram" in result["adaptations"]
        assert "twitter" in result["adaptations"]
        assert "facebook" in result["adaptations"]
        assert "youtube_community" in result["adaptations"]

    def test_hashtag_generation(self):
        from app.services.multiverse_adapter import MultiverseAdapter
        adapter = MultiverseAdapter()
        hashtags = adapter._generate_platform_hashtags(["yapay zeka", "AI"], "tiktok")
        assert any(h.startswith("#") for h in hashtags)
        assert "#fyp" in hashtags or "#viral" in hashtags


# ---------------------------------------------------------------------------
# GHOST AUDITOR TESTS
# ---------------------------------------------------------------------------

class TestGhostAuditor:

    def test_shadowban_signal_detection_view_drop(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        metrics = {
            "views_7d": 1000,
            "views_prev_7d": 2000,  # -50% drop = critical
            "ctr": 3.0,
            "ctr_prev": 3.0,
            "comments_7d": 50,
            "comments_prev_7d": 50,
            "search_position": 5,
            "search_position_prev": 5
        }
        signals = auditor._analyze_shadowban_signals(metrics)
        assert len(signals) >= 1
        view_signal = next(s for s in signals if s["signal"] == "view_velocity_drop")
        assert view_signal["severity"] == "critical"

    def test_no_signals_on_healthy_metrics(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        metrics = {
            "views_7d": 10000,
            "views_prev_7d": 9500,  # +5% = healthy
            "ctr": 5.0,
            "ctr_prev": 4.8,
            "comments_7d": 200,
            "comments_prev_7d": 190,
            "search_position": 3,
            "search_position_prev": 3
        }
        signals = auditor._analyze_shadowban_signals(metrics)
        assert len(signals) == 0

    def test_risk_level_critical(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        signals = [
            {"severity": "critical", "signal": "view_velocity_drop"},
            {"severity": "critical", "signal": "comment_suppression"}
        ]
        proxy = {"health": "critical", "status": "assigned"}
        fp = {"fresh": False, "status": "active"}
        risk = auditor._calculate_risk_level(signals, proxy, fp)
        assert risk == "critical"

    def test_risk_level_low(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        signals = []
        proxy = {"health": "healthy", "status": "assigned"}
        fp = {"fresh": True, "status": "active"}
        risk = auditor._calculate_risk_level(signals, proxy, fp)
        assert risk == "low"

    @pytest.mark.asyncio
    async def test_proxy_rotation(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        proxy = await auditor._rotate_proxy("test_channel_1")
        assert "host" in proxy
        assert proxy["anonymity"] == "high"
        assert proxy["failure_rate"] == 0.0
        assert "test_channel_1" in auditor.proxy_registry

    def test_fingerprint_generation(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        fp = auditor._generate_fingerprint("test_channel_2")
        assert "canvas_hash" in fp
        assert "user_agent" in fp
        assert "Mozilla/5.0" in fp["user_agent"]
        assert "test_channel_2" in auditor.fingerprint_registry

    @pytest.mark.asyncio
    async def test_full_audit_healthy_channel(self):
        from app.services.ghost_auditor import GhostAuditor
        auditor = GhostAuditor()
        metrics = {
            "views_7d": 50000, "views_prev_7d": 48000,
            "ctr": 6.5, "ctr_prev": 6.2,
            "comments_7d": 500, "comments_prev_7d": 480,
            "search_position": 2, "search_position_prev": 2
        }
        result = await auditor.start_channel_audit("healthy_channel", metrics)
        assert "risk_level" in result
        assert "signals_detected" in result
        assert result["risk_level"] in ["low", "medium", "high", "critical"]
        assert "recommendations" in result


# ---------------------------------------------------------------------------
# THUMBNAIL ANALYZER TESTS
# ---------------------------------------------------------------------------

class TestThumbnailAnalyzer:

    def test_complementary_color_180_degrees(self):
        from app.services.thumbnail_analyzer import _complementary_color, _hex_to_rgb, _rgb_to_hsv
        primary = "#3498DB"  # Blue
        comp = _complementary_color(primary)
        r, g, b = _hex_to_rgb(comp)
        h, _, _ = _rgb_to_hsv(r, g, b)
        # Should be in orange/warm hue range (~0.08 hue)
        r_p, g_p, b_p = _hex_to_rgb(primary)
        h_p, _, _ = _rgb_to_hsv(r_p, g_p, b_p)
        hue_diff = abs(h - h_p)
        # Allow for wraparound
        hue_diff = min(hue_diff, 1.0 - hue_diff)
        assert hue_diff > 0.3, f"Complementary color hue diff too small: {hue_diff}"

    def test_contrast_ratio_calculation(self):
        from app.services.thumbnail_analyzer import _contrast_ratio
        # Black on white should be ~21:1
        cr = _contrast_ratio("#FFFFFF", "#000000")
        assert cr > 15.0

        # Same color = 1:1
        cr_same = _contrast_ratio("#FF0000", "#FF0000")
        assert cr_same == pytest.approx(1.0, abs=0.01)

    def test_hex_rgb_conversion(self):
        from app.services.thumbnail_analyzer import _hex_to_rgb, _rgb_to_hex
        r, g, b = _hex_to_rgb("#FF5733")
        assert r == 255
        assert g == 87
        assert b == 51
        # Round-trip
        assert _rgb_to_hex(r, g, b) == "#FF5733"

    def test_niche_palette_db_complete(self):
        from app.services.thumbnail_analyzer import ThumbnailAnalyzer
        analyzer = ThumbnailAnalyzer()
        for niche in ["technology", "business", "education", "gaming", "entertainment"]:
            assert niche in analyzer._niche_palette_db
            assert len(analyzer._niche_palette_db[niche]) >= 2

    @pytest.mark.asyncio
    async def test_full_analysis_pipeline(self):
        from app.services.thumbnail_analyzer import ThumbnailAnalyzer
        analyzer = ThumbnailAnalyzer()
        result = await analyzer.analyze_competitor_thumbnails(
            niche="technology",
            competitor_channels=["UCtest1"],
            sample_count=10
        )
        assert "dominant_competitor_colors" in result
        assert "color_gaps" in result
        assert "winning_palette" in result
        assert "design_recommendations" in result
        assert result["visual_dominance_score"] > 0

    def test_winning_palette_has_all_keys(self):
        from app.services.thumbnail_analyzer import ThumbnailAnalyzer
        analyzer = ThumbnailAnalyzer()
        dominant = [
            {"representative_color": "#3498DB", "hue_degrees": 210, "count": 5, "frequency_pct": 50.0, "avg_saturation": 0.7, "avg_value": 0.86}
        ]
        gaps = [
            {"hue_degrees": 30, "gap_color": "#FF8C00", "opportunity_level": "high", "description": "Turuncu tonu"}
        ]
        palette = analyzer._generate_winning_palette(dominant, gaps)
        for key in ["primary", "secondary", "accent", "background", "text"]:
            assert key in palette
            assert palette[key].startswith("#")

    def test_dominance_score_range(self):
        from app.services.thumbnail_analyzer import ThumbnailAnalyzer
        analyzer = ThumbnailAnalyzer()
        palette = {
            "primary": "#FF5733",
            "secondary": "#33B4FF",
            "accent": "#C70039",
            "background": "#0D0D0D",
            "text": "#FFFFFF",
            "contrast_with_background": 12.5
        }
        dominant = [
            {"representative_color": "#3498DB", "hue_degrees": 210, "count": 3, "frequency_pct": 30.0, "avg_saturation": 0.6, "avg_value": 0.86}
        ]
        score = analyzer._calculate_dominance_score(palette, dominant)
        assert 0 <= score <= 10


# ---------------------------------------------------------------------------
# ENGAGEMENT LOOP TESTS
# ---------------------------------------------------------------------------

class TestEngagementLoop:

    @pytest.mark.asyncio
    async def test_debate_injection(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        result = await loop.inject_debate(
            video_id="test_video_123",
            niche="technology",
            persona_ids=["TechWizard_TR", "CodeNinja_TR"],
            video_duration_seconds=600
        )
        assert "thread" in result
        assert "timestamp_comments" in result
        assert len(result["thread"]) >= 2
        assert result["video_id"] == "test_video_123"

    @pytest.mark.asyncio
    async def test_debate_thread_structure(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        result = await loop.inject_debate(
            video_id="vid_001",
            niche="business",
            persona_ids=["BusinessGuru_TR", "StartupMentor_TR"],
        )
        thread = result["thread"]
        types = [c["type"] for c in thread]
        assert "opener" in types
        assert "counter" in types
        # At least one comment should be pinnable
        has_pinnable = any(c.get("is_pinnable") for c in thread)
        assert has_pinnable

    @pytest.mark.asyncio
    async def test_timestamp_comments_within_duration(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        result = await loop.inject_debate(
            video_id="vid_002",
            niche="gaming",
            persona_ids=["ProGamer_TR"],
            video_duration_seconds=300
        )
        for ts_comment in result["timestamp_comments"]:
            assert ts_comment["timestamp_seconds"] <= 300
            assert ts_comment["type"] == "timestamp"

    def test_session_time_impact_prediction(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        thread = [
            {"type": "opener", "is_pinnable": False},
            {"type": "counter", "is_pinnable": False},
            {"type": "nuance", "is_pinnable": False},
            {"type": "engagement_hook", "is_pinnable": True},
        ]
        ts_comments = [
            {"type": "timestamp"},
            {"type": "timestamp"}
        ]
        impact = loop._predict_session_time_impact(thread, ts_comments)
        assert impact["session_time_increase_pct"] > 0
        assert impact["session_time_increase_pct"] <= 45
        assert impact["prediction_confidence"] > 0

    @pytest.mark.asyncio
    async def test_boost_comments_plan(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        result = await loop.boost_top_comments(
            "vid_003",
            ["comment_1", "comment_2"]
        )
        assert result["video_id"] == "vid_003"
        assert result["boost_actions"] > 0
        assert result["status"] == "scheduled"

    def test_engagement_summary_accumulates(self):
        from app.services.engagement_loop import EngagementLoop
        loop = EngagementLoop()
        loop.debate_history = [
            {
                "video_id": "v1",
                "thread": [{"type": "opener"}, {"type": "counter"}],
                "timestamp_comments": [{"type": "timestamp"}],
                "session_impact_prediction": {"session_time_increase_pct": 15.0}
            },
            {
                "video_id": "v2",
                "thread": [{"type": "opener"}],
                "timestamp_comments": [],
                "session_impact_prediction": {"session_time_increase_pct": 8.0}
            }
        ]
        summary = loop.get_engagement_summary()
        assert summary["total_debates_injected"] == 2
        assert summary["total_comments_generated"] >= 3
        assert summary["avg_session_impact_pct"] == pytest.approx(11.5, abs=0.1)


# ---------------------------------------------------------------------------
# TRANSCRIPTION SEO TESTS
# ---------------------------------------------------------------------------

class TestTranscriptionSEO:

    def test_lsi_pool_by_niche(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        for niche in ["technology", "business", "education"]:
            pool = seo._get_lsi_pool(niche, ["test"])
            assert len(pool) >= 10

    def test_keyword_density_calculation(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        text = "yapay zeka yapay zeka yapay zeka diğer kelimeler burada"
        density = seo._calculate_keyword_density(text, ["yapay zeka"])
        assert density["yapay zeka"] > 0

    def test_stt_score_improves_with_keywords(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        lsi_pool = ["yapay zeka uygulamaları", "makine öğrenmesi"]
        score_without = seo._calculate_stt_score("Bu bir test metni", ["yapay zeka"], lsi_pool)
        score_with = seo._calculate_stt_score(
            "yapay zeka ile çalışıyoruz. yapay zeka uygulamaları oldukça faydalı. "
            "Makine öğrenmesi konusunda çok şey öğrendik. Nasıl yapılır?",
            ["yapay zeka"], lsi_pool
        )
        assert score_with > score_without

    def test_lsi_injection_returns_optimized_script(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        script = (
            "Merhaba arkadaşlar. Bugün önemli bir konuyu ele alacağız. "
            "Bu konu herkes için çok faydalı olacak. "
            "Adım adım ilerliyoruz. Detaylara bakalım. "
            "Bu bilgi ile çok şey öğrenebilirsiniz. "
        )
        result = seo.inject_lsi_keywords(script, ["yapay zeka", "AI"], "technology")
        assert "optimized_script" in result
        assert result["injection_count"] >= 1
        assert result["stt_score"] > 0
        assert len(result["timestamp_map"]) > 0

    def test_srt_timestamp_format(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        ts = seo._seconds_to_srt(90.5)
        assert ts == "00:01:30,500"
        ts2 = seo._seconds_to_srt(3661.0)
        assert ts2 == "01:01:01,000"

    def test_caption_generation(self):
        from app.services.transcription_seo import TranscriptionSEO
        seo = TranscriptionSEO()
        script = "Bu bir test metnidir. Çok yararlı bilgiler içermektedir. Yapay zeka hakkında konuşacağız."
        captions = seo.generate_stt_optimized_captions(script, ["yapay zeka"])
        assert len(captions) >= 1
        for cap in captions:
            assert "start_srt" in cap
            assert "end_srt" in cap
            assert "text" in cap
            assert cap["start_time"] < cap["end_time"]
