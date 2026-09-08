---
type: moc
draft: false
description: 投研知识图谱入口——将代码实体（Pydantic 契约模型）、spec 决策、战法、数据源链接成可导航的语义层。21 实体类，2510+ 实体，12 战法卡。
---

# Vibe-Research 投研知识图谱

> [!abstract] 关于本图谱
> 这个 vault 是 Vibe-Research 项目的**语义层**，把代码里的实体（Pydantic 契约模型）、spec 决策、战法、数据源链接成可导航的知识图谱。代码层管"数据怎么流"，本 vault 管"知识怎么连"——个股属于哪个行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来，都在这里通过 `[[]]` 双链和 Dataview 查询织成网。

> [!tip] 🔍 快速搜索
> 在特定类型里找内容？按 `Ctrl/Cmd + K` 打开搜索，支持按标题/正文/标签匹配。下方「热门查询」段直接展示 5 个最常用查询的结果。

---

## 📊 图谱健康摘要

> [!abstract] 实时统计——总实体数、各类型分布、最近更新、孤立节点。

<!-- stats-anchor:total -->
| 实体总数 |
|---|
| 2510 |
<!-- /stats-anchor -->

### 各类型实体计数

<!-- stats-anchor:type-counts -->
| 类型 | 数量 |
|---|---|
| stock | 411 |
| metric | 401 |
| valuation | 401 |
| analyst | 396 |
| report | 393 |
| concept | 130 |
| industry | 126 |
| spec | 101 |
| dragon_tiger | 41 |
| logic | 24 |
| event | 22 |
| data_source | 17 |
| strategy | 13 |
| agent_role | 7 |
| action | 5 |
| decision | 5 |
| index | 5 |
| inbox_item | 4 |
| project | 4 |
| audit | 3 |
| procedure | 1 |
<!-- /stats-anchor -->

<!-- dataview-precompiled:4c078f03a97b query:VEFCTEUK57G75Z6LIEFTICLnsbvlnosiLAogIOaVsOmHjyBBUyAi5pWw6YePIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nIgpXSEVSRSB0eXBlID0gIm1vYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 类型 | 数量 |
|---|---|---|
| [[10_Reference/investing/MOC]] | — | — |
<!-- /dataview-precompiled -->

---

## 🕐 最近更新

> [!note] 最近 7 天修改的 10 个文件——追踪图谱最新活动。侧边栏「最近更新」组件同步显示。

<!-- dataview-precompiled:edab4ad6d5d8 query:VEFCTEUK57G75Z6LIEFTICLnsbvlnosiLAogIOS/ruaUueaXtumXtCBBUyAi5L+u5pS55pe26Ze0IgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nIgpXSEVSRSB0eXBlID0gIm1vYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 类型 | 修改时间 |
|---|---|---|
| [[10_Reference/investing/MOC]] | — | — |
<!-- /dataview-precompiled -->

---

## 🔥 热门查询

> [!example] 5 个最常用的查询——直接展示结果，复制查询代码到其他笔记即可复用。

### 1. 白酒行业股票 PE 排序

<!-- dataview-precompiled:46df5088dad8 query:VEFCTEUK5Luj56CBIEFTICLku6PnoIEiLAogIG5hbWUgQVMgIuWQjeensCIsCiAgcGVfdHRtIEFTICJQRShUVE0pIiwKICBtYXJrZXRfY2FwIEFTICLluILlgLwiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmciCldIRVJFIHR5cGUgPSAibW9jIgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 代码 | 名称 | PE(TTM) | 市值 |
|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — |
<!-- /dataview-precompiled -->

### 2. PE < 15 低估值股票

<!-- dataview-precompiled:65066dc55f3a query:VEFCTEUK5Luj56CBIEFTICLku6PnoIEiLAogIG5hbWUgQVMgIuWQjeensCIsCiAgcGVfdHRtIEFTICJQRShUVE0pIiwKICBwYiBBUyAiUEIiLAogIG1hcmtldF9jYXAgQVMgIuW4guWAvCIKRlJPTSAiMTBfUmVmZXJlbmNlL2ludmVzdGluZyIKV0hFUkUgdHlwZSA9ICJtb2MiClNPUlQgY29kZSBBU0MK -->
| 文件 | 代码 | 名称 | PE(TTM) | PB | 市值 |
|---|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — | — |
<!-- /dataview-precompiled -->

### 3. 近期涨停池事件

<!-- dataview-precompiled:8bdfe02cd754 query:VEFCTEUKY3JlYXRlZCBBUyAi5pel5pyfIiwKICDnsbvlnosgQVMgIuexu+WeiyIsCiAg5pGY6KaBIEFTICLmkZjopoEiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmciCldIRVJFIHR5cGUgPSAibW9jIgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 日期 | 类型 | 摘要 |
|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — |
<!-- /dataview-precompiled -->

### 4. 最近研报

<!-- dataview-precompiled:ceda303a2d34 query:VEFCTEUKY3JlYXRlZCBBUyAi5pel5pyfIiwKICDmnLrmnoQgQVMgIuacuuaehCIsCiAg5YiG5p6Q5biIIEFTICLliIbmnpDluIgiLAogIOagh+mimCBBUyAi5qCH6aKYIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nIgpXSEVSRSB0eXBlID0gIm1vYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 日期 | 机构 | 分析师 | 标题 |
|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — |
<!-- /dataview-precompiled -->

### 5. 龙虎榜游资席位

<!-- dataview-precompiled:9f11fc53feaf query:VEFCTEUKY3JlYXRlZCBBUyAi5pel5pyfIiwKICDogqHnpaggQVMgIuiCoeelqCIsCiAg5py65p6E5YeA6aKdIEFTICLmnLrmnoTlh4Dpop0iLAogIOW4reS9jSBBUyAi5bit5L2NIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nIgpXSEVSRSB0eXBlID0gIm1vYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 日期 | 股票 | 机构净额 | 席位 |
|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — |
<!-- /dataview-precompiled -->

---

## 🗂 实体类导航（本体构件 1：实体）

> 四构件本体模型蒸馏自 nano-ontoprompt。构件 1-2 为静态层，3-4 为动态层。

| 实体类 | 文件夹 | 说明 |
|---|---|---|
| 📈 股票 | [stocks/](10_Reference/meta/index) |A 股/美股/港股个股]]，对应 `Quote` + `CompanyInfo` |
| 🏭 行业板块 | [industries/](10_Reference/meta/index) |证监会行业分类]]，对应 `IndustrySector` |
| 💡 概念板块 | [concepts/](10_Reference/meta/index) |概念题材板块]]，对应 `ConceptBlock` + `Sector` |
| 📊 指数 | [indices/](10_Reference/meta/index) |沪深300/中证500等宽基与行业指数 |]]
| 📰 研报 | [reports/](10_Reference/meta/index) |机构研报]]，对应 `Report` 契约 |
| 👤 分析师 | [analysts/](10_Reference/meta/index) |研报作者]]，对应 `Report.researcher` |
| 💰 财务指标 | [metrics/](10_Reference/meta/index) |营收/ROE/毛利率等]]，对应 `Financials` + `FinancialPeriod` |
| 📈 估值 | [valuations/](10_Reference/meta/index) |PE/PB/PEG/分位]]，对应 `Valuation` + `ValuationPercentile` |
| 🐉 龙虎榜 | [dragon-tiger/](10_Reference/meta/index) |游资席位]]，对应 `Seat` + `BillboardDetail` + `DragonTiger` |
| ⚡ 事件 | [events/](10_Reference/meta/index) |新闻/公告/涨停]]，对应 `News` + `Announcement` + `ZTPoolItem` |
| ⚔️ 战法 | [strategies/](10_Reference/meta/index) |战法卡（从 `backend/strategies/cards/` 导入） |]]
| 📋 项目决策 | [specs/](10_Reference/meta/index) |SDD spec 决策实体]]，对应 `specs/` 目录 |
| 📡 数据源 | [data-sources/](10_Reference/meta/index) |外部数据源]]，对应 `ARCHITECTURE` 数据流 |
| 🤖 AI 角色 | [agents/](10_Reference/meta/index) |trading-agents 的 7 Analyst（区别于 analysts 真人） |]]


<!-- index 入边段 -->
> 各类型 index.md 入边——确保每个类型索引页至少有 1 个入边。

- [[10_Reference/investing/actions/index]]
- [[10_Reference/investing/agents/index]]
- [[10_Reference/investing/analysts/index]]
- [[10_Reference/investing/concepts/index]]
- [[10_Reference/investing/data-sources/index]]
- [[10_Reference/investing/dragon-tiger/index]]
- [[10_Reference/investing/events/index]]
- [[10_Reference/investing/indices/index]]
- [[10_Reference/investing/industries/index]]
- [[10_Reference/investing/logic/index]]
- [[10_Reference/investing/metrics/index]]
- [[10_Reference/investing/reports/index]]
- [[10_Reference/investing/specs/index]]
- [[10_Reference/investing/stocks/index]]
- [[10_Reference/investing/strategies/index]]
- [[10_Reference/investing/valuations/index]]

### 各类型实体计数（Dataview 动态）

<!-- dataview-precompiled:4c078f03a97b query:VEFCTEUK57G75Z6LIEFTICLnsbvlnosiLAogIOaVsOmHjyBBUyAi5pWw6YePIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nIgpXSEVSRSB0eXBlID0gIm1vYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 类型 | 数量 |
|---|---|---|
| [[10_Reference/investing/MOC]] | — | — |
<!-- /dataview-precompiled -->

---

## 🔗 关系层（本体构件 2：关系）

关系通过 `[[]]` 双向链接 + frontmatter 谓词标注实现。预定义关系谓词：
`belongs_to` / `tagged` / `covered_by` / `has_metric` / `valued_at` / `involves` / `affects` / `matches` / `authored_by` / `triggered_by`

## ⚙️ 动态层（本体构件 3-4）

| 构件 | 文件夹 | 说明 |
|---|---|---|
| **⚙️ 逻辑规则** | [logic/](10_Reference/meta/index) |schema 约束/校验/状态机/推断规则 |]]
| **⚡ 动作** | [actions/](10_Reference/meta/index) |CRUD/状态流转/链接维护/审计快照 |]]

## 🛡 质量门（Curated）

| 层 | 文件夹 | 作用 |
|---|---|---|
| **📥 待审** | [inbox/](10_Reference/meta/index) |LLM 抽取实体先进此]]，带 confidence + source + quality_score，审核通过才进正式区 |
| **🔍 审查** | [reviews/](10_Reference/meta/index) |ReAct Agent 定期体检报告（8 项检查） |]]

> 不直接灌入是知识图谱健康的第一道防线。详见 [[10_Reference/investing/inbox/index]] 质量四维度。

### ⚔️ 战法卡统计

<!-- dataview-precompiled:fa24d87c9428 query:VEFCTEUK5oiY5rOVIEFTICLmiJjms5UiLAogIGVkZ2Ug5a625pePIEFTICJlZGdlIOWutuaXjyIsCiAg6K+m5oOFIEFTICLor6bmg4UiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmciCldIRVJFIHR5cGUgPSAibW9jIgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 战法 | edge 家族 | 详情 |
|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — |
<!-- /dataview-precompiled -->

### 📋 项目决策统计

<!-- dataview-precompiled:9ae122d084ed query:VEFCTEUK57yW5Y+3IEFTICLnvJblj7ciLAogIOagh+mimCBBUyAi5qCH6aKYIiwKICDnirbmgIEgQVMgIueKtuaAgSIsCiAg6K+m5oOFIEFTICLor6bmg4UiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmciCldIRVJFIHR5cGUgPSAibW9jIgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 编号 | 标题 | 状态 | 详情 |
|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — |
<!-- /dataview-precompiled -->

---

## 📖 使用说明

### 1. 新建实体（Templater）

1. 在 Obsidian 中安装 **Templater** 插件并启用。
2. 设置 → Templater → Template folder location 填 `templates`。
3. 在任意实体文件夹下新建笔记 → 命令面板 `Ctrl/Cmd+P` → `Templater: Create new note from template` → 选对应模板（如 `stock`）。
4. 模板会自动填入 YAML frontmatter + 正文骨架，`<% tp.date.now("YYYY-MM-DD") %>` 自动替换为当日日期。

### 2. 链接（`[[]]` 双链）

- 在任意笔记正文中输入 `[[10_Reference/investing/stocks/600519]]` 即可链接到个股笔记；若笔记不存在，Obsidian 会高亮提示并支持一键创建。
- **双向**：在股票笔记里写 `[[10_Reference/investing/industries/食品饮料]]`，行业笔记的"反向链接"区会自动出现该股票。
- 文件夹链接用 `[[10_Reference/investing/stocks/index|stocks/]]` 形式，Obsidian 会指向该文件夹的 `index.md`。

### 3. 查询（Dataview）

- 安装 **Dataview** 插件后，所有 `index.md` 里的 ```dataview 代码块会动态渲染。
- 查询语法：`TABLE 字段 FROM "文件夹" WHERE 条件 SORT 字段`。
- 示例——查所有 PE < 15 的股票：

<!-- dataview-precompiled:7cc371739e87 query:VEFCTEUK5Luj56CBIEFTICLku6PnoIEiLAogIG5hbWUgQVMgIuWQjeensCIsCiAgcGVfdHRtIEFTICJQRShUVE0pIiwKICBwYiBBUyAiUEIiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmciCldIRVJFIHR5cGUgPSAibW9jIgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 代码 | 名称 | PE(TTM) | PB |
|---|---|---|---|---|
| [[10_Reference/investing/MOC]] | — | — | — | — |
<!-- /dataview-precompiled -->

### 4. 图谱视图

左侧栏图标 → Graph View（快捷键 `Ctrl/Cmd+G`），可看到所有实体的双链网络。建议按 `type` 字段染色区分股票/行业/研报/战法。

## 🔍 分析工具

> 知识图谱深度分析层——图算法/时间线/因果链，从"实体+关系"两层扩展到可计算的图结构。

- **图算法分析**：`scripts/graph_analysis.py` → `docs/graph-analysis-report.md`
  - 社区发现（LPA 标签传播）/ 入度中心性（hub 节点）/ 桥节点（跨社区连接者）/ BFS 最短路径
- **时间线视图**：`scripts/timeline_view.py` → `docs/timeline-report.md`
  - 按 frontmatter date 字段排列所有事件实体，按月分组
- **因果链规则**：[[10_Reference/investing/logic/因果链]] — 因果（→）vs 相关（↔）vs 待验证（?>）标注规范

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

- [[10_Reference/market_sentiment/情绪仪表盘]] — 市场情绪追踪（每日 pre/mid/post 报告 + z-score 温度）
- 战法卡有"适用天气：阴天"，market_sentiment 有温度 Z 值——但定义"阴天 = 哪个 Z 区间"的逻辑待建（见 [[10_Reference/investing/logic/战法天气映射]]）

### 关联项目（ora-2 方案 D 纳入的外部投研项目）

- [[10_Reference/investing/specs/a-Plate-Sentinel项目 — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架阶段）]]
- [[10_Reference/investing/specs/TradingAgents项目]] — TradingAgents A股深度特化 fork（7 Analyst + 多 Agent 辩论）
- [[10_Reference/investing/specs/每日股票分析项目]] — 每日股票分析报告生成器（多市场、多渠道推送）

关联项目使用的数据源：
- [[10_Reference/investing/data-sources/Tushare]]（a-Plate-Sentinel 专用，积分制）
- [[10_Reference/investing/data-sources/AkShare]] / [[10_Reference/investing/data-sources/baostock（K线日更）]] / [[10_Reference/investing/data-sources/mootdx]]（与 Vibe-Research 共用）

## 🌐 跨领域链接（ora-3 §4）

> 投研方法论与其他知识域的"同构"[[10_Reference/investing/logic/跨域门控]]，待建）：
> 跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

### 已建链接

- [[10_Reference/investing/strategies/龙头战法]] §方法论链接 — 「板块轮动识别龙头」↔ 时间序列状态识别（🚧 待建）
- [[10_Reference/meta/四构件本体方法论]] — 四构件本体方法论（领域无关模板）

### 待建领域

- **技术学习领域**（智驾/时序模型/世界模型）：与投研的同构点见 ora-3 §4.2 表（时序模型↔情绪温度 ΔZ / 世界模型↔反事实推演 / 端到端 vs 模块化↔规则+LLM 兜底 / 多传感器融合↔6 层 z-score+三重护栏 / corner case↔熔断机制）
- **元知识层**：[[10_Reference/meta/index]] — 通用方法论（PARA/MOC/四构件本体）

> 跨域链接数 / 单域链接数 < 20%（防"什么都记但什么都不深"）。当前投研子区跨域链接 = 0，远未到风险，待跨域实体落地后监控。
