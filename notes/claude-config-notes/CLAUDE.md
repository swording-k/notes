# Claude Code 配置笔记

> 本项目记录我对 Claude Code 的所有配置操作，供日常查阅和持续完善。

**最后更新：2026-03-27**

---

## Obsidian Vault 说明

本目录是一个 **Obsidian Vault**，可以使用 Obsidian 的所有特性来组织笔记：

| 特性 | 语法 | 示例 |
|------|------|------|
| **Wiki-link** | `[[文件夹/笔记]]` | `[[USAGE/README]]` → 链接到 USAGE/README.md |
| **嵌入内容** | `![[文件夹/笔记]]` | `![[SKILLS/README]]` → 嵌入另一个笔记的内容 |
| **标签** | `#标签名` | `#技巧` → 在正文中添加标签 |
| **标题锚点** | `[[#标题]]` | `[[#brainstorming]]` → 跳转到同一笔记的标题 |

**快速导航**：
- [[USAGE/README]] - 使用指南、快捷键、模式切换
- [[HIDDEN_COMMANDS/README]] - 隐藏命令技巧
- [[SKILLS/README]] - Skills 完整指南
- [[MCP/README]] - MCP 配置详解
- [[PLUGINS/README]] - Plugins 和 Hooks

---

## 目录结构

```
Claude-Config-Notes/
├── CLAUDE.md              # 本文件 - 项目索引
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
| `/writing-plans` | 实施计划 | "拆解计划"、"执行步骤" |
| `/claudeception` | 持续学习 | "save this as a skill" |
| `/planning-with-files` | 持久化规划 | "帮我规划项目" |
| `/find-skills` | 发现新 Skills | "帮我找 xxx 相关的 skill" |
| `/agent-skill-creator` | 创建自定义 Skill | "创建 skill"、"自动化流程" |
| `/systematic-debugging` | 系统调试 | "帮我调试这个 bug" |
| `/ui-ux-pro-max` | UI/UX 设计 | "帮我设计界面" |
| `/agent-browser` | 浏览器自动化 | "操作这个网页" |
| `/youtube-fetcher` | YouTube 转笔记 | 发 YouTube 链接 |
| `/defuddle` | 网页内容提取 | "把网页转 Markdown" |
| `/obsidian-markdown` | Obsidian 语法 | "帮我写 Obsidian 笔记" |
| `/obsidian-cli` | Obsidian CLI | "用命令行操作 vault" |

---

## 常用命令

| 命令 | 功能 |
|------|------|
| `/btw` | 插入问题不污染上下文 |
| `/rewind` | 代码/对话分别回退 |
| `/simplify` | 三合一代码审查 |
| `/branch` | 对话分叉 |
| `/loop` | 定时循环任务 |
| `/export` | 导出对话 |
| `/insights` | 使用习惯分析 |

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
| 2026-04-22 | 清理错误配置的 MCP servers（frontend-design, web-access, pua, claude-mem, crosspaste），这些实际上是 Skills 不是 MCP Servers |
| 2026-04-26 | 扩大权限 Allow 列表：新增 Read/Write/Edit/Glob 作用于当前目录的规则、Bash(ls:*)、Bash(cd:*)、Bash(grep:*)、WebFetch；设置响应语言为简体中文、启用 IDE 自动连接；新增 Keybindings 快捷键列表到 [[USAGE/README]] |

---

*本目录已初始化 Git 仓库管理配置变更*
