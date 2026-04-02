#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 混合检索技能 - 记忆检索

功能：
1. 提供 WorkBuddy 可调用的记忆检索技能
2. 支持多种检索模式（全文、向量、混合）
3. 返回结构化检索结果
4. 集成到 WorkBuddy 技能系统

作者：阿中
版本：v1.0.0
日期：2026-04-01
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class MemorySearchSkill:
    """
    WorkBuddy 记忆检索技能
    
    使用方式：
    ```python
    from hybrid_search.memory_search_skill import MemorySearchSkill
    
    skill = MemorySearchSkill()
    results = skill.search("记忆系统", limit=10)
    ```
    """
    
    def __init__(self, mode: str = "hybrid"):
        """
        初始化技能
        
        Args:
            mode: 检索模式
                - "hybrid": 混合检索（默认，推荐）
                - "full_text": 仅全文检索
                - "vector": 仅向量检索
        """
        self.mode = mode
        self.engine = None
        
        if mode == "hybrid":
            from hybrid_search.hybrid_search import HybridSearchEngine
            self.engine = HybridSearchEngine()
            print(f"[MemorySearchSkill] 混合检索模式已初始化")
        elif mode == "full_text":
            # 仅全文检索
            from whoosh.index import open_dir
            from whoosh.qparser import QueryParser
            
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.whoosh_ix = open_dir(config['index_path'])
            print(f"[MemorySearchSkill] 全文检索模式已初始化")
        elif mode == "vector":
            # 仅向量检索
            import lancedb
            from hybrid_search.embedding_service import EmbeddingService
            
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.lancedb = lancedb.connect(config['db_path'])
            self.embedding_service = EmbeddingService()
            print(f"[MemorySearchSkill] 向量检索模式已初始化")
    
    def search(self, query: str, limit: int = 10, 
               category: str = None,
               memory_type: str = None,
               tags: List[str] = None) -> List[Dict]:
        """
        搜索记忆
        
        Args:
            query: 查询文本
            limit: 返回结果数量
            category: 分类过滤（如"人工智能"、"零碳园区"）
            memory_type: 记忆类型过滤（daily/project/long_term）
            tags: 标签过滤列表
        
        Returns:
            List[Dict]: 检索结果列表
        """
        if self.mode == "hybrid":
            # 混合检索
            results = self.engine.search(query, limit=limit)
            
        elif self.mode == "full_text":
            # 全文检索
            results = self._search_full_text(query, limit=limit)
            
        elif self.mode == "vector":
            # 向量检索
            results = self._search_vector(query, limit=limit)
        
        else:
            raise ValueError(f"未知检索模式：{self.mode}")
        
        # 应用过滤器
        if category or memory_type or tags:
            results = self._apply_filters(results, category, memory_type, tags)
        
        # 限制返回数量
        return results[:limit]
    
    def _search_full_text(self, query: str, limit: int = 10) -> List[Dict]:
        """全文检索实现"""
        from whoosh.qparser import QueryParser
        from whoosh import scoring
        
        results = []
        
        with self.whoosh_ix.searcher() as searcher:
            parser = QueryParser("content", schema=self.whoosh_ix.schema)
            query_obj = parser.parse(query)
            
            search_results = searcher.search(query_obj, limit=limit)
            
            for hit in search_results:
                results.append({
                    'doc_id': hit['doc_id'],
                    'score': hit.score,
                    'title': hit.get('title', ''),
                    'category': hit.get('category', ''),
                    'tags': hit.get('tags', ''),
                    'memory_type': hit.get('memory_type', ''),
                    'retrieval_method': 'full_text'
                })
        
        return results
    
    def _search_vector(self, query: str, limit: int = 10) -> List[Dict]:
        """向量检索实现"""
        # 向量化查询
        query_vec = self.embedding_service.encode(query)
        
        results = []
        
        try:
            table = self.lancedb.open_table("memories")
            search_results = table.search(query_vec).limit(limit).to_pandas()
            
            for _, row in search_results.iterrows():
                results.append({
                    'doc_id': row.get('doc_id', ''),
                    'score': 1 - row.get('_distance', 1),
                    'title': row.get('title', ''),
                    'category': row.get('category', ''),
                    'tags': row.get('tags', ''),
                    'memory_type': row.get('memory_type', ''),
                    'retrieval_method': 'vector'
                })
        except Exception as e:
            print(f"  向量检索失败：{str(e)}")
        
        return results
    
    def _apply_filters(self, results: List[Dict], 
                       category: str = None,
                       memory_type: str = None,
                       tags: List[str] = None) -> List[Dict]:
        """
        应用过滤器
        
        Args:
            results: 检索结果
            category: 分类过滤
            memory_type: 类型过滤
            tags: 标签过滤
        
        Returns:
            List[Dict]: 过滤后的结果
        """
        filtered = []
        
        for result in results:
            # 分类过滤
            if category and result.get('category') != category:
                continue
            
            # 记忆类型过滤
            if memory_type and result.get('memory_type') != memory_type:
                continue
            
            # 标签过滤
            if tags:
                result_tags = result.get('tags', '').split()
                if not any(tag in result_tags for tag in tags):
                    continue
            
            filtered.append(result)
        
        return filtered
    
    def search_and_format(self, query: str, limit: int = 5) -> str:
        """
        搜索并格式化输出（适合直接展示给用户）
        
        Args:
            query: 查询文本
            limit: 返回结果数量
        
        Returns:
            str: 格式化的检索结果
        """
        results = self.search(query, limit=limit)
        
        if len(results) == 0:
            return "未找到相关记忆"
        
        output_lines = [
            f"🔍 找到 {len(results)} 条相关记忆：",
            ""
        ]
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            category = result.get('category', 'N/A')
            memory_type = result.get('memory_type', 'N/A')
            score = result.get('score', 0)
            rrf_score = result.get('rrf_score', 0)
            
            # 格式化输出
            output_lines.append(f"{i}. **{title}**")
            output_lines.append(f"   - 分类：{category}")
            output_lines.append(f"   - 类型：{memory_type}")
            output_lines.append(f"   - 相关度：{score:.2%}" if 'score' in result else f"   - RRF 分数：{rrf_score:.4f}")
            output_lines.append("")
        
        return "\n".join(output_lines)


def demo_search():
    """演示搜索功能"""
    print("=" * 60)
    print("WorkBuddy 记忆检索技能演示")
    print("=" * 60)
    print()
    
    # 创建技能
    skill = MemorySearchSkill(mode="hybrid")
    print()
    
    # 测试查询
    test_queries = [
        "记忆系统",
        "零碳园区",
        "技能进化",
        "WorkBuddy",
    ]
    
    for query in test_queries:
        print(f"\n查询：{query}")
        print("-" * 60)
        
        results = skill.search(query, limit=3)
        
        if len(results) == 0:
            print("  未找到结果（可能是数据库为空）")
        else:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result.get('title', 'N/A')}")
                print(f"     分类：{result.get('category', 'N/A')}")
                print(f"     分数：{result.get('rrf_score', result.get('score', 0)):.4f}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_search()
    sys.exit(0 if success else 1)
