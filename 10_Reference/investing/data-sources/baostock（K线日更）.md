---
type: data_source
name: baostock（K线日更）
layer: 4
endpoint: bbaostock.com
rate_limit: 无
fallback: S090 kline_refresh
compliance: ok
provides: [K线日更, 5minK线]
projects: [vibe-research, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：baostock（K线日更）  **层级**：L4
> **接口**：`bbaostock.com`
> **限流**：`无`  **降级**：`S090 kline_refresh`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 交易日（YYYY-MM-DD） |
| time | str | 时间（5min K线，HH:MM:SS） |
| open | float | 开盘价（前复权 qfq） |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |
| volume | float | 成交量 |
| **peTTM** | float | **市盈率 TTM（2026-09-09 核实 w7go86zon：kline fields 自带，日频现成，不用自己算）** |
| **pbMRQ** | float | **市净率 MRQ（kline 自带）** |
| **psTTM** | float | **市销率 TTM（kline 自带）** |
| **pcfNcfTTM** | float | **市现率 TTM（kline 自带）** |
| **turn** | float | **换手率（kline 自带）** |
| isST | str | ST 标记（"0"/"1"） |

> 数据源：baostock `query_history_k_data_plus`（frequency=5/d，adjustflag=2 前复权 或 3 不复权）
> **2026-09-09 重大修正**：fields 自带 peTTM/pbMRQ/psTTM/pcfNcfTTM/turn 日频值——选股 capture 层直接用 kline 一次出 PE/PB/换手，不用跑 query_profit_data 44Q PIT（省 ~22hr）。caveat：kline peTTM 是 as-reported 按当日股本+close 算（可能 restated），pubDate PIT 锚点在 query_profit_data（仅深度回测验证需，S171 已停）。
> 单次 login（进程级幂等），无 IP 限制，免防封

## ⏱ 限流策略

- 无（baostock 证券宝，无 IP 限制，免防封）


## 🔄 降级链

- 无网络降级
- 任务级：由 `scheduled_tasks.py` 的 `kline_refresh`（S090）定时执行


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

- 🔧 [[10_Reference/tech-learning/concepts/优雅降级|优雅降级]] — K线日更失败时 S090 kline_refresh 降级
- 🔧 [[10_Reference/tech-learning/tools/uv包管理|uv]] — baostock Python 包由 uv 管理锁版本
- 🔧 [[10_Reference/tech-learning/concepts/缓存策略|缓存策略]] — 历史日 K 入缓存
