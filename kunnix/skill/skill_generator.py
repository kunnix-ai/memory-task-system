#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 技能自动进化 - 技能生成器（MVP 版本）

功能：
1. 基于模式生成技能草稿
2. 填充 SKILL.md 模板
3. 生成 Python 代码框架

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
from pathlib import Path
from typing import Dict
from datetime import datetime


class SkillGenerator:
    """技能生成器"""
    
    def __init__(self, workspace_root: str = None):
        """初始化技能生成器"""
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.skill_drafts_dir = self.workspace_root / ".workbuddy" / "skills" / "drafts"
        
        # 确保目录存在
        self.skill_drafts_dir.mkdir(parents=True, exist_ok=True)
        
        # SKILL.md 模板
        self.skill_template = """---
name: {skill_name}
version: 1.0.0
created: {created_date}
author: WorkBuddy 技能自动进化系统
project: {project}
---

# {skill_name}

> **描述**: {skill_description}

---

## 🎯 触发条件

当用户消息包含以下关键字时自动触发：
{trigger_keywords}

---

## 🔧 执行动作

**执行脚本**:
```python
# {skill_name} 自动生成的代码框架
# 项目：{project}
# 创建时间：{created_date}

def execute(user_input: str) -> str:
    \"\"\"
    执行技能
    
    Args:
        user_input: 用户输入
    
    Returns:
        str: 执行结果
    \"\"\"
    # TODO: 实现具体逻辑
    # 基于以下任务模式生成：
    {task_patterns}
    
    return "技能执行成功"

if __name__ == "__main__":
    result = execute("")
    print(result)
```

---

## 📊 执行流程

1. 接收用户输入
2. 解析参数
3. 执行核心逻辑
4. 返回结果

---

## 🎯 使用示例

```
用户：{example_input}
AI: {example_output}
```

---

## 🔒 安全机制

- [ ] 无危险操作
- [ ] 无需外部 API 调用
- [ ] 无需文件写入权限

---

## 📝 配置方法

将以下配置添加到 `.workbuddy/automations/`:

```toml
name = "{skill_name}"
trigger = "{trigger_keywords_first}"
action = "execute_script"
script = "skills/{skill_name}/{skill_name}.py"
```

---

**生成时间**: {generated_time}  
**生成器版本**: v1.0.0
"""
    
    def generate_skill(self, candidate: Dict) -> str:
        """
        生成技能草稿
        
        Args:
            candidate: 技能候选
        
        Returns:
            str: 技能文档路径
        """
        project = candidate['project']
        task_count = candidate['task_count']
        actions = candidate['common_actions']
        
        # 生成技能名称
        skill_name = f"{project}自动助手"
        
        # 生成描述
        description = f"基于{task_count}个{project}项目任务自动生成的技能，提供{project}相关任务的自动化支持"
        
        # 触发关键词
        trigger_keywords = '\n'.join([f"- {kw}" for kw in candidate['project'].split('、')])
        
        # 任务模式
        task_patterns = '\n    '.join([f"- {action}" for action in actions[:5]])
        
        # 示例
        example_input = f"帮我{actions[0] if actions else '处理'}{project}相关任务"
        example_output = f"好的，正在{actions[0] if actions else '处理'}{project}任务..."
        
        # 填充模板
        skill_doc = self.skill_template.format(
            skill_name=skill_name,
            created_date=datetime.now().strftime('%Y-%m-%d'),
            project=project,
            skill_description=description,
            trigger_keywords=trigger_keywords,
            task_patterns=task_patterns,
            example_input=example_input,
            example_output=example_output,
            trigger_keywords_first=project.split('、')[0],
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        
        # 保存技能草稿
        skill_dir = self.skill_drafts_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_file = skill_dir / "SKILL.md"
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(skill_doc)
        
        print(f"[SkillGenerator] 技能草稿已生成：{skill_file}")
        
        return str(skill_file)


def demo_skill_generator():
    """演示技能生成"""
    print("=" * 60)
    print("技能生成器演示（MVP）")
    print("=" * 60)
    print()
    
    generator = SkillGenerator()
    
    # 模拟技能候选
    candidate = {
        'project': '零碳园区',
        'task_count': 3,
        'common_actions': ['创建', '申报', '整理'],
        'common_deliverables': ['文档', '报告'],
    }
    
    print("生成技能草稿...")
    skill_path = generator.generate_skill(candidate)
    print(f"技能路径：{skill_path}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = demo_skill_generator()
    sys.exit(0 if success else 1)
