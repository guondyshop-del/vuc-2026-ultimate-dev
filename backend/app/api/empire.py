"""
VUC-2026 Empire API
Central nervous system endpoints for multi-agent orchestration

This API provides endpoints for managing the empire orchestrator,
agent communications, and intelligence object processing.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

from ..core.empire_orchestrator import empire_orchestrator
from ..agents.script_agent import script_agent
from ..agents.media_agent import media_agent
from ..agents.seo_agent import seo_agent
from ..agents.upload_agent import upload_agent
from ..agents.spy_agent import spy_agent
from ..agents.devops_agent import devops_agent
from ..agents.cinematic_engine import cinematic_engine
from ..services.lurker_algorithm import lurker_algorithm
from ..services.transcription_seo import transcription_seo
from ..services.engagement_loop import engagement_loop
from ..core.intelligence_objects import (
    ScriptIntelligence, MediaIntelligence, SEOIntelligence, UploadIntelligence,
    AgentType, PriorityLevel
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/status")
async def get_empire_status() -> Dict[str, Any]:
    """Get empire-wide status"""
    try:
        status = empire_orchestrator.get_empire_status()
        
        return {
            "success": True,
            "empire_status": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Empire durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/status")
async def get_all_agents_status() -> Dict[str, Any]:
    """Get status of all agents"""
    try:
        agents_status = {
            "script_agent": script_agent.get_agent_status(),
            "media_agent": media_agent.get_agent_status(),
            "seo_agent": seo_agent.get_agent_status(),
            "upload_agent": upload_agent.get_agent_status()
        }
        
        return {
            "success": True,
            "agents": agents_status,
            "total_agents": len(agents_status),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Ajan durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str) -> Dict[str, Any]:
    """Get specific agent status"""
    try:
        agents = {
            "script": script_agent,
            "media": media_agent,
            "seo": seo_agent,
            "upload": upload_agent
        }
        
        if agent_name not in agents:
            raise HTTPException(status_code=404, detail=f"Ajan bulunamadı: {agent_name}")
        
        agent_status = agents[agent_name].get_agent_status()
        
        return {
            "success": True,
            "agent_name": agent_name,
            "status": agent_status,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ajan durumu alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intelligence/process")
async def process_intelligence(intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process intelligence object through empire orchestrator"""
    try:
        # Create intelligence object based on agent type
        agent_type = intelligence_data.get("agent")
        
        if agent_type == "script_agent":
            result = await script_agent.generate_script(intelligence_data)
        elif agent_type == "media_agent":
            result = await media_agent.produce_video(intelligence_data)
        elif agent_type == "seo_agent":
            result = await seo_agent.optimize_content(intelligence_data)
        elif agent_type == "upload_agent":
            result = await upload_agent.upload_video(intelligence_data)
        else:
            raise HTTPException(status_code=400, detail=f"Bilinmeyen ajan türü: {agent_type}")
        
        # Process through empire orchestrator
        orchestration_result = await empire_orchestrator.process_intelligence(result)
        
        return {
            "success": True,
            "intelligence_id": result.id,
            "agent": agent_type,
            "orchestration": orchestration_result,
            "confidence": result.confidence.score,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"İstihbarı işleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/script/generate")
async def generate_script(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate script using script agent"""
    try:
        script_intelligence = await script_agent.generate_script(request_data)
        
        # Process through empire orchestrator
        orchestration_result = await empire_orchestrator.process_intelligence(script_intelligence)
        
        return {
            "success": True,
            "script": script_intelligence,
            "orchestration": orchestration_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Senaryo üretme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/media/produce")
async def produce_video(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Produce video using media agent"""
    try:
        media_intelligence = await media_agent.produce_video(request_data)
        
        # Process through empire orchestrator
        orchestration_result = await empire_orchestrator.process_intelligence(media_intelligence)
        
        return {
            "success": True,
            "media": media_intelligence,
            "orchestration": orchestration_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Video üretme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seo/optimize")
async def optimize_content(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize content using SEO agent"""
    try:
        seo_intelligence = await seo_agent.optimize_content(request_data)
        
        # Process through empire orchestrator
        orchestration_result = await empire_orchestrator.process_intelligence(seo_intelligence)
        
        return {
            "success": True,
            "seo": seo_intelligence,
            "orchestration": orchestration_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"SEO optimizasyonu hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/video")
async def upload_video(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Upload video using upload agent"""
    try:
        upload_intelligence = await upload_agent.upload_video(request_data)
        
        # Process through empire orchestrator
        orchestration_result = await empire_orchestrator.process_intelligence(upload_intelligence)
        
        return {
            "success": True,
            "upload": upload_intelligence,
            "orchestration": orchestration_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Video yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaign/execute")
async def execute_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute complete campaign through all agents"""
    try:
        campaign_id = f"campaign_{int(datetime.now().timestamp())}"
        campaign_results = []
        
        # Step 1: Generate script
        script_request = {
            "topic": campaign_data.get("topic", ""),
            "script_type": campaign_data.get("script_type", "educational"),
            "tone": campaign_data.get("tone", "professional"),
            "target_audience": campaign_data.get("target_audience", "general"),
            "duration_target": campaign_data.get("duration_target", 300),
            "seo_keywords": campaign_data.get("seo_keywords", []),
            "priority": PriorityLevel.HIGH
        }
        
        script_result = await script_agent.generate_script(script_request)
        script_orchestration = await empire_orchestrator.process_intelligence(script_result)
        
        campaign_results.append({
            "step": 1,
            "agent": "script_agent",
            "result": script_result,
            "orchestration": script_orchestration
        })
        
        # Step 2: Produce video (if script was successful)
        if script_orchestration.get("success", False):
            media_request = {
                "script_content": script_result.data.get("content", ""),
                "resolution": campaign_data.get("resolution", "1920x1080"),
                "fps": campaign_data.get("fps", 30),
                "codec": campaign_data.get("codec", "h264"),
                "duration_target": campaign_data.get("duration_target", 300),
                "priority": PriorityLevel.HIGH,
                "shadowban_shield": campaign_data.get("shadowban_shield", True),
                "device_type": campaign_data.get("device_type", "iphone_15_pro")
            }
            
            media_result = await media_agent.produce_video(media_request)
            media_orchestration = await empire_orchestrator.process_intelligence(media_result)
            
            campaign_results.append({
                "step": 2,
                "agent": "media_agent",
                "result": media_result,
                "orchestration": media_orchestration
            })
        else:
            campaign_results.append({
                "step": 2,
                "agent": "media_agent",
                "result": "Skipped due to script failure",
                "orchestration": script_orchestration
            })
        
        # Step 3: Optimize SEO (if media was successful)
        if (len(campaign_results) > 1 and 
            campaign_results[1]["orchestration"].get("success", False)):
            
            seo_request = {
                "content_type": "video",
                "title": campaign_data.get("title", ""),
                "description": campaign_data.get("description", ""),
                "keywords": campaign_data.get("seo_keywords", []),
                "target_audience": campaign_data.get("target_audience", "general"),
                "niche": campaign_data.get("niche", "general"),
                "priority": PriorityLevel.HIGH
            }
            
            seo_result = await seo_agent.optimize_content(seo_request)
            seo_orchestration = await empire_orchestrator.process_intelligence(seo_result)
            
            campaign_results.append({
                "step": 3,
                "agent": "seo_agent",
                "result": seo_result,
                "orchestration": seo_orchestration
            })
        else:
            campaign_results.append({
                "step": 3,
                "agent": "seo_agent",
                "result": "Skipped due to media failure",
                "orchestration": campaign_results[-1]["orchestration"]
            })
        
        # Step 4: Upload video (if SEO was successful)
        if (len(campaign_results) > 2 and 
            campaign_results[2]["orchestration"].get("success", False)):
            
            upload_request = {
                "video_file": campaign_data.get("video_file", {"size_mb": 100}),
                "metadata": {
                    "title": campaign_data.get("title", ""),
                    "description": campaign_data.get("description", ""),
                    "tags": campaign_data.get("tags", []),
                    "category": campaign_data.get("category", "Entertainment"),
                    "privacy_status": campaign_data.get("privacy_status", "public")
                },
                "priority": PriorityLevel.HIGH,
                "use_proxy": campaign_data.get("use_proxy", True),
                "schedule_time": campaign_data.get("schedule_time")
            }
            
            upload_result = await upload_agent.upload_video(upload_request)
            upload_orchestration = await empire_orchestrator.process_intelligence(upload_result)
            
            campaign_results.append({
                "step": 4,
                "agent": "upload_agent",
                "result": upload_result,
                "orchestration": upload_orchestration
            })
        else:
            campaign_results.append({
                "step": 4,
                "agent": "upload_agent",
                "result": "Skipped due to SEO failure",
                "orchestration": campaign_results[-1]["orchestration"]
            })
        
        # Calculate overall campaign success
        successful_steps = len([r for r in campaign_results if r["orchestration"].get("success", False)])
        overall_success = successful_steps == 4
        
        return {
            "success": overall_success,
            "campaign_id": campaign_id,
            "results": campaign_results,
            "successful_steps": successful_steps,
            "total_steps": 4,
            "overall_success": overall_success,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Kampanya yürütme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consultations/pending")
async def get_pending_consultations() -> Dict[str, Any]:
    """Get pending co-founder consultations"""
    try:
        empire_status = empire_orchestrator.get_empire_status()
        pending_consultations = empire_status.get("pending_consultations", [])
        
        return {
            "success": True,
            "pending_consultations": pending_consultations,
            "total_pending": len(pending_consultations),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Bekleyen danışmanlıklar alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/consultations/{consultation_id}/respond")
async def respond_to_consultation(consultation_id: str, response: Dict[str, Any]) -> Dict[str, Any]:
    """Respond to co-founder consultation"""
    try:
        # Find consultation
        empire_status = empire_orchestrator.get_empire_status()
        pending_consultations = empire_status.get("pending_consultations", [])
        
        consultation = None
        for cons in pending_consultations:
            if cons.get("consultation", {}).get("id") == consultation_id:
                consultation = cons
                break
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Danışmanlık bulunamadı")
        
        # Process response
        response_action = response.get("action", "approve")
        response_message = response.get("message", "")
        
        # Update consultation
        consultation["consultation"]["status"] = "responded"
        consultation["consultation"]["response"] = response_action
        consultation["consultation"]["response_message"] = response_message
        consultation["consultation"]["response_timestamp"] = datetime.now().isoformat()
        
        # Execute action based on response
        if response_action == "approve":
            # Execute autonomous action
            execution_result = {
                "action": "autonomous_execution_approved",
                "status": "executing",
                "message": "Co-Founder onayı ile otonom yürütme başlatıldı"
            }
        elif response_action == "modify":
            # Request revision
            execution_result = {
                "action": "revision_requested",
                "status": "revision_pending",
                "message": "Revize isteği Co-Founder tarafından onaylandı"
            }
        elif response_action == "reject":
            # Cancel execution
            execution_result = {
                "action": "execution_cancelled",
                "status": "cancelled",
                "message": "Co-Founder tarafından iptal edildi"
            }
        else:
            raise HTTPException(status_code=400, detail="Geçersiz yanıt eylemi")
        
        consultation["execution_result"] = execution_result
        
        return {
            "success": True,
            "consultation_id": consultation_id,
            "response": response_action,
            "execution_result": execution_result,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Danışmanlık yanıtlama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get empire performance metrics"""
    try:
        # Get agent performance
        agent_performance = empire_orchestrator.get_agent_performance()
        
        # Get empire metrics
        empire_status = empire_orchestrator.get_empire_status()
        empire_metrics = empire_status.get("empire_metrics", {})
        
        # Calculate overall performance
        overall_performance = {
            "total_intelligence_objects": empire_status.get("active_intelligence_objects", 0),
            "autonomous_decisions": empire_status.get("system_health", {}).get("autonomous_rate", 0),
            "human_consultations": len(empire_status.get("pending_consultations", [])),
            "success_rate": empire_metrics.get("success_rate", 0),
            "active_campaigns": empire_metrics.get("active_campaigns", 0),
            "monthly_revenue": empire_metrics.get("monthly_revenue", 0)
        }
        
        return {
            "success": True,
            "agent_performance": agent_performance,
            "empire_metrics": empire_metrics,
            "overall_performance": overall_performance,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Performans metrikleri alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/system/restart")
async def restart_system() -> Dict[str, Any]:
    """Restart empire system"""
    try:
        logger.info("Empire sistemi yeniden başlatılıyor...")
        empire_orchestrator.active_intelligence_objects.clear()
        empire_orchestrator.agent_communication_log.clear()
        empire_orchestrator.decision_history.clear()
        return {
            "success": True,
            "message": "Empire sistemi başarıyla yeniden başlatıldı",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Sistem yeniden başlatma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# SPY AGENT ENDPOINTS
# ---------------------------------------------------------------------------

@router.post("/spy/analyze")
async def analyze_competitor(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run competitor intelligence analysis"""
    try:
        result = await spy_agent.analyze_competitor(request_data)
        orchestration = await empire_orchestrator.process_intelligence(result)
        return {
            "success": True,
            "spy_intelligence": result.dict(),
            "orchestration": orchestration,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Rakip analizi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spy/status")
async def get_spy_status() -> Dict[str, Any]:
    """Get spy agent status"""
    return {"success": True, "status": spy_agent.get_agent_status()}


# ---------------------------------------------------------------------------
# DEVOPS AGENT ENDPOINTS
# ---------------------------------------------------------------------------

@router.get("/devops/health")
async def get_devops_health() -> Dict[str, Any]:
    """Get DevOps agent health report and failure blacklist"""
    try:
        return {
            "success": True,
            "health_report": devops_agent.get_health_report(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"DevOps sağlık raporu hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/devops/record-error")
async def record_error(error_data: Dict[str, Any]) -> Dict[str, Any]:
    """Manually record an error to the blacklist"""
    try:
        module = error_data.get("module", "unknown")
        error = error_data.get("error", "")
        context = error_data.get("context", {})
        devops_agent.record_error(module, error, context)
        return {
            "success": True,
            "message": f"{module} modülü için hata kaydedildi",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Hata kayıt hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/devops/blacklist/{module}")
async def clear_blacklist_entry(module: str) -> Dict[str, Any]:
    """Remove a module from the failure blacklist"""
    try:
        removed = [
            k for k in list(devops_agent.failure_blacklist.keys())
            if k.startswith(module + ":")
        ]
        for key in removed:
            del devops_agent.failure_blacklist[key]
        devops_agent._save_failure_blacklist()
        return {
            "success": True,
            "removed_entries": len(removed),
            "module": module
        }
    except Exception as e:
        logger.error(f"Blacklist temizleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# CINEMATIC ENGINE ENDPOINTS
# ---------------------------------------------------------------------------

@router.post("/cinematic/analyze")
async def analyze_script_cinematic(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze script and return cinematic production plan"""
    try:
        script = request_data.get("script", "")
        if not script:
            raise HTTPException(status_code=400, detail="Script metni gerekli")
        plan = cinematic_engine.analyze_script(script)
        return {
            "success": True,
            "cinematic_plan": plan,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sinematik analiz hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cinematic/ffmpeg-command")
async def generate_ffmpeg_command(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate FFmpeg filter_complex command from cinematic plan"""
    try:
        plan = request_data.get("cinematic_plan", {})
        input_file = request_data.get("input_file", "input.mp4")
        output_file = request_data.get("output_file", "output.mp4")
        cmd = cinematic_engine.generate_ffmpeg_filter(plan, input_file, output_file)
        return {
            "success": True,
            "ffmpeg_command": cmd,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"FFmpeg komut üretme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cinematic/status")
async def get_cinematic_status() -> Dict[str, Any]:
    """Get cinematic engine status"""
    return {"success": True, "status": cinematic_engine.get_engine_status()}


# ---------------------------------------------------------------------------
# LURKER ALGORITHM ENDPOINTS
# ---------------------------------------------------------------------------

@router.post("/lurker/run-session")
async def run_lurker_session(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run a behavioral humanization session for a persona"""
    try:
        persona_id = request_data.get("persona_id", "default_persona")
        niche = request_data.get("niche", "general")
        duration_minutes = request_data.get("duration_minutes", 15)
        result = await lurker_algorithm.run_lurker_session(persona_id, niche, duration_minutes)
        return {
            "success": True,
            "session_result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Lurker oturumu hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lurker/trust-scores")
async def get_trust_scores() -> Dict[str, Any]:
    """Get trust scores for all personas"""
    return {
        "success": True,
        "trust_scores": lurker_algorithm.get_all_trust_scores(),
        "summary": lurker_algorithm.get_session_summary()
    }


@router.get("/lurker/trust-scores/{persona_id}")
async def get_persona_trust_score(persona_id: str) -> Dict[str, Any]:
    """Get trust score for a specific persona"""
    return {
        "success": True,
        "persona_id": persona_id,
        "trust_score": lurker_algorithm.get_trust_score(persona_id)
    }


# ---------------------------------------------------------------------------
# TRANSCRIPTION SEO ENDPOINTS
# ---------------------------------------------------------------------------

@router.post("/transcription-seo/inject")
async def inject_lsi_keywords(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Inject LSI keywords into script at strategic timestamps"""
    try:
        script = request_data.get("script", "")
        keywords = request_data.get("keywords", [])
        niche = request_data.get("niche", "general")
        if not script:
            raise HTTPException(status_code=400, detail="Script metni gerekli")
        result = transcription_seo.inject_lsi_keywords(script, keywords, niche)
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LSI enjeksiyon hatas\u0131: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transcription-seo/analyze")
async def analyze_transcript_seo(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze transcript SEO and return optimization report"""
    try:
        transcript = request_data.get("transcript", "")
        keywords = request_data.get("keywords", [])
        niche = request_data.get("niche", "general")
        if not transcript:
            raise HTTPException(status_code=400, detail="Transcript metni gerekli")
        result = transcription_seo.analyze_transcript_seo(transcript, keywords, niche)
        return {
            "success": True,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcript SEO analiz hatas\u0131: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transcription-seo/captions")
async def generate_stt_captions(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate STT-optimized caption entries with timestamps"""
    try:
        script = request_data.get("script", "")
        keywords = request_data.get("keywords", [])
        timing = request_data.get("timing_seconds_per_word", 0.5)
        if not script:
            raise HTTPException(status_code=400, detail="Script metni gerekli")
        captions = transcription_seo.generate_stt_optimized_captions(script, keywords, timing)
        return {
            "success": True,
            "captions": captions,
            "total_captions": len(captions),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Caption \u00fcretme hatas\u0131: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# ENGAGEMENT LOOP ENDPOINTS
# ---------------------------------------------------------------------------

@router.post("/engagement/inject-debate")
async def inject_debate(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Inject coordinated persona debate to boost session time"""
    try:
        video_id = request_data.get("video_id", "")
        niche = request_data.get("niche", "general")
        persona_ids = request_data.get("persona_ids", ["persona_a", "persona_b"])
        duration = request_data.get("video_duration_seconds", 600)
        if not video_id:
            raise HTTPException(status_code=400, detail="video_id gerekli")
        result = await engagement_loop.inject_debate(video_id, niche, persona_ids, duration)
        return {"success": True, "debate": result, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Engagement loop hatas\u0131: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/engagement/boost-comments")
async def boost_comments(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Coordinate persona likes to push specific comments to top"""
    try:
        video_id = request_data.get("video_id", "")
        comment_ids = request_data.get("comment_ids", [])
        if not video_id or not comment_ids:
            raise HTTPException(status_code=400, detail="video_id ve comment_ids gerekli")
        result = await engagement_loop.boost_top_comments(video_id, comment_ids)
        return {"success": True, "boost": result, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comment boost hatas\u0131: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/engagement/summary")
async def get_engagement_summary() -> Dict[str, Any]:
    """Get engagement loop summary"""
    return {"success": True, "summary": engagement_loop.get_engagement_summary()}
