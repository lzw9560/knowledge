# Vibe-Research 投研知识图谱

> 这个 vault 是 Vibe-Research 项目的**语义层**，把代码里的实体（Pydantic 契约模型）、spec 决策、战法、数据源链接成可导航的知识图谱。代码层管"数据怎么流"，本 vault 管"知识怎么连"——个股属于哪个行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来，都在这里通过 `[[]]` 双链和 Dataview 查询织成网。

---

## 📊 图谱健康摘要

> 实时统计——总实体数、各类型分布、最近更新、孤立节点。

```dataview
TABLE WITHOUT ID
  length(rows) AS "实体总数"
FROM "10_Reference/investing"
WHERE type != null AND file.name != "index" AND file.name != "MOC" AND file.name != "README"
```

### 各类型实体计数

```dataview
TABLE WITHOUT ID
  key AS "类型",
  length(rows) AS "数量",
  rows.file.link AS "样本"
FROM "10_Reference/investing"
WHERE type != null AND file.name != "index" AND file.name != "MOC" AND file.name != "README"
GROUP BY type AS key
SORT key ASC
FLATTEN rows
LIMIT 1
```

```dataview
TABLE length(rows) AS "实体数"
FROM "10_Reference/investing"
WHERE type != null AND file.name != "index" AND file.name != "MOC" AND file.name != "README"
GROUP BY type
SORT type ASC
```

---

## 🗂 实体类导航（本体构件 1：实体）

> 四构件本体模型蒸馏自 nano-ontoprompt。构件 1-2 为静态层，3-4 为动态层。

| 实体类 | 文件夹 | 说明 |
|---|---|---|
| 📈 股票 | [[stocks/]] | A 股/美股/港股个股，对应 `Quote` + `CompanyInfo` |
| 🏭 行业板块 | [[industries/]] | 证监会行业分类，对应 `IndustrySector` |
| 💡 概念板块 | [[concepts/]] | 概念题材板块，对应 `ConceptBlock` + `Sector` |
| 📊 指数 | [[indices/]] | 沪深300/中证500等宽基与行业指数 |
| 📰 研报 | [[reports/]] | 机构研报，对应 `Report` 契约 |
| 👤 分析师 | [[analysts/]] | 研报作者，对应 `Report.researcher` |
| 💰 财务指标 | [[metrics/]] | 营收/ROE/毛利率等，对应 `Financials` + `FinancialPeriod` |
| 📈 估值 | [[valuations/]] | PE/PB/PEG/分位，对应 `Valuation` + `ValuationPercentile` |
| 🐉 龙虎榜 | [[dragon-tiger/]] | 游资席位，对应 `Seat` + `BillboardDetail` + `DragonTiger` |
| ⚡ 事件 | [[events/]] | 新闻/公告/涨停，对应 `News` + `Announcement` + `ZTPoolItem` |
| ⚔️ 战法 | [[strategies/]] | 战法卡（从 `backend/strategies/cards/` 导入） |
| 📋 项目决策 | [[specs/]] | SDD spec 决策实体，对应 `specs/` 目录 |
| 📡 数据源 | [[data-sources/]] | 外部数据源，对应 `ARCHITECTURE` 数据流 |
| 🤖 AI 角色 | [[agents/]] | trading-agents 的 7 Analyst（区别于 analysts 真人） |

### 各类型实体计数（Dataview 动态）

```dataview
TABLE length(rows) AS "实体数"
FROM "10_Reference/investing"
WHERE type != null AND file.name != "index" AND file.name != "MOC" AND file.name != "README"
GROUP BY type
SORT type ASC
```

---

## 🔍 快速查询

> 5 个最常用的 Dataview 查询模板——复制粘贴即可用。

### 1. 白酒行业股票 PE 排序

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  pe_ttm AS "PE(TTM)",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND industry = "白酒"
SORT pe_ttm ASC
```

### 2. PE < 15 低估值股票

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  pe_ttm AS "PE(TTM)",
  pb AS "PB",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND pe_ttm < 15 AND pe_ttm > 0
SORT pe_ttm ASC
LIMIT 20
```

### 3. 近期涨停池事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event"
SORT date DESC
LIMIT 10
```

### 4. 最近研报

```dataview
TABLE WITHOUT ID
  publish_date AS "日期",
  org AS "机构",
  researcher AS "分析师",
  title AS "标题"
FROM "10_Reference/investing/reports"
WHERE type = "report"
SORT publish_date DESC
LIMIT 15
```

### 5. 龙虎榜游资席位

```dataview
TABLE WITHOUT ID
  date AS "日期",
  code AS "股票",
  institution_net AS "机构净额",
  seats AS "席位"
FROM "10_Reference/investing/dragon-tiger"
WHERE type = "dragon_tiger"
SORT date DESC
LIMIT 10
```

---

## 🕐 最近更新

> 最近修改的 10 个文件——追踪图谱最新活动。

```dataview
TABLE WITHOUT ID
  file.link AS "文件",
  type AS "类型",
  file.mtime AS "修改时间"
FROM "10_Reference/investing"
WHERE type != null
SORT file.mtime DESC
LIMIT 10
```

---

## 🔗 关系层（本体构件 2：关系）

关系通过 `[[]]` 双向链接 + frontmatter 谓词标注实现。预定义关系谓词：
`belongs_to` / `tagged` / `covered_by` / `has_metric` / `valued_at` / `involves` / `affects` / `matches` / `authored_by` / `triggered_by`

## ⚙️ 动态层（本体构件 3-4）

| 构件 | 文件夹 | 说明 |
|---|---|---|
| **⚙️ 逻辑规则** | [[logic/]] | schema 约束/校验/状态机/推断规则 |
| **⚡ 动作** | [[actions/]] | CRUD/状态流转/链接维护/审计快照 |

## 🛡 质量门（Curated）

| 层 | 文件夹 | 作用 |
|---|---|---|
| **📥 待审** | [[inbox/]] | LLM 抽取实体先进此，带 confidence + source + quality_score，审核通过才进正式区 |
| **🔍 审查** | [[reviews/]] | ReAct Agent 定期体检报告（8 项检查） |

> 不直接灌入是知识图谱健康的第一道防线。详见 [[inbox/index]] 质量四维度。

### ⚔️ 战法卡统计

```dataview
TABLE WITHOUT ID
  name AS "战法",
  edge_family AS "edge 家族",
  file.link AS "详情"
FROM "10_Reference/investing/strategies"
WHERE type = "strategy"
SORT name ASC
```

### 📋 项目决策统计

```dataview
TABLE WITHOUT ID
  number AS "编号",
  title AS "标题",
  status AS "状态",
  file.link AS "详情"
FROM "10_Reference/investing/specs"
WHERE type = "spec"
SORT number ASC
```

---

## 📖 使用说明

### 1. 新建实体（Templater）

1. 在 Obsidian 中安装 **Templater** 插件并启用。
2. 设置 → Templater → Template folder location 填 `templates`。
3. 在任意实体文件夹下新建笔记 → 命令面板 `Ctrl/Cmd+P` → `Templater: Create new note from template` → 选对应模板（如 `stock`）。
4. 模板会自动填入 YAML frontmatter + 正文骨架，`<% tp.date.now("YYYY-MM-DD") %>` 自动替换为当日日期。

### 2. 链接（`[[]]` 双链）

- 在任意笔记正文中输入 `[[stocks/600519]]` 即可链接到个股笔记；若笔记不存在，Obsidian 会高亮提示并支持一键创建。
- **双向**：在股票笔记里写 `[[industries/食品饮料]]`，行业笔记的"反向链接"区会自动出现该股票。
- 文件夹链接用 `[[stocks/]]` 形式，Obsidian 会指向该文件夹的 `index.md`。

### 3. 查询（Dataview）

- 安装 **Dataview** 插件后，所有 `index.md` 里的 ```dataview 代码块会动态渲染。
- 查询语法：`TABLE 字段 FROM "文件夹" WHERE 条件 SORT 字段`。
- 示例——查所有 PE < 15 的股票：

```dataview
TABLE code AS "代码", name AS "名称", pe_ttm AS "PE(TTM)", pb AS "PB"
FROM "stocks"
WHERE type = "stock" AND pe_ttm < 15
SORT pe_ttm ASC
```

### 4. 图谱视图

左侧栏图标 → Graph View（快捷键 `Ctrl/Cmd+G`），可看到所有实体的双链网络。建议按 `type` 字段染色区分股票/行业/研报/战法。

## 🔍 分析工具

> 知识图谱深度分析层——图算法/时间线/因果链，从"实体+关系"两层扩展到可计算的图结构。

- **图算法分析**：`scripts/graph_analysis.py` → `docs/graph-analysis-report.md`
  - 社区发现（LPA 标签传播）/ 入度中心性（hub 节点）/ 桥节点（跨社区连接者）/ BFS 最短路径
- **时间线视图**：`scripts/timeline_view.py` → `docs/timeline-report.md`
  - 按 frontmatter date 字段排列所有事件实体，按月分组
- **因果链规则**：[[logic/causal-chains]] — 因果（→）vs 相关（↔）vs 待验证（?>）标注规范

---

## 🏗 与项目代码的关系

| 层 | 位置 | 职责 |
|---|---|---|
| 代码契约层 | `backend/models/` | Pydantic 模型定义数据结构（Quote/Valuation/Financials…） |
| 数据流层 | `backend/` + `ARCHITECTURE.md` | 数据采集/加工/存储管线 |
| 战法执行层 | `backend/strategies/` | 战法 match 逻辑 + cards/ 战法卡 |
| **语义层（本 vault）** | `knowledge/` | 实体关系导航、研报笔记、投研知识沉淀 |
| 决策记录层 | `specs/` | SDD spec 决策文档 |

本 vault 不复制代码逻辑，只做**知识表征**：一个股票笔记链接它的行业、研报、财务、估值、龙虎榜、相关战法，形成可回溯的投研上下文。代码改了模型字段，来这里改对应模板的 frontmatter 即可。

---

## 🔗 关联子区

- [[10_Reference/market_sentiment/DASHBOARD]] — 市场情绪追踪（每日 pre/mid/post 报告 + z-score 温度）
- 战法卡有"适用天气：阴天"，market_sentiment 有温度 Z 值——但定义"阴天 = 哪个 Z 区间"的逻辑待建（见 [[logic/战法天气映射]]）

### 关联项目（ora-2 方案 D 纳入的外部投研项目）

- [[specs/a-plate-sentinel-project]] — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架阶段）
- [[specs/trading-agents-project]] — TradingAgents A股深度特化 fork（7 Analyst + 多 Agent 辩论）
- [[specs/daily-stock-analysis-project]] — 每日股票分析报告生成器（多市场、多渠道推送）

关联项目使用的数据源：
- [[data-sources/tushare]]（a-Plate-Sentinel 专用，积分制）
- [[data-sources/akshare]] / [[data-sources/baostock]] / [[data-sources/mootdx]]（与 Vibe-Research 共用）

## 🌐 跨领域链接（ora-3 §4）

> 投研方法论与其他知识域的"同构"链接。判据（[[logic/cross-domain-gate]]，待建）：
> 跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

### 已建链接

- [[strategies/dragon_head]] §方法论链接 — 「板块轮动识别龙头」↔ 时间序列状态识别（🚧 待建）
- [[10_Reference/meta/four-construct-ontology]] — 四构件本体方法论（领域无关模板）

### 待建领域

- **技术学习领域**（智驾/时序模型/世界模型）：与投研的同构点见 ora-3 §4.2 表（时序模型↔情绪温度 ΔZ / 世界模型↔反事实推演 / 端到端 vs 模块化↔规则+LLM 兜底 / 多传感器融合↔6 层 z-score+三重护栏 / corner case↔熔断机制）
- **元知识层**：[[10_Reference/meta/]] — 通用方法论（PARA/MOC/四构件本体）

> 跨域链接数 / 单域链接数 < 20%（防"什么都记但什么都不深"）。当前投研子区跨域链接 = 0，远未到风险，待跨域实体落地后监控。
