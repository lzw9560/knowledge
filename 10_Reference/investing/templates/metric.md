---
type: metric
code: 
period: 
revenue: 
net_profit: 
roe: 
gross_margin: 
net_margin: 
eps: 
bvps: 
op_cf_ps: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 💰 财务指标
> **股票**：`code`  **报告期**：period  **来源**：source
> **营收**：revenue  **净利**：net_profit  **EPS**：eps
> 
> **所属股票**：[[stocks/]]

## 📊 财务摘要

- 股票代码：`code`
- 报告期：`period`
- 营收（亿）：`revenue`
- 归母净利（亿）：`net_profit`
- EPS：`eps`
- BVPS：`bvps`
- 每股经营现金流：`op_cf_ps`

## 📈 盈利能力

- ROE：`roe`%
- 毛利率：`gross_margin`%
- 净利率：`net_margin`%

## 📉 趋势

```dataview
TABLE WITHOUT ID
  period AS "周期",
  revenue AS "营收(亿)",
  net_profit AS "净利(亿)",
  roe AS "ROE%",
  gross_margin AS "毛利率%"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND code = this.code
SORT period DESC
LIMIT 8
```

## 🔗 关联

- **所属股票**：[[stocks/]]
- **数据源**：[[data-sources/]]
- **出链**：0 个 · **入链**：0 个
