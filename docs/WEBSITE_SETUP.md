# Kunnix 网站部署指南

> 使用 VitePress 构建的现代化文档网站

## 📦 目录结构

```
kunnix/
├── docs/
│   ├── .vitepress/          # VitePress 配置
│   │   ├── config.mjs       # 网站配置
│   │   ├── theme/           # 自定义主题
│   │   │   ├── index.js
│   │   │   └── style.css
│   │   └── dist/            # 构建输出（自动生成）
│   ├── public/              # 静态资源
│   │   └── logo.svg
│   ├── guide/               # 指南文档
│   ├── api/                 # API 文档
│   ├── examples/            # 使用示例
│   ├── blog/                # 博客文章
│   └── index.md             # 首页
├── .github/workflows/       # GitHub Actions
│   └── deploy.yml           # 自动部署配置
└── package.json             # Node.js 配置
```

## 🚀 本地开发

### 1. 安装 Node.js

确保已安装 Node.js 20+：

```bash
node --version  # 应显示 v20.x.x 或更高
```

如未安装，访问 https://nodejs.org 下载安装。

### 2. 安装依赖

```bash
cd kunnix
npm install
```

### 3. 启动开发服务器

```bash
npm run docs:dev
```

访问 http://localhost:5173 查看网站。

### 4. 实时预览

```bash
npm run docs:preview
```

## 📤 部署到 GitHub Pages

### 方式 1：自动部署（推荐）

GitHub Actions 会自动部署：

1. 推送到 main 分支
2. 触发 `.github/workflows/deploy.yml`
3. 自动构建并部署到 GitHub Pages

**访问地址**: https://kunnix-ai.github.io/memory-task-system

### 方式 2：手动部署

```bash
# 1. 构建
npm run docs:build

# 2. 进入构建目录
cd docs/.vitepress/dist

# 3. 初始化 Git（如未初始化）
git init

# 4. 添加所有文件
git add .

# 5. 提交
git commit -m "Deploy documentation"

# 6. 推送到 gh-pages 分支
git push -f git@github.com:kunnix-ai/memory-task-system.git master:gh-pages
```

## ⚙️ 配置 GitHub Pages

1. 访问仓库 Settings
2. 进入 Pages 设置
3. Source 选择 `gh-pages` 分支
4. Folder 选择 `/ (root)`
5. 保存后等待几分钟

## 🎨 自定义主题

### 修改配色

编辑 `docs/.vitepress/theme/style.css`：

```css
:root {
  --vp-c-brand-1: #1E88E5;  /* 鲲蓝 */
  --vp-c-brand-2: #1565C0;
  --vp-c-accent: #FF7043;   /* 凰橙 */
}
```

### 修改导航

编辑 `docs/.vitepress/config.mjs`：

```javascript
nav: [
  { text: '首页', link: '/' },
  { text: '指南', link: '/guide/what-is-kunnix' },
  // 添加更多导航项...
]
```

### 添加新页面

在对应目录创建 `.md` 文件：

```bash
# 创建指南文档
echo "# 新页面" > docs/guide/new-page.md

# 创建示例文档
echo "# 新示例" > docs/examples/new-example.md
```

## 📊 性能优化

### 图片优化

- 使用 WebP 格式
- 压缩图片（TinyPNG）
- 使用响应式图片

### 构建优化

```bash
# 分析构建大小
npm run docs:build -- --debug

# 预览构建结果
npm run docs:preview
```

## 🔍 故障排查

### 问题：构建失败

```bash
# 清理缓存
rm -rf node_modules package-lock.json
npm install
npm run docs:build
```

### 问题：本地预览正常，部署后异常

检查：
1. 所有路径是否使用相对路径
2. 静态资源是否在 `public/` 目录
3. GitHub Actions 日志是否有错误

### 问题：GitHub Pages 404

等待几分钟，GitHub Pages 需要时间构建。
检查 Settings → Pages 是否配置正确。

## 📚 相关资源

- [VitePress 官方文档](https://vitepress.dev)
- [VitePress 中文文档](https://vitepress.docschina.org)
- [GitHub Pages 文档](https://pages.github.com)

## 🤝 贡献

欢迎改进网站！

1. Fork 仓库
2. 创建分支 `git checkout -b feature/website-improvement`
3. 提交更改 `git commit -m "Add website improvement"`
4. 推送到分支 `git push origin feature/website-improvement`
5. 提交 Pull Request

---

**Kunnix Documentation Website** 🚀

Built with VitePress and ❤️
