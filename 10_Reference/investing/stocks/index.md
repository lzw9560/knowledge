# 股票 索引

> 个股是投研知识图谱的核心节点。对应 Pydantic 契约 `Quote` + `CompanyInfo`，覆盖 A 股/美股/港股。每只股票链接其行业、研报、财务、估值、龙虎榜、相关事件、匹配战法。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "代码", name AS "名称", market AS "市场", industry AS "行业", pe_ttm AS "PE(TTM)", market_cap AS "市值"
FROM "stocks"
WHERE type = "stock"
SORT code ASC
```

## 关系

- belongs_to: [[industries/]]（每只股票属于一个证监会行业）
- tagged: [[concepts/]]（每只股票可被多个概念题材打标）
- covered_by: [[reports/]]（机构研报覆盖）
- financials: [[metrics/]]（财务周期数据）
- valued_by: [[valuations/]]（估值快照）
- appears_on: [[dragon-tiger/]]（龙虎榜上榜记录）
- triggers: [[events/]]（新闻/公告/涨停事件）
- matches: [[strategies/]]（匹配的战法）
- listed_in: [[indices/]]（宽基/行业指数成分）
- sourced_from: [[data-sources/]]（行情数据来源）

## 新建实体

用 Templater 应用 `templates/stock` 新建。模板会自动填入 YAML frontmatter（code/name/market/industry/pe_ttm/pb/market_cap 等）+ 正文骨架（基本信息/核心业务/财务速览/估值/相关研报/龙虎榜/相关事件/匹配战法）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/stock` 新建 股票 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "股票总数"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
