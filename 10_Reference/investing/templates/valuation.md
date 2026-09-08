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

> [!info] 📈 估值快照
> **股票**：`code`  **PE(TTM)**：pe_ttm  **PB**：pb  **PEG**：peg
> **PE 分位**：pe_percentile%  **PB 分位**：pb_percentile%
> 
> **所属股票**：[[stocks/]]

## 💰 估值指标

- 股票代码：`code`
- PE(TTM)：`pe_ttm`
- PB：`pb`
- PS(TTM)：`ps_ttm`
- PCF(TTM)：`pcf_ttm`
- 股息率：`dividend_yield`%
- PEG：`peg`
- 远期 PE：`forward_pe`

## 📊 历史分位

- PE 历史分位：`pe_percentile`%
- PB 历史分位：`pb_percentile`%

> 分位口径待统一（3 年/5 年/全上市以来）。建议在 `data-sources` 的估值源笔记里记录口径。

## 📋 一致预期

- 一致预期 EPS：`consensus_eps`

## 📉 历史估值序列

```dataview
TABLE WITHOUT ID
  created AS "日期",
  pe_ttm AS "PE(TTM)",
  pb AS "PB",
  pe_percentile AS "PE分位%",
  pb_percentile AS "PB分位%"
FROM "10_Reference/investing/valuations"
WHERE type = "valuation" AND code = this.code
SORT created DESC
LIMIT 10
```

## 🔗 关联

- **所属股票**：[[stocks/]]
- **数据源**：[[data-sources/]]
- **出链**：0 个 · **入链**：0 个
