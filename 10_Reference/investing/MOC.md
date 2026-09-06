# Vibe-Research 投研知识图谱

> 这个 vault 是 Vibe-Research 项目的**语义层**，把代码里的实体（Pydantic 契约模型）、spec 决策、战法、数据源链接成可导航的知识图谱。代码层管"数据怎么流"，本 vault 管"知识怎么连"——个股属于哪个行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来，都在这里通过 `[[]]` 双链和 Dataview 查询织成网。

## 实体类导航（本体构件 1：实体）

> 四构件本体模型蒸馏自 nano-ontoprompt。构件 1-2 为静态层，3-4 为动态层。

| 实体类  | 文件夹               | 说明                                                  | 当前数量                                                                    |
| ---- | ----------------- | --------------------------------------------------- | ----------------------------------------------------------------------- |
| 股票   | [[stocks/]]       | A 股/美股/港股个股，对应 `Quote` + `CompanyInfo`              | `= length(filter(this.file.inlinks, (l) => l.folder = "stocks"))`       |
| 行业板块 | [[industries/]]   | 证监会行业分类，对应 `IndustrySector`                         | `= length(filter(this.file.inlinks, (l) => l.folder = "industries"))`   |
| 概念板块 | [[concepts/]]     | 概念题材板块，对应 `ConceptBlock` + `Sector`                 | `= length(filter(this.file.inlinks, (l) => l.folder = "concepts"))`     |
| 指数   | [[indices/]]      | 沪深300/中证500等宽基与行业指数                                 | `= length(filter(this.file.inlinks, (l) => l.folder = "indices"))`      |
| 研报   | [[reports/]]      | 机构研报，对应 `Report` 契约                                 | `= length(filter(this.file.inlinks, (l) => l.folder = "reports"))`      |
| 分析师  | [[analysts/]]     | 研报作者，对应 `Report.researcher`                         | `= length(filter(this.file.inlinks, (l) => l.folder = "analysts"))`     |
| 财务指标 | [[metrics/]]      | 营收/ROE/毛利率等，对应 `Financials` + `FinancialPeriod`     | `= length(filter(this.file.inlinks, (l) => l.folder = "metrics"))`      |
| 估值   | [[valuations/]]   | PE/PB/PEG/分位，对应 `Valuation` + `ValuationPercentile` | `= length(filter(this.file.inlinks, (l) => l.folder = "valuations"))`   |
| 龙虎榜  | [[dragon-tiger/]] | 游资席位，对应 `Seat` + `BillboardDetail` + `DragonTiger`  | `= length(filter(this.file.inlinks, (l) => l.folder = "dragon-tiger"))` |
| 事件   | [[events/]]       | 新闻/公告/涨停，对应 `News` + `Announcement` + `ZTPoolItem`  | `= length(filter(this.file.inlinks, (l) => l.folder = "events"))`       |
| 战法   | [[strategies/]]   | 战法卡（从 `backend/strategies/cards/` 导入）               | `= length(filter(this.file.inlinks, (l) => l.folder = "strategies"))`   |
| 项目决策 | [[specs/]]        | SDD spec 决策实体，对应 `specs/` 目录                        | `= length(filter(this.file.inlinks, (l) => l.folder = "specs"))`        |
| 数据源  | [[data-sources/]] | 外部数据源，对应 `ARCHITECTURE` 数据流                         | `= length(filter(this.file.inlinks, (l) => l.folder = "data-sources"))` |
| AI 角色 | [[agents/]]       | trading-agents 的 7 Analyst（区别于 analysts 真人）          | `= length(filter(this.file.inlinks, (l) => l.folder = "agents"))`       |

### 各类型实体计数（Dataview 动态）

```dataview
TABLE length(rows) AS "实体数"
FROM "10_Reference/investing"
WHERE type != null AND file.name != "index" AND file.name != "MOC" AND file.name != "README"
GROUP BY type
SORT type ASC
```

## 关系层（本体构件 2：关系）

关系通过 `[[]]` 双向链接 + frontmatter 谓词标注实现。预定义关系谓词：
`belongs_to` / `tagged` / `covered_by` / `has_metric` / `valued_at` / `involves` / `affects` / `matches` / `authored_by` / `triggered_by`

## 动态层（本体构件 3-4）

| 构件 | 文件夹 | 说明 |
|---|---|---|
| **逻辑规则** | [[logic/]] | schema 约束/校验/状态机/推断规则 |
| **动作** | [[actions/]] | CRUD/状态流转/链接维护/审计快照 |

## 质量门（Curated）

| 层 | 文件夹 | 作用 |
|---|---|---|
| **待审** | [[inbox/]] | LLM 抽取实体先进此，带 confidence + source + quality_score，审核通过才进正式区 |
| **审查** | [[reviews/]] | ReAct Agent 定期体检报告（8 项检查） |

> 不直接灌入是知识图谱健康的第一道防线。详见 [[inbox/index]] 质量四维度。

### 战法卡统计

```dataview
TABLE name AS "战法", edge_family AS "edge 家族"
FROM "strategies"
WHERE type = "strategy"
SORT name ASC
```

### 项目决策统计

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "spec"
SORT number ASC
```

---

## 使用说明

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

---

## 与项目代码的关系

| 层 | 位置 | 职责 |
|---|---|---|
| 代码契约层 | `backend/models/` | Pydantic 模型定义数据结构（Quote/Valuation/Financials…） |
| 数据流层 | `backend/` + `ARCHITECTURE.md` | 数据采集/加工/存储管线 |
| 战法执行层 | `backend/strategies/` | 战法 match 逻辑 + cards/ 战法卡 |
| **语义层（本 vault）** | `knowledge/` | 实体关系导航、研报笔记、投研知识沉淀 |
| 决策记录层 | `specs/` | SDD spec 决策文档 |

本 vault 不复制代码逻辑，只做**知识表征**：一个股票笔记链接它的行业、研报、财务、估值、龙虎榜、相关战法，形成可回溯的投研上下文。代码改了模型字段，来这里改对应模板的 frontmatter 即可。
