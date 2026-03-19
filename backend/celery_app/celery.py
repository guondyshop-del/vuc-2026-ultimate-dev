from celery import Celery
from celery.schedules import crontab
import os

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Create Celery app
celery_app = Celery(
    "vuc2026",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "celery_app.tasks.competitor_analysis",
        "celery_app.tasks.video_rendering",
        "celery_app.tasks.upload_tasks",
        "celery_app.tasks.analytics_tasks",
        "celery_app.tasks.ai_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Istanbul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Rakip analizi - her 6 saatte bir
    "analyze-competitors": {
        "task": "celery_app.tasks.competitor_analysis.analyze_all_competitors",
        "schedule": crontab(hour="*/6", minute="0"),
    },
    # Trend analizi - her 2 saatte bir
    "analyze-trends": {
        "task": "celery_app.tasks.analytics_tasks.update_trending_topics",
        "schedule": crontab(hour="*/2", minute="0"),
    },
    # Analytics güncelleme - her saat
    "update-analytics": {
        "task": "celery_app.tasks.analytics_tasks.update_channel_analytics",
        "schedule": crontab(minute="0"),
    },
    # Sistem performans kontrolü - her 5 dakika
    "monitor-system": {
        "task": "celery_app.tasks.analytics_tasks.monitor_system_performance",
        "schedule": crontab(minute="*/5"),
    },
    # Otomatik video üretim planı - her 4 saatte bir
    "auto-production": {
        "task": "celery_app.tasks.ai_tasks.auto_generate_content",
        "schedule": crontab(hour="*/4", minute="30"),
    },
    # Hayalet etkileşimler - her 15 dakikada bir
    "ghost-interactions": {
        "task": "celery_app.tasks.upload_tasks.process_ghost_interactions",
        "schedule": crontab(minute="*/15"),
    },
}

# Worker configuration for different task types
celery_app.conf.task_routes = {
    "celery_app.tasks.video_rendering.*": {"queue": "rendering"},
    "celery_app.tasks.upload_tasks.*": {"queue": "upload"},
    "celery_app.tasks.ai_tasks.*": {"queue": "ai"},
    "celery_app.tasks.competitor_analysis.*": {"queue": "analytics"},
    "celery_app.tasks.analytics_tasks.*": {"queue": "analytics"},
}

# Queue priorities
celery_app.conf.task_annotations = {
    "celery_app.tasks.upload_tasks.upload_video": {"rate_limit": "10/m"},
    "celery_app.tasks.video_rendering.render_video": {"rate_limit": "5/m"},
    "celery_app.tasks.ai_tasks.generate_script": {"rate_limit": "20/m"},
}

if __name__ == "__main__":
    celery_app.start()
