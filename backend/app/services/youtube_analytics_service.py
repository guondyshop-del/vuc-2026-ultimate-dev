"""
VUC-2026 YouTube Analytics Service
Complete YouTube Analytics API integration for advanced metrics
"""

import os
import asyncio
import json
import logging
import aiohttp
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import numpy as np
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .youtube_auth_service import youtube_auth_service

logger = logging.getLogger(__name__)

@dataclass
class VideoAnalytics:
    """Video analytics data structure"""
    video_id: str
    title: str
    views: int
    likes: int
    dislikes: int
    comments: int
    shares: int
    watch_time_minutes: float
    average_view_duration: float
    audience_retention: float
    click_through_rate: float
    impressions: int
    unique_viewers: int
    revenue: float
    published_at: datetime

@dataclass
class ChannelAnalytics:
    """Channel analytics data structure"""
    channel_id: str
    channel_title: str
    total_views: int
    total_subscribers: int
    total_videos: int
    watch_time_hours: float
    average_view_duration: float
    subscriber_growth: int
    revenue_total: float
    top_videos: List[str]
    demographics: Dict[str, Any]

@dataclass
class AnalyticsMetric:
    """Analytics metric data structure"""
    name: str
    value: Union[int, float, str]
    change_percent: float
    trend: str  # up, down, stable
    date: datetime

class YouTubeAnalyticsService:
    """
    Complete YouTube Analytics service for VUC-2026
    Handles channel analytics, video performance, and insights
    """
    
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/analytics/v1"
        self.reports_url = "https://www.googleapis.com/youtube/reporting/v1"
        
        # Analytics cache
        self.analytics_cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Initialize service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize analytics service"""
        try:
            logger.info("YouTube Analytics Service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize analytics service: {str(e)}")
    
    async def get_channel_analytics(self, 
                                  channel_id: str,
                                  start_date: datetime,
                                  end_date: datetime,
                                  state: str = None) -> Optional[ChannelAnalytics]:
        """
        Get comprehensive channel analytics
        
        Args:
            channel_id: YouTube channel ID
            start_date: Start date for analytics
            end_date: End date for analytics
            state: OAuth session state
            
        Returns:
            ChannelAnalytics object or None
        """
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            # Build YouTube Analytics service
            analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Get channel basic info
            channel_response = youtube.channels().list(
                part="snippet,statistics",
                id=channel_id
            ).execute()
            
            channel_info = channel_response.get("items", [{}])[0]
            snippet = channel_info.get("snippet", {})
            statistics = channel_info.get("statistics", {})
            
            # Get channel analytics
            analytics_response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",
                dimensions="day"
            ).execute()
            
            # Process analytics data
            rows = analytics_response.get("rows", [])
            total_views = sum(row[1] for row in rows) if rows else 0
            total_watch_time = sum(row[2] for row in rows) if rows else 0
            avg_duration = np.mean([row[3] for row in rows]) if rows else 0
            subs_gained = sum(row[4] for row in rows) if rows else 0
            subs_lost = sum(row[5] for row in rows) if rows else 0
            
            # Get top videos
            top_videos_response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views",
                dimensions="video",
                sort="-views",
                maxResults=10
            ).execute()
            
            top_video_ids = [row[0] for row in top_videos_response.get("rows", [])]
            
            # Get demographics data
            demographics = await self._get_demographics(channel_id, start_date, end_date, analytics)
            
            channel_analytics = ChannelAnalytics(
                channel_id=channel_id,
                channel_title=snippet.get("title", ""),
                total_views=total_views,
                total_subscribers=int(statistics.get("subscriberCount", 0)),
                total_videos=int(statistics.get("videoCount", 0)),
                watch_time_hours=total_watch_time / 60,
                average_view_duration=avg_duration,
                subscriber_growth=subs_gained - subs_lost,
                revenue_total=0.0,  # Would need YouTube Partner Program access
                top_videos=top_video_ids,
                demographics=demographics
            )
            
            logger.info(f"Retrieved channel analytics for: {channel_analytics.channel_title}")
            
            return channel_analytics
            
        except Exception as e:
            logger.error(f"Error getting channel analytics: {str(e)}")
            return None
    
    async def get_video_analytics(self, 
                                 video_ids: List[str],
                                 start_date: datetime,
                                 end_date: datetime,
                                 state: str = None) -> List[VideoAnalytics]:
        """
        Get analytics for specific videos
        
        Args:
            video_ids: List of video IDs
            start_date: Start date for analytics
            end_date: End date for analytics
            state: OAuth session state
            
        Returns:
            List of VideoAnalytics objects
        """
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
            youtube = build('youtube', 'v3', credentials=credentials)
            
            video_analytics_list = []
            
            for video_id in video_ids:
                try:
                    # Get video basic info
                    video_response = youtube.videos().list(
                        part="snippet,statistics",
                        id=video_id
                    ).execute()
                    
                    video_info = video_response.get("items", [{}])[0]
                    snippet = video_info.get("snippet", {})
                    statistics = video_info.get("statistics", {})
                    
                    # Get video analytics
                    analytics_response = analytics.reports().query(
                        ids=f"video=={video_id}",
                        startDate=start_date.strftime("%Y-%m-%d"),
                        endDate=end_date.strftime("%Y-%m-%d"),
                        metrics="views,likes,dislikes,comments,shares,estimatedMinutesWatched,averageViewDuration,audienceRetentionRate,clickThroughRate,impressions,uniqueViewers",
                        dimensions="day"
                    ).execute()
                    
                    # Aggregate analytics data
                    rows = analytics_response.get("rows", [])
                    
                    if rows:
                        views = sum(row[1] for row in rows)
                        likes = sum(row[2] for row in rows)
                        dislikes = sum(row[3] for row in rows)
                        comments = sum(row[4] for row in rows)
                        shares = sum(row[5] for row in rows)
                        watch_time = sum(row[6] for row in rows)
                        avg_duration = np.mean([row[7] for row in rows])
                        retention = np.mean([row[8] for row in rows]) if any(row[8] for row in rows) else 0
                        ctr = np.mean([row[9] for row in rows]) if any(row[9] for row in rows) else 0
                        impressions = sum(row[10] for row in rows)
                        unique_viewers = sum(row[11] for row in rows)
                    else:
                        # Fallback to basic statistics
                        views = int(statistics.get("viewCount", 0))
                        likes = int(statistics.get("likeCount", 0))
                        dislikes = 0  # Not available in v3
                        comments = int(statistics.get("commentCount", 0))
                        shares = 0
                        watch_time = 0
                        avg_duration = 0
                        retention = 0
                        ctr = 0
                        impressions = 0
                        unique_viewers = 0
                    
                    video_analytics = VideoAnalytics(
                        video_id=video_id,
                        title=snippet.get("title", ""),
                        views=views,
                        likes=likes,
                        dislikes=dislikes,
                        comments=comments,
                        shares=shares,
                        watch_time_minutes=watch_time,
                        average_view_duration=avg_duration,
                        audience_retention=retention,
                        click_through_rate=ctr,
                        impressions=impressions,
                        unique_viewers=unique_viewers,
                        revenue=0.0,  # Would need YouTube Partner Program access
                        published_at=datetime.fromisoformat(snippet.get("publishedAt", "").replace("Z", "+00:00"))
                    )
                    
                    video_analytics_list.append(video_analytics)
                    
                except Exception as e:
                    logger.error(f"Error getting analytics for video {video_id}: {str(e)}")
                    continue
            
            logger.info(f"Retrieved analytics for {len(video_analytics_list)} videos")
            
            return video_analytics_list
            
        except Exception as e:
            logger.error(f"Error getting video analytics: {str(e)}")
            return []
    
    async def _get_demographics(self, 
                               channel_id: str,
                               start_date: datetime,
                               end_date: datetime,
                               analytics) -> Dict[str, Any]:
        """Get audience demographics data"""
        try:
            # Get age group demographics
            age_response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views",
                dimensions="ageGroup"
            ).execute()
            
            # Get gender demographics
            gender_response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views",
                dimensions="gender"
            ).execute()
            
            # Get device demographics
            device_response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views",
                dimensions="deviceType"
            ).execute()
            
            demographics = {
                "age_groups": {},
                "genders": {},
                "devices": {}
            }
            
            # Process age groups
            for row in age_response.get("rows", []):
                age_group, views = row
                demographics["age_groups"][age_group] = views
            
            # Process genders
            for row in gender_response.get("rows", []):
                gender, views = row
                demographics["genders"][gender] = views
            
            # Process devices
            for row in device_response.get("rows", []):
                device, views = row
                demographics["devices"][device] = views
            
            return demographics
            
        except Exception as e:
            logger.error(f"Error getting demographics: {str(e)}")
            return {}
    
    async def get_real_time_metrics(self, channel_id: str, state: str = None) -> Dict[str, Any]:
        """Get real-time channel metrics"""
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Get current channel statistics
            response = youtube.channels().list(
                part="snippet,statistics",
                id=channel_id
            ).execute()
            
            items = response.get("items", [])
            if not items:
                return {}
            
            channel = items[0]
            statistics = channel.get("statistics", {})
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "views": int(statistics.get("viewCount", 0)),
                "subscribers": int(statistics.get("subscriberCount", 0)),
                "videos": int(statistics.get("videoCount", 0)),
                "comments": int(statistics.get("commentCount", 0))
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting real-time metrics: {str(e)}")
            return {}
    
    async def get_top_performing_videos(self, 
                                       channel_id: str,
                                       days: int = 30,
                                       metric: str = "views",
                                       state: str = None) -> List[Dict[str, Any]]:
        """Get top performing videos by metric"""
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
            
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics=metric,
                dimensions="video",
                sort=f"-{metric}",
                maxResults=50
            ).execute()
            
            top_videos = []
            for row in response.get("rows", []):
                video_id, metric_value = row
                top_videos.append({
                    "video_id": video_id,
                    "metric": metric,
                    "value": metric_value
                })
            
            return top_videos
            
        except Exception as e:
            logger.error(f"Error getting top performing videos: {str(e)}")
            return []
    
    async def get_engagement_metrics(self, 
                                   video_ids: List[str],
                                   state: str = None) -> Dict[str, Dict[str, float]]:
        """Calculate engagement metrics for videos"""
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            youtube = build('youtube', 'v3', credentials=credentials)
            
            engagement_data = {}
            
            # Get video statistics in batches
            for i in range(0, len(video_ids), 50):  # API limit is 50 videos
                batch_ids = video_ids[i:i+50]
                
                response = youtube.videos().list(
                    part="statistics",
                    id=",".join(batch_ids)
                ).execute()
                
                for item in response.get("items", []):
                    video_id = item["id"]
                    stats = item.get("statistics", {})
                    
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    comments = int(stats.get("commentCount", 0))
                    
                    # Calculate engagement rates
                    engagement_rate = 0
                    if views > 0:
                        engagement_rate = ((likes + comments) / views) * 100
                    
                    like_rate = 0
                    if views > 0:
                        like_rate = (likes / views) * 100
                    
                    comment_rate = 0
                    if views > 0:
                        comment_rate = (comments / views) * 100
                    
                    engagement_data[video_id] = {
                        "engagement_rate": engagement_rate,
                        "like_rate": like_rate,
                        "comment_rate": comment_rate,
                        "views": views,
                        "likes": likes,
                        "comments": comments
                    }
            
            return engagement_data
            
        except Exception as e:
            logger.error(f"Error calculating engagement metrics: {str(e)}")
            return {}
    
    async def get_growth_trends(self, 
                               channel_id: str,
                               days: int = 30,
                               state: str = None) -> Dict[str, List[AnalyticsMetric]]:
        """Get growth trends over time"""
        try:
            credentials = await youtube_auth_service.get_credentials(state)
            if not credentials:
                raise ValueError("Invalid OAuth credentials")
            
            analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
            
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get daily metrics
            response = analytics.reports().query(
                ids=f"channel=={channel_id}",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,subscribersGained,subscribersLost",
                dimensions="day"
            ).execute()
            
            trends = {
                "views": [],
                "subscribers": []
            }
            
            previous_views = 0
            previous_subs = 0
            
            for row in response.get("rows", []):
                date_str, views, subs_gained, subs_lost = row
                current_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Views trend
                views_change = 0
                views_trend = "stable"
                if previous_views > 0:
                    views_change = ((views - previous_views) / previous_views) * 100
                    if views_change > 5:
                        views_trend = "up"
                    elif views_change < -5:
                        views_trend = "down"
                
                trends["views"].append(AnalyticsMetric(
                    name="views",
                    value=views,
                    change_percent=views_change,
                    trend=views_trend,
                    date=current_date
                ))
                
                # Subscribers trend
                net_subs = subs_gained - subs_lost
                subs_change = 0
                subs_trend = "stable"
                if previous_subs > 0:
                    subs_change = ((net_subs - previous_subs) / abs(previous_subs)) * 100
                    if subs_change > 5:
                        subs_trend = "up"
                    elif subs_change < -5:
                        subs_trend = "down"
                
                trends["subscribers"].append(AnalyticsMetric(
                    name="subscribers",
                    value=net_subs,
                    change_percent=subs_change,
                    trend=subs_trend,
                    date=current_date
                ))
                
                previous_views = views
                previous_subs = net_subs
            
            return trends
            
        except Exception as e:
            logger.error(f"Error getting growth trends: {str(e)}")
            return {}
    
    async def export_analytics_report(self, 
                                    channel_id: str,
                                    start_date: datetime,
                                    end_date: datetime,
                                    format: str = "csv",
                                    state: str = None) -> Optional[str]:
        """Export analytics report to file"""
        try:
            # Get comprehensive analytics
            channel_analytics = await self.get_channel_analytics(
                channel_id, start_date, end_date, state
            )
            
            if not channel_analytics:
                return None
            
            # Create report data
            report_data = {
                "channel_title": channel_analytics.channel_title,
                "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                "total_views": channel_analytics.total_views,
                "total_subscribers": channel_analytics.total_subscribers,
                "total_videos": channel_analytics.total_videos,
                "watch_time_hours": channel_analytics.watch_time_hours,
                "average_view_duration": channel_analytics.average_view_duration,
                "subscriber_growth": channel_analytics.subscriber_growth,
                "demographics": channel_analytics.demographics
            }
            
            # Export to requested format
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            
            if format == "json":
                filename = f"analytics_report_{timestamp}.json"
                filepath = f"reports/{filename}"
                
                os.makedirs("reports", exist_ok=True)
                with open(filepath, 'w') as f:
                    json.dump(report_data, f, indent=2, default=str)
            
            elif format == "csv":
                filename = f"analytics_report_{timestamp}.csv"
                filepath = f"reports/{filename}"
                
                os.makedirs("reports", exist_ok=True)
                
                # Flatten data for CSV
                flattened_data = {
                    "metric": [],
                    "value": []
                }
                
                for key, value in report_data.items():
                    if key != "demographics" and isinstance(value, (int, float, str)):
                        flattened_data["metric"].append(key)
                        flattened_data["value"].append(value)
                
                df = pd.DataFrame(flattened_data)
                df.to_csv(filepath, index=False)
            
            logger.info(f"Analytics report exported: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting analytics report: {str(e)}")
            return None

# Global instance
youtube_analytics_service = YouTubeAnalyticsService()
