"""
AI 角色数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AIRole(Base):
    """AI 角色表"""
    __tablename__ = "t_ai_role"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="角色 ID")
    role_code = Column(String(50), nullable=False, unique=True, comment="角色编码")
    name = Column(String(50), nullable=False, comment="角色名称")
    avatar = Column(String(500), nullable=False, comment="头像地址")
    duty = Column(Text, nullable=False, comment="核心职责")
    default_prompt = Column(Text, nullable=False, comment="默认系统 Prompt")
    custom_prompt = Column(Text, nullable=True, comment="自定义 Prompt")
    model_id = Column(Integer, nullable=False, comment="绑定模型 ID")
    status = Column(String(20), nullable=False, default='idle', comment="状态：idle/running/error")
    current_task = Column(String(255), nullable=True, comment="当前执行任务")
    total_task = Column(Integer, nullable=False, default=0, comment="总任务数")
    finish_task = Column(Integer, nullable=False, default=0, comment="已完成任务数")
    success_rate = Column(DECIMAL(5, 2), default=0, comment="成功率")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<AIRole(id={self.id}, name='{self.name}', role_code='{self.role_code}')>"
