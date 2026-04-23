"""
其他数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Proxy(Base):
    """代理池表"""
    __tablename__ = "t_proxy"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy_name = Column(String(100), nullable=False)
    proxy_type = Column(String(20), default='http')
    ip_address = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(100))
    password = Column(String(100))
    country = Column(String(50))
    city = Column(String(50))
    status = Column(String(20), default='active')
    health_status = Column(String(20), default='unknown')
    last_check = Column(DateTime)
    response_time = Column(Integer)
    success_rate = Column(Integer)
    total_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Account(Base):
    """账号表"""
    __tablename__ = "t_account"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(50), nullable=False)
    account_name = Column(String(100), nullable=False)
    account_email = Column(String(255))
    username = Column(String(100))
    encrypted_password = Column(String(500))
    cookie_data = Column(Text)
    status = Column(String(20), default='active')
    health_status = Column(String(20), default='unknown')
    proxy_id = Column(Integer)
    last_login = Column(DateTime)
    last_post = Column(DateTime)
    daily_post_count = Column(Integer, default=0)
    total_post_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    risk_level = Column(String(20), default='low')
    create_time = Column(DateTime, server_default=func.now())


class Keyword(Base):
    """关键词监控表"""
    __tablename__ = "t_keyword"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("t_project.id"))
    keyword = Column(String(255), nullable=False)
    search_volume = Column(Integer)
    competition = Column(String(20))
    current_rank = Column(Integer)
    best_rank = Column(Integer)
    target_rank = Column(Integer)
    status = Column(String(20), default='tracking')
    last_check = Column(DateTime)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Content(Base):
    """内容库表"""
    __tablename__ = "t_content"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("t_project.id"))
    title = Column(String(500), nullable=False)
    content_type = Column(String(50))
    platform = Column(String(50))
    content_text = Column(Text)
    media_urls = Column(Text)
    status = Column(String(20), default='draft')
    publish_time = Column(DateTime)
    view_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class SystemLog(Base):
    """系统日志表"""
    __tablename__ = "t_system_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_level = Column(String(20))
    module = Column(String(100))
    action = Column(String(255))
    user_id = Column(Integer)
    request_data = Column(Text)
    response_data = Column(Text)
    ip_address = Column(String(50))
    create_time = Column(DateTime, server_default=func.now())
