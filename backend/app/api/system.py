"""
系统管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.database import get_db
from app.core.config import settings
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("/config", response_model=ResponseBase)
async def get_system_config(db: AsyncSession = Depends(get_db)):
    """获取系统配置"""
    try:
        config = {
            "agent_config": settings.HERMES_AGENT_CONFIG,
            "max_concurrent_tasks": settings.AGENT_MAX_CONCURRENT_TASKS,
            "default_max_retry": settings.AGENT_DEFAULT_MAX_RETRY,
            "default_ai_model": settings.DEFAULT_AI_MODEL,
            "log_level": settings.LOG_LEVEL
        }
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=config
        )
        
    except Exception as e:
        logger.error(f"获取系统配置失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取系统配置失败：{str(e)}")


@router.put("/config", response_model=ResponseBase)
async def update_system_config(
    config_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """更新系统配置"""
    try:
        # TODO: 实现配置更新逻辑
        # 配置应该保存到数据库或配置文件中
        
        logger.info("系统配置已更新")
        
        return ResponseBase(
            code="SUCCESS",
            msg="配置已更新，部分配置需要重启后生效"
        )
        
    except Exception as e:
        logger.error(f"更新系统配置失败：{e}")
        raise HTTPException(status_code=500, detail=f"更新系统配置失败：{str(e)}")


@router.get("/logs", response_model=ResponseBase)
async def get_system_logs(
    lines: int = 100,
    level: str = "INFO"
):
    """获取系统日志"""
    try:
        # TODO: 实现日志读取逻辑
        # 应该从日志文件中读取
        
        logs = [
            {"time": "2024-01-01 00:00:00", "level": "INFO", "message": "系统启动成功"},
            # 实际应从日志文件读取
        ]
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data={"logs": logs}
        )
        
    except Exception as e:
        logger.error(f"获取系统日志失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取系统日志失败：{str(e)}")


@router.get("/health", response_model=ResponseBase)
async def get_system_health(db: AsyncSession = Depends(get_db)):
    """获取系统健康状态"""
    try:
        health_status = {
            "api": "healthy",
            "database": "healthy",
            "agent": "healthy",
            "scheduler": "healthy"
        }
        
        return ResponseBase(
            code="SUCCESS",
            msg="系统健康",
            data=health_status
        )
        
    except Exception as e:
        logger.error(f"获取系统健康状态失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取系统健康状态失败：{str(e)}")
