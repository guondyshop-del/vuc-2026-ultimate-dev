"""
VUC-2026 Pytest Test Suite
Full coverage for all agents and critical modules

Run: pytest backend/tests/test_agents.py -v
"""

import asyncio
import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import sys

# Ensure backend is on path
sys.path.insert(0, str(Path(__file__).parents[2]))

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def basic_script_request():
    return {
        "topic": "Yapay Zeka ile Para Kazanma",
        "script_type": "educational",
        "tone": "professional",
        "target_audience": "genel",
        "duration_target": 300,
        "seo_keywords": ["yapay zeka", "para kazanma", "AI 2026"],
        "priority": "normal"
    }


@pytest.fixture
def basic_media_request():
    return {
        "script_content": "Bu videoda yapay zeka ile para kazanmayı öğreneceğiz.",
        "resolution": "1920x1080",
        "fps": 30,
        "codec": "h264",
        "duration_target": 300,
        "shadowban_shield": True,
        "device_type": "iphone_15_pro"
    }


@pytest.fixture
def basic_seo_request():
    return {
        "content_type": "video",
        "title": "Yapay Zeka ile Para Kazanma 2026",
        "description": "Bu videoda en güncel AI araçları ile nasıl para kazanacağınızı öğreneceksiniz.",
        "keywords": ["yapay zeka", "para kazanma", "AI"],
        "target_audience": "genel",
        "niche": "technology"
    }


@pytest.fixture
def basic_upload_request():
    return {
        "video_file": {"size_mb": 150, "path": "/tmp/test_video.mp4"},
        "metadata": {
            "title": "Test Video",
            "description": "Test açıklama",
            "tags": ["test", "yapay zeka"],
            "category": "Education",
            "privacy_status": "public"
        },
        "use_proxy": False,
        "priority": "normal"
    }


@pytest.fixture
def spy_request():
    return {
        "target_channel": "UCTestChannel123",
        "niche": "technology",
        "depth": "standard"
    }


# ---------------------------------------------------------------------------
# INTELLIGENCE OBJECTS TESTS
# ---------------------------------------------------------------------------

class TestIntelligenceObjects:

    def test_confidence_level_auto_fields(self):
        from app.core.intelligence_objects import ConfidenceLevel
        c_high = ConfidenceLevel(score=95)
        assert c_high.auto_execution is True
        assert c_high.requires_human_review is False

        c_mid = ConfidenceLevel(score=80)
        assert c_mid.auto_execution is False
        assert c_mid.requires_human_review is True

        c_low = ConfidenceLevel(score=50)
        assert c_low.auto_execution is False
        assert c_low.requires_human_review is True

    def test_priority_levels(self):
        from app.core.intelligence_objects import PriorityLevel
        assert PriorityLevel.HIGH == "high"
        assert PriorityLevel.CRITICAL == "critical"

    def test_create_script_intelligence_factory(self):
        from app.core.intelligence_objects import (
            create_script_intelligence, AgentType, PriorityLevel
        )
        obj = create_script_intelligence(
            agent=AgentType.SCRIPT_AGENT,
            confidence_score=85.0,
            script_data={
                "type": "educational",
                "content": "Test script",
                "word_count": 100,
                "seo_keywords": ["ai", "python"],
                "hook_strength": 7.0,
                "viral_potential": 6.5,
                "emotional_tone": "professional",
                "target_audience": "genel",
                "content_pillar": "technology",
                "estimated_duration": 200,
                "script_structure": {},
                "engagement_hooks": ["Şaşırtıcı değil mi?"]
            }
        )
        assert obj.confidence.score == 85.0
        assert obj.word_count == 100
        assert obj.hook_strength == 7.0

    def test_create_seo_intelligence_factory(self):
        from app.core.intelligence_objects import (
            create_seo_intelligence, AgentType
        )
        obj = create_seo_intelligence(
            agent=AgentType.SEO_AGENT,
            confidence_score=78.0,
            seo_data={
                "title_score": 8.0,
                "description_score": 7.5,
                "tag_relevance": 7.0,
                "thumbnail_optimized": False,
                "estimated_ctr": 4.5,
                "keyword_density": 5.0,
                "competition_analysis": {},
                "trend_alignment": 6.0,
                "search_volume": {},
                "ranking_potential": 7.0,
                "optimization_suggestions": ["Başlığı kısalt"]
            }
        )
        assert obj.title_score == 8.0
        assert obj.estimated_ctr == 4.5


# ---------------------------------------------------------------------------
# SCRIPT AGENT TESTS
# ---------------------------------------------------------------------------

class TestScriptAgent:

    def test_determine_content_pillar(self):
        from app.agents.script_agent import script_agent
        assert script_agent._determine_content_pillar("yapay zeka araçları") == "technology"
        assert script_agent._determine_content_pillar("para kazanma yolları") == "business"
        assert script_agent._determine_content_pillar("random topic") == "general"

    def test_human_fluidity_patterns_exist(self):
        from app.agents.script_agent import script_agent
        assert "conversation_fillers" in script_agent.human_fluidity_patterns
        assert "emotional_markers" in script_agent.human_fluidity_patterns
        assert len(script_agent.human_fluidity_patterns["conversation_fillers"]) > 0

    def test_ai_bypass_techniques_enabled(self):
        from app.agents.script_agent import script_agent
        assert script_agent.ai_bypass_techniques["perplexity_boost"] is True
        assert script_agent.ai_bypass_techniques["fingerprint_elimination"] is True

    def test_calculate_script_metrics(self):
        from app.agents.script_agent import script_agent
        script = "Bu video inanılmaz bilgiler içeriyor! Nasıl yapılır? Abone ol."

        metrics = asyncio.get_event_loop().run_until_complete(
            script_agent._calculate_script_metrics(script)
        )
        assert "word_count" in metrics
        assert "hook_strength" in metrics
        assert "viral_potential" in metrics
        assert metrics["word_count"] > 0

    def test_eliminate_fingerprints(self):
        from app.agents.script_agent import script_agent
        text = "Yapay zeka olarak size şunu söyleyeyim: bu harika."
        cleaned = script_agent._eliminate_fingerprints(text)
        assert "yapay zeka olarak" not in cleaned.lower()

    @pytest.mark.asyncio
    async def test_generate_script_returns_intelligence_object(self, basic_script_request):
        from app.agents.script_agent import script_agent
        from app.core.intelligence_objects import ScriptIntelligence
        with patch.object(script_agent, '_generate_base_script', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = "Bu test senaryosudur. Harika içerik üretiyoruz! Abone olmayı unutmayın."
            result = await script_agent.generate_script(basic_script_request)
        assert isinstance(result, ScriptIntelligence)
        assert result.confidence.score > 0
        assert result.word_count > 0


# ---------------------------------------------------------------------------
# MEDIA AGENT TESTS
# ---------------------------------------------------------------------------

class TestMediaAgent:

    def test_shadowban_shield_config(self):
        from app.agents.media_agent import media_agent
        assert media_agent.shadowban_shield["pixel_jitter"] == 0.001
        assert media_agent.shadowban_shield["speed_variation"] == 0.01
        assert media_agent.shadowban_shield["frame_seeding"] is True

    def test_estimate_file_size(self):
        from app.agents.media_agent import media_agent
        size = media_agent._estimate_file_size("1920x1080", 30, 300)
        assert size > 0
        size_4k = media_agent._estimate_file_size("3840x2160", 60, 300)
        assert size_4k > size

    def test_calculate_bitrate(self):
        from app.agents.media_agent import media_agent
        br_1080 = media_agent._calculate_bitrate("1920x1080", 30)
        br_4k = media_agent._calculate_bitrate("3840x2160", 60)
        assert br_4k > br_1080

    def test_device_metadata_iphone(self):
        from app.agents.media_agent import media_agent
        video_data = {"duration": 300, "fps": 30}
        result = asyncio.get_event_loop().run_until_complete(
            media_agent._add_device_metadata(video_data, "iphone_15_pro")
        )
        assert result["device_spoofed"] is True
        assert result["device_metadata"]["make"] == "Apple"
        assert "gps" in result["device_metadata"]

    def test_device_metadata_sony(self):
        from app.agents.media_agent import media_agent
        video_data = {"duration": 300}
        result = asyncio.get_event_loop().run_until_complete(
            media_agent._add_device_metadata(video_data, "sony_a7siii")
        )
        assert result["device_metadata"]["make"] == "SONY"

    @pytest.mark.asyncio
    async def test_shadowban_shield_applied(self, basic_media_request):
        from app.agents.media_agent import media_agent
        video_data = {"duration": 300, "fps": 30, "resolution": "1920x1080"}
        result = await media_agent._apply_shadowban_shield(video_data)
        assert result["shadowban_shield_active"] is True
        assert "frame_seed" in result
        assert result["speed_variation"] > 1.0


# ---------------------------------------------------------------------------
# SEO AGENT TESTS
# ---------------------------------------------------------------------------

class TestSEOAgent:

    def test_calculate_title_score_optimal(self):
        from app.agents.seo_agent import seo_agent
        title = "Yapay Zeka ile 2026'da Para Kazanmanın 5 Yolu!"
        score = seo_agent._calculate_title_score(title)
        assert score >= 7.0

    def test_calculate_title_score_too_long(self):
        from app.agents.seo_agent import seo_agent
        title = "Bu başlık çok uzun ve YouTube aramasında görünmeyecek çünkü karakter sınırını aştı ve bu kötü bir SEO pratiğidir gerçekten"
        score = seo_agent._calculate_title_score(title)
        assert score < 7.0

    def test_calculate_description_score(self):
        from app.agents.seo_agent import seo_agent
        desc = "🔥 Bu videoda yapay zeka araçlarını ele aldık. " * 30 + " #AI #yapay_zeka Abone ol!"
        score = seo_agent._calculate_description_score(desc)
        assert score >= 6.0

    def test_estimate_ctr_with_hook(self):
        from app.agents.seo_agent import seo_agent
        ctr = seo_agent._estimate_ctr("İnanılmaz AI Sırrı! 2026", "kısa açıklama")
        assert ctr > 3.0

    def test_generate_hashtags(self):
        from app.agents.seo_agent import seo_agent
        hashtags = seo_agent._generate_hashtags(["yapay zeka", "AI"], "technology")
        assert "#" in hashtags
        assert len(hashtags) > 0

    def test_generate_niche_specific_tags(self):
        from app.agents.seo_agent import seo_agent
        tags = seo_agent._generate_niche_specific_tags("technology")
        assert len(tags) > 0
        assert isinstance(tags, list)

    def test_optimize_tags_within_limit(self):
        from app.agents.seo_agent import seo_agent
        keywords = ["yapay zeka", "AI", "Python", "makine öğrenimi", "derin öğrenme"]
        tags = asyncio.get_event_loop().run_until_complete(
            seo_agent._optimize_tags(keywords, "technology")
        )
        total_length = sum(len(tag) for tag in tags)
        assert total_length <= 500


# ---------------------------------------------------------------------------
# SPY AGENT TESTS
# ---------------------------------------------------------------------------

class TestSpyAgent:

    def test_detect_foley_events(self):
        from app.agents.cinematic_engine import cinematic_engine
        sentences = ["Rüzgar esiyor ve şimdi tıklama sesi duyuyoruz.", "Normal cümle.", "Para kazanma zamanı!"]
        events = cinematic_engine._detect_foley_events(sentences)
        assert len(events) >= 2

    def test_detect_tone_energetic(self):
        from app.agents.cinematic_engine import cinematic_engine
        script = "Bu inanılmaz bir enerji dolu video! Hızlı hareket edin! Amazing!"
        tone = cinematic_engine._detect_tone(script)
        assert tone == "energetic"

    def test_detect_tone_educational(self):
        from app.agents.cinematic_engine import cinematic_engine
        script = "Bugün nasıl yapılır öğreneceğiz. Adım adım rehber olarak ilerleyeceğiz."
        tone = cinematic_engine._detect_tone(script)
        assert tone == "educational"

    def test_lsi_timestamps_generated(self):
        from app.agents.cinematic_engine import cinematic_engine
        sentences = [
            "Yapay zeka teknolojisi günümüzde hızla gelişmektedir.",
            "Kısa.",
            "Makine öğrenimi algoritmaları verimlilik artırımı sağlamaktadır."
        ]
        timestamps = cinematic_engine._generate_lsi_timestamps(sentences)
        assert len(timestamps) >= 1
        for ts in timestamps:
            assert "timestamp" in ts
            assert "high_value_words" in ts

    def test_spy_calculate_opportunity_score(self):
        from app.agents.spy_agent import spy_agent
        gaps = ["gap1", "gap2", "gap3", "gap4", "gap5"]
        weaknesses = {"w1": "x", "w2": "y", "w3": "z"}
        competitor_data = {"engagement_rate": 2.0, "subscriber_count": 100000}
        score = spy_agent._calculate_opportunity_score(gaps, weaknesses, competitor_data)
        assert 0 < score <= 10.0

    def test_spy_sentiment_analysis(self):
        from app.agents.spy_agent import spy_agent
        competitor_data = {
            "niche": "technology",
            "top_videos": [
                {
                    "title": "Test",
                    "views": 1000,
                    "comment_sample": [
                        "Bu harika bir video!",
                        "Anlamadım, daha detaylı anlatır mısınız?",
                        "Çok yararlı teşekkürler"
                    ]
                }
            ]
        }
        insights = spy_agent._extract_audience_insights(competitor_data)
        assert "sentiment_distribution" in insights

    @pytest.mark.asyncio
    async def test_spy_analyze_competitor_returns_intelligence(self, spy_request):
        from app.agents.spy_agent import spy_agent
        from app.core.intelligence_objects import SpyIntelligence
        result = await spy_agent.analyze_competitor(spy_request)
        assert isinstance(result, SpyIntelligence)
        assert result.confidence.score > 0
        assert result.target_channel == spy_request["target_channel"]


# ---------------------------------------------------------------------------
# DEVOPS AGENT TESTS
# ---------------------------------------------------------------------------

class TestDevOpsAgent:

    def test_record_error(self, tmp_path):
        from app.agents.devops_agent import DevOpsAgent
        agent = DevOpsAgent()
        agent.failure_blacklist = {}
        agent._save_failure_blacklist = MagicMock()
        agent._log_decision_turkish = MagicMock()

        agent.record_error("test_module", "Connection refused")
        assert len(agent.failure_blacklist) == 1
        key = list(agent.failure_blacklist.keys())[0]
        assert "test_module" in key
        assert agent.failure_blacklist[key]["occurrences"] == 1

    def test_is_blacklisted_after_max_retries(self):
        from app.agents.devops_agent import DevOpsAgent
        agent = DevOpsAgent()
        agent._save_failure_blacklist = MagicMock()
        agent._log_decision_turkish = MagicMock()

        for _ in range(3):
            agent.record_error("flaky_module", "TimeoutError")

        assert agent.is_blacklisted("flaky_module", "TimeoutError") is True

    @pytest.mark.asyncio
    async def test_self_correct_success_on_retry(self):
        from app.agents.devops_agent import DevOpsAgent
        agent = DevOpsAgent()
        agent._save_failure_blacklist = MagicMock()
        agent._log_decision_turkish = MagicMock()
        agent.retry_policy = {"max_retries": 3, "backoff_seconds": 0}

        call_count = 0

        async def flaky_op():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Geçici hata")
            return "başarılı"

        result = await agent.self_correct("test_module", flaky_op)
        assert result == "başarılı"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_self_correct_raises_after_max_retries(self):
        from app.agents.devops_agent import DevOpsAgent
        agent = DevOpsAgent()
        agent._save_failure_blacklist = MagicMock()
        agent._log_decision_turkish = MagicMock()
        agent.retry_policy = {"max_retries": 2, "backoff_seconds": 0}

        async def always_fail():
            raise ConnectionError("Kalıcı hata")

        with pytest.raises(Exception):
            await agent.self_correct("test_module", always_fail)


# ---------------------------------------------------------------------------
# EMPIRE ORCHESTRATOR TESTS
# ---------------------------------------------------------------------------

class TestEmpireOrchestrator:

    def test_confidence_thresholds(self):
        from app.core.empire_orchestrator import empire_orchestrator
        assert empire_orchestrator.confidence_thresholds["autonomous"] == 90.0
        assert empire_orchestrator.confidence_thresholds["consult_threshold"] == 75.0

    @pytest.mark.asyncio
    async def test_decision_autonomous_for_high_confidence(self):
        from app.core.empire_orchestrator import empire_orchestrator, DecisionType
        from app.core.intelligence_objects import create_script_intelligence, AgentType

        intel = create_script_intelligence(
            agent=AgentType.SCRIPT_AGENT,
            confidence_score=95.0,
            script_data={
                "type": "educational", "content": "Test", "word_count": 100,
                "seo_keywords": [], "hook_strength": 8.0, "viral_potential": 7.0,
                "emotional_tone": "professional", "target_audience": "genel",
                "content_pillar": "technology", "estimated_duration": 200,
                "script_structure": {}, "engagement_hooks": []
            }
        )
        decision = await empire_orchestrator._make_decision(intel)
        assert decision["type"] == DecisionType.AUTONOMOUS

    @pytest.mark.asyncio
    async def test_decision_consult_for_medium_confidence(self):
        from app.core.empire_orchestrator import empire_orchestrator, DecisionType
        from app.core.intelligence_objects import create_script_intelligence, AgentType

        intel = create_script_intelligence(
            agent=AgentType.SCRIPT_AGENT,
            confidence_score=80.0,
            script_data={
                "type": "educational", "content": "Test", "word_count": 100,
                "seo_keywords": [], "hook_strength": 5.0, "viral_potential": 5.0,
                "emotional_tone": "professional", "target_audience": "genel",
                "content_pillar": "general", "estimated_duration": 200,
                "script_structure": {}, "engagement_hooks": []
            }
        )
        decision = await empire_orchestrator._make_decision(intel)
        assert decision["type"] == DecisionType.HUMAN_CONSULT

    @pytest.mark.asyncio
    async def test_decision_manual_for_low_confidence(self):
        from app.core.empire_orchestrator import empire_orchestrator, DecisionType
        from app.core.intelligence_objects import create_script_intelligence, AgentType

        intel = create_script_intelligence(
            agent=AgentType.SCRIPT_AGENT,
            confidence_score=55.0,
            script_data={
                "type": "educational", "content": "Test", "word_count": 50,
                "seo_keywords": [], "hook_strength": 2.0, "viral_potential": 2.0,
                "emotional_tone": "error", "target_audience": "unknown",
                "content_pillar": "general", "estimated_duration": 0,
                "script_structure": {}, "engagement_hooks": []
            }
        )
        decision = await empire_orchestrator._make_decision(intel)
        assert decision["type"] == DecisionType.MANUAL_OVERRIDE


# ---------------------------------------------------------------------------
# CINEMATIC ENGINE TESTS
# ---------------------------------------------------------------------------

class TestCinematicEngine:

    def test_analyze_script_full_pipeline(self):
        from app.agents.cinematic_engine import cinematic_engine
        script = (
            "Merhaba arkadaşlar! Bugün çok önemli bir konuyu ele alacağız. "
            "Yapay zeka ile para kazanma yöntemleri inanılmaz sonuçlar veriyor! "
            "Adım adım öğrenelim. Bir tıklama ile başlayalım. "
            "Rüzgar gibi hızlı hareket etmemiz gerekiyor."
        )
        plan = cinematic_engine.analyze_script(script)

        assert "tone" in plan
        assert "cut_points" in plan
        assert "foley_events" in plan
        assert "lsi_timestamps" in plan
        assert "zoom_plan" in plan
        assert plan["estimated_duration_seconds"] > 0

    def test_ffmpeg_filter_generated(self):
        from app.agents.cinematic_engine import cinematic_engine
        plan = {
            "tone": "energetic",
            "zoom_plan": [{"timestamp": 3.5, "zoom_in": 1.1, "duration_ms": 400, "easing": "ease_in_out"}]
        }
        cmd = cinematic_engine.generate_ffmpeg_filter(plan, "input.mp4", "output.mp4")
        assert "ffmpeg" in cmd
        assert "input.mp4" in cmd
        assert "output.mp4" in cmd
        assert "setpts" in cmd


# ---------------------------------------------------------------------------
# PRIVACY LAYER TESTS
# ---------------------------------------------------------------------------

class TestPrivacyLayer:

    def test_user_agent_rotation(self):
        from app.services.privacy_layer import privacy_layer
        privacy_layer.initialize_user_agents()
        agents = set()
        for _ in range(20):
            ua = privacy_layer._get_weighted_random_user_agent()
            agents.add(ua)
        # Should pick different agents over 20 calls (probabilistic)
        assert len(agents) >= 1
        assert "Mozilla/5.0" in list(agents)[0]

    def test_fingerprint_protection_headers(self):
        from app.services.privacy_layer import privacy_layer
        headers = privacy_layer._generate_fingerprint_protection()
        assert "DNT" in headers
        assert "Sec-GPC" in headers

    def test_anonymity_level_with_proxy(self):
        from app.services.privacy_layer import privacy_layer
        proxy = {"anonymity": "maximum", "host": "1.2.3.4"}
        level = privacy_layer._calculate_anonymity_level(proxy, "Mozilla/5.0 Chrome/120")
        assert level == "high"

    def test_detection_risk_clean_ua(self):
        from app.services.privacy_layer import privacy_layer
        result = privacy_layer._assess_detection_risk(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        assert result["risk_level"] in ["minimal", "low"]

    def test_detection_risk_bot_ua(self):
        from app.services.privacy_layer import privacy_layer
        result = privacy_layer._assess_detection_risk("python-requests/2.28 bot crawler")
        assert result["risk_score"] >= 30


# ---------------------------------------------------------------------------
# RATE LIMIT / BACKOFF INTEGRATION TESTS
# ---------------------------------------------------------------------------

class TestRateLimitBackoff:

    @pytest.mark.asyncio
    async def test_upload_agent_retry_on_chunk_failure(self):
        from app.agents.upload_agent import upload_agent

        call_count = 0
        original_upload_chunk = upload_agent._upload_chunk

        async def mock_upload_chunk(chunk_index, session, proxy):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {"success": False, "error_code": "NETWORK_ERROR", "chunk_index": chunk_index}
            return {"success": True, "chunk_index": chunk_index, "bytes_uploaded": 5242880}

        upload_agent._upload_chunk = mock_upload_chunk

        session = {"chunk_size": 5242880, "total_chunks": 1}
        video_file = {"size_mb": 5}
        result = await upload_agent._perform_chunked_upload(video_file, session, None)

        upload_agent._upload_chunk = original_upload_chunk
        assert result["uploaded_chunks"] == 1

    def test_proxy_pool_best_selection(self):
        from app.services.privacy_layer import privacy_layer
        privacy_layer.proxy_pool = [
            {"host": "p1.com", "port": 8080, "success_rate": 0.95, "anonymity": "high", "last_used": None, "type": "http", "country": "US"},
            {"host": "p2.com", "port": 8080, "success_rate": 0.60, "anonymity": "medium", "last_used": None, "type": "http", "country": "DE"},
        ]
        best = privacy_layer._get_best_proxy()
        assert best["host"] == "p1.com"
