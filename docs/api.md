# Kunnix API 参考

> 完整的 API 文档和使用说明

## 📦 模块导入

```python
from kunnix import (
    MemorySystem,           # 记忆系统
    TaskOrchestrator,       # 任务编排器
    SkillEvolution,         # 技能进化系统
    AutomationManager,      # 自动化管理器
)
```

## 🧠 MemorySystem API

### 初始化

```python
memory = MemorySystem(
    db_path: str = "~/.kunnix/database",
    embedding_model: str = "text2vec-base-chinese",
    top_k: int = 10,
    threshold: float = 0.5
)
```

**参数说明**:
- `db_path`: 数据库路径
- `embedding_model`: 嵌入模型名称
- `top_k`: 默认返回数量
- `threshold`: 相似度阈值

### add() - 添加记忆

```python
memory_id = memory.add(
    content: str,              # 记忆内容
    tags: List[str] = None,    # 标签列表
    project: str = None,       # 项目名称
    metadata: Dict = None,     # 额外元数据
    auto_index: bool = True    # 自动索引
) -> str
```

**返回值**: 记忆 ID（字符串）

**示例**:
```python
mid = memory.add(
    content="零碳园区申报需要准备可研报告",
    tags=["申报", "文档"],
    project="零碳园区"
)
```

### search() - 检索记忆

```python
results = memory.search(
    query: str,                    # 查询文本
    filters: Dict = None,          # 过滤条件
    limit: int = None,             # 返回数量
    threshold: float = None,       # 相似度阈值
    with_scores: bool = True       # 是否返回分数
) -> List[Dict]
```

**返回值**: 结果列表，每项包含：
- `content`: 记忆内容
- `score`: 相似度分数
- `tags`: 标签
- `metadata`: 元数据

**示例**:
```python
results = memory.search(
    "零碳园区申报",
    filters={"project": "零碳园区"},
    limit=5
)

for r in results:
    print(f"{r['content']} ({r['score']:.2f})")
```

### add_batch() - 批量添加

```python
ids = memory.add_batch(
    memories: List[Dict],     # 记忆列表
    auto_index: bool = True   # 自动索引
) -> List[str]
```

**示例**:
```python
memories = [
    {"content": "记忆 1", "tags": ["标签 1"]},
    {"content": "记忆 2", "tags": ["标签 2"]},
]
ids = memory.add_batch(memories)
```

### delete() - 删除记忆

```python
memory.delete(
    memory_id: str    # 记忆 ID
) -> bool
```

### cleanup() - 清理旧记忆

```python
memory.cleanup(
    days: int = 30,    # 保留天数
    dry_run: bool = False  # 预览模式
) -> int
```

**返回值**: 清理的记忆数量

## 📋 TaskOrchestrator API

### 初始化

```python
task_manager = TaskOrchestrator(
    db_path: str = "~/.kunnix/tasks",
    auto_archive: bool = True,
    archive_after_days: int = 30
)
```

### create_task() - 创建任务

```python
task = task_manager.create_task(
    title: str,                  # 任务标题
    description: str = None,     # 任务描述
    project: str = None,         # 项目名称
    priority: str = "normal",    # 优先级
    auto_start: bool = False     # 自动开始
) -> Task
```

**Task 对象属性**:
- `id`: 任务 ID
- `title`: 标题
- `status`: 状态
- `progress`: 进度（0-100）
- `created_at`: 创建时间
- `updated_at`: 更新时间

### get_task() - 获取任务

```python
task = task_manager.get_task(
    task_id: str    # 任务 ID
) -> Task
```

### update_task() - 更新任务

```python
task_manager.update_task(
    task_id: str,              # 任务 ID
    status: str = None,        # 状态
    progress: int = None,      # 进度
    title: str = None,         # 标题
    description: str = None    # 描述
) -> Task
```

### complete_task() - 完成任务

```python
task_manager.complete_task(
    task_id: str,      # 任务 ID
    auto_archive: bool = True  # 自动归档
) -> Task
```

### list_tasks() - 查询任务列表

```python
tasks = task_manager.list_tasks(
    status: str = None,        # 状态过滤
    project: str = None,       # 项目过滤
    limit: int = None,         # 数量限制
    sort_by: str = "created_at"  # 排序字段
) -> List[Task]
```

## 🤖 SkillEvolution API

### 初始化

```python
skill_system = SkillEvolution(
    drafts_dir: str = "~/.kunnix/skills/drafts",
    published_dir: str = "~/.kunnix/skills/published",
    min_confidence: float = 0.7
)
```

### extract_patterns() - 提取模式

```python
patterns = skill_system.extract_patterns(
    task_archives: List[str],    # 任务档案路径
    min_cluster_size: int = 3,   # 最小聚类大小
    threshold: float = 0.5       # 相似度阈值
) -> Dict
```

### generate_skill() - 生成技能

```python
skill = skill_system.generate_skill(
    pattern: Dict,        # 模式数据
    output_dir: str = None  # 输出目录
) -> Dict
```

**返回值**:
- `skill_name`: 技能名称
- `path`: SKILL.md 路径
- `confidence`: 置信度

### review_skill() - 审核技能

```python
result = skill_system.review_skill(
    skill_path: str,       # 技能路径
    auto_pass: bool = True  # 自动通过
) -> Dict
```

**返回值**:
- `status`: "approved" | "needs_revision" | "rejected"
- `pass_rate`: 通过率
- `issues`: 问题列表

### publish_skill() - 发布技能

```python
skill_system.publish_skill(
    skill_path: str    # 技能路径
) -> str
```

**返回值**: 发布后的技能路径

## ⚙️ AutomationManager API

### 初始化

```python
automation = AutomationManager(
    rules_file: str = "~/.kunnix/automation_rules.yaml"
)
```

### create_rule() - 创建自动化规则

```python
rule_id = automation.create_rule(
    name: str,                   # 规则名称
    trigger: str,                # 触发条件
    actions: List[Dict],         # 动作列表
    enabled: bool = True         # 是否启用
) -> str
```

**动作类型**:
- `create_task`: 创建任务
- `search_memory`: 检索记忆
- `add_memory`: 添加记忆
- `run_skill`: 运行技能

### trigger() - 触发自动化

```python
results = automation.trigger(
    trigger_text: str    # 触发文本
) -> List[Dict]
```

### get_history() - 获取执行历史

```python
history = automation.get_history(
    limit: int = 10,         # 数量限制
    rule_name: str = None    # 规则过滤
) -> List[Dict]
```

## 🔧 工具函数

### utils.embedding() - 文本向量化

```python
from kunnix.utils import embedding

vector = embedding.text_to_vector("文本内容")
```

### utils.similarity() - 计算相似度

```python
from kunnix.utils import similarity

score = similarity.cosine_similarity(vec1, vec2)
```

### utils.format_time() - 格式化时间

```python
from kunnix.utils import format_time

time_str = format_time(datetime.now())
```

## 📚 示例代码

### 完整工作流

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化
memory = MemorySystem()
task_manager = TaskOrchestrator()

# 1. 创建任务
task = task_manager.create_task(
    title="编写项目申报文档",
    project="零碳园区",
    auto_start=True
)

# 2. 检索相关记忆
related = memory.search(
    "零碳园区申报文档",
    filters={"project": "零碳园区"},
    limit=5
)

# 3. 添加新记忆
memory.add(
    content="已完成项目申报文档编写",
    tags=["完成", "文档"],
    project="零碳园区"
)

# 4. 完成任务
task_manager.complete_task(task.id)

print("✅ 工作流完成！")
```

## 🐛 错误处理

```python
from kunnix import MemorySystem
from kunnix.exceptions import MemoryError, TaskError

try:
    memory = MemorySystem()
    results = memory.search("查询")
except MemoryError as e:
    print(f"记忆检索失败：{e}")
except TaskError as e:
    print(f"任务管理失败：{e}")
```

## 📖 相关文档

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [系统架构](architecture.md)
- [使用示例](examples.md)
