## MCP 配置指南

## MCP 配置文件

`~/.claude.json` - MCP 服务器配置

## 已配置的 MCP 服务器

### MiniMax MCP

```json
"MiniMax": {
  "type": "stdio",
  "command": "/Users/baojian/.local/bin/uvx",
  "args": ["minimax-coding-plan-mcp", "-y"],
  "env": {
    "MINIMAX_API_KEY": "sk-cp-fj-...(你的API Key)",
    "MINIMAX_API_HOST": "https://api.minimaxi.com"
  }
}
```

**功能**：
- `web_search` - 网络搜索
- `understand_image` - 图片理解（支持截图粘贴）

---

### GitHub MCP

```json
"github": {
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": {
    "Authorization": "Bearer github_pat_11BI3N46Q...(你的PAT)"
  }
}
```

**功能**：
- 创建 Pull Request
- 查看/管理 Issues
- 查看 GitHub Actions
- 评论 PR/Issue

## 验证 MCP 配置

```
/mcp
```

应该看到：
- `MiniMax` - ✅ connected
- `github` - ✅ connected

## 已移除的 MCP（2026-04-22 清理）

以下 MCP 之前配置但已移除：
- `crosspaste` - 服务器端口 13130 无响应，已移除
- `claude-mem` - npm 包 @thedotmack/claude-mem 不存在，已移除
- `frontend-design` - npm 包 @anthropic/frontend-design 不存在，作为 skill 使用
- `web-access` - npm 包 @ezeis/web-access 不存在，作为 skill 使用
- `pua` - npm 包 @tanweai/pua 不存在，作为 skill 使用

**注意**：frontend-design、web-access、pua 实际上是 **Skills**（技能模块），不是 **MCP Servers**。它们不需要连接，直接通过 `/skill-name` 或任务上下文自动触发。

---

## 常见问题

**Q: 为什么 `/mcp` 看不到 MiniMax？**
A: MCP 配置修改后需要完全重启 Claude Code（新开窗口）

**Q: Skills 和 MCP Servers 有什么区别？**
A:
- **MCP Servers**：通过 `.mcp.json` 配置的外部服务连接，需要正常运行
- **Skills**：存放在 `~/.claude/skills/` 的技能模块，直接通过上下文触发

---


