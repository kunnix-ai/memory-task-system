# 快速开始

> 5 分钟快速上手 Kunnix

## 📦 安装

```bash
# 从源码安装
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system
pip install -e .
```

## 🚀 快速使用

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化
memory = MemorySystem()
task_manager = TaskOrchestrator()

# 添加记忆
memory.add(
    content="零碳园区申报需要准备可研报告、技术方案、预算方案",
    tags=["零碳园区", "申报文档"]
)

# 检索记忆
results = memory.search("零碳园区申报", limit=5)

# 创建任务
task = task_manager.create_task(
    title="编写申报文档",
    project="零碳园区",
    auto_start=True
)

print("✅ Kunnix 已就绪！")
```

## 📚 下一步

- [安装指南](/guide/installation) - 详细安装步骤
- [什么是 Kunnix](/guide/what-is-kunnix) - 了解核心概念
- [使用示例](/examples/basic) - 更多实战案例
