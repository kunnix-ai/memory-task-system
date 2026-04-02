#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合检索系统简单功能演示
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hybrid_search.memory_search_skill import MemorySearchSkill

print("=" * 60)
print("WorkBuddy 混合检索系统 - 功能演示")
print("=" * 60)
print()

# 创建技能
print("初始化混合检索技能...")
skill = MemorySearchSkill(mode="hybrid")
print()

# 测试查询
test_queries = [
    "记忆系统",
    "零碳园区",
    "MasterMind",
]

for query in test_queries:
    print(f"查询：{query}")
    print("-" * 60)
    
    results = skill.search(query, limit=5)
    
    if len(results) == 0:
        print("  未找到结果")
    else:
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            category = result.get('category', 'N/A')
            score = result.get('rrf_score', result.get('score', 0))
            print(f"  {i}. {title}")
            print(f"     分类：{category}")
            print(f"     分数：{score:.4f}")
    
    print()

print("=" * 60)
print("演示完成！混合检索系统运行正常")
print("=" * 60)
