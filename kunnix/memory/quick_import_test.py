#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速导入测试 - 仅导入最近的记忆文件
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hybrid_search.memory_importer import MemoryImporter

# 获取工作区根目录
workspace_root = Path(__file__).parent.parent

print("=" * 60)
print("快速导入测试（仅最近 7 天的记忆）")
print("=" * 60)

# 创建导入器
importer = MemoryImporter(workspace_root)

# 扫描文件
memory_files = importer.scan_memory_files()

# 只导入最近的 7 个文件
recent_files = sorted(memory_files, key=lambda x: x.name, reverse=True)[:7]

print(f"\n准备导入 {len(recent_files)} 个文件...")

success = 0
fail = 0

for i, file_path in enumerate(recent_files, 1):
    print(f"[{i}/{len(recent_files)}] 导入：{file_path.name}")
    try:
        importer.import_memory(file_path)
        success += 1
    except Exception as e:
        print(f"  [FAIL] {str(e)}")
        fail += 1

print(f"\n导入完成：{success} 成功，{fail} 失败")
print("\n下一步：运行 performance_test.py")
