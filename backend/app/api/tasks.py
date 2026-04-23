"""
任务管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from loguru import logger

from app.core.database import get_db
from app.models.task import Task
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("", response_model=ResponseBase)
async def get_tasks(
    status: Optional[str] = Query(None, description="任务状态筛选"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    project_id: Optional[int] = Query(None, description="项目 ID 筛选"),
    role_id: Optional[int] = Query(None, description="角色 ID 筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """获取任务列表"""
    try:
        query = select(Task)
        
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if project_id:
            query = query.where(Task.project_id == project_id)
        if role_id:
            query = query.where(Task.role_id == role_id)
        
        query = query.order_by(Task.create_time.desc())
        
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=[{
                "id": task.id,
                "project_name": task.project_name,
                "role_name": task.role_name,
                "task_name": task.task_name,
                "status": task.status,
                "priority": task.priority,
                "progress": task.progress,
                "create_time": task.create_time,
                "deadline": task.deadline
            } for task in tasks]
        )
        
    except Exception as e:
        logger.error(f"获取任务列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取任务列表失败：{str(e)}")


@router.get("/{task_id}", response_model=ResponseBase)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取任务详情"""
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data={
                "id": task.id,
                "project_id": task.project_id,
                "project_name": task.project_name,
                "role_id": task.role_id,
                "role_name": task.role_name,
                "task_name": task.task_name,
                "content": task.content,
                "priority": task.priority,
                "status": task.status,
                "progress": task.progress,
                "result": task.result,
                "retry_count": task.retry_count,
                "execute_log": task.execute_log,
                "create_time": task.create_time,
                "deadline": task.deadline,
                "finish_time": task.finish_time
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务详情失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取任务详情失败：{str(e)}")


@router.post("/{task_id}/retry", response_model=ResponseBase)
async def retry_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """重试任务"""
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        if task.retry_count >= task.max_retry:
            raise HTTPException(status_code=400, detail="已达到最大重试次数")
        
        task.status = 'pending'
        task.retry_count += 1
        task.progress = 0
        
        await db.commit()
        
        logger.info(f"任务重试：{task.task_name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="任务已加入重试队列"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"重试任务失败：{e}")
        raise HTTPException(status_code=500, detail=f"重试任务失败：{str(e)}")


@router.post("/{task_id}/cancel", response_model=ResponseBase)
async def cancel_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """取消任务"""
    try:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        if task.status in ['finished', 'failed']:
            raise HTTPException(status_code=400, detail="已完成或失败的任务无法取消")
        
        task.status = 'cancelled'
        
        await db.commit()
        
        logger.info(f"任务取消：{task.task_name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="任务已取消"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"取消任务失败：{e}")
        raise HTTPException(status_code=500, detail=f"取消任务失败：{str(e)}")
