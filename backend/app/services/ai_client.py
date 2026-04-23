"""
AI 客户端 - 对接各大 AI 模型服务商
"""
import httpx
import json
from typing import Optional, Dict, Any
from loguru import logger
from app.core.config import settings


class AIClient:
    """AI 模型客户端"""
    
    def __init__(self):
        self.api_base = settings.AI_API_BASE_URL
        self.model = settings.DEFAULT_AI_MODEL
        self.timeout = 120
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        调用 AI 模型生成回复
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户输入
            max_tokens: 最大 token 数
            temperature: 温度参数
            
        Returns:
            AI 生成的文本
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if 'claude' in self.model.lower():
                    return await self._call_claude(client, system_prompt, user_prompt, max_tokens, temperature)
                elif 'gpt' in self.model.lower():
                    return await self._call_gpt(client, system_prompt, user_prompt, max_tokens, temperature)
                else:
                    # 默认使用 Claude
                    return await self._call_claude(client, system_prompt, user_prompt, max_tokens, temperature)
        except Exception as e:
            logger.error(f"AI 调用失败：{e}")
            raise
    
    async def _call_claude(
        self,
        client: httpx.AsyncClient,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """调用 Anthropic Claude API"""
        # TODO: 从数据库读取 API Key
        api_key = ""
        
        if not api_key:
            # 演示模式：返回模拟数据
            logger.warning("未配置 API Key，使用模拟数据")
            return self._generate_mock_response(user_prompt)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
            ]
        }
        
        response = await client.post(
            f"{self.api_base}/v1/messages",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Claude API 错误：{response.status_code} - {response.text}")
        
        data = response.json()
        return data["content"][0]["text"]
    
    async def _call_gpt(
        self,
        client: httpx.AsyncClient,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """调用 OpenAI GPT API"""
        # TODO: 从数据库读取 API Key
        api_key = ""
        
        if not api_key:
            logger.warning("未配置 API Key，使用模拟数据")
            return self._generate_mock_response(user_prompt)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        response = await client.post(
            f"{self.api_base}/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"GPT API 错误：{response.status_code} - {response.text}")
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def _generate_mock_response(self, user_prompt: str) -> str:
        """生成模拟响应（用于演示）"""
        return f"""【模拟响应 - 请在配置文件中添加真实的 API Key】

已收到任务：{user_prompt[:100]}...

这是一个模拟的 AI 响应。要使用真实的 AI 功能，请：

1. 在后台管理添加 AI 模型配置（API Key）
2. 或在 .env 文件中配置 AI_API_KEY

系统当前配置：
- 模型：{self.model}
- API 地址：{self.api_base}
- 最大 Token：4096

示例真实响应格式将根据具体任务类型返回结构化数据。"""


# 全局客户端实例
ai_client = AIClient()
