# Kunnix 快速开始指南

> 5 分钟上手 Kunnix 记忆与任务调度系统

## 🎯 学习目标

完成本教程后，你将能够：
- ✅ 初始化 Kunnix 系统
- ✅ 使用记忆存储和检索
- ✅ 创建和管理任务
- ✅ 配置自动化流程

## 📦 第一步：初始化系统

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化记忆系统
memory = MemorySystem(
    db_path="./kunnix_db",  # 数据库路径
    top_k=10                # 默认返回数量
)

# 初始化任务管理器
task_manager = TaskOrchestrator()
```

## 🧠 第二步：使用记忆系统

### 存储记忆

```python
# 添加单条记忆
memory.add(
    content="零碳园区项目申报需要准备：可行性研究报告、技术方案、预算方案",
    tags=["零碳园区", "申报文档"],
    project="零碳园区"
)

# 批量添加记忆
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

# 高级检索（带过滤）
results = memory.search(
    "申报文档",
    filters={"project": "零碳园区"},
    limit=5
)

# 查看结果
for result in results:
    print(f"内容：{result['content']}")
    print(f"相似度：{result['score']}")
    print(f"标签：{result['tags']}")
    print("---")
```

## 📋 第三步：管理任务

### 创建任务

```python
# 创建任务
task = task_manager.create_task(
    title="创建零碳园区申报文档",
    description="准备项目申报所需的全部文档",
    project="零碳园区",
    auto_start=True  # 自动开始任务
)

print(f"任务 ID: {task.id}")
print(f"状态：{task.status}")
```

### 更新任务状态

```python
# 更新进度
task_manager.update_task(
    task_id=task.id,
    status="in_progress",
    progress=50  # 完成 50%
)

# 完成任务
task_manager.complete_task(task.id)
```

### 查询任务

```python
# 获取任务详情
task = task_manager.get_task(task_id)

# 查询所有任务
tasks = task_manager.list_tasks(
    status="in_progress",
    project="零碳园区"
)
```

## 🔄 第四步：配置自动化

### 创建自动化规则

```python
from kunnix import AutomationManager

automation = AutomationManager()

# 创建自动化规则
automation.create_rule(
    name="零碳园区文档自动创建",
    trigger="创建零碳园区文档",
    actions=[
        {"type": "create_task", "params": {"project": "零碳园区"}},
        {"type": "search_memory", "params": {"limit": 5}},
    ]
)
```

### 触发自动化

```python
# 手动触发
automation.trigger("创建零碳园区文档")

# 查看自动化历史
history = automation.get_history(limit=10)
```

## 🎓 完整示例

```python
from kunnix import MemorySystem, TaskOrchestrator

# 1. 初始化
memory = MemorySystem()
task_manager = TaskOrchestrator()

# 2. 存储项目信息
memory.add(
    content="零碳园区项目：总投资 5000 万，建设周期 6 个月",
    tags=["项目信息"],
    project="零碳园区"
)

# 3. 创建任务
task = task_manager.create_task(
    title="编写可行性研究报告",
    project="零碳园区"
)

# 4. 检索相关记忆
related = memory.search("零碳园区", limit=5)

# 5. 完成任务
task_manager.complete_task(task.id)

print("✅ 任务完成！")
```

## 📚 下一步

- [系统架构](architecture.md) - 了解内部原理
- [API 参考](api.md) - 完整 API 文档
- [使用示例](examples.md) - 更多实战案例

## 💡 提示

- 使用 `memory.search()` 时，关键词越具体，结果越精准
- 任务命名建议：`动词 + 名词` 格式（如"创建文档"）
- 定期清理旧记忆：`memory.cleanup(days=30)`
