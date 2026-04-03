# 安装指南

> 详细的安装步骤和配置说明

## 📋 系统要求

- **Python**: 3.10+
- **操作系统**: Windows / macOS / Linux
- **内存**: 至少 4GB RAM
- **存储**: 至少 1GB 可用空间

## 🚀 安装方式

### 方式 1：从源码安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system

# 2. 安装依赖
pip install -e .

# 3. 验证安装
python -c "import kunnix; print(kunnix.__version__)"
```

### 方式 2：pip 安装（即将上线）

```bash
pip install kunnix
```

## ⚙️ 配置

### 环境变量

创建 `.env` 文件：

```bash
# 数据库配置
KUNNIX_DB_PATH=~/.kunnix/database

# 日志级别
KUNNIX_LOG_LEVEL=INFO
```

## ✅ 验证安装

```python
from kunnix import MemorySystem

# 初始化
memory = MemorySystem()

# 测试检索
results = memory.search("测试", limit=5)
print(f"找到 {len(results)} 条结果")
```

## 🔧 故障排查

### 常见问题

**Q: 安装时提示依赖冲突？**
```bash
pip install --upgrade pip
pip install kunnix --no-deps
```

**Q: 导入错误？**
```bash
# 重新安装
pip uninstall kunnix
pip install kunnix
```

## 📚 下一步

- [快速开始](/guide/quickstart)
- [什么是 Kunnix](/guide/what-is-kunnix)
