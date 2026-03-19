"""
VUC-2026 YouTube Comments Auto-Reply API
AI-driven community management endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.community_management_service import CommunityManagementService, CommenterPersona, ResponseTone
from app.core.ai_intelligence import AIIntelligence

router = APIRouter(prefix="/api/yt/comments", tags=["comments"])
community_service = CommunityManagementService()
ai_intelligence = AIIntelligence()

class CommentAnalysisRequest(BaseModel):
    comment_text: str
    video_context: Optional[Dict] = None

class CommentAnalysisResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str
    timestamp: datetime

class AutoReplyRequest(BaseModel):
    video_id: str
    max_comments: int = 50
    auto_reply: bool = True
    affiliate_enabled: bool = True

class AutoReplyResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str
    timestamp: datetime

class TemplateUpdateRequest(BaseModel):
    tone: str
    category: str
    templates: List[str]

@router.post("/analyze", response_model=CommentAnalysisResponse)
async def analyze_comment(request: CommentAnalysisRequest):
    """
    Analyze comment and determine persona/response strategy
    """
    try:
        analysis = await community_service.analyze_comment(
            comment_text=request.comment_text,
            video_context=request.video_context
        )
        
        return CommentAnalysisResponse(
            success=True,
            data={
                "analysis": {
                    "persona": analysis.persona.value,
                    "sentiment": analysis.sentiment,
                    "urgency": analysis.urgency,
                    "keywords": analysis.keywords,
                    "response_tone": analysis.response_tone.value,
                    "confidence_score": analysis.confidence_score
                }
            },
            message="Comment analysis completed",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comment analysis failed: {str(e)}"
        )

@router.post("/generate-response", response_model=CommentAnalysisResponse)
async def generate_response(
    comment_text: str,
    video_context: Optional[Dict] = None,
    affiliate_enabled: bool = True
):
    """
    Generate AI-powered response for comment
    """
    try:
        # Analyze comment first
        analysis = await community_service.analyze_comment(comment_text, video_context)
        
        # Generate response
        response = await community_service.generate_response(
            comment_analysis=analysis,
            video_context=video_context,
            affiliate_enabled=affiliate_enabled
        )
        
        return CommentAnalysisResponse(
            success=True,
            data=response,
            message="Response generated successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Response generation failed: {str(e)}"
        )

@router.post("/auto-reply", response_model=AutoReplyResponse)
async def auto_reply_comments(
    background_tasks: BackgroundTasks,
    request: AutoReplyRequest
):
    """
    Process and auto-reply to new comments
    """
    try:
        # Process comments
        result = await community_service.process_new_comments(
            video_id=request.video_id,
            max_comments=request.max_comments,
            auto_reply=request.auto_reply
        )
        
        return AutoReplyResponse(
            success=True,
            data=result,
            message=f"Processed {result['comments_processed']} comments, posted {result['auto_replies_posted']} replies",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Auto-reply processing failed: {str(e)}"
        )

@router.post("/batch-auto-reply", response_model=AutoReplyResponse)
async def batch_auto_reply_comments(
    background_tasks: BackgroundTasks,
    video_requests: List[AutoReplyRequest]
):
    """
    Batch process comments for multiple videos
    """
    try:
        results = []
        
        for request in video_requests:
            try:
                result = await community_service.process_new_comments(
                    video_id=request.video_id,
                    max_comments=request.max_comments,
                    auto_reply=request.auto_reply
                )
                results.append({
                    "video_id": request.video_id,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "video_id": request.video_id,
                    "success": False,
                    "error": str(e)
                })
        
        successful_count = sum(1 for r in results if r["success"])
        total_comments = sum(r["result"]["comments_processed"] for r in results if r["success"])
        total_replies = sum(r["result"]["auto_replies_posted"] for r in results if r["success"])
        
        return AutoReplyResponse(
            success=True,
            data={
                "total_videos": len(video_requests),
                "successful": successful_count,
                "failed": len(video_requests) - successful_count,
                "total_comments_processed": total_comments,
                "total_auto_replies_posted": total_replies,
                "results": results
            },
            message=f"Batch processing completed: {successful_count}/{len(video_requests)} videos successful",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch auto-reply failed: {str(e)}"
        )

@router.get("/analytics", response_model=CommentAnalysisResponse)
async def get_community_analytics(
    video_id: Optional[str] = None,
    time_range: str = "7_days"
):
    """
    Get community management analytics
    """
    try:
        analytics = await community_service.get_community_analytics(
            video_id=video_id,
            time_range=time_range
        )
        
        return CommentAnalysisResponse(
            success=True,
            data=analytics,
            message="Community analytics retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analytics retrieval failed: {str(e)}"
        )

@router.get("/engagement/{video_id}", response_model=CommentAnalysisResponse)
async def get_engagement_metrics(video_id: str):
    """
    Get engagement metrics for specific video
    """
    try:
        metrics = await community_service.get_engagement_metrics(video_id)
        
        return CommentAnalysisResponse(
            success=True,
            data=metrics,
            message="Engagement metrics retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Engagement metrics retrieval failed: {str(e)}"
        )

@router.get("/personas", response_model=CommentAnalysisResponse)
async def get_commenter_personas():
    """
    Get available commenter personas
    """
    try:
        personas = [
            {
                "value": persona.value,
                "label": persona.value.replace("_", " ").title(),
                "description": f"Comments from {persona.value.replace('_', ' ')}"
            }
            for persona in CommenterPersona
        ]
        
        return CommentAnalysisResponse(
            success=True,
            data={"personas": personas},
            message="Commenter personas retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Personas retrieval failed: {str(e)}"
        )

@router.get("/response-tones", response_model=CommentAnalysisResponse)
async def get_response_tones():
    """
    Get available response tones
    """
    try:
        tones = [
            {
                "value": tone.value,
                "label": tone.value.replace("_", " ").title(),
                "description": f"Response tone for {tone.value.replace('_', ' ')} comments"
            }
            for tone in ResponseTone
        ]
        
        return CommentAnalysisResponse(
            success=True,
            data={"response_tones": tones},
            message="Response tones retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Response tones retrieval failed: {str(e)}"
        )

@router.get("/templates", response_model=CommentAnalysisResponse)
async def get_response_templates():
    """
    Get current response templates
    """
    try:
        templates = community_service.response_templates
        
        return CommentAnalysisResponse(
            success=True,
            data={"templates": templates},
            message="Response templates retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Templates retrieval failed: {str(e)}"
        )

@router.put("/templates", response_model=CommentAnalysisResponse)
async def update_response_templates(request: TemplateUpdateRequest):
    """
    Update response templates
    """
    try:
        # Convert string to enum
        tone_enum = ResponseTone(request.tone)
        
        result = await community_service.update_response_templates(
            tone=tone_enum,
            category=request.category,
            templates=request.templates
        )
        
        return CommentAnalysisResponse(
            success=True,
            data=result,
            message="Response templates updated successfully",
            timestamp=datetime.now()
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tone or category: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Template update failed: {str(e)}"
        )

@router.get("/affiliate-products", response_model=CommentAnalysisResponse)
async def get_affiliate_products():
    """
    Get available affiliate products
    """
    try:
        products = community_service.affiliate_products
        
        return CommentAnalysisResponse(
            success=True,
            data={"affiliate_products": products},
            message="Affiliate products retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Affiliate products retrieval failed: {str(e)}"
        )

@router.post("/schedule-auto-reply", response_model=AutoReplyResponse)
async def schedule_auto_reply(
    background_tasks: BackgroundTasks,
    video_id: str,
    schedule_interval: int = 15,  # minutes
    max_comments_per_run: int = 50
):
    """
    Schedule periodic auto-reply processing
    """
    try:
        # Add background task for periodic processing
        background_tasks.add_task(
            community_service.process_new_comments,
            video_id=video_id,
            max_comments=max_comments_per_run,
            auto_reply=True
        )
        
        return AutoReplyResponse(
            success=True,
            data={
                "video_id": video_id,
                "schedule_interval": schedule_interval,
                "max_comments_per_run": max_comments_per_run,
                "scheduled_at": datetime.now().isoformat()
            },
            message="Auto-reply processing scheduled successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Auto-reply scheduling failed: {str(e)}"
        )

@router.get("/settings", response_model=CommentAnalysisResponse)
async def get_community_settings():
    """
    Get community management settings
    """
    try:
        settings = {
            "persona_keywords": community_service.persona_keywords,
            "response_templates": community_service.response_templates,
            "affiliate_products": community_service.affiliate_products
        }
        
        return CommentAnalysisResponse(
            success=True,
            data=settings,
            message="Community settings retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Settings retrieval failed: {str(e)}"
        )
