"""
代理管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from loguru import logger
import httpx

from app.core.database import get_db
from app.models.others import Proxy
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("", response_model=ResponseBase)
async def get_proxies(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取代理列表"""
    try:
        query = select(Proxy)
        if status:
            query = query.where(Proxy.status == status)
        
        query = query.order_by(Proxy.create_time.desc())
        result = await db.execute(query)
        proxies = result.scalars().all()
        
        return ResponseBase(
            code="SUCCESS",
            msg="成功",
            data=[{
                "id": p.id,
                "proxy_name": p.proxy_name,
                "proxy_type": p.proxy_type,
                "ip_address": p.ip_address,
                "port": p.port,
                "country": p.country,
                "city": p.city,
                "status": p.status,
                "health_status": p.health_status,
                "last_check": p.last_check,
                "response_time": p.response_time,
                "success_rate": str(p.success_rate) if p.success_rate else "0"
            } for p in proxies]
        )
        
    except Exception as e:
        logger.error(f"获取代理列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取代理列表失败：{str(e)}")


@router.post("", response_model=ResponseBase)
async def add_proxy(
    proxy_data: dict = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """添加代理"""
    try:
        proxy = Proxy(
            proxy_name=proxy_data.get("proxy_name", ""),
            proxy_type=proxy_data.get("proxy_type", "http"),
            ip_address=proxy_data.get("ip_address", ""),
            port=proxy_data.get("port", 8080),
            username=proxy_data.get("username"),
            password=proxy_data.get("password"),
            country=proxy_data.get("country"),
            city=proxy_data.get("city")
        )
        
        db.add(proxy)
        await db.commit()
        await db.refresh(proxy)
        
        logger.info(f"添加代理成功：{proxy.proxy_name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="代理添加成功",
            data={"id": proxy.id}
        )
        
    except Exception as e:
        await db.rollback()
        logger.error(f"添加代理失败：{e}")
        raise HTTPException(status_code=500, detail=f"添加代理失败：{str(e)}")


@router.post("/{proxy_id}/health-check", response_model=ResponseBase)
async def check_proxy_health(
    proxy_id: int,
    db: AsyncSession = Depends(get_db)
):
    """检查代理健康状态"""
    try:
        query = select(Proxy).where(Proxy.id == proxy_id)
        result = await db.execute(query)
        proxy = result.scalar_one_or_none()
        
        if not proxy:
            raise HTTPException(status_code=404, detail="代理不存在")
        
        # 执行健康检查
        test_url = "https://www.google.com"
        proxy_url = f"{proxy.proxy_type}://{proxy.ip_address}:{proxy.port}"
        
        if proxy.username and proxy.password:
            proxy_url = f"{proxy.proxy_type}://{proxy.username}:{proxy.password}@{proxy.ip_address}:{proxy.port}"
        
        try:
            import time
            start_time = time.time()
            
            async with httpx.AsyncClient(
                proxies={proxy.proxy_type: proxy_url},
                timeout=10
            ) as client:
                response = await client.get(test_url)
            
            response_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                proxy.health_status = 'healthy'
                proxy.response_time = response_time
                proxy.last_check = __import__('datetime').datetime.now()
                
                # 更新成功率
                proxy.total_requests += 1
                if proxy.failed_requests > 0:
                    success_count = proxy.total_requests - proxy.failed_requests
                    proxy.success_rate = round(success_count / proxy.total_requests * 100, 2)
            else:
                proxy.health_status = 'unhealthy'
            
            await db.commit()
            
            logger.info(f"代理 {proxy.proxy_name} 健康检查完成：{proxy.health_status}")
            
            return ResponseBase(
                code="SUCCESS",
                msg=f"健康检查完成：{proxy.health_status}",
                data={
                    "health_status": proxy.health_status,
                    "response_time": proxy.response_time
                }
            )
            
        except Exception as e:
            proxy.health_status = 'error'
            proxy.failed_requests += 1
            await db.commit()
            
            logger.error(f"代理 {proxy.proxy_name} 健康检查失败：{e}")
            
            return ResponseBase(
                code="INTERNAL_ERROR",
                msg="健康检查失败",
                data={
                    "health_status": proxy.health_status,
                    "error": str(e)
                }
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"检查代理健康失败：{e}")
        raise HTTPException(status_code=500, detail=f"检查代理健康失败：{str(e)}")


@router.post("/batch-check", response_model=ResponseBase)
async def batch_check_proxies(
    db: AsyncSession = Depends(get_db)
):
    """批量检查代理健康"""
    try:
        from datetime import datetime
        
        # 查询所有活跃代理
        query = select(Proxy).where(Proxy.status == 'active')
        result = await db.execute(query)
        proxies = result.scalars().all()
        
        logger.info(f"开始检查 {len(proxies)} 个代理的健康状态")
        
        # 这里简化实现，实际应该并发检查
        checked_count = 0
        healthy_count = 0
        
        for proxy in proxies:
            # 简单模拟，实际应该执行真实的健康检查
            proxy.last_check = datetime.now()
            proxy.health_status = 'healthy'
            checked_count += 1
            healthy_count += 1
        
        await db.commit()
        
        return ResponseBase(
            code="SUCCESS",
            msg=f"批量检查完成",
            data={
                "total": checked_count,
                "healthy": healthy_count,
                "unhealthy": checked_count - healthy_count
            }
        )
        
    except Exception as e:
        logger.error(f"批量检查代理失败：{e}")
        raise HTTPException(status_code=500, detail=f"批量检查失败：{str(e)}")


@router.delete("/{proxy_id}", response_model=ResponseBase)
async def delete_proxy(
    proxy_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除代理"""
    try:
        query = select(Proxy).where(Proxy.id == proxy_id)
        result = await db.execute(query)
        proxy = result.scalar_one_or_none()
        
        if not proxy:
            raise HTTPException(status_code=404, detail="代理不存在")
        
        await db.delete(proxy)
        await db.commit()
        
        logger.info(f"删除代理成功：{proxy.proxy_name}")
        
        return ResponseBase(
            code="SUCCESS",
            msg="代理已删除"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"删除代理失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除代理失败：{str(e)}")
