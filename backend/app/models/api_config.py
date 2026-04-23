"""
API 配置模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class APIConfig(Base):
    """API 配置表"""
    __tablename__ = "t_api_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置 ID")
    platform = Column(String(50), nullable=False, comment="平台名称")
    api_name = Column(String(100), nullable=False, comment="API 名称")
    api_key = Column(String(500), nullable=True, comment="API Key")
    api_secret = Column(String(500), nullable=True, comment="API Secret")
    access_token = Column(String(500), nullable=True, comment="访问令牌")
    refresh_token = Column(String(500), nullable=True, comment="刷新令牌")
    token_expires = Column(DateTime, nullable=True, comment="令牌过期时间")
    config_json = Column(Text, nullable=True, comment="其他配置（JSON）")
    status = Column(String(20), nullable=False, default='active', comment="状态：active/inactive")
    last_used = Column(DateTime, nullable=True, comment="最后使用时间")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<APIConfig(id={self.id}, platform='{self.platform}', api_name='{self.api_name}')>"
