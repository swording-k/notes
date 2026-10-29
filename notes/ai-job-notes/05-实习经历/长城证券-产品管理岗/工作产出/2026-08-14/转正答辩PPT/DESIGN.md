# DESIGN.md · 实习转正答辩 PPT

## 1. 画布与全局母版（A/B/C 三区）

- 画布：1280 × 720，padding 上下 20px、左右 72px。
- **A 标题块** 0–120px：主标题 34px bold，左对齐，色 #1E3A8A。
- **B 内容区** 120–660px：正文/图/卡片。
- **C 页脚条** 660–720px：左"飞书项目管理智能体 · 转正答辩"，右页码 `NN / 17`，14px 灰字 #94A3B8。
- 封面/章节扉页/结束页用自定义版式，省略 C 区或弱化处理。

## 2. 颜色系统（≤ 4 hex）

| 角色 | hex | 用途 | 面积 |
|---|---|---|---|
| 主色 | `#2563EB` | 标题、主色块、章节序号 | ≤ 60% |
| 辅色 | `#0EA5E9` | 卡片底、分隔、图表第二色 | ≤ 30% |
| 强调色 | `#F97316` | 关键数字、状态点、焦点 | ≤ 10%（Hero 可 15–20%） |
| 文本 | `#1E293B` / `#475569` | 正文、次级文本 | 剩余 |
| 背景 | `#FFFFFF` | 页面底 | — |

- 渐变：`linear-gradient(135deg, #2563EB 0%, #0EA5E9 100%)` 用于封面/章节序号块/标题栏。
- 半透明：`rgba(37,99,235,0.08)` 卡片浅底。
- 色彩节奏：Hero 页（01/08/10/17）强调色 15–20%；Supporting 页强调色 ≤ 5%。

## 3. 字体系统

- 标题：`'PingFang SC','Microsoft YaHei',sans-serif`，bold，字距略收紧。
- 正文：同字体族，regular，行高 1.6。
- 巨型数字：`'PingFang SC',sans-serif`，bold 72–110px，强调色或主色。
- 字体个性：商务现代（科技蓝），标题与正文同族不同字重。

## 4. 信息密度

- 内容页留白 ≤ 35%；卡片填充率 ≥ 85%，尾部元素 `marginTop:auto` 钉底。
- 焦点元素周围留白 ≥ 40px。

## 5. 配图清单（P0 材料图，已复制到 assets/）

| 文件 | 来源 | 真实内容 | 用途页 |
|---|---|---|---|
| cap_requirement.png | 验证截图 verify-01 | 群聊识别需求、忽略闲聊 | 08 |
| cap_decision.png | 验证截图 verify-03 | 识别决策/开项目/分配工时 | 08 |
| cap_selfheal.png | 验证截图 verify-04 | 报错后提醒自优化 | 08 |
| er_model.png | 领域模型 ER 图 | 项目-需求-任务 M:N 关系图 | 10 |
| flow_overview.svg | 自绘 SVG | 建项目→需求→任务→…→播报链路 | 06 |
| db_schema.svg | 自绘 SVG | 10 张子表结构 | 07 |
| pain_chaos.svg | 自绘 SVG | 散乱聊天气泡 | 04 |

> SVG 均为结构化低语义元素（流程图/架构/关系网络），符合 P2 允许范围。

## 6. 页面映射表（契约）

| # | 文件 | 类型 | 角色 | 版式 | L1 | 字数 | 留白 | 色彩分配 |
|---|---|---|---|---|---|---|---|---|
| 01 | 01_cover | cover | hero | 全屏视觉+骑线 | 渐变背景 | 40 | 35% | 主60%+辅30% |
| 02 | 02_catalog | catalog | supporting | 左标题+右内容 | — | 120 | 25% | 主40%+辅25% |
| 03 | 03_section1 | section | transition | 章节大字 | 序号块 | 40 | 40% | 主50% |
| 04 | 04_pain | content | supporting | 非对称双栏 | pain_chaos | 220 | 28% | 主45%+辅20% |
| 05 | 05_section2 | section | transition | 章节大字 | 序号块 | 40 | 40% | 主50% |
| 06 | 06_overview | content | supporting | 上大图+下方卡片 | flow_overview | 180 | 25% | 主40%+辅25% |
| 07 | 07_database | content | supporting | 左大图+右文字 | db_schema | 220 | 28% | 主45%+辅20% |
| 08 | 08_capability | content | hero | 非对称双栏 | 3截图 | 160 | 25% | 强调18%爆发 |
| 09 | 09_section3 | section | transition | 章节大字 | 序号块 | 40 | 40% | 主50% |
| 10 | 10_rn_mn | content | hero | 左大图+右文字 | er_model | 200 | 28% | 强调15% |
| 11 | 11_method | content | supporting | 左标题+右内容 | — | 230 | 25% | 主40%+辅20% |
| 12 | 12_section4 | section | transition | 章节大字 | 序号块 | 40 | 40% | 主50% |
| 13 | 13_progress | content | supporting | 非对称双栏 | — | 200 | 28% | 主45%+辅20% |
| 14 | 14_verify | content | supporting | 巨型数字+洞察 | 大数字 | 120 | 35% | 强调15% |
| 15 | 15_section5 | section | transition | 章节大字 | 序号块 | 40 | 40% | 主50% |
| 16 | 16_growth | content | supporting | 非对称双栏 | — | 240 | 25% | 主40%+辅20% |
| 17 | 17_ending | ending | hero | 居中金句 | 收束大字 | 30 | 40% | 主55% |
