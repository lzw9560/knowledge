---
type: index
code: 
name: 
market: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 📊 指数
> **代码**：code  **名称**：name  **市场**：market
> 
> **关联**：[[stocks/]] · [[data-sources/]]

## 📋 指数概览

- 指数代码：`code`
- 名称：name
- 市场：`market`

## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  industry AS "行业",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(indices, this.code)
SORT market_cap DESC
LIMIT 30
```

## 📈 近期走势

> 链接 K 线数据源或粘贴关键点位。

## 🔗 关联

- **数据源**：[[data-sources/eastmoney-push2|东财 push2]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
