---
type: stock
code: 
name: 
market: A
industry: 
concept: 
list_date: 
st: false
pe_ttm: 
pb: 
market_cap: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 基本信息

- 代码：`code`
- 名称：
- 市场：`market`
- 上市日期：`list_date`
- ST：`st`

# 核心业务



# 财务速览

链接 [[metrics/]] 查看该股财务周期数据。

```dataview
TABLE period AS "周期", revenue AS "营收(亿)", net_profit AS "净利(亿)", roe AS "ROE%", gross_margin AS "毛利率%"
FROM "metrics"
WHERE type = "metric" AND code = this.code
SORT period DESC
```

# 估值

链接 [[valuations/]] 查看估值快照与历史分位。

```dataview
TABLE pe_ttm AS "PE(TTM)", pb AS "PB", peg AS "PEG", pe_percentile AS "PE分位%", pb_percentile AS "PB分位%"
FROM "valuations"
WHERE type = "valuation" AND code = this.code
SORT created DESC
LIMIT 1
```

# 相关研报

```dataview
TABLE title AS "标题", org AS "机构", researcher AS "分析师", publish_date AS "日期", rating_change AS "评级"
FROM "reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
```

# 龙虎榜

链接 [[dragon-tiger/]] 查看游资席位明细。

```dataview
TABLE date AS "日期", institution_net AS "机构净额", seats AS "席位"
FROM "dragon-tiger"
WHERE type = "dragon_tiger" AND code = this.code
SORT date DESC
```

# 相关事件

链接 [[events/]] 查看新闻/公告/涨停事件。

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
```

# 匹配战法

链接 [[strategies/]] 查看该股可能触发的战法。

> 手动标注或后续 LLM 推断填充。

- [[strategies/]]
