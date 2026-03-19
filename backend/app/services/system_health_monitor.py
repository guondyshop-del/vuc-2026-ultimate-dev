"""
VUC-2026 System Health Monitor
Production-ready system monitoring with automated alerts
"""

import os
import logging
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from celery import Celery
from pydantic import BaseModel, Field

from app.services.self_healing_service import SelfHealingService

# Global instance
self_healing_service = SelfHealingService()

logger = logging.getLogger(__name__)

# Celery app instance
celery_app = Celery('vuc2026')

class SystemAlert(BaseModel):
    """System alert data structure"""
    model_config = {"arbitrary_types_allowed": True}
    
    alert_type: str
    severity: str  # info, warning, critical
    message: str
    metric_value: Union[str, int, float, bool, Dict[str, Any], List[Any]]
    threshold: Union[str, int, float, bool, Dict[str, Any], List[Any]]
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None

class SystemHealthMonitor:
    """VUC-2026 System Health Monitor"""
    
    def __init__(self):
        self.alerts_history = []
        self.active_alerts = []
        self.metrics_history = []
        
        # Alert thresholds from .windsurfrules
        self.thresholds = {
            "disk_space_below_10gb": 10,  # GB
            "memory_usage_above_90": 90,  # %
            "cpu_threshold": 90,  # %
            "gpu_threshold": 85,  # %
            "api_quota_exhausted": True,
            "render_queue_overflow": 10,  # tasks
            "upload_failure_rate_above_20": 20  # %
        }
        
        # Alert persistence
        self.alerts_file = "../vuc_memory/system_alerts.json"
        self.metrics_file = "../vuc_memory/system_metrics.json"
        
        # Load existing data
        self._load_alerts_history()
        self._load_metrics_history()
    
    def _load_alerts_history(self):
        """Load alerts history from file"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.alerts_history = [
                        SystemAlert(**alert) for alert in data.get("alerts", [])
                    ]
                    self.active_alerts = [
                        alert for alert in self.alerts_history if not alert.resolved
                    ]
        except Exception as e:
            logger.error(f"Failed to load alerts history: {e}")
    
    def _load_metrics_history(self):
        """Load metrics history from file"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    self.metrics_history = json.load(f).get("metrics", [])
        except Exception as e:
            logger.error(f"Failed to load metrics history: {e}")
    
    def _save_alerts(self):
        """Save alerts to file"""
        try:
            data = {
                "alerts": [
                    {
                        "alert_type": alert.alert_type,
                        "severity": alert.severity,
                        "message": alert.message,
                        "metric_value": alert.metric_value,
                        "threshold": alert.threshold,
                        "timestamp": alert.timestamp.isoformat(),
                        "resolved": alert.resolved,
                        "resolution_time": alert.resolution_time.isoformat() if alert.resolution_time else None
                    }
                    for alert in self.alerts_history
                ],
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save alerts: {e}")
    
    def _save_metrics(self):
        """Save metrics to file"""
        try:
            # Keep only last 1000 entries
            recent_metrics = self.metrics_history[-1000:]
            
            data = {
                "metrics": recent_metrics,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def create_alert(self, alert_type: str, severity: str, message: str, 
                    metric_value: Any, threshold: Any) -> SystemAlert:
        """Create and log a new alert"""
        
        alert = SystemAlert(
            alert_type=alert_type,
            severity=severity,
            message=message,
            metric_value=metric_value,
            threshold=threshold,
            timestamp=datetime.now()
        )
        
        # Add to history and active alerts
        self.alerts_history.append(alert)
        self.active_alerts.append(alert)
        
        # Log the alert
        log_level = {
            "info": logger.info,
            "warning": logger.warning,
            "critical": logger.error
        }.get(severity, logger.info)
        
        log_level(f"ALERT [{severity.upper()}] {alert_type}: {message}")
        
        # Save to file
        self._save_alerts()
        
        return alert
    
    def resolve_alert(self, alert_type: str) -> bool:
        """Resolve active alerts by type"""
        resolved_count = 0
        
        for alert in self.active_alerts:
            if alert.alert_type == alert_type and not alert.resolved:
                alert.resolved = True
                alert.resolution_time = datetime.now()
                resolved_count += 1
        
        if resolved_count > 0:
            logger.info(f"Resolved {resolved_count} alerts for {alert_type}")
            self._save_alerts()
            return True
        
        return False
    
    async def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        try:
            # Get basic health status from self-healing service
            health_status = self_healing_service.check_system_health()
            
            # Record metrics
            metrics_entry = {
                "timestamp": datetime.now().isoformat(),
                "metrics": health_status.get("metrics", {}),
                "overall_health": health_status.get("overall_health", "unknown")
            }
            
            self.metrics_history.append(metrics_entry)
            self._save_metrics()
            
            # Check for alerts
            await self._check_for_alerts(health_status)
            
            # Add alert summary to health status
            health_status["active_alerts_count"] = len(self.active_alerts)
            health_status["active_alerts"] = [
                {
                    "type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat()
                }
                for alert in self.active_alerts
            ]
            
            return health_status
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            
            # Create critical alert
            self.create_alert(
                alert_type="health_check_failure",
                severity="critical",
                message=f"System health check failed: {str(e)}",
                metric_value=str(e),
                threshold="N/A"
            )
            
            return {
                "timestamp": datetime.now().isoformat(),
                "overall_health": "error",
                "alerts": [f"Health check failed: {str(e)}"],
                "metrics": {},
                "active_alerts_count": len(self.active_alerts)
            }
    
    async def _check_for_alerts(self, health_status: Dict[str, Any]):
        """Check health status for alert conditions"""
        metrics = health_status.get("metrics", {})
        
        # Disk space alert
        disk_free_gb = metrics.get("disk_free_gb")
        if disk_free_gb is not None and disk_free_gb < self.thresholds["disk_space_below_10gb"]:
            self.create_alert(
                alert_type="disk_space_low",
                severity="critical",
                message=f"Low disk space: {disk_free_gb:.1f}GB remaining",
                metric_value=disk_free_gb,
                threshold=self.thresholds["disk_space_below_10gb"]
            )
        else:
            # Resolve if back to normal
            if disk_free_gb is not None and disk_free_gb >= self.thresholds["disk_space_below_10gb"]:
                self.resolve_alert("disk_space_low")
        
        # Memory usage alert
        memory_usage = metrics.get("memory_usage")
        if memory_usage is not None and memory_usage > self.thresholds["memory_usage_above_90"]:
            self.create_alert(
                alert_type="memory_high",
                severity="warning",
                message=f"High memory usage: {memory_usage:.1f}%",
                metric_value=memory_usage,
                threshold=self.thresholds["memory_usage_above_90"]
            )
        else:
            # Resolve if back to normal
            if memory_usage is not None and memory_usage <= self.thresholds["memory_usage_above_90"]:
                self.resolve_alert("memory_high")
        
        # CPU usage alert
        cpu_usage = metrics.get("cpu_usage")
        if cpu_usage is not None and cpu_usage > self.thresholds["cpu_threshold"]:
            self.create_alert(
                alert_type="cpu_high",
                severity="warning",
                message=f"High CPU usage: {cpu_usage:.1f}%",
                metric_value=cpu_usage,
                threshold=self.thresholds["cpu_threshold"]
            )
        else:
            # Resolve if back to normal
            if cpu_usage is not None and cpu_usage <= self.thresholds["cpu_threshold"]:
                self.resolve_alert("cpu_high")
        
        # GPU usage alert
        gpu_usage = metrics.get("gpu_usage")
        if isinstance(gpu_usage, (int, float)) and gpu_usage > self.thresholds["gpu_threshold"]:
            self.create_alert(
                alert_type="gpu_high",
                severity="warning",
                message=f"High GPU usage: {gpu_usage:.1f}%",
                metric_value=gpu_usage,
                threshold=self.thresholds["gpu_threshold"]
            )
        else:
            # Resolve if back to normal
            if isinstance(gpu_usage, (int, float)) and gpu_usage <= self.thresholds["gpu_threshold"]:
                self.resolve_alert("gpu_high")
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts"""
        total_alerts = len(self.alerts_history)
        active_alerts = len(self.active_alerts)
        
        # Count by severity
        severity_counts = {"info": 0, "warning": 0, "critical": 0}
        for alert in self.active_alerts:
            severity_counts[alert.severity] += 1
        
        # Count by type
        type_counts = {}
        for alert in self.active_alerts:
            type_counts[alert.alert_type] = type_counts.get(alert.alert_type, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "severity_breakdown": severity_counts,
            "type_breakdown": type_counts,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_metrics_trend(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics trend for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_metrics = [
            entry for entry in self.metrics_history
            if datetime.fromisoformat(entry["timestamp"]) >= cutoff_time
        ]
        
        if not recent_metrics:
            return {"error": "No metrics data available"}
        
        # Calculate averages and trends
        metrics_summary = {}
        
        for metric_name in ["memory_usage", "cpu_usage", "gpu_usage", "disk_free_gb"]:
            values = []
            timestamps = []
            
            for entry in recent_metrics:
                metric_value = entry.get("metrics", {}).get(metric_name)
                if metric_value is not None and isinstance(metric_value, (int, float)):
                    values.append(metric_value)
                    timestamps.append(entry["timestamp"])
            
            if values:
                metrics_summary[metric_name] = {
                    "current": values[-1] if values else None,
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "trend": "increasing" if len(values) > 1 and values[-1] > values[0] else "decreasing" if len(values) > 1 and values[-1] < values[0] else "stable",
                    "data_points": len(values)
                }
        
        return {
            "time_period_hours": hours,
            "metrics_summary": metrics_summary,
            "data_points": len(recent_metrics),
            "generated_at": datetime.now().isoformat()
        }

# Global health monitor instance
health_monitor = SystemHealthMonitor()

@celery_app.task
def system_health_check_task() -> Dict[str, Any]:
    """Periodic system health check task"""
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(health_monitor.check_system_health())
        loop.close()
        return result
    except Exception as e:
        logger.error(f"System health check task failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@celery_app.task
def cleanup_old_alerts_task(days_to_keep: int = 30) -> Dict[str, Any]:
    """Clean up old resolved alerts"""
    try:
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Remove old resolved alerts
        original_count = len(health_monitor.alerts_history)
        health_monitor.alerts_history = [
            alert for alert in health_monitor.alerts_history
            if not alert.resolved or alert.resolution_time >= cutoff_date
        ]
        
        # Update active alerts
        health_monitor.active_alerts = [
            alert for alert in health_monitor.alerts_history if not alert.resolved
        ]
        
        removed_count = original_count - len(health_monitor.alerts_history)
        
        # Save updated alerts
        health_monitor._save_alerts()
        
        logger.info(f"Cleaned up {removed_count} old alerts")
        
        return {
            "success": True,
            "removed_count": removed_count,
            "remaining_count": len(health_monitor.alerts_history),
            "cleanup_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Alert cleanup failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
