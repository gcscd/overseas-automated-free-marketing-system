"""
Hermes Agent 核心引擎
负责 AI 任务调度、执行和结果管理
"""
import asyncio
import json
from datetime import datetime
from typing import Optional, Dict, Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.services.ai_client import AIClient
from app.services.task_executor import TaskExecutor


class HermesAgent:
    """Hermes AI Agent 核心类"""
    
    def __init__(self):
        self.ai_client = AIClient()
        self.task_executor = TaskExecutor()
        self.running_tasks: Dict[int, Any] = {}
        logger.info("Hermes Agent 初始化完成")
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Optional[str]:
        """
        执行单个 AI 任务
        
        Args:
            task_data: 任务数据，包含 role_name, task_name, content, prompt 等
            
        Returns:
            执行结果或 None
        """
        task_id = task_data.get('id')
        role_name = task_data.get('role_name', 'AI Assistant')
        task_name = task_data.get('task_name', 'Unknown Task')
        content = task_data.get('content', '')
        prompt = task_data.get('prompt', '')
        
        logger.info(f"开始执行任务 {task_id}: {task_name} (角色：{role_name})")
        
        try:
            # 标记任务为运行中
            self.running_tasks[task_id] = {
                'start_time': datetime.now(),
                'status': 'running',
                'progress': 10
            }
            
            # 构建系统提示词
            system_prompt = f"""你是一位专业的{role_name}，{prompt}

请根据以下任务要求执行任务：
{content}

请以专业、详细的方式完成任务，并输出结构化的结果。"""
            
            # 调用 AI 模型
            logger.info(f"调用 AI 模型执行任务...")
            self.running_tasks[task_id]['progress'] = 50
            
            response = await self.ai_client.generate(
                system_prompt=system_prompt,
                user_prompt=content,
                max_tokens=settings.AI_MAX_TOKENS,
                temperature=settings.AI_TEMPERATURE
            )
            
            self.running_tasks[task_id]['progress'] = 80
            
            # 处理结果
            result = self.task_executor.parse_result(response, task_data)
            
            self.running_tasks[task_id]['progress'] = 100
            self.running_tasks[task_id]['status'] = 'finished'
            
            logger.info(f"任务 {task_id} 执行完成")
            
            return result
            
        except Exception as e:
            logger.error(f"任务 {task_id} 执行失败：{e}")
            self.running_tasks[task_id]['status'] = 'failed'
            self.running_tasks[task_id]['error'] = str(e)
            raise e
        finally:
            # 清理运行中任务记录（延迟清理，保留一段时间用于查询）
            asyncio.create_task(self._cleanup_task(task_id))
    
    async def _cleanup_task(self, task_id: int, delay: int = 300):
        """延迟清理任务记录"""
        await asyncio.sleep(delay)
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True
    )
    async def execute_with_retry(self, task_data: Dict[str, Any]) -> Optional[str]:
        """带重试机制的任务执行"""
        return await self.execute_task(task_data)
    
    def get_task_progress(self, task_id: int) -> Optional[Dict]:
        """获取任务进度"""
        return self.running_tasks.get(task_id)
    
    async def batch_execute(self, tasks: list) -> list:
        """批量执行任务（并发控制）"""
        semaphore = asyncio.Semaphore(settings.AGENT_MAX_CONCURRENT_TASKS)
        
        async def execute_with_semaphore(task):
            async with semaphore:
                return await self.execute_task(task)
        
        results = await asyncio.gather(
            *[execute_with_semaphore(task) for task in tasks],
            return_exceptions=True
        )
        
        return results


# 全局 Agent 实例
agent = HermesAgent()
