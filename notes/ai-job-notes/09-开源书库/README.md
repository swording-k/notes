# 开源书库

> 导入日期：2026-11-20
> 用途：大模型、Agent、Python 三本系统教材的本地阅读与练习副本
> 来源：Datawhale 开源社区（https://github.com/datawhalechina）

---

## 为什么放在仓库里

这三本书对应现在的学习主线：

- **大模型基础**：从 NLP、Transformer 讲到预训练、微调、RLHF
- **Agent**：从智能体概念、经典范式讲到框架、记忆、上下文工程和综合项目
- **Python**：面向 AI 的 Python 专项教程，补语法和工程基础

放在仓库里是为了和笔记、面试材料放在同一个知识网络里，读到哪里就在旁边记到哪里，不再散落在桌面。

---

## 三本书

| 书 | 定位 | 入口 | 体积 |
|----|------|------|------|
| **Hello-Agents** | 《从零开始构建智能体》，16 章 + 练习代码 | [[09-开源书库/hello-agents/docs/README]] | 79M |
| **Happy-LLM** | 大模型原理与实践，8 章 + 扩展章 | [[09-开源书库/happy-llm/docs/README]] | 30M |
| **聪明办法学 Python 第二版** | 面向 AI 的 Python 教程（Chap0–6 已完成） | [[09-开源书库/learn-python-the-smart-way-v2/docs/index]] | 26M |

### 建议顺序

```
当前阶段（gap / 美团提前实习前）
  1. Happy-LLM          → 补大模型底层：Transformer、预训练、微调、RLHF
  2. Hello-Agents       → 主攻 Agent：范式、框架、记忆、上下文、通信协议
  3. 聪明办法学 Python   → 当工具书，遇到语法或工程问题再查

对应仓库笔记
  Happy-LLM      ↔ [[07-AI应用工程师知识/大模型基础/transformer]]
  Hello-Agents   ↔ [[07-AI应用工程师知识/概念笔记/Agent]]
  Python         ↔ [[04-代码练习/Python基础/Python刷题语法速查]]
```

---

## 目录说明

```
09-开源书库/
├── happy-llm/
│   ├── docs/                 # 正文 8 章（Markdown + 图片）
│   ├── Extra-Chapter/        # 扩展章节
│   └── notes/                # 原仓库笔记
│
├── hello-agents/
│   ├── docs/                 # 正文 16 章（中英双语）
│   ├── code/                 # 配套练习代码
│   └── Additional-Chapter/   # 附加章节
│
└── learn-python-the-smart-way-v2/
    ├── docs/                 # 课程正文
    ├── textbook/             # 教材 notebook
    ├── homework/             # 作业
    └── resources/            # 课件与素材
```

> **阅读版说明**：为了控制仓库体积，导入时排除了三本书的 `.git` 历史，以及 Hello-Agents 的 `Extra-Chapter/`（77M 图片）和 `Co-creation-projects/`（35M 共创项目）。需要时从桌面 `GitHub书库/` 原仓库取用。

---

## 使用约定

1. **书里的相对链接保持原样**，不要批量改成 `[[wikilink]]`；只有我们自己写的笔记用 Obsidian 双链。
2. **读书笔记写到 `07-AI应用工程师知识/`**，不要直接改书稿；需要批注时在对应笔记里引用章节。
3. **更新书籍**：从桌面 `~/Desktop/GitHub书库/` 重新 rsync 对应目录，不要手工改书稿。
4. 三本书均为 **CC BY-NC-SA 4.0**，仅用于个人学习，保留原作者署名与协议，不用于商业用途。

---

## 授权与署名

| 书 | 作者 / 组织 | 协议 | 原仓库 |
|----|------------|------|--------|
| Hello-Agents | Datawhale | CC BY-NC-SA 4.0 | https://github.com/datawhalechina/Hello-Agents |
| Happy-LLM | Datawhale | CC BY-NC-SA 4.0 | https://github.com/datawhalechina/happy-llm |
| 聪明办法学 Python 第二版 | Datawhale | CC BY-NC-SA 4.0 | https://github.com/datawhalechina/learn-python-the-smart-way-v2 |

各书目录下的 `LICENSE` / `LICENSE.txt` 为原始协议全文。
