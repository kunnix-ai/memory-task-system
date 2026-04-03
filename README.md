# 🚀 Kunnix Memory & Task Scheduling System

> **让 AI 拥有永久记忆与任务调度能力**  
> **Give Your AI Assistant Memory & Task Scheduling**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/kunnix-ai/memory-task-system.svg)](https://github.com/kunnix-ai/memory-task-system/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/kunnix-ai/memory-task-system.svg)](https://github.com/kunnix-ai/memory-task-system/issues)

---

## 🌟 特性亮点

- 🧠 **永久记忆** - L0-L5 分级记忆架构，混合检索（全文 + 向量），响应<300ms
- 📋 **任务管理** - 自动提取、智能关联、跨会话追踪、自动总结
- 🤖 **技能进化** - 从成功任务中自动学习，生成可复用的自动化技能
- 🔄 **会话集成** - 完整自动化流程，无感知使用
- 🔒 **安全可靠** - 7 项安全检查，危险操作拦截，完整审计日志

---

## 🎯 为什么选择 Kunnix？

### 痛点解决

| 痛点 | Kunnix 解决方案 |
|------|----------------|
| ❌ AI 助手没有记忆，每次对话从零开始 | ✅ **永久记忆系统**，跨会话知识积累 |
| ❌ 任务管理混乱，难以追踪进度 | ✅ **智能任务编排**，自动提取 + 关联 + 总结 |
| ❌ 重复工作多，效率低下 | ✅ **技能自动进化**，从成功任务中学习 |
| ❌ 数据孤岛，知识难以复用 | ✅ **混合检索**，快速定位所需信息 |

### 核心价值

> **Kunnix 不仅是一个工具，更是 AI 助手的"外挂大脑"和"进化引擎"**

---

## 🚀 快速开始

### 安装

```bash
# 方式 1：pip 安装（推荐）
pip install kunnix

# 方式 2：从源码安装
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system
pip install -e .
```

### 5 分钟上手

```python
from kunnix import MemorySystem, TaskOrchestrator

# 1. 初始化记忆系统
memory = MemorySystem(db_path="./my_memory")

# 2. 添加记忆
memory.add(
    content="零碳园区项目申报需要准备：可研报告、技术方案、预算方案",
    tags=["零碳园区", "申报文档"],
    project="零碳园区"
)

# 3. 检索记忆
results = memory.search("零碳园区申报", limit=5)
for r in results:
    print(f"{r['content']} (相似度：{r['score']:.2f})")

# 4. 创建任务
task_manager = TaskOrchestrator()
task = task_manager.create_task(
    title="编写零碳园区申报文档",
    project="零碳园区",
    auto_start=True
)

print(f"✅ 任务已创建：{task.title}")
```

---

## 📚 核心模块

### 1. 记忆系统（Memory）

**混合检索引擎** = 全文检索（Whoosh）+ 向量检索（LanceDB）+ RRF 融合 + MMR 重排

```python
from kunnix import MemorySystem

memory = MemorySystem()

# 添加记忆
memory.add("记忆内容", tags=["标签"], project="项目")

# 混合检索（全文 + 向量）
results = memory.search("查询内容", limit=10)

# 高级检索（带过滤）
results = memory.search(
    "查询",
    filters={"project": "零碳园区"},
    threshold=0.7
)
```

**性能指标**:
- 检索速度：**100-300ms**
- 向量化：**~17ms**
- 批量处理：**0.13s/100 条**

### 2. 任务管理（Task）

**智能任务编排器** - 自动提取、状态追踪、记忆关联、自动总结

```python
from kunnix import TaskOrchestrator

task_manager = TaskOrchestrator()

# 创建任务
task = task_manager.create_task(
    title="创建申报文档",
    description="准备项目申报所需全部文档",
    project="零碳园区",
    priority="high",
    auto_start=True
)

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

### 3. 技能进化（Skill）

**从成功任务中自动学习** → 识别模式 → 生成技能 → 审核发布 → 自动执行

```python
from kunnix import SkillEvolution

skill_system = SkillEvolution()

# 模式提取（从历史任务中学习）
patterns = skill_system.extract_patterns(
    task_archives=["./tasks/archives"],
    min_cluster_size=3,
    threshold=0.5
)

# 技能生成
skill = skill_system.generate_skill(patterns[0])

# 审核发布
review_result = skill_system.review_skill(skill["path"])
if review_result["status"] == "approved":
    skill_system.publish_skill(skill["path"])
    print(f"✅ 技能已发布：{skill['skill_name']}")
```

**已发布技能示例**:
- ✅ **零碳园区文档创建助手** - 基于 4 个零碳园区任务生成
- ✅ **任务自动总结助手** - 基于 10+ 个任务总结生成
- ✅ **微信文章保存助手** - 基于日常文章管理生成

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────┐
│          Kunnix Memory & Task System        │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │   Memory     │  │    Task      │        │
│  │   System     │  │  Orchestrator│        │
│  │              │  │              │        │
│  │  - Storage   │  │  - Create    │        │
│  │  - Search    │  │  - Track     │        │
│  │  - Index     │  │  - Archive   │        │
│  └──────────────┘  └──────────────┘        │
│         │                  │                │
│         └────────┬─────────┘                │
│                  │                          │
│         ┌────────▼────────┐                 │
│         │  Skill Evolution│                 │
│         │     System      │                 │
│         │                 │                 │
│         │  - Extract      │                 │
│         │  - Generate     │                 │
│         │  - Review       │                 │
│         │  - Publish      │                 │
│         └─────────────────┘                 │
└─────────────────────────────────────────────┘
```

### L0-L5 分级记忆架构

- **L0**: 会话上下文（当前对话历史）
- **L1**: 短期记忆（每日日志，30 天滚动）
- **L2**: 长期记忆（MEMORY.md，结构化元数据）
- **L3**: 结构化记忆（标签系统 + 双向链接）
- **L4**: 跨 Agent 共享记忆（多 Agent 同步）
- **L5**: 人类知识层（Obsidian Vault 集成）

---

## 📊 性能实测

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| 检索速度 | <500ms | **100-300ms** | ✅ 优秀 |
| 向量化 | <500ms | **~17ms** | ✅ 优秀 |
| 批量处理 | <5s | **0.13s/100 条** | ✅ 优秀 |
| 模式识别准确率 | >85% | **100%** | ✅ 完美 |
| 技能生成可用率 | >90% | **100%** | ✅ 完美 |

**测试环境**: Python 3.10, 16GB RAM, SSD

---

## 📖 文档

- 📘 [安装指南](docs/installation.md) - 详细安装步骤和配置
- 🚀 [快速开始](docs/quickstart.md) - 5 分钟上手教程
- 🏗️ [系统架构](docs/architecture.md) - 深入理解内部原理
- 📚 [API 参考](docs/api.md) - 完整 API 文档
- 💡 [使用示例](docs/examples.md) - 实战案例和最佳实践

---

## 🤝 贡献

欢迎贡献代码、文档、建议！

### 贡献方式

1. **提交 Issue** - 报告 Bug 或提出新功能
2. **提交 PR** - 修复 Bug 或添加功能
3. **完善文档** - 改进现有文档或添加示例
4. **分享案例** - 分享你的使用经验

详见 [贡献指南](CONTRIBUTING.md)。

### 贡献者

感谢所有为 Kunnix 做出贡献的开发者！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

**商业友好**：允许商用，无需开源你的代码

---

## 🌟 命名由来

**Kunnix** = **Kun**（鲲）+ **nix**（Phoenix 后半部）

> 鲲，北冥之鱼，化而为鸟，其名为凰。  
> Kunnix 取"鲲"之音、"凰"之形，寓意 AI 助手如鲲凰般不断进化。

**品牌故事**:
- 🐟 **鲲** - 中国古代神话中的巨鱼，代表博大、深邃、变化
- 🦅 **凰** - 凤凰，代表涅槃、重生、进化
- 🔄 **鲲化为凰** - 从鱼到鸟的蜕变，象征 AI 的持续进化能力

---

## 🎯 愿景

> **让每个 AI 都拥有记忆与进化能力**

Kunnix 不仅是一个技术项目，更是对 AI 助手未来的探索：
- 让 AI 拥有**永久记忆**，不再"聊完即忘"
- 让 AI 具备**任务管理能力**，成为真正的工作伙伴
- 让 AI 能够**持续进化**，从每次互动中学习成长

---

## 📬 联系方式

- **GitHub**: [kunnix-ai/memory-task-system](https://github.com/kunnix-ai/memory-task-system)
- **Issues**: [问题反馈](https://github.com/kunnix-ai/memory-task-system/issues)
- **讨论**: [Discussions](https://github.com/kunnix-ai/memory-task-system/discussions)

---

## 🙏 致谢

感谢以下开源项目：

- [Whoosh](https://github.com/whoosh-search/whoosh) - 全文检索引擎
- [LanceDB](https://github.com/lancedb/lancedb) - 向量数据库
- [text2vec](https://github.com/shibing624/text2vec) - 中文文本向量化

---

**Kunnix - Evolve Your AI Assistant** 🚀

**Star 不迷路** ⭐ | **Issue 提建议** 💡 | **PR 共建设** 🤝
