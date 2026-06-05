# Claude Code 配置笔记

> 本项目记录我对 Claude Code 的所有配置操作，供日常查阅和持续完善。

**最后更新：2026-04-01**

---

## Obsidian Vault 说明

本目录是一个 **Obsidian Vault**，使用 Obsidian 的所有特性来组织笔记：

| 特性 | 语法 | 示例 |
|------|------|------|
| **Wiki-link** | `[[文件夹/笔记]]` | `[[USAGE/README]]` → 链接到 USAGE/README.md |
| **嵌入内容** | `![[文件夹/笔记]]` | `![[SKILLS/README]]` → 嵌入另一个笔记的内容 |
| **标签** | `#标签名` | `#技巧` → 在正文中添加标签 |
| **标题锚点** | `[[#标题]]` | `[[#brainstorming]]` → 跳转到同一笔记的标题 |

---

## 目录结构

```
Claude-Config-Notes/
├── CLAUDE.md              # 项目索引和导航
├── USAGE/                 # 使用指南
│   └── README.md          # 终端操作、快捷键、模式切换
├── HIDDEN_COMMANDS/       # 隐藏命令技巧
│   └── README.md          # /btw、/rewind、/simplify 等
├── SKILLS/                # Skills 完整指南
│   └── README.md          # 所有已安装 Skills
├── MCP/                   # MCP 配置详解
│   └── README.md
├── PLUGINS/               # Plugins 和 Hooks
│   └── README.md
└── SETTINGS/              # 配置文件备份
```

---

## Skills 快速索引

### 官方文档 Skills

| 命令 | 功能 | 触发场景 |
|------|------|----------|
| `/pdf` | 读取 PDF | "读取 PDF"、"分析 PDF" |
| `/docx` | 生成 Word | "生成 Word"、"导出 docx" |
| `/xlsx` | 处理 Excel | "生成 Excel"、"分析表格" |
| `/pptx` | 生成 PPT | "生成 PPT"、"制作演示文稿" |

### 其他 Skills

| 命令 | 功能 | 触发场景 |
|------|------|----------|
| `/brainstorming` | 方案头脑风暴 | "头脑风暴"、"分析可行方案" |
| `/write-a-prd` | PRD 撰写 | "写 PRD"、"梳理需求" |
| `/planning-with-files` | 持久化规划 | "帮我规划项目" |
| `/find-skills` | 发现新 Skills | "帮我找 xxx 相关的 skill" |
| `/agent-browser` | 浏览器自动化 | "操作这个网页" |
| `/systematic-debugging` | 系统调试 | "帮我调试这个 bug" |
| `/claudeception` | 持续学习 | "save this as a skill" |
| `/youtube-fetcher` | YouTube 转笔记 | 发 YouTube 链接 |
| `/defuddle` | 网页内容提取 | "把网页转 Markdown" |

---

## Plugins

| 插件 | 功能 |
|------|------|
| explanatory-output-style | 解释性输出样式 |
| learning-output-style | 学习输出样式 |
| hookify | 创建行为钩子防止错误 |

---

## 配置文件位置

| 文件 | 用途 |
|------|------|
| `~/.claude/settings.json` | Plugins、Hooks、Permissions |
| `~/.claude.json` | MCP 服务器配置 |
| `~/.claude/skills/` | Skills 安装目录 |

---

## 更新日志

| 日期 | 操作 |
|------|------|
| 2026-03-25 | 初始配置 |
| 2026-03-26 | 添加 Skills、文档 Skills、Ghostty |
| 2026-03-26 | 重组目录结构 |
| 2026-03-27 | 新增 11 个 Skills，清理无关文件，完善 Obsidian 集成 |
| 2026-03-27 | 删除 ppt-generator、remotion（使用率低） |
| 2026-03-29 | 安装 Pixel Agents（Trae/VS Code 扩展） |
| 2026-04-01 | 同步到 GitHub，完善 README |

---

*本目录已初始化 Git 仓库管理配置变更*
