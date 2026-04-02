#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 技能自动进化 - 模式提取器

功能：
1. 读取任务档案中的完成任务
2. 聚类分析相似任务
3. 识别高频工作流模式
4. 提取通用参数和变量

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class PatternExtractor:
    """模式提取器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化模式提取器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.task_archive_dir = self.workspace_root / ".workbuddy" / "tasks" / "archives"
        
        # 确保目录存在
        self.task_archive_dir.mkdir(parents=True, exist_ok=True)
        
        # 项目别名映射
        self.project_aliases = {
            '零碳园区': ['零碳', '园区', '光伏', '储能', '新能源'],
            '慢病逆转': ['健康', '慢病', '功能医学', '营养', '逆转'],
            '小说变现': ['小说', '网文', '写作', '番茄', '创作'],
            'MasterMind': ['专家大脑', '多 Agent', '系统'],
        }
    
    def load_completed_tasks(self) -> List[Dict]:
        """
        加载已完成的仼务档案
        
        Returns:
            List[Dict]: 任务列表
        """
        tasks = []
        
        if not self.task_archive_dir.exists():
            print(f"[PatternExtractor] 任务档案目录不存在：{self.task_archive_dir}")
            return tasks
        
        # 扫描所有任务档案
        for file_path in self.task_archive_dir.glob("task_*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析 frontmatter
                task_data = self._parse_frontmatter(content)
                task_data['content'] = content
                task_data['file_path'] = str(file_path)
                
                # 只处理已完成的任务
                if task_data.get('status') == 'completed':
                    tasks.append(task_data)
                    
            except Exception as e:
                print(f"[PatternExtractor] 读取任务档案失败：{str(e)}")
        
        print(f"[PatternExtractor] 加载到 {len(tasks)} 个已完成任务")
        return tasks
    
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
    
    def cluster_tasks(self, tasks: List[Dict], min_cluster_size: int = 2) -> Dict[str, List[Dict]]:
        """
        聚类分析相似任务
        
        Args:
            tasks: 任务列表
            min_cluster_size: 最小聚类大小（至少几个任务才考虑生成技能）
        
        Returns:
            Dict[str, List[Dict]]: 聚类结果 {项目名：[任务列表]}
        """
        clusters = {}
        
        for task in tasks:
            # 按项目分类
            project = task.get('project', 'general')
            
            if project not in clusters:
                clusters[project] = []
            
            clusters[project].append(task)
        
        # 过滤掉太小的聚类
        filtered_clusters = {
            project: tasks_list
            for project, tasks_list in clusters.items()
            if len(tasks_list) >= min_cluster_size
        }
        
        print(f"[PatternExtractor] 聚类结果：{len(filtered_clusters)} 个项目，共 {sum(len(v) for v in filtered_clusters.values())} 个任务")
        
        return filtered_clusters
    
    def extract_workflow_patterns(self, tasks: List[Dict]) -> Dict:
        """
        提取工作流模式
        
        Args:
            tasks: 任务列表
        
        Returns:
            Dict: 工作流模式
        """
        if len(tasks) == 0:
            return {}
        
        # 统计高频关键词
        all_keywords = []
        for task in tasks:
            # 从标题和标签中提取关键词
            title = task.get('title', '')
            tags_str = task.get('tags', '')
            
            # 简单分词（中文按字符）
            words = list(title)
            all_keywords.extend(words)
        
        # 统计词频
        keyword_freq = Counter(all_keywords)
        
        # 提取 top 关键词
        top_keywords = keyword_freq.most_common(20)
        
        # 识别共同动作
        action_keywords = ['创建', '建立', '实现', '完成', '执行', '测试', '优化', '修复', '整理', '导入']
        common_actions = [kw for kw, freq in top_keywords if kw in action_keywords and freq >= 2]
        
        # 识别共同成果物
        deliverable_keywords = ['文档', '代码', '报告', '脚本', '配置', '模板']
        common_deliverables = [kw for kw, freq in top_keywords if kw in deliverable_keywords and freq >= 2]
        
        pattern = {
            'task_count': len(tasks),
            'common_actions': common_actions,
            'common_deliverables': common_deliverables,
            'top_keywords': top_keywords[:10],
            'reusable': len(tasks) >= 2,  # 至少 2 个任务才考虑生成技能
        }
        
        return pattern
    
    def extract_skill_candidates(self, clusters: Dict[str, List[Dict]]) -> List[Dict]:
        """
        提取技能候选
        
        Args:
            clusters: 聚类结果
        
        Returns:
            List[Dict]: 技能候选列表
        """
        candidates = []
        
        for project, tasks in clusters.items():
            # 提取工作流模式
            pattern = self.extract_workflow_patterns(tasks)
            
            if pattern['reusable']:
                candidate = {
                    'project': project,
                    'task_count': pattern['task_count'],
                    'common_actions': pattern['common_actions'],
                    'common_deliverables': pattern['common_deliverables'],
                    'confidence': min(1.0, pattern['task_count'] / 5),  # 5 个任务以上置信度 1.0
                    'tasks': tasks,
                }
                candidates.append(candidate)
        
        # 按置信度排序
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"[PatternExtractor] 提取到 {len(candidates)} 个技能候选")
        
        return candidates


def demo_pattern_extractor():
    """演示模式提取"""
    print("=" * 60)
    print("模式提取器演示")
    print("=" * 60)
    print()
    
    extractor = PatternExtractor()
    
    # 加载任务
    print("1. 加载已完成任务...")
    tasks = extractor.load_completed_tasks()
    print(f"   加载到 {len(tasks)} 个任务")
    print()
    
    # 聚类分析
    print("2. 聚类分析...")
    clusters = extractor.cluster_tasks(tasks)
    for project, task_list in clusters.items():
        print(f"   {project}: {len(task_list)} 个任务")
    print()
    
    # 提取技能候选
    print("3. 提取技能候选...")
    candidates = extractor.extract_skill_candidates(clusters)
    
    if candidates:
        print(f"   找到 {len(candidates)} 个技能候选:")
        for i, candidate in enumerate(candidates, 1):
            print(f"   {i}. {candidate['project']} 项目 (置信度：{candidate['confidence']:.2f})")
            print(f"      任务数：{candidate['task_count']}")
            print(f"      共同动作：{', '.join(candidate['common_actions']) or '无'}")
    else:
        print("   暂无技能候选（任务数量不足）")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_pattern_extractor()
    sys.exit(0 if success else 1)
