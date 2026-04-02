# Kunnix Memory & Task Scheduling System

> **让 AI 拥有永久记忆与任务调度能力**  
> **Give Your AI Assistant Memory & Task Scheduling**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 简介

**Kunnix** 是一个完整的 AI 记忆与任务调度系统，为 AI 助手提供：

- 🧠 **永久记忆** - L0-L5 分级记忆架构，混合检索（全文 + 向量）
- 📋 **任务管理** - 自动提取、智能关联、自动总结、跨会话追踪
- 🚀 **技能进化** - 从成功任务中自动学习，生成新技能
- 🔄 **会话集成** - 完整自动化流程，无感知使用

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

### 基础使用

```python
from kunnix import MemorySystem, TaskOrchestrator

# 初始化记忆系统
memory = MemorySystem()

# 记忆检索
results = memory.search("查询内容", limit=10)

# 任务管理
task_manager = TaskOrchestrator()
task = task_manager.create_task("创建申报文档", auto_start=True)
```

## 📚 核心模块

### 1. 记忆系统（Memory）

- 混合检索（Whoosh + LanceDB）
- RRF 融合排序
- MMR 重排
- 时间衰减

### 2. 任务管理（Task）

- 自动任务提取
- 记忆关联
- 状态追踪
- 自动总结归档

### 3. 技能进化（Skill）

- 模式识别
- 技能自动生成
- 审核发布流程

## 📊 性能指标

| 指标 | 目标值 | 实测值 |
|------|--------|--------|
| 检索速度 | <500ms | 100-260ms ✅ |
| 向量化 | <500ms | ~17ms ✅ |
| 批量处理 | <5s | 0.13s ✅ |

## 📖 文档

- [安装指南](docs/installation.md)
- [快速开始](docs/quickstart.md)
- [系统架构](docs/architecture.md)
- [API 参考](docs/api.md)
- [使用示例](docs/examples.md)

## 🤝 贡献

欢迎贡献代码、文档、建议！详见 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🌟 命名由来

**Kunnix** = **Kun**（鲲）+ **nix**（Phoenix 后半部）

> 鲲，北冥之鱼，化而为鸟，其名为凰。  
> Kunnix 取"鲲"之音、"凰"之形，寓意 AI 助手如鲲凰般不断进化。

---

**Kunnix - Evolve Your AI Assistant**
