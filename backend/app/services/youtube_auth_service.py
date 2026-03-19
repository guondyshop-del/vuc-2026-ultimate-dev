"""
VUC-2026 YouTube OAuth 2.0 Authentication Service
Complete OAuth 2.0 flow for YouTube API operations
"""

import os
import json
import logging
import secrets
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlencode
import redis
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import base64

logger = logging.getLogger(__name__)

@dataclass
class OAuthToken:
    """OAuth token data structure"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: str
    client_id: str
    client_secret: str

@dataclass
class UserProfile:
    """YouTube user profile data"""
    channel_id: str
    channel_title: str
    email: str
    thumbnail_url: str
    subscriber_count: int

class YouTubeAuthService:
    """
    YouTube OAuth 2.0 authentication service for VUC-2026
    Handles authentication flow, token management, and user sessions
    """
    
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        # Redis for session storage
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        
        # OAuth 2.0 configuration
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtubepartner",
            "https://www.googleapis.com/auth/youtube.force-ssl"
        ]
        
        # Redirect URI
        self.redirect_uri = "http://localhost:8000/api/youtube/oauth/callback"
        
        # Session storage
        self.sessions = {}
        
        # Initialize OAuth flow
        self._initialize_oauth_flow()
    
    def _initialize_oauth_flow(self):
        """Initialize OAuth 2.0 flow configuration"""
        try:
            self.flow_config = {
                "client_config": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                },
                "scopes": self.scopes,
                "redirect_uri": self.redirect_uri
            }
            
            logger.info("OAuth 2.0 flow initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize OAuth flow: {str(e)}")
    
    def get_authorization_url(self, state: str = None) -> Dict[str, str]:
        """
        Generate OAuth authorization URL
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Dictionary containing authorization URL and state
        """
        try:
            # Generate state if not provided
            if not state:
                state = secrets.token_urlsafe(32)
            
            # Create OAuth flow
            flow = Flow.from_client_config(
                {"web": self.flow_config["client_config"]},
                scopes=self.flow_config["scopes"],
                redirect_uri=self.flow_config["redirect_uri"]
            )
            
            # Generate authorization URL
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
                prompt="consent",
                state=state
            )
            
            # Store flow in Redis temporarily
            flow_data = pickle.dumps(flow)
            self.redis_client.setex(f"oauth_flow:{state}", 600, flow_data)
            
            logger.info(f"Generated authorization URL for state: {state}")
            
            return {
                "authorization_url": authorization_url,
                "state": state,
                "expires_in": 600  # 10 minutes
            }
            
        except Exception as e:
            logger.error(f"Error generating authorization URL: {str(e)}")
            raise
    
    async def exchange_code_for_tokens(self, code: str, state: str) -> Optional[OAuthToken]:
        """
        Exchange authorization code for access tokens
        
        Args:
            code: Authorization code from Google
            state: State parameter from original request
            
        Returns:
            OAuthToken object or None if failed
        """
        try:
            # Retrieve OAuth flow from Redis
            flow_data = self.redis_client.get(f"oauth_flow:{state}")
            if not flow_data:
                logger.error(f"OAuth flow not found for state: {state}")
                return None
            
            flow = pickle.loads(flow_data)
            
            # Exchange code for tokens
            flow.fetch_token(code=code)
            
            # Create credentials object
            credentials = flow.credentials
            
            # Create OAuth token
            token = OAuthToken(
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_type="Bearer",
                expires_at=datetime.utcnow() + timedelta(seconds=credentials.expiry),
                scope=" ".join(credentials.scopes),
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Store token in Redis
            await self._store_token(token, state)
            
            # Clean up flow
            self.redis_client.delete(f"oauth_flow:{state}")
            
            logger.info(f"Successfully exchanged code for tokens, state: {state}")
            
            return token
            
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {str(e)}")
            return None
    
    async def _store_token(self, token: OAuthToken, state: str):
        """Store OAuth token in Redis"""
        try:
            token_data = {
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "token_type": token.token_type,
                "expires_at": token.expires_at.isoformat(),
                "scope": token.scope,
                "client_id": token.client_id,
                "client_secret": token.client_secret
            }
            
            # Store token with user session
            self.redis_client.setex(f"youtube_token:{state}", 3600, json.dumps(token_data))
            
            logger.info(f"Token stored for state: {state}")
            
        except Exception as e:
            logger.error(f"Error storing token: {str(e)}")
    
    async def get_credentials(self, state: str) -> Optional[Credentials]:
        """
        Get Google credentials from stored token
        
        Args:
            state: User session state
            
        Returns:
            Google Credentials object or None
        """
        try:
            # Retrieve token from Redis
            token_data = self.redis_client.get(f"youtube_token:{state}")
            if not token_data:
                logger.error(f"No token found for state: {state}")
                return None
            
            token_json = json.loads(token_data)
            
            # Check if token is expired
            expires_at = datetime.fromisoformat(token_json["expires_at"])
            if datetime.utcnow() >= expires_at:
                # Refresh token
                return await self._refresh_token(state)
            
            # Create credentials
            credentials = Credentials(
                token=token_json["access_token"],
                refresh_token=token_json["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_json["client_id"],
                client_secret=token_json["client_secret"],
                scopes=token_json["scope"].split()
            )
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error getting credentials: {str(e)}")
            return None
    
    async def _refresh_token(self, state: str) -> Optional[Credentials]:
        """Refresh expired access token"""
        try:
            # Get token data
            token_data = self.redis_client.get(f"youtube_token:{state}")
            if not token_data:
                return None
            
            token_json = json.loads(token_data)
            
            # Create credentials for refresh
            credentials = Credentials(
                token=None,
                refresh_token=token_json["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_json["client_id"],
                client_secret=token_json["client_secret"],
                scopes=token_json["scope"].split()
            )
            
            # Refresh token
            credentials.refresh(Request())
            
            # Update stored token
            updated_token = OAuthToken(
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_type="Bearer",
                expires_at=datetime.utcnow() + timedelta(seconds=credentials.expiry),
                scope=" ".join(credentials.scopes),
                client_id=token_json["client_id"],
                client_secret=token_json["client_secret"]
            )
            
            await self._store_token(updated_token, state)
            
            logger.info(f"Token refreshed for state: {state}")
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return None
    
    async def get_user_profile(self, state: str) -> Optional[UserProfile]:
        """
        Get YouTube user profile information
        
        Args:
            state: User session state
            
        Returns:
            UserProfile object or None
        """
        try:
            credentials = await self.get_credentials(state)
            if not credentials:
                return None
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Get channel information
            response = youtube.channels().list(
                part="snippet,statistics",
                mine=True
            ).execute()
            
            items = response.get("items", [])
            if not items:
                return None
            
            channel = items[0]
            snippet = channel.get("snippet", {})
            statistics = channel.get("statistics", {})
            
            profile = UserProfile(
                channel_id=channel["id"],
                channel_title=snippet.get("title", ""),
                email=snippet.get("customUrl", ""),  # YouTube custom URL if available
                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                subscriber_count=int(statistics.get("subscriberCount", 0))
            )
            
            logger.info(f"Retrieved user profile for channel: {profile.channel_title}")
            
            return profile
            
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None
    
    async def revoke_token(self, state: str) -> bool:
        """
        Revoke OAuth token
        
        Args:
            state: User session state
            
        Returns:
            True if successful, False otherwise
        """
        try:
            credentials = await self.get_credentials(state)
            if not credentials:
                return False
            
            # Revoke token
            credentials.revoke(Request())
            
            # Remove from Redis
            self.redis_client.delete(f"youtube_token:{state}")
            
            logger.info(f"Token revoked for state: {state}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error revoking token: {str(e)}")
            return False
    
    async def validate_token(self, state: str) -> bool:
        """
        Validate if token is still valid
        
        Args:
            state: User session state
            
        Returns:
            True if valid, False otherwise
        """
        try:
            credentials = await self.get_credentials(state)
            return credentials is not None and credentials.valid
            
        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            return False
    
    def get_scopes_info(self) -> Dict[str, Any]:
        """Get information about OAuth scopes"""
        return {
            "scopes": self.scopes,
            "scope_descriptions": {
                "https://www.googleapis.com/auth/youtube.readonly": "View your YouTube account",
                "https://www.googleapis.com/auth/youtube.upload": "Upload videos to your YouTube account",
                "https://www.googleapis.com/auth/youtubepartner": "Manage your YouTube account",
                "https://www.googleapis.com/auth/youtube.force-ssl": "Manage your YouTube account (secure)"
            },
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id
        }
    
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions in Redis"""
        try:
            # This would be called periodically
            # Redis handles TTL automatically, but we can add additional cleanup
            pass
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")

# Global instance
youtube_auth_service = YouTubeAuthService()
