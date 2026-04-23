"""
Pydantic Schemas - 通用响应格式
"""
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ResponseBase(BaseModel):
    """通用响应基类"""
    code: str = Field(default="SUCCESS", description="响应码")
    msg: str = Field(default="成功", description="响应消息")
    data: Optional[Any] = Field(default=None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class ErrorResponse(BaseModel):
    """错误响应"""
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    detail: Optional[Any] = Field(default=None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    path: Optional[str] = Field(default=None, description="请求路径")


# 错误码定义
ERROR_CODES = {
    "SUCCESS": "成功",
    "VALIDATION_ERROR": "参数校验失败",
    "NOT_FOUND": "资源不存在",
    "UNAUTHORIZED": "未授权",
    "FORBIDDEN": "禁止访问",
    "INTERNAL_ERROR": "服务器内部错误",
    "TASK_FAILED": "任务执行失败",
    "API_ERROR": "第三方 API 错误",
    "DATABASE_ERROR": "数据库错误",
}
