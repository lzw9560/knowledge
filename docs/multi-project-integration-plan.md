# 多项目投研知识图谱整合架构设计

> **状态**：设计草案（待评审）
> **生成时间**：2026-09-06
> **作用域**：把 `/Users/lizhiwei/project/code/stock/` 下多个投研项目纳入 `10_Reference/investing/` 知识图谱
> **决策风格**：对齐 `specs/decision-log.md`——关键决策给「选择 / 理由 / 被否决方案」三段式
> **数据来源**：基于 2026-09-06 对 4 个项目的实际探查（README / AGENTS.md / docs / 源码目录）。未探查到的标「待探查」，不臆造。

---

## 目录

- [0. 背景与现状](#0-背景与现状)
  - [0.1 当前图谱结构](#01-当前图谱结构)
  - [0.2 待纳入项目探查结果](#02-待纳入项目探查结果)
  - [0.3 探查中发现的三个关键事实](#03-探查中发现的三个关键事实)
- [1. 结构方案：图谱怎么容纳多项目](#1-结构方案图谱怎么容纳多项目)
  - [1.1 方案对比](#11-方案对比)
  - [1.2 推荐方案 D（决策）](#12-推荐方案-d决策)
  - [1.3 目标目录结构](#13-目标目录结构)
- [2. 跨项目实体处理策略](#2-跨项目实体处理策略)
  - [2.1 实体分治总表](#21-实体分治总表)
  - [2.2 数据源去重策略（决策）](#22-数据源去重策略决策)
  - [2.3 战法 vs Analyst 角色：命名冲突处理（决策）](#23-战法-vs-analyst-角色命名冲突处理决策)
  - [2.4 跨项目对比关系](#24-跨项目对比关系)
- [3. frontmatter schema 扩展](#3-frontmatter-schema-扩展)
  - [3.1 双字段设计（决策）](#31-双字段设计决策)
  - [3.2 各类实体 schema 示例](#32-各类实体-schema-示例)
  - [3.3 存量实体迁移](#33-存量实体迁移)
- [4. MOC 更新方案](#4-moc-更新方案)
  - [4.1 双轴导航（决策）](#41-双轴导航决策)
  - [4.2 MOC 新增内容](#42-moc-新增内容)
- [5. 跨项目对比视图（Dataview）](#5-跨项目对比视图dataview)
- [6. 纳入优先级与步骤](#6-纳入优先级与步骤)
  - [6.1 优先级排序（决策）](#61-优先级排序决策)
  - [6.2 单项目纳入步骤（通用流程）](#62-单项目纳入步骤通用流程)
  - [6.3 各项目纳入清单](#63-各项目纳入清单)
- [7. 风险与未决项](#7-风险与未决项)
- [附录 A：探查原始记录](#附录-a探查原始记录)

---

## 0. 背景与现状

### 0.1 当前图谱结构

vault 路径：`/Users/lizhiwei/Documents/Obsidian Vault/`，投研子区在 `10_Reference/investing/`。

当前为 **单项目（Vibe-Research）服务**，13 类实体文件夹 + 四构件（logic/actions/inbox/reviews）+ templates：

| 文件夹 | 内容 | 数量 | 归属 |
|---|---|---|---|
| `stocks/` | 个股实体 | 11 | 全局共享 |
| `industries/` | 行业实体 | 7 | 全局共享 |
| `concepts/` | 概念实体 | 6 | 全局共享 |
| `indices/` | 指数实体 | 待探查 | 全局共享 |
| `reports/` | 研报实体 | 待探查 | 全局共享 |
| `analysts/` | **券商研报作者**（真人） | 仅 index | 全局共享 |
| `metrics/` `valuations/` `dragon-tiger/` `events/` | 财务/估值/龙虎榜/事件 | 待探查 | 全局共享 |
| `strategies/` | 战法卡 | 12 | Vibe-Research 专属 |
| `specs/` | SDD spec + DEC | 13 spec + 5 DEC | Vibe-Research 专属 |
| `data-sources/` | 外部数据源 | 16 | Vibe-Research 专属（但实际多源跨项目共享） |
| `logic/` `actions/` `inbox/` `reviews/` | 四构件 + 质量门 | — | 图谱级 |
| `templates/` | Templater 模板 | 19 | 图谱级 |

**关键现状**：所有实体 frontmatter **没有 `project:` 字段**（已 grep 确认），MOC.md 标题即「Vibe-Research 投研知识图谱」，整个子区是单项目语义。

### 0.2 待纳入项目探查结果

| 项目 | 路径 | 定位 | 许可证 | 数据源 | 特色实体 | 纳入判断 |
|---|---|---|---|---|---|---|
| **Vibe-Research** | `.../Vibe-Research` | 个人 AI 投研看板（A股/美股/港股），FastAPI+React | 私有 | 腾讯/东财(4 端点)/akshare/mootdx/新浪/巨潮/百度/同花顺/FRED/baostock/worldmonitor/rss | 12 战法 + 60+ SDD spec | ✅ 已纳入 |
| **Vibe-Research-bakup** | `.../Vibe-Research-bakup` | Vibe-Research 备份 | — | 同上 | — | ❌ 备份不纳入 |
| **trading-agents** | `.../trading-agents` | TradingAgents A 股深度特化 fork（基于 TauricResearch 65K⭐），多 Agent 辩论 | Apache 2.0（开源） | mootdx/腾讯/东财/新浪/同花顺/财联社/百度 | **7 个 AI Analyst 角色**（市场/舆情/新闻/基本面/政策/游资/解禁）+ Bull/Bear 辩论 + 三方风险辩论 | ⭐ 先纳入 |
| **daily-stock-analysis** | `.../daily-stock-analysis/daily_stock_analysis` | ZhuLinsen/daily_stock_analysis，多市场自选股智能分析（A股/港股/美股/日股/韩股/台股），GitHub Actions/Docker 推送 | MIT（开源） | AkShare/Tushare/Pytdx/Baostock/YFinance/Longbridge/TickFlow + 新闻搜索(Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG) | **18+ yaml 战法**（strategies/*.yaml）+ Agent 策略问股（15 种内置策略） | ⭐ 次纳入（已被 Vibe-Research 引用） |
| **a-Plate-Sentinel** | `.../a-Plate-Sentinel` | A股打板情绪监控与投研决策看板，Docker，FastAPI+React+TimescaleDB | 私有 | Tushare | 8 大功能模块（情绪看板/打板选股/个股深度/每日复盘/持仓/回测/风控/设置）+ STI 情绪温度指数 + 龙虎榜席位标签引擎 | ⏸ 延后（MVP 骨架阶段，模块未实现） |

### 0.3 探查中发现的三个关键事实

这三个事实直接推翻/修正了任务描述里的部分假设，是后续决策的依据：

**事实 1：daily-stock-analysis 不是「待查」，且已与 Vibe-Research 交叉引用。**
它是成熟开源项目（ZhuLinsen/daily_stock_analysis，MIT，Trendshift #1 Python Repo），有 18+ 个 yaml 战法。Vibe-Research 的 `strategies/龙头战法.md` 第 38 行已明确引用 `ZhuLinsen/daily_stock_analysis strategies/dragon_head.yaml` 作为参数来源。**这意味着战法体系已经存在跨项目交叉引用，不是「未来可能」，是「已经发生」。**

**事实 2：`analysts/` 文件夹语义冲突。**
现有 `analysts/` 模板（`type: analyst`，字段 `name/org/coverage_count`）对应 Pydantic 契约 `Report.researcher`，是**真人券商研报作者**。trading-agents 的 7 个 Analyst 是 **AI agent 角色**（market_analyst.py / policy_analyst.py 等代码模块）。两者语义完全不同，不能复用同一文件夹——否则 Dataview `FROM "analysts" WHERE type = "analyst"` 会把真人和 AI 角色混在一张表里。

**事实 3：a-Plate-Sentinel 处于 MVP 骨架阶段。**
其 README 自述「当前进度：数据模型+计算服务骨架已生成，待补全算法细节与API/前端」，AGENTS.md 明确「龙虎榜席位引擎、回测系统、AI复盘Agent、动态止盈止损自动化 → Phase 2，不要在MVP阶段提前实现」。**现在纳入会产生大量「待补」占位实体，违背 inbox 质量门「不直接灌入是知识图谱健康的第一道防线」原则。**

---

## 1. 结构方案：图谱怎么容纳多项目

### 1.1 方案对比

| 维度 | 方案 A：项目子文件夹 | 方案 B：纯 frontmatter | 方案 C：项目实体+单 project 字段 | 方案 D：项目实体+双字段+平铺（推荐） |
|---|---|---|---|---|
| **共享实体归属** | ❌ 困境：东财放 `specs/vibe-research/` 还是 `specs/trading-agents/`？数据源/股票无法分子文件夹 | ✅ 平铺，frontmatter 标多项目 | ⚠️ 单 `project` 字段无法表达「被 3 个项目引用」 | ✅ `projects:` 列表标引用，`origin_project:` 标溯源 |
| **项目级元信息** | ❌ 无项目节点，仓库/许可证/技术栈无处放 | ❌ 同左 | ✅ `projects/x.md` 承载 | ✅ 同 C |
| **导航锚点** | ⚠️ 靠文件夹，但共享实体无锚点 | ❌ 无节点可链 | ✅ 项目实体是 `` 锚点 | ✅ 同 C |
| **Dataview 按项目筛** | ⚠️ `FROM "specs/vibe-research"` 可以，但共享实体筛不到 | ✅ `WHERE project = "x"` | ✅ `WHERE project = "x"` | ✅ 专属 `WHERE project = "x"` / 共享 `WHERE contains(projects, "x")` |
| **Dataview 跨项目查** | ❌ 子文件夹割裂，跨项目查要 union 多路径 | ✅ 平铺天然跨项目 | ✅ 平铺 | ✅ 平铺 |
| **新项目扩展性** | ❌ 每加项目建 N 个子文件夹，共享实体要决定归属 | ✅ 加 frontmatter 值即可 | ✅ 加项目实体 + frontmatter 值 | ✅ 同 C |
| **存量迁移成本** | ❌ 高：要移动文件 + 改所有 `` 链接路径 | ⚠️ 中：加字段 | ⚠️ 中：加字段 + 建项目实体 | ⚠️ 中：加字段 + 建项目实体（不移动文件，链接不变） |
| **命名冲突处理** | ❌ 无机制（analysts/ 冲突无解） | ⚠️ 靠 type 字段区分，但同文件夹仍混 | ⚠️ 同 B | ✅ 新建 `agents/` 文件夹分流（见 §2.3） |

### 1.2 推荐方案 D（决策）

**选择**：方案 D——**项目实体 + 双字段（`project` 单值给专属实体 / `projects` 列表给共享实体）+ 平铺不分子文件夹 + 新增 `agents/` 文件夹解决命名冲突**。

具体形态：
1. 新建 `projects/` 文件夹，放 4 个项目实体（vibe-research / trading-agents / daily-stock-analysis / a-plate-sentinel），承载项目级元信息（仓库路径/许可证/技术栈/状态/市场覆盖/数据源清单）。
2. **不拆子文件夹**——所有实体仍平铺在现有类型文件夹（stocks/ data-sources/ specs/ strategies/）。
3. 专属实体（spec/DEC/战法/agent 角色）frontmatter 加 **`project:` 单值**，标发源项目。
4. 共享实体（股票/行业/概念/指数/数据源）frontmatter 加 **`projects:` 列表**（被哪些项目引用）+ **`origin_project:` 单值**（首次从哪个项目灌入，溯源用）。
5. 新建 `agents/` 文件夹（`type: agent_role`）放 AI agent 角色（trading-agents 的 7 Analyst + 未来 a-Plate-Sentinel 的 AI 复盘 Agent + daily-stock-analysis 的 Agent 策略问股），与 `analysts/`（真人券商研报作者）分流。

**理由**：
- **共享实体是图谱的主体价值所在**。东财数据源被 3 个项目用、贵州茅台被所有项目关注——这些跨项目连接正是知识图谱区别于「每项目一个文档堆」的核心。方案 A 的子文件夹会把这些连接割裂成「每项目一份副本」或「归属争议」，直接摧毁图谱价值。
- **项目实体是必要的锚点**。项目本身有元信息（仓库/许可证/技术栈/状态），这些信息不属于任何单个 spec 或数据源，需要一个一等实体承载。同时它是 `` 双链和 Dataview 反向聚合的目标——在 `projects/vibe-research.md` 里可以 `FROM ... WHERE project = this.name OR contains(projects, this.name)` 一键盘点该项目所有相关实体。
- **双字段解决「发源 vs 引用」语义**。单一 `project` 字段无法回答「东财数据源属于谁」——它发源于 Vibe-Research 的灌入，但被 trading-agents 也引用。`origin_project`（单值，溯源）+ `projects`（列表，引用）分开，Dataview 查询和审计都清晰。
- **平铺不移动文件 = 存量 `` 链接零破坏**。现有 18 spec + 16 数据源 + 12 战法 + 11 股票的所有双链路径不变，只加 frontmatter 字段。方案 A 要移动文件并改所有链接，迁移成本和出错风险都高一个量级。
- **`agents/` 新文件夹是语义正确性要求**。事实 2 已证明 `analysts/` 是真人券商分析师，AI agent 角色塞进去会污染 Dataview 查询。新建 `agents/` 是 YAGNI 的反面——这不是过度设计，是修复一个已存在的语义冲突。

**被否决方案**：

1. **方案 A（项目子文件夹）**：否决理由——共享实体（数据源/股票/行业/概念）无法归属单一项目子文件夹。东财放 `data-sources/vibe-research/` 则 trading-agents 引用时路径别扭且暗示「不属于它」；放 `data-sources/trading-agents/` 则 Vibe-Research 同理。每项目各建一份副本则违反「同一数据源只建一份」的去重原则，且副本间同步是维护噩梦。子文件夹还割裂跨项目 Dataview 查询（要 union 多路径）。**核心矛盾：方案 A 假设实体能按项目分区，但图谱的主体价值恰恰是跨项目共享实体，这个假设与目标冲突。**

2. **方案 B（纯 frontmatter，无项目实体）**：否决理由——项目本身没有节点。仓库路径/许可证/技术栈/状态/市场覆盖这些项目级元信息无处安放（塞进每个 spec 的 frontmatter 会重复 N 次）。没有 `` 锚点意味着无法从「项目」这个维度导航，也无法做项目级 Dataview 聚合（`FROM "projects"` 不存在）。MOC 想加项目导航也没有目标可链。**B 是「有字段无实体」，能筛不能聚。**

3. **方案 C（项目实体 + 单一 `project` 字段）**：部分采纳（项目实体 + 平铺），但单一 `project` 字段否决——它无法表达共享实体的多项目归属。若强行用单值，东财数据源的 `project:` 填谁？填 vibe-research 则 trading-agents 查不到，填 trading-agents 则 Vibe-Research 查不到，填列表则又退化成方案 D 的 `projects:`。**C 的缺陷是「有实体无区分」——不区分专属实体和共享实体，用一把钥匙开两种锁。D 是 C 的精细化：专属实体用单值（简单），共享实体用列表+溯源（准确）。**

### 1.3 目标目录结构

```
10_Reference/investing/
├── MOC.md                  # 双轴导航（实体类型轴 + 项目轴）
├── README.md
├── projects/               # 【新增】项目实体（4 个）
│   ├── index.md
│   ├── vibe-research.md
│   ├── trading-agents.md
│   ├── daily-stock-analysis.md
│   └── a-plate-sentinel.md
├── stocks/                 # 全局共享，frontmatter 加 projects:[...] + origin_project:
├── industries/             # 同上
├── concepts/               # 同上
├── indices/                # 同上
├── reports/                # 同上
├── analysts/               # 真人券商研报作者（保持不变）
├── metrics/ valuations/ dragon-tiger/ events/   # 同上
├── data-sources/           # 共享，frontmatter 加 projects:[...] + origin_project:
├── strategies/             # 专属，frontmatter 加 project: （单值）
├── agents/                 # 【新增】AI agent 角色（type: agent_role）
│   ├── index.md
│   ├── market-analyst.md       # trading-agents
│   ├── social-media-analyst.md # trading-agents
│   ├── news-analyst.md         # trading-agents
│   ├── fundamentals-analyst.md # trading-agents
│   ├── policy-analyst.md       # trading-agents
│   ├── hot-money-tracker.md    # trading-agents
│   └── lockup-watcher.md       # trading-agents
├── specs/                  # 专属，frontmatter 加 project: （单值）
├── logic/ actions/ inbox/ reviews/   # 图谱级（不变）
└── templates/              # 新增 project.md / agent.md 模板，存量模板加字段
```

**不新增 `modules/` 文件夹**：a-Plate-Sentinel 的 8 大功能模块是产品功能分解，不是投研知识实体，且项目处于 MVP 骨架阶段（事实 3）。延后到该项目实现后再评估是否需要独立实体（见 §6.1）。

---

## 2. 跨项目实体处理策略

### 2.1 实体分治总表

| 实体类型 | 文件夹 | 跨项目情况 | `project` 字段形态 | 处理策略 |
|---|---|---|---|---|
| 股票 | `stocks/` | 全局共享 | `projects:` 列表 + `origin_project:` 单值 | 只建一份，所有项目引用同一实体。新项目纳入时不新建股票实体，只在已有股票的 `projects:` 列表追加项目名 |
| 行业/概念 | `industries/` `concepts/` | 全局共享 | 同上 | 同上 |
| 指数 | `indices/` | 全局共享 | 同上 | 同上 |
| 研报/分析师 | `reports/` `analysts/` | 全局共享 | 同上 | 同上。注意 `analysts/` 是真人，与 `agents/` 分流 |
| 财务/估值/龙虎榜/事件 | `metrics/` `valuations/` `dragon-tiger/` `events/` | 全局共享 | 同上 | 同上 |
| **数据源** | `data-sources/` | **部分共享** | `projects:` 列表 + `origin_project:` 单值 | **去重合并**：同一数据源（如东财 push2）只建一份，`projects:` 列出所有引用它的项目。见 §2.2 |
| **战法** | `strategies/` | **多体系** | `project:` 单值（发源） | 各建各的，用 `variant_of` / `same_as` 关系连跨项目同源战法。见 §2.4 |
| **AI agent 角色** | `agents/`【新增】 | 项目专属 | `project:` 单值 | trading-agents 7 Analyst 建 7 个实体。未来 a-Plate-Sentinel AI 复盘 Agent、daily-stock-analysis Agent 策略问股也归此 |
| spec/DEC | `specs/` | 项目专属 | `project:` 单值 | 各项目独立 SDD spec，不共享。编号空间各自独立（Vibe-Research 用 S001-S166 + DEC-001~005；trading-agents 用 TA-S001... 或沿用其 CHANGELOG 编号；daily-stock-analysis 用 DSA-...）。**编号前缀避免冲突** |
| 项目 | `projects/`【新增】 | — | `name:` 单值 | 4 个项目实体，承载项目级元信息 |

### 2.2 数据源去重策略（决策）

**选择**：**同一数据源只建一份实体**，用 `projects:` 列表标注所有引用它的项目，用 `origin_project:` 标注首次灌入的项目。

**理由**：
- 数据源是客观外部实体（东财 push2 接口就是一个 API），不因项目不同而变成两个东西。每项目各建一份会导致：① 限流策略/降级链/endpoint 信息重复维护，改一处忘另一处；② Dataview 查「所有用东财的项目」要跨副本 union；③ 违背知识图谱「同一实体同一节点」原则。
- 探查发现的实际重叠：

| 数据源 | Vibe-Research | trading-agents | daily-stock-analysis | a-Plate-Sentinel | 处理 |
|---|---|---|---|---|---|
| mootdx | ✅ | ✅ | — | — | 合并，`projects: [vibe-research, trading-agents]` |
| 腾讯财经 | ✅（tencent） | ✅ | — | — | 合并 |
| 东财 push2 | ✅ | ✅ | — | — | 合并 |
| 东财 datacenter | ✅ | ✅（龙虎榜/解禁） | — | — | 合并 |
| 新浪财经 | ✅ | ✅ | — | — | 合并 |
| 同花顺 | ✅（hithink-ths） | ✅（EPS 一致预期） | — | — | 合并 |
| 百度股市通 | ✅（baidu-stock） | ✅（概念板块/资金流） | — | — | 合并 |
| akshare | ✅ | — | ✅ | — | 合并，`projects: [vibe-research, daily-stock-analysis]` |
| baostock | ✅ | — | ✅ | — | 合并 |
| Tushare | — | — | ✅ | ✅ | 合并，`projects: [daily-stock-analysis, a-plate-sentinel]` |
| 财联社 cls.cn | — | ✅ | — | — | 新建，`project: trading-agents`（暂单项目，未来共享再转列表） |
| FRED | ✅ | — | — | — | 保持 Vibe-Research 专属 |
| 巨潮 cninfo | ✅ | — | — | — | 保持 Vibe-Research 专属 |
| worldmonitor / rss-newsradar | ✅ | — | — | — | 保持 Vibe-Research 专属 |
| YFinance / Longbridge / TickFlow / Pytdx | — | — | ✅ | — | 新建，daily-stock-analysis 专属 |
| 新闻搜索（Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG） | — | — | ✅ | — | 新建，daily-stock-analysis 专属。可合并为一个 `news-search-aggregators.md` 实体或各建——**待探查 daily-stock-analysis 各搜索源职责差异后定** |

- 去重后数据源实体数：现有 16（Vibe-Research）+ trading-agents 新增 1（财联社）+ daily-stock-analysis 新增约 11（Tushare 已计入共享、YFinance/Longbridge/TickFlow/Pytdx/新闻搜索 7 个）≈ 28 个。具体数以纳入时实际探查为准。

**被否决方案**：
1. **每项目各建一份数据源副本**：否决理由见上（重复维护 + 查询割裂 + 违反图谱原则）。
2. **数据源不分项目，只用 `origin_project` 单值**：否决——无法回答「trading-agents 用了哪些数据源」这个高频查询。`projects:` 列表是必要的。

### 2.3 战法 vs Analyst 角色：命名冲突处理（决策）

**选择**：
- `analysts/` 保持「真人券商研报作者」语义不变（`type: analyst`）。
- 新建 `agents/` 文件夹放「AI agent 角色」（`type: agent_role`），trading-agents 的 7 个 Analyst 归此。
- 战法（`strategies/`）与 agent 角色（`agents/`）是**不同实体类型**，不混放。

**理由**：
- 事实 2 已证明语义冲突：`analysts/` 模板字段 `org/coverage_count` 是券商机构属性，trading-agents 的 market_analyst.py 是代码模块，没有「机构」概念。
- 战法和 agent 角色是不同抽象：战法（dragon_head）是「匹配条件+入场+出场」的交易规则，agent 角色（policy_analyst）是「职责+数据工具+输出报告」的分析单元。一个回答「什么形态买什么」，一个回答「谁来分析什么」。混放会让 `type` 字段失去区分力。
- 新建 `agents/` 的成本低（一个文件夹 + 一个模板 + 7 个实体），收益是语义清晰 + 未来可扩展（a-Plate-Sentinel 的 AI 复盘 Agent、daily-stock-analysis 的 Agent 策略问股都是 agent 角色）。

**被否决方案**：
1. **复用 `analysts/`，靠 `type` 字段区分**：否决——同文件夹下真人和 AI 混放，Dataview `FROM "analysts"` 默认查询会混表，每个查询都要加 `WHERE type = ...` 过滤，易错。文件夹是 Obsidian 的第一导航维度，语义应该在文件夹层就分开。
2. **agent 角色放 `strategies/`，`type: agent_role`**：否决——战法和角色是不同抽象（见上），混放污染 `strategies/` 的语义。

### 2.4 跨项目对比关系

新增关系谓词（补充 MOC.md 现有谓词表）：

| 谓词 | 语义 | 示例 |
|---|---|---|
| `variant_of` | 同源战法的不同项目变体 | Vibe-Research `dragon_head.md` `variant_of` daily-stock-analysis `dragon_head.yaml`（已确认交叉引用） |
| `same_as` | 跨项目完全等价的实体 | 暂无（待纳入时识别） |
| `contrasts_with` | 不同体系但功能可对比 | Vibe-Research 12 战法 `contrasts_with` trading-agents 7 Analyst（一个是交易规则体系，一个是分析角色体系，功能上都是「投研决策的输入」） |
| `complements` | 项目间能力互补 | a-Plate-Sentinel STI 情绪指数 `complements` Vibe-Research market_sentiment 子区 |
| `embeds` | 项目内嵌另一项目副本 | daily-stock-analysis `embeds` trading-agents（其目录下有 TradingAgents-astock 副本，以独立 trading-agents 项目为准，副本不重复纳入） |

**战法对比的具体处理**：
- Vibe-Research 12 战法 vs daily-stock-analysis 18 战法：先做名称匹配（dragon_head 已确认同源），同源的建 `variant_of` 关系，不同的各建各的。daily-stock-analysis 的战法是 yaml 格式，纳入时转为 md 实体，`project: daily-stock-analysis`，`imported_from: strategies/xxx.yaml`。
- trading-agents 7 Analyst 不是战法，建 `agents/` 实体，与战法建 `contrasts_with` 关系（在 MOC 的跨项目对比视图里呈现，不在每个实体 frontmatter 里标——避免关系爆炸）。

---

## 3. frontmatter schema 扩展

### 3.1 双字段设计（决策）

**选择**：
- **专属实体**（spec/DEC/战法/agent 角色）：`project:` **单值**——发源项目。
- **共享实体**（股票/行业/概念/指数/数据源/研报/分析师/财务/估值/龙虎榜/事件）：`projects:` **列表**（被哪些项目引用）+ `origin_project:` **单值**（首次从哪个项目灌入，溯源用）。

**理由**：
- 专属实体只属于一个项目，单值最简单，Dataview `WHERE project = "x"` 直接筛。
- 共享实体被多项目引用，必须用列表，Dataview `WHERE contains(projects, "x")` 筛。
- `origin_project` 解决溯源问题：「这个东财数据源实体最初是从 Vibe-Research 的 ARCHITECTURE.md 灌入的」——审计、去重、质量回溯都需要这个信息。它与 `projects` 正交：`origin_project` 是历史事实（不变），`projects` 是当前状态（随新项目纳入增长）。
- 不用单一 `source_project` 字段同时承担「发源」和「引用」两个语义——那会迫使共享实体的 `source_project` 填列表，而专属实体填单值，同一字段两种类型，Dataview 查询要分支处理，易错。

**被否决方案**：
1. **所有实体统一用 `project:` 单值**：否决——共享实体无法表达多项目归属（见 §1.2 方案 C 否决理由）。
2. **所有实体统一用 `projects:` 列表**：否决——专属实体（如 S017 spec）只属于 Vibe-Research，用列表是过度设计，且 Dataview 查询 `WHERE contains(projects, "x")` 比 `WHERE project = "x"` 慢且语义模糊（「包含」不等于「属于」）。
3. **`source_project` 单字段兼发源与引用**：否决——语义重载，类型不一致（专属单值/共享列表），查询分支。

### 3.2 各类实体 schema 示例

**项目实体（`projects/vibe-research.md`）**：

```yaml
---
type: project
name: vibe-research
display_name: Vibe-Research
repo: /Users/lizhiwei/project/code/stock/Vibe-Research
license: proprietary
stack: [FastAPI, React, Python, TypeScript]
status: active
market: [A股, 美股, 港股]
data_sources: [tencent, eastmoney-push2, eastmoney-datacenter, eastmoney-reportapi, eastmoney-searchapi, akshare, mootdx, sina-financial, cninfo, baidu-stock, hithink-ths, fred, baostock, worldmonitor, rss-newsradar]
entity_counts:
  specs: 18
  strategies: 12
  data_sources: 16
created: 2026-09-06
---
```

**共享实体（`data-sources/eastmoney-push2.md`，存量改造）**：

```yaml
---
type: data_source
name: 东财 push2
layer: 2
endpoint: push2/api.eastmoney.com
rate_limit: em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）
fallback: 熔断器+push2delay降级
compliance: ok
provides: [行情, K线, 分时]
projects: [vibe-research, trading-agents]      # 【新增】被引用项目
origin_project: vibe-research                   # 【新增】首次灌入项目
created: 2026-09-06
---
```

**专属实体（`specs/S017-A股涨跌预测模型栈.md`，存量改造）**：

```yaml
---
type: spec
number: S017
title: A股涨跌预测模型栈（四头解耦）
status: 已实现
project: vibe-research                          # 【新增】发源项目（单值）
created: 2026-09-06
---
```

**专属实体（`strategies/dragon_head.md`，存量改造 + 跨项目关系）**：

```yaml
---
type: strategy
name: 龙头战法
edge_family: 龙头追踪
project: vibe-research                          # 【新增】发源项目
imported_from: backend/strategies/cards/
variant_of: "[[10_Reference/[[projects/active/daily-stock-analysis]]#dragon_head.yaml"  # 【新增】跨项目同源
created: 2026-09-06
---
```

**新增 agent 角色实体（`agents/policy-analyst.md`）**：

```yaml
---
type: agent_role
name: 政策分析师
project: trading-agents                         # 发源项目（单值）
source_file: tradingagents/agents/analysts/policy_analyst.py
tools: [get_news, get_global_news]
responsibility: 监管政策、产业政策、窗口指导
rationale: A股是政策市，政策变化直接影响板块轮动
llm_tier: quick_think                           # quick_think / deep_think
created: 2026-09-06
---
```

**新增模板（`templates/project.md`）**：

```yaml
---
type: project
name: <% tp.file.title %>
display_name: 
repo: 
license: 
stack: []
status: active
market: []
data_sources: []
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 项目定位

# 技术栈

# 数据源清单

```dataview
TABLE name AS "数据源", layer AS "层级", provides AS "提供字段"
FROM "data-sources"
WHERE type = "data_source" AND contains(projects, this.name)
SORT layer ASC, name ASC
```

# 专属实体

```dataview
TABLE type AS "类型", title AS "标题", status AS "状态"
FROM "specs" OR "strategies" OR "agents"
WHERE project = this.name
SORT type ASC
```

# 关联项目

> 互补/内嵌/对比关系。
```

**新增模板（`templates/agent.md`）**：

```yaml
---
type: agent_role
name: 
project: 
source_file: 
tools: []
responsibility: 
llm_tier: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 角色职责

# 数据工具

# 输出

# 关联

- 所属项目：[[projects/]]
- 对比战法：[[strategies/]]（contrasts_with）
```

### 3.3 存量实体迁移

存量改造范围（不移动文件，只加 frontmatter 字段）：

| 文件夹 | 实体数 | 加字段 | 值 |
|---|---|---|---|
| `specs/` | 18 | `project: vibe-research` | 单值 |
| `strategies/` | 12 | `project: vibe-research` | 单值 |
| `data-sources/` | 16 | `projects: [vibe-research]` + `origin_project: vibe-research` | 列表+单值（未来纳入 trading-agents 时，共享源的 `projects:` 追加） |
| `stocks/` | 11 | `projects: [vibe-research]` + `origin_project: vibe-research` | 同上 |
| `industries/` | 7 | 同上 | 同上 |
| `concepts/` | 6 | 同上 | 同上 |
| `indices/` `reports/` `analysts/` `metrics/` `valuations/` `dragon-tiger/` `events/` | 待探查 | 同上 | 同上 |

迁移脚本建议：用 Python 脚本批量改 frontmatter（规则脚本，非 LLM，对齐 data-sources/index.md 第 31 行「规则脚本，非 LLM」的灌入原则）。迁移后跑 `reviews/` 质量门体检确认无字段遗漏。

---

## 4. MOC 更新方案

### 4.1 双轴导航（决策）

**选择**：**双轴导航**——保留现有「实体类型轴」（13 类实体表），新增「项目轴」（projects/ 锚点 + 各项目实体数 Dataview）。

**理由**：
- 单轴「实体类型」（现状）适合回答「所有股票有哪些」「所有数据源有哪些」，但无法回答「trading-agents 这个项目有什么」。
- 单轴「项目」适合回答「某项目有什么」，但无法回答「跨项目的数据源全景」。
- 双轴并存，MOC 顶部放项目轴（4 个项目实体链接 + 各项目实体计数 Dataview），中部保留实体类型轴（13 类表），底部放跨项目对比视图入口（§5 的 Dataview）。两轴通过 `` 双链交叉——项目实体里链类型文件夹，类型 index 里链项目实体。

**被否决方案**：
1. **仅按项目导航（替换实体类型轴）**：否决——摧毁现有 13 类实体的导航能力，跨项目查询无入口。
2. **仅按实体类型导航（现状不动）**：否决——无项目维度，无法回答「某项目有什么」，新项目纳入后 MOC 无锚点。

### 4.2 MOC 新增内容

MOC.md 改造点（在现有内容基础上新增，不删）：

1. **标题改**：「Vibe-Research 投研知识图谱」→「投研知识图谱（多项目）」。
2. **顶部新增「项目轴」章节**（放在「实体类导航」之前）：

```markdown
## 项目导航（本体构件 0：项目）

> 4 个投研项目，每个项目是一等实体，承载仓库/许可证/技术栈/状态/数据源清单。

| 项目 | 定位 | 许可证 | 状态 | 专属实体数 |
|---|---|---|---|---|
| [[10_Reference/[[projects/active/vibe-research]] | 个人 AI 投研看板 | 私有 | 🟢 活跃 | `= length(filter(...))` |
| [[10_Reference/[[projects/active/trading-agents]] | 多 Agent 辩论投研 | Apache 2.0 | 🟢 活跃 | ... |
| [[10_Reference/[[projects/active/daily-stock-analysis]] | 多市场智能分析推送 | MIT | 🟢 活跃 | ... |
| [[10_Reference/[[projects/active/a-plate-sentinel]] | 打板情绪监控看板 | 私有 | 🟡 MVP | ... |

### 各项目实体计数（Dataview 动态）

```dataview
TABLE WITHOUT ID file.link AS "项目", 
  length(filter(file.outlinks, (l) => l.folder = "specs")) AS "spec",
  length(filter(file.outlinks, (l) => l.folder = "strategies")) AS "战法",
  length(filter(file.outlinks, (l) => l.folder = "agents")) AS "agent"
FROM "projects"
WHERE type = "project"
SORT name ASC
```
```

3. **实体类导航表新增两行**：

```markdown
| 项目 | [[projects/]] | 投研项目实体，承载仓库/许可证/技术栈 | ... |
| AI agent 角色 | [[agents/]] | 多 Agent 分析角色（区别于真人分析师） | ... |
```

4. **关系层谓词表补充**：`variant_of` / `same_as` / `contrasts_with` / `complements` / `embeds`（见 §2.4）。

5. **底部新增「跨项目对比视图」章节**，放 §5 的 Dataview 查询。

---

## 5. 跨项目对比视图（Dataview）

以下查询放在 MOC.md 底部「跨项目对比视图」章节，以及各项目实体页内。

**查询 1：各项目数据源对比**（放在 MOC + 各项目实体页）

```dataview
TABLE WITHOUT ID name AS "数据源", layer AS "层级", 
  projects AS "引用项目", origin_project AS "首次灌入", provides AS "提供字段"
FROM "data-sources"
WHERE type = "data_source"
SORT length(projects) DESC, name ASC
```

> 按「引用项目数」降序——共享度最高的数据源（东财/mootdx/腾讯）排最前，一眼看出跨项目依赖热点。

**查询 2：单项目数据源清单**（放在 `projects/x.md` 内，`this.name` 自动取当前项目）

```dataview
TABLE WITHOUT ID name AS "数据源", layer AS "层级", provides AS "提供字段"
FROM "data-sources"
WHERE type = "data_source" AND contains(projects, this.name)
SORT layer ASC, name ASC
```

**查询 3：跨项目共享数据源（被 ≥2 项目引用）**（放在 MOC）

```dataview
TABLE WITHOUT ID name AS "数据源", projects AS "共享项目", layer AS "层级"
FROM "data-sources"
WHERE type = "data_source" AND length(projects) >= 2
SORT length(projects) DESC, name ASC
```

**查询 4：Vibe-Research 战法 vs trading-agents Analyst 角色对比**（放在 MOC）

```dataview
TABLE WITHOUT ID 
  file.link AS "实体", type AS "类型", project AS "项目",
  edge_family AS "edge家族/职责", name AS "名称"
FROM "strategies" OR "agents"
WHERE type = "strategy" OR type = "agent_role"
SORT project ASC, type ASC, name ASC
```

> 战法（交易规则）与 agent 角色（分析单元）并排呈现，体现「投研决策输入」的两种体系。

**查询 5：跨项目同源战法（variant_of 关系）**（放在 MOC + strategies/index.md）

```dataview
TABLE WITHOUT ID 
  file.link AS "战法", project AS "项目", variant_of AS "同源变体"
FROM "strategies"
WHERE type = "strategy" AND variant_of != null
SORT name ASC
```

**查询 6：各项目架构决策时间线**（放在 MOC + 各项目实体页）

```dataview
TABLE WITHOUT ID number AS "编号", title AS "标题", project AS "项目", 
  status AS "状态", created AS "创建日期"
FROM "specs"
WHERE type = "spec" OR type = "decision"
SORT created DESC, project ASC
```

**查询 7：单项目全景**（放在 `projects/x.md` 内，一键盘点该项目所有相关实体）

```dataview
TABLE WITHOUT ID file.link AS "实体", type AS "类型", 
  title AS "标题/名称", status AS "状态"
FROM "specs" OR "strategies" OR "agents" OR "data-sources" OR "stocks"
WHERE (project = this.name) OR (type = "data_source" AND contains(projects, this.name)) 
   OR (type = "stock" AND contains(projects, this.name))
SORT type ASC, file.name ASC
```

**查询 8：未关联任何项目的孤儿实体**（放在 reviews/ 质量门，审计用）

```dataview
TABLE WITHOUT ID file.link AS "实体", type AS "类型"
FROM "specs" OR "strategies" OR "agents" OR "data-sources"
WHERE (type = "spec" OR type = "strategy" OR type = "agent_role") AND project = null
   OR (type = "data_source") AND projects = null
SORT type ASC
```

> 质量门检查项：专属实体必须有 `project`，共享实体必须有 `projects`。孤儿实体触发审查。

---

## 6. 纳入优先级与步骤

### 6.1 优先级排序（决策）

**选择**：**trading-agents → daily-stock-analysis → a-Plate-Sentinel**。

**理由**：
1. **trading-agents 先纳入**：① 开源（Apache 2.0），信息完整（README/CHANGES_FROM_UPSTREAM/docs 齐全），抽取成本低；② 7 个 AI Analyst 角色是**全新实体类型**（`agents/`），纳入它能立刻验证新文件夹+新模板+新 schema 的设计是否成立，是「试金石」；③ 数据源与 Vibe-Research 大量重叠（mootdx/腾讯/东财/新浪/同花顺/百度），能立刻验证 §2.2 去重策略；④ 与 Vibe-Research 互补最强（多 Agent 辩论 vs 单 pipeline 看板）。
2. **daily-stock-analysis 次纳入**：① 已被 Vibe-Research 交叉引用（dragon_head 战法来源），纳入它能立刻建立第一条 `variant_of` 跨项目关系，验证 §2.4 对比关系设计；② 开源（MIT），信息完整；③ 18+ yaml 战法 + 多市场数据源（YFinance/Longbridge/TickFlow），扩充图谱广度。**注意**：其目录下内嵌的 TradingAgents-astock 副本不重复纳入，标 `embeds` 关系指向独立的 trading-agents 项目实体。
3. **a-Plate-Sentinel 延后**：① 处于 MVP 骨架阶段（事实 3），8 大模块未实现，现在纳入会产生大量「待补」占位实体，违背 inbox 质量门原则；② Tushare 数据源与现有图谱不重叠（daily-stock-analysis 也用 Tushare，但两者都未纳入，等 daily-stock-analysis 纳入时建 Tushare 实体，a-Plate-Sentinel 后续追加 `projects:` 即可）；③ STI 情绪指数与 `10_Reference/market_sentiment/` 子区互补，但该子区是独立子区，纳入时机应与 market_sentiment 子区的演进对齐，不宜抢跑。**触发条件**：a-Plate-Sentinel 至少 1 个模块（情绪看板）实现并通过其 AGENTS.md 的「变更闭环验证」后，再纳入。

**被否决方案**：
1. **任务原顺序（trading-agents → a-Plate-Sentinel → daily-stock-analysis）**：否决——a-Plate-Sentinel 处于 MVP 骨架阶段（事实 3），中间纳入它会把「待补」占位实体灌进图谱，污染质量门；而 daily-stock-analysis 已被 Vibe-Research 交叉引用（事实 1），延后它会让已存在的 `variant_of` 关系无法落地。调整为 daily-stock-analysis 提前到第二位。
2. **四项目同时纳入**：否决——schema 改造（双字段）+ 新文件夹（projects/ agents/）+ 存量迁移（54+ 实体加字段）+ 4 项目抽取，同时做风险过高，无法逐步验证设计。应串行纳入，每纳入一个跑一次 reviews/ 质量门。

### 6.2 单项目纳入步骤（通用流程）

每个项目纳入按以下 7 步，**串行执行，每步后跑质量门**：

1. **读项目文档**：README / ARCHITECTURE / AGENTS.md / docs/ / CHANGELOG。产出：项目定位、技术栈、数据源清单、特色实体清单、架构决策清单。
2. **建项目实体**：`projects/<name>.md`，用 `templates/project.md`，填 frontmatter（repo/license/stack/status/market/data_sources）。
3. **抽取数据源 → `data-sources/`**：
   - 先查现有 16 个数据源，匹配的**不新建**，只在已有实体的 `projects:` 列表追加当前项目名。
   - 不匹配的新建实体，`projects: [<current>]` + `origin_project: <current>`。
   - 限流/降级/endpoint 信息从项目代码或 docs 抽取，抽不到的标「待补」。
4. **抽取架构决策 → `specs/`**：
   - 各项目独立编号空间，**加项目前缀避免冲突**：trading-agents 用 `TA-S001`/`TA-DEC-001`，daily-stock-analysis 用 `DSA-S001`，a-Plate-Sentinel 用 `APS-S001`。Vibe-Research 保持现有 `S001`/`DEC-001`（隐含前缀 VR）。
   - frontmatter 加 `project: <current>`。
   - 只抽「已实现 + 影响架构」的关键决策，不全量灌入（对齐 specs/index.md 第 35 行「选已实现 + 影响架构的关键 spec 灌入」原则）。
5. **抽取特色实体**：
   - AI agent 角色 → `agents/`（`type: agent_role`，`project: <current>`）。
   - 战法 → `strategies/`（`type: strategy`，`project: <current>`），同源已有战法的建 `variant_of` 关系。
   - 产品功能模块（如 a-Plate-Sentinel 8 模块）→ **暂不建独立实体**，作为项目实体内部章节。待项目实现后再评估。
6. **更新共享实体的 `projects:` 列表**：当前项目引用的已有股票/行业/概念/指数实体，在其 `projects:` 列表追加当前项目名。
7. **跑质量门 + 更新 MOC**：
   - `reviews/` 体检：检查孤儿实体（查询 8）、字段完整性、`` 链接有效性。
   - MOC.md 项目轴表追加当前项目行。
   - `10_Reference/index/MASTER_INDEX.md` 项目目录表追加当前项目（若 MASTER_INDEX 有「项目目录」表）。

### 6.3 各项目纳入清单

**trading-agents（第一位）**：

| 步骤 | 产出 | 数量 | 备注 |
|---|---|---|---|
| 项目实体 | `projects/trading-agents.md` | 1 | repo/license=Apache 2.0/stack=[LangGraph, Python, Streamlit]/market=[A股] |
| 数据源去重 | 已有 6 个追加 `projects:`（mootdx/tencent/eastmoney-push2/eastmoney-datacenter/sina-financial/hithink-ths/baidu-stock） | 0 新建 | 实际匹配数以纳入时探查为准 |
| 数据源新建 | `data-sources/cls-cn.md`（财联社） | 1 | `projects: [trading-agents]` |
| agent 角色 | `agents/market-analyst.md` 等 | 7 | source_file 指向 `tradingagents/agents/analysts/*.py` |
| 架构决策 | `specs/TA-S001-...md` 等 | 待探查 | 从 CHANGES_FROM_UPSTREAM.md / DEV_LOG.md / docs/limitup-sniper-prd.md 抽取关键决策 |
| 跨项目关系 | 7 agent `contrasts_with` Vibe-Research 12 战法 | — | 在 MOC 查询 4 呈现，不在每个实体 frontmatter 标 |

**daily-stock-analysis（第二位）**：

| 步骤 | 产出 | 数量 | 备注 |
|---|---|---|---|
| 项目实体 | `projects/daily-stock-analysis.md` | 1 | license=MIT/stack=[Python, FastAPI, GitHub Actions]/market=[A股,港股,美股,日股,韩股,台股]，`embeds: trading-agents`（内嵌副本） |
| 数据源去重 | akshare/baostock/tushare 追加 `projects:` | 0 新建 | Tushare 此时新建（a-Plate-Sentinel 后续追加） |
| 数据源新建 | tushare/yfinance/longbridge/tickflow/pytdx + 新闻搜索源 | 5+ | 新闻搜索源（Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG）是合并为一个实体还是各建——**待探查各源职责差异后定** |
| 战法 | `strategies/<name>.md`（from yaml） | 18+ | `project: daily-stock-analysis`，`imported_from: strategies/xxx.yaml`。dragon_head 建 `variant_of` 指向 Vibe-Research 的 dragon_head（或反向——以先发源为 origin，待纳入时确认哪个是「原始」） |
| 架构决策 | `specs/DSA-S001-...md` 等 | 待探查 | 从 docs/architecture/ docs/full-guide.md 抽取 |

**a-Plate-Sentinel（延后，触发条件：情绪看板模块实现）**：

| 步骤 | 产出 | 数量 | 备注 |
|---|---|---|---|
| 项目实体 | `projects/a-plate-sentinel.md` | 1 | license=proprietary/stack=[FastAPI, React, TimescaleDB, Celery, Redis]/market=[A股]/status=mvp |
| 数据源 | tushare 追加 `projects:` | 0 新建 | Tushare 已在 daily-stock-analysis 纳入时建 |
| 8 模块 | 项目实体内部章节 | 0 独立实体 | 待实现后评估是否建 `modules/` 文件夹 |
| STI 情绪指数 | 待探查 | — | 与 `10_Reference/market_sentiment/` 子区建 `complements` 关系 |` 子区建 `complements` 关系

---

## 7. 风险与未决项

| # | 风险/未决项 | 影响 | 处置 |
|---|---|---|---|
| R1 | **编号空间冲突**：Vibe-Research 用 S001-S166，新项目若也用 S 前缀会撞号 | spec 实体混淆 | §6.2 步骤 4 已定项目前缀方案（TA-/DSA-/APS-），纳入时严格执行 |
| R2 | **战法 origin 争议**：dragon_head 在 Vibe-Research 和 daily-stock-analysis 都有，哪个是「原始」 | `origin_project` / `variant_of` 方向 | 待纳入 daily-stock-analysis 时探查：Vibe-Research 的 dragon_head.md 第 38 行已声明参数来源是 daily-stock-analysis 的 yaml，故 daily-stock-analysis 是 origin，Vibe-Research 是 variant。`variant_of` 方向：VR → DSA |
| R3 | **新闻搜索源粒度**：daily-stock-analysis 的 7 个新闻搜索源（Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG）合并为一个实体还是各建 | data-sources/ 实体数 | 待探查各源职责差异。若仅「提供商不同、能力同」则合并为 `news-search-aggregators.md`；若职责分化则各建 |
| R4 | **a-Plate-Sentinel 纳入时机**：MVP 骨架阶段，过早纳入产生「待补」占位实体 | 图谱质量 | §6.1 已定触发条件（情绪看板实现 + 闭环验证通过），纳入前不建实体 |
| R5 | **存量迁移字段遗漏**：54+ 实体加字段，手工易漏 | 孤儿实体 | §3.3 建议规则脚本批量改 + 查询 8 审计 |
| R6 | **`embeds` 副本**：daily-stock-analysis 内嵌 TradingAgents-astock 副本，若误纳入会重复 | 数据源/spec 重复 | §6.3 已定：副本不纳入，标 `embeds` 关系指向独立 trading-agents 项目实体 |
| R7 | **indices/reports/metrics/valuations/dragon-tiger/events 实体数未探查** | 存量迁移范围不全 | 纳入前补探查，更新 §3.3 迁移表 |
| R8 | **MOC 标题与 README 一致性**：MOC 改「投研知识图谱（多项目）」后，README.md / MASTER_INDEX.md 的描述也要同步 | 文档不一致 | §6.2 步骤 7 纳入流程含 MASTER_INDEX 更新；README.md 在第一个项目（trading-agents）纳入时一并改 |

---

## 附录 A：探查原始记录

探查时间：2026-09-06。探查方法：读 README/AGENTS.md/docs/ + ls 源码目录。

**A.1 trading-agents**
- README.md（392 行）：Apache 2.0，基于 TauricResearch/TradingAgents fork，7 Analyst 角色（市场/舆情/新闻/基本面/政策/游资/解禁），双 LLM 设计（quick_think + deep_think），数据源 mootdx/腾讯/东财/新浪/同花顺/财联社/百度，东财防封 `_em_get()` 串行限流。
- 源码：`tradingagents/agents/analysts/` 下 7 个 .py（market/social_media/news/fundamentals/policy/hot_money_tracker/lockup_watcher）+ `_factory.py`。
- docs/：仅 `limitup-sniper-prd.md`。
- CHANGES_FROM_UPSTREAM.md / DEV_LOG.md / CHANGELOG.md 存在，是抽取架构决策的来源。

**A.2 daily-stock-analysis**
- 实际路径：`daily-stock-analysis/daily_stock_analysis/`（外层目录还嵌了一份 `TradingAgents-astock/` 副本）。
- README.md（301 行）：ZhuLinsen/daily_stock_analysis，MIT，多市场（A股/港股/美股/日股/韩股/台股），GitHub Actions/Docker/本地定时，推送企业微信/飞书/Telegram/Discord/Slack/邮件。数据源 AkShare/Tushare/Pytdx/Baostock/YFinance/Longbridge/TickFlow + 新闻搜索 Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG。Agent 策略问股 15 种内置策略。
- 战法：`strategies/*.yaml` 18+ 个（bottom_volume/box_oscillation/bull_trend/chan_theory/debate_battle/debate_consensus/debate_research/dragon_head/emotion_cycle/event_driven/expectation_repricing/growth_quality/hot_theme/ma_golden_cross/one_yang_three_yin/shrink_pullback/volume_breakout/wave_theory）。
- docs/：50+ 文档（architecture/ full-guide.md market-support.md decision-signals.md limitup-trading-workflow-prd.md 等），是抽取架构决策的来源。

**A.3 a-Plate-Sentinel**
- README.md（51 行）：A股打板情绪监控，Docker Compose，Tushare 数据源，8 大模块，docs/prd.md V2.0 + docs/module-design.md。**当前进度：情绪看板数据模型+计算服务骨架已生成，待补全算法细节与API/前端。**
- AGENTS.md（78 行）：技术栈 FastAPI+Python 3.11+React 18+TimescaleDB+PostgreSQL 15+Redis 7+Celery。核心算法 STI（情绪温度指数，7维加权）+ 龙虎榜席位标签。MVP 阶段，龙虎榜席位引擎/回测/AI复盘Agent 留 Phase 2。
- docs/：prd.md / module-design.md / sti-backtest-plan.md。

**A.4 Vibe-Research（现状，已纳入）**
- 图谱已有：13 spec + 5 DEC（specs/）、16 数据源（data-sources/）、12 战法（strategies/）、11 股票、7 行业、6 概念。
- 所有实体 frontmatter 无 `project:` 字段（已 grep 确认）。
- strategies/dragon_head.md 第 38 行已引用 daily-stock-analysis 的 dragon_head.yaml（事实 1 证据）。

**A.5 Vibe-Research-bakup**
- 备份目录，不纳入。

---

> **下一步**：本设计评审通过后，按 §6.1 优先级串行纳入。第一个纳入 trading-agents 时，同步完成：① 存量 54+ 实体加字段（§3.3）；② 新建 projects/ + agents/ 文件夹与模板；③ MOC 双轴改造（§4.2）；④ 跑质量门（查询 8）。每纳入一个项目跑一次 reviews/ 体检，确认设计成立再继续下一个。
