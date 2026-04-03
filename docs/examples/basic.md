# 基础示例

> Kunnix 基础使用示例

## 🧠 记忆系统

### 添加记忆

```python
from kunnix import MemorySystem

memory = MemorySystem()

# 添加单条记忆
memory.add(
    content="零碳园区申报需要准备可研报告、技术方案、预算方案",
    tags=["零碳园区", "申报文档"],
    project="零碳园区"
)

# 批量添加
memories = [
    {"content": "记忆 1", "tags": ["标签 1"]},
    {"content": "记忆 2", "tags": ["标签 2"]},
]
memory.add_batch(memories)
```

### 检索记忆

```python
# 基础检索
results = memory.search("零碳园区申报")

# 带过滤检索
results = memory.search(
    "申报文档",
    filters={"project": "零碳园区"},
    limit=5
)

# 查看结果
for r in results:
    print(f"内容：{r['content']}")
    print(f"相似度：{r['score']}")
```

## 📋 任务管理

### 创建任务

```python
from kunnix import TaskOrchestrator

task_manager = TaskOrchestrator()

task = task_manager.create_task(
    title="编写申报文档",
    description="准备项目申报所需全部文档",
    project="零碳园区",
    priority="high",
    auto_start=True
)
```

### 更新任务

```python
# 更新进度
task_manager.update_task(task.id, progress=50)

# 完成任务
task_manager.complete_task(task.id)

# 查询任务
tasks = task_manager.list_tasks(
    status="in_progress",
    project="零碳园区"
)
```

## 🤖 完整工作流

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化
memory = MemorySystem()
task_manager = TaskOrchestrator()

# 1. 添加项目信息
memory.add(
    content="零碳园区项目：总投资 5000 万，建设周期 6 个月",
    tags=["项目信息"],
    project="零碳园区"
)

# 2. 创建任务
task = task_manager.create_task(
    title="编写可研报告",
    project="零碳园区"
)

# 3. 检索相关记忆
related = memory.search("零碳园区", limit=5)

# 4. 完成任务
task_manager.complete_task(task.id)

print("✅ 工作流完成！")
```

## 📚 更多示例

- [个人知识管理](/examples/knowledge-management)
- [项目管理](/examples/project-management)
- [技能自动化](/examples/skill-automation)
