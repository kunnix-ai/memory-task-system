import { defineConfig } from 'vitepress'

export default defineConfig({
  // 站点配置
  title: 'Kunnix',
  titleTemplate: ':title - Kunnix',
  description: '让 AI 拥有永久记忆与任务调度能力',
  
  // GitHub Pages 基础路径（重要！）
  base: '/memory-task-system/',
  
  // 语言和主题
  lang: 'zh-CN',
  themeConfig: {
    logo: {
      src: '/logo.svg',
      alt: 'Kunnix Logo'
    },
    
    // 导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide/what-is-kunnix' },
      { text: 'API', link: '/api/memory-system' },
      { text: '示例', link: '/examples/basic' },
      { text: '博客', link: '/blog/' },
      { 
        text: '生态', 
        items: [
          { text: '技能系统', link: '/guide/skill-evolution' },
          { text: '任务管理', link: '/guide/task-management' },
          { text: '贡献指南', link: '/contributing' }
        ]
      },
      { 
        text: 'v1.0.0', 
        items: [
          { text: '更新日志', link: '/changelog' },
          { text: '发布说明', link: '/release/v1.0.0' }
        ]
      }
    ],
    
    // 侧边栏
    sidebar: {
      '/guide/': [
        {
          text: '开始',
          collapsed: false,
          items: [
            { text: '什么是 Kunnix？', link: '/guide/what-is-kunnix' },
            { text: '快速开始', link: '/guide/quickstart' },
            { text: '安装指南', link: '/guide/installation' }
          ]
        },
        {
          text: '核心模块',
          collapsed: false,
          items: [
            { text: '记忆系统', link: '/guide/memory-system' },
            { text: '任务管理', link: '/guide/task-management' },
            { text: '技能进化', link: '/guide/skill-evolution' },
            { text: '会话集成', link: '/guide/session-integration' }
          ]
        },
        {
          text: '架构设计',
          collapsed: true,
          items: [
            { text: '系统架构', link: '/guide/architecture' },
            { text: 'L0-L5 分级记忆', link: '/guide/memory-layers' },
            { text: '混合检索', link: '/guide/hybrid-search' },
            { text: '性能优化', link: '/guide/performance' }
          ]
        },
        {
          text: '最佳实践',
          collapsed: true,
          items: [
            { text: '使用技巧', link: '/guide/tips' },
            { text: '故障排查', link: '/guide/troubleshooting' },
            { text: '常见问题', link: '/guide/faq' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API 参考',
          collapsed: false,
          items: [
            { text: '概览', link: '/api/overview' },
            { text: 'MemorySystem', link: '/api/memory-system' },
            { text: 'TaskOrchestrator', link: '/api/task-orchestrator' },
            { text: 'SkillEvolution', link: '/api/skill-evolution' },
            { text: 'AutomationManager', link: '/api/automation-manager' }
          ]
        }
      ],
      '/examples/': [
        {
          text: '使用示例',
          collapsed: false,
          items: [
            { text: '基础示例', link: '/examples/basic' },
            { text: '个人知识管理', link: '/examples/knowledge-management' },
            { text: '项目管理', link: '/examples/project-management' },
            { text: '技能自动化', link: '/examples/skill-automation' },
            { text: '企业级应用', link: '/examples/enterprise' }
          ]
        }
      ]
    },
    
    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/kunnix-ai/memory-task-system' },
      { icon: 'discord', link: 'https://discord.gg/kunnix' }
    ],
    
    // 页脚
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 Kunnix Team'
    },
    
    // 搜索配置
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换'
                }
              }
            }
          }
        }
      }
    },
    
    // 编辑链接
    editLink: {
      pattern: 'https://github.com/kunnix-ai/memory-task-system/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页面'
    },
    
    // 最后更新时间
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  },
  
  // Markdown 配置
  markdown: {
    lineNumbers: true,
    image: {
      lazyLoading: true
    }
  },
  
  // Vite 配置
  vite: {
    resolve: {
      alias: {
        '@': './.vitepress'
      }
    }
  }
})
