# 什么是 Kunnix？

> Kunnix 是一个完整的 AI 记忆与任务调度系统，为 AI 助手提供永久记忆、任务管理和技能进化能力。

## 🎯 核心理念

**Kunnix** 的名字来源于中国古代神话：
- **鲲（Kun）** - 北冥之鱼，代表博大、深邃、变化
- **凰（Phoenix）** - 神话中的凤凰，代表涅槃、重生、进化
- **Kunnix** = 鲲 + 凰，寓意 AI 助手如鲲凰般不断进化

> 鲲，北冥之鱼，化而为鸟，其名为凰。  
> Kunnix 取"鲲"之音、"凰"之形，让 AI 拥有记忆与进化能力。

## 🧠 核心能力

### 1. 永久记忆系统

Kunnix 提供 **L0-L5 分级记忆架构**：

- **L0** - 会话上下文（当前对话历史）
- **L1** - 短期记忆（每日日志，30 天滚动）
- **L2** - 长期记忆（MEMORY.md，结构化元数据）
- **L3** - 结构化记忆（标签系统 + 双向链接）
- **L4** - 跨 Agent 共享记忆（多 Agent 同步）
- **L5** - 人类知识层（Obsidian Vault 集成）

**混合检索引擎** = 全文检索（Whoosh）+ 向量检索（LanceDB）+ RRF 融合 + MMR 重排

**性能指标**:
- 检索速度：**100-300ms**
- 向量化：**~17ms**
- 批量处理：**0.13s/100 条**

### 2. 智能任务管理

**任务编排器**提供完整的任务生命周期管理：

```
pending → in_progress → reviewing → completed → archived
```

- ✅ 自动任务提取
- ✅ 状态追踪
- ✅ 记忆关联
- ✅ 跨会话追踪
- ✅ 自动总结
- ✅ 自动归档

### 3. 技能自动进化

从成功任务中自动学习，生成可复用的自动化技能：

```
任务完成 → 模式识别 → 技能生成 → 审核 → 发布 → 自动执行
```

**已发布技能示例**:
- 零碳园区文档创建助手
- 任务自动总结助手
- 微信文章保存助手

## 🎯 解决什么痛点？

| 痛点 | Kunnix 解决方案 |
|------|----------------|
| ❌ AI 助手没有记忆，每次对话从零开始 | ✅ **永久记忆系统**，跨会话知识积累 |
| ❌ 任务管理混乱，难以追踪进度 | ✅ **智能任务编排**，自动提取 + 关联 + 总结 |
| ❌ 重复工作多，效率低下 | ✅ **技能自动进化**，从成功任务中学习 |
| ❌ 数据孤岛，知识难以复用 | ✅ **混合检索**，快速定位所需信息 |

## 🚀 核心价值

> **Kunnix 不仅是一个工具，更是 AI 助手的"外挂大脑"和"进化引擎"**

### 对个人用户

- 🧠 **构建第二大脑** - 管理笔记、文章、想法
- 📋 **提升工作效率** - 自动化重复任务
- 📚 **知识高效复用** - 快速检索所需信息

### 对开发者

- 🔧 **代码记忆管理** - 管理 10 万行代码的记忆
- 🤖 **技能自动化** - 自动生成开发工具
- 📊 **项目知识沉淀** - 团队协作知识库

### 对企业

- 🏢 **团队知识库** - 构建企业知识资产
- 🔄 **流程自动化** - 标准化工作流自动执行
- 📈 **效率提升** - 减少重复劳动，提高生产力

## 📦 快速开始

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
```

## 📚 下一步

- [快速开始](/guide/quickstart) - 5 分钟上手教程
- [安装指南](/guide/installation) - 详细安装步骤
- [系统架构](/guide/architecture) - 深入理解内部原理
- [使用示例](/examples/basic) - 实战案例

## 🤝 参与贡献

欢迎加入 Kunnix 社区！

- 🐛 [提交 Issue](https://github.com/kunnix-ai/memory-task-system/issues)
- 🔧 [提交 PR](https://github.com/kunnix-ai/memory-task-system/pulls)
- 💬 [参与讨论](https://github.com/kunnix-ai/memory-task-system/discussions)

---

**Kunnix - Evolve Your AI Assistant** 🚀
