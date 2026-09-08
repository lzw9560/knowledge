---
type: dragon_tiger
code: 
date: 
institution_net: 
seats: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 🐉 龙虎榜
> **股票**：`code`  **日期**：date  **机构净额**：institution_net
> **席位**：seats
> 
> **关联**：[[stocks/]] · [[events/]] · [[strategies/]]

## 📊 席位明细

- 股票代码：`code`（[[stocks/]]）
- 日期：`date`
- 机构净额（亿）：`institution_net`
- 席位：`seats`

## 🎭 游资画像

> 记录上榜席位的游资风格：一日游/趋势/接力/量化。可链接到 [[strategies/]] 的对应战法。

## 📈 所属股票

```dataview
TABLE WITHOUT ID
  name AS "名称",
  industry AS "行业"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND code = this.code
```

## ⚡ 相关事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code) AND date = this.date
SORT date DESC
LIMIT 5
```

## 🔗 关联

- **数据源**：[[data-sources/]]
- **出链**：0 个 · **入链**：0 个
