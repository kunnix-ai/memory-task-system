# Kunnix 使用示例

> 实战案例和最佳实践

## 📚 目录

1. [个人知识管理](#1-个人知识管理)
2. [项目管理](#2-项目管理)
3. [技能自动化](#3-技能自动化)
4. [多 Agent 协作](#4-多-agent 协作)
5. [企业级应用](#5-企业级应用)

---

## 1. 个人知识管理

### 1.1 构建第二大脑

**场景**: 知识工作者需要管理大量笔记、文章、想法

```python
from kunnix import MemorySystem

# 初始化
memory = MemorySystem(db_path="./my_brain")

# 添加读书笔记
memory.add(
    content="《深度工作》核心观点：深度工作是稀缺且宝贵的，需要刻意练习",
    tags=["读书笔记", "个人成长"],
    metadata={"book": "深度工作", "author": "卡尔·纽波特"}
)

# 添加文章摘要
memory.add(
    content="AI 记忆系统三大核心：存储、检索、进化",
    tags=["AI", "技术文章"],
    metadata={"source": "知乎", "url": "https://..."}
)

# 检索相关内容
results = memory.search("AI 记忆系统", limit=5)
for r in results:
    print(f"- {r['content']}")
```

### 1.2 微信文章管理

**场景**: 自动保存和整理微信文章

```python
from kunnix import MemorySystem

memory = MemorySystem()

# 保存微信文章
def save_wechat_article(title, content, url):
    memory.add(
        content=f"{title}: {content[:500]}...",  # 摘要
        tags=["微信文章", "待读"],
        metadata={
            "type": "article",
            "source": "wechat",
            "url": url,
            "saved_at": datetime.now().isoformat()
        }
    )

# 使用
save_wechat_article(
    title="AI 记忆系统详解",
    content="文章内容...",
    url="https://mp.weixin.qq.com/..."
)

# 查找待读文章
articles = memory.search(
    "微信文章",
    filters={"tags": ["待读"]}
)
```

---

## 2. 项目管理

### 2.1 零碳园区项目管理

**场景**: 管理零碳园区项目的全流程文档

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化
memory = MemorySystem()
task_manager = TaskOrchestrator()

# 1. 创建项目记忆
memory.add(
    content="零碳园区项目：总投资 5000 万，建设周期 6 个月，包含光伏、储能、充电桩",
    tags=["项目信息"],
    project="零碳园区"
)

# 2. 创建任务
tasks = [
    ("编写可行性研究报告", "high"),
    ("设计技术方案", "high"),
    ("编制预算方案", "medium"),
    ("准备申报材料", "high"),
]

for title, priority in tasks:
    task_manager.create_task(
        title=title,
        project="零碳园区",
        priority=priority
    )

# 3. 检索项目信息
project_info = memory.search(
    "零碳园区",
    filters={"project": "零碳园区"}
)
```

### 2.2 多项目并行管理

**场景**: 同时管理多个项目

```python
from kunnix import TaskOrchestrator

task_manager = TaskOrchestrator()

# 创建多个项目
projects = ["零碳园区", "慢病逆转", "小说变现"]

for project in projects:
    # 创建项目任务
    task_manager.create_task(
        title=f"{project} 项目周报",
        project=project,
        priority="normal"
    )

# 查询所有项目任务
all_tasks = task_manager.list_tasks()

# 按项目分组
from collections import defaultdict
by_project = defaultdict(list)
for task in all_tasks:
    by_project[task.project].append(task)

for project, tasks in by_project.items():
    print(f"{project}: {len(tasks)} 个任务")
```

---

## 3. 技能自动化

### 3.1 自动文档创建技能

**场景**: 自动创建零碳园区项目文档

```python
# 触发词："创建零碳园区文档"
# 技能自动执行：

from kunnix import MemorySystem

memory = MemorySystem()

# 1. 检索相关记忆
memories = memory.search(
    "零碳园区申报文档",
    filters={"project": "零碳园区"},
    limit=10
)

# 2. 整理文档大纲
outline = """
# 零碳园区项目申报文档

## 一、项目概况
- 项目名称
- 建设地点
- 投资规模

## 二、技术方案
- 光伏系统
- 储能系统
- 充电桩

## 三、投资估算
- 总投资
- 分项投资
"""

# 3. 保存记忆
memory.add(
    content=f"已创建申报文档：{outline}",
    tags=["文档创建", "完成"],
    project="零碳园区"
)
```

### 3.2 自动任务总结技能

**场景**: 任务完成后自动总结

```python
# 触发词："总结任务"
# 技能自动执行：

from kunnix import TaskOrchestrator

task_manager = TaskOrchestrator()

# 获取已完成任务
completed = task_manager.list_tasks(status="completed")

# 生成总结
for task in completed:
    summary = f"""
任务：{task.title}
状态：{task.status}
完成时间：{task.updated_at}
项目：{task.project}
    """
    print(summary)
```

---

## 4. 多 Agent 协作

### 4.1 MasterMind 专家大脑集成

**场景**: 多专家协作提供专业建议

```python
from kunnix import MemorySystem

memory = MemorySystem()

# 1. 存储专家知识
expert_knowledge = [
    {
        "expert": "Jeffrey Bland",
        "field": "功能医学",
        "knowledge": "功能医学七大系统：消化、免疫、内分泌...",
        "tags": ["功能医学", "专家知识"]
    },
    {
        "expert": "零碳专家",
        "field": "新能源",
        "knowledge": "零碳园区四大核心：光伏、储能、充电桩、能效管理",
        "tags": ["零碳园区", "专家知识"]
    }
]

for item in expert_knowledge:
    memory.add(
        content=item["knowledge"],
        tags=item["tags"],
        metadata={"expert": item["expert"], "field": item["field"]}
    )

# 2. 检索专家建议
def query_expert(field, question):
    results = memory.search(
        f"{field} {question}",
        filters={"tags": ["专家知识"]},
        limit=3
    )
    return results

# 使用
advice = query_expert("功能医学", "如何改善肠道健康？")
```

### 4.2 跨 Agent 记忆共享

**场景**: 多个 Agent 共享同一记忆库

```python
from kunnix import MemorySystem

# 所有 Agent 使用同一数据库
shared_memory = MemorySystem(
    db_path="./shared_knowledge",
    top_k=5
)

# Agent A 添加记忆
shared_memory.add(
    content="用户偏好：喜欢简洁的代码风格",
    tags=["用户偏好"],
    metadata={"agent": "assistant_a"}
)

# Agent B 检索记忆
prefs = shared_memory.search("用户偏好")
print(f"发现 {len(prefs)} 条用户偏好")

# Agent C 也使用同样的记忆
```

---

## 5. 企业级应用

### 5.1 团队知识库

**场景**: 构建团队共享知识库

```python
from kunnix import MemorySystem

# 团队知识库
team_memory = MemorySystem(
    db_path="./team_knowledge",
    top_k=10
)

# 添加团队文档
team_memory.add(
    content="团队编码规范：Python 使用 black 格式化，行宽 88 字符",
    tags=["编码规范", "Python"],
    metadata={
        "department": "技术部",
        "created_by": "技术总监",
        "version": "1.0"
    }
)

# 按部门过滤
tech_docs = team_memory.search(
    "编码规范",
    filters={"metadata.department": "技术部"}
)
```

### 5.2 客户服务支持

**场景**: 智能客服知识库

```python
from kunnix import MemorySystem

kb = MemorySystem(db_path="./customer_support")

# 添加 FAQ
faqs = [
    ("如何安装 Kunnix？", "pip install kunnix"),
    ("支持哪些操作系统？", "Windows/macOS/Linux"),
    ("如何配置数据库？", "创建.env 文件设置 KUNNIX_DB_PATH"),
]

for question, answer in faqs:
    kb.add(
        content=f"Q: {question}\nA: {answer}",
        tags=["FAQ", "客服"],
        metadata={"category": "常见问题"}
    )

# 智能问答
def answer_question(user_question):
    results = kb.search(user_question, limit=3)
    if results:
        return results[0]["content"]
    return "抱歉，暂未找到相关答案"

# 使用
answer = answer_question("怎么安装？")
print(answer)
```

---

## 🎯 最佳实践

### 1. 记忆组织

✅ **推荐**:
- 使用标签分类（3-5 个标签）
- 添加项目元数据
- 定期清理旧记忆

❌ **避免**:
- 标签过多（>10 个）
- 不添加元数据
- 从不清理

### 2. 任务管理

✅ **推荐**:
- 任务命名：动词 + 名词
- 设置合理优先级
- 及时更新状态

❌ **避免**:
- 任务描述模糊
- 优先级全是"高"
- 创建后不管

### 3. 性能优化

```python
# 批量操作
memory.add_batch(memories)  # 比单个添加快 10 倍

# 使用缓存
@cache.ttl_cache(maxsize=1024, ttl=3600)
def expensive_operation():
    ...

# 异步处理
async def process_async():
    results = await memory.search_async(query)
```

---

## 📖 相关文档

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [系统架构](architecture.md)
- [API 参考](api.md)
