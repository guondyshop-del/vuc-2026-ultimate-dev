"""
VUC-2026 Bigtable Data Warehouse Service
YouTube analytics and metadata storage using Google Cloud Bigtable
Inspired by YouTube's own Bigtable architecture
"""

import os
import asyncio
from typing import Dict, List, Optional, Any, Union
from google.cloud import bigtable
from google.cloud.bigtable.row_set import RowSet
from google.cloud.bigtable.row_data import PartialRowData
from google.protobuf import timestamp_pb2
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class BigtableWarehouseService:
    """
    Bigtable-based data warehouse for YouTube analytics
    Based on YouTube's actual Bigtable architecture patterns
    """
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "karacocuk")
        self.instance_id = os.getenv("BIGTABLE_INSTANCE_ID", "vuc2026-warehouse")
        self.database_name = os.getenv("BIGTABLE_DATABASE", "youtube-analytics")
        
        # Initialize Bigtable client
        self.client = bigtable.Client(project=self.project_id, admin=True)
        self.instance = self.client.instance(self.instance_id)
        self.database = None
        
        # Table configurations based on YouTube's architecture
        self.table_configs = {
            "videos": {
                "column_families": {
                    "metadata": ["title", "description", "tags", "category", "duration"],
                    "analytics": ["views", "likes", "comments", "shares", "retention"],
                    "engagement": ["ctr", "avg_watch_time", "audience_retention", "engagement_rate"],
                    "monetization": ["revenue", "rpm", "cpm", "ad_types"],
                    "timestamps": ["upload_time", "publish_time", "last_updated"],
                    "versions": ["version_id", "is_current", "change_type", "change_timestamp"]
                }
            },
            "channels": {
                "column_families": {
                    "metadata": ["name", "description", "country", "language", "category"],
                    "analytics": ["subscribers", "total_views", "total_videos", "avg_views"],
                    "engagement": ["engagement_rate", "growth_rate", "activity_score"],
                    "monetization": ["channel_revenue", "sponsorships", "merchandise"],
                    "timestamps": ["created_time", "last_updated", "last_video_upload"],
                    "versions": ["version_id", "is_current", "change_type", "change_timestamp"]
                }
            },
            "playlists": {
                "column_families": {
                    "metadata": ["title", "description", "privacy", "video_count"],
                    "analytics": ["total_views", "avg_views_per_video", "completion_rate"],
                    "timestamps": ["created_time", "last_updated", "last_modified"],
                    "versions": ["version_id", "is_current", "change_type", "change_timestamp"]
                }
            },
            "analytics_events": {
                "column_families": {
                    "event_data": ["event_type", "event_value", "user_id", "session_id"],
                    "context": ["video_id", "channel_id", "playlist_id", "timestamp"],
                    "metadata": ["user_agent", "ip_address", "country", "device_type"]
                }
            }
        }
    
    async def initialize_database(self):
        """Initialize Bigtable database and tables"""
        try:
            # Create database if it doesn't exist
            if not self.database:
                self.database = self.instance.database(self.database_name)
                self.database.create()
            
            # Create tables with column families
            for table_name, config in self.table_configs.items():
                table = self.database.table(table_name)
                
                # Create column families
                for family_name in config["column_families"].keys():
                    column_family = table.column_family(family_name)
                    column_family.create()
                
                # Create table
                table.create()
                
            logger.info("Bigtable database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Bigtable database: {str(e)}")
            return False
    
    def _generate_row_key(self, entity_type: str, entity_id: str, version: Optional[str] = None) -> str:
        """
        Generate row keys following YouTube's Bigtable patterns
        
        Args:
            entity_type: Type of entity (video, channel, playlist)
            entity_id: Unique identifier
            version: Optional version for change tracking
            
        Returns:
            Formatted row key
        """
        if version:
            # Change-tracked dimension table
            return f"{entity_type}#{entity_id}#{version}"
        else:
            # Standard dimension table
            return f"{entity_type}#{entity_id}"
    
    async def store_video_metadata(self, video_data: Dict[str, Any], track_changes: bool = True) -> bool:
        """
        Store video metadata with change tracking
        
        Args:
            video_data: Video metadata dictionary
            track_changes: Whether to track changes over time
            
        Returns:
            Success status
        """
        try:
            if not self.database:
                await self.initialize_database()
            
            table = self.database.table("videos")
            video_id = video_data["video_id"]
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Standard dimension table (current state)
            row_key = self._generate_row_key("video", video_id)
            row = table.direct_row(row_key)
            
            # Store metadata
            metadata_cf = "metadata"
            for field, value in video_data.items():
                if field in self.table_configs["videos"]["column_families"][metadata_cf]:
                    row.set_cell(
                        metadata_cf,
                        field.encode(),
                        str(value).encode()
                    )
            
            # Store timestamps
            row.set_cell("timestamps", "upload_time".encode(), video_data.get("upload_time", "").encode())
            row.set_cell("timestamps", "last_updated".encode(), timestamp.encode())
            
            # Mark as current version
            row.set_cell("versions", "is_current".encode(), b"1")
            row.set_cell("versions", "version_id".encode(), timestamp.encode())
            
            # Change tracking (if enabled)
            if track_changes:
                version_key = self._generate_row_key("video", video_id, timestamp)
                version_row = table.direct_row(version_key)
                
                # Copy all data to version row
                for cf_name, columns in self.table_configs["videos"]["column_families"].items():
                    for column in columns:
                        if column in video_data:
                            version_row.set_cell(
                                cf_name,
                                column.encode(),
                                str(video_data[column]).encode()
                            )
                
                version_row.set_cell("versions", "is_current".encode(), b"0")
                version_row.set_cell("versions", "version_id".encode(), timestamp.encode())
                version_row.set_cell("versions", "change_timestamp".encode(), timestamp.encode())
                
                version_row.commit()
            
            row.commit()
            logger.info(f"Stored video metadata for {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing video metadata: {str(e)}")
            return False
    
    async def store_analytics_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Store analytics events for real-time processing
        
        Args:
            event_data: Analytics event data
            
        Returns:
            Success status
        """
        try:
            if not self.database:
                await self.initialize_database()
            
            table = self.database.table("analytics_events")
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Generate unique event row key
            event_id = f"{timestamp}#{event_data.get('user_id', 'anonymous')}#{event_data.get('event_type', 'unknown')}"
            row_key = self._generate_row_key("event", event_id)
            
            row = table.direct_row(row_key)
            
            # Store event data
            for cf_name, columns in self.table_configs["analytics_events"]["column_families"].items():
                for column in columns:
                    if column in event_data:
                        row.set_cell(
                            cf_name,
                            column.encode(),
                            str(event_data[column]).encode()
                        )
            
            # Add timestamp
            row.set_cell("context", "timestamp".encode(), timestamp.encode())
            
            row.commit()
            logger.info(f"Stored analytics event: {event_data.get('event_type', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing analytics event: {str(e)}")
            return False
    
    async def get_video_analytics(self, video_id: str, include_history: bool = False) -> Dict[str, Any]:
        """
        Retrieve video analytics with optional historical data
        
        Args:
            video_id: YouTube video ID
            include_history: Whether to include change history
            
        Returns:
            Video analytics data
        """
        try:
            if not self.database:
                await self.initialize_database()
            
            table = self.database.table("videos")
            results = {}
            
            # Get current data
            row_key = self._generate_row_key("video", video_id)
            row_set = RowSet()
            row_set.add_row_key(row_key.encode())
            
            partial_row_data = table.read_rows(row_set=row_set)
            
            for row in partial_row_data:
                results[row.row_key.decode().split('#')[-1]] = self._parse_row_data(row)
            
            # Get historical data if requested
            if include_history:
                history_results = {}
                row_set = RowSet()
                row_set.add_row_range_from_keys(
                    f"video#{video_id}#".encode(),
                    f"video#{video_id}~".encode()
                )
                
                historical_data = table.read_rows(row_set=row_set)
                
                for row in historical_data:
                    row_key_decoded = row.row_key.decode()
                    if row_key_decoded != f"video#{video_id}":  # Skip current row
                        history_results[row_key_decoded] = self._parse_row_data(row)
                
                results["history"] = history_results
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving video analytics: {str(e)}")
            return {}
    
    def _parse_row_data(self, row: PartialRowData) -> Dict[str, Any]:
        """Parse Bigtable row data into dictionary"""
        data = {}
        
        for column_family_id, columns in row.cells.items():
            data[column_family_id] = {}
            
            for column_key, cells in columns.items():
                # Get the most recent cell value
                latest_cell = max(cells, key=lambda cell: cell.timestamp)
                column_name = column_key.decode()
                cell_value = latest_cell.value.decode()
                
                # Try to parse as JSON, otherwise keep as string
                try:
                    data[column_family_id][column_name] = json.loads(cell_value)
                except (json.JSONDecodeError, ValueError):
                    data[column_family_id][column_name] = cell_value
        
        return data
    
    async def batch_store_videos(self, videos_data: List[Dict[str, Any]]) -> List[bool]:
        """
        Store multiple videos in batch for better performance
        
        Args:
            videos_data: List of video data dictionaries
            
        Returns:
            List of success statuses
        """
        tasks = [
            self.store_video_metadata(video_data) 
            for video_data in videos_data
        ]
        
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def get_channel_performance_metrics(self, channel_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive channel performance metrics
        
        Args:
            channel_id: YouTube channel ID
            days: Number of days to analyze
            
        Returns:
            Channel performance metrics
        """
        try:
            if not self.database:
                await self.initialize_database()
            
            # This would typically involve complex Bigtable queries
            # For now, return a placeholder structure
            
            metrics = {
                "channel_id": channel_id,
                "period_days": days,
                "total_videos": 0,
                "total_views": 0,
                "avg_views_per_video": 0,
                "engagement_rate": 0,
                "growth_rate": 0,
                "top_performing_videos": [],
                "upload_frequency": 0,
                "audience_demographics": {},
                "revenue_metrics": {}
            }
            
            # TODO: Implement actual Bigtable queries for metrics calculation
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting channel metrics: {str(e)}")
            return {}

# Initialize global service instance
bigtable_service = BigtableWarehouseService()
