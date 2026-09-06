---
type: report
code: 
title: 
org: 
researcher: 
publish_date: 
report_type: 
rating_change: 
target_price: 
eps_forecast: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 报告摘要

- 标题：`title`
- 机构：`org`
- 分析师：`researcher`（链接 [[analysts/]]）
- 发布日期：`publish_date`
- 报告类型：`report_type`

# 核心观点



# 覆盖标的

链接 [[stocks/]] 查看个股详情。

- 代码：`code`

```dataview
TABLE name AS "名称", industry AS "行业", market_cap AS "市值"
FROM "stocks"
WHERE type = "stock" AND code = this.code
```

# 分析师

链接 [[analysts/]] 查看该分析师的其他研报。

```dataview
TABLE title AS "标题", publish_date AS "日期", rating_change AS "评级"
FROM "reports"
WHERE type = "report" AND researcher = this.researcher AND title != this.title
SORT publish_date DESC
```

# 评级与目标价

- 评级变动：`rating_change`
- 目标价：`target_price`
- EPS 预测：`eps_forecast`
