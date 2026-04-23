"""
认证 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from loguru import logger

from app.core.database import get_db
from app.schemas.common import ResponseBase

router = APIRouter()

# JWT 配置
SECRET_KEY = "hermes-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 认证
security = HTTPBearer()


class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证认证信息",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # TODO: 从数据库查询用户
    return {"username": username}


@router.post("/login", response_model=ResponseBase)
async def login(login_data: LoginRequest):
    """用户登录"""
    try:
        # TODO: 从数据库验证用户
        # 这里是临时实现，仅用于演示
        
        # 验证用户名密码（演示用，硬编码）
        if login_data.username == "admin" and login_data.password == "admin123":
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": login_data.username},
                expires_delta=access_token_expires
            )
            
            logger.info(f"用户登录成功：{login_data.username}")
            
            return ResponseBase(
                code="SUCCESS",
                msg="登录成功",
                data={
                    "access_token": access_token,
                    "token_type": "bearer",
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
                }
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="用户名或密码错误"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录失败：{e}")
        raise HTTPException(status_code=500, detail=f"登录失败：{str(e)}")


@router.post("/logout", response_model=ResponseBase)
async def logout(current_user: dict = Depends(get_current_user)):
    """用户登出"""
    try:
        logger.info(f"用户登出：{current_user['username']}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="登出成功"
        )
        
    except Exception as e:
        logger.error(f"登出失败：{e}")
        raise HTTPException(status_code=500, detail=f"登出失败：{str(e)}")


@router.get("/me", response_model=ResponseBase)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data={
                "username": current_user["username"],
                "role": "admin"
            }
        )
        
    except Exception as e:
        logger.error(f"获取用户信息失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取用户信息失败：{str(e)}")
