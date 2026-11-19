# Python 后端工程（FastAPI）速成

> 你问"Web 服务框架……这是后端？"——本篇先讲清概念，再带你写一个**直接对应 JD 的"智能体服务"最小骨架**。看完你就能说"我懂后端了"。

## 1. 先搞懂概念：什么是"后端" / "Web 服务框架"

```
浏览器 / App / 业务系统（客户端）
        │  HTTP 请求（如 POST /chat）
        ▼
   ┌─────────────────────────┐
   │  你的 Python 后端程序     │  ← 你写的 AI 应用开发工程师干的活
   │  （FastAPI 框架承载）     │
   │  · 解析请求               │
   │  · 调 LLM / Agent 逻辑    │
   │  · 拼结果                 │
   └─────────────────────────┘
        │  HTTP 响应（JSON）
        ▼
   客户端展示
```

- **后端** = 跑在服务器上、处理业务逻辑、对外提供 API 的程序。
- **Web 框架** = 帮你处理"路由 / 请求解析 / 响应 / 文档"的工具，你只写业务函数。
- **为什么 AI 应用必须后端**：LLM / Agent 要被光伏业务系统（极光/逐光）调用，得有个**稳定 API 服务**（模型服务 / 智能体服务）——这正是 JD 第 1 条"Python 后端开发"的意思。
- **FastAPI vs Flask**：
  - FastAPI：**异步**、类型安全、自动生成交互式文档（/docs）、基于 Pydantic → **现代 AI 服务首选**。
  - Flask：简单、生态老，但同步、要手写很多。

## 2. 最小 FastAPI 服务（跑起来）

```bash
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()   # 创建应用实例

class ChatReq(BaseModel):      # Pydantic 模型：自动校验 + 生成文档
    message: str
    user_id: str | None = None

@app.post("/chat")             # 装饰器把 POST /chat 绑定到这个函数
async def chat(req: ChatReq):  # req 自动按 ChatReq 解析校验
    # 这里调你的 LLM / Agent（伪代码）
    reply = f"收到: {req.message}"
    return {"reply": reply}
```

运行：`uvicorn main:app --reload`，浏览器开 `http://127.0.0.1:8000/docs` 就能看到**自动生成的 API 文档**并直接试调。

## 3. 写一个"智能体服务"最小骨架（直接对应 JD）

下面这个骨架把 JD 第 1（后端）+ 第 2（Agent）+ 第 4（评测）条串起来了，**面试时能照着讲**：

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class AgentReq(BaseModel):
    session_id: str
    user_msg: str

class AgentResp(BaseModel):
    reply: str
    latency_ms: int

# 依赖注入：模拟"鉴权 / 取共享资源"（FastAPI 的 Depends）
def get_current_user(token: str | None = None):
    if not token:
        raise HTTPException(status_code=401, detail="未授权")
    return {"uid": "demo"}

@app.post("/agent", response_model=AgentResp)
async def agent_chat(req: AgentReq, user=Depends(get_current_user)):
    import time
    start = time.time()
    try:
        # 1) 查记忆（短期 session）
        # 2) 调 LLM 做任务规划（ReAct）
        # 3) 工具调用（Function Calling 调外部 API）
        reply = f"[{req.session_id}] 处理了: {req.user_msg}"
        latency = int((time.time() - start) * 1000)
        return AgentResp(reply=reply, latency_ms=latency)
    except Exception as e:
        # 全局异常处理：面试常问"怎么保证接口稳定"
        raise HTTPException(status_code=500, detail=f"Agent 执行失败: {e}")
```

**这段你能讲的工程点**（面试弹药）：
- `Depends` 依赖注入 → 解耦鉴权/资源共享
- `BaseModel` → 入参自动校验，出错返回 422
- `async` → 高并发等模型返回不阻塞
- `try/except` + `HTTPException` → 异常处理保证接口不崩
- `latency_ms` → 呼应 JD 第 4 条"响应时延评测"

## 4. 后端基础名词（加分项，先认脸）

| 名词 | 一句话 | 在 AI 服务里的角色 |
|---|---|---|
| **RESTful** | 用 URL + HTTP 方法（GET/POST）表达资源 | 你的 `/chat` `/agent` 接口设计 |
| **状态码** | 200 成功 / 401 未授权 / 422 参数错 / 500 服务器错 | 异常处理返回对应码 |
| **中间件 / CORS** | 请求前后统一处理（日志、跨域） | 前端调用你的服务要开 CORS |
| **数据库** | 存结构化数据（MySQL/PostgreSQL） | 存会话/用户/评测结果 |
| **缓存 Redis** | 热点数据放内存加速 | 缓存 LLM 回答降成本/延时 |
| **消息队列 Kafka** | 异步解耦、削峰 | 批量任务（如批量设计电站图）排队 |
| **WebSocket / SSE** | 服务端主动推（流式） | LLM token 流式输出 |

> 这些不用现在深究，面试被问到能说出"是什么、干嘛用"即可（详见 `01` 的 C/D 节名词清单）。

## 5. 自测
1. 用 FastAPI 写个 `GET /hello` 返回 `{"msg": "hi"}`。
2. 给 `/agent` 加一个 Pydantic 响应模型并打印 `latency_ms`。
3. 解释为什么 Agent 服务用 `async` 而不是同步函数。
4. 说清"后端"和"Web 框架"的关系，以及 FastAPI 比 Flask 好在哪。

## 6. 下一步
→ 看 `05-AI-Agent架构与Harness实战.md`，把"Agent 内部怎么跑"和最新的 deepseekharness / codexharness 讲透——这是你面试的核心差异化。
