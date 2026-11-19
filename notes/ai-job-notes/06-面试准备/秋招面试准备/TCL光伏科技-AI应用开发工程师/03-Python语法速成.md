# Python 语法速成（面向已会 Swift / C++ 的你）

> 你是会 SwiftUI / C++ / LLVM 的程序员，**Python 语法半天就能捡起来**。本篇不讲"什么是变量"，只讲**和 Swift/C++ 不一样、且 AI 后端必用**的部分。看完直接进 `04-FastAPI后端速成`。

## 1. 和 Swift / C++ 最不一样的 5 件事

| 差异点 | Swift/C++ | Python | 你要记住的 |
|---|---|---|---|
| **缩进** | 大括号 `{}` | **缩进就是语法**（4 空格） | 缩进错了直接报错，别用 Tab |
| **类型** | 强类型 | 动态类型，但推荐加 type hints | 写 `def f(x: int) -> str:` 既规范又帮 IDE 提示 |
| **变量** | 值/引用分明 | **一切皆对象，变量是引用** | `a = b` 是让 a 指向 b 的对象，不是拷贝 |
| **容器推导** | 循环/map | **列表/字典推导式一行搞定** | `[x*2 for x in lst if x>0]` |
| **可变参数** | 重载 | `*args` / `**kwargs` | 接任意位置/关键字参数 |

## 2. AI 后端必会的 Python 特性（带代码）

### 2.1 函数、默认参数
```python
def greet(name: str, title: str = "同学") -> str:
    return f"你好, {title} {name}"

print(greet("杨锟"))          # 你好, 同学 杨锟
print(greet("杨锟", "工程师")) # 你好, 工程师 杨锟
```

### 2.2 列表 / 字典 / 集合（最常用容器）
```python
lst = [1, 2, 3]                 # 列表（可变，类似 Array）
d = {"a": 1, "b": 2}            # 字典（key-value，类似 Dictionary/Map）
s = {1, 2, 3}                   # 集合（去重，类似 Set）
# 推导式（重点！）
squares = [x*x for x in range(5)]          # [0,1,4,9,16]
filtered = {k: v for k, v in d.items() if v > 1}  # {'b': 2}
```

### 2.3 装饰器 @decorator（FastAPI 路由就是它）
装饰器 = 不改动原函数、给它"加功能"的语法糖。FastAPI 用 `@app.get("/path")` 把函数和路由绑定。
```python
def log_time(func):
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result
    return wrapper

@log_time
def add(a, b):
    return a + b
```

### 2.4 上下文管理器 with（文件/连接自动关闭）
```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()   # 退出 with 自动 close，不怕忘关
```

### 2.5 生成器 yield（流式输出常用）
`yield` 每次返回一个值、保留函数状态——**大模型流式输出（token 一个个吐）就靠它**。
```python
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

for x in count_up(3):
    print(x)   # 0 1 2
```

### 2.6 异步 async / await（⭐ LLM API 调用必用）
AI 服务要等 LLM 返回（网络 IO 慢），用异步才能高并发。**面试必问"为什么 LLM 调用常用异步"**——答案：等模型返回时不阻塞线程，能同时处理更多请求。
```python
import asyncio

async def call_llm(prompt: str) -> str:
    # 伪代码：实际用 openai/anthropic SDK 的 async 方法
    await asyncio.sleep(1)   # 模拟等待模型返回
    return f"回答: {prompt}"

async def main():
    # 并发跑 3 个，总耗时约 1 秒而非 3 秒
    results = await asyncio.gather(
        call_llm("A"), call_llm("B"), call_llm("C")
    )
    print(results)

asyncio.run(main())
```

### 2.7 类型提示 + dataclass + pydantic（FastAPI 核心）
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    age: Optional[int] = None   # Optional = 可空

u = User("杨锟", 22)
```
`pydantic` 是 FastAPI 用来**校验请求参数、自动生成文档**的库（见 `04`）。

## 3. 30 分钟自测（写得出就过关）
1. 用列表推导式生成 1~10 的偶数平方。
2. 写一个 `with` 读文件的函数。
3. 写一个 `async` 函数，用 `asyncio.gather` 并发调 2 个异步任务。
4. 解释 `*args` / `**kwargs` 分别接什么。
5. 写一个简单的 `@decorator` 打印函数名再执行。

> 答案自己搜/问我都行；核心是**动手写一遍**，别只看。

## 4. 下一步
→ 直接看 `04-FastAPI后端速成.md`，把上面语法落到一个真实"智能体服务"里。
