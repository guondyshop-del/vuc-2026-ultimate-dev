# YouTube API Integration with OAuth 2.0
import httpx
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class YouTubeOAuthService:
    """YouTube API service with OAuth 2.0 authentication"""
    
    def __init__(self):
        self.api_base_url = "https://www.googleapis.com/youtube/v3"
        self.oauth_token_url = "https://oauth2.googleapis.com/token"
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        
    async def get_authenticated_user_info(self, access_token: str) -> Dict:
        """Get authenticated YouTube user information"""
        try:
            url = f"{self.api_base_url}/channels"
            params = {
                "part": "snippet,statistics,contentDetails",
                "mine": "true"
            }
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("items"):
                        channel = data["items"][0]
                        return {
                            "success": True,
                            "channel_id": channel["id"],
                            "title": channel["snippet"]["title"],
                            "description": channel["snippet"]["description"],
                            "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
                            "video_count": int(channel["statistics"].get("videoCount", 0)),
                            "view_count": int(channel["statistics"].get("viewCount", 0)),
                            "thumbnail": channel["snippet"]["thumbnails"]["high"]["url"],
                            "created_at": channel["snippet"]["publishedAt"]
                        }
                    else:
                        return {"success": False, "error": "No channel found"}
                else:
                    logger.error(f"YouTube API error: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"API error: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_channel_videos(self, access_token: str, max_results: int = 10) -> Dict:
        """Get videos from authenticated user's channel"""
        try:
            # First get channel's uploads playlist
            channel_info = await self.get_authenticated_user_info(access_token)
            if not channel_info["success"]:
                return channel_info
            
            # Get uploads playlist ID from channel
            url = f"{self.api_base_url}/channels"
            params = {
                "part": "contentDetails",
                "mine": "true"
            }
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code != 200:
                    return {"success": False, "error": "Failed to get channel details"}
                
                data = response.json()
                if not data.get("items"):
                    return {"success": False, "error": "No channel found"}
                
                channel = data["items"][0]
                uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]
                
                # Get videos from uploads playlist
                playlist_url = f"{self.api_base_url}/playlistItems"
                playlist_params = {
                    "part": "snippet,contentDetails,status",
                    "playlistId": uploads_playlist,
                    "maxResults": max_results
                }
                
                playlist_response = await client.get(playlist_url, params=playlist_params, headers=headers)
                
                if playlist_response.status_code != 200:
                    return {"success": False, "error": "Failed to get playlist items"}
                
                playlist_data = playlist_response.json()
                videos = []
                
                for item in playlist_data.get("items", []):
                    video = {
                        "video_id": item["snippet"]["resourceId"]["videoId"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"][:200] + "..." if len(item["snippet"]["description"]) > 200 else item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"] if "high" in item["snippet"]["thumbnails"] else item["snippet"]["thumbnails"]["default"]["url"],
                        "published_at": item["snippet"]["publishedAt"],
                        "privacy_status": item["status"]["privacyStatus"]
                    }
                    videos.append(video)
                
                return {
                    "success": True,
                    "videos": videos,
                    "total_results": len(videos),
                    "channel_info": channel_info
                }
                
        except Exception as e:
            logger.error(f"Error getting channel videos: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_videos(self, access_token: str, query: str, max_results: int = 25) -> Dict:
        """Search YouTube videos using OAuth authentication"""
        try:
            url = f"{self.api_base_url}/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": "relevance"
            }
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    videos = []
                    
                    for item in data.get("items", []):
                        video = {
                            "video_id": item["id"]["videoId"],
                            "title": item["snippet"]["title"],
                            "description": item["snippet"]["description"][:200] + "..." if len(item["snippet"]["description"]) > 200 else item["snippet"]["description"],
                            "channel_title": item["snippet"]["channelTitle"],
                            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"] if "high" in item["snippet"]["thumbnails"] else item["snippet"]["thumbnails"]["default"]["url"],
                            "published_at": item["snippet"]["publishedAt"]
                        }
                        videos.append(video)
                    
                    return {
                        "success": True,
                        "videos": videos,
                        "total_results": len(videos),
                        "query": query
                    }
                else:
                    logger.error(f"Search API error: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"Search failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_video_analytics(self, access_token: str, video_id: str) -> Dict:
        """Get detailed analytics for a specific video"""
        try:
            url = f"{self.api_base_url}/videos"
            params = {
                "part": "statistics,snippet,contentDetails",
                "id": video_id
            }
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("items"):
                        video = data["items"][0]
                        return {
                            "success": True,
                            "video_id": video["id"],
                            "title": video["snippet"]["title"],
                            "statistics": {
                                "views": int(video["statistics"].get("viewCount", 0)),
                                "likes": int(video["statistics"].get("likeCount", 0)),
                                "comments": int(video["statistics"].get("commentCount", 0))
                            },
                            "duration": video["contentDetails"]["duration"],
                            "published_at": video["snippet"]["publishedAt"]
                        }
                    else:
                        return {"success": False, "error": "Video not found"}
                else:
                    return {"success": False, "error": f"Analytics failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error getting video analytics: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_trending_videos(self, access_token: str, region_code: str = "TR") -> Dict:
        """Get trending videos in a specific region"""
        try:
            url = f"{self.api_base_url}/videos"
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": 25
            }
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    videos = []
                    
                    for item in data.get("items", []):
                        video = {
                            "video_id": item["id"],
                            "title": item["snippet"]["title"],
                            "channel_title": item["snippet"]["channelTitle"],
                            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"] if "high" in item["snippet"]["thumbnails"] else item["snippet"]["thumbnails"]["default"]["url"],
                            "statistics": {
                                "views": int(item["statistics"].get("viewCount", 0)),
                                "likes": int(item["statistics"].get("likeCount", 0)),
                                "comments": int(item["statistics"].get("commentCount", 0))
                            },
                            "published_at": item["snippet"]["publishedAt"]
                        }
                        videos.append(video)
                    
                    return {
                        "success": True,
                        "videos": videos,
                        "total_results": len(videos),
                        "region_code": region_code
                    }
                else:
                    return {"success": False, "error": f"Trending videos failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error getting trending videos: {e}")
            return {"success": False, "error": str(e)}
