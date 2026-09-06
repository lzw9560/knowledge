---
type: industry
code: 
name: 
source: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 行业概览

- 行业代码：`code`
- 名称：
- 分类来源：`source`（证监会/申万/中信）

# 成分股

```dataview
TABLE code AS "代码", name AS "名称", market_cap AS "市值"
FROM "stocks"
WHERE type = "stock" AND industry = this.name
SORT market_cap DESC
```

# 资金流向



# 相关概念

```dataview
TABLE name AS "概念名"
FROM "concepts"
WHERE type = "concept" AND related_industry = this.name
SORT name ASC
```

# 近期事件

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```

# 新建实体

用 Templater 应用 `templates/industry` 新建。
