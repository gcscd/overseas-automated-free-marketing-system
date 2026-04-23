"""
Pydantic Schemas - 项目相关
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProjectBase(BaseModel):
    """项目基础 Schema"""
    name: str = Field(..., description="项目名称", min_length=1, max_length=255)
    product: str = Field(..., description="推广产品/服务", min_length=1, max_length=255)
    target_market: str = Field(..., description="目标市场", min_length=1, max_length=50)
    core_selling_point: str = Field(..., description="核心卖点")
    target_keyword: str = Field(..., description="目标关键词")
    target_channel: str = Field(..., description="目标推广渠道（JSON 数组）")
    target_domain: Optional[str] = Field(None, description="目标域名", max_length=255)
    affiliate_link: Optional[str] = Field(None, description="联盟链接", max_length=500)
    deadline: Optional[datetime] = Field(None, description="截止时间")
    remark: Optional[str] = Field(None, description="备注")


class ProjectCreate(ProjectBase):
    """创建项目请求"""
    pass


class ProjectUpdate(BaseModel):
    """更新项目请求"""
    name: Optional[str] = Field(None, description="项目名称", min_length=1, max_length=255)
    product: Optional[str] = Field(None, description="推广产品/服务")
    target_market: Optional[str] = Field(None, description="目标市场")
    core_selling_point: Optional[str] = Field(None, description="核心卖点")
    target_keyword: Optional[str] = Field(None, description="目标关键词")
    target_channel: Optional[str] = Field(None, description="目标推广渠道")
    target_domain: Optional[str] = Field(None, description="目标域名")
    affiliate_link: Optional[str] = Field(None, description="联盟链接")
    status: Optional[str] = Field(None, description="项目状态")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    remark: Optional[str] = Field(None, description="备注")


class ProjectResponse(ProjectBase):
    """项目响应"""
    id: int
    status: str
    progress: int
    total_task: int
    finish_task: int
    total_view: int
    total_click: int
    total_conversion: int
    total_commission: Decimal
    create_time: datetime
    research_report: Optional[str] = None
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    code: str = "SUCCESS"
    msg: str = "成功"
    data: List[ProjectResponse]
    total: int = 0
