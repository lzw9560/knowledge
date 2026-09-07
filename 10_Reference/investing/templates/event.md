---
type: event
date: 
event_type: 
codes: 
source: 
summary: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] ⚡ 事件
> **日期**：date  **类型**：event_type  **来源**：source
> **摘要**：summary
> 
> **影响标的数**：`=(length(split(this.codes, ",")))`

## 📋 事件概述

- 日期：`date`
- 类型：`event_type`（新闻/公告/涨停/跌停/停牌/复牌）
- 来源：`source`
- 摘要：`summary`

## 🎯 影响标的

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  industry AS "行业"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(this.codes, code)
SORT code ASC
LIMIT 30
```

## ⚔️ 触发战法

> 该事件可能触发哪些战法？手动标注或后续 LLM 推断。

- [[strategies/]]

## 📰 连板梯队

> 涨停事件记录连板梯队（首板/2连板/3连板…）。

## 🔗 关联

- **数据源**：[[data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
