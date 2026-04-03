# 记忆系统

> Kunnix 核心模块：永久记忆存储和检索

## 🧠 核心功能

- 混合检索（全文 + 向量）
- L0-L5 分级架构
- RRF 融合 + MMR 重排

## 🚀 快速开始

```python
from kunnix import MemorySystem

memory = MemorySystem()
memory.add("记忆内容", tags=["标签"])
results = memory.search("查询", limit=5)
```

## 📚 详细文档

- [API 参考](/api/memory-system)
- [使用示例](/examples/basic)

*（文档完善中，敬请期待）*
