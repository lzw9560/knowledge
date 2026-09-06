---
type: strategy
name: 
edge_family: 
match_conditions: 
entry_conditions: 
exit_conditions: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 战法逻辑

- 战法名：`name`
- edge 家族：`edge_family`（动量溢价/事件溢价/均值回归/待分类）
- match 条件：`match_conditions`

# 入场条件

`entry_conditions`

# 出场条件

`exit_conditions`

# 历史战绩

> 胜率/盈亏比/样本量。来源标注。n<30 标注"探索性"。

# 匹配股票

```dataview
TABLE code AS "代码", name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND contains(matched_strategies, this.name)
SORT code ASC
```

# 关联事件

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(triggered_strategies, this.name)
SORT date DESC
LIMIT 10
```

# 来源 spec

> 该战法的 match 逻辑对应的 SDD spec 编号。

- [[specs/]]
