# 项目管理

> 使用 Kunnix 管理项目全流程

## 📋 场景说明

管理项目的全流程文档和任务。

## 💼 使用示例

```python
from kunnix import MemorySystem, TaskOrchestrator

memory = MemorySystem()
task_manager = TaskOrchestrator()

# 创建项目记忆
memory.add(
    content="零碳园区项目：总投资 5000 万，建设周期 6 个月",
    tags=["项目信息"],
    project="零碳园区"
)

# 创建任务
task = task_manager.create_task(
    title="编写可研报告",
    project="零碳园区",
    priority="high"
)

# 检索相关信息
related = memory.search("零碳园区", limit=5)
```

## 📖 相关示例

- [基础示例](/examples/basic)
- [知识管理](/examples/knowledge-management)
