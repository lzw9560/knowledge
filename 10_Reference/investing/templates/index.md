---
type: index
code: 
name: 
market: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 指数概览

- 指数代码：`code`
- 名称：
- 市场：`market`

# 成分股

```dataview
TABLE code AS "代码", name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND contains(indices, this.code)
SORT code ASC
```

# 近期走势

> 链接 K 线数据源或粘贴关键点位。
