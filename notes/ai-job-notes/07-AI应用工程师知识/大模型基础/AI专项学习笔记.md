# AI专项学习笔记

## 学习目标

能够用语言表述：
> 熟练使用Python完成文本清洗、数据处理、大模型API对接，了解RAG/Agent落地逻辑

---

## 一、API调用基础 (requests库)

### 核心知识点

- HTTP请求方法（GET/POST）
- 请求头、请求体
- 响应状态码
- JSON数据解析

### 常用代码模板

```python
import requests

# GET 请求
response = requests.get(
    "https://api.example.com/data",
    params={"key": "value"}
)

# POST 请求
response = requests.post(
    "https://api.example.com/generate",
    json={"prompt": "你好", "max_tokens": 100}
)

# 处理响应
result = response.json()
print(result["choices"][0]["text"])
```

---

## 二、JSON数据处理

### 核心知识点

- JSON字符串 ↔ Python对象转换
- 嵌套数据结构处理
- 数据提取与封装

### 常用代码模板

```python
import json

# JSON字符串 → Python对象
json_str = '{"name": "张三", "age": 20}'
data = json.loads(json_str)

# Python对象 → JSON字符串
json_output = json.dumps(data, ensure_ascii=False, indent=2)

# 从文件读取JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 写入JSON文件
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## 三、LLM调用流程

### 基本概念

1. **Prompt工程**：如何写好给模型的指令
2. **Temperature**：控制随机性（0=确定，1=随机）
3. **Max Tokens**：限制输出长度
4. **流式输出**：实时显示生成结果

### 典型调用流程

```
用户输入 → Prompt构建 → API调用 → 响应解析 → 结果输出
```

---

## 四、RAG简易原理

### 什么是RAG

**R**etrieval **A**ugmented **G**eneration（检索增强生成）

### 工作流程

```
文档 → 分块 → 向量化 → 存入向量数据库
                              ↓
用户问题 → 向量化 → 相似度检索 → 上下文注入 → LLM生成 → 回答
```

### 核心组件

| 组件 | 作用 |
| ---- | ---- |
| 文档加载器 | 读取PDF/Word/TXT等 |
| 文本分块 | 将长文档切成小块 |
| Embedding模型 | 将文本转为向量 |
| 向量数据库 | 存储和检索向量 |
| LLM | 根据上下文生成回答 |

---

## 五、Agent基础链路

### 什么是Agent

Agent = LLM + 工具调用 + 记忆 + 规划

### 简单Agent架构

```
┌─────────────────────────────────────┐
│            用户输入                  │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         理解用户意图                  │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         规划行动步骤                  │
│  ┌─────────────────────────────────┐│
│  │ Tool 1: 搜索                     ││
│  │ Tool 2: 计算                     ││
│  │ Tool 3: 调用API                  ││
│  └─────────────────────────────────┘│
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         执行并获取结果                │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         组织回答返回用户              │
└─────────────────────────────────────┘
```

### 常用框架

- LangChain
- LlamaIndex
- AutoGen
- CrewAI

---

## 学习资源

- B站：Python调用大模型API入门
- [LangChain官方文档](https://docs.langchain.com/)
- [阿里云百炼API](https://bailian.console.aliyun.com/)
- [智谱AI开放平台](https://open.bigmodel.cn/)

---

## 实践项目建议

1. **项目一**：用Python调用LLM API实现一个对话机器人
2. **项目二**：实现一个简单的RAG问答系统
3. **项目三**：构建一个能调用搜索工具的Agent
