"""
定时任务调度器
使用 APScheduler 实现任务调度
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from datetime import datetime
from typing import Optional, Callable, Dict
import asyncio

from app.core.config import settings
from app.core.agent import agent
from app.models.task import Task
from app.models.project import Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.jobs: Dict[str, any] = {}
        logger.info("任务调度器初始化完成")
    
    def start(self):
        """启动调度器"""
        self.scheduler.start()
        logger.info("任务调度器已启动")
        
        # 添加定期任务
        self._add_periodic_tasks()
    
    def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        logger.info("任务调度器已停止")
    
    def _add_periodic_tasks(self):
        """添加定期执行的任务"""
        
        # 每 10 秒检查待处理任务
        self.scheduler.add_job(
            func=self._check_pending_tasks,
            trigger=IntervalTrigger(seconds=10),
            id='check_pending_tasks',
            name='检查待处理任务',
            replace_existing=True
        )
        
        # 每分钟检查超时任务
        self.scheduler.add_job(
            func=self._check_timeout_tasks,
            trigger=IntervalTrigger(minutes=1),
            id='check_timeout_tasks',
            name='检查超时任务',
            replace_existing=True
        )
        
        # 每天凌晨 2 点清理完成的任务
        self.scheduler.add_job(
            func=self._cleanup_finished_tasks,
            trigger=CronTrigger(hour=2, minute=0),
            id='cleanup_finished_tasks',
            name='清理完成的任务',
            replace_existing=True
        )
        
        # 每小时更新关键词排名
        self.scheduler.add_job(
            func=self._update_keyword_rankings,
            trigger=IntervalTrigger(hours=1),
            id='update_keyword_rankings',
            name='更新关键词排名',
            replace_existing=True
        )
        
        # 每天上午 9 点生成日报
        self.scheduler.add_job(
            func=self._generate_daily_report,
            trigger=CronTrigger(hour=9, minute=0),
            id='generate_daily_report',
            name='生成日报',
            replace_existing=True
        )
    
    async def _check_pending_tasks(self):
        """检查并执行待处理的任务"""
        try:
            from app.core.database import async_session_maker
            
            async with async_session_maker() as session:
                # 查询待处理任务
                query = select(Task).where(Task.status == 'pending')
                query = query.order_by(Task.priority.desc(), Task.create_time.asc())
                query = query.limit(10)  # 每次最多处理 10 个任务
                
                result = await session.execute(query)
                tasks = result.scalars().all()
                
                for task in tasks:
                    # 检查是否有前置任务
                    if task.pre_task_id:
                        pre_query = select(Task).where(Task.id == task.pre_task_id)
                        pre_result = await session.execute(pre_query)
                        pre_task = pre_result.scalar_one_or_none()
                        
                        if pre_task and pre_task.status != 'finished':
                            logger.info(f"任务 {task.id} 的前置任务未完成，跳过")
                            continue
                    
                    # 更新任务状态为运行中
                    task.status = 'running'
                    task.progress = 10
                    await session.commit()
                    
                    # 异步执行任务
                    asyncio.create_task(self._execute_task(task, session))
                    
        except Exception as e:
            logger.error(f"检查待处理任务失败：{e}")
    
    async def _execute_task(self, task: Task, session: AsyncSession):
        """执行单个任务"""
        task_id = task.id
        
        try:
            logger.info(f"开始执行任务 {task_id}: {task.task_name}")
            
            # 准备任务数据
            task_data = {
                'id': task_id,
                'role_name': task.role_name,
                'task_name': task.task_name,
                'content': task.content,
                'prompt': task.content,  # 简化处理
                'task_type': 'general'
            }
            
            # 执行任务
            result = await agent.execute_with_retry(task_data)
            
            # 更新任务状态
            task.status = 'finished'
            task.progress = 100
            task.result = result
            task.finish_time = datetime.now()
            
            # 更新项目进度
            await self._update_project_progress(session, task.project_id)
            
            logger.info(f"任务 {task_id} 执行完成")
            
        except Exception as e:
            logger.error(f"任务 {task_id} 执行失败：{e}")
            task.status = 'failed'
            task.execute_log = f"{task.execute_log or ''}\n错误：{str(e)}"
            
            # 判断是否重试
            if task.retry_count < task.max_retry:
                task.status = 'pending'
                task.retry_count += 1
                logger.info(f"任务 {task_id} 将重试（第 {task.retry_count} 次）")
            else:
                logger.error(f"任务 {task_id} 已达到最大重试次数，标记为失败")
        
        finally:
            await session.commit()
    
    async def _update_project_progress(self, session: AsyncSession, project_id: int):
        """更新项目进度"""
        try:
            # 查询项目的所有任务
            from sqlalchemy import func as sa_func
            
            task_count_query = select(
                sa_func.count(Task.id).label("total"),
                sa_func.sum(sa_func.case((Task.status == "finished", 1), else_=0)).label("finished")
            ).where(Task.project_id == project_id)
            
            result = await session.execute(task_count_query)
            stats = result.first()
            
            if stats:
                total = stats.total or 0
                finished = stats.finished or 0
                
                # 更新项目
                project_query = select(Project).where(Project.id == project_id)
                project_result = await session.execute(project_query)
                project = project_result.scalar_one_or_none()
                
                if project:
                    project.total_task = total
                    project.finish_task = finished
                    project.progress = int((finished / total * 100) if total > 0 else 0)
                    
                    # 如果所有任务完成，更新项目状态
                    if finished == total and total > 0:
                        project.status = 'finished'
                    
                    logger.info(f"项目 {project_id} 进度更新：{project.progress}%")
                    
        except Exception as e:
            logger.error(f"更新项目进度失败：{e}")
    
    async def _check_timeout_tasks(self):
        """检查超时任务"""
        try:
            from app.core.database import async_session_maker
            from sqlalchemy import and_
            
            async with async_session_maker() as session:
                # 查询超时任务
                query = select(Task).where(
                    and_(
                        Task.status == 'running',
                        Task.deadline < datetime.now()
                    )
                )
                
                result = await session.execute(query)
                tasks = result.scalars().all()
                
                for task in tasks:
                    logger.warning(f"任务 {task.id} 已超时")
                    task.status = 'failed'
                    task.execute_log = f"{task.execute_log or ''}\n超时：{datetime.now()}"
                
                await session.commit()
                
        except Exception as e:
            logger.error(f"检查超时任务失败：{e}")
    
    async def _cleanup_finished_tasks(self):
        """清理完成的任务"""
        try:
            from app.core.database import async_session_maker
            from sqlalchemy import delete
            from datetime import timedelta
            
            async with async_session_maker() as session:
                # 删除 30 天前完成的失败任务
                cutoff_date = datetime.now() - timedelta(days=30)
                
                # 这里简化实现，实际应该更复杂的清理逻辑
                logger.info("清理完成的任务...")
                
        except Exception as e:
            logger.error(f"清理任务失败：{e}")
    
    async def _update_keyword_rankings(self):
        """更新关键词排名"""
        try:
            # TODO: 实现关键词排名查询
            logger.debug("执行关键词排名更新...")
        except Exception as e:
            logger.error(f"更新关键词排名失败：{e}")
    
    async def _generate_daily_report(self):
        """生成日报"""
        try:
            # TODO: 实现日报生成逻辑
            logger.info("生成系统日报...")
        except Exception as e:
            logger.error(f"生成日报失败：{e}")


# 全局调度器实例
scheduler = TaskScheduler()
