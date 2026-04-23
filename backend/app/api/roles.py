"""
AI 角色管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from loguru import logger

from app.core.database import get_db
from app.models.ai_role import AIRole
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("", response_model=ResponseBase)
async def get_roles(
    status: Optional[str] = Query(None, description="角色状态筛选"),
    db: AsyncSession = Depends(get_db)
):
    """获取角色列表"""
    try:
        query = select(AIRole)
        
        if status:
            query = query.where(AIRole.status == status)
        
        query = query.order_by(AIRole.create_time.asc())
        result = await db.execute(query)
        roles = result.scalars().all()
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=[{
                "id": role.id,
                "role_code": role.role_code,
                "name": role.name,
                "avatar": role.avatar,
                "duty": role.duty,
                "status": role.status,
                "current_task": role.current_task,
                "total_task": role.total_task,
                "finish_task": role.finish_task,
                "success_rate": str(role.success_rate) if role.success_rate else "0"
            } for role in roles]
        )
        
    except Exception as e:
        logger.error(f"获取角色列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色列表失败：{str(e)}")


@router.get("/{role_id}", response_model=ResponseBase)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取角色详情"""
    try:
        query = select(AIRole).where(AIRole.id == role_id)
        result = await db.execute(query)
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data={
                "id": role.id,
                "role_code": role.role_code,
                "name": role.name,
                "avatar": role.avatar,
                "duty": role.duty,
                "default_prompt": role.default_prompt,
                "custom_prompt": role.custom_prompt,
                "status": role.status,
                "current_task": role.current_task
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取角色详情失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色详情失败：{str(e)}")


@router.get("/{role_id}/current-task", response_model=ResponseBase)
async def get_role_current_task(
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取角色当前任务"""
    try:
        query = select(AIRole).where(AIRole.id == role_id)
        result = await db.execute(query)
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data={
                "current_task": role.current_task,
                "status": role.status
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取角色当前任务失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色当前任务失败：{str(e)}")


@router.get("/{role_id}/history", response_model=ResponseBase)
async def get_role_history(
    role_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """获取角色历史任务"""
    try:
        from app.models.task import Task
        from sqlalchemy import select, func
        
        # 检查角色是否存在
        query = select(AIRole).where(AIRole.id == role_id)
        result = await db.execute(query)
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        # 查询历史任务
        query = select(Task).where(Task.role_id == role_id)
        query = query.order_by(Task.finish_time.desc())
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=[{
                "id": task.id,
                "task_name": task.task_name,
                "project_name": task.project_name,
                "status": task.status,
                "progress": task.progress,
                "result": task.result,
                "finish_time": task.finish_time
            } for task in tasks]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取角色历史任务失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色历史任务失败：{str(e)}")
