# Vibe-Research 投研知识图谱（Obsidian Vault）

> 阶段 0 · 纯结构骨架。本 vault 是 Vibe-Research 项目的语义层，把代码里的实体（Pydantic 契约）、spec 决策、战法、数据源链接成可导航的知识图谱。

## 这是什么

Vibe-Research 是 A 股投研系统，已有 12+ Pydantic 契约模型（Quote/Valuation/Financials/Report/KLine/FundFlow/News/Seat/GlobalStock/Emotion/Sector/IndustrySector/LianbanStock/ZTPoolItem）和 12 张战法卡（`backend/strategies/cards/`）。代码层管"数据怎么流"，本 vault 管"知识怎么连"——个股属于哪个行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来，都在这里通过 `[[]]` 双链和 Dataview 查询织成网。

## 如何打开

1. 安装 [Obsidian](https://obsidian.md/)（桌面端免费）。
2. Open vault as folder → 选本目录 `knowledge/`。
3. Obsidian 会在根生成 `.obsidian/` 配置目录（已通过 `.gitignore` 忽略个人状态）。

## 推荐插件清单

| 插件 | 用途 | 是否必需 |
|---|---|---|
| **Dataview** | 动态查询（所有 `index.md` 的表格/列表由它渲染） | ✅ 必需 |
| **Templater** | 新建实体时自动填 frontmatter + 骨架 | ✅ 必需 |
| **Smart Connections** | 语义相似度推荐（找"和这篇笔记像的笔记"） | 推荐 |
| **Copilot for Obsidian** | 本地/外部 LLM 问答，基于当前笔记上下文 | 推荐 |
| **Graph Analysis** | 图算法分析（中心性/社区发现/聚类） | 可选 |

> 阶段 0 不含 LLM 集成。Smart Connections / Copilot 装上但未配置模型时不会报错，只是不工作。

## 目录结构

```
knowledge/
├── MOC.md                  # Map of Content，入口
├── README.md               # 本文件
├── .gitignore              # 忽略 Obsidian 个人状态
├── stocks/                 # 股票（Quote + CompanyInfo）
├── industries/             # 行业板块（IndustrySector）
├── concepts/               # 概念板块（ConceptBlock + Sector）
├── indices/                # 指数（沪深300/中证500等）
├── reports/                # 研报（Report）
├── analysts/               # 分析师（Report.researcher）
├── metrics/                # 财务指标（Financials + FinancialPeriod）
├── valuations/             # 估值（Valuation + ValuationPercentile）
├── dragon-tiger/           # 龙虎榜（Seat + BillboardDetail + DragonTiger）
├── events/                 # 事件（News + Announcement + ZTPoolItem）
├── strategies/             # 战法（12 张卡，已导入）
├── specs/                  # 项目决策（SDD spec 实体）
├── data-sources/           # 数据源（15+ 外部源）
├── templates/              # Templater 模板（13 个）
│   ├── stock.md
│   ├── industry.md
│   ├── concept.md
│   ├── index.md
│   ├── report.md
│   ├── analyst.md
│   ├── metric.md
│   ├── valuation.md
│   ├── dragon-tiger.md
│   ├── event.md
│   ├── strategy.md
│   ├── spec.md
│   └── data-source.md
└── .obsidian/              # Obsidian 配置（gitignore）
```

每个实体文件夹下都有一个 `index.md`，是该实体类的 Dataview 动态列表入口。从 `MOC.md` 开始导航。

## 与 Vibe-Research 项目代码的关系

| 层 | 位置 | 职责 |
|---|---|---|
| 代码契约层 | `backend/models/` | Pydantic 模型定义数据结构 |
| 数据流层 | `backend/` + `ARCHITECTURE.md` | 数据采集/加工/存储管线 |
| 战法执行层 | `backend/strategies/` | 战法 match 逻辑 + cards/ 战法卡 |
| **语义层（本 vault）** | `knowledge/` | 实体关系导航、研报笔记、投研知识沉淀 |
| 决策记录层 | `specs/` | SDD spec 决策文档 |

本 vault 不复制代码逻辑，只做**知识表征**。模板的 frontmatter 字段名对应 Pydantic 模型字段，代码改了模型字段，来这里改对应模板的 frontmatter 即可保持一致。

## 阶段规划

- **阶段 0（当前）**：纯结构骨架。13 个模板 + 11 个 index + MOC + 12 张战法卡导入。不含 LLM。
- 阶段 1（待定）：导入存量 spec 为决策实体、首批龙头股笔记。
- 阶段 2（待定）：接 LLM 做语义相似度/自动聚类/图谱问答。

## 许可

随 Vibe-Research 主项目。
