---
tags:
  - 抖音
  - Claude-Code
  - 使用技巧
  - Vishwas
created: 2026-03-27
source: https://v.douyin.com/tWr5jZ-yKTU/
author: AI产品兴起
platform: 抖音
original_source: X @vishwas
---

# 50 条 Claude Code 使用技巧

> 分享来自 X 上博主 Vishwas 总结的50条 Claude Code 日常使用技巧与最佳实践

## 视频信息

| 项目 | 内容 |
|------|------|
| **作者** | AI产品兴起 |
| **抖音号** | 前美洽CTO｜现AI创业者 |
| **Discord 社群** | Cocrea World 万人社群主理人 |
| **视频ID** | 7619553993160674277 |
| **点赞** | 479 |
| **收藏** | 581 |
| **分享** | 70 |

**话题标签**：#vibecoding #AI技巧 #claude #claudecode #人工智能

---

## 一、基础心法

| # | 技巧 |
|---|------|
| 1 | **任务描述永远放在最前面**，重要指令置顶。这是大多数人忽略的细节。 |
| 2 | **给 Claude 一个自我验证的方式**，比如测试用例、截图或预期输出。这是提升效果最立竿见影的一招。 |
| 3 | **推荐的提示词结构**：角色 + 任务 + 上下文。简洁有力，屡试不爽。 |
| 4 | 工作流程遵循 **"先探索，再规划，后执行"**。可以先用其他大模型做调研，进入 Plan Mode 规划，最后切回正常模式写代码。 |
| 5 | **假设 Claude 对你的项目一无所知**，把它需要的信息全部告诉它。用 @ 符号链接文件、数据和图片，提供丰富的上下文。 |
| 6 | 运行 `/init` 可以为当前项目生成一个 CLAUDE.md 模板文件。 |

---

## 二、项目与技能管理

| # | 技巧 |
|---|------|
| 7 | **用项目级指令定义长期行为**，避免重复提示。 |
| 8 | **编辑 Memory 标签**精确控制 Claude 应该记住或忽略什么。 |
| 9 | **把重复性工作流转化为 Skills**。一个取巧的方法：贴一个优秀输出，让 Claude 把它变成可复用的 Skill。甚至可以上传截图让 Claude 复刻。 |
| 10 | **定期清理 memory、文件和指令**，防止项目漂移。 |
| 11 | **不相关的工作流要分开项目**，避免上下文污染。 |
| 12 | 推荐两个 Skills 资源库：[skillsmp.com](https://skillsmp.com) 收录了 8 万多个 Skills，[mcpservers.org/claude-skills](https://mcpservers.org/claude-skills) 提供即插即用的 Skills。 |

---

## 三、冷门但实用的技巧

| # | 技巧 |
|---|------|
| 13 | **用其他大模型规划项目、生成高级提示词**，再交给 Claude Code 执行。这个策略还能节省 Plan Mode 的 token 消耗。 |
| 14 | 在 `.claude/agents/` 目录下**定义专门的子代理**，让 Claude 把特定任务委派出去。 |
| 15 | **让 Claude 根据你预设的成功标准给自己的答案打分**。 |
| 16 | 运行 `/plugin` **浏览插件市场**，无需配置即可扩展能力。 |
| 17 | **大型项目可以让 Claude 先采访你**。用一个简短提示开始，让 Claude 通过 AskUserQuestion 工具向你提问。 |
| 18 | 发现 Claude 跑偏时立刻纠正，按 **ESC** 中断操作。`/clear` 开启干净会话，双击 ESC 或 `/rewind` 打开检查点菜单。 |
| 19 | 可以**运行多个并行会话**：Claude Desktop 管理多个本地会话，每个会话有独立的工作树；Claude Web 在 Anthropic 的云端隔离虚拟机中运行。 |

---

## 四、调试与错误处理

| # | 技巧 |
|---|------|
| 20 | **只重跑出错的步骤**，不要重新生成所有内容。 |
| 21 | **让 Claude 故意复现错误**来理解问题本质。 |
| 22 | **回滚到上一个正常的提示词**，逐步重新应用修改。 |
| 23 | CLAUDE.md 太长会适得其反，重要规则被淹没。**解决方案：无情地精简**，如果 Claude 本来就能做对的事，删掉那条指令。 |
| 24 | 常见错误：一个任务没完成就问不相关的问题，再回到第一个任务，上下文被无关信息污染。**解决方案：不相关任务之间用 /clear**。 |
| 25 | **连续纠正两次还是错的话**，`/clear` 后写一个更好的初始提示词，把学到的教训融入进去。 |
| 26 | 上下文窗口填满后，Claude 可能开始遗忘早期指令。参考官方文档减少 token 消耗：[code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs#reduce-token-usage) |

---

## 五、进阶资源

| # | 技巧 |
|---|------|
| 27 | **把 Notion 数据库连接到 Claude**，存储常用提示词。 |
| 28 | 使用 `claude --dangerously-skip-permissions` **跳过所有权限检查**，适合修复 lint 错误或生成样板代码这类安全的自动化工作流。 |
| 29 | **Hooks 适合那些必须每次都执行、零例外的操作**。 |
| 30 | 推荐资源：<br>- [Anthropic 官方学习资源](https://anthropic.com/learn)<br>- [Claude Code 最佳实践文档](https://code.claude.com/docs/en/best-practices)<br>- [GitHub superpowers 仓库](https://github.com/obra/superpowers) |
| 31 | **最后一条忠告：慢即是快**。尤其是构建严肃的工作流时，规划、规划、再规划，然后才是执行。 |

---

## 相关资源

- [[SKILLS/README]] - 我们已安装的 Skills
- [[USAGE/README]] - Claude Code 使用指南
- [[HIDDEN_COMMANDS/README]] - 隐藏命令技巧

## 备注

> 完整50条技巧来自 X @vishwas（Vishwas Mittal），抖音由 @AI产品兴起 分享整理。
