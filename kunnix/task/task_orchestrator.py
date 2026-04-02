#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 任务管理优化 - 任务调度器

功能：
1. 任务状态管理（pending → in_progress → completed/cancelled）
2. 跨会话任务追踪
3. 任务执行日志记录
4. 与记忆系统联动

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from task_management.task_extractor import TaskExtractor
from task_management.memory_linker import MemoryLinker
from task_management.task_summarizer import TaskSummarizer


class TaskOrchestrator:
    """任务调度器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化任务调度器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.tasks_dir = self.workspace_root / ".workbuddy" / "tasks"
        
        # 子组件
        self.extractor = TaskExtractor()
        self.linker = MemoryLinker(workspace_root=str(self.workspace_root))
        self.summarizer = TaskSummarizer(workspace_root=str(self.workspace_root))
        
        # 任务存储
        self.active_tasks_file = self.tasks_dir / "active_tasks.json"
        self.task_history_file = self.tasks_dir / "task_history.json"
        
        # 确保目录存在
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载活跃任务
        self.active_tasks = self._load_active_tasks()
    
    def _load_active_tasks(self) -> Dict:
        """加载活跃任务"""
        if self.active_tasks_file.exists():
            try:
                with open(self.active_tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_active_tasks(self):
        """保存活跃任务"""
        with open(self.active_tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.active_tasks, f, indent=2, ensure_ascii=False)
    
    def create_task(self, text: str, auto_start: bool = False) -> Dict:
        """
        创建任务
        
        Args:
            text: 任务描述文本
            auto_start: 是否自动开始任务
        
        Returns:
            Dict: 创建的任务
        """
        # 提取任务
        tasks = self.extractor.extract_tasks(text)
        
        if len(tasks) == 0:
            # 如果没有提取到结构化任务，创建默认任务
            task = {
                'id': datetime.now().strftime('%Y%m%d%H%M%S'),
                'title': text[:100],
                'description': text,
                'priority': 'P1',
                'project': self.linker.link_project(text) or 'general',
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'tags': [],
            }
        else:
            task = tasks[0]
            task['id'] = datetime.now().strftime('%Y%m%d%H%M%S')
            task['description'] = text
        
        # 关联记忆
        related_memories = self.linker.get_related_memories(text)
        if related_memories:
            task['related_projects'] = [item['project'] for item in related_memories]
        
        # 添加到活跃任务
        self.active_tasks[task['id']] = task
        self._save_active_tasks()
        
        # 如果自动开始，立即启动
        if auto_start:
            self.start_task(task['id'])
        
        return task
    
    def start_task(self, task_id: str) -> bool:
        """
        开始任务
        
        Args:
            task_id: 任务 ID
        
        Returns:
            bool: 是否成功
        """
        if task_id not in self.active_tasks:
            print(f"[TaskOrchestrator] 任务不存在：{task_id}")
            return False
        
        task = self.active_tasks[task_id]
        task['status'] = 'in_progress'
        task['started_at'] = datetime.now().isoformat()
        task['execution_log'] = []
        
        self._save_active_tasks()
        
        print(f"[TaskOrchestrator] 任务已开始：{task['title']}")
        return True
    
    def log_task_action(self, task_id: str, action: str, details: str = ""):
        """
        记录任务执行动作
        
        Args:
            task_id: 任务 ID
            action: 动作（create/update/delete/execute）
            details: 详细信息
        """
        if task_id not in self.active_tasks:
            return
        
        task = self.active_tasks[task_id]
        if 'execution_log' not in task:
            task['execution_log'] = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
        }
        
        task['execution_log'].append(log_entry)
        self._save_active_tasks()
    
    def complete_task(self, task_id: str, summary: str = "") -> Optional[str]:
        """
        完成任务并生成总结
        
        Args:
            task_id: 任务 ID
            summary: 手动总结（可选）
        
        Returns:
            Optional[str]: 任务档案路径
        """
        if task_id not in self.active_tasks:
            print(f"[TaskOrchestrator] 任务不存在：{task_id}")
            return None
        
        task = self.active_tasks[task_id]
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()
        
        # 执行日志
        execution_log = ""
        if 'execution_log' in task:
            execution_log = "\n".join([
                f"{entry['timestamp']}: {entry['action']} - {entry['details']}"
                for entry in task['execution_log']
            ])
        
        # 生成总结
        if not summary:
            summary_doc = self.summarizer.summarize_task(task, execution_log)
        else:
            summary_doc = summary
        
        # 保存档案
        archive_path = self.summarizer.save_archive(summary_doc, task_id)
        
        # 移动到历史
        if 'task_history' not in self.active_tasks:
            history = []
        else:
            history = self.active_tasks.pop('task_history', [])
        
        history.append(task)
        self.active_tasks['task_history'] = history[-100:]  # 保留最近 100 条
        
        # 保存到历史文件
        with open(self.task_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        self._save_active_tasks()
        
        print(f"[TaskOrchestrator] 任务已完成：{task['title']}")
        print(f"  档案路径：{archive_path}")
        
        return archive_path
    
    def cancel_task(self, task_id: str, reason: str = "") -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务 ID
            reason: 取消原因
        
        Returns:
            bool: 是否成功
        """
        if task_id not in self.active_tasks:
            return False
        
        task = self.active_tasks[task_id]
        task['status'] = 'cancelled'
        task['cancelled_at'] = datetime.now().isoformat()
        task['cancel_reason'] = reason
        
        self._save_active_tasks()
        
        print(f"[TaskOrchestrator] 任务已取消：{task['title']}")
        return True
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)
    
    def list_active_tasks(self, project: str = None) -> List[Dict]:
        """
        列出活跃任务
        
        Args:
            project: 项目过滤
        
        Returns:
            List[Dict]: 任务列表
        """
        tasks = []
        for task_id, task in self.active_tasks.items():
            if task_id == 'task_history':
                continue
            
            # 项目过滤
            if project and task.get('project') != project:
                continue
            
            # 只返回非完成状态
            if task.get('status') in ['pending', 'in_progress']:
                tasks.append(task)
        
        # 按优先级排序
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4}
        tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'P1'), 1))
        
        return tasks


def demo_orchestrator():
    """演示任务调度"""
    print("=" * 60)
    print("任务调度器演示")
    print("=" * 60)
    print()
    
    orchestrator = TaskOrchestrator()
    
    # 创建任务
    print("1. 创建任务...")
    task = orchestrator.create_task(
        "创建零碳园区项目申报文档，需要包含技术方案和预算",
        auto_start=True
    )
    print(f"   任务 ID: {task['id']}")
    print(f"   标题：{task['title']}")
    print(f"   项目：{task.get('project', 'N/A')}")
    print(f"   状态：{task['status']}")
    print()
    
    # 记录执行动作
    print("2. 记录执行动作...")
    orchestrator.log_task_action(task['id'], 'create', '创建申报文档框架')
    orchestrator.log_task_action(task['id'], 'write', '完成技术方案章节')
    orchestrator.log_task_action(task['id'], 'write', '完成预算章节')
    print("   已记录 3 个执行动作")
    print()
    
    # 查看任务状态
    print("3. 查看任务状态...")
    status = orchestrator.get_task_status(task['id'])
    print(f"   状态：{status['status']}")
    print(f"   执行日志：{len(status.get('execution_log', []))} 条")
    print()
    
    # 完成任务
    print("4. 完成任务...")
    archive_path = orchestrator.complete_task(task['id'])
    print(f"   档案已保存：{archive_path}")
    print()
    
    # 列出活跃任务
    print("5. 列出活跃任务...")
    active = orchestrator.list_active_tasks()
    print(f"   当前活跃任务：{len(active)} 个")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_orchestrator()
    sys.exit(0 if success else 1)
