# Plugins 配置指南

## Plugins 配置文件

`~/.claude/settings.json` - 全局设置（Plugins、Hooks、Permissions）

## 已启用的 Plugins

```json
"enabledPlugins": {
  "hookify@claude-plugins-official": true,
  "ralph-loop@claude-plugins-official": true,
  "explanatory-output-style@claude-plugins-official": true,
  "learning-output-style@claude-plugins-official": true,
  "code-review@claude-plugins-official": true,
  "security-guidance@claude-plugins-official": true
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
