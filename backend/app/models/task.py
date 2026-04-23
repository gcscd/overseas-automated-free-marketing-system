"""
任务数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Task(Base):
    """任务表"""
    __tablename__ = "t_task"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="任务 ID")
    project_id = Column(Integer, ForeignKey("t_project.id"), nullable=False, comment="所属项目 ID")
    project_name = Column(String(255), nullable=False, comment="所属项目名称")
    role_id = Column(Integer, ForeignKey("t_ai_role.id"), nullable=False, comment="负责角色 ID")
    role_name = Column(String(50), nullable=False, comment="负责角色名称")
    task_name = Column(String(255), nullable=False, comment="任务名称")
    content = Column(Text, nullable=False, comment="任务执行要求")
    priority = Column(String(20), nullable=False, default='medium', comment="优先级：high/medium/low")
    status = Column(String(20), nullable=False, default='pending', comment="状态：pending/running/finished/failed")
    progress = Column(Integer, nullable=False, default=0, comment="任务进度 0-100")
    result = Column(Text, nullable=True, comment="任务执行结果")
    retry_count = Column(Integer, nullable=False, default=0, comment="已重试次数")
    max_retry = Column(Integer, nullable=False, default=2, comment="最大重试次数")
    pre_task_id = Column(Integer, ForeignKey("t_task.id"), nullable=True, comment="前置任务 ID")
    dependency_type = Column(String(50), default='finish_to_start', comment="依赖类型")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    deadline = Column(DateTime, nullable=False, comment="截止时间")
    finish_time = Column(DateTime, nullable=True, comment="完成时间")
    execute_log = Column(Text, nullable=True, comment="执行日志")
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.task_name}', status='{self.status}')>"
