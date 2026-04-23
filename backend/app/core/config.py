"""
应用配置模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/hermes.db"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False
    
    # JWT 配置
    JWT_SECRET_KEY: str = "hermes-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Hermes Agent 配置
    HERMES_AGENT_CONFIG: str = "config/agent.yaml"
    AGENT_MAX_CONCURRENT_TASKS: int = 10
    AGENT_DEFAULT_MAX_RETRY: int = 2
    
    # AI 配置
    DEFAULT_AI_MODEL: str = "claude-3-5-sonnet"
    AI_API_BASE_URL: str = "https://api.anthropic.com"
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.7
    
    # 安全配置
    ENCRYPTION_KEY: str = "32-byte-encryption-key-here!!"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/hermes.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
