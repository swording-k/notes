# Skills 配置指南

## Skills 存放位置

```
~/.claude/skills/          # Claude Code 官方路径（symlink）
~/.agents/skills/          # skills 命令安装位置
```

---

## 已安装 Skills 总览 (2026-04-13 更新)

| Skill                        | 分类       | 功能                   |
| ---------------------------- | -------- | -------------------- |
| [[#brainstorming]]           | PM 场景    | 方案头脑风暴               |
| [[#writing-plans]]           | PM 场景    | 实施计划拆分               |
| [[#write-a-prd]]             | PM 场景    | PRD 撰写               |
| [[#find-skills]]             | 元工具      | 发现更多 Skills          |
| [[#agent-skill-creator]]     | 元工具      | 创建自定义 Skills         |
| [[#planning-with-files]]     | 项目管理     | Manus 风格持久化规划        |
| [[#systematic-debugging]]    | 开发       | 系统化调试                |
| [[#test-driven-development]] | 开发       | 测试驱动开发               |
| [[#obsidian-markdown]]       | Obsidian | Obsidian Markdown 规范 |
| [[#obsidian-cli]]            | Obsidian | Obsidian CLI 操作      |
| [[#obsidian-knowledge-manager]] | Obsidian | 自适应知识库管理          |
| [[#defuddle]]                | Obsidian | 网页内容提取               |
| [[#ui-ux-pro-max]]           | UI/UX    | 专业 UI 设计指导           |
| [[#youtube-fetcher]]         | 视频       | YouTube 视频转 Markdown |
| [[#agent-browser]]           | 浏览器      | 浏览器自动化               |
| [[#web-access]]              | 联网       | 联网搜索 + 浏览器操控（⚠️ 之前误配为MCP，已清理）         |
| [[#pua-skill]]                     | 开发       | 专治 AI 摆烂（⚠️ 之前误配为MCP，已清理）             |
| [[#pdf]]                     | 文档       | PDF 处理               |
| [[#docx]]                    | 文档       | Word 文档              |
| [[#xlsx]]                    | 文档       | Excel 处理             |
| [[#pptx]]                    | 文档       | PPT 处理               |
| [[#claudeception]]           | 元工具      | 从会话中提取可复用知识          |

**2026-04-22 更新说明**：
- `frontend-design` - 之前错误配置为 MCP server（npm包不存在），现在作为 skill 正常可用
- `pua` → 重命名为 `pua-skill` - 之前错误配置为 MCP server，现在作为 skill 正常可用
- `claude-mem` - 之前错误配置为 MCP server（npm包不存在），已移除 MCP 配置

**2026-04-23 更新说明**：
- `obsidian-knowledge-manager` - 新增自创技能，自适应知识库管理，自动推断目录结构

---

## 已安装 Skills

### 产品经理场景（2026-03-26 新增）

#### brainstorming

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/obra/superpowers |
| **功能** | 将模糊想法通过结构化对话转化为清晰设计方案 |
| **触发** | "头脑风暴"、"分析可行方案"、"帮我想想" |
| **使用** | `/brainstorming` 或直接描述需求 |

**工作模式**：
- "一次只问一个问题" 的对话方式
- 主动提出 2-3 个可行方案并给出推荐理由
- 产出包含架构、数据流、测试策略的完整设计文档

**使用示例**：
```
"我想做一个 AI 写作助手，帮我头脑风暴一下产品形态"
"我们的用户激活率很低，帮我想想新手引导流程该怎么设计"
"帮我分析这个功能的三种实现方案并给出建议"
```

---

#### write-a-prd

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/mattpocock/skills |
| **功能** | 访谈式 PRD 文档生成 |
| **触发** | "写 PRD"、"梳理需求"、"帮我写产品文档" |
| **使用** | `/write-a-prd` 或直接描述需求 |

**工作模式**：
- 深度对话式访谈，逐步厘清需求全貌
- 像产品评审一样对每个设计分支追问到底
- 生成可直接作为 GitHub Issue 提交的 PRD

**PRD 结构**：
1. 用户视角描述面临的问题
2. 用户视角描述解决方案
3. 详细用户故事类型
4. 模块划分、接口设计、架构
5. 测试范围和测试策略

---

#### writing-plans

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/obra/superpowers |
| **功能** | 将方案拆解为极细颗粒度的执行计划 |
| **触发** | "拆解计划"、"制定执行步骤"、"分解任务" |
| **使用** | `/writing-plans` 或直接描述需求 |

**计划内容**：
- 功能目标（一句话）
- 架构说明（2-3 句）
- 技术栈、文件结构 Map
- 每个任务块的分步骤检查清单（含代码、命令、预期输出）

---

### 官方文档 Skills (2026-03-26 新增)

#### pdf

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/anthropics/skills |
| **功能** | 读取 PDF 文件内容 |
| **触发** | "读取 PDF"、"分析 PDF"、"打开这个 PDF" |
| **使用** | 直接描述需求，自动触发 |

---

#### docx

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/anthropics/skills |
| **功能** | 生成 Word 文档 |
| **触发** | "生成 Word"、"导出为 docx"、"创建文档" |
| **使用** | 直接描述需求，自动触发 |

---

#### xlsx

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/anthropics/skills |
| **功能** | 生成和分析 Excel 表格 |
| **触发** | "生成 Excel"、"分析表格"、"创建 xlsx" |
| **使用** | 直接描述需求，自动触发 |

---

#### pptx

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/anthropics/skills |
| **功能** | 生成 PPT 演示文稿 |
| **触发** | "生成 PPT"、"制作演示文稿"、"创建 pptx" |
| **使用** | 直接描述需求，自动触发 |

---

#### claudeception

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/blader/Claudeception |
| **功能** | 从工作会话中提取可复用知识，自动创建新的 Skills |
| **触发** | "save this as a skill"、"extract a skill"、"what did we learn?" |

---

### 元工具 Skills (2026-03-27 新增)

#### find-skills

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/haha0815/claude-meta-skills |
| **功能** | 帮你发现和搜索更多有用的 Skills |
| **触发** | "帮我找 xxx 相关的 skills"、"推荐一些 xxx 工具" |
| **使用** | 直接描述需求，自动触发 |

**★ Insight ─────────────────────────────────────**
- find-skills 是"Skills 的 Skills"，让你持续扩展能力边界
- 搜索时用中文描述需求也能找到相关 skills
`─────────────────────────────────────────────────`

---

#### agent-skill-creator

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/FrancyJGLisboa/agent-skill-creator |
| **功能** | 将工作流程转化为可复用的自定义 Skill |
| **触发** | "帮我创建一个 skill"、"把这个流程封装成 skill" |
| **使用** | `/agent-skill-creator` 或直接描述需求 |

---

### 项目管理 Skills (2026-03-27 新增)

#### planning-with-files

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/OthmanAdi/planning-with-files |
| **功能** | Manus 风格的持久化 Markdown 规划，避免长任务丢失上下文 |
| **⭐** | 17,390 - 非常热门 |
| **触发** | "帮我规划这个项目"、"复杂任务需要持久化跟踪" |
| **使用** | 直接描述需求，自动触发 |

**核心特点**：
- 任务状态持久化到文件
- 复杂任务分步骤执行
- 意外中断后可从断点恢复
- 来自 Manus（$2B 收购的 AI 代理项目）

---

### 开发技能补充 (2026-03-27 新增)

#### systematic-debugging

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/obra/superpowers |
| **功能** | 结构化调试方法论，快速定位问题根因 |
| **触发** | "帮我调试这个 bug"、"这个问题怎么排查" |
| **使用** | 直接描述问题，自动触发 |

---

#### test-driven-development

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/obra/superpowers |
| **功能** | TDD 工作流，先写测试再写实现 |
| **触发** | "用 TDD 方式"、"先写测试" |
| **使用** | 直接描述需求，自动触发 |

---

### Obsidian 增强 (2026-03-27 新增)

> 来自 Obsidian 插件开发者 kepano，完美配合你的知识库

#### obsidian-knowledge-manager

| 项目 | 说明 |
|------|------|
| **仓库** | 本地创建（`~/.claude/skills/obsidian-knowledge-manager/`） |
| **功能** | 自适应 Obsidian 知识库管理，自动推断目录结构 |
| **触发** | "创建笔记"、"初始化知识库"、"整理知识"、"设置目录结构" |
| **使用** | 直接描述需求，自动触发 |

**核心特点**：
- **自适应设计**：不绑定固定模板，根据用户描述自动推断目录结构
- **智能推断**：分析关键词（Python → 语法/练习/错题），不预设模板
- **严格格式**：wikilink 只链接已存在文件，遵循 Obsidian 规范
- **自动创建**：CLAUDE.md、README.md 自动生成

**示例**：
```
用户：帮我建一个学习大模型的知识库
→ 推断目录：理论/ 实践/ 应用/ 案例/
→ 用户确认后创建完整结构

用户：创建一篇关于RAG的笔记
→ 分析主题 → 选择目录 → 检查相关笔记 → 创建并链接
```

---

#### obsidian-markdown

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/kepano/obsidian-skills |
| **功能** | 教你正确使用 Obsidian Markdown 语法 |
| **触发** | "帮我写 Obsidian 笔记"、"如何使用 wiki-link" |
| **使用** | 直接描述需求，自动触发 |

---

#### obsidian-cli

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/kepano/obsidian-skills |
| **功能** | 通过 CLI 操作 Obsidian vault |
| **触发** | "用命令行操作 Obsidian"、"批量处理笔记" |
| **使用** | 直接描述需求，自动触发 |

---

#### defuddle

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/kepano/obsidian-skills |
| **功能** | 从网页提取干净的内容，转为 Markdown |
| **触发** | "把网页转成 Markdown"、"提取这个页面的内容" |
| **使用** | 直接描述需求，自动触发 |

**★ Insight ─────────────────────────────────────**
- defuddle 配合 agent-browser 可以实现：打开网页 → 提取内容 → 存入 Obsidian
- 这是抖音/网页视频内容进入知识库的关键工具
`─────────────────────────────────────────────────`

---

### UI/UX 设计 (2026-03-27 新增)

#### ui-ux-pro-max

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| **功能** | 提供专业 UI/UX 设计指导，161 种产品类型、84 种风格 |
| **⭐** | 51,953 - 目前最热门的 Skills 之一 |
| **触发** | "帮我设计界面"、"这个 UI 怎么样"、"用什么设计模式" |
| **使用** | 直接描述需求，自动触发 |

**支持平台**：React、Vue、HTML5、Tailwind、Mobile UI 等

---

### 视频内容 (2026-03-27 新增)

#### youtube-fetcher

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/JimmySadek/youtube-fetcher-to-markdown |
| **功能** | 将 YouTube 视频转成带字幕和章节的 Markdown 笔记 |
| **触发** | "把这个 YouTube 视频转成笔记"、"总结这个视频" |
| **使用** | 直接发链接，自动触发 |

**前置要求**：需要安装 yt-dlp

---

#### agent-browser

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/CalebDane7/agent-browser |
| **功能** | 浏览器自动化控制，支持登录态、文件上传等 |
| **触发** | "帮我操作这个网页"、"自动化浏览器任务" |
| **⚠️** | 需要安装 agent-browser CLI |
| **使用** | 直接描述需求，自动触发 |

**★ Insight ─────────────────────────────────────**
- agent-browser + defuddle = 抖音/网页视频内容抓取方案
- 需要先安装：`npm install -g agent-browser`
- 支持保持登录态，访问需要认证的内容
`─────────────────────────────────────────────────`

---

### 联网与浏览器 (2026-04-13 新增)

#### web-access

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/eze-is/web-access |
| **⭐** | 2,000+ |
| **功能** | 联网搜索 + 浏览器操控，可访问登录态内容（小红书、B站等） |
| **触发** | "帮我搜一下小红书"、"访问这个需要登录的网页" |
| **使用** | 直接描述需求，自动触发 |

**核心特点**：
- 通过 Chrome DevTools Protocol 连接本地 Chrome，带着登录状态
- 自动沉淀每个网站的操作经验，越用越快
- 可配合 Jina 将网页转 Markdown，节省 token

**前置要求**：
- Chrome 更新到最新版
- 开启远程调试：地址栏输入 `chrome://inspect/#remote-debugging` 勾选

---

#### pua

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/tanweai/pua |
| **功能** | 专治 AI 摆烂，强制 AI 换思路解决问题 |
| **触发** | "这个 bug 改不明白"、"/pua" |
| **使用** | `/pua` 或在 AI 摆烂时手动触发 |

**核心特点**：
- 四级压力升级，强制打断 AI 原地打转
- 执行 7 项检查清单，逼 AI 换思路
- v3 版本内置阿里、字节、华为、腾讯等十几家公司方法论

**★ Insight ─────────────────────────────────────**
- PUA 不是真的在骂 AI，而是给它施压让它跳出思维定式
- 建议在实在解决不了时再用，不建议默认开启
`─────────────────────────────────────────────────`

---

#### frontend-design

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/anthropics/skills/tree/main/skills/frontend-design |
| **⭐** | 官方排名第一 |
| **功能** | 改善 AI 做前端的"AI 味"，优化排版、字体、配色 |
| **触发** | "帮我做前端页面"、"生成一个网页 UI" |
| **使用** | 直接描述需求，自动触发 |

**核心特点**：
- 要求 AI 先确定美学方向（极简、复古未来等）
- 禁止烂大街的 Inter/Roboto/Arial 字体
- 禁止紫色渐变配白底的经典 AI 审美

**★ Insight ─────────────────────────────────────**
- 能力越差的模型，效果提升越明显
- 配合 pptx skill 使用，PPT 颜值也能大幅提升
`─────────────────────────────────────────────────`

---

#### claude-mem

| 项目 | 说明 |
|------|------|
| **仓库** | https://github.com/thedotmack/claude-mem |
| **功能** | 记忆持久化，新会话自动注入历史上下文 |
| **触发** | 自动触发，无需手动调用 |
| **使用** | 开新会话时自动加载相关记忆 |

**核心特点**：
- 三层检索机制（索引 → 时间线 → 细节），节省 token
- 自带 Web 界面：`localhost:37777` 查看记忆内容
- 支持隐私标签 `<private>内容</private>` 跳过记忆

**★ Insight ─────────────────────────────────────**
- 类似 OpenClaw 的 Memory 功能，但给 Claude Code 用的
- 越用越懂你，但隐私内容记得加标签
`─────────────────────────────────────────────────`

---

## Skills 触发机制

Claude Code 根据 `SKILL.md` 中的 `description` 字段自动判断何时触发：

```yaml
---
name: skill-name
description: |
  触发条件描述。当用户提到相关内容时自动激活。
---
```

## 安装新 Skills

```bash
# 使用 npx skills add 命令
npx skills add <作者>/<仓库> --skill <skill名称> --yes --global

# 示例
npx skills add obra/superpowers --skill brainstorming --yes --global
```

## 常见问题

**Q: Skills 和 Plugins 有什么区别？**
A:
- **Plugins**：内置功能模块（如 hookify, ralph-loop）
- **Skills**：用户可添加的扩展，存放在 `~/.claude/skills/`

**Q: 已删除的 Skills？**
A:
- `ppt-generator`：基于 Gemini API，有配额限制
- `remotion`：动画逻辑图，当前使用频率低
