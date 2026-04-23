"""
Hermes Marketing System - Backend Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.core.config import settings
from app.core.database import init_db
from app.core.agent import agent
from app.services.scheduler import scheduler
from app.api import projects, roles, tasks, stats, system, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    logger.info("正在初始化数据库...")
    await init_db()
    
    logger.info("正在启动任务调度器...")
    scheduler.start()
    
    logger.info("Hermes Agent 系统启动成功!")
    
    yield
    
    # 关闭时清理
    logger.info("正在关闭 Hermes Agent 系统...")
    scheduler.stop()
    await agent.ai_client.close()


# 创建 FastAPI 应用
app = FastAPI(
    title="Hermes Marketing System",
    description="海外全自动免费营销系统 API",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(projects.router, prefix="/api/projects", tags=["项目管理"])
app.include_router(roles.router, prefix="/api/roles", tags=["AI 角色"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务管理"])
app.include_router(stats.router, prefix="/api/stats", tags=["数据统计"])
app.include_router(system.router, prefix="/api/system", tags=["系统管理"])
app.include_router(proxies.router, prefix="/api/proxies", tags=["代理管理"])


@app.get("/")
async def root():
    """健康检查接口"""
    return {
        "code": "SUCCESS",
        "msg": "Hermes Marketing System 运行正常",
        "data": {
            "version": "1.0.0",
            "status": "running",
            "agent": "ready",
            "scheduler": "running"
        }
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "code": "SUCCESS",
        "msg": "服务正常",
        "data": {
            "status": "healthy",
            "components": {
                "api": "ok",
                "database": "ok",
                "agent": "ok",
                "scheduler": "running"
            }
        }
    }
