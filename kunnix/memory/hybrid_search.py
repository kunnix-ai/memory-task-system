#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 混合检索系统 - 混合检索引擎

功能：
1. FTS5 全文检索（Whoosh）
2. 向量检索（LanceDB）
3. RRF 融合排序（Reciprocal Rank Fusion）
4. MMR 多样性优化（Maximal Marginal Relevance）
5. 时间衰减因子

作者：阿中
版本：v1.0.0
日期：2026-04-01
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import numpy as np

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from hybrid_search.embedding_service import EmbeddingService


class HybridSearchEngine:
    """
    混合检索引擎
    
    结合全文检索和向量检索的优势，通过 RRF 融合排序提供最优检索结果
    """
    
    def __init__(self, db_path: str = None, index_path: str = None):
        """
        初始化混合检索引擎
        
        Args:
            db_path: LanceDB 数据库路径
            index_path: Whoosh 索引路径
        """
        # 加载配置
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.db_path = db_path or config.get('db_path')
                self.index_path = index_path or config.get('index_path')
        else:
            # 默认路径
            workspace_root = Path(__file__).parent.parent
            self.db_path = db_path or str(workspace_root / ".workbuddy" / "vector_db")
            self.index_path = index_path or str(workspace_root / ".workbuddy" / "whoosh_index")
        
        # 初始化组件
        self.embedding_service = EmbeddingService()
        self.whoosh_ix = self._init_whoosh()
        self.lancedb = self._init_lancedb()
        
        # RRF 参数
        self.rrf_k = 60  # RRF 融合参数，通常设为 60
        
        print(f"[HybridSearchEngine] 初始化完成")
        print(f"  向量数据库：{self.db_path}")
        print(f"  全文索引：{self.index_path}")
    
    def _init_whoosh(self):
        """初始化 Whoosh 全文检索"""
        from whoosh.index import open_dir
        from whoosh.qparser import QueryParser
        
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Whoosh 索引不存在：{self.index_path}")
        
        ix = open_dir(self.index_path)
        print(f"  Whoosh 索引已加载")
        return ix
    
    def _init_lancedb(self):
        """初始化 LanceDB 向量检索"""
        import lancedb
        
        db = lancedb.connect(self.db_path)
        print(f"  LanceDB 数据库已连接")
        return db
    
    def search_full_text(self, query: str, limit: int = 20) -> List[Dict]:
        """
        全文检索（Whoosh）
        
        Args:
            query: 查询文本
            limit: 返回结果数量
        
        Returns:
            List[Dict]: 检索结果列表，每个结果包含 doc_id, score, metadata
        """
        from whoosh.qparser import QueryParser
        from whoosh import scoring
        
        results = []
        
        with self.whoosh_ix.searcher() as searcher:
            # 创建查询解析器
            parser = QueryParser("content", schema=self.whoosh_ix.schema)
            query_obj = parser.parse(query)
            
            # 执行检索
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
        
        print(f"  全文检索返回 {len(results)} 条结果")
        return results
    
    def search_vector(self, query: str, limit: int = 20) -> List[Dict]:
        """
        向量检索（LanceDB）
        
        Args:
            query: 查询文本
            limit: 返回结果数量
        
        Returns:
            List[Dict]: 检索结果列表
        """
        # 向量化查询
        query_vec = self.embedding_service.encode(query)
        
        results = []
        
        try:
            # 尝试打开记忆表
            table = self.lancedb.open_table("memories")
            
            # 向量检索
            search_results = table.search(query_vec).limit(limit).to_pandas()
            
            for _, row in search_results.iterrows():
                results.append({
                    'doc_id': row.get('doc_id', ''),
                    'score': 1 - row.get('_distance', 1),  # 距离转相似度
                    'vector': row.get('vector'),
                    'title': row.get('title', ''),
                    'category': row.get('category', ''),
                    'tags': row.get('tags', ''),
                    'memory_type': row.get('memory_type', ''),
                    'retrieval_method': 'vector'
                })
        except Exception as e:
            print(f"  向量检索失败：{str(e)}（可能是记忆表还未创建）")
        
        print(f"  向量检索返回 {len(results)} 条结果")
        return results
    
    def rrf_fusion(self, full_text_results: List[Dict], 
                   vector_results: List[Dict], 
                   limit: int = 20) -> List[Dict]:
        """
        RRF 融合排序（Reciprocal Rank Fusion）
        
        公式：RRF Score = Σ 1 / (k + rank_i)
        其中 k 是常数（通常 60），rank_i 是第 i 个检索结果中的排名
        
        Args:
            full_text_results: 全文检索结果
            vector_results: 向量检索结果
            limit: 返回结果数量
        
        Returns:
            List[Dict]: 融合后的结果
        """
        # 构建 doc_id -> 结果映射
        doc_map = {}
        
        # 处理全文检索结果
        for rank, result in enumerate(full_text_results, 1):
            doc_id = result['doc_id']
            if doc_id not in doc_map:
                doc_map[doc_id] = {
                    **result,
                    'rrf_score': 0,
                    'ranks': {'full_text': rank, 'vector': None}
                }
            doc_map[doc_id]['ranks']['full_text'] = rank
        
        # 处理向量检索结果
        for rank, result in enumerate(vector_results, 1):
            doc_id = result['doc_id']
            if doc_id not in doc_map:
                doc_map[doc_id] = {
                    **result,
                    'rrf_score': 0,
                    'ranks': {'full_text': None, 'vector': rank}
                }
            doc_map[doc_id]['ranks']['vector'] = rank
        
        # 计算 RRF 分数
        for doc_id, doc_data in doc_map.items():
            rrf_score = 0.0
            
            # 全文检索排名贡献
            if doc_data['ranks']['full_text'] is not None:
                rrf_score += 1.0 / (self.rrf_k + doc_data['ranks']['full_text'])
            
            # 向量检索排名贡献
            if doc_data['ranks']['vector'] is not None:
                rrf_score += 1.0 / (self.rrf_k + doc_data['ranks']['vector'])
            
            doc_data['rrf_score'] = rrf_score
        
        # 按 RRF 分数排序
        sorted_results = sorted(
            doc_map.values(),
            key=lambda x: x['rrf_score'],
            reverse=True
        )
        
        # 返回 top-k
        return sorted_results[:limit]
    
    def mmr_rerank(self, results: List[Dict], query_vec: np.ndarray,
                   lambda_param: float = 0.5, limit: int = 10) -> List[Dict]:
        """
        MMR 重排（Maximal Marginal Relevance）
        
        在相关性和多样性之间取得平衡，避免结果过于相似
        
        Args:
            results: RRF 融合后的结果
            query_vec: 查询向量
            lambda_param: 相关性 - 多样性权衡参数（0-1，越大越重视相关性）
            limit: 返回结果数量
        
        Returns:
            List[Dict]: MMR 重排后的结果
        """
        if len(results) == 0:
            return []
        
        # 提取向量
        vectors = []
        for result in results:
            if 'vector' in result and result['vector'] is not None:
                vectors.append(np.array(result['vector']))
            else:
                # 如果没有向量，现场编码（较慢）
                content = f"{result.get('title', '')} {result.get('tags', '')}"
                vec = self.embedding_service.encode(content)
                vectors.append(vec)
        
        vectors = np.array(vectors)
        
        # MMR 算法
        selected = []
        remaining = list(range(len(results)))
        
        while len(selected) < min(limit, len(results)) and len(remaining) > 0:
            best_score = -float('inf')
            best_idx = None
            
            for idx in remaining:
                # 与查询的相似度（相关性）
                query_sim = self.embedding_service.similarity(query_vec, vectors[idx])
                
                # 与已选结果的最大相似度（冗余度）
                max_sim = 0
                for sel_idx in selected:
                    sim = self.embedding_service.similarity(vectors[idx], vectors[sel_idx])
                    max_sim = max(max_sim, sim)
                
                # MMR 分数
                mmr_score = lambda_param * query_sim - (1 - lambda_param) * max_sim
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx
            
            if best_idx is not None:
                selected.append(best_idx)
                remaining.remove(best_idx)
        
        # 按 MMR 选择的顺序返回结果
        mmr_results = [results[i] for i in selected]
        
        return mmr_results
    
    def apply_time_decay(self, results: List[Dict], decay_rate: float = 0.1) -> List[Dict]:
        """
        应用时间衰减因子
        
        最近的记忆更重要，旧记忆分数会衰减
        
        Args:
            results: 检索结果
            decay_rate: 衰减率（每天）
        
        Returns:
            List[Dict]: 应用时间衰减后的结果
        """
        now = datetime.now()
        
        for result in results:
            # 获取文档时间
            created_at = result.get('created_at')
            if created_at:
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                
                # 计算时间差（天）
                days_diff = (now - created_at).days
                
                # 时间衰减因子（指数衰减）
                time_factor = np.exp(-decay_rate * days_diff)
                
                # 更新分数
                result['rrf_score'] *= time_factor
                result['time_decay_factor'] = time_factor
        
        # 重新排序
        sorted_results = sorted(
            results,
            key=lambda x: x['rrf_score'],
            reverse=True
        )
        
        return sorted_results
    
    def search(self, query: str, limit: int = 10, 
               use_mmr: bool = True, 
               use_time_decay: bool = True,
               mmr_lambda: float = 0.7) -> List[Dict]:
        """
        完整的混合检索流程
        
        Args:
            query: 查询文本
            limit: 返回结果数量
            use_mmr: 是否使用 MMR 重排
            use_time_decay: 是否应用时间衰减
            mmr_lambda: MMR 相关性参数
        
        Returns:
            List[Dict]: 最终检索结果
        """
        print(f"\n[HybridSearch] 检索查询：{query}")
        print(f"  参数：limit={limit}, mmr={use_mmr}, time_decay={use_time_decay}")
        
        # 1. 全文检索
        print("\n步骤 1: 全文检索...")
        full_text_results = self.search_full_text(query, limit=limit * 2)
        
        # 2. 向量检索
        print("\n步骤 2: 向量检索...")
        vector_results = self.search_vector(query, limit=limit * 2)
        
        # 3. RRF 融合
        print("\n步骤 3: RRF 融合排序...")
        fused_results = self.rrf_fusion(full_text_results, vector_results, limit=limit * 2)
        
        # 4. MMR 重排（可选）
        if use_mmr and len(fused_results) > 0:
            print(f"\n步骤 4: MMR 重排 (lambda={mmr_lambda})...")
            query_vec = self.embedding_service.encode(query)
            reranked_results = self.mmr_rerank(fused_results, query_vec, 
                                              lambda_param=mmr_lambda, 
                                              limit=limit)
        else:
            reranked_results = fused_results[:limit]
        
        # 5. 时间衰减（可选）
        if use_time_decay and len(reranked_results) > 0:
            print(f"\n步骤 5: 时间衰减 (decay_rate=0.1)...")
            final_results = self.apply_time_decay(reranked_results, decay_rate=0.1)
        else:
            final_results = reranked_results
        
        print(f"\n最终返回 {len(final_results)} 条结果")
        return final_results


def test_hybrid_search():
    """测试混合检索引擎"""
    print("=" * 60)
    print("测试混合检索引擎")
    print("=" * 60)
    print()
    
    try:
        # 创建引擎
        engine = HybridSearchEngine()
        print()
        
        # 测试检索
        query = "WorkBuddy 记忆系统"
        print(f"测试查询：{query}")
        results = engine.search(query, limit=5)
        
        print("\n检索结果:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('title', 'N/A')}")
            print(f"   类型：{result.get('memory_type', 'N/A')}")
            print(f"   分类：{result.get('category', 'N/A')}")
            print(f"   RRF 分数：{result.get('rrf_score', 0):.4f}")
            if 'time_decay_factor' in result:
                print(f"   时间衰减：{result['time_decay_factor']:.4f}")
        
        print("\n" + "=" * 60)
        print("混合检索引擎测试完成！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_hybrid_search()
    sys.exit(0 if success else 1)
