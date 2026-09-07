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

> [!info] 📰 研报
> **标题**：title  **机构**：org  **日期**：publish_date
> **分析师**：researcher  **评级**：report_type  **目标价**：target_price
> 
> **覆盖标的**：[[stocks/]]

## 📋 报告摘要

- 标题：`title`
- 机构：`org`
- 分析师：`researcher`（[[analysts/]]）
- 发布日期：`publish_date`
- 报告类型：`report_type`

## 💡 核心观点



## 🎯 覆盖标的

```dataview
TABLE WITHOUT ID
  name AS "名称",
  industry AS "行业",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND code = this.code
```

## 👤 分析师其他研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  publish_date AS "日期",
  rating_change AS "评级"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND researcher = this.researcher AND title != this.title
SORT publish_date DESC
LIMIT 10
```

## 📊 评级与目标价

- 评级变动：`rating_change`
- 目标价：`target_price`
- EPS 预测：`eps_forecast`

## 🔗 关联

- **数据源**：[[data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
