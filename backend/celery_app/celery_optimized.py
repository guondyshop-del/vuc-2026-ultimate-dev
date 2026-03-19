"""
VUC-2026 Optimized Celery Configuration
High-concurrency video processing with Redis backend
"""

import os
from celery import Celery
from kombu import Queue, Exchange
from celery.schedules import crontab
from typing import Dict, Any

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery app configuration with optimized settings
celery_app = Celery(
    "vuc2026",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "app.celery_app.tasks.video_tasks",
        "app.celery_app.tasks.upload_tasks", 
        "app.celery_app.tasks.render_tasks",
        "app.celery_app.tasks.analytics_tasks"
    ]
)

# Optimized configuration for high-concurrency video processing
celery_app.conf.update(
    # Task execution settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Concurrency and performance settings
    worker_prefetch_multiplier=1,  # Disable prefetch for better load balancing
    task_acks_late=True,  # Only acknowledge after task completion
    worker_disable_rate_limits=False,
    
    # Result backend settings
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
        "retry_policy": {
            "timeout": 5.0
        }
    },
    
    # Task routing and queues
    task_routes={
        "app.celery_app.tasks.video_tasks.*": {"queue": "video_processing"},
        "app.celery_app.tasks.upload_tasks.*": {"queue": "upload_queue"},
        "app.celery_app.tasks.render_tasks.*": {"queue": "render_queue"},
        "app.celery_app.tasks.analytics_tasks.*": {"queue": "analytics_queue"},
    },
    
    # Queue definitions with priorities
    task_default_queue="default",
    task_queues={
        Queue("video_processing", Exchange("video_processing"), routing_key="video_processing",
              queue_arguments={"x-max-priority": 10}),
        Queue("upload_queue", Exchange("upload_queue"), routing_key="upload_queue",
              queue_arguments={"x-max-priority": 8}),
        Queue("render_queue", Exchange("render_queue"), routing_key="render_queue",
              queue_arguments={"x-max-priority": 6}),
        Queue("analytics_queue", Exchange("analytics_queue"), routing_key="analytics_queue",
              queue_arguments={"x-max-priority": 4}),
        Queue("default", Exchange("default"), routing_key="default"),
    },
    
    # Retry and error handling
    task_reject_on_worker_lost=True,
    task_ignore_result=False,
    task_track_started=True,
    task_publish_retry_policy={
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    },
    
    # Monitoring and health checks
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Beat scheduler for periodic tasks
    beat_schedule={
        "cleanup-expired-results": {
            "task": "app.celery_app.tasks.maintenance.cleanup_expired_results",
            "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
        },
        "health-check": {
            "task": "app.celery_app.tasks.maintenance.health_check",
            "schedule": crontab(minute="*/5"),  # Every 5 minutes
        },
        "audit-system-metrics": {
            "task": "app.celery_app.tasks.analytics.audit_system_metrics",
            "schedule": crontab(minute=0, hour="*/1"),  # Every hour
        },
    },
    
    # Resource limits
    worker_max_tasks_per_child=50,  # Restart workers after 50 tasks
    worker_max_memory_per_child=500000,  # 500MB memory limit
    
    # Shadowban shield settings
    task_annotations={
        "*": {"rate_limit": "10/m"},  # Default rate limit
        "app.celery_app.tasks.upload_tasks.upload_video": {"rate_limit": "2/m"},
        "app.celery_app.tasks.render_tasks.render_video": {"rate_limit": "5/m"},
    }
)


class TaskPriority:
    """Task priority constants for VUC-2026"""
    CRITICAL = 10
    HIGH = 8
    NORMAL = 5
    LOW = 2


class TaskConfig:
    """Task configuration with retry policies"""
    
    @staticmethod
    def get_video_render_config() -> Dict[str, Any]:
        """Configuration for video rendering tasks"""
        return {
            "queue": "render_queue",
            "priority": TaskPriority.HIGH,
            "retry": True,
            "retry_policy": {
                "max_retries": 3,
                "interval_start": 60,  # 1 minute
                "interval_step": 60,    # Add 1 minute each retry
                "interval_max": 300,    # Max 5 minutes
            },
            "time_limit": 1800,  # 30 minutes
            "soft_time_limit": 1500,  # 25 minutes
            "bind": True,
        }
    
    @staticmethod
    def get_video_upload_config() -> Dict[str, Any]:
        """Configuration for video upload tasks"""
        return {
            "queue": "upload_queue",
            "priority": TaskPriority.CRITICAL,
            "retry": True,
            "retry_policy": {
                "max_retries": 5,
                "interval_start": 120,  # 2 minutes
                "interval_step": 120,   # Add 2 minutes each retry
                "interval_max": 600,    # Max 10 minutes
            },
            "time_limit": 900,   # 15 minutes
            "soft_time_limit": 720,  # 12 minutes
            "bind": True,
        }
    
    @staticmethod
    def get_analytics_config() -> Dict[str, Any]:
        """Configuration for analytics tasks"""
        return {
            "queue": "analytics_queue",
            "priority": TaskPriority.LOW,
            "retry": True,
            "retry_policy": {
                "max_retries": 2,
                "interval_start": 30,
                "interval_step": 30,
                "interval_max": 180,
            },
            "time_limit": 300,  # 5 minutes
            "soft_time_limit": 240,  # 4 minutes
        }


# Worker configuration for different task types
WORKER_CONFIGS = {
    "video_worker": {
        "queues": ["video_processing", "render_queue"],
        "concurrency": 2,  # Limited for CPU-intensive tasks
        "prefetch_multiplier": 1,
        "max_tasks_per_child": 10,  # Restart more often for video processing
    },
    "upload_worker": {
        "queues": ["upload_queue"],
        "concurrency": 4,  # Higher for I/O-bound uploads
        "prefetch_multiplier": 2,
        "max_tasks_per_child": 20,
    },
    "analytics_worker": {
        "queues": ["analytics_queue", "default"],
        "concurrency": 8,  # High for lightweight analytics
        "prefetch_multiplier": 4,
        "max_tasks_per_child": 100,
    }
}


def get_celery_worker_args(worker_type: str = "default") -> list:
    """Get celery worker arguments for specific worker type"""
    config = WORKER_CONFIGS.get(worker_type, WORKER_CONFIGS["analytics_worker"])
    
    args = [
        "worker",
        f"--loglevel=info",
        f"--queues={','.join(config['queues'])}",
        f"--concurrency={config['concurrency']}",
        f"--prefetch-multiplier={config['prefetch_multiplier']}",
        f"--max-tasks-per-child={config['max_tasks_per_child']}",
        "--without-gossip",
        "--without-mingle",
        "--without-heartbeat",
    ]
    
    return args


if __name__ == "__main__":
    celery_app.start()
