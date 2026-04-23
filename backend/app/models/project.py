"""
项目数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """项目表"""
    __tablename__ = "t_project"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="项目 ID")
    name = Column(String(255), nullable=False, comment="项目名称")
    product = Column(String(255), nullable=False, comment="推广产品/服务")
    target_market = Column(String(50), nullable=False, comment="目标市场")
    core_selling_point = Column(Text, nullable=False, comment="核心卖点")
    target_keyword = Column(Text, nullable=False, comment="目标关键词")
    target_channel = Column(Text, nullable=False, comment="目标推广渠道（JSON 数组）")
    target_domain = Column(String(255), nullable=True, comment="目标域名")
    affiliate_link = Column(String(500), nullable=True, comment="联盟链接")
    status = Column(String(20), nullable=False, default='pending', comment="项目状态：pending/researching/running/finished/paused")
    progress = Column(Integer, nullable=False, default=0, comment="项目进度 0-100")
    total_task = Column(Integer, nullable=False, default=0, comment="总任务数")
    finish_task = Column(Integer, nullable=False, default=0, comment="已完成任务数")
    total_view = Column(Integer, nullable=False, default=0, comment="累计曝光量")
    total_click = Column(Integer, nullable=False, default=0, comment="累计点击量")
    total_conversion = Column(Integer, nullable=False, default=0, comment="累计转化量")
    total_commission = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment="累计佣金收入")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    deadline = Column(DateTime, nullable=True, comment="截止时间")
    research_report = Column(Text, nullable=True, comment="市场研究报告")
    remark = Column(Text, nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
