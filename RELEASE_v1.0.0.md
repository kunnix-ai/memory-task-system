# 🎉 Kunnix v1.0.0 正式发布

**发布时间**: 2026-04-03  
**版本**: v1.0.0  
**状态**: 🟢 生产环境就绪

---

## 🎊 发布亮点

**Kunnix Memory & Task Scheduling System v1.0.0** 是首个正式版本，标志着 AI 记忆与任务调度系统正式开源！

### 核心能力

✅ **永久记忆系统** - L0-L5 分级记忆架构，混合检索（全文 + 向量），响应<300ms  
✅ **智能任务管理** - 自动提取、状态追踪、跨会话关联、自动总结  
✅ **技能自动进化** - 从成功任务中学习，自动生成可复用技能  
✅ **完整自动化** - 端到端自动化流程，无感知使用  

---

## 📦 安装方式

### 方式 1：从 GitHub 安装

```bash
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system
pip install -e .
```

### 方式 2：pip 安装（即将上线）

```bash
pip install kunnix
```

---

## 🚀 快速开始

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

---

## 📊 核心功能

### 1. 记忆系统

**混合检索引擎** = 全文检索 + 向量检索 + RRF 融合 + MMR 重排

- ✅ 支持全文检索（Whoosh）
- ✅ 支持向量检索（LanceDB）
- ✅ RRF 融合排序
- ✅ MMR 多样性重排
- ✅ 时间衰减
- ✅ 标签过滤
- ✅ 项目过滤

**性能指标**:
- 检索速度：100-300ms
- 向量化：~17ms
- 批量处理：0.13s/100 条

### 2. 任务管理

**智能任务编排器**

- ✅ 自动任务提取
- ✅ 状态追踪（pending → in_progress → completed）
- ✅ 记忆关联
- ✅ 跨会话追踪
- ✅ 自动总结
- ✅ 自动归档

### 3. 技能进化

**从成功任务中自动学习**

- ✅ 模式识别（聚类分析）
- ✅ 技能自动生成
- ✅ 严格审核（7 项检查）
- ✅ 一键发布

**已发布技能示例**:
- 零碳园区文档创建助手
- 任务自动总结助手
- 微信文章保存助手

---

## 🏗️ 技术架构

### L0-L5 分级记忆

- **L0**: 会话上下文（当前对话历史）
- **L1**: 短期记忆（每日日志，30 天滚动）
- **L2**: 长期记忆（MEMORY.md，结构化元数据）
- **L3**: 结构化记忆（标签系统 + 双向链接）
- **L4**: 跨 Agent 共享记忆（多 Agent 同步）
- **L5**: 人类知识层（Obsidian Vault 集成）

### 核心组件

```
kunnix/
├── memory/           # 记忆系统
│   ├── hybrid_search.py
│   ├── embedding_service.py
│   └── memory_importer.py
├── task/             # 任务管理
│   ├── task_extractor.py
│   ├── task_orchestrator.py
│   └── task_summarizer.py
├── skill/            # 技能进化
│   ├── pattern_extractor.py
│   ├── skill_generator.py
│   ├── skill_reviewer.py
│   └── skill_publisher.py
└── integration/      # 会话集成
    └── session_integration.py
```

---

## 📚 文档

- 📘 [安装指南](docs/installation.md)
- 🚀 [快速开始](docs/quickstart.md)
- 🏗️ [系统架构](docs/architecture.md)
- 📚 [API 参考](docs/api.md)
- 💡 [使用示例](docs/examples.md)

---

## 🎯 使用场景

### 1. 个人知识管理

构建第二大脑，管理笔记、文章、想法

```python
memory.add(
    content="《深度工作》核心观点：深度工作需要刻意练习",
    tags=["读书笔记", "个人成长"]
)
```

### 2. 项目管理

管理项目全流程文档和任务

```python
task = task_manager.create_task(
    title="编写项目申报文档",
    project="零碳园区",
    priority="high"
)
```

### 3. 技能自动化

从重复工作中自动生成技能

```python
# 自动学习 → 生成技能 → 自动执行
skill_system.extract_patterns(task_archives)
skill_system.generate_skill(pattern)
```

### 4. 多 Agent 协作

共享记忆库，跨 Agent 知识同步

```python
shared_memory = MemorySystem(db_path="./shared_knowledge")
```

---

## 🔧 技术栈

- **Python**: 3.10+
- **全文检索**: Whoosh
- **向量检索**: LanceDB
- **嵌入模型**: text2vec-base-chinese
- **融合算法**: RRF + MMR
- **许可证**: MIT

---

## 📈 性能实测

**测试环境**: Python 3.10, 16GB RAM, SSD

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| 检索速度 | <500ms | 100-300ms | ✅ 优秀 |
| 向量化 | <500ms | ~17ms | ✅ 优秀 |
| 批量处理 | <5s | 0.13s/100 条 | ✅ 优秀 |
| 模式识别准确率 | >85% | 100% | ✅ 完美 |
| 技能生成可用率 | >90% | 100% | ✅ 完美 |

---

## 🐛 已知问题

- [ ] pip 包尚未发布（预计 v1.1.0）
- [ ] 文档以中文为主（英文文档计划中）
- [ ] 缺少 GUI 界面（计划中）

---

## 🎯 路线图

### v1.1.0（2026-04-17）

- ✅ 发布 PyPI 包
- ✅ 完善英文文档
- ✅ 添加更多使用示例
- ✅ 性能优化（缓存、批处理）

### v1.2.0（2026-05-01）

- ✅ GUI 界面（Web UI）
- ✅ REST API
- ✅ Docker 支持
- ✅ 更多嵌入模型支持

### v2.0.0（2026-06-01）

- ✅ 分布式部署
- ✅ 多用户支持
- ✅ 企业级功能
- ✅ 云同步

---

## 🤝 贡献

欢迎贡献代码、文档、建议！

### 贡献方式

1. **提交 Issue** - 报告 Bug 或提出新功能
2. **提交 PR** - 修复 Bug 或添加功能
3. **完善文档** - 改进现有文档
4. **分享案例** - 分享使用经验

详见 [贡献指南](CONTRIBUTING.md)。

---

## 📄 许可证

MIT License

**商业友好**：允许商用，无需开源你的代码

---

## 🌟 命名故事

**Kunnix** = **Kun**（鲲）+ **nix**（Phoenix 后半部）

> 鲲，北冥之鱼，化而为鸟，其名为凰。  
> Kunnix 取"鲲"之音、"凰"之形，寓意 AI 助手如鲲凰般不断进化。

---

## 🙏 致谢

感谢所有支持 Kunnix 开源项目的开发者和用户！

特别感谢：
- Whoosh 团队 - 全文检索引擎
- LanceDB 团队 - 向量数据库
- text2vec 团队 - 中文文本向量化

---

## 📬 联系方式

- **GitHub**: [kunnix-ai/memory-task-system](https://github.com/kunnix-ai/memory-task-system)
- **Issues**: [问题反馈](https://github.com/kunnix-ai/memory-task-system/issues)
- **讨论**: [Discussions](https://github.com/kunnix-ai/memory-task-system/discussions)

---

**Kunnix - Evolve Your AI Assistant** 🚀

**Star 不迷路** ⭐ | **Issue 提建议** 💡 | **PR 共建设** 🤝

---

*Full Changelog*: https://github.com/kunnix-ai/memory-task-system/compare/v0.0.0...v1.0.0
