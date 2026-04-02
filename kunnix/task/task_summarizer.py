#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 任务管理优化 - 任务总结器

功能：
1. 任务完成后自动总结成果
2. 提炼关键决策和技术选型
3. 记录经验教训
4. 生成任务档案

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json


class TaskSummarizer:
    """任务总结器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化任务总结器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.task_archive_dir = self.workspace_root / ".workbuddy" / "tasks" / "archives"
        
        # 确保目录存在
        self.task_archive_dir.mkdir(parents=True, exist_ok=True)
        
        # 总结模板
        self.summary_template = """---
title: {title}
task_id: {task_id}
project: {project}
status: {status}
created_at: {created_at}
completed_at: {completed_at}
tags: {tags}
---

# 任务总结：{title}

## 📋 任务描述

{description}

## ✅ 完成内容

{completed_work}

## 🎯 关键决策

{key_decisions}

## 🛠️ 技术选型

{technical_choices}

## 📊 成果物

{deliverables}

## 💡 经验教训

{lessons_learned}

## 🔗 相关链接

{related_links}

---

**总结时间**: {summary_time}  
**总结人**: {summarizer}
"""
    
    def summarize_task(self, task: Dict, execution_log: str = "") -> str:
        """
        总结任务
        
        Args:
            task: 任务字典
            execution_log: 执行日志
        
        Returns:
            str: 总结文档（Markdown）
        """
        # 提取关键信息
        title = task.get('title', '未命名任务')
        task_id = task.get('id', datetime.now().strftime('%Y%m%d%H%M%S'))
        project = task.get('project', 'general')
        status = task.get('status', 'completed')
        created_at = task.get('created_at', datetime.now().isoformat())
        completed_at = datetime.now().isoformat()
        tags = task.get('tags', [])
        
        # 从执行日志中提取信息
        completed_work = self._extract_completed_work(execution_log)
        key_decisions = self._extract_key_decisions(execution_log)
        technical_choices = self._extract_technical_choices(execution_log)
        deliverables = self._extract_deliverables(execution_log)
        lessons_learned = self._extract_lessons_learned(execution_log)
        related_links = task.get('related_links', [])
        
        # 填充模板
        summary = self.summary_template.format(
            title=title,
            task_id=task_id,
            project=project,
            status=status,
            created_at=created_at,
            completed_at=completed_at,
            tags=', '.join(tags),
            description=task.get('description', 'N/A'),
            completed_work=completed_work,
            key_decisions=key_decisions,
            technical_choices=technical_choices,
            deliverables=deliverables,
            lessons_learned=lessons_learned,
            related_links='\n'.join(related_links) if related_links else 'N/A',
            summary_time=datetime.now().strftime('%Y-%m-%d %H:%M'),
            summarizer='阿中',
        )
        
        return summary
    
    def _extract_completed_work(self, log: str) -> str:
        """从日志中提取完成的工作"""
        if not log:
            return "任务执行日志为空"
        
        # 简单实现：返回日志前 500 字符
        lines = log.split('\n')
        completed = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['完成', '成功', '创建', '实现', '修复']):
                completed.append(f"- {line.strip()}")
        
        if not completed:
            return log[:500] + "..." if len(log) > 500 else log
        
        return '\n'.join(completed[:10])
    
    def _extract_key_decisions(self, log: str) -> str:
        """提取关键决策"""
        decisions = []
        
        # 查找决策关键词
        decision_keywords = ['决定', '选择', '采用', '使用', '放弃', '改为']
        lines = log.split('\n')
        
        for line in lines:
            if any(keyword in line for keyword in decision_keywords):
                decisions.append(f"- {line.strip()}")
        
        if not decisions:
            return "无重大决策"
        
        return '\n'.join(decisions[:5])
    
    def _extract_technical_choices(self, log: str) -> str:
        """提取技术选型"""
        tech_keywords = ['Python', 'LanceDB', 'Whoosh', 'React', 'TypeScript', 
                        'API', '数据库', '框架', '工具', '库']
        lines = log.split('\n')
        
        choices = []
        for line in lines:
            if any(keyword in line for keyword in tech_keywords):
                choices.append(f"- {line.strip()}")
        
        if not choices:
            return "无特殊技术选型"
        
        return '\n'.join(choices[:5])
    
    def _extract_deliverables(self, log: str) -> str:
        """提取成果物"""
        deliverables = []
        
        # 查找文件创建
        file_keywords = ['创建', '保存', '生成', '输出', '文件', '.py', '.md', '.json']
        lines = log.split('\n')
        
        for line in lines:
            if any(keyword in line for keyword in file_keywords):
                deliverables.append(f"- {line.strip()}")
        
        if not deliverables:
            return "无明确成果物"
        
        return '\n'.join(deliverables[:10])
    
    def _extract_lessons_learned(self, log: str) -> str:
        """提取经验教训"""
        lessons = []
        
        # 查找经验关键词
        lesson_keywords = ['注意', '问题', '错误', '修复', '优化', '改进', '建议']
        lines = log.split('\n')
        
        for line in lines:
            if any(keyword in line for keyword in lesson_keywords):
                lessons.append(f"- {line.strip()}")
        
        if not lessons:
            return "待总结"
        
        return '\n'.join(lessons[:5])
    
    def save_archive(self, summary: str, task_id: str = None) -> str:
        """
        保存任务档案
        
        Args:
            summary: 总结文档
            task_id: 任务 ID
        
        Returns:
            str: 保存的文件路径
        """
        if not task_id:
            task_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 生成文件名
        filename = f"task_{task_id}.md"
        filepath = self.task_archive_dir / filename
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return str(filepath)


def demo_summarizer():
    """演示任务总结"""
    print("=" * 60)
    print("任务总结器演示")
    print("=" * 60)
    print()
    
    summarizer = TaskSummarizer()
    
    # 模拟任务
    task = {
        'id': 'test_001',
        'title': '修复 performance_test.py 的 Windows 编码问题',
        'project': 'MasterMind',
        'description': '解决性能测试脚本在 Windows PowerShell 中的 emoji 编码问题',
        'tags': ['#修复', '#编码', '#Windows', '#测试'],
        'status': 'completed',
    }
    
    # 模拟执行日志
    execution_log = """
    1. 创建 fix_encoding.py 脚本
    2. 替换所有 emoji 为文本标记
    3. 运行性能测试，成功通过
    4. 注意：Windows 需要使用 UTF-8 编码
    5. 问题已解决，测试通过
    6. 创建了 README.md 文档
    7. 保存到 .workbuddy/hybrid_search/ 目录
    """
    
    # 生成总结
    print("生成任务总结...\n")
    summary = summarizer.summarize_task(task, execution_log)
    
    print(summary)
    
    # 保存档案
    print("\n" + "=" * 60)
    filepath = summarizer.save_archive(summary, 'test_001')
    print(f"任务档案已保存：{filepath}")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_summarizer()
    sys.exit(0 if success else 1)
