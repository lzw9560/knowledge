---
type: data_source
name: 百度股市通（日K线）
layer: 4
endpoint: finance.pae.baidu.com
rate_limit: 不封IP
fallback: 无
compliance: ok
provides: [日K线]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：百度股市通（日K线）  **层级**：L4
> **接口**：`finance.pae.baidu.com`
> **限流**：`不封IP`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 交易日（YYYY-MM-DD） |
| open | float | 开盘价 |
| close | float | 收盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| volume | int | 成交量（股） |
| amount | float | 成交额 |
| ma5 | float | 5日均价 |
| ma10 | float | 10日均价 |
| ma20 | float | 20日均价 |

> 数据源：`finance.pae.baidu.com/selfselect/getstockquotation`（urllib 直连，不封 IP）
> 自带 ma5/ma10/ma20，免本地重算移动平均

## ⏱ 限流策略

- 不封 IP
- 直连


## 🔄 降级链

- 无


## 🔗 相关实体

- [[stocks/]]
- [[reports/]]
- [[dragon-tiger/]]
- [[metrics/]]
- [[valuations/]]
- [[events/]]

## 📜 关联 spec

- [[specs/]]

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个

## 🔧 技术栈

- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — 百度股市通日 K 线无降级，失败即标灰
- 🔧 [[tech-learning/concepts/data-contract|数据契约]] — 返回数据由 Pydantic 契约层统一形状
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — 日 K 入缓存
