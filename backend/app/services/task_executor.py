"""
任务执行器 - 解析和处理 AI 任务结果
"""
import json
import re
from typing import Any, Dict, Optional
from loguru import logger
from datetime import datetime


class TaskExecutor:
    """任务执行器"""
    
    def __init__(self):
        self.result_handlers = {
            'market_research': self._handle_market_research,
            'content_creation': self._handle_content_creation,
            'task_planning': self._handle_task_planning,
            'data_analysis': self._handle_data_analysis,
        }
    
    def parse_result(self, response: str, task_data: Dict[str, Any]) -> str:
        """
        解析 AI 响应结果
        
        Args:
            response: AI 原始响应
            task_data: 任务数据
            
        Returns:
            处理后的结果
        """
        task_type = task_data.get('task_type', 'general')
        handler = self.result_handlers.get(task_type, self._handle_general)
        
        try:
            result = handler(response, task_data)
            logger.info(f"任务结果解析完成，类型：{task_type}")
            return result
        except Exception as e:
            logger.error(f"任务结果解析失败：{e}")
            return response
    
    def _handle_general(self, response: str, task_data: Dict) -> str:
        """通用任务处理"""
        return response
    
    def _handle_market_research(self, response: str, task_data: Dict) -> str:
        """市场调研任务处理"""
        # 尝试提取结构化数据
        result = {
            'type': 'market_research',
            'content': response,
            'timestamp': datetime.now().isoformat()
        }
        
        # 尝试解析 JSON
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_data = json.loads(json_match.group())
                result['structured_data'] = json_data
        except:
            pass
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _handle_content_creation(self, response: str, task_data: Dict) -> str:
        """内容创作任务处理"""
        result = {
            'type': 'content_creation',
            'title': self._extract_title(response),
            'content': response,
            'platform': task_data.get('platform', 'general'),
            'timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _handle_task_planning(self, response: str, task_data: Dict) -> str:
        """任务规划处理"""
        result = {
            'type': 'task_planning',
            'tasks': self._extract_tasks(response),
            'timeline': self._extract_timeline(response),
            'timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _handle_data_analysis(self, response: str, task_data: Dict) -> str:
        """数据分析任务处理"""
        result = {
            'type': 'data_analysis',
            'metrics': self._extract_metrics(response),
            'insights': response,
            'timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _extract_title(self, text: str) -> str:
        """提取标题"""
        lines = text.strip().split('\n')
        return lines[0][:100] if lines else '无标题'
    
    def _extract_tasks(self, text: str) -> list:
        """提取任务列表"""
        # 简单实现，实际应该更复杂
        return [{'description': line.strip()} for line in text.split('\n') if line.strip()][:10]
    
    def _extract_timeline(self, text: str) -> str:
        """提取时间线"""
        return "详见任务详情"
    
    def _extract_metrics(self, text: str) -> dict:
        """提取指标数据"""
        return {'raw_text': text[:500]}


# 全局执行器实例
task_executor = TaskExecutor()
