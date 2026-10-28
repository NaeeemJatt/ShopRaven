"""
Celery distributed worker and Beat scheduler configuration.
"""

from celery import Celery
from celery.schedules import crontab
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "shopraven",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.pipeline_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Karachi",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    beat_schedule={
        # 1. Product Hunting Scout: Runs every 30 minutes
        "run_market_scout_every_30m": {
            "task": "app.tasks.pipeline_tasks.run_market_scout_task",
            "schedule": crontab(minute="*/30"),
        },
        # 2. Parallel SEO & AI Search Engine Optimization (AEO/GEO): Every 30 minutes
        "run_parallel_seo_ai_every_30m": {
            "task": "app.tasks.pipeline_tasks.run_parallel_seo_ai_task",
            "schedule": crontab(minute="*/30"),
        },
        # 3. Parallel Autonomous Storefront Auditor & Self-Healing: Every 30 minutes
        "run_storefront_auditor_every_30m": {
            "task": "app.tasks.pipeline_tasks.run_storefront_auditor_task",
            "schedule": crontab(minute="*/30"),
        },
        # 4. Parallel Visitor Clickstream & Drop-Off Analyzer: Every 15 minutes
        "run_visitor_behavior_analyzer_every_15m": {
            "task": "app.tasks.pipeline_tasks.run_visitor_behavior_analyzer_task",
            "schedule": crontab(minute="*/15"),
        },
        # 5. Supplier Stock & Waitlist Sync: Runs every 2 hours
        "run_stock_sync_every_2h": {
            "task": "app.tasks.pipeline_tasks.sync_supplier_stock_and_waitlists",
            "schedule": crontab(minute="0", hour="*/2"),
        },
        # 6. Weekly Auto-Blog & Menu Reorder: Every Sunday at 02:00 AM PKT
        "run_weekly_blog_and_menu_sort": {
            "task": "app.tasks.pipeline_tasks.run_weekly_blog_and_menu_task",
            "schedule": crontab(minute="0", hour="2", day_of_week="sunday"),
        },
        # 7. Hugging Face Dataset Database Checkpoint: Runs every 30 minutes
        "backup_database_to_hf_dataset_every_30m": {
            "task": "app.tasks.pipeline_tasks.backup_database_to_hf_dataset",
            "schedule": crontab(minute="*/30"),
        },
    },
)

