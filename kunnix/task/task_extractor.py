#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 任务管理优化 - 任务提取器

功能：
1. 从对话中自动提取待办事项
2. 识别任务优先级（P0-P4）
3. 关联项目记忆（别名映射）
4. 生成结构化任务档案

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import re
from typing import List, Dict, Optional
from datetime import datetime


class TaskExtractor:
    """任务提取器"""
    
    def __init__(self):
        """初始化任务提取器"""
        # 任务优先级关键词
        self.priority_keywords = {
            'P0': ['紧急', '重要', '必须', '今天', '立即', '马上', '高优先级'],
            'P1': ['待办', '需要', '应该', '计划', '安排', '中优先级'],
            'P2': ['可选', '有空', '低优先级', '后续', '之后'],
            'P3': ['了解', '参考', '阅读', '学习'],
            'P4': ['记录', '备注', '标记'],
        }
        
        # 项目别名映射（从 MEMORY.md 读取）
        self.project_aliases = {
            '零碳园区': ['零碳', '园区', '光伏', '储能', '新能源'],
            '慢病逆转': ['健康', '慢病', '功能医学', '营养', '逆转'],
            '小说变现': ['小说', '网文', '写作', '番茄', '创作'],
            'MasterMind': ['专家大脑', '多 Agent', '系统'],
        }
        
        # 任务动作关键词
        self.action_keywords = [
            '创建', '建立', '实现', '完成', '执行', '实施',
            '测试', '验证', '检查', '审查',
            '优化', '改进', '修复', '解决',
            '研究', '分析', '调研', '评估',
            '编写', '撰写', '记录', '整理',
            '导入', '导出', '备份', '恢复',
            '安装', '配置', '部署', '发布',
            '学习', '阅读', '了解', '掌握',
        ]
    
    def extract_tasks(self, text: str) -> List[Dict]:
        """
        从文本中提取任务
        
        Args:
            text: 输入文本（对话内容）
        
        Returns:
            List[Dict]: 任务列表
        """
        tasks = []
        
        # 1. 识别任务行（包含动作关键词或待办标记）
        task_patterns = [
            r'[-*•]\s*\[([ x])\]\s*(.+)',  # Markdown 待办：- [ ] 或 - [x]
            r'^\s*待办 [：:]\s*(.+)',  # "待办：xxx"
            r'^\s*需要\s+(.+)',  # "需要 xxx"
            r'^\s*要\s+(.+)',  # "要 xxx"
            r'^\s*计划\s+(.+)',  # "计划 xxx"
            r'^\s*准备\s+(.+)',  # "准备 xxx"
        ]
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否包含任务动作
            has_action = any(action in line for action in self.action_keywords)
            
            for pattern in task_patterns:
                match = re.search(pattern, line, re.MULTILINE)
                if match or (has_action and self._is_task_like(line)):
                    task_text = match.group(2) if match else line
                    task = self._parse_task(task_text)
                    if task:
                        tasks.append(task)
                    break
        
        return tasks
    
    def _is_task_like(self, text: str) -> bool:
        """判断文本是否像任务"""
        # 包含动作关键词
        has_action = any(action in text for action in self.action_keywords)
        
        # 不是疑问句
        is_question = '?' in text or '？' in text
        
        # 不是纯描述
        is_description = any(
            word in text 
            for word in ['是', '有', '在', '的', '了', '过']
        )
        
        return has_action and not is_question and not is_description
    
    def _parse_task(self, text: str) -> Optional[Dict]:
        """
        解析单个任务文本
        
        Args:
            text: 任务文本
        
        Returns:
            Dict: 结构化任务
        """
        task = {
            'title': text.strip(),
            'priority': self._detect_priority(text),
            'project': self._detect_project(text),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'tags': [],
        }
        
        # 提取标签
        task['tags'] = self._extract_tags(text)
        
        return task
    
    def _detect_priority(self, text: str) -> str:
        """检测任务优先级"""
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in text for keyword in keywords):
                return priority
        return 'P1'  # 默认中优先级
    
    def _detect_project(self, text: str) -> str:
        """检测关联项目"""
        for project, aliases in self.project_aliases.items():
            # 检查项目名或别名
            if project in text or any(alias in text for alias in aliases):
                return project
        return 'general'  # 默认通用项目
    
    def _extract_tags(self, text: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 提取 #标签
        hashtag_pattern = r'#(\w+)'
        matches = re.findall(hashtag_pattern, text)
        tags.extend([f'#{tag}' for tag in matches])
        
        # 提取关键词作为标签
        keywords = ['优化', '修复', '创建', '测试', '文档', '性能', '功能']
        for keyword in keywords:
            if keyword in text and f'#{keyword}' not in tags:
                tags.append(f'#{keyword}')
        
        return tags[:5]  # 限制最多 5 个标签


def demo_extraction():
    """演示任务提取"""
    print("=" * 60)
    print("任务提取器演示")
    print("=" * 60)
    print()
    
    extractor = TaskExtractor()
    
    # 测试文本
    test_texts = [
        """
        今天需要完成以下任务：
        - [ ] 修复 performance_test.py 的编码问题（紧急）
        - [ ] 导入全部记忆文件
        - [x] 已完成的任务
        计划下周优化混合检索系统
        需要研究 LanceDB 的性能优化
        """,
        """
        待办事项：
        1. 创建零碳园区项目申报文档
        2. 测试 MasterMind 专家大脑路由
        3. 整理慢病逆转知识库
        高优先级：今天必须完成性能测试
        """,
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n测试文本 {i}:")
        print("-" * 60)
        
        tasks = extractor.extract_tasks(text)
        
        print(f"提取到 {len(tasks)} 个任务:\n")
        for j, task in enumerate(tasks, 1):
            print(f"  {j}. {task['title']}")
            print(f"     优先级：{task['priority']}")
            print(f"     项目：{task['project']}")
            print(f"     标签：{', '.join(task['tags'])}")
            print()
    
    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_extraction()
    import sys
    sys.exit(0 if success else 1)
