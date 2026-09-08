---
type: concept
code: 
name: 
related_industry: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 概念信息
> **概念**：name  **关联行业**：related_industry  **成分股数**：0
> 
> **关联**：[[industries/]] · [[data-sources/]]

## 📊 概念概览



## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT market_cap DESC
LIMIT 20
```

## 🔄 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

- **发酵期**：
- **高潮期**：
- **退潮期**：

## 💰 资金流向

- 数据源：[[data-sources/eastmoney-push2|东财 push2]]

## 📰 相关研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  org AS "机构",
  publish_date AS "日期"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
LIMIT 10
```

## ⚡ 近期事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```

## 🔗 关联

- **行业**：[[industries/]]
- **数据源**：[[data-sources/]]
- **出链**：0 个 · **入链**：0 个
