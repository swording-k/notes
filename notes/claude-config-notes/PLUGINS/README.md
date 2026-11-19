# Plugins 配置指南

## Plugins 配置文件

`~/.claude/settings.json` - 全局设置（Plugins、Hooks、Permissions）

## 已启用的 Plugins (2026-06-20 更新)

```json
"enabledPlugins": {
  "hookify@claude-plugins-official": true,
  "ralph-loop@claude-plugins-official": true,
  "explanatory-output-style@claude-plugins-official": true,
  "learning-output-style@claude-plugins-official": true,
  "code-review@claude-plugins-official": true,
  "security-guidance@claude-plugins-official": true,
  "swift-lsp@claude-plugins-official": true
}
```

| Plugin | 作用 |
|--------|------|
| **hookify** | 自定义 hooks 管理框架 |
| **ralph-loop** | 防止 AI 无敌循环（检测到循环自动停止） |
| **explanatory-output-style** | 输出代码时解释设计模式和实现思路 |
| **learning-output-style** | 交互式学习，代码决策点会请求有意义的贡献 |
| **code-review** | PR 自动代码审查，多代理评分 |
| **security-guidance** | 编辑文件时警告安全问题（命令注入、XSS 等） |
| **swift-lsp** | Swift 语言支持（LSP 集成） |

---

## Obsidian Skills（2026-11-20 新增）

官方 Agent Skills 插件，作者是 Obsidian CEO Steph Ango（kepano），MIT 协议。

| 项目 | 说明 |
|------|------|
| 仓库 | https://github.com/obsidianmd/obsidian-skills |
| Marketplace | `obsidian-skills` |
| Plugin | `obsidian@obsidian-skills` v1.2.0 |
| 安装范围 | user（`~/.claude/settings.json`） |
| 状态 | ✅ enabled |

### 安装命令

```bash
claude plugin marketplace add obsidianmd/obsidian-skills
claude plugin install obsidian@obsidian-skills
```

安装后需要**重启 Claude Code**（或开新会话）才会加载这些 skill。

### 包含的 7 个 Skill

| Skill | 作用 |
|-------|------|
| `obsidian-markdown` | Obsidian 风格 Markdown：wikilink、embed、callout、properties、frontmatter |
| `obsidian-bases` | `.base` 数据库视图 |
| `json-canvas` | `.canvas` 白板 JSON |
| `obsidian-cli` | 通过 Obsidian CLI 读写笔记、搜索、任务、属性；插件/主题开发调试 |
| `obsidian-headless` | 不开桌面端做 Sync / Publish |
| `defuddle` | 网页转干净 Markdown，节省 token |
| `knap` | 用 JSON/CSV 批量渲染模板 |

### 使用场景

- 在本仓库写笔记时自动遵守 Obsidian 语法（双链、callout、frontmatter）
- 需要批量整理、搜索、建 Canvas / Base 时调用对应 skill
- `obsidian-cli` 需要 Obsidian 桌面端打开并启用 CLI

### 注意事项

- 本机 `~/.agents/skills/` 下已有 `obsidian-markdown`、`obsidian-cli`，那是给 Codex 等其他工具用的；Claude Code 走 plugin，不要重复安装。
- 更新：`claude plugin update obsidian@obsidian-skills`
- 查看组件：`claude plugin details obsidian@obsidian-skills`

---

## Permissions 配置

```json
"permissions": {
  "allow": [
    "Bash(git:*)", "Bash(npm:*)", "Bash(node:*)",
    "Bash(pnpm:*)", "Bash(yarn:*)", "Bash(brew:*)",
    "Bash(xcodebuild:*)", "Bash(flutter:*)", "Bash(swift:*)",
    "Bash(cargo:*)", "Bash(python3:*)", "Bash(curl:*)",
    "Read", "Glob", "Grep", "Edit", "Write"
  ],
  "defaultMode": "plan"
}
```

**说明**：`defaultMode: "plan"` 表示危险操作会进入 plan 模式确认，不会自动执行。

## Hooks 配置

```json
"hooks": {
  "Stop": [{
    "matcher": "",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/plugins/ralph-loop/hooks/stop-hook.sh",
      "timeout": 10
    }]
  }]
}
```

**作用**：与 ralph-loop 插件配合，防止 AI 进入无限循环后无法停止。

## 修改配置

| 目标 | 操作 |
|------|------|
| 添加/修改 Plugins | 编辑 `~/.claude/settings.json` 的 `enabledPlugins` |
| 添加权限 | 编辑 `~/.claude/settings.json` 的 `permissions.allow` |
| 修改 Hooks | 编辑 `~/.claude/settings.json` 的 `hooks` |

---

## VS Code / Trae 扩展

### Pixel Agents

| 项目 | 说明 |
|------|------|
| **名称** | Pixel Agents |
| **开发者** | Pablo De Lucia |
| **类型** | VS Code / Trae 扩展 |
| **仓库** | VS Code Marketplace / Trae 扩展市场 |
| **安装** | `Cmd/Ctrl + Shift + X` → 搜索 "Pixel Agents" |

**功能**：为 Claude Code 提供像素艺术虚拟办公室可视化界面，AI 工作时显示像素小人动画。

**打开方式**：
```
Cmd + Shift + P (Mac) / Ctrl + Shift + P (Windows)
→ 输入 "Pixel Agents: Show Panel"
→ 回车
```

**小人状态**：
- 💻 编写代码 → 打字动画
- 📁 搜索文件 → 阅读动画
- ⏳ 等待干预 → 静止等待

**兼容性**：
| 终端 | 支持 |
|------|------|
| Trae 内置终端 | ✅ 支持 |
| Mac 原生终端 | ❌ 不支持 |
| Obsidian Claudian | ❌ 不支持 |
| VS Code 内置终端 | ✅ 支持 |

**★ Insight ─────────────────────────────────────**
- Pixel Agents 是 VS Code/Trae 专属扩展，不能在独立终端使用
- 小人只在 Claude Code 运行时显示，不运行时光标静止
- Trae 基于 VS Code，兼容 VS Code 扩展市场
`─────────────────────────────────────────────────`
