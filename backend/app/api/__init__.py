"""
API 路由__init__.py
"""
from app.api import auth, projects, roles, tasks, stats, system

__all__ = [
    "auth",
    "projects",
    "roles",
    "tasks",
    "stats",
    "system",
]
