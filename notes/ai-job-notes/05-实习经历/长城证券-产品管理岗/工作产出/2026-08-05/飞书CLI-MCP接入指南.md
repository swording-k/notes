# 飞书 CLI / MCP 接入指南（PM Agent Demo 用）

> 目的：让"我"(WorkBuddy 里的助手)能直接操作飞书，从而动手搭建 PRD 里的群聊项目管理 Agent。
> 状态：**工具已安装并验证可用，唯一缺的是账号授权（需你本人在浏览器点一下）。**

## 1. 结论先讲

飞书**官方**同时提供了 CLI 和 MCP，都是 MIT 开源、官方维护：

| 工具 | 包名 | 用途 | 给谁用 |
|---|---|---|---|
| 飞书官方 CLI | `@larksuite/cli` | 终端命令直接操作飞书（IM / 多维表格 / 云文档 / 日历 / 事件消费…） | 我（WorkBuddy）从终端驱动；也适合任何能跑命令的 Agent |
| 飞书官方 OpenAPI MCP | `@larksuiteoapi/lark-mcp` | 把飞书 API 封装成 MCP 工具 | Codex / Claude Code / Cursor 这类 MCP 客户端 |

**本次 demo 走 CLI 路线**：我已经在本地装好并验证可用，下一步你完成授权，我就能从终端真正操作飞书、把 Agent 搭出来。

## 2. 我已经做完的部分（证据）

- 安装命令：`npx -y @larksuite/cli@latest --help` ✅ 成功，版本 **v1.0.83**
- 命令面覆盖 PRD 全部需求：
  - `im`：消息 / 群聊管理
  - `base`：多维表格（需求池）
  - `docs`：云文档（决策日志）
  - `event`：实时事件消费（群消息"耳朵"）
  - `auth` / `config`：授权与配置
- `lark-cli doctor` 当前状态：`cli_version` pass，但 `config_file: fail`（未授权）。

## 3. 你只需补的一步：授权

CLI 不授权什么都调不了。两个路径，二选一：

### 路径 A：没有飞书应用，让 CLI 帮你新建（推荐首次）

在终端**后台**跑（它会输出一个验证 URL，你把 URL 在浏览器打开完成绑定）：

```bash
lark-cli config init --new
```

> 说明：这个命令会阻塞等浏览器验证。让我帮你后台跑、把 URL 截出来给你打开即可；
> 不想新建应用、想用公司已有的测试应用，走路径 B。

### 路径 B：已有飞书自建应用（App ID + App Secret）

```bash
lark-cli config init --app-id <你的APP_ID> --app-secret-stdin
# 然后按提示从 stdin 输入 App Secret（避免明文出现在进程列表）
```

### 用户身份授权（可选，但建议做）

默认应用身份只能发消息 / 建文档；要**读你的私聊、日程、个人文档**，需再跑一次用户授权：

```bash
lark-cli auth login      # Device Flow，浏览器点一下
# 或生成二维码：lark-cli auth qrcode
```

## 4. 我们的 demo 需要在开放平台开的权限

| PRD 能力 | 需要的飞书权限（scope） | 对应命令行 |
|---|---|---|
| 接收群消息（耳朵） | 接收消息 `im.message.receive_v1` 事件 + 机器人进群 | `event consume im.message.receive_v1` |
| 读群聊历史 | 获取群消息 `im:message` / `im:message:readonly` | `im +chat-messages-list` |
| 发消息 / 回复 | 发送消息 `im:message:send_as_bot` | `im +messages-send` / `+messages-reply` |
| 建测试群 | 创建群 `im:chat` | `im +chat-create` |
| 多维表格需求池 | 多维表格读写 `bitable:app` / `bitable:app:readonly` | `base +base-create` / `+field-create` / `+data-query` / record 增改 |
| 云文档决策日志 | 云文档读写 `docx:document` / `drive:drive` | `docs` / `markdown` |

> 用 CLI 官方工具，`config init --new` 通常会引导把常用权限勾上；缺权限时 CLI 会提示你补，按提示去开放平台后台开即可。

## 5. PRD 能力 → CLI 命令映射（证明我真的能操作）

| PRD 里的功能 | 具体 CLI 命令 |
|---|---|
| 建测试群并把 Bot 拉进去 | `lark-cli im +chat-create --invites <user/bot>` |
| 实时监听群消息 | `lark-cli event consume im.message.receive_v1` |
| 读群聊历史补全上下文 | `lark-cli im +chat-messages-list --chat-id <id> --order asc` |
| 被 @ 时回答问题 / 改状态 | `lark-cli im +messages-reply` |
| 新建需求池多维表格 | `lark-cli base +base-create` + `+field-create` |
| 写入 / 更新需求条目 | `lark-cli base` record 增改（`+data-query` 查） |
| 写决策日志到云文档 | `lark-cli docs` / `lark-cli markdown` |
| 每天 / 每周自动推送摘要 | `lark-cli im +messages-send` + 本地定时器（launchd / cron） |

## 6. 架构因此怎么变（对比 PRD）

原 PRD 写的是「自建 Bot + 外部 Python 后端调飞书 API」。现在飞书官方 CLI 直接覆盖了**飞书 API 调用层 + 事件接收层**，所以落地架构简化为：

```
群聊 ──(event consume 实时消息)──▶ 大脑(我写的 LLM 分类 + 版本匹配脚本)
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
      lark-cli im                   lark-cli base                lark-cli docs
      (发消息/读历史)                (需求池多维表格)             (决策日志云文档)
```

- **耳朵**：`lark-cli event consume im.message.receive_v1`（替代自己搭 webhook / 长连接）
- **大脑**：我来写（消息分类、需求关联、版本演进、建议生成）——这部分是 demo 的真正工作量
- **手**：`lark-cli im / base / docs` 系列命令（替代自己封装飞书 SDK）

> 也就是说：飞书对接的脏活 CLI 包了，我们的工作收敛成「写好那个会思考的大脑」。

## 7. 如果让 Codex 接手（备选）

Codex / Claude Code 这类 MCP 客户端走 MCP 路线，不改架构只换"驱动方式"：

```bash
# 在 Codex / Claude Code 的 mcp 配置里加：
npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>
# 只启用 demo 需要的工具可加 -t 参数，例如：
# -t im.v1.message.create,im.v1.message.list,bitable.v1.app.table.create,...
```

但无论谁做，**第一步都是第 3 节的授权**——这个绕不开。

## 8. 下一步

1. 你确认用路径 A（新建）还是路径 B（已有应用）；
2. 我后台跑 `lark-cli config init`（或你直接自己跑），把验证 URL 给你；
3. 你在浏览器打开、登录飞书、完成授权；
4. 我 `lark-cli doctor` 复核变绿，然后我开始建群 + 建表 + 写"大脑"脚本，真正动手搭 demo。
