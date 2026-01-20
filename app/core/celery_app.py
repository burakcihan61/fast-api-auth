"""Celery application configuration"""

import os
from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
)

# Auto-discover tasks in 'app.tasks' package
celery_app.autodiscover_tasks(["app"])
