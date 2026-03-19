"""
VUC-2026 BigQuery Data Transfer Service
Automated YouTube data collection using Google Cloud BigQuery Data Transfer Service
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
from google.cloud import bigquery_datatransfer_v1
from google.protobuf import timestamp_pb2
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BigQueryTransferService:
    """
    BigQuery Data Transfer Service for automated YouTube analytics data collection
    """
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "karacocuk")
        self.dataset_id = os.getenv("BIGQUERY_DATASET", "vuc2026_youtube_analytics")
        self.transfer_config_name = os.getenv("BIGQUERY_TRANSFER_CONFIG_NAME")
        self.transfer_service = os.getenv("BIGQUERY_TRANSFER_SERVICE", "bigquerydatatransfer.googleapis.com")
        self.project_resource = os.getenv("BIGQUERY_PROJECT_RESOURCE")
        self.enabled = os.getenv("BIGQUERY_TRANSFER_ENABLED", "false").lower() == "true"
        
        # Initialize client
        self.client = bigquery_datatransfer_v1.DataTransferServiceClient()
        
        # YouTube Analytics transfer configuration
        self.youtube_transfer_config = {
            "data_source_id": "youtube_analytics",
            "display_name": "VUC-2026 YouTube Analytics Transfer",
            "schedule_options": {
                "disable_auto_scheduling": False,
                "start_time": {"hours": 3, "minutes": 0},  # 3 AM UTC
                "end_time": {"hours": 5, "minutes": 0}      # 5 AM UTC
            },
            "params": {
                "channel_ids": [],  # Will be populated dynamically
                "table_names": [
                    "channel_basic",
                    "video_performance", 
                    "video_analytics",
                    "channel_demographics",
                    "traffic_sources",
                    "playback_locations",
                    "device_types"
                ]
            },
            "notification_pubsub_topic": os.getenv("PUBSUB_TOPIC", "vuc2026-notifications")
        }
    
    async def create_youtube_transfer_config(self, channel_ids: List[str]) -> Dict[str, Any]:
        """
        Create YouTube Analytics data transfer configuration
        
        Args:
            channel_ids: List of YouTube channel IDs to monitor
            
        Returns:
            Transfer configuration details
        """
        try:
            if not self.enabled:
                return {
                    "success": False,
                    "error": "BigQuery Data Transfer service is not enabled"
                }
            
            if not channel_ids:
                return {
                    "success": False,
                    "error": "No channel IDs provided"
                }
            
            # Prepare transfer configuration
            transfer_config = bigquery_datatransfer_v1.TransferConfig(
                name=self.transfer_config_name,
                destination_dataset_id=self.dataset_id,
                display_name=self.youtube_transfer_config["display_name"],
                data_source_id=self.youtube_transfer_config["data_source_id"],
                schedule_options=bigquery_datatransfer_v1.ScheduleOptions(
                    disable_auto_scheduling=self.youtube_transfer_config["schedule_options"]["disable_auto_scheduling"],
                    start_time={"hours": 3, "minutes": 0},
                    end_time={"hours": 5, "minutes": 0}
                ),
                params={
                    "channel_ids": ",".join(channel_ids),
                    "table_names": self.youtube_transfer_config["params"]["table_names"]
                },
                notification_pubsub_topic=self.youtube_transfer_config["notification_pubsub_topic"]
            )
            
            # Create the transfer configuration
            response = self.client.create_transfer_config(
                parent=self.project_resource,
                transfer_config=transfer_config
            )
            
            logger.info(f"Created YouTube transfer config: {response.name}")
            
            return {
                "success": True,
                "transfer_config_id": response.name,
                "dataset_id": self.dataset_id,
                "channel_count": len(channel_ids),
                "schedule": "Daily at 3:00 AM UTC",
                "next_run_time": response.next_run_time.isoformat() if response.next_run_time else None
            }
            
        except Exception as e:
            logger.error(f"Error creating YouTube transfer config: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_transfer_configs(self) -> List[Dict[str, Any]]:
        """
        List all transfer configurations in the project
        
        Returns:
            List of transfer configurations
        """
        try:
            if not self.enabled:
                return []
            
            response = self.client.list_transfer_configs(parent=self.project_resource)
            
            configs = []
            for config in response:
                configs.append({
                    "name": config.name,
                    "display_name": config.display_name,
                    "data_source_id": config.data_source_id,
                    "destination_dataset_id": config.destination_dataset_id,
                    "state": config.state.name,
                    "schedule": str(config.schedule_options) if config.schedule_options else "Manual",
                    "next_run_time": config.next_run_time.isoformat() if config.next_run_time else None,
                    "last_modified_time": config.last_modified_time.isoformat() if config.last_modified_time else None
                })
            
            return configs
            
        except Exception as e:
            logger.error(f"Error listing transfer configs: {str(e)}")
            return []
    
    async def get_transfer_config(self, config_name: str) -> Dict[str, Any]:
        """
        Get details of a specific transfer configuration
        
        Args:
            config_name: Name of the transfer configuration
            
        Returns:
            Transfer configuration details
        """
        try:
            if not self.enabled:
                return {"success": False, "error": "Service not enabled"}
            
            response = self.client.get_transfer_config(name=config_name)
            
            return {
                "success": True,
                "name": response.name,
                "display_name": response.display_name,
                "data_source_id": response.data_source_id,
                "destination_dataset_id": response.destination_dataset_id,
                "state": response.state.name,
                "schedule_options": {
                    "disable_auto_scheduling": response.schedule_options.disable_auto_scheduling,
                    "start_time": str(response.schedule_options.start_time) if response.schedule_options.start_time else None,
                    "end_time": str(response.schedule_options.end_time) if response.schedule_options.end_time else None
                } if response.schedule_options else None,
                "params": dict(response.params) if response.params else {},
                "next_run_time": response.next_run_time.isoformat() if response.next_run_time else None,
                "last_modified_time": response.last_modified_time.isoformat() if response.last_modified_time else None
            }
            
        except Exception as e:
            logger.error(f"Error getting transfer config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def update_transfer_config(self, config_name: str, channel_ids: List[str]) -> Dict[str, Any]:
        """
        Update transfer configuration with new channel IDs
        
        Args:
            config_name: Name of the transfer configuration
            channel_ids: Updated list of YouTube channel IDs
            
        Returns:
            Update result
        """
        try:
            if not self.enabled:
                return {"success": False, "error": "Service not enabled"}
            
            # Get current config
            current_config = await self.get_transfer_config(config_name)
            if not current_config["success"]:
                return current_config
            
            # Update parameters
            updated_params = current_config["params"]
            updated_params["channel_ids"] = ",".join(channel_ids)
            
            # Prepare update mask
            update_mask = ["params"]
            
            # Update the configuration
            transfer_config = bigquery_datatransfer_v1.TransferConfig(
                name=config_name,
                params=updated_params
            )
            
            response = self.client.update_transfer_config(
                transfer_config=transfer_config,
                update_mask=update_mask
            )
            
            logger.info(f"Updated transfer config: {config_name}")
            
            return {
                "success": True,
                "transfer_config_id": response.name,
                "channel_count": len(channel_ids),
                "updated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error updating transfer config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def disable_transfer_config(self, config_name: str) -> Dict[str, Any]:
        """
        Disable a transfer configuration
        
        Args:
            config_name: Name of the transfer configuration
            
        Returns:
            Disable result
        """
        try:
            if not self.enabled:
                return {"success": False, "error": "Service not enabled"}
            
            self.client.disable_transfer_config(name=config_name)
            
            logger.info(f"Disabled transfer config: {config_name}")
            
            return {
                "success": True,
                "message": f"Transfer configuration {config_name} has been disabled",
                "disabled_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error disabling transfer config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def enable_transfer_config(self, config_name: str) -> Dict[str, Any]:
        """
        Enable a transfer configuration
        
        Args:
            config_name: Name of the transfer configuration
            
        Returns:
            Enable result
        """
        try:
            if not self.enabled:
                return {"success": False, "error": "Service not enabled"}
            
            self.client.enable_transfer_config(name=config_name)
            
            logger.info(f"Enabled transfer config: {config_name}")
            
            return {
                "success": True,
                "message": f"Transfer configuration {config_name} has been enabled",
                "enabled_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error enabling transfer config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def delete_transfer_config(self, config_name: str) -> Dict[str, Any]:
        """
        Delete a transfer configuration
        
        Args:
            config_name: Name of the transfer configuration
            
        Returns:
            Delete result
        """
        try:
            if not self.enabled:
                return {"success": False, "error": "Service not enabled"}
            
            self.client.delete_transfer_config(name=config_name)
            
            logger.info(f"Deleted transfer config: {config_name}")
            
            return {
                "success": True,
                "message": f"Transfer configuration {config_name} has been deleted",
                "deleted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error deleting transfer config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_transfer_runs(self, config_name: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get recent transfer runs for a configuration
        
        Args:
            config_name: Name of the transfer configuration
            days: Number of days to look back
            
        Returns:
            List of transfer runs
        """
        try:
            if not self.enabled:
                return []
            
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            # Create time range
            start_time_pb = timestamp_pb2.Timestamp()
            start_time_pb.FromDatetime(start_time)
            
            end_time_pb = timestamp_pb2.Timestamp()
            end_time_pb.FromDatetime(end_time)
            
            # List transfer runs
            response = self.client.list_transfer_runs(
                parent=config_name,
                start_time=start_time_pb,
                end_time=end_time_pb
            )
            
            runs = []
            for run in response:
                runs.append({
                    "name": run.name,
                    "run_time": run.run_time.isoformat() if run.run_time else None,
                    "state": run.state.name,
                    "error_status": run.error_status.message if run.error_status else None,
                    "start_time": run.start_time.isoformat() if run.start_time else None,
                    "end_time": run.end_time.isoformat() if run.end_time else None,
                    "notification_pubsub_topic": run.notification_pubsub_topic
                })
            
            return runs
            
        except Exception as e:
            logger.error(f"Error getting transfer runs: {str(e)}")
            return []
    
    async def get_service_status(self) -> Dict[str, Any]:
        """
        Get BigQuery Data Transfer service status
        
        Returns:
            Service status information
        """
        try:
            configs = await self.list_transfer_configs()
            
            active_configs = [c for c in configs if c["state"] == "ENABLED"]
            total_configs = len(configs)
            
            return {
                "enabled": self.enabled,
                "project_id": self.project_id,
                "dataset_id": self.dataset_id,
                "total_configurations": total_configs,
                "active_configurations": len(active_configs),
                "service_endpoint": self.transfer_service,
                "configurations": configs,
                "last_checked": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting service status: {str(e)}")
            return {
                "enabled": self.enabled,
                "error": str(e),
                "last_checked": datetime.utcnow().isoformat()
            }

# Initialize global service instance
bigquery_transfer_service = BigQueryTransferService()
