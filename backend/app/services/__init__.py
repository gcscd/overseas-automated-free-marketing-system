"""
服务模块__init__.py
"""
from app.services.ai_client import ai_client, AIClient
from app.services.task_executor import task_executor, TaskExecutor
from app.services.scheduler import scheduler, TaskScheduler
from app.services.platforms import get_platform, SocialMediaPlatform

__all__ = [
    "ai_client",
    "AIClient",
    "task_executor",
    "TaskExecutor",
    "scheduler",
    "TaskScheduler",
    "get_platform",
    "SocialMediaPlatform",
]
