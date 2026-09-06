---
type: concept
code: 
name: 
related_industry: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 概念概览

- 概念代码：`code`
- 名称：
- 关联行业：`related_industry`

# 成分股

```dataview
TABLE code AS "代码", name AS "名称"
FROM "stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT code ASC
```

# 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

# 资金流向



# 近期事件

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```

# 相关研报

```dataview
TABLE title AS "标题", org AS "机构", publish_date AS "日期"
FROM "reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
```
