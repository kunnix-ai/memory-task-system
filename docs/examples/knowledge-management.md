# 个人知识管理

> 使用 Kunnix 构建第二大脑

## 🧠 场景说明

知识工作者需要管理大量笔记、文章、想法。

## 📚 使用示例

```python
from kunnix import MemorySystem

memory = MemorySystem(db_path="./my_brain")

# 添加读书笔记
memory.add(
    content="《深度工作》核心观点：深度工作需要刻意练习",
    tags=["读书笔记", "个人成长"],
    metadata={"book": "深度工作"}
)

# 添加文章摘要
memory.add(
    content="AI 记忆系统三大核心：存储、检索、进化",
    tags=["AI", "技术文章"]
)

# 检索
results = memory.search("AI 记忆系统", limit=5)
```

## 📖 相关示例

- [基础示例](/examples/basic)
- [项目管理](/examples/project-management)
