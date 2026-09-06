---
type: valuation
code: 
pe_ttm: 
pb: 
ps_ttm: 
pcf_ttm: 
dividend_yield: 
peg: 
forward_pe: 
consensus_eps: 
pe_percentile: 
pb_percentile: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 估值快照

- 股票代码：`code`（链接 [[stocks/]]）
- PE(TTM)：`pe_ttm`
- PB：`pb`
- PS(TTM)：`ps_ttm`
- PCF(TTM)：`pcf_ttm`
- 股息率：`dividend_yield`%
- PEG：`peg`
- 远期 PE：`forward_pe`

# 历史分位

- PE 历史分位：`pe_percentile`%
- PB 历史分位：`pb_percentile`%

> 分位口径待统一（3 年/5 年/全上市以来）。建议在 `data-sources` 的估值源笔记里记录口径。

# 一致预期

- 一致预期 EPS：`consensus_eps`

# 所属股票

```dataview
TABLE name AS "名称", industry AS "行业", market_cap AS "市值"
FROM "stocks"
WHERE type = "stock" AND code = this.code
```

# 历史估值序列

```dataview
TABLE created AS "日期", pe_ttm AS "PE(TTM)", pb AS "PB", pe_percentile AS "PE分位%"
FROM "valuations"
WHERE type = "valuation" AND code = this.code
SORT created DESC
```
