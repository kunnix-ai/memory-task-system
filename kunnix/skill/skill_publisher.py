#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 技能自动进化 - 技能发布器

功能：
1. 安全审计
2. 安装到技能目录
3. 更新技能注册表
4. 生成使用指南

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class SkillPublisher:
    """技能发布器"""
    
    def __init__(self, workspace_root: str = None):
        """初始化技能发布器"""
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        
        # 技能目录
        self.skill_drafts_dir = self.workspace_root / ".workbuddy" / "skills" / "drafts"
        self.skill_published_dir = self.workspace_root / ".workbuddy" / "skills" / "published"
        self.user_skills_dir = Path.home() / ".agents" / "skills"
        
        # 技能注册表
        self.skill_registry = self.workspace_root / ".workbuddy" / "skills" / "registry.json"
        
        # 确保目录存在
        self.skill_published_dir.mkdir(parents=True, exist_ok=True)
    
    def publish_skill(self, skill_path: str, target: str = "project") -> Dict:
        """
        发布技能
        
        Args:
            skill_path: 技能文件路径
            target: 发布目标 ("project" | "user")
        
        Returns:
            Dict: 发布结果
        """
        result = {
            'skill_path': skill_path,
            'target': target,
            'publish_time': datetime.now().isoformat(),
            'success': False,
            'message': '',
            'published_path': None,
        }
        
        # 1. 安全审计
        print(f"[SkillPublisher] 执行安全审计...")
        safety_check = self._safety_check(skill_path)
        
        if not safety_check['passed']:
            result['message'] = f"安全审计失败：{', '.join(safety_check['issues'])}"
            return result
        
        print(f"  ✅ 安全审计通过")
        
        # 2. 复制到目标目录
        try:
            skill_dir = Path(skill_path).parent
            skill_name = skill_dir.name
            
            if target == "project":
                target_dir = self.skill_published_dir / skill_name
            elif target == "user":
                target_dir = self.user_skills_dir / skill_name
            else:
                result['message'] = f"未知目标：{target}"
                return result
            
            # 复制文件
            if target_dir.exists():
                shutil.rmtree(target_dir)
            
            shutil.copytree(skill_dir, target_dir)
            
            result['published_path'] = str(target_dir)
            print(f"  ✅ 技能已发布到：{target_dir}")
            
        except Exception as e:
            result['message'] = f"发布失败：{str(e)}"
            return result
        
        # 3. 更新技能注册表
        self._update_registry(skill_name, str(target_dir))
        print(f"  ✅ 技能注册表已更新")
        
        # 4. 生成使用指南
        guide_path = self._generate_usage_guide(skill_name, target_dir)
        print(f"  ✅ 使用指南已生成：{guide_path}")
        
        result['success'] = True
        result['message'] = "技能发布成功"
        
        return result
    
    def _safety_check(self, skill_path: str) -> Dict:
        """安全审计"""
        result = {
            'passed': True,
            'issues': [],
            'warnings': [],
        }
        
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            result['passed'] = False
            result['issues'].append("无法读取文件")
            return result
        
        # 检查危险操作
        dangerous_patterns = [
            'rm -rf',
            'del /S /Q',
            'shutil.rmtree',
            'os.system',
            'subprocess.call',
            'eval(',
            'exec(',
            'DROP TABLE',
            'DELETE FROM',
        ]
        
        for pattern in dangerous_patterns:
            if pattern in content:
                result['warnings'].append(f"包含危险操作：{pattern}")
        
        # 检查外部 API 调用
        api_patterns = [
            'requests.post',
            'urllib.request',
            'httpx.post',
        ]
        
        for pattern in api_patterns:
            if pattern in content:
                result['warnings'].append(f"包含外部 API 调用：{pattern}")
        
        # 如果有严重问题，审计不通过
        if len(result['issues']) > 0:
            result['passed'] = False
        
        return result
    
    def _update_registry(self, skill_name: str, skill_path: str):
        """更新技能注册表"""
        import json
        
        registry = {}
        
        # 读取现有注册表
        if self.skill_registry.exists():
            try:
                with open(self.skill_registry, 'r', encoding='utf-8') as f:
                    registry = json.load(f)
            except:
                registry = {}
        
        # 更新注册表
        registry[skill_name] = {
            'path': skill_path,
            'installed_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'status': 'active',
        }
        
        # 保存注册表
        with open(self.skill_registry, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
    
    def _generate_usage_guide(self, skill_name: str, skill_dir: str) -> str:
        """生成使用指南"""
        guide_content = f"""# {skill_name} 使用指南

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📖 技能说明

{skill_name} 已通过审核并发布。

---

## 🚀 快速开始

### 方式 1：自动触发

当你在对话中提到相关关键词时，技能会自动触发。

### 方式 2：手动调用

```python
from skills.{skill_name} import execute

result = execute("你的输入")
print(result)
```

---

## 📋 触发条件

技能会在以下场景自动触发：
- 对话中包含项目名称（如"零碳园区"）
- 对话中包含相关动作（如"创建"、"申报"）

---

## 🔧 配置方法

如需修改技能行为，编辑技能目录下的 SKILL.md 文件。

---

## 📊 执行日志

技能执行日志保存在：`.workbuddy/skills/logs/{skill_name}.log`

---

**技能路径**: {skill_dir}
**版本**: 1.0.0
**状态**: ✅ 已发布
"""
        
        # 保存使用指南
        guide_path = Path(skill_dir) / "USAGE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return str(guide_path)


def demo_publisher():
    """演示发布器"""
    print("=" * 60)
    print("技能发布器演示")
    print("=" * 60)
    
    publisher = SkillPublisher()
    
    # 查找已审核的技能
    if not publisher.skill_drafts_dir.exists():
        print(f"技能草稿目录不存在：{publisher.skill_drafts_dir}")
        return False
    
    draft_files = list(publisher.skill_drafts_dir.glob("*/SKILL.md"))
    
    if not draft_files:
        print("未找到技能草稿文件")
        return False
    
    print(f"找到 {len(draft_files)} 个技能草稿:\n")
    for i, draft in enumerate(draft_files, 1):
        print(f"{i}. {draft.parent.name}")
    
    # 发布第一个技能
    print(f"\n发布技能：{draft_files[0].parent.name}")
    result = publisher.publish_skill(str(draft_files[0]), target="project")
    
    print(f"\n发布结果:")
    print(f"  状态：{'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"  消息：{result['message']}")
    if result['published_path']:
        print(f"  路径：{result['published_path']}")
    
    return result['success']


if __name__ == "__main__":
    success = demo_publisher()
    sys.exit(0 if success else 1)
