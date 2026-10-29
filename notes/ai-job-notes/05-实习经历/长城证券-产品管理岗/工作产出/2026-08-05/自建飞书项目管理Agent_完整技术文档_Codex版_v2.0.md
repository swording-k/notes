# 自建「飞书项目管理智能体」完整技术文档（Codex 开发版）

> **版本**：v2.0 ｜ **日期**：2026-08-13
> **本版定位**：本版是《自建「飞书项目管理智能体」原理与开发文档》(v1.0，2026-08-12) 的升级版。**核心升级 = 数据模型按《领域模型与业务逻辑 v1》从「需求任务同表」升级为「需求表 + 任务表、M:N 关联」**，工具 schema 同步更新（新增 create_requirement，群聊识别先判「需求 vs 任务」再分别落表）。飞书多维表格侧已按此目标模型落地（需求表、工时表已建），本文档直接对照真实表结构编写。
>
> **配套规格**：《飞书项目管理 Agent 产品需求文档（PRD v4.0 / 目标模型 §6.0）》——功能定义（F1–F13）、数据模型、验收标准（§8）一律以 PRD 为准；本文档只解决「自建怎么做 + 怎么写代码」。
>
> **本文档用途**：直接交给 Codex，让它把服务写出来并在本地跑通。跑通后 Bot 常驻即可，Codex 只负责「开发」，不负责「在线」。
>
> **诚实声明**：文中飞书 API 的精确参数 / scope 名称 / SDK 调用以「飞书开放平台文档 + lark-oapi 最新版」为准；无法在线核实的项已逐条标注「⚠️ 待核实」。Aily 侧能力边界已在附录 A 如实标注。

---

## 第 1 部分 · 运行原理：AI 项目管理智能体由哪几层构成

### 1.1 「大脑 / 身体 / 房子」三层模型

任何「IM 里的 AI 机器人」，本质都由三层叠起来。**搞懂这三层，就搞懂了 Aily 卖的是什么、自建要自己搭什么**：

| 层 | 叫什么 | 干什么 | Aily 里的样子 | 自建时的替代 |
|---|---|---|---|---|
| 引擎 | LLM 大脑 | 理解自然语言、判断意图、决定「现在该做哪个动作」 | Aily 内置大模型，按 token 计费 | 直连任意 LLM API：DeepSeek / Qwen / GLM / Claude / GPT |
| 框架 | Agent Runtime 身体 | 跑「循环」：消息喂给大脑 → 大脑说调工具 → 身体执行工具 → 结果喂回 → 生成回复；管工具注册、上下文、去重 | Aily 内置 agent runtime | 自写最简 agent loop（约 100–200 行），或用 Claude Code / Codex CLI / OpenClaw |
| 载体 | Host / 集成 房子 | 让机器人被「触发」并碰到外部世界：收到飞书群消息、到点定时、读写多维表格、发群消息、查成员 | Aily 托管：事件订阅、定时器、多维表格工具都配好了 | 自己的服务器 / 本地电脑常驻 + 飞书开放平台自建应用 + lark-oapi SDK |

**一句话结论**：Aily 卖的不是「AI」，是「打包好的房子 + 身体 + 大脑」三合一托管服务。自建 = 这三层分别自己解决：

- 你付给 Aily 的钱 = 平台托管费 + 它代收的 LLM 用量费；
- 自建后托管费消失，LLM 用量费变成直接付给模型厂商（且可换便宜得多的 DeepSeek / Qwen 中文模型）。

### 1.2 自建系统的目标架构

```
飞书客户端（成员 / 一骢哥在群里说话）
      │  @机器人 或 触发词（"要做…""确定了""把 X 派给张三"…）
      ▼
飞书开放平台（你的企业自建应用）
  · 机器人能力
  · 事件订阅 im.message.receive_v1（WebSocket 长连接，免公网）
  · 权限 scope：发消息 / 读群消息 / 多维表格 / 通讯录
      │ 事件推送
      ▼
┌──────────────────────────────────────────────────┐
│  你的 Bot 服务（常驻进程，推荐 Python）                │
│                                                    │
│  ① 事件接收层  收到群消息 → 判断是否@机器人 / 触发词 / 目标群   │
│  ② 意图识别层  调 LLM（function calling）→ 得出结构化动作    │
│                （建需求? 拆任务? 派给人? 记决策? 改状态? 查状态? 填工时?）│
│  ③ 工具执行层  把意图翻译成飞书 API 调用                     │
│                · 多维表格读写（需求/任务/项目/决策/成员/工时/周报） │
│                · 发群消息（机器人身份）                    │
│                · 姓名 → open_id / 成员记录 解析            │
│  ④ 定时调度层  工作日 16:35 每日速递 ｜ 周五 14:43 周报       │
│  ⑤ 存储        飞书多维表格 Base（对照 §4 数据模型）          │
└──────────────────────────────────────────────────┘
      │ LLM API（function calling / tool use）
      ▼
   大语言模型（DeepSeek / Qwen / GLM / Claude / GPT…任选）
```

### 1.3 核心机制：function calling 把「自然语言」变成「结构化动作」

这是整台机器最关键的机制，原理一句话：**LLM 不直接写数据库，它只负责「理解 + 决策」，写库动作由你的代码执行。**

一次群消息的处理流程：

1. 群消息到达 → 服务判断要不要处理（@ 到机器人 / 命中触发词 / 属于目标群）；
2. 组装 prompt：系统提示（你是谁、规则）+ 近期消息上下文 + **工具清单**（JSON schema）；
3. 调 LLM → 若判断需要动作，返回 `tool_calls`，例如：
   - 「加一个审批流功能」→ `create_requirement(name="协同平台审批流", ...)`
   - 「把【审批流】拆成 后端/前端 两个任务」→ `create_task(requirement="审批流", name="审批流后端接口", ...)` ×2
   - 「确定了，就按方案 B 做」→ `record_decision(title="…", content="按方案B推进")`
   - 「查一下 XX 的状态」→ `query_task(name="XX")`
4. 服务执行对应工具（读 / 写多维表格）；
5. 把工具结果喂回 LLM → 生成一句简短回复发到群里（PRD 验收标准 5：任何写入都在群里给一句简短说明）。

**为什么必须用 function calling**：建需求 / 拆任务 / 派任务 / 改状态是「要精确落库」的操作，参数（名称、被指派人、状态值）必须和表格字段严格对应；function calling 由模型保证输出结构、由代码保证执行正确。识别类需求（F1 / F2 / F7）本质也是 function calling，只是调的工具是「写需求表 / 写决策日志」。

**去重（验收标准 1：连续 5 条同一需求只建 1 条）**：服务维护「最近建过的需求/任务指纹」（key = 群 id + 归一化名称 / 描述前 30 字 + 30 分钟窗口），命中则跳过并提示「已记录过，如需修改请说『改…』」。MVP 用内存 dict 即可，重启丢失可接受。

**修改追加（验收标准 2）**：同一对象后续的「改 / 补」对话，走 `update_task` / `update_requirement` 在原记录上追加描述或写更新日志，不新建记录、不丢原文。

### 1.4 数据层：飞书多维表格 + 表格公式

- 主数据源 = PRD §6 那张 Base（现已是 8 张表，§4 详列真实字段）。
- **凡是表格里能用公式解决的，服务端一律不重复实现**：项目「任务完成度」、任务「剩余天数 / 是否逾期 / 任务完成率」等公式已在表内（真实 Base 已配置）。服务端只负责「读写记录 + 触发计算字段依赖的字段更新」，视图和公式在表格里维护。
- 这样服务端逻辑最薄、最不容易错，且数据随时可在表格里人工核对、补录（PRD 明确支持手动加行）。

### 1.5 权限与身份：Aily 的做法 vs 自建的做法

| | 读 / 写多维表格 | 发群消息 / 读群消息 |
|---|---|---|
| Aily 现状（双身份） | `--as user`（权限绑用户） | `--as bot`（不冒用户身份） |
| **自建推荐** | 优先**应用身份统一**（tenant_access_token）——把 Base 添加机器人为协作者即可 | 机器人身份天然是 bot |

- 自建应用一旦被授权进 Base（Base 的「添加协作者」里加上机器人应用），**读写表格和发消息都统一用应用身份**，比 Aily 的双身份更简单。
- 若目标 Base 无法授权给应用，**回退双身份**：用 `user_access_token`（OAuth，scope 含 bitable 读写）读表，用 bot token 发消息——和 Aily 现状一致。优先实现应用身份方案。

---

## 第 2 部分 · 技术选型

### 2.1 四条路线本质

| 路线 | 谁当「大脑」 | 谁当「身体」 | 谁当「房子」 | 开发量 | 典型形态 |
|---|---|---|---|---|---|
| A. 直连大模型 API | 任意 LLM API（DeepSeek / Qwen / GLM / Claude / GPT） | 自己写最简 agent loop + function calling | 自己的服务器 / 本地常驻 | 中 | **自研 Bot 服务（推荐形态）** |
| B. 接 Claude Code | Claude 模型 | Claude Code CLI | 服务器 / 本地 + 订阅或按量 | 低 | 把「终端代码 agent」硬当机器人跑 |
| C. 接 Codex | OpenAI 模型 | Codex CLI | 服务器 / 本地 + 计费 | 低 | 同上 |
| D. 接 OpenClaw | 任意 LLM | OpenClaw 开源框架（自带 IM 适配器 / 定时） | 服务器 / 本地 | 中 | 开源无人值守 agent 框架跑的 IM 机器人 |

### 2.2 选型结论与理由

> **最终推荐：路线 A —— 自研轻量 Bot 服务（Python + lark-oapi SDK + 直连 LLM API + function calling）。**
> **Plan B：路线 D OpenClaw（想少写代码时）。**
> **路线 B / C（Claude Code / Codex）不当机器人常驻，但作为「开发工具」用来写路线 A 的代码——这正是「交给 Codex 开发」的正确用法。**

理由：

1. **场景本质是「有状态、常驻、事件驱动的机器人服务」，不是「终端代码 agent」**。Codex / Claude Code 每次调用都带大量系统提示、上下文窗口大、token 消耗是「对话级」的几倍，拿来无人值守常驻当机器人是错配——稳定性差、成本高。
2. **成本最低且模型任选**：直连 DeepSeek / Qwen 这类中文强模型，function calling 全部支持，价格只有旗舰的几十分之一；真要更强再切 Claude / GPT，代码一行不用改。
3. **function calling 是行业标准能力**，自己写 agent loop 只需 100–200 行，无框架锁、完全可控。
4. **飞书官方 SDK（lark-oapi）成熟**：事件订阅（WebSocket 长连接，免公网）、多维表格读写、发消息、查成员全部现成 API，开发量集中在业务逻辑，整体 800–1500 行 Python。
5. **和 Aily 的关系最清楚**：Aily 就是「路线 A 的托管版」。自建 = 把 Aily 托管的那层用自己的进程顶替，行为可完全对齐 PRD F1–F13。

### 2.3 成本模型：自建 vs Aily

| 成本项 | Aily 平台方式 | 自建方式（路线 A 推荐配置） |
|---|---|---|
| 平台服务费 | 按订阅 / 用量计费 | 0 |
| LLM 费用 | 含在 Aily 用量里（模型不可换） | 直连 API：DeepSeek / Qwen 档每百万 tokens 几分～几元；群机器人日消耗约几十～几百 k tokens → 每月约几元～几十元 |
| 服务器 | Aily 托管 | 本地 Mac 常驻 0 元；云服务器轻量约 ¥20–60/月（可选） |
| 开发成本 | 在 Aily 内配置（少） | 一次性开发（Codex / 开发者，约 800–1500 行） |
| 运维 | Aily 维护 | 自己维护（重启 / 更新 / 日志，量很小） |
| 权限 / 数据 | 归 Aily 应用持有 | 归你自己的自建应用持有，数据完全在自己手里 |

**关于 Aily 计费的一手信息（⚠️ 部分待核实）**：

- Aily 官方计费手册：https://aily.feishu.cn/hc1u7kleqg/1cnvbb55 （需要登录 / 前端渲染，本文档撰写时无法完整抓取到套餐价格明细，**请以页面实际显示为准**）。
- 已核实（客服答复截图，OCR 原文）：「接入第三方智能体和给智能伙伴接自定义模型两者没什么区别，都是接入第三方模型；后续可能看产品侧调整会收费」。→ 即：当前第三方模型接入与自定义模型接入同价，**收费调整在路线图上**，是自建的一个现实动机。
- 结论：Aily = 省心但持续付费；自建 = 一次性开发 + 极低运营成本，长期便宜，数据和权限自主。

---

## 第 3 部分 · 飞书开放平台配置（Codex 按步骤执行，缺一不可）

### 3.1 创建应用 + 开通机器人

1. 登录飞书开放平台（https://open.feishu.cn/app ）→ 开发者后台 → **创建企业自建应用** → 记下 **App ID**（cli_xxx）与 **App Secret**（只显示一次，保存好，放 .env）。
2. 应用 → 添加应用能力 → **机器人**。

### 3.2 权限 scope（应用 → 权限管理 → 添加权限）

全部开通后需「创建版本并发布」，管理员审核后生效（⚠️ scope 名称以开放平台最新文档为准）：

| scope | 用途 |
|---|---|
| im:message:send_as_bot | 以应用身份发送消息（群回复必需） |
| im:message.group_msg | 读取群消息（收群消息事件必需） |
| im:message.p2p_msg | 读取单聊消息（若需接私聊，可先不开） |
| bitable:app | 查看、编辑多维表格（读写 Base 必需） |
| contact:user.base:readonly | 读取用户基本信息（把「张三」解析成 open_id 用） |

### 3.3 事件订阅（WebSocket 长连接）

1. 应用 → 事件与回调 → 添加事件 → **im.message.receive_v1（接收消息）**。
2. 订阅方式选 **「使用长连接接收事件」**（WebSocket 长连接，**不需要公网地址 / 不需要配回调 URL**，SDK 直连）。

### 3.4 发布 + 拉群 + Base 授权

1. 权限 / 能力变更后「版本管理与发布」→ 创建版本 → 发布（自建应用需租户管理员审核）。
2. 在飞书群里「添加机器人」搜索你的应用并添加；记下群 **chat_id**（oc_xxx，群设置或开放平台调试可查）。
3. **多维表格授权给应用**：打开目标 Base → 右上角「…」→ 添加协作者 → 搜索你的机器人应用名 → 授予可编辑权限。此后应用即可用 tenant_access_token 读写该 Base（应用身份统一，不需要 OAuth 用户授权）。
   - ⚠️ 若该 Base 无法添加机器人为协作者，**回退方案**：把应用加为「网页应用」并开通 OAuth（scope 含 bitable:app），用 user_access_token 读写表格、bot token 发消息（同 Aily 双身份）。优先实现应用身份方案。

### 3.5 配置项（.env）

```
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_BASE_TOKEN=Z2rcbRElNauBTmsySI6c7S46ntE       # 项目 Base
FEISHU_REQUIREMENT_TABLE_ID=tblDMh4ugeVEgoNg        # 需求表（v1 目标模型新增）
FEISHU_TASK_TABLE_ID=tblxY7V5NXfyiIkG               # 任务表
FEISHU_PROJECT_TABLE_ID=tblubema3wO4HBrp            # 项目表
FEISHU_DECISION_TABLE_ID=tblNHufHr16mFV92           # 决策日志
FEISHU_MEMBER_TABLE_ID=tblOwKqkEWuKBCxu             # 成员表
FEISHU_REPORT_TABLE_ID=tblogWAMyrddH3r6             # 周报表
FEISHU_WORKLOG_TABLE_ID=tblFqDKV10sQi4vO            # 工时表（已建）
FEISHU_TARGET_CHAT_ID=oc_e63829e8dd009fb398a380621d067d85   # 目标项目群
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com/v1            # 或通义/智谱等 OpenAI 兼容地址
LLM_MODEL=deepseek-chat
BOT_NAME=项目管理agent                               # 群里 @ 的名字，用于识别是否被@
```

---

## 第 4 部分 · 数据模型与多维表结构（按领域模型 v1 · 需求表 + 任务表 M:N）

### 4.1 概念基线：需求 ≠ 任务（M:N）

- **需求（Requirement）** = 做什么 / 为什么（what / why），含验收标准。回答「我们要解决什么业务问题、做到什么程度算完」。
- **任务（Task）** = 怎么做（how），具体的执行工作单元。回答「由谁、花多少工时、把需求落地」。
- 两者是 **M:N（多对多）**：一个需求可拆成多个任务；一个任务可服务多个需求。用**双向「关联记录」字段**表达（需求表加「关联任务」、任务表加「关联需求」，飞书自动维护多对多），**不建独立关联表**。
- 需求与任务**无强绑定关键词**：靠「上下文 + 创建人角色」区分——业务方 / PM 建需求，PM / 技术负责人提取任务（领域模型 §3 规则 4）。
- **责任人 vs 执行人**：责任人是问责方（RACI 的 A，初始 = 小队长）；执行人是实际做的人（RACI 的 R，小队长细分派时填）。群聊 @ 一人默认同写；@ 小队长后再细化则责任人在前、执行人在后（领域模型 §3 规则 5）。

### 4.2 ER 关系总览

```
项目 1──N 需求  M:N  任务  N──1 项目
         │                 │
         │                 ├──1 责任人(user) + N 协同人(user)
         │                 └──N 任务执行人(link→成员) —— 成员表「我的任务」钻取来源
任务 1──N 工时（工时归属主体是任务，人是填报者）
决策日志 关联 任务/项目（"谁拍板、为什么、何时"的痕）
```

### 4.3 真实 Base 表结构（8 张表 · 字段已按真实情况核对）

Base token：`Z2rcbRElNauBTmsySI6c7S46ntE`。**Codex 落库时字段名、选项值一律按本表，不要自造。**

#### 需求表 tblDMh4ugeVEgoNg（状态机：草稿 → 评审中 → 已采纳 → 研发中 → 已实现 → 已验收 → 关闭，+已拒绝）

| 字段 | 类型 | 说明 |
|---|---|---|
| 需求名称 | 文本 | 必填 |
| 描述 | 文本 | 含业务价值（为什么提这条） |
| 验收标准 | 文本 | 「做到什么算完」——需求与任务的边界，F1 识别时尽量让 LLM 提炼 |
| 提出人 | 人员 | 业务方 / PM |
| 来源 | 单选 | 业务交流 / 群聊 / 评审 |
| 优先级 | 单选 | P0 / P1 / P2 / P3 |
| 状态 | 单选 | 草稿 / 评审中 / 已采纳 / 研发中 / 已实现 / 已验收 / 关闭 / 已拒绝 |
| 所属项目 | 关联→项目 | 1:N |
| 关联任务 | 关联→任务 | **M:N**（与任务表「关联需求」双向自动维护） |

#### 任务表 tblxY7V5NXfyiIkG（状态机：未开始 → 进行中 → 已完成 / 已停滞，+已确认(遗留)）

| 字段 | 类型 | 说明 |
|---|---|---|
| 任务 | 文本 | 必填 |
| 状态 | 单选 | 未开始 / 进行中 / 已完成 / 已停滞 / 已确认 |
| 优先级 | 单选 | P0 / P1 / P2 / P3 |
| 关联需求 | 关联→需求 | **M:N**（可空；设计/测试任务可独立不关联） |
| 所属项目 | 关联→项目 | 1:N |
| 责任人 | 人员 | 问责方，初始 = 小队长（F8 双写字段一） |
| 任务执行人 | 关联→成员 | 实际执行人，驱动成员表「我的任务」钻取（F8 双写字段二） |
| 协同人 | 人员 | 多选 |
| 开始时间 / 截止时间 | 日期 | 排期（F12）依赖 |
| 实际完成时间 | 日期 | F6 标记完成时写 |
| 预估工时 / 实际工时 | 数字 | 人天（F11） |
| 任务完成率 | 数字 | F13，0–100 |
| 剩余天数 / 是否逾期 | 公式 | 表内自动算（F12），服务端不实现 |
| ⏱️ 工时 | 关联→工时 | 任务下挂的工时记录 |
| 需求描述 | 文本 | **遗留字段**（旧模型用，新记录留空即可，不删以免影响历史） |

#### 项目表 tblubema3wO4HBrp（状态机：未启动 → 推进中 → 已完成）

| 字段 | 类型 | 说明 |
|---|---|---|
| 项目名称 | 文本 | 必填 |
| 目标 | 文本 | 为什么做 |
| 项目情况概述 | 文本 | 进展速记（速递/周报可回写） |
| 总负责人 | 人员 | 问责方 |
| 状态 | 单选 | 未启动 / 推进中 / 进行中(遗留) / 已完成 |
| 项目截止时间 | 日期 | |
| 对应任务 | 关联→任务 | 1:N |
| 需求 | 关联→需求 | 1:N |
| 任务数量 | 查找 | 表内自动算 |
| 任务完成度 | 公式 | 项目级完成率（F13，表内自动算） |
| 成员 | 查找 | 该项目的任务挂的人 |
| 项目进展 | 关联→周报 | |
| 最后更新时间 | 自动 | |

#### 成员表 tblOwKqkEWuKBCxu

| 字段 | 类型 | 说明 |
|---|---|---|
| 成员名 | 公式 | |
| 账号 | 人员 | 与通讯录人员对应，姓名→open_id 解析来源 |
| 部门 | 单选 | 基础产品部 / 用户增长部 / 创新功能部 |
| 任务 | 关联→任务 | 与任务表「任务执行人」双向——「我的任务」钻取来源 |

#### 决策日志表 tblNHufHr16mFV92

| 字段 | 类型 | 说明 |
|---|---|---|
| 决策标题 | 文本 | 必填 |
| 决策内容 | 文本 | 谁拍板、为什么 |
| 影响范围 | 文本 | |
| 备注 | 文本 | |
| 决策人 | 人员 | 多选 |
| 决策时间 | 日期时间 | |
| 状态 | 单选 | 已决策 / 执行中 / 已完成 / 已废弃 |
| 关联任务 | 关联→任务 | |
| 关联项目 | 关联→项目 | |

> 注：领域模型 v1 建议决策状态为「提议 / 已确认 / 已推翻」，真实 Base 用「已决策 / 执行中 / 已完成 / 已废弃」——以真实 Base 为准。

#### 工时表 tblFqDKV10sQi4vO（F11，已建）

| 字段 | 类型 | 说明 |
|---|---|---|
| 任务 | 文本 | 冗余可读名（联调方便） |
| 关联任务 | 关联→任务 | 归属主体（与任务表「⏱️ 工时」双向） |
| 成员 | 人员 | 填报者 |
| 日期 | 日期 | |
| 时长 | 数字 | 小时 |
| 备注 | 文本 | |

#### 周报表 tblogWAMyrddH3r6（F4，可写）

| 字段 | 类型 | 说明 |
|---|---|---|
| 汇报标题 | 公式 | |
| 汇报人 | 人员 | |
| 所属项目 | 关联→项目 | |
| 进度内容 | 文本 | 周报正文 |
| 日期 | 日期 | |

#### 快速上手 tblj740cKSkiquB3

系统默认表，非业务数据，不动它。

### 4.4 状态机汇总（服务端严格用这些枚举值）

| 实体 | 状态枚举（按真实 Base） | 流转 |
|---|---|---|
| 需求 | 草稿 / 评审中 / 已采纳 / 研发中 / 已实现 / 已验收 / 关闭 / 已拒绝 | 草稿→评审中→已采纳→研发中→已实现→已验收→关闭（+已拒绝） |
| 任务 | 未开始 / 进行中 / 已完成 / 已停滞 / 已确认 | 未开始→进行中→已完成（或已停滞）；已确认为旧数据遗留值 |
| 决策 | 已决策 / 执行中 / 已完成 / 已废弃 | 已决策→执行中→已完成 |
| 项目 | 未启动 / 推进中 / 已完成 / 进行中 | 未启动→推进中→已完成 |

### 4.5 与领域模型 v1 的两处差异（如实标注，Codex 自行取舍）

1. **任务.type（开发/设计/测试/缺陷）字段在真实 Base 尚不存在**。领域模型 v1 定义「Bug = 任务.type=缺陷」，但当前 Base 任务表没有 type 字段——Bug 场景目前用「任务标题/描述标注 + 关联原需求」表达。若需完整对齐领域模型 v1，需在任务表新增「type」单选字段（开发/设计/测试/缺陷）——**标注为可选增强**，不影响 F1–F13 闭环。
2. 决策状态枚举见 4.3（领域模型概念 vs 真实 Base 以真实 Base 为准）。

---

## 第 5 部分 · 代码结构 + function calling 工具 schema 完整清单

### 5.1 代码结构

```
feishu-pm-agent/
├── README.md
├── requirements.txt          # lark-oapi>=1.6  openai>=1.30  apscheduler>=3.10  python-dotenv>=1.0
├── .env                      # 不提交 git（见 §3.5）
├── config.py                 # 读 .env + 常量 + 表/字段映射表
├── main.py                   # 入口：启动长连接 + 后台定时器
├── event_handler.py          # 收到消息：过滤 → 取文本 → 交 agent
├── agent.py                  # agent loop：system prompt + 上下文 + LLM function calling
├── tools_schema.py           # function calling 的 JSON schema 清单（§5.4）
├── tools.py                  # 工具实现：每个 function 的落地代码
├── bitable_store.py          # 多维表格读写封装（需求/任务/项目/决策/成员/工时/周报）
├── messenger.py              # 发群消息封装
├── user_resolver.py          # 姓名 → open_id / 成员记录 ID
├── dedup.py                  # 建记录去重指纹（验收标准 1）
├── scheduler.py              # APScheduler：速递 / 周报
├── briefs.py                 # 速递 / 周报内容生成
└── tests/sim_bot.py          # 模拟 bot 自测：按脚本抛对话、断言表格
```

### 5.2 agent loop（agent.py 伪代码）

```python
def handle_text(chat_id, sender_open_id, text):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}]
    # 循环：最多 N 轮，直到 LLM 不再要求调工具
    for _ in range(MAX_ITERS):
        resp = llm.chat(messages, tools=TOOLS, tool_choice="auto")
        if not resp.tool_calls:
            return resp.content                 # 最终回复，发给群里
        messages.append({"role": "assistant", "content": None,
                         "tool_calls": resp.tool_calls})
        for tc in resp.tool_calls:
            result = run_tool(tc.function.name, json.loads(tc.function.arguments),
                              chat_id, sender_open_id)
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps(result, ensure_ascii=False)})
```

### 5.3 需求 / 任务分类识别（v1 模型新增的关键逻辑）

LLM 一次调用可能同时识别出多个动作（如「把 X 拆成两个任务并派给张三」→ create_task ×2 + assign_task）。**最关键的判断是「这条消息该落需求表还是任务表」**，遵循领域模型 §7 的映射：

| 群聊信号 | 落表 | 工具 |
|---|---|---|
| 「开个新项目 / 第X期」 | 项目表 | create_project |
| 业务方描述痛点 / 「希望系统能…」「加个…」 | **需求表** | create_requirement |
| 「把这个拆成…任务 / 谁来做」 | **任务表**（关联需求） | create_task |
| 「就这么定了 / 确定按X做」 | 决策日志 | record_decision |
| 报「今天做了X小时」 | 工时表 | log_work |
| 提 bug / 「这里有问题」 | 任务表（type=缺陷，见 §4.5；无 type 字段则标题标注） | create_task |
| @Agent 「改状态为已完成」 | 任务/需求状态 | update_*_status |
| 普通闲聊 / 无项目含义 | **忽略，不建任何记录** | — |

**分类规则（写进 SYSTEM_PROMPT）**：先识别「是否在谈项目相关的事」（防闲聊）；再判定落哪个实体。需求与任务靠「上下文 + 创建人角色」区分，不靠关键词硬匹配——**描述"要做什么/为什么" → 需求；描述"谁来做、怎么做、拆成什么执行单元" → 任务**。LLM 拿不准时，返回一个「需要澄清」的回复而不是瞎建。

### 5.4 工具 schema 完整清单（tools_schema.py，给 Codex 照抄实现）

#### 1. create_requirement —— 建需求（F1）

```json
{"name": "create_requirement", "description": "群里识别到新需求（业务方/PM 提'要做什么/为什么'）时，向需求表建一条记录",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string", "description": "需求名称"},
   "description": {"type": "string", "description": "需求描述，含业务价值"},
   "acceptance": {"type": "string", "description": "验收标准，'做到什么算完'（可空，尽量提炼）"},
   "project": {"type": "string", "description": "所属项目名（可空，按项目表匹配）"},
   "priority": {"type": "string", "enum": ["P0", "P1", "P2", "P3"], "description": "优先级（可空）"},
   "source": {"type": "string", "enum": ["业务交流", "群聊", "评审"], "description": "来源，默认群聊"}},
  "required": ["name"]}}
```

#### 2. create_task —— 拆任务 / 提取执行单元（从需求拆出）

```json
{"name": "create_task", "description": "把需求拆成执行任务，或群里直接派单个任务时，向任务表建一条记录",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string", "description": "任务名称"},
   "requirement": {"type": "string", "description": "关联的需求名称（可空；若正在谈某条需求，必填，用于 M:N 关联）"},
   "project": {"type": "string", "description": "所属项目名（可空）"},
   "priority": {"type": "string", "enum": ["P0", "P1", "P2", "P3"], "description": "优先级（可空）"},
   "assignee": {"type": "string", "description": "责任人姓名（可空）"},
   "due_date": {"type": "string", "description": "截止时间 YYYY-MM-DD（可空）"}},
  "required": ["name"]}}
```

#### 3. update_task / 4. update_requirement —— 修改追加（验收标准 2）

```json
{"name": "update_task", "description": "对已有任务追加信息或修改字段（不新建、保留原文）",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string", "description": "要改的任务名"},
   "description_to_append": {"type": "string", "description": "追加的描述/更新内容（可空）"},
   "due_date": {"type": "string"}, "priority": {"type": "string", "enum": ["P0","P1","P2","P3"]}},
  "required": ["name"]}}

{"name": "update_requirement", "description": "对已有需求追加信息或修改字段（不新建、保留原文）",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string", "description": "要改的需求名"},
   "description_to_append": {"type": "string"},
   "acceptance": {"type": "string", "description": "验收标准（可空）"},
   "priority": {"type": "string", "enum": ["P0","P1","P2","P3"]}},
  "required": ["name"]}}
```

#### 5. update_task_status / 6. update_requirement_status —— 改状态（F6）

```json
{"name": "update_task_status", "description": "把任务状态改为指定值",
 "parameters": {"type": "object", "properties": {
   "task_name": {"type": "string"},
   "status": {"type": "string", "enum": ["未开始", "进行中", "已完成", "已停滞", "已确认"]}},
  "required": ["task_name", "status"]}}

{"name": "update_requirement_status", "description": "把需求状态改为指定值",
 "parameters": {"type": "object", "properties": {
   "requirement_name": {"type": "string"},
   "status": {"type": "string", "enum": ["草稿", "评审中", "已采纳", "研发中", "已实现", "已验收", "关闭", "已拒绝"]}},
  "required": ["requirement_name", "status"]}}
```

#### 7. query_task / 8. query_requirement —— 查状态（F5）

```json
{"name": "query_task", "description": "按名称/负责人/项目查询任务，返回状态、负责人、执行人、截止、所属项目、关联需求",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string"}, "assignee": {"type": "string"}, "project": {"type": "string"}}}}

{"name": "query_requirement", "description": "按名称/项目查询需求，返回状态、验收标准、提出人、关联任务",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string"}, "project": {"type": "string"}}}}
```

#### 9. assign_task —— 人员分配（F8，**双写**：责任人 + 任务执行人 + 协同人）

```json
{"name": "assign_task", "description": "把任务派给某人（可带协同人），双写'责任人'人员字段与'任务执行人'成员关联字段，保证成员表'我的任务'钻取立即生效",
 "parameters": {"type": "object", "properties": {
   "task_name": {"type": "string"},
   "assignee": {"type": "string", "description": "责任人姓名（主负责人）"},
   "collaborators": {"type": "array", "items": {"type": "string"}, "description": "协同人姓名列表（可空）"},
   "due_date": {"type": "string", "description": "截止时间 YYYY-MM-DD（可空）"}},
  "required": ["task_name", "assignee"]}}
```

#### 10. record_decision —— 记决策（F2 / F7）

```json
{"name": "record_decision", "description": "群里出现确定/拍板结论时写入决策日志",
 "parameters": {"type": "object", "properties": {
   "title": {"type": "string"}, "content": {"type": "string"},
   "related_task": {"type": "string"}, "related_project": {"type": "string"}},
  "required": ["title", "content"]}}
```

#### 11. create_project —— 建项目（F10）

```json
{"name": "create_project", "description": "群里说开新项目时向项目表建记录",
 "parameters": {"type": "object", "properties": {
   "name": {"type": "string"}, "goal": {"type": "string"},
   "owner": {"type": "string", "description": "总负责人姓名（可空）"},
   "status": {"type": "string", "enum": ["未启动", "推进中", "已完成", "进行中"], "default": "未启动"}},
  "required": ["name"]}}
```

#### 12. log_work —— 填工时（F11）

```json
{"name": "log_work", "description": "成员填报工时",
 "parameters": {"type": "object", "properties": {
   "task_name": {"type": "string"}, "member": {"type": "string"},
   "date": {"type": "string", "description": "YYYY-MM-DD"}, "hours": {"type": "number"},
   "note": {"type": "string"}},
  "required": ["task_name", "member", "date", "hours"]}}
```

> 实现提示：LLM 可能把「一句话」同时判定为多个动作（如「把 X 派给张三并标记进行中」）——工具调用天然支持一次返回多个 tool_calls，逐个执行即可。

### 5.5 数据映射与落库规则（bitable_store.py）

多维表格写入格式（lark bitable v1 API 的 fields 对象，⚠️ 以 lark-oapi 最新版文档为准）：

| 字段类型 | 写入格式 |
|---|---|
| 文本 | {"任务": "上线公告"} |
| 单选（状态/优先级/来源） | {"状态": "已完成"}（写选项名即可） |
| 人员（提出人/责任人/协同人/决策人/成员） | {"责任人": [{"id": "ou_xxx"}]} |
| 关联→成员（任务执行人） | {"任务执行人": [{"record_ids": ["rec_member"]}]} |
| 关联→需求/任务/项目（M:N / 1:N） | {"关联需求": [{"record_ids": ["rec_req"]}]} |
| 日期 | {"截止时间": 1786496000000}（毫秒时间戳） |

**M:N 关联（需求 ↔ 任务）写一侧即可**：写任务表的「关联需求」= [{"record_ids": ["rec_req"]}]，需求表「关联任务」由双向关联字段自动同步。

**F8 双写实现（重点，assign_task 执行时）**：

1. user_resolver.name_to_open_id("张三")：用通讯录 / 成员表把姓名解析成 open_id；查不到 → 回复「成员表里没有张三，请先加成员」并不写库；
2. 写「责任人」字段 = [{"id": open_id}]；
3. 查成员表按「成员名 / 账号」找到张三的**记录 ID**，写「任务执行人」字段 = [{"record_ids": [member_record_id]}] —— 这步保证成员表「我的任务」钻取立即生效；
4. 协同人同 1 步写「协同人」字段。

> ⚠️ 参考数据核对：抽样任务记录显示 Aily 侧当前已写「任务执行人」，抽样记录中「责任人」尚空。自建实现**按 PRD §5.8 双写两个字段**，以通过 PRD §8 验收标准 6（双写一致 + 成员钻取立即可见）。

---

## 第 6 部分 · 定时任务（scheduler.py）

| 任务 | 触发 | 行为 |
|---|---|---|
| 每日速递（F3） | 工作日 16:35，CronTrigger(day_of_week="mon-fri", hour=16, minute=35) | 拉当天群消息 + 任务表，LLM 生成摘要（新增待办 / 今日决策 / 风险 / 重要更新）；扫描新建任务中责任人 / 截止 / 描述为空 → 标「待补充」列出 |
| 每周周报（F4） | 每周五 14:43，CronTrigger(day_of_week="fri", hour=14, minute=43) | 汇总本周项目 / 需求 / 任务 / 决策 / 工时，LLM 生成周报发群，并写入周报表（所属项目 / 进度内容 / 日期 / 汇报人） |

- 与长连接共存：主进程跑 lark_oapi.ws.Client（阻塞），定时器用 BackgroundScheduler（独立线程）。
- 时间 / 文案建议做成配置项，方便调整。

---

## 第 7 部分 · 核心代码骨架（给 Codex 起手）

```python
# main.py —— 入口
import logging
from lark_oapi.ws import Client as WsClient
from scheduler import start_scheduler
from event_handler import on_im_message

def main():
    logging.basicConfig(level=logging.INFO)
    ws = WsClient(app_id=APP_ID, app_secret=APP_SECRET, log_level=logging.INFO)
    ws.event.im.message.receive_v1(on_im_message)   # 注册事件回调
    start_scheduler()                                # 后台定时器
    ws.start()                                       # 阻塞，保持长连接

if __name__ == "__main__":
    main()
```

```python
# event_handler.py —— 收到群消息
def on_im_message(message):
    chat_id = message.event.message.chat_id
    if chat_id != FEISHU_TARGET_CHAT_ID:          # 只处理目标项目群
        return
    msg_type = message.event.message.message_type
    if msg_type != "text":
        return
    text = json.loads(message.event.message.content)["text"]
    if not (f"@{BOT_NAME}" in text or is_trigger_phrase(text)):
        return                                     # 未被@ 且非触发词
    text = text.replace(f"@{BOT_NAME}", "").strip()
    reply = agent.handle_text(chat_id, sender_open_id(message), text)
    messenger.send_text(chat_id, reply)
```

```python
# tools.py —— 工具落地（示意 create_requirement / create_task / assign_task 的关键分支）
def create_requirement(args, chat_id, sender_open_id):
    name = args["name"]
    if dedup.is_duplicate(chat_id, "req", name):
        return {"ok": False, "msg": f"已记录过「{name}」，如需修改请说『改…』"}
    fields = {"需求名称": name, "描述": args.get("description", ""),
              "状态": "草稿", "来源": args.get("source", "群聊")}
    if args.get("acceptance"): fields["验收标准"] = args["acceptance"]
    if args.get("project"):
        fields["所属项目"] = [{"record_ids": [store.find_project(args["project"])]}]
    if args.get("priority"): fields["优先级"] = args["priority"]
    if args.get("source"): fields["来源"] = args["source"]
    rec = store.create_record(REQUIREMENT_TABLE, fields)
    dedup.mark(chat_id, "req", name)
    return {"ok": True, "record_id": rec, "msg": f"已建需求「{name}」"}

def create_task(args, chat_id, sender_open_id):
    # ... 同 create_requirement，写任务表（任务/状态=未开始）...
    if args.get("requirement"):
        req_rec = store.find_requirement(args["requirement"])
        if req_rec:
            fields["关联需求"] = [{"record_ids": [req_rec]}]   # M:N 写一侧即可
    # 关联所属项目、优先级、责任人、截止时间同 §5.5
    return {"ok": True, "record_id": rec, "msg": f"已建任务「{name}」"}

def assign_task(args, chat_id, sender_open_id):
    task_rec = store.find_task(args["task_name"])
    if not task_rec:
        return {"ok": False, "msg": f"任务表里没有「{args['task_name']}」，请先建任务"}
    oid = user_resolver.name_to_open_id(args["assignee"])
    if not oid:
        return {"ok": False, "msg": f"成员表里没有 {args['assignee']}，请先加成员"}
    member_rec = user_resolver.member_record_id(args["assignee"])
    fields = {"责任人": [{"id": oid}],                     # 双写 1：人员字段
              "任务执行人": [{"record_ids": [member_rec]}]}  # 双写 2：关联成员字段
    if args.get("collaborators"):
        fields["协同人"] = [{"id": user_resolver.name_to_open_id(c)} for c in args["collaborators"] if c]
    if args.get("due_date"): fields["截止时间"] = date_to_ts(args["due_date"])
    store.update_record(TASK_TABLE, task_rec, fields)
    return {"ok": True, "msg": f"已把「{args['task_name']}」派给 {args['assignee']}"}
```

---

## 第 8 部分 · 分阶段验收步骤（对照 PRD §8 验收标准）

| 阶段 | 目标 | 验收点（跑通即过） |
|---|---|---|
| **P0 打通通道** | 事件订阅 + 收发消息 | 测试群 @机器人原样回一句；机器人能主动发一条消息 |
| **P1 F1/F2** | 需求识别 + 决策记录（v1 模型：需求落**需求表**） | 群里说「要做 X」→ **需求表**新增一条（名称/描述/状态=草稿，带验收标准更佳）；说「确定了按方案B」→ 决策日志新增一条；群内各给一句简短确认；**连续 5 条同一需求只建 1 条（验收 1）、修改在原记录追加（验收 2）** |
| **P2 F5/F6** | @查状态 / 改状态 | 「查 XX 状态」→ 返回 状态/负责人/截止/所属项目；「把 XX 标为已完成」→ 表格与群回复同步更新（验收 3） |
| **P3 F8** | 人员分配（双写） | 「把 XX 派给张三」→ 责任人=张三 且 任务执行人=张三的成员记录（**双写一致**，验收 6）；成员表「我的任务」钻取立即能看到；协同人支持多人 |
| **P4 F3/F4** | 每日速递 + 周报 | 手动触发速递：输出当日摘要，责任人/截止为空的新任务标「待补充」（验收 7）；手动触发周报：输出本周汇总并可写入周报表 |
| **P5 F10/F11** | 建项目 + 工时 | 「开个新项目 XX」→ 项目表新增（验收 8）；「今天在 XX 花了 3h」→ 工时表新增，周报纳入 |
| **P6 F9/F12/F13** | 合规开关 + 排期量化 | 敏感模式开关（配置项）；任务表开始/截止后，剩余天数/是否逾期/完成率/项目完成度由表格公式自动更新（验收 9），速递高亮逾期 |

> P0–P4 即 PRD「Now + Next 最小闭环」；P5–P6 为 PRD 规划项。每阶段验收用「测试群 + 模拟对话脚本」（tests/sim_bot.py 抛对话、断言表格变化）；跑通才进下一步。
> **相对 v1 文档的差异**：P1 的「建需求」现在写需求表而非任务表；P1/P2/P3 需额外验证「需求↔任务 M:N 关联」「责任人+任务执行人双写」两个新验收点。

**全量回归 + 真实群试跑一周**（速递 16:35 / 周报周五 14:43 到点正常）。

---

## 附录 A · 与 PRD F1–F13 能力覆盖对照（自建可实现性，如实标注）

| 能力 | PRD 状态 | 自建能否完整实现 | 自建实现方式 / 说明 |
|---|---|---|---|
| F1 需求自动识别 | ✅ 已部署 | ✅ **完整实现** | function calling 识别「要做/加个」→ create_requirement 写**需求表**（v1 模型） |
| F2 决策自动记录 | ✅ 已部署 | ✅ **完整实现** | record_decision 写决策日志，关联任务/项目 |
| F3 每日速递 + 缺失追问 | ✅/⚠️ | ✅ **完整实现** | APScheduler 16:35 + LLM 摘要 + 空字段扫描标「待补充」 |
| F4 每周周报 | ✅ 已部署 | ✅ **完整实现** | APScheduler 周五 14:43 + LLM 汇总 + 可写周报表 |
| F5 被@查状态 | ⚠️ 待验 | ✅ **完整实现** | query_task / query_requirement 读表返回 |
| F6 被@改状态 | ⚠️ 待验 | ✅ **完整实现** | update_task_status / update_requirement_status 写表 + 群确认 |
| F7 收敛信号检测 | ⚠️ 待验 | ✅ **完整实现** | 触发词 + record_decision，回复 ≤1 句 |
| F8 人员分配（双写） | ⚠️ 待验 | ✅ **完整实现** | assign_task 双写「责任人」人员字段 +「任务执行人」成员关联字段 +「协同人」 |
| F9 合规开关 | 🔲 规划 | ⚠️ **需自行开发** | 配置项「敏感模式」+ 指定内容不处理/脱敏逻辑；自建实现反而更直接 |
| F10 自动建项目 | 🔲 规划 | ✅ **完整实现** | create_project 写项目表，后续需求/任务按「所属项目」关联 |
| F11 工时管理 | 🔲 规划 | ✅ **完整实现** | 工时表已建（tblFqDKV10sQi4vO），log_work 写入 + 汇总公式 |
| F12 公式排期与里程碑 | 🔲 规划 | ✅ **完整实现** | 剩余天数/是否逾期公式已在表内，服务端只触发字段更新；速递高亮逾期 |
| F13 进度量化 | 🔲 规划 | ✅ **完整实现** | 项目完成度（公式）+ 任务完成率已在表内；服务端不重复实现 |
| 需求↔任务 M:N | 目标模型 | ✅ **完整实现** | 双向「关联记录」字段，写一侧自动同步（§5.5） |
| 定时播报（每日/每周） | ✅ | ✅ **完整实现** | 服务端 APScheduler，时间/文案可配 |
| 成员「我的任务」自看 | — | ✅ **完整实现** | 成员表「任务(关联)」钻取（双写对了即生效），无需服务端 |
| 团队共享 / 权限控制 | — | ⚠️ **需自行设计** | 自建应用的 Base 协作者权限即共享边界；如需「按人隔离」需单独设计（PRD §10 注明现为便捷入口非权限隔离） |
| 群事件触发 | ✅ | ✅ **完整实现** | 飞书长连接事件订阅，无需轮询 |

**一句话总结**：**F1–F8、F10–F13 及全部定时能力、需求↔任务 M:N，自建都可完整实现**（数据模型、字段、公式直接用现有 Base 那套）；真正要「自行开发替代」的只有三块——**多维表格读写链路**（用应用授权 + SDK，不依赖 Aily 工具层）、**定时/事件触发**（服务端自己调度）、**团队共享权限**（以 Base 协作者为边界，如需更细需自行设计）。加上 F9 合规开关需自行开发。这四块在本文档 §3 / §5 / §6 / 附录 A 均已给落地方案。

## 附录 B · 与 Aily 现状能力栈逐项对照（自建去哪一层找）

| Aily 提供的能力 | 自建对应的替代 | 在本文档哪节 |
|---|---|---|
| 托管 Agent 运行环境 | 自己的服务器 / 本地进程 | §1.1、§7 |
| 内置 LLM（按量计费） | 直连 LLM API（可选便宜模型） | §1.3、§5.2 |
| 飞书事件订阅 / 被@触发 | 自建应用事件订阅（长连接） | §3.3 |
| 定时任务（速递/周报） | APScheduler 定时 | §6 |
| 多维表格读写工具 | lark-oapi + 应用授权 | §3.4、§5.5 |
| 发群消息 | bot token 发消息 | §3.4、§7 |
| 姓名→用户解析 | 通讯录 API + 成员表 | §5.5 |
| 平台计费 | 0（一次开发 + LLM 按量） | §2.3 |

## 附录 C · 参考资料与待核实项

| 项 | 参考 / 状态 |
|---|---|
| 飞书开放平台应用配置 | https://open.feishu.cn/app （scope 名称、事件订阅以平台最新文档为准，⚠️ 待核实） |
| lark-oapi（飞书官方 Python SDK） | 最新稳定版 1.6.x（PyPI：https://pypi.org/project/lark-oapi/ ），requirements 用 lark-oapi>=1.6 ⚠️ 以 PyPI 最新为准 |
| Aily 计费手册 | https://aily.feishu.cn/hc1u7kleqg/1cnvbb55 （需登录/前端渲染，本文档无法抓取明细，⚠️ 以页面为准） |
| 第三方智能体收费 | 客服答复（截图 OCR）：「接入第三方智能体和给智能伙伴接自定义模型两者没什么区别，都是接入第三方模型；后续可能看产品侧调整会收费」 |
| 领域模型 v1 | 《领域模型与业务逻辑（飞书群聊项目管理智能体）v1 定稿》 |
| PRD | 《飞书项目管理 Agent-PRD》（F1–F13、验收 §8、目标模型 §6.0） |

---

*本文档为 Codex 开发任务书与自建方案说明；飞书 API 精确参数 / scope 名称 / SDK 调用以开放平台文档与 lark-oapi 最新版为准。*
