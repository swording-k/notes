# LangChain

> AI 应用开发的"工具箱"，让 AI 开发像搭积木一样简单

---

## 一、什么是 LangChain？

### 一句话解释
```
LangChain = AI 应用开发的工具箱（不是模板，是现成的代码组件）
类似 Flask 是 Web 开发工具箱
```

### 和"手写代码"对比

| 维度 | 手写代码 | 用 LangChain |
|------|---------|-------------|
| 调用 LLM | 写一堆 HTTP 请求 | 一行代码 |
| 管理 Prompt | 字符串拼接 | PromptTemplate |
| 工具调用 | 自己写逻辑 | 简单配置 |
| 记忆管理 | 自己存历史 | 自动处理 |
| 代码量 | 几百行 | 几十行 |

---

## 二、为什么需要 LangChain？

### 问题1：每次调 LLM 要写很多代码

```python
# ❌ 不用框架：写一堆重复代码
headers = {"Authorization": f"Bearer {api_key}"}
data = {"model": "gpt-4", "messages": [...]}
response = requests.post(url, headers=headers, json=data)

# ✅ 用 LangChain：简洁
llm = ChatOpenAI(model="gpt-4")
result = llm.invoke("你好")
```

### 问题2：LLM 不知道怎么调用工具

```python
# ❌ 不用框架：自己处理工具调用逻辑（很复杂）

# ✅ 用 LangChain：简单配置
tools = [search_tool, calculator_tool]
agent = create_agent(llm, tools)
agent.run("查天气再计算10%税")
# LLM 自动决定用哪个工具
```

### 问题3：LLM 不记得之前说过的话

```python
# ❌ 不用框架：自己存历史、自己拼接 Prompt

# ✅ 用 LangChain：自动管理记忆
memory = ConversationBufferMemory()
memory.save_context({"input": "我叫张三"}, {"output": "你好张三"})
# 后续对话自动包含历史
```

---

## 三、LangChain 核心概念

### 五大核心概念

| 概念 | 通俗理解 | 生活中的例子 |
|------|---------|-------------|
| **PromptTemplate** | 提示词模板 | 填表格的模板 |
| **Chain** | 流水线 | 工厂流水线 |
| **Tool** | 工具 | 瑞士军刀 |
| **Agent** | 智能体 | 机器人 |
| **Memory** | 记忆 | 聊天记录 |

---

### 1. PromptTemplate（提示词模板）

```python
from langchain.prompts import PromptTemplate

# 定义模板
template = """你是{role}，请用{style}风格回答问题。
问题：{question}
答案："""

prompt = PromptTemplate(
    template=template,
    input_variables=["role", "style", "question"]
)

# 使用模板
result = prompt.format(
    role="老师",
    style="幽默",
    question="为什么学习"
)
```

---

### 2. Chain（流水线）

```python
from langchain.chains import LLMChain

# 把 Prompt + LLM 串成流水线
chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=prompt
)

# 一行调用
result = chain.run(question="什么是 RAG")
```

---

### 3. Tool（工具）

```python
from langchain.agents import load_tools

# 加载预制工具
tools = load_tools(["serpapi", "llm-math"])

# 工具让 Agent 能调用外部世界
```

---

### 4. Agent（智能体）

```python
from langchain.agents import initialize_agent

# 创建 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react"
)

# Agent 自动决定用哪个工具
result = agent.run("查北京天气，然后计算适合穿什么")
```

---

### 5. Memory（记忆）

```python
from langchain.memory import ConversationBufferMemory

# 短期记忆
memory = ConversationBufferMemory()

# 保存对话
memory.save_context(
    {"input": "我叫张三"},
    {"output": "你好张三"}
)

# 自动管理历史
```

---

## 四、LangChain vs LlamaIndex

| 维度 | LangChain | LlamaIndex |
|------|-----------|------------|
| 定位 | 全流程框架 | 专注数据接入 |
| 优势 | 功能全、灵活性高 | RAG 做得更专业 |
| 劣势 | 上手复杂 | 通用性稍差 |
| 选择 | 复杂 Agent 系统 | 主要是 RAG 应用 |

**可以结合使用**：LlamaIndex 处理数据，LangChain 做 Agent 编排

---

## 五、LangChain 应用场景

### 场景1：RAG 问答

```python
from langchain.chains import RetrievalQA

# RAG 流水线
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

result = qa_chain.run("什么是 RAG")
```

### 场景2：智能客服

```python
# Agent + 工具 + 记忆
agent = initialize_agent(
    tools=[...],
    llm=llm,
    memory=memory
)

# 自动处理用户问题
while True:
    user_input = input()
    response = agent.run(user_input)
    print(response)
```

### 场景3：数据分析

```python
# 工具链
chain = LLMChain(
    llm=llm,
    prompt=analysis_prompt
)

# 分析数据
result = chain.run(data=csv_content)
```

---

## 六、面试回答模板

### Q: 什么是 LangChain？

```
LangChain 是一个 AI 应用开发框架，类似于 Web 开发里的 Flask。

核心价值是把 AI 应用开发的常见操作封装成现成的模块：
- PromptTemplate 管理提示词
- Chain 把多个步骤串成流水线
- Tool 让 AI 能调用外部 API
- Memory 自动管理对话历史
- Agent 实现智能决策和执行

我理解它的核心思想是"搭积木"——不用从零写代码，
直接调用现成模块组装成完整的 AI 应用。
```

### Q: LangChain 和手写代码有什么区别？

```
手写代码每次调用 LLM 要写很多 HTTP 请求、错误处理、Prompt 拼接。
用 LangChain 可以：
- 调用 LLM：一行代码
- 管理记忆：自动保存
- 工具调用：配置即可
- 代码量：从几百行减少到几十行

就像 Web 开发不用 socket 自己写，用 Flask 框架一样。
```

---

## 七、相关概念

| 概念 | 关系 | 说明 |
|------|------|------|
| [[Agent]] | 用 LangChain 构建 | Agent 是 LangChain 的核心 |
| [[RAG]] | 用 LangChain 实现 | RAG 是常见应用场景 |
| [[工具调用]] | LangChain 的能力 | Tool 是 LangChain 的组件 |

---

*相关笔记：[[../AI应用工程师面试速览]]（面试速查）、[[Agent]]（LangChain 主要应用）*