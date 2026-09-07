# 财务指标 索引

> 个股财务周期数据节点。对应 Pydantic 契约 `Financials` + `FinancialPeriod`。每条记录链接其所属股票、趋势、盈利能力。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "股票代码", period AS "报告期", revenue AS "营收(亿)", net_profit AS "净利(亿)", roe AS "ROE%", gross_margin AS "毛利率%", eps AS "EPS"
FROM "metrics"
WHERE type = "metric"
SORT code ASC, period DESC
```

## 关系

- belongs_to: [[stocks/]]（每条财务数据所属股票）
- pairs_with: [[valuations/]]（财务与估值配对看）
- sourced_from: [[data-sources/]]（财务数据来源，如东方财富/同花顺）

## 新建实体

用 Templater 应用 `templates/metric` 新建。模板 frontmatter 对应 `Financials` 字段（revenue/net_profit/roe/gross_margin/net_margin/eps/bvps/op_cf_ps）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/metric` 新建 财务指标 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "财务指标总数"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
