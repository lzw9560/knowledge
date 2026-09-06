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
