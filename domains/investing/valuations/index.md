# 估值 索引

> 个股估值快照与历史分位节点。对应 Pydantic 契约 `Valuation` + `ValuationPercentile`。每条记录链接其所属股票、历史估值序列、一致预期。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "股票代码", pe_ttm AS "PE(TTM)", pb AS "PB", peg AS "PEG", pe_percentile AS "PE分位%", pb_percentile AS "PB分位%", dividend_yield AS "股息率%"
FROM "valuations"
WHERE type = "valuation"
SORT code ASC, created DESC
```

## 关系

- belongs_to: [[stocks/]]（每条估值数据所属股票）
- pairs_with: [[metrics/]]（估值与财务配对看，PE = 股价 / EPS）
- consensus: [[reports/]]（一致预期 EPS 来自研报）
- sourced_from: [[data-sources/]]（估值数据来源）

## 新建实体

用 Templater 应用 `templates/valuation` 新建。模板 frontmatter 对应 `Valuation` + `ValuationPercentile` 字段（pe_ttm/pb/ps_ttm/pcf_ttm/dividend_yield/peg/forward_pe/consensus_eps/pe_percentile/pb_percentile）。
