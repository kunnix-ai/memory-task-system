# Kunnix 系统架构

> 深入了解 Kunnix 的内部设计和技术原理

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────┐
│            Kunnix Memory & Task System          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Memory     │  │    Task      │            │
│  │   System     │  │  Orchestrator│            │
│  │              │  │              │            │
│  │  - Storage   │  │  - Create    │            │
│  │  - Search    │  │  - Track     │            │
│  │  - Index     │  │  - Archive   │            │
│  └──────────────┘  └──────────────┘            │
│         │                  │                    │
│         └────────┬─────────┘                    │
│                  │                              │
│         ┌────────▼────────┐                     │
│         │  Skill Evolution│                     │
│         │     System      │                     │
│         │                 │                     │
│         │  - Extract      │                     │
│         │  - Generate     │                     │
│         │  - Review       │                     │
│         │  - Publish      │                     │
│         └─────────────────┘                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 📊 核心模块

### 1. 记忆系统（Memory System）

**职责**: 提供 AI 助手的永久记忆存储和检索能力

**核心组件**:
```
kunnix/memory/
├── hybrid_search.py       # 混合检索引擎
├── embedding_service.py   # 向量化服务
├── memory_importer.py     # 记忆导入器
└── memory_search_skill.py # 记忆检索技能
```

**技术栈**:
- **全文检索**: Whoosh
- **向量检索**: LanceDB
- **嵌入模型**: text2vec-base-chinese
- **融合算法**: RRF（Reciprocal Rank Fusion）

**工作流程**:
```
用户查询 → 查询理解 → 全文检索 + 向量检索 → RRF 融合 → MMR 重排 → 返回结果
```

### 2. 任务管理系统（Task Orchestration）

**职责**: 自动化任务的创建、追踪和归档

**核心组件**:
```
kunnix/task/
├── task_extractor.py       # 任务自动提取
├── task_orchestrator.py    # 任务编排器
├── task_summarizer.py      # 任务自动总结
└── memory_linker.py        # 记忆关联器
```

**任务状态机**:
```
pending → in_progress → reviewing → completed
                ↓
            archived
```

### 3. 技能进化系统（Skill Evolution）

**职责**: 从成功任务中自动学习，生成新技能

**核心组件**:
```
kunnix/skill/
├── pattern_extractor.py    # 模式提取器
├── skill_generator.py      # 技能生成器
├── skill_reviewer.py       # 技能审核器
└── skill_publisher.py      # 技能发布器
```

**进化流程**:
```
任务完成 → 模式识别 → 技能生成 → 审核 → 发布 → 使用
```

## 🔍 记忆系统详解

### L0-L5 分级记忆架构

```
L0: 会话上下文（Session Context）
    └─ 当前对话历史（自动注入）

L1: 短期记忆（Short-term Memory）
    └─ 每日日志（30 天滚动）

L2: 长期记忆（Long-term Memory）
    └─ MEMORY.md（结构化元数据）

L3: 结构化记忆（Structured Memory）
    └─ 标签系统 + 双向链接

L4: 跨 Agent 共享记忆（Shared Memory）
    └─ 多 Agent 同步机制

L5: 人类知识层（Human Knowledge）
    └─ Obsidian Vault 集成
```

### 混合检索算法

**步骤 1: 双路检索**
```python
# 全文检索（Whoosh）
bm25_results = whoosh_search(query, top_k=50)

# 向量检索（LanceDB）
vector_results = lancedb_search(query_embedding, top_k=50)
```

**步骤 2: RRF 融合**
```python
# 倒数排名融合
def rrf_score(rank, k=60):
    return 1 / (k + rank)

# 合并分数
for doc in all_docs:
    doc['rrf_score'] = rrf_score(doc['rank_bm25']) + \
                       rrf_score(doc['rank_vector'])
```

**步骤 3: MMR 重排**
```python
# 最大边界相关（多样性）
final_results = mmr_rerank(
    candidates, 
    query_embedding,
    lambda_param=0.5  # 相关性 vs 多样性
)
```

## ⚡ 性能优化

### 1. 缓存策略

```python
# TTL 缓存（时间 + 容量）
@cache.ttl_cache(maxsize=1024, ttl=3600)
def get_embedding(text):
    return model.encode(text)
```

### 2. 批量处理

```python
# 批量向量化
embeddings = model.encode_batch(
    texts, 
    batch_size=32
)
```

### 3. 异步 IO

```python
# 异步数据库操作
async def search_async(query):
    results = await db.search(query)
    return results
```

## 🔒 安全机制

### 1. 数据隔离

- 每个项目独立数据库
- 敏感数据加密存储
- 访问权限控制

### 2. 操作审计

- 所有检索操作记录日志
- 技能执行前安全检查
- 危险操作拦截

### 3. 错误处理

```python
try:
    result = memory.search(query)
except MemoryError as e:
    logger.error(f"记忆检索失败：{e}")
    result = []
```

## 📈 扩展性设计

### 水平扩展

- 支持分布式部署
- 数据库分片
- 负载均衡

### 垂直扩展

- 插件化架构
- 自定义检索器
- 自定义嵌入模型

## 🎯 设计原则

1. **模块化**: 每个组件职责单一
2. **可扩展**: 易于添加新功能
3. **高性能**: 响应时间<500ms
4. **易用性**: 简洁的 API 设计
5. **可靠性**: 完善的错误处理

## 📚 相关文档

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [API 参考](api.md)
- [使用示例](examples.md)
