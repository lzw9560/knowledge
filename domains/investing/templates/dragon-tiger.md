---
type: dragon_tiger
code: 
date: 
institution_net: 
seats: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 席位明细

- 股票代码：`code`（链接 [[stocks/]]）
- 日期：`date`
- 机构净额（亿）：`institution_net`
- 席位：`seats`

# 游资画像

> 记录上榜席位的游资风格：一日游/趋势/接力/量化。可链接到 [[strategies/]] 的对应战法。

# 所属股票

```dataview
TABLE name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND code = this.code
```

# 相关事件

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(codes, this.code) AND date = this.date
SORT date DESC
```

# 近期同席位个股

> 查该游资席位近期还上过哪些股——手动维护或后续 LLM 推断。
