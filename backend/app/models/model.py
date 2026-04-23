"""
AI 模型数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Time
from sqlalchemy.sql import func
from app.core.database import Base


class AIModel(Base):
    """AI 模型表"""
    __tablename__ = "t_model"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="模型 ID")
    model_code = Column(String(50), nullable=False, unique=True, comment="模型编码")
    model_name = Column(String(100), nullable=False, comment="模型名称")
    provider = Column(String(50), nullable=False, comment="提供商")
    api_key = Column(String(500), nullable=False, comment="API 密钥")
    api_base_url = Column(String(255), nullable=True, comment="API 基础 URL")
    max_tokens = Column(Integer, default=4096, comment="最大 tokens")
    temperature = Column(DECIMAL(3, 2), default=0.70, comment="温度参数")
    status = Column(String(20), nullable=False, default='active', comment="状态：active/inactive")
    daily_limit = Column(Integer, nullable=True, comment="每日调用限制")
    used_today = Column(Integer, default=0, comment="今日已使用次数")
    reset_time = Column(Time, default=func.time('00:00:00'), comment="重置时间")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, model_name='{self.model_name}', provider='{self.provider}')>"
