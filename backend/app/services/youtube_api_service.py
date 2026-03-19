"""
VUC-2026 YouTube API Service
Complete YouTube Data API v3 integration with advanced features
"""

import os
import asyncio
import json
import logging
import aiohttp
import requests
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote_plus
import hashlib
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import io
from dotenv import load_dotenv

# Load environment variables from root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../2048'))
load_dotenv(os.path.join(project_root, '.env'))

logger = logging.getLogger(__name__)

@dataclass
class YouTubeVideo:
    """YouTube video data structure"""
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    published_at: datetime
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    tags: List[str]
    category_id: str
    thumbnail_url: str
    embed_url: str

@dataclass
class YouTubeChannel:
    """YouTube channel data structure"""
    channel_id: str
    title: str
    description: str
    subscriber_count: int
    video_count: int
    view_count: int
    thumbnail_url: str
    country: str
    published_at: datetime

@dataclass
class YouTubePlaylist:
    """YouTube playlist data structure"""
    playlist_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    video_count: int
    thumbnail_url: str
    published_at: datetime

class YouTubeAPIService:
    """
    Complete YouTube Data API v3 service for VUC-2026
    """
    
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        # API endpoints
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.upload_url = "https://www.googleapis.com/upload/youtube/v3"
        
        # OAuth 2.0 flow
        self.oauth_flow = None
        self.credentials = None
        
        # Rate limiting
        self.quota_usage = 0
        self.daily_quota_limit = 10000
        self.last_reset = datetime.now().date()
        
        # Caching
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Initialize YouTube client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize YouTube API client"""
        try:
            if self.api_key:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube API client initialized with API key")
            else:
                logger.warning("No YouTube API key found")
                
        except Exception as e:
            logger.error(f"Failed to initialize YouTube client: {str(e)}")
    
    async def search_videos(self, 
                          query: str, 
                          max_results: int = 25,
                          order: str = "relevance",
                          duration: str = None,
                          published_after: datetime = None,
                          published_before: datetime = None) -> List[YouTubeVideo]:
        """
        Search for videos with advanced filters
        
        Args:
            query: Search query
            max_results: Maximum number of results (1-50)
            order: Order by (relevance, date, rating, viewCount, title)
            duration: Filter by duration (short, medium, long)
            published_after: Filter by publish date
            published_before: Filter by publish date
        """
        try:
            # Build search parameters
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": min(max_results, 50),
                "order": order,
                "key": self.api_key
            }
            
            # Add optional filters
            if duration:
                params["videoDuration"] = duration
            
            if published_after:
                params["publishedAfter"] = published_after.isoformat() + "Z"
            
            if published_before:
                params["publishedBefore"] = published_before.isoformat() + "Z"
            
            # Make request
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/search", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get detailed video information
                        video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
                        videos = await self.get_video_details(video_ids)
                        
                        return videos
                    else:
                        logger.error(f"Search failed: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error searching videos: {str(e)}")
            return []
    
    async def get_video_details(self, video_ids: List[str]) -> List[YouTubeVideo]:
        """Get detailed information for videos"""
        try:
            params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(video_ids),
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/videos", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        videos = []
                        for item in data.get("items", []):
                            video = self._parse_video_data(item)
                            if video:
                                videos.append(video)
                        
                        return videos
                    else:
                        logger.error(f"Failed to get video details: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting video details: {str(e)}")
            return []
    
    def _parse_video_data(self, item: Dict[str, Any]) -> Optional[YouTubeVideo]:
        """Parse YouTube video data from API response"""
        try:
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            content_details = item.get("contentDetails", {})
            
            return YouTubeVideo(
                video_id=item["id"],
                title=snippet.get("title", ""),
                description=snippet.get("description", ""),
                channel_id=snippet.get("channelId", ""),
                channel_title=snippet.get("channelTitle", ""),
                published_at=datetime.fromisoformat(snippet.get("publishedAt", "").replace("Z", "+00:00")),
                duration=content_details.get("duration", ""),
                view_count=int(statistics.get("viewCount", 0)),
                like_count=int(statistics.get("likeCount", 0)),
                comment_count=int(statistics.get("commentCount", 0)),
                tags=snippet.get("tags", []),
                category_id=snippet.get("categoryId", ""),
                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                embed_url=f"https://www.youtube.com/embed/{item['id']}"
            )
            
        except Exception as e:
            logger.error(f"Error parsing video data: {str(e)}")
            return None
    
    async def get_channel_details(self, channel_id: str) -> Optional[YouTubeChannel]:
        """Get detailed channel information"""
        try:
            params = {
                "part": "snippet,statistics",
                "id": channel_id,
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/channels", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        items = data.get("items", [])
                        if items:
                            return self._parse_channel_data(items[0])
                        
                    return None
                        
        except Exception as e:
            logger.error(f"Error getting channel details: {str(e)}")
            return None
    
    def _parse_channel_data(self, item: Dict[str, Any]) -> Optional[YouTubeChannel]:
        """Parse YouTube channel data from API response"""
        try:
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            
            return YouTubeChannel(
                channel_id=item["id"],
                title=snippet.get("title", ""),
                description=snippet.get("description", ""),
                subscriber_count=int(statistics.get("subscriberCount", 0)),
                video_count=int(statistics.get("videoCount", 0)),
                view_count=int(statistics.get("viewCount", 0)),
                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                country=snippet.get("country", ""),
                published_at=datetime.fromisoformat(snippet.get("publishedAt", "").replace("Z", "+00:00"))
            )
            
        except Exception as e:
            logger.error(f"Error parsing channel data: {str(e)}")
            return None
    
    async def get_playlist_details(self, playlist_id: str) -> Optional[YouTubePlaylist]:
        """Get detailed playlist information"""
        try:
            params = {
                "part": "snippet,contentDetails",
                "id": playlist_id,
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/playlists", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        items = data.get("items", [])
                        if items:
                            return self._parse_playlist_data(items[0])
                        
                    return None
                        
        except Exception as e:
            logger.error(f"Error getting playlist details: {str(e)}")
            return None
    
    def _parse_playlist_data(self, item: Dict[str, Any]) -> Optional[YouTubePlaylist]:
        """Parse YouTube playlist data from API response"""
        try:
            snippet = item.get("snippet", {})
            content_details = item.get("contentDetails", {})
            
            return YouTubePlaylist(
                playlist_id=item["id"],
                title=snippet.get("title", ""),
                description=snippet.get("description", ""),
                channel_id=snippet.get("channelId", ""),
                channel_title=snippet.get("channelTitle", ""),
                video_count=int(content_details.get("itemCount", 0)),
                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                published_at=datetime.fromisoformat(snippet.get("publishedAt", "").replace("Z", "+00:00"))
            )
            
        except Exception as e:
            logger.error(f"Error parsing playlist data: {str(e)}")
            return None
    
    async def get_trending_videos(self, region_code: str = "US", category_id: str = None) -> List[YouTubeVideo]:
        """Get trending videos for a specific region"""
        try:
            params = {
                "part": "snippet,statistics,contentDetails",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": 50,
                "key": self.api_key
            }
            
            if category_id:
                params["videoCategoryId"] = category_id
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/videos", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        videos = []
                        for item in data.get("items", []):
                            video = self._parse_video_data(item)
                            if video:
                                videos.append(video)
                        
                        return videos
                    else:
                        logger.error(f"Failed to get trending videos: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting trending videos: {str(e)}")
            return []
    
    async def get_video_categories(self, region_code: str = "US") -> List[Dict[str, Any]]:
        """Get available video categories for a region"""
        try:
            params = {
                "part": "snippet",
                "regionCode": region_code,
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/videoCategories", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("items", [])
                    else:
                        logger.error(f"Failed to get video categories: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting video categories: {str(e)}")
            return []
    
    async def get_channel_videos(self, channel_id: str, max_results: int = 25) -> List[YouTubeVideo]:
        """Get videos from a specific channel"""
        try:
            params = {
                "part": "snippet",
                "channelId": channel_id,
                "type": "video",
                "maxResults": min(max_results, 50),
                "order": "date",
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/search", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get detailed video information
                        video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
                        videos = await self.get_video_details(video_ids)
                        
                        return videos
                    else:
                        logger.error(f"Failed to get channel videos: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting channel videos: {str(e)}")
            return []
    
    async def get_playlist_videos(self, playlist_id: str, max_results: int = 25) -> List[YouTubeVideo]:
        """Get videos from a specific playlist"""
        try:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": min(max_results, 50),
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/playlistItems", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get video IDs
                        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in data.get("items", [])]
                        videos = await self.get_video_details(video_ids)
                        
                        return videos
                    else:
                        logger.error(f"Failed to get playlist videos: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting playlist videos: {str(e)}")
            return []
    
    def _check_quota(self) -> bool:
        """Check if API quota is available"""
        today = datetime.now().date()
        
        # Reset quota usage daily
        if today != self.last_reset:
            self.quota_usage = 0
            self.last_reset = today
        
        return self.quota_usage < self.daily_quota_limit
    
    def _update_quota(self, cost: int):
        """Update quota usage"""
        self.quota_usage += cost
        logger.info(f"Quota usage: {self.quota_usage}/{self.daily_quota_limit}")
    
    async def get_api_health(self) -> Dict[str, Any]:
        """Check YouTube API health and quota status"""
        try:
            # Test API with a simple request
            params = {
                "part": "snippet",
                "q": "test",
                "type": "video",
                "maxResults": 1,
                "key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/search", params=params) as response:
                    return {
                        "api_status": "healthy" if response.status == 200 else "unhealthy",
                        "status_code": response.status,
                        "quota_used": self.quota_usage,
                        "quota_limit": self.daily_quota_limit,
                        "quota_remaining": self.daily_quota_limit - self.quota_usage,
                        "last_reset": self.last_reset.isoformat()
                    }
                    
        except Exception as e:
            return {
                "api_status": "error",
                "error": str(e),
                "quota_used": self.quota_usage,
                "quota_limit": self.daily_quota_limit
            }

# Global instance
youtube_service = YouTubeAPIService()
