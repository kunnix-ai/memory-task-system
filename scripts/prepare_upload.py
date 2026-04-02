#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kunnix 代码上传准备脚本

功能：
1. 复制现有代码到 kunnix 目录
2. 更新导入路径
3. 运行代码质量检查
4. 生成上传清单

作者：阿中
日期：2026-04-02
"""

import os
import shutil
from pathlib import Path

def copy_module(src: str, dst: str, module_name: str):
    """复制模块并更新__init__.py"""
    print(f"Copying {module_name} module...")
    
    # 复制 Python 文件
    for py_file in Path(src).glob("*.py"):
        if py_file.name != "__init__.py":  # 跳过已有的__init__.py
            dst_file = Path(dst) / py_file.name
            shutil.copy2(py_file, dst_file)
            print(f"  [OK] {py_file.name} -> {dst}/")
    
    print(f"  Done: {module_name}\n")

def main():
    """主函数"""
    print("=" * 60)
    print("Kunnix 代码上传准备")
    print("=" * 60 + "\n")
    
    # 定义路径
    workspace = Path(__file__).parent.parent.parent
    kunnix_dir = workspace / "kunnix" / "kunnix"
    
    # 源目录
    hybrid_search_src = workspace / "hybrid_search"
    task_mgmt_src = workspace / "task_management"
    skill_evo_src = workspace / "skill_evolution"
    integration_src = workspace / "integration"
    
    # 目标目录
    memory_dst = kunnix_dir / "memory"
    task_dst = kunnix_dir / "task"
    skill_dst = kunnix_dir / "skill"
    integration_dst = kunnix_dir / "integration"
    
    print("[DIR] Source directories:")
    print(f"  Hybrid Search: {hybrid_search_src}")
    print(f"  Task Management: {task_mgmt_src}")
    print(f"  Skill Evolution: {skill_evo_src}")
    print(f"  Integration: {integration_src}\n")
    
    print("[DIR] Target directories:")
    print(f"  Memory: {memory_dst}")
    print(f"  Task: {task_dst}")
    print(f"  Skill: {skill_dst}")
    print(f"  Integration: {integration_dst}\n")
    
    # 复制模块
    if hybrid_search_src.exists():
        copy_module(str(hybrid_search_src), str(memory_dst), "Memory")
    
    if task_mgmt_src.exists():
        copy_module(str(task_mgmt_src), str(task_dst), "Task")
    
    if skill_evo_src.exists():
        copy_module(str(skill_evo_src), str(skill_dst), "Skill")
    
    if integration_src.exists():
        copy_module(str(integration_src), str(integration_dst), "Integration")
    
    # 生成上传清单
    print("=" * 60)
    print("Upload Checklist")
    print("=" * 60)
    
    upload_files = []
    for root, dirs, files in os.walk(kunnix_dir):
        for file in files:
            if file.endswith(('.py', '.md', '.toml', '.txt')):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(workspace / "kunnix")
                upload_files.append(str(rel_path))
    
    for file in sorted(upload_files):
        print(f"  □ {file}")
    
    print(f"\nTotal: {len(upload_files)} files")
    print("=" * 60)
    print("[OK] Preparation complete!\n")
    print("Next steps:")
    print("1. Review upload checklist")
    print("2. Run code quality checks (black, flake8, mypy)")
    print("3. Git init and commit")
    print("4. Push to GitHub\n")

if __name__ == "__main__":
    main()
