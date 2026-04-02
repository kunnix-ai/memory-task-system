#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 混合检索系统 - 数据库初始化脚本

功能：
1. 创建 LanceDB 向量数据库
2. 创建 Whoosh 全文检索索引
3. 初始化记忆数据表结构

作者：阿中
版本：v1.0.0
日期：2026-04-01
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# 设置控制台输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def init_lancedb(db_path: str):
    """
    初始化 LanceDB 向量数据库
    
    Args:
        db_path: 数据库路径
    """
    import lancedb
    
    print(f"📦 正在初始化 LanceDB 向量数据库...")
    print(f"   路径：{db_path}")
    
    # 创建数据库连接
    db = lancedb.connect(db_path)
    
    # 定义记忆表 schema
    # 注意：实际 schema 在首次创建表时定义
    print("   ✅ LanceDB 初始化完成")
    
    return db


def init_whoosh_index(index_path: str):
    """
    初始化 Whoosh 全文检索索引
    
    Args:
        index_path: 索引路径
    
    Returns:
        IndexWriter: 索引写入器
    """
    from whoosh.index import create_in
    from whoosh.fields import Schema, TEXT, ID, DATETIME, NGRAM
    from whoosh.analysis import SimpleAnalyzer
    
    print(f"📚 正在初始化 Whoosh 全文检索索引...")
    print(f"   路径：{index_path}")
    
    # 如果索引已存在，删除重建
    if os.path.exists(index_path):
        print(f"   ⚠️  检测到已有索引，正在清理...")
        shutil.rmtree(index_path)
    
    # 创建目录
    os.makedirs(index_path, exist_ok=True)
    
    # 定义检索 schema
    schema = Schema(
        # 唯一标识
        doc_id=ID(stored=True, unique=True),
        
        # 文档元数据
        title=TEXT(stored=True, analyzer=SimpleAnalyzer()),  # 标题
        content=TEXT(stored=False, analyzer=SimpleAnalyzer()),  # 正文内容
        category=ID(stored=True),  # 分类（人工智能、零碳园区等）
        tags=TEXT(stored=True),  # 标签（空格分隔）
        
        # 时间信息
        created_at=DATETIME(stored=True),
        updated_at=DATETIME(stored=True),
        
        # 记忆类型
        memory_type=ID(stored=True),  # daily, project, long_term
        
        # 全文检索优化
        # NGRAM 用于部分匹配（如搜索"记忆"能匹配"记忆系统"）
        content_ngram=NGRAM(minsize=2, maxsize=4, stored=False),
    )
    
    # 创建索引
    ix = create_in(index_path, schema)
    print("   ✅ Whoosh 索引初始化完成")
    
    return ix


def get_workspace_root() -> str:
    """
    获取 WorkBuddy 工作区根目录
    
    Returns:
        str: 根目录路径
    """
    # 当前文件位置：.workbuddy/hybrid_search/init_database.py
    current_file = Path(__file__).resolve()
    # 向上两级到工作区根目录
    return str(current_file.parent.parent)


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 WorkBuddy 混合检索系统 - 数据库初始化")
    print("=" * 60)
    print()
    
    # 获取工作区根目录
    workspace_root = get_workspace_root()
    print(f"📂 工作区根目录：{workspace_root}")
    print()
    
    # 定义数据库路径
    db_path = os.path.join(workspace_root, ".workbuddy", "vector_db")
    index_path = os.path.join(workspace_root, ".workbuddy", "whoosh_index")
    
    # 创建目录
    os.makedirs(db_path, exist_ok=True)
    os.makedirs(index_path, exist_ok=True)
    
    print(f"📁 数据库目录：{db_path}")
    print(f"📁 索引目录：{index_path}")
    print()
    
    try:
        # 1. 初始化 LanceDB
        db = init_lancedb(db_path)
        print()
        
        # 2. 初始化 Whoosh
        ix = init_whoosh_index(index_path)
        print()
        
        # 3. 创建配置文件
        config = {
            "db_path": db_path,
            "index_path": index_path,
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "embedding_dim": 384,
        }
        
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        import json
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"配置文件已保存：{config_path}")
        print()
        print("=" * 60)
        print("✅ 数据库初始化完成！")
        print("=" * 60)
        print()
        print("下一步：")
        print("1. 运行 embedding_service.py 测试向量化服务")
        print("2. 运行 hybrid_search.py 测试混合检索")
        print("3. 导入现有记忆数据")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 初始化失败：{str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
