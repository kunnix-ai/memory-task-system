# Kunnix 安装指南

> 详细的安装步骤和配置说明

## 📋 系统要求

- **Python**: 3.10+
- **操作系统**: Windows / macOS / Linux
- **内存**: 至少 4GB RAM
- **存储**: 至少 1GB 可用空间

## 🚀 安装方式

### 方式 1：pip 安装（推荐）

```bash
pip install kunnix
```

### 方式 2：从源码安装

```bash
# 1. 克隆仓库
git clone https://github.com/kunnix-ai/memory-task-system.git
cd memory-task-system

# 2. 安装依赖
pip install -e .

# 3. 验证安装
python -c "import kunnix; print(kunnix.__version__)"
```

## ⚙️ 配置

### 环境变量

创建 `.env` 文件（项目根目录）：

```bash
# 数据库配置
KUNNIX_DB_PATH=~/.kunnix/database

# API 密钥（如使用云服务）
KUNNIX_API_KEY=your_api_key_here

# 日志级别
KUNNIX_LOG_LEVEL=INFO
```

### 配置文件

创建 `kunnix_config.yaml`：

```yaml
memory:
  db_path: ~/.kunnix/database
  embedding_model: text2vec-base-chinese
  top_k: 10
  
task:
  auto_archive: true
  archive_after_days: 30
  
skill:
  auto_learn: true
  min_confidence: 0.7
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

**Q: 数据库初始化失败？**
```bash
# 检查目录权限
chmod -R 755 ~/.kunnix
```

**Q: 导入错误？**
```bash
# 重新安装
pip uninstall kunnix
pip install kunnix
```

## 📚 下一步

- [快速开始](quickstart.md)
- [系统架构](architecture.md)
- [API 参考](api.md)
