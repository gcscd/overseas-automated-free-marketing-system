"""
数据库配置模块
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from loguru import logger

# 创建数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# 创建会话工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 创建基础模型类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """获取数据库会话依赖"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库"""
    try:
        async with engine.begin() as conn:
            # 导入所有模型以确保表被创建
            from app.models import project, ai_role, task, model, api_config, proxy, account, keyword, content, system_log
            
            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败：{e}")
        raise


async def create_db_and_tables():
    """创建数据库和表（用于开发环境）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
