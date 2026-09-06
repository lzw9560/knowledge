---
type: event
date: 
event_type: 
codes: 
source: 
summary: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 事件概述

- 日期：`date`
- 类型：`event_type`（新闻/公告/涨停/跌停/停牌/复牌）
- 来源：`source`
- 摘要：`summary`

# 影响标的

链接 [[stocks/]] 查看个股详情。

- 代码列表：`codes`

```dataview
TABLE name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND contains(this.codes, code)
SORT code ASC
```

# 触发战法

> 该事件可能触发哪些战法？手动标注或后续 LLM 推断。

- [[strategies/]]

# 来源

- 原始链接：
- 抓取时间：`created`
