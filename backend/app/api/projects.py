"""
项目管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from loguru import logger

from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse
)
from app.schemas.common import ResponseBase, ERROR_CODES
from datetime import datetime
import json

router = APIRouter()


@router.get("", response_model=ProjectListResponse)
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="项目状态筛选"),
    db: AsyncSession = Depends(get_db)
):
    """获取项目列表"""
    try:
        # 构建查询
        query = select(Project)
        
        # 状态筛选
        if status:
            query = query.where(Project.status == status)
        
        # 按创建时间倒序
        query = query.order_by(Project.create_time.desc())
        
        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # 执行查询
        result = await db.execute(query)
        projects = result.scalars().all()
        
        # 获取总数
        count_query = select(func.count(Project.id))
        if status:
            count_query = count_query.where(Project.status == status)
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        return ProjectListResponse(
            code="SUCCESS",
            msg="成功",
            data=[ProjectResponse.model_validate(p) for p in projects],
            total=total
        )
        
    except Exception as e:
        logger.error(f"获取项目列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取项目列表失败：{str(e)}")


@router.post("", response_model=ResponseBase)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新项目"""
    try:
        # 创建项目实例
        project = Project(
            name=project_data.name,
            product=project_data.product,
            target_market=project_data.target_market,
            core_selling_point=project_data.core_selling_point,
            target_keyword=project_data.target_keyword,
            target_channel=project_data.target_channel,
            target_domain=project_data.target_domain,
            affiliate_link=project_data.affiliate_link,
            deadline=project_data.deadline,
            remark=project_data.remark,
            status='pending',
            progress=0
        )
        
        db.add(project)
        await db.commit()
        await db.refresh(project)
        
        logger.info(f"创建新项目成功：{project.name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="项目创建成功",
            data={"id": project.id, "name": project.name}
        )
        
    except Exception as e:
        await db.rollback()
        logger.error(f"创建项目失败：{e}")
        raise HTTPException(status_code=500, detail=f"创建项目失败：{str(e)}")


@router.get("/{project_id}", response_model=ResponseBase)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取项目详情"""
    try:
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=ProjectResponse.model_validate(project)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目详情失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取项目详情失败：{str(e)}")


@router.put("/{project_id}", response_model=ResponseBase)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新项目"""
    try:
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        # 更新字段
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await db.commit()
        await db.refresh(project)
        
        logger.info(f"更新项目成功：{project.name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="项目更新成功",
            data=ProjectResponse.model_validate(project)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"更新项目失败：{e}")
        raise HTTPException(status_code=500, detail=f"更新项目失败：{str(e)}")


@router.patch("/{project_id}/status", response_model=ResponseBase)
async def update_project_status(
    project_id: int,
    status: str = Query(..., description="项目状态"),
    db: AsyncSession = Depends(get_db)
):
    """更新项目状态"""
    try:
        valid_statuses = ['pending', 'researching', 'running', 'finished', 'paused']
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"无效的状态值，必须是：{', '.join(valid_statuses)}")
        
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        project.status = status
        await db.commit()
        await db.refresh(project)
        
        logger.info(f"更新项目状态成功：{project.name} -> {status}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="项目状态更新成功",
            data=ProjectResponse.model_validate(project)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"更新项目状态失败：{e}")
        raise HTTPException(status_code=500, detail=f"更新项目状态失败：{str(e)}")


@router.delete("/{project_id}", response_model=ResponseBase)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除项目"""
    try:
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        await db.delete(project)
        await db.commit()
        
        logger.info(f"删除项目成功：{project.name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="项目删除成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"删除项目失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除项目失败：{str(e)}")


@router.get("/{project_id}/tasks", response_model=ResponseBase)
async def get_project_tasks(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取项目任务列表"""
    try:
        from app.models.task import Task
        
        # 先检查项目是否存在
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        # 查询任务列表
        query = select(Task).where(Task.project_id == project_id)
        query = query.order_by(Task.create_time.desc())
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=[{
                "id": t.id,
                "task_name": t.task_name,
                "role_name": t.role_name,
                "status": t.status,
                "progress": t.progress,
                "priority": t.priority,
                "create_time": t.create_time,
                "finish_time": t.finish_time
            } for t in tasks]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目任务列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取项目任务列表失败：{str(e)}")


@router.get("/{project_id}/stats", response_model=ResponseBase)
async def get_project_stats(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取项目统计数据"""
    try:
        from app.models.task import Task
        from sqlalchemy import func as sa_func
        
        # 检查项目是否存在
        query = select(Project).where(Project.id == project_id)
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        # 统计任务数据
        task_count_query = select(
            sa_func.count(Task.id).label("total"),
            sa_func.sum(sa_func.case((Task.status == "finished", 1), else_=0)).label("finished"),
            sa_func.sum(sa_func.case((Task.status == "running", 1), else_=0)).label("running"),
            sa_func.sum(sa_func.case((Task.status == "failed", 1), else_=0)).label("failed")
        ).where(Task.project_id == project_id)
        
        result = await db.execute(task_count_query)
        task_stats = result.first()
        
        stats_data = {
            "project": {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "progress": project.progress,
                "total_view": project.total_view,
                "total_click": project.total_click,
                "total_conversion": project.total_conversion,
                "total_commission": str(project.total_commission)
            },
            "tasks": {
                "total": task_stats.total or 0,
                "finished": task_stats.finished or 0,
                "running": task_stats.running or 0,
                "failed": task_stats.failed or 0
            }
        }
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=stats_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目统计数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取项目统计数据失败：{str(e)}")
