---
type: analyst
name: 
org: 
coverage_count: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 覆盖领域



# 近期研报

```dataview
TABLE title AS "标题", code AS "标的", publish_date AS "日期", rating_change AS "评级", target_price AS "目标价"
FROM "reports"
WHERE type = "report" AND researcher = this.name
SORT publish_date DESC
```

# 机构

- 所属：`org`

# 历史评级胜率

> 手动跟踪或后续 LLM 推断填充：该分析师历史评级的后续涨跌统计。
