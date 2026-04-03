# API 概览

> Kunnix API 完整参考

## 📦 模块导入

```python
from kunnix import (
    MemorySystem,           # 记忆系统
    TaskOrchestrator,       # 任务编排器
    SkillEvolution,         # 技能进化系统
    AutomationManager,      # 自动化管理器
)
```

## 🧠 MemorySystem

记忆系统的核心 API：

- `add()` - 添加记忆
- `search()` - 检索记忆
- `add_batch()` - 批量添加
- `delete()` - 删除记忆
- `cleanup()` - 清理旧记忆

[查看 MemorySystem 详细 API](/api/memory-system)

## 📋 TaskOrchestrator

任务管理的核心 API：

- `create_task()` - 创建任务
- `get_task()` - 获取任务
- `update_task()` - 更新任务
- `complete_task()` - 完成任务
- `list_tasks()` - 查询任务列表

[查看 TaskOrchestrator 详细 API](/api/task-orchestrator)

## 🤖 SkillEvolution

技能进化的核心 API：

- `extract_patterns()` - 提取模式
- `generate_skill()` - 生成技能
- `review_skill()` - 审核技能
- `publish_skill()` - 发布技能

[查看 SkillEvolution 详细 API](/api/skill-evolution)

## ⚙️ AutomationManager

自动化管理的核心 API：

- `create_rule()` - 创建规则
- `trigger()` - 触发自动化
- `get_history()` - 获取历史

[查看 AutomationManager 详细 API](/api/automation-manager)

## 📚 使用示例

[查看使用示例](/examples/basic)
