#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 混合检索系统 - 记忆数据导入器

功能：
1. 扫描现有记忆文件（每日日志、项目记忆、长期记忆）
2. 解析 YAML frontmatter
3. 向量化并导入到 LanceDB
4. 建立 Whoosh 全文索引
5. 批量处理（带进度条）

作者：阿中
版本：v1.0.0
日期：2026-04-01
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import hashlib

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from hybrid_search.embedding_service import EmbeddingService


def parse_yaml_frontmatter(content: str) -> Dict:
    """
    解析 Markdown 文件的 YAML frontmatter
    
    Args:
        content: Markdown 文件内容
    
    Returns:
        Dict: frontmatter 字典
    """
    frontmatter = {}
    
    # 匹配 frontmatter 区域
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return frontmatter
    
    yaml_content = match.group(1)
    
    # 简单 YAML 解析（键：值格式）
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # 处理列表
            if value.startswith('[') and value.endswith(']'):
                # 列表格式：[tag1, tag2, tag3]
                items = value[1:-1].split(',')
                frontmatter[key] = [item.strip().strip('"\'') for item in items]
            else:
                # 普通字符串
                frontmatter[key] = value.strip('"\'')
    
    return frontmatter


def extract_content_without_frontmatter(content: str) -> str:
    """
    提取去除 frontmatter 后的正文内容
    
    Args:
        content: Markdown 文件内容
    
    Returns:
        str: 正文内容
    """
    # 去除 frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return content[match.end():]
    return content


def generate_doc_id(file_path: str, content: str) -> str:
    """
    生成文档唯一 ID
    
    Args:
        file_path: 文件路径
        content: 文件内容
    
    Returns:
        str: MD5 哈希 ID
    """
    # 使用文件路径 + 内容前 1000 字符生成唯一 ID
    unique_str = f"{file_path}:{content[:1000]}"
    return hashlib.md5(unique_str.encode('utf-8')).hexdigest()


class MemoryImporter:
    """记忆数据导入器"""
    
    def __init__(self, workspace_root: str = None):
        """
        初始化导入器
        
        Args:
            workspace_root: WorkBuddy 工作区根目录
        """
        # 当前文件位置：.workbuddy/hybrid_search/memory_importer.py
        # 父目录的父目录是工作区根目录
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        
        # 记忆文件目录（直接在 workspace_root/memory/）
        self.memory_dir = self.workspace_root / "memory"
        
        # 初始化服务
        self.embedding_service = EmbeddingService()
        
        # 初始化数据库
        self._init_databases()
        
        print(f"[MemoryImporter] 初始化完成")
        print(f"  工作区：{self.workspace_root}")
        print(f"  记忆目录：{self.memory_dir}")
    
    def _init_databases(self):
        """初始化数据库连接"""
        import lancedb
        from whoosh.index import open_dir
        
        # 加载配置
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # LanceDB
        self.lancedb = lancedb.connect(config['db_path'])
        print(f"  LanceDB: {config['db_path']}")
        
        # Whoosh
        self.whoosh_ix = open_dir(config['index_path'])
        print(f"  Whoosh: {config['index_path']}")
    
    def scan_memory_files(self) -> List[Path]:
        """
        扫描所有记忆文件
        
        Returns:
            List[Path]: 记忆文件路径列表
        """
        memory_files = []
        
        if not self.memory_dir.exists():
            print(f"  [WARN] 记忆目录不存在：{self.memory_dir}")
            return memory_files
        
        # 扫描不同类型的记忆文件
        patterns = [
            "*.md",  # 所有 Markdown 文件
        ]
        
        for pattern in patterns:
            for file_path in self.memory_dir.rglob(pattern):
                # 跳过目录
                if file_path.is_dir():
                    continue
                
                # 跳过特定文件
                if file_path.name.startswith('.'):
                    continue
                
                memory_files.append(file_path)
        
        print(f"  扫描到 {len(memory_files)} 个记忆文件")
        return memory_files
    
    def import_to_lancedb(self, doc_id: str, content: str, metadata: Dict):
        """
        导入文档到 LanceDB
        
        Args:
            doc_id: 文档 ID
            content: 文档内容
            metadata: 元数据
        """
        # 向量化
        embedding = self.embedding_service.encode(content)
        
        # 准备数据
        data = {
            "doc_id": doc_id,
            "vector": embedding.tolist(),
            "title": metadata.get('title', ''),
            "content": content[:10000],  # 限制内容长度
            "category": metadata.get('category', ''),
            "tags": ' '.join(metadata.get('tags', [])) if isinstance(metadata.get('tags'), list) else metadata.get('tags', ''),
            "memory_type": metadata.get('memory_type', 'unknown'),
            "created_at": metadata.get('created_at', datetime.now().isoformat()),
            "updated_at": metadata.get('updated_at', datetime.now().isoformat()),
        }
        
        # 创建或追加到表
        try:
            table = self.lancedb.open_table("memories")
            table.add([data])
        except:
            # 表不存在，创建新表
            table = self.lancedb.create_table("memories", [data])
    
    def import_to_whoosh(self, doc_id: str, title: str, content: str, metadata: Dict):
        """
        导入文档到 Whoosh 全文索引
        
        Args:
            doc_id: 文档 ID
            title: 标题
            content: 内容
            metadata: 元数据
        """
        from whoosh.writing import AsyncWriter
        
        # 准备文档
        doc = {
            "doc_id": doc_id,
            "title": title,
            "content": content,
            "category": metadata.get('category', ''),
            "tags": ' '.join(metadata.get('tags', [])) if isinstance(metadata.get('tags'), list) else metadata.get('tags', ''),
            "memory_type": metadata.get('memory_type', 'unknown'),
            "created_at": datetime.fromisoformat(metadata.get('created_at', datetime.now().isoformat())),
            "updated_at": datetime.fromisoformat(metadata.get('updated_at', datetime.now().isoformat())),
            "content_ngram": content,  # NGRAM 自动处理
        }
        
        # 写入索引
        with self.whoosh_ix.writer() as writer:
            writer.add_document(**doc)
    
    def import_memory(self, file_path: Path):
        """
        导入单个记忆文件
        
        Args:
            file_path: 文件路径
        """
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 frontmatter
            frontmatter = parse_yaml_frontmatter(content)
            
            # 提取正文
            body_content = extract_content_without_frontmatter(content)
            
            # 生成文档 ID
            doc_id = generate_doc_id(str(file_path), content)
            
            # 提取标题
            title = frontmatter.get('title', file_path.stem)
            
            # 确定记忆类型
            if "daily" in str(file_path).lower() or re.match(r'\d{4}-\d{2}-\d{2}\.md', file_path.name):
                memory_type = 'daily'
            elif "project" in str(file_path).lower():
                memory_type = 'project'
            elif "memory.md" in file_path.name:
                memory_type = 'long_term'
            else:
                memory_type = 'other'
            
            # 构建元数据
            metadata = {
                'title': title,
                'category': frontmatter.get('category', ''),
                'tags': frontmatter.get('tags', []),
                'memory_type': memory_type,
                'created_at': frontmatter.get('created_at', datetime.now().isoformat()),
                'updated_at': frontmatter.get('modified', datetime.now().isoformat()),
                'file_path': str(file_path),
            }
            
            # 导入到 LanceDB
            self.import_to_lancedb(doc_id, body_content, metadata)
            
            # 导入到 Whoosh
            self.import_to_whoosh(doc_id, title, body_content, metadata)
            
            return True
            
        except Exception as e:
            print(f"  [FAIL] 导入失败 {file_path.name}: {str(e)}")
            return False
    
    def import_all(self, batch_size: int = 50):
        """
        批量导入所有记忆文件
        
        Args:
            batch_size: 批处理大小
        """
        print("\n" + "=" * 60)
        print("开始导入记忆数据...")
        print("=" * 60)
        
        # 扫描文件
        memory_files = self.scan_memory_files()
        
        if len(memory_files) == 0:
            print("  没有找到记忆文件")
            return
        
        # 批量导入
        success_count = 0
        fail_count = 0
        
        for i, file_path in enumerate(memory_files, 1):
            try:
                # 显示进度
                progress = f"[{i}/{len(memory_files)}]"
                print(f"{progress} 导入：{file_path.name}", end='\r')
                
                # 导入
                if self.import_memory(file_path):
                    success_count += 1
                else:
                    fail_count += 1
                
            except Exception as e:
                fail_count += 1
                print(f"\n  [FAIL] 导入失败 {file_path.name}: {str(e)}")
        
        # 提交 Whoosh 索引
        print("\n正在提交索引...")
        
        print("\n" + "=" * 60)
        print(f"导入完成！")
        print(f"  成功：{success_count} 个文件")
        print(f"  失败：{fail_count} 个文件")
        print("=" * 60)


def main():
    """主函数"""
    print("=" * 60)
    print("WorkBuddy 记忆数据导入工具")
    print("=" * 60)
    print()
    
    # 获取工作区根目录
    workspace_root = Path(__file__).parent.parent
    
    # 创建导入器
    importer = MemoryImporter(workspace_root)
    
    # 导入所有记忆
    importer.import_all()
    
    print("\n下一步：")
    print("1. 运行 hybrid_search.py 测试检索")
    print("2. 运行 memory_search_skill.py 集成到 WorkBuddy")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
