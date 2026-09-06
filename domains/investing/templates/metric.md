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

# 财务摘要

- 股票代码：`code`（链接 [[stocks/]]）
- 报告期：`period`
- 营收（亿）：`revenue`
- 归母净利（亿）：`net_profit`
- EPS：`eps`
- BVPS：`bvps`
- 每股经营现金流：`op_cf_ps`

# 盈利能力

- ROE：`roe`%
- 毛利率：`gross_margin`%
- 净利率：`net_margin`%

# 趋势

```dataview
TABLE period AS "周期", revenue AS "营收(亿)", net_profit AS "净利(亿)", roe AS "ROE%", gross_margin AS "毛利率%"
FROM "metrics"
WHERE type = "metric" AND code = this.code
SORT period ASC
```

# 所属股票

```dataview
TABLE name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND code = this.code
```
