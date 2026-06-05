# Claude Code 使用指南

## 终端使用基础

### 启动方式

```bash
# 进入项目目录后直接启动
cd ~/your-project
claude

# 或一次性任务（执行后退出）
claude "你的指令"

# 查看帮助
claude --help
```

---

## 聊天记录管理

### 恢复历史对话

启动 Claude Code 时会显示最近会话列表：

```
Recent sessions:
↑↓ to navigate, Enter to select, /new to start fresh
─────────────────────────────────────────────────
1. 重构用户认证模块      (2 hours ago)
2. 修复登录 bug          (yesterday)
3. 写 API 文档           (3 days ago)
```

| 操作         | 方法                                       |
| ---------- | ---------------------------------------- |
| **继续某次对话** | 启动后用 ↑↓ 选择，回车确认                          |
| **新对话**    | 启动后按 `/new`，或 `exit` 后重新 `claude`        |
| **查看历史**   | `~/.claude/projects/<项目路径>/transcripts/` |
| **导出对话**   | `/export` 命令                             |

### 重要提示

| 特性 | 说明 |
|------|------|
| **目录隔离** | 不同项目目录有独立的历史记录 |
| **不跨项目共享** | 在 `~/projects/web/` 的会话不会出现在 `~/projects/api/` |
| **想复用内容** | 用 `/export` 导出到笔记，或复制关键代码到笔记 |

---

## 模式切换

| 模式 | 进入方式 | 说明 |
|------|----------|------|
| **交互模式** | 直接 `claude` | 默认，逐轮对话 |
| **Plan 模式** | `/plan` 或自动触发 | 规划阶段，不执行代码 |
| **Auto 模式** | `/auto` | 自动执行，无需确认 |
| **YOLO 模式** | `/yolo` | 跳过所有确认 |

---

## 文件操作

| 操作 | 命令 |
|------|------|
| **读取文件** | 直接在 prompt 中说"读取某文件" |
| **粘贴图片** | `Ctrl+V` 直接粘贴截图（终端中！） |
| **拖入文件** | 拖拽文件到终端窗口 |
| **路径输入** | 输入文件路径即可 |

---

## 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+L` | 清屏 |
| `Ctrl+J` / `Option+回车` | 换行（输入多行） |
| `Ctrl+R` | 搜索历史 prompt |
| `Ctrl+U` | 删除整行 |
| `Ctrl+V` | 粘贴 |
| `Esc` + `Esc` | 回退（/rewind） |

### Claude Code 专属快捷键

| 快捷键 | 功能 |
|--------|------|
| `Shift+Tab` | 自动接受编辑建议 |
| `#` | 创建记忆 (create a memory) |
| `!` | 进入 bash 模式 |
| `@` | 添加文件/文件夹到上下文 |
| `Esc` | 取消操作 |
| `Double-Esc` | 回到历史记录，`--resume` 恢复对话 |
| `Ctrl+R` | 获取详细输出 (verbose output) |
| `/vibe` | 快捷指令 |

**截图参考**：

![Keybindings 演示](https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/ccv2%2F2026-04-26%2FMiniMax-M2.7%2F2033839697825898985%2Ff6403874a8ee59ace3441723226293543dbb71a3838cca5d0ad66ac73ac055aa..png)

---

## 会话控制命令

| 命令 | 功能 |
|------|------|
| `/exit` | 退出当前会话 |
| `/compact` | 压缩历史，释放上下文 |
| `/clear` | 清空对话历史 |
| `/session` | 查看当前会话信息 |

---

## 与 Trae IDE 对比

| 功能 | 终端 Claude Code | Trae |
|------|------------------|------|
| 聊天历史 | 需手动查看 transcripts 目录 | UI 直接查看 |
| 模式切换 | 命令或快捷键 | 按钮切换 |
| 文件上传 | 拖拽或 Ctrl+V | UI 按钮 |
| 代码高亮 | 无 | 有 |
| 预览图片 | 无 | 有 |

---

## 权限模式配置

编辑 `~/.claude/settings.json`：

```json
"permissions": {
  "defaultMode": "plan"  // plan / auto / yolo
}
```

| 模式 | 确认频率 | 安全性 |
|------|----------|--------|
| `plan` | 每个操作都确认 | 最安全 |
| `auto` | 仅危险操作确认 | 中等 |
| `yolo` | 完全不确认 | 风险自负 |

---

## 常见问题

**Q: 为什么 `/mcp` 看不到 MiniMax？**
A: MCP 配置修改后需要完全重启 Claude Code（新开窗口）

**Q: Skills 需要手动开启吗？**
A: 不需要。在 `settings.json` 启用后，每次新 session 自动加载。

**Q: 终端和 Trae 哪个好用？**
A: 重要项目用 Trae（方便查看历史），快速任务用终端。
