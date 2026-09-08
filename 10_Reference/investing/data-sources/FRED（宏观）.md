---
type: data_source
name: FRED（宏观）
layer: 5
endpoint: api.stlouisfed.org
rate_limit: API key 隔离
fallback: 无
compliance: ok
provides: [宏观指标]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：FRED（宏观）  **层级**：L5
> **接口**：`api.stlouisfed.org`
> **限流**：`API key 隔离`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 观测日期（YYYY-MM-DD） |
| value | float | 指标值（None=缺失观测） |
| series_id | str | FRED 序列 ID |
| us_10y_yield | float | 美债10Y收益率（DGS10） |
| dxy | float | 贸易加权美元指数（DTWEXBGS） |
| us_fed_funds_eff | float | 有效联邦基金利率（DFF） |
| us_10y2y_spread | float | 美债10Y-2Y利差（T10Y2Y） |
| usd_cny | float | 人民币兑美元现汇（DEXCHUS） |
| wti_crude | float | WTI原油即期（DCOILWTICO） |
| lme_copper | float | LME铜价（PCOPPUSDM） |

> 数据源：`api.stlouisfed.org/fred/series/observations`（独立 requests 通道，非 em_get）
> 7 宏观序列均日频，T 开盘前（S2）可得

## ⏱ 限流策略

- API key 隔离
- FRED 免费 API key 限 120 次/分钟（官方文档），本源低频调用不触顶


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

- **出链**：10 个 · **入链**：0 个

## 🔧 技术栈

- 🔧 [[10_Reference/tech-learning/concepts/数据契约|数据契约]] — 宏观 7 系列（DEC-002 定稿）由 Pydantic 契约层统一形状
- 🔧 [[10_Reference/tech-learning/concepts/优雅降级|优雅降级]] — FRED 宏观无降级，失败标灰
- 🔧 [[10_Reference/tech-learning/concepts/缓存策略|缓存策略]] — 宏观数据低频，入缓存降低请求
