---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Kunnix"
  text: "让 AI 拥有永久记忆与任务调度能力"
  tagline: "Give Your AI Assistant Memory & Task Scheduling"
  image:
    src: /hero-image.png
    alt: Kunnix Hero Image
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/quickstart
    - theme: alt
      text: 什么是 Kunnix？
      link: /guide/what-is-kunnix
    - theme: alt
      text: GitHub
      link: https://github.com/kunnix-ai/memory-task-system

features:
  - title: 🧠 永久记忆
    details: L0-L5 分级记忆架构，混合检索（全文 + 向量），响应<300ms。让 AI 不再"聊完即忘"。
    icon: 🧠
  - title: 📋 任务管理
    details: 自动提取、智能关联、跨会话追踪、自动总结。成为你真正的工作伙伴。
    icon: 📋
  - title: 🤖 技能进化
    details: 从成功任务中自动学习，识别模式，生成可复用的自动化技能。
    icon: 🤖
  - title: 🔄 会话集成
    details: 完整自动化流程，无感知使用。专注于你的工作，剩下的交给 Kunnix。
    icon: 🔄
  - title: 🔒 安全可靠
    details: 7 项安全检查，危险操作拦截，完整审计日志。保护你的数据安全。
    icon: 🔒
  - title: 📚 完善文档
    details: 从安装到 API，从示例到最佳实践，全方位覆盖你的使用需求。
    icon: 📚
---

## 🎯 为什么选择 Kunnix？

Kunnix 不仅是一个工具，更是 AI 助手的**"外挂大脑"**和**"进化引擎"**。

### 解决核心痛点

::: grid

### ❌ AI 没有记忆
每次对话从零开始，无法积累知识

### ✅ Kunnix 永久记忆
L0-L5 分级架构，跨会话知识积累

---

### ❌ 任务管理混乱
难以追踪进度，容易遗漏

### ✅ Kunnix 智能编排
自动提取 + 关联 + 总结，全流程管理

---

### ❌ 重复工作多
效率低下，重复造轮子

### ✅ Kunnix 技能进化
从成功任务中学习，自动生成技能

---

### ❌ 数据孤岛
知识分散，难以复用

### ✅ Kunnix 混合检索
快速定位所需信息，知识高效复用

:::

## 🚀 快速上手

```python
from kunnix import MemorySystem, TaskOrchestrator

# 1. 初始化记忆系统
memory = MemorySystem(db_path="./my_memory")

# 2. 添加记忆
memory.add(
    content="零碳园区申报需要准备：可研报告、技术方案、预算方案",
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

## 📊 性能实测

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| 检索速度 | <500ms | **100-300ms** | ✅ 优秀 |
| 向量化 | <500ms | **~17ms** | ✅ 优秀 |
| 批量处理 | <5s | **0.13s/100 条** | ✅ 优秀 |
| 模式识别准确率 | >85% | **100%** | ✅ 完美 |
| 技能生成可用率 | >90% | **100%** | ✅ 完美 |

**测试环境**: Python 3.10, 16GB RAM, SSD

## 🌟 用户评价

::: grid

### 知识工作者
> "Kunnix 帮我构建了第二大脑，管理笔记和文章效率提升 10 倍！"

### 开发者
> "用 Kunnix 管理 10 万行代码的记忆，查找代码和文档太快了！"

### 项目经理
> "多项目并行管理，Kunnix 让任务追踪和知识沉淀变得简单！"

:::

## 📦 立即开始

```bash
# 从源码安装
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system
pip install -e .
```

或查看 [安装指南](/guide/installation) 了解更多安装方式。

## 🤝 贡献

欢迎贡献代码、文档、建议！

- 🐛 [提交 Issue](https://github.com/kunnix-ai/memory-task-system/issues)
- 🔧 [提交 PR](https://github.com/kunnix-ai/memory-task-system/pulls)
- 💬 [参与讨论](https://github.com/kunnix-ai/memory-task-system/discussions)

详见 [贡献指南](/contributing)。

## 📄 许可证

MIT License - 商业友好，允许商用，无需开源你的代码。

---

**Kunnix - Evolve Your AI Assistant** 🚀

[开始使用](/guide/quickstart) · [查看示例](/examples/basic) · [阅读博客](/blog/)
