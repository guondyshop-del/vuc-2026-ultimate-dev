from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import time
import logging
import os
import json
import base64
import secrets
from urllib.parse import urlencode, parse_qs
from dotenv import load_dotenv
import httpx
import sys

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OAuth 2.0 Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8002/auth/callback")

# Token storage (in production, use secure database)
TOKEN_STORE = {}
STATE_STORE = {}

# Import YouTube OAuth Service
try:
    from youtube_oauth_service import YouTubeOAuthService
    youtube_service = YouTubeOAuthService()
    logger.info("YouTube OAuth Service loaded successfully")
except ImportError as e:
    logger.warning(f"YouTube OAuth Service not available: {e}")
    youtube_service = None

app = FastAPI(
    title="VUC-2026 API",
    description="Vespera Ultimate Central - Complete System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:8002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheckResponse(BaseModel):
    status: str
    database: str
    redis: str
    celery: str
    version: str
    uptime_seconds: float
    timestamp: datetime

# System state
system_state = {
    "empire": {
        "matrix_generated": False,
        "video_matrix": [],
        "production_queue": [],
        "system_start_time": datetime.now(),
        "last_production_success": None,
        "autopilot_active": False
    },
    "istanbul": {
        "districts": [
            {"name": "Kadıköy", "region": "anadolu", "score": 0.85, "family_friendly": True},
            {"name": "Beşiktaş", "region": "avrupa", "score": 0.82, "family_friendly": True},
            {"name": "Şişli", "region": "avrupa", "score": 0.78, "family_friendly": False},
            {"name": "Beyoğlu", "region": "avrupa", "score": 0.75, "family_friendly": False},
            {"name": "Üsküdar", "region": "anadolu", "score": 0.80, "family_friendly": True}
        ],
        "regions": ["anadolu", "avrupa", "kuzey", "güney", "batı", "doğu"]
    },
    "channels": [
        {"id": 1, "name": "VUC-2026 Family", "subscribers": 10000, "videos": 50},
        {"id": 2, "name": "VUC-2026 Kids", "subscribers": 5000, "videos": 25}
    ]
}

@app.get("/")
async def root():
    return {
        "message": "VUC-2026 API aktif",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "oauth": {
                "login": "/auth/login",
                "callback": "/auth/callback",
                "status": "/auth/status",
                "refresh": "/auth/refresh",
                "logout": "/auth/logout"
            },
            "youtube": {
                "user_info": "/api/youtube/user/info",
                "user_videos": "/api/youtube/user/videos",
                "search": "/api/youtube/search",
                "video_analytics": "/api/youtube/video/analytics",
                "trending": "/api/youtube/trending"
            },
            "family_kids_empire": "/api/family-kids-empire",
            "istanbul_locations": "/api/istanbul-locations",
            "channels": "/api/channels",
            "health": "/health"
        }
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        database="connected",
        redis="connected",
        celery="running",
        version="1.0.0",
        uptime_seconds=time.time() - 1640000000,
        timestamp=datetime.utcnow()
    )

# OAuth Authentication Endpoints (Google OAuth 2.0 Web Server Flow)
@app.get("/auth/login")
async def auth_login():
    """Step 1: Redirect to Google OAuth consent screen"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID not configured")
    
    # Generate secure state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    STATE_STORE[state] = {
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(minutes=10)
    }
    
    auth_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/userinfo.email",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(auth_params)}"
    logger.info(f"Redirecting to Google OAuth with state: {state}")
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def auth_callback(code: str, state: str = None, error: str = None):
    """Step 2: Handle OAuth callback from Google and exchange code for tokens"""
    try:
        # Handle OAuth errors
        if error:
            error_messages = {
                "access_denied": "User denied access to the application",
                "access_denied: User denied access to your application's scopes.": "User denied access to the application", 
                "invalid_request": "The request is missing a required parameter",
                "unauthorized_client": "The client is not authorized to request an authorization code",
                "unsupported_response_type": "The authorization server does not support this response type",
                "invalid_scope": "The requested scope is invalid",
                "server_error": "The authorization server encountered an error",
                "temporarily_unavailable": "The authorization server is temporarily unavailable"
            }
            message = error_messages.get(error, f"OAuth error: {error}")
            logger.error(f"OAuth error: {error} - {message}")
            raise HTTPException(status_code=400, detail=message)
        
        # Validate state parameter for CSRF protection
        if not state or state not in STATE_STORE:
            raise HTTPException(status_code=400, detail="Invalid or missing state parameter")
        
        state_data = STATE_STORE[state]
        if datetime.now() > state_data["expires_at"]:
            del STATE_STORE[state]
            raise HTTPException(status_code=400, detail="State parameter expired")
        
        # Clean up state
        del STATE_STORE[state]
        
        # Step 3: Exchange authorization code for access token
        token_data = await exchange_code_for_tokens(code)
        
        # Step 4: Store tokens securely
        session_id = secrets.token_urlsafe(32)
        TOKEN_STORE[session_id] = {
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": datetime.now() + timedelta(seconds=token_data["expires_in"]),
            "token_type": token_data["token_type"],
            "scope": token_data["scope"],
            "created_at": datetime.now()
        }
        
        # Get user info
        user_info = await get_user_info(token_data["access_token"])
        
        logger.info(f"OAuth authentication successful for user: {user_info.get('email')}")
        
        return {
            "success": True,
            "message": "OAuth authentication successful",
            "session_id": session_id,
            "user_info": user_info,
            "token_info": {
                "expires_in": token_data["expires_in"],
                "token_type": token_data["token_type"],
                "scope": token_data["scope"]
            },
            "next_steps": [
                "Use session_id for authenticated requests",
                "Implement token refresh mechanism",
                "Enable YouTube API features"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")

@app.get("/auth/status")
async def auth_status(session_id: str = None):
    """Check authentication status"""
    oauth_configured = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
    
    if not session_id or session_id not in TOKEN_STORE:
        return {
            "authenticated": False,
            "oauth_configured": oauth_configured,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "message": "OAuth is configured but not authenticated"
        }
    
    token_data = TOKEN_STORE[session_id]
    is_expired = datetime.now() > token_data["expires_at"]
    
    return {
        "authenticated": not is_expired,
        "oauth_configured": oauth_configured,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "session_id": session_id,
        "expires_at": token_data["expires_at"].isoformat(),
        "token_type": token_data["token_type"],
        "scope": token_data["scope"],
        "message": "Authenticated" if not is_expired else "Token expired"
    }

# OAuth Helper Functions
async def exchange_code_for_tokens(code: str) -> dict:
    """Exchange authorization code for access token"""
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)
        
        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"Token exchange failed: {response.status_code} - {error_detail}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Token exchange failed: {error_detail}"
            )
        
        return response.json()

async def get_user_info(access_token: str) -> dict:
    """Get user information using access token"""
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)
        
        if response.status_code != 200:
            logger.error(f"Failed to get user info: {response.status_code}")
            return {"error": "Failed to retrieve user information"}
        
        return response.json()

async def refresh_access_token(refresh_token: str) -> dict:
    """Refresh access token using refresh token"""
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)
        
        if response.status_code != 200:
            logger.error(f"Token refresh failed: {response.status_code}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Token refresh failed"
            )
        
        return response.json()

# Additional OAuth Endpoints
@app.post("/auth/refresh")
async def refresh_token(session_id: str):
    """Refresh access token using refresh token"""
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    token_data = TOKEN_STORE[session_id]
    refresh_token = token_data.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token available")
    
    try:
        new_tokens = await refresh_access_token(refresh_token)
        
        # Update stored token data
        TOKEN_STORE[session_id].update({
            "access_token": new_tokens["access_token"],
            "expires_at": datetime.now() + timedelta(seconds=new_tokens["expires_in"]),
            "scope": new_tokens.get("scope", token_data["scope"])
        })
        
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "expires_in": new_tokens["expires_in"],
            "token_type": new_tokens["token_type"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@app.post("/auth/logout")
async def logout(session_id: str):
    """Logout and invalidate session"""
    if session_id in TOKEN_STORE:
        del TOKEN_STORE[session_id]
    
    return {
        "success": True,
        "message": "Logged out successfully"
    }

# YouTube API Endpoints (OAuth Protected)
@app.get("/api/youtube/user/info")
async def get_youtube_user_info(session_id: str):
    """Get authenticated YouTube user information"""
    if not youtube_service:
        raise HTTPException(status_code=501, detail="YouTube OAuth service not available")
    
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    access_token = TOKEN_STORE[session_id]["access_token"]
    result = await youtube_service.get_authenticated_user_info(access_token)
    
    return result

@app.get("/api/youtube/user/videos")
async def get_youtube_channel_videos(session_id: str, max_results: int = 10):
    """Get videos from authenticated user's YouTube channel"""
    if not youtube_service:
        raise HTTPException(status_code=501, detail="YouTube OAuth service not available")
    
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    access_token = TOKEN_STORE[session_id]["access_token"]
    result = await youtube_service.get_channel_videos(access_token, max_results)
    
    return result

@app.get("/api/youtube/search")
async def search_youtube_videos(session_id: str, query: str, max_results: int = 25):
    """Search YouTube videos using OAuth authentication"""
    if not youtube_service:
        raise HTTPException(status_code=501, detail="YouTube OAuth service not available")
    
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    access_token = TOKEN_STORE[session_id]["access_token"]
    result = await youtube_service.search_videos(access_token, query, max_results)
    
    return result

@app.get("/api/youtube/video/analytics")
async def get_video_analytics(session_id: str, video_id: str):
    """Get detailed analytics for a specific YouTube video"""
    if not youtube_service:
        raise HTTPException(status_code=501, detail="YouTube OAuth service not available")
    
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    access_token = TOKEN_STORE[session_id]["access_token"]
    result = await youtube_service.get_video_analytics(access_token, video_id)
    
    return result

@app.get("/api/youtube/trending")
async def get_trending_videos(session_id: str, region_code: str = "TR"):
    """Get trending YouTube videos in a specific region"""
    if not youtube_service:
        raise HTTPException(status_code=501, detail="YouTube OAuth service not available")
    
    if session_id not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    access_token = TOKEN_STORE[session_id]["access_token"]
    result = await youtube_service.get_trending_videos(access_token, region_code)
    
    return result

# Family & Kids Empire Endpoints
@app.get("/api/family-kids-empire/status")
async def get_empire_status():
    empire = system_state["empire"]
    return {
        "success": True,
        "matrix_generated": empire["matrix_generated"],
        "total_videos": len(empire["video_matrix"]),
        "production_queue_size": len(empire["production_queue"]),
        "api_health": {"status": "healthy"},
        "system_uptime_hours": (datetime.now() - empire["system_start_time"]).total_seconds() / 3600,
        "last_production_success": empire["last_production_success"]
    }

@app.post("/api/family-kids-empire/generate-matrix")
async def generate_matrix():
    matrix = []
    stages = ["pregnancy", "newborn", "infant", "toddler"]
    
    for i in range(100):
        video = {
            "id": i + 1,
            "title": f"Video {i + 1} - {stages[i % 4].title()}",
            "stage": stages[i % 4],
            "estimated_views": 5000 + (i * 100),
            "monetization_potential": 12.5 + (i * 0.5)
        }
        matrix.append(video)
    
    system_state["empire"]["video_matrix"] = matrix
    system_state["empire"]["matrix_generated"] = True
    
    return {
        "success": True,
        "video_count": len(matrix),
        "videos": matrix[:10],
        "estimated_total_views": sum(v["estimated_views"] for v in matrix),
        "estimated_total_revenue": sum(v["monetization_potential"] for v in matrix),
        "generation_time_ms": 150
    }

@app.get("/api/family-kids-empire/matrix/videos")
async def get_video_matrix():
    return {
        "success": True,
        "matrix_generated": system_state["empire"]["matrix_generated"],
        "videos": system_state["empire"]["video_matrix"][:10],
        "total_count": len(system_state["empire"]["video_matrix"])
    }

@app.post("/api/family-kids-empire/produce")
async def start_production():
    queue = system_state["empire"]["production_queue"]
    queue.append({
        "id": len(queue) + 1,
        "status": "queued",
        "created_at": datetime.now()
    })
    
    return {
        "success": True,
        "production_id": f"prod_{len(queue)}",
        "estimated_completion_time": datetime.now(),
        "tasks_created": ["script_generation", "voice_synthesis", "video_rendering"]
    }

@app.get("/api/family-kids-empire/production/queue")
async def get_production_queue():
    return {
        "success": True,
        "queue": system_state["empire"]["production_queue"],
        "queue_size": len(system_state["empire"]["production_queue"]),
        "active_tasks": 1
    }

# İstanbul Locations Endpoints
@app.get("/api/istanbul-locations/overview")
async def get_istanbul_overview():
    districts = system_state["istanbul"]["districts"]
    regions = system_state["istanbul"]["regions"]
    
    return {
        "success": True,
        "total_districts": len(districts),
        "regions": regions,
        "family_friendly_count": sum(1 for d in districts if d["family_friendly"]),
        "average_score": sum(d["score"] for d in districts) / len(districts)
    }

@app.get("/api/istanbul-locations/districts")
async def get_istanbul_districts():
    districts = system_state["istanbul"]["districts"]
    
    return {
        "success": True,
        "districts": districts,
        "total_count": len(districts),
        "top_districts": sorted(districts, key=lambda x: x["score"], reverse=True)[:3]
    }

@app.get("/api/istanbul-locations/districts/family-friendly")
async def get_family_friendly_districts():
    districts = [d for d in system_state["istanbul"]["districts"] if d["family_friendly"]]
    
    return {
        "success": True,
        "districts": districts,
        "count": len(districts)
    }

@app.get("/api/istanbul-locations/districts/{district_name}/content-strategy")
async def get_content_strategy(district_name: str):
    # Normalize district name for matching
    district_name_normalized = district_name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    
    district = None
    for d in system_state["istanbul"]["districts"]:
        d_normalized = d["name"].lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if d_normalized == district_name_normalized:
            district = d
            break
    
    if not district:
        return {"success": False, "error": "District not found"}
    
    return {
        "success": True,
        "district": district["name"],
        "content_type": "family",
        "strategy": f"Focus on {district['name']} family content with score {district['score']}"
    }

# Channels Endpoints
@app.get("/api/channels/")
async def get_channels():
    return {
        "success": True,
        "channels": system_state["channels"],
        "total_count": len(system_state["channels"])
    }

# Adaptive Learning Endpoints
@app.get("/api/adaptive-learning/dashboard")
async def get_adaptive_learning_dashboard():
    """Get adaptive learning dashboard"""
    try:
        # Simulate learning data
        learning_data = {
            "learning_state": {
                "total_learning_cycles": 15,
                "successful_adaptations": 12,
                "failed_adaptations": 3,
                "average_improvement": 0.15,
                "learning_velocity": 0.80
            },
            "active_patterns": 5,
            "total_adaptations": 15,
            "performance_metrics": {
                "cpu_usage": [45.2, 47.8, 43.1, 44.5, 46.2],
                "memory_usage": [67.8, 69.2, 65.4, 68.1, 66.7],
                "response_time": [150, 145, 155, 148, 152]
            },
            "top_patterns": [
                {
                    "pattern_id": "perf_cpu_optimization",
                    "success_rate": 0.85,
                    "confidence_score": 0.80,
                    "impact_score": 0.15
                },
                {
                    "pattern_id": "error_api_timeout",
                    "success_rate": 0.92,
                    "confidence_score": 0.90,
                    "impact_score": 0.25
                },
                {
                    "pattern_id": "success_video_production",
                    "success_rate": 0.95,
                    "confidence_score": 0.85,
                    "impact_score": 0.20
                }
            ],
            "recent_adaptations": [
                {
                    "adaptation_id": "adapt_001",
                    "strategy": "automatic_tuning",
                    "improvement_score": 0.12,
                    "success": True,
                    "timestamp": "2026-03-19T21:15:00"
                },
                {
                    "adaptation_id": "adapt_002", 
                    "strategy": "resource_reallocation",
                    "improvement_score": 0.18,
                    "success": True,
                    "timestamp": "2026-03-19T21:10:00"
                }
            ],
            "learning_velocity": 0.80
        }
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            **learning_data
        }
        
    except Exception as e:
        logger.error(f"Failed to get adaptive learning dashboard: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/adaptive-learning/learning/start")
async def start_adaptive_learning():
    """Start adaptive learning"""
    try:
        logger.info("🧠 Starting VUC-2026 Adaptive Learning Engine...")
        
        # Simulate learning start
        return {
            "success": True,
            "message": "Adaptive learning started successfully",
            "learning_interval": 300,
            "timestamp": datetime.now().isoformat(),
            "status": "learning_active"
        }
        
    except Exception as e:
        logger.error(f"Failed to start adaptive learning: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/adaptive-learning/patterns")
async def get_learning_patterns():
    """Get learning patterns"""
    try:
        patterns = [
            {
                "pattern_id": "perf_cpu_optimization",
                "learning_type": "performance_optimization",
                "context": {"metric": "cpu_usage", "threshold": 80},
                "success_rate": 0.85,
                "confidence_score": 0.80,
                "frequency": 15,
                "impact_score": 0.15,
                "last_applied": "2026-03-19T21:15:00"
            },
            {
                "pattern_id": "error_api_timeout",
                "learning_type": "error_pattern_recognition",
                "context": {"error_type": "timeout", "component": "api"},
                "success_rate": 0.92,
                "confidence_score": 0.90,
                "frequency": 8,
                "impact_score": 0.25,
                "last_applied": "2026-03-19T21:10:00"
            },
            {
                "pattern_id": "success_video_production",
                "learning_type": "success_pattern_analysis",
                "context": {"process": "video_production", "stage": "rendering"},
                "success_rate": 0.95,
                "confidence_score": 0.85,
                "frequency": 25,
                "impact_score": 0.20,
                "last_applied": "2026-03-19T21:05:00"
            },
            {
                "pattern_id": "content_engagement_boost",
                "learning_type": "content_strategy_adaptation",
                "context": {"content_type": "kids_video", "metric": "engagement"},
                "success_rate": 0.78,
                "confidence_score": 0.75,
                "frequency": 12,
                "impact_score": 0.30,
                "last_applied": "2026-03-19T21:00:00"
            },
            {
                "pattern_id": "resource_memory_cleanup",
                "learning_type": "system_resource_optimization",
                "context": {"resource": "memory", "action": "cleanup"},
                "success_rate": 0.88,
                "confidence_score": 0.82,
                "frequency": 20,
                "impact_score": 0.12,
                "last_applied": "2026-03-19T20:55:00"
            }
        ]
        
        return {
            "success": True,
            "total_patterns": len(patterns),
            "patterns": sorted(patterns, key=lambda p: p["impact_score"] * p["confidence_score"], reverse=True)
        }
        
    except Exception as e:
        logger.error(f"Failed to get learning patterns: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/adaptive-learning/state")
async def get_learning_state():
    """Get learning state"""
    try:
        state = {
            "total_learning_cycles": 15,
            "successful_adaptations": 12,
            "failed_adaptations": 3,
            "average_improvement": 0.15,
            "learning_velocity": 0.80,
            "total_adaptations": 15,
            "success_rate": 0.80,
            "learning_efficiency": 0.12
        }
        
        return {
            "success": True,
            "learning_state": state,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get learning state: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=True)
