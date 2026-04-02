#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 任务管理优化 - 记忆关联器

功能：
1. 自动关联项目记忆（基于任务内容）
2. 加载相关记忆上下文
3. 提供记忆检索接口
4. 支持跨会话记忆追踪

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import json

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class MemoryLinker:
    """记忆关联器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化记忆关联器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.memory_dir = self.workspace_root / ".workbuddy" / "memory"
        
        # 项目记忆位置
        self.project_memory_dir = self.memory_dir / "projects"
        
        # 项目别名映射
        self.project_aliases = {
            '零碳园区': ['零碳', '园区', '光伏', '储能', '新能源'],
            '慢病逆转': ['健康', '慢病', '功能医学', '营养', '逆转'],
            '小说变现': ['小说', '网文', '写作', '番茄', '创作'],
            'MasterMind': ['专家大脑', '多 Agent', '系统'],
        }
        
        # 缓存已加载的记忆
        self.loaded_memories = {}
    
    def link_project(self, task_text: str) -> Optional[str]:
        """
        关联项目记忆
        
        Args:
            task_text: 任务文本
        
        Returns:
            Optional[str]: 关联的项目名称，无匹配返回 None
        """
        for project, aliases in self.project_aliases.items():
            # 检查项目名或别名
            if project in task_text or any(alias in task_text for alias in aliases):
                return project
        
        return None
    
    def load_project_memory(self, project_name: str) -> Optional[Dict]:
        """
        加载项目记忆
        
        Args:
            project_name: 项目名称
        
        Returns:
            Dict: 项目记忆内容，不存在返回 None
        """
        # 检查缓存
        if project_name in self.loaded_memories:
            return self.loaded_memories[project_name]
        
        # 读取项目记忆文件
        memory_file = self.project_memory_dir / f"{project_name}.md"
        
        if not memory_file.exists():
            return None
        
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML frontmatter
            memory_data = self._parse_frontmatter(content)
            memory_data['content'] = content
            memory_data['file_path'] = str(memory_file)
            
            # 缓存
            self.loaded_memories[project_name] = memory_data
            
            return memory_data
            
        except Exception as e:
            print(f"[MemoryLinker] 加载项目记忆失败：{str(e)}")
            return None
    
    def _parse_frontmatter(self, content: str) -> Dict:
        """解析 YAML frontmatter"""
        import re
        
        frontmatter = {}
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1)
            for line in yaml_content.split('\n'):
                line = line.strip()
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
        
        return frontmatter
    
    def get_related_memories(self, task_text: str, limit: int = 3) -> List[Dict]:
        """
        获取相关记忆（支持多个项目）
        
        Args:
            task_text: 任务文本
            limit: 返回数量限制
        
        Returns:
            List[Dict]: 相关记忆列表
        """
        related = []
        
        # 检测所有可能关联的项目
        for project, aliases in self.project_aliases.items():
            if project in task_text or any(alias in task_text for alias in aliases):
                memory = self.load_project_memory(project)
                if memory:
                    related.append({
                        'project': project,
                        'memory': memory,
                        'relevance': 'high'
                    })
        
        # 如果没有匹配到项目，返回通用记忆建议
        if len(related) == 0:
            # 尝试从关键词推断
            keywords = {
                '记忆': 'MasterMind',
                '技能': 'MasterMind',
                'AI': 'MasterMind',
                '申报': '零碳园区',
                '医疗': '慢病逆转',
                '创作': '小说变现',
            }
            
            for keyword, project in keywords.items():
                if keyword in task_text:
                    memory = self.load_project_memory(project)
                    if memory:
                        related.append({
                            'project': project,
                            'memory': memory,
                            'relevance': 'medium'
                        })
                        break
        
        return related[:limit]
    
    def get_memory_context(self, task_text: str) -> str:
        """
        获取记忆上下文（用于任务执行参考）
        
        Args:
            task_text: 任务文本
        
        Returns:
            str: 格式化的记忆上下文
        """
        related = self.get_related_memories(task_text)
        
        if len(related) == 0:
            return ""
        
        context_parts = []
        for item in related:
            project = item['project']
            memory = item['memory']
            
            context = f"\n## {project} 项目记忆\n"
            context += f"**定位**: {memory.get('定位', 'N/A')}\n"
            context += f"**目标**: {memory.get('目标', 'N/A')}\n"
            context += f"**技术栈**: {memory.get('技术栈', 'N/A')}\n"
            
            context_parts.append(context)
        
        return "\n".join(context_parts)


def demo_memory_linker():
    """演示记忆关联"""
    print("=" * 60)
    print("记忆关联器演示")
    print("=" * 60)
    print()
    
    linker = MemoryLinker()
    
    # 测试任务
    test_tasks = [
        "创建零碳园区项目申报文档",
        "优化 MasterMind 专家大脑路由性能",
        "整理慢病逆转知识库，添加新的功能医学资料",
        "修复混合检索系统的编码问题",
    ]
    
    for task in test_tasks:
        print(f"\n任务：{task}")
        print("-" * 60)
        
        # 关联项目
        project = linker.link_project(task)
        print(f"关联项目：{project or '无'}")
        
        # 获取相关记忆
        related = linker.get_related_memories(task)
        if related:
            print(f"相关记忆：{len(related)} 个")
            for item in related:
                print(f"  - {item['project']} ({item['relevance']})")
        else:
            print("无相关记忆")
        
        # 获取记忆上下文
        context = linker.get_memory_context(task)
        if context:
            print("\n记忆上下文:")
            print(context[:200] + "..." if len(context) > 200 else context)
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_memory_linker()
    sys.exit(0 if success else 1)
