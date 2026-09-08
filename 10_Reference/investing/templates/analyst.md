---
type: analyst
name: 
org: 
coverage_count: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 👤 分析师
> **姓名**：name  **机构**：org  **覆盖数**：coverage_count
> 
> **关联**：[[reports/]] · [[stocks/]]

## 📋 覆盖领域



## 📰 近期研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  code AS "标的",
  publish_date AS "日期",
  rating_change AS "评级",
  target_price AS "目标价"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(researcher, this.name) AND org = this.org
SORT publish_date DESC
LIMIT 10
```

## 🏢 机构

- 所属：`org`

## 📊 历史评级胜率

> 手动跟踪或后续 LLM 推断填充：该分析师历史评级的后续涨跌统计。

## 🔗 关联

- **研报**：[[reports/]]
- **覆盖标的**：[[stocks/]]
- **数据源**：[[data-sources/]]
- **出链**：0 个 · **入链**：0 个
