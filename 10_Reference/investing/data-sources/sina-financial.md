---
type: data_source
name: 新浪财经（财报三表）
layer: 4
endpoint: vip.stock.finance.sina.com.cn
rate_limit: urllib 直连
fallback: 无
compliance: ok
provides: [资产负债表, 利润表, 现金流量表]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：新浪财经（财报三表）  **层级**：L4
> **接口**：`vip.stock.finance.sina.com.cn`
> **限流**：`urllib 直连`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| 报告期 | str | 报告期日期（YYYY-MM-DD） |
| <科目> | str | 财务科目值（中文键，字符串） |
| <科目>_同比 | str | 科目同比变化 |

> 数据源：`quotes.sina.cn/cn/api/openapi.php/CompanyFinanceService.getFinanceReport2022`（urllib 直连）
> 三表 report_type：lrb（利润表）/ fzb（资产负债表）/ llb（现金流量表）
> 按 period 倒序，中文科目键 + 可选同比；fetch_merged_periods 合并三表产完整 FinancialPeriod

## ⏱ 限流策略

- urllib 直连
- 源端未明示封禁行为，低频调用直连


## 🔄 降级链

- 无


## 🔗 相关实体

- [[10_Reference/investing/stocks/index|stocks/]]
- [[10_Reference/investing/reports/index|reports/]]
- [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]
- [[10_Reference/investing/metrics/index|metrics/]]
- [[10_Reference/investing/valuations/index|valuations/]]
- [[10_Reference/investing/events/index|events/]]

## 📜 关联 spec

- [[10_Reference/investing/specs/index|specs/]]

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个

## 🔧 技术栈

- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — 新浪财报三表无降级，失败标灰
- 🔧 [[10_Reference/tech-learning/concepts/data-contract|数据契约]] — 财报三表数据由契约层统一形状
- 🔧 [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 财报低频数据入缓存
