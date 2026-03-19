"""
VUC-2026 BigQuery YouTube Analytics Service
Advanced YouTube channel data transfer and analytics using Google Cloud BigQuery
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BigQueryYouTubeService:
    """
    BigQuery service for YouTube analytics and data warehouse operations
    Integrates with YouTube Data Transfer Service for automated data collection
    """
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "karacocuk")
        self.dataset_id = os.getenv("BIGQUERY_DATASET", "vuc2026_youtube_analytics")
        self.location = os.getenv("BIGQUERY_LOCATION", "US")
        
        # Initialize BigQuery client
        self.client = bigquery.Client(project=self.project_id)
        
        # Define table schemas based on YouTube Analytics API
        self.table_schemas = {
            "channel_basic": [
                SchemaField("channel_id", "STRING", mode="REQUIRED"),
                SchemaField("channel_title", "STRING", mode="REQUIRED"),
                SchemaField("subscriber_count", "INTEGER"),
                SchemaField("video_count", "INTEGER"),
                SchemaField("total_views", "INTEGER"),
                SchemaField("upload_playlist", "STRING"),
                SchemaField("country", "STRING"),
                SchemaField("published_at", "TIMESTAMP"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "video_performance": [
                SchemaField("video_id", "STRING", mode="REQUIRED"),
                SchemaField("channel_id", "STRING", mode="REQUIRED"),
                SchemaField("title", "STRING", mode="REQUIRED"),
                SchemaField("description", "STRING"),
                SchemaField("published_at", "TIMESTAMP"),
                SchemaField("duration_seconds", "INTEGER"),
                SchemaField("category_id", "STRING"),
                SchemaField("tags", "STRING", mode="REPEATED"),
                SchemaField("default_language", "STRING"),
                SchemaField("view_count", "INTEGER"),
                SchemaField("like_count", "INTEGER"),
                SchemaField("comment_count", "INTEGER"),
                SchemaField("dislike_count", "INTEGER"),
                SchemaField("favorite_count", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "video_analytics": [
                SchemaField("video_id", "STRING", mode="REQUIRED"),
                SchemaField("date", "DATE", mode="REQUIRED"),
                SchemaField("views", "INTEGER"),
                SchemaField("estimated_minutes_watched", "INTEGER"),
                SchemaField("average_view_duration", "INTEGER"),
                SchemaField("average_view_percentage", "FLOAT"),
                SchemaField("annotation_clicks", "INTEGER"),
                SchemaField("annotation_clickable_impressions", "INTEGER"),
                SchemaField("annotation_closable_impressions", "INTEGER"),
                SchemaField("annotation_impressions", "INTEGER"),
                SchemaField("shares", "INTEGER"),
                SchemaField("subscribers_gained", "INTEGER"),
                SchemaField("subscribers_lost", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "channel_demographics": [
                SchemaField("channel_id", "STRING", mode="REQUIRED"),
                SchemaField("date", "DATE", mode="REQUIRED"),
                SchemaField("country", "STRING"),
                SchemaField("age_group", "STRING"),
                SchemaField("gender", "STRING"),
                SchemaField("viewer_percentage", "FLOAT"),
                SchemaField("views", "INTEGER"),
                SchemaField("estimated_minutes_watched", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "traffic_sources": [
                SchemaField("video_id", "STRING", mode="REQUIRED"),
                SchemaField("date", "DATE", mode="REQUIRED"),
                SchemaField("insight_traffic_source_type", "STRING"),
                SchemaField("insight_traffic_source_detail", "STRING"),
                SchemaField("views", "INTEGER"),
                SchemaField("estimated_minutes_watched", "INTEGER"),
                SchemaField("average_view_duration", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "playback_locations": [
                SchemaField("video_id", "STRING", mode="REQUIRED"),
                SchemaField("date", "DATE", mode="REQUIRED"),
                SchemaField("insight_playback_location_type", "STRING"),
                SchemaField("insight_playback_location_detail", "STRING"),
                SchemaField("views", "INTEGER"),
                SchemaField("estimated_minutes_watched", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ],
            
            "device_types": [
                SchemaField("video_id", "STRING", mode="REQUIRED"),
                SchemaField("date", "DATE", mode="REQUIRED"),
                SchemaField("device_type", "STRING"),
                SchemaField("operating_system", "STRING"),
                SchemaField("views", "INTEGER"),
                SchemaField("estimated_minutes_watched", "INTEGER"),
                SchemaField("data_updated_at", "TIMESTAMP")
            ]
        }
    
    async def initialize_dataset(self) -> bool:
        """Initialize BigQuery dataset and tables"""
        try:
            # Create dataset if it doesn't exist
            dataset_ref = self.client.dataset(self.dataset_id)
            
            try:
                dataset = self.client.get_dataset(dataset_ref)
                logger.info(f"Dataset {self.dataset_id} already exists")
            except Exception:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = self.location
                dataset = self.client.create_dataset(dataset)
                logger.info(f"Created dataset {self.dataset_id}")
            
            # Create tables
            for table_name, schema in self.table_schemas.items():
                table_ref = dataset_ref.table(table_name)
                
                try:
                    self.client.get_table(table_ref)
                    logger.info(f"Table {table_name} already exists")
                except Exception:
                    table = bigquery.Table(table_ref, schema=schema)
                    table = self.client.create_table(table)
                    logger.info(f"Created table {table_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing BigQuery dataset: {str(e)}")
            return False
    
    async def setup_youtube_data_transfer(self, channel_ids: List[str]) -> Dict[str, Any]:
        """
        Setup YouTube Data Transfer Service for automated data collection
        
        Args:
            channel_ids: List of YouTube channel IDs to monitor
            
        Returns:
            Setup status and configuration
        """
        try:
            # This would typically use the BigQuery Data Transfer Service API
            # For now, provide the setup instructions and configuration
            
            transfer_config = {
                "display_name": "VUC-2026 YouTube Analytics Transfer",
                "data_source_id": "youtube_analytics",
                "schedule_options": {
                    "disable_auto_scheduling": False,
                    "start_time": "03:00",  # 3 AM UTC
                    "end_time": "05:00"
                },
                "dataset_location": self.location,
                "params": {
                    "channel_ids": channel_ids,
                    "table_names": list(self.table_schemas.keys())
                },
                "notification_pubsub_topic": os.getenv("PUBSUB_TOPIC", "vuc2026-notifications")
            }
            
            # TODO: Implement actual Data Transfer Service setup
            # This requires additional permissions and service account configuration
            
            return {
                "success": True,
                "message": "YouTube Data Transfer configuration prepared",
                "config": transfer_config,
                "next_steps": [
                    "Ensure service account has BigQuery Data Transfer Admin role",
                    "Enable YouTube Analytics API",
                    "Create transfer using Data Transfer Service API",
                    "Set up Pub/Sub notifications for transfer completion"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error setting up data transfer: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def insert_channel_data(self, channel_data: Dict[str, Any]) -> bool:
        """
        Insert channel basic data into BigQuery
        
        Args:
            channel_data: Channel data from YouTube API
            
        Returns:
            Success status
        """
        try:
            table_ref = self.client.dataset(self.dataset_id).table("channel_basic")
            
            # Prepare row data
            row = {
                "channel_id": channel_data["id"],
                "channel_title": channel_data["snippet"]["title"],
                "subscriber_count": int(channel_data["statistics"].get("subscriberCount", 0)),
                "video_count": int(channel_data["statistics"].get("videoCount", 0)),
                "total_views": int(channel_data["statistics"].get("viewCount", 0)),
                "upload_playlist": channel_data["contentDetails"].get("relatedPlaylists", {}).get("uploads"),
                "country": channel_data["snippet"].get("country"),
                "published_at": channel_data["snippet"].get("publishedAt"),
                "data_updated_at": datetime.utcnow().isoformat()
            }
            
            # Insert data
            errors = self.client.insert_rows_json(table_ref, [row])
            
            if errors:
                logger.error(f"Errors inserting channel data: {errors}")
                return False
            
            logger.info(f"Successfully inserted channel data for {channel_data['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting channel data: {str(e)}")
            return False
    
    async def insert_video_performance(self, video_data: Dict[str, Any]) -> bool:
        """
        Insert video performance data into BigQuery
        
        Args:
            video_data: Video data from YouTube API
            
        Returns:
            Success status
        """
        try:
            table_ref = self.client.dataset(self.dataset_id).table("video_performance")
            
            # Prepare row data
            row = {
                "video_id": video_data["id"],
                "channel_id": video_data["snippet"]["channelId"],
                "title": video_data["snippet"]["title"],
                "description": video_data["snippet"].get("description", ""),
                "published_at": video_data["snippet"]["publishedAt"],
                "duration_seconds": self._parse_duration(video_data["contentDetails"].get("duration", "")),
                "category_id": video_data["snippet"].get("categoryId"),
                "tags": video_data["snippet"].get("tags", []),
                "default_language": video_data["snippet"].get("defaultLanguage"),
                "view_count": int(video_data["statistics"].get("viewCount", 0)),
                "like_count": int(video_data["statistics"].get("likeCount", 0)),
                "comment_count": int(video_data["statistics"].get("commentCount", 0)),
                "dislike_count": int(video_data["statistics"].get("dislikeCount", 0)),
                "favorite_count": int(video_data["statistics"].get("favoriteCount", 0)),
                "data_updated_at": datetime.utcnow().isoformat()
            }
            
            # Insert data
            errors = self.client.insert_rows_json(table_ref, [row])
            
            if errors:
                logger.error(f"Errors inserting video data: {errors}")
                return False
            
            logger.info(f"Successfully inserted video data for {video_data['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting video data: {str(e)}")
            return False
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse YouTube duration format (PT4M13S) to seconds"""
        try:
            import re
            pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
            matches = re.match(pattern, duration_str)
            
            if not matches:
                return 0
            
            hours = int(matches.group(1) or 0)
            minutes = int(matches.group(2) or 0)
            seconds = int(matches.group(3) or 0)
            
            return hours * 3600 + minutes * 60 + seconds
            
        except Exception:
            return 0
    
    async def execute_analytics_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute custom analytics query
        
        Args:
            query: SQL query string
            
        Returns:
            Query results
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convert to list of dictionaries
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return []
    
    async def get_top_performing_videos(self, channel_id: str, days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top performing videos for a channel
        
        Args:
            channel_id: YouTube channel ID
            days: Number of days to analyze
            limit: Maximum number of videos to return
            
        Returns:
            List of top performing videos
        """
        query = f"""
        SELECT 
            video_id,
            title,
            view_count,
            like_count,
            comment_count,
            published_at,
            ROUND(view_count / NULLIF(like_count, 0), 2) as views_per_like
        FROM `{self.project_id}.{self.dataset_id}.video_performance`
        WHERE channel_id = '{channel_id}'
            AND published_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        ORDER BY view_count DESC
        LIMIT {limit}
        """
        
        return await self.execute_analytics_query(query)
    
    async def get_channel_growth_metrics(self, channel_id: str, days: int = 90) -> Dict[str, Any]:
        """
        Get comprehensive channel growth metrics
        
        Args:
            channel_id: YouTube channel ID
            days: Number of days to analyze
            
        Returns:
            Channel growth metrics
        """
        query = f"""
        SELECT 
            COUNT(*) as total_videos,
            SUM(view_count) as total_views,
            AVG(view_count) as avg_views_per_video,
            SUM(like_count) as total_likes,
            SUM(comment_count) as total_comments,
            DATE(published_at) as upload_date
        FROM `{self.project_id}.{self.dataset_id}.video_performance`
        WHERE channel_id = '{channel_id}'
            AND published_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY DATE(published_at)
        ORDER BY upload_date DESC
        """
        
        results = await self.execute_analytics_query(query)
        
        # Calculate growth metrics
        if results:
            total_views = sum(row["total_views"] for row in results)
            total_videos = len(results)
            avg_views = total_views / total_videos if total_videos > 0 else 0
            
            return {
                "channel_id": channel_id,
                "period_days": days,
                "total_videos": total_videos,
                "total_views": total_views,
                "avg_views_per_video": avg_views,
                "daily_breakdown": results,
                "growth_trend": self._calculate_growth_trend(results)
            }
        
        return {}
    
    def _calculate_growth_trend(self, daily_data: List[Dict[str, Any]]) -> str:
        """Calculate growth trend from daily data"""
        if len(daily_data) < 2:
            return "insufficient_data"
        
        # Simple trend calculation based on recent vs older performance
        recent_avg = sum(row["total_views"] for row in daily_data[:7]) / 7
        older_avg = sum(row["total_views"] for row in daily_data[-7:]) / 7
        
        if recent_avg > older_avg * 1.1:
            return "growing"
        elif recent_avg < older_avg * 0.9:
            return "declining"
        else:
            return "stable"

# Initialize global service instance
bigquery_service = BigQueryYouTubeService()
