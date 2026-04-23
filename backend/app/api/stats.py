"""
数据统计 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sa_func
from datetime import datetime, timedelta
from loguru import logger

from app.core.database import get_db
from app.models.project import Project
from app.models.task import Task
from app.models.ai_role import AIRole
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("/overview", response_model=ResponseBase)
async def get_overview_stats(db: AsyncSession = Depends(get_db)):
    """获取总览数据"""
    try:
        # 项目统计
        project_count_query = select(
            sa_func.count(Project.id).label("total"),
            sa_func.sum(sa_func.case((Project.status == "running", 1), else_=0)).label("running"),
            sa_func.sum(sa_func.case((Project.status == "finished", 1), else_=0)).label("finished"),
            sa_func.sum(sa_func.case((Project.status == "pending", 1), else_=0)).label("pending")
        )
        result = await db.execute(project_count_query)
        project_stats = result.first()
        
        # 任务统计
        task_count_query = select(
            sa_func.count(Task.id).label("total"),
            sa_func.sum(sa_func.case((Task.status == "finished", 1), else_=0)).label("finished"),
            sa_func.sum(sa_func.case((Task.status == "running", 1), else_=0)).label("running"),
            sa_func.sum(sa_func.case((Task.status == "failed", 1), else_=0)).label("failed")
        )
        result = await db.execute(task_count_query)
        task_stats = result.first()
        
        # 角色统计
        role_count_query = select(
            sa_func.count(AIRole.id).label("total"),
            sa_func.sum(sa_func.case((AIRole.status == "idle", 1), else_=0)).label("idle"),
            sa_func.sum(sa_func.case((AIRole.status == "running", 1), else_=0)).label("running")
        )
        result = await db.execute(role_count_query)
        role_stats = result.first()
        
        # 总计数据
        total_data_query = select(
            sa_func.sum(Project.total_view).label("total_view"),
            sa_func.sum(Project.total_click).label("total_click"),
            sa_func.sum(Project.total_conversion).label("total_conversion"),
            sa_func.sum(Project.total_commission).label("total_commission")
        )
        result = await db.execute(total_data_query)
        total_data = result.first()
        
        overview = {
            "projects": {
                "total": project_stats.total or 0,
                "running": project_stats.running or 0,
                "finished": project_stats.finished or 0,
                "pending": project_stats.pending or 0
            },
            "tasks": {
                "total": task_stats.total or 0,
                "finished": task_stats.finished or 0,
                "running": task_stats.running or 0,
                "failed": task_stats.failed or 0
            },
            "roles": {
                "total": role_stats.total or 0,
                "idle": role_stats.idle or 0,
                "running": role_stats.running or 0
            },
            "totals": {
                "total_view": total_data.total_view or 0,
                "total_click": total_data.total_click or 0,
                "total_conversion": total_data.total_conversion or 0,
                "total_commission": str(total_data.total_commission or 0)
            }
        }
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=overview
        )
        
    except Exception as e:
        logger.error(f"获取总览数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取总览数据失败：{str(e)}")


@router.get("/trend", response_model=ResponseBase)
async def get_trend_stats(db: AsyncSession = Depends(get_db)):
    """获取趋势数据"""
    try:
        # 这里简化实现，返回模拟数据
        # 实际应该根据时间聚合统计数据
        
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        
        trend_data = {
            "dates": dates,
            "views": [0] * 7,  # 实际应从数据库查询
            "clicks": [0] * 7,
            "conversions": [0] * 7
        }
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=trend_data
        )
        
    except Exception as e:
        logger.error(f"获取趋势数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取趋势数据失败：{str(e)}")


@router.get("/channel", response_model=ResponseBase)
async def get_channel_stats(db: AsyncSession = Depends(get_db)):
    """获取渠道数据"""
    try:
        # 简化实现，返回模拟数据
        channel_data = [
            {"channel": "Facebook", "views": 0, "clicks": 0, "conversions": 0},
            {"channel": "TikTok", "views": 0, "clicks": 0, "conversions": 0},
            {"channel": "Instagram", "views": 0, "clicks": 0, "conversions": 0},
            {"channel": "YouTube", "views": 0, "clicks": 0, "conversions": 0}
        ]
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=channel_data
        )
        
    except Exception as e:
        logger.error(f"获取渠道数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取渠道数据失败：{str(e)}")
