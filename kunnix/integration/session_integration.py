#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 会话流程集成

功能：
1. 会话中自动识别任务（阶段 2）
2. 会话中自动记忆检索（阶段 1）
3. 会话结束时自动总结
4. 技能自动进化触发（阶段 3）

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入阶段 1 和阶段 2 的组件
from hybrid_search.memory_search_skill import MemorySearchSkill
from task_management.task_orchestrator import TaskOrchestrator
from skill_evolution.pattern_extractor import PatternExtractor
from skill_evolution.skill_generator import SkillGenerator


class WorkBuddySessionIntegration:
    """WorkBuddy 会话流程集成器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化集成器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        
        # 阶段 1：混合检索
        self.memory_search = MemorySearchSkill(mode="hybrid")
        
        # 阶段 2：任务管理
        self.task_orchestrator = TaskOrchestrator(workspace_root=str(self.workspace_root))
        
        # 阶段 3：技能进化
        self.pattern_extractor = PatternExtractor(workspace_root=str(self.workspace_root))
        self.skill_generator = SkillGenerator(workspace_root=str(self.workspace_root))
        
        # 会话状态
        self.session_active = False
        self.session_tasks = []
        self.session_memory = []
    
    def start_session(self):
        """开始新会话"""
        self.session_active = True
        self.session_tasks = []
        self.session_memory = []
        print("[SessionIntegration] 会话已开始")
    
    def process_user_message(self, message: str) -> Dict:
        """
        处理用户消息
        
        Args:
            message: 用户消息
        
        Returns:
            Dict: 处理结果
        """
        if not self.session_active:
            self.start_session()
        
        result = {
            'tasks_created': [],
            'memories_found': [],
            'actions': [],
        }
        
        # 1. 自动识别任务
        tasks = self.task_orchestrator.extractor.extract_tasks(message)
        for task in tasks:
            # 创建任务并自动开始
            created_task = self.task_orchestrator.create_task(
                task['title'],
                auto_start=True
            )
            self.session_tasks.append(created_task)
            result['tasks_created'].append(created_task)
            result['actions'].append(f"已创建任务：{created_task['title']}")
        
        # 2. 自动记忆检索
        if any(keyword in message for keyword in ['查询', '搜索', '查找', '看看', '了解']):
            memories = self.memory_search.search(message, limit=5)
            for memory in memories:
                self.session_memory.append(memory)
                result['memories_found'].append(memory)
            
            if memories:
                result['actions'].append(f"找到 {len(memories)} 条相关记忆")
        
        # 3. 技能进化检查（每 10 条消息检查一次）
        if len(self.session_tasks) % 10 == 0 and len(self.session_tasks) > 0:
            result['actions'].append("正在检查技能进化机会...")
            # 这里可以调用 skill_evolution 逻辑
        
        return result
    
    def end_session(self) -> Dict:
        """
        结束会话并生成总结
        
        Returns:
            Dict: 会话总结
        """
        self.session_active = False
        
        summary = {
            'session_time': datetime.now().isoformat(),
            'tasks_created': len(self.session_tasks),
            'memories_found': len(self.session_memory),
            'completed_tasks': [],
            'skill_candidates': [],
        }
        
        # 自动完成进行中的任务
        for task in self.session_tasks:
            if task.get('status') == 'in_progress':
                # 自动生成总结
                archive_path = self.task_orchestrator.complete_task(task['id'])
                summary['completed_tasks'].append({
                    'task_id': task['id'],
                    'title': task['title'],
                    'archive': archive_path,
                })
        
        # 检查技能进化
        tasks = self.pattern_extractor.load_completed_tasks()
        clusters = self.pattern_extractor.cluster_tasks(tasks)
        candidates = self.pattern_extractor.extract_skill_candidates(clusters)
        
        if candidates:
            print(f"\n[SessionIntegration] 发现 {len(candidates)} 个技能进化机会:")
            for candidate in candidates:
                print(f"  - {candidate['project']} 项目 ({candidate['task_count']} 个任务)")
                
                # 自动生成技能草稿
                skill_path = self.skill_generator.generate_skill(candidate)
                summary['skill_candidates'].append({
                    'project': candidate['project'],
                    'skill_path': skill_path,
                })
        
        return summary


def demo_integration():
    """演示集成流程"""
    print("=" * 60)
    print("WorkBuddy 会话流程集成演示")
    print("=" * 60)
    print()
    
    integration = WorkBuddySessionIntegration()
    
    # 开始会话
    print("1. 开始会话...")
    integration.start_session()
    print()
    
    # 模拟用户消息
    print("2. 处理用户消息...")
    messages = [
        "今天需要完成以下任务：创建零碳园区项目申报文档",
        "查询一下记忆系统中关于 MasterMind 的资料",
        "需要优化混合检索系统的性能",
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n消息 {i}: {message}")
        result = integration.process_user_message(message)
        
        if result['tasks_created']:
            print(f"  创建任务：{len(result['tasks_created'])} 个")
            for task in result['tasks_created']:
                print(f"    - {task['title']}")
        
        if result['memories_found']:
            print(f"  找到记忆：{len(result['memories_found'])} 条")
        
        for action in result['actions']:
            print(f"  {action}")
    
    # 结束会话
    print("\n3. 结束会话...")
    summary = integration.end_session()
    
    print(f"\n会话总结:")
    print(f"  创建任务：{summary['tasks_created']} 个")
    print(f"  找到记忆：{summary['memories_found']} 条")
    print(f"  完成任务：{len(summary['completed_tasks'])} 个")
    print(f"  技能候选：{len(summary['skill_candidates'])} 个")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_integration()
    sys.exit(0 if success else 1)
