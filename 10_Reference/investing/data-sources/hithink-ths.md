---
type: data_source
name: 同花顺 THS（一致预期/涨停揭秘）
layer: 4
endpoint: basic.10jqka.com.cn
rate_limit: 直连
fallback: 无
compliance: ok
provides: [一致预期, 涨停揭秘]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：同花顺 THS（一致预期/涨停揭秘）  **层级**：L4
> **接口**：`basic.10jqka.com.cn`
> **限流**：`直连`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| pe_ttm | float | 滚动市盈率（估值快照） |
| pe_mrq | float | 最近报告期市盈率 |
| pb_mrq | float | 最近报告期市净率 |
| ps_ttm | float | 滚动市销率（东财零供给唯一源） |
| pcf_ttm | float | 滚动市现率（东财零供给唯一源） |
| code | str | 股票代码（裸6位） |
| name | str | 股票名称 |
| rank | int | 飙升/热股榜排名 |
| heat | float | 热度值 |
| rank_change | int | 排名变动 |
| rank_trend | str | 排名趋势 |
| auction_price | float | 集合竞价价 |
| auction_pct | float | 竞价涨跌幅 vs 昨收 |
| auction_volume | float | 竞价量 |
| auction_amount | float | 竞价额 |
| auction_unmatched | float | 未匹配量 |
| auction_volume_ratio | float | 竞价量比（§44 关键信号） |
| auction_turnover_pct | float | 竞价换手 |
| float_market_cap | float | 流通市值 |
| lbc | int | 连板数（涨停池） |

> 数据源：`fuyao.aicubes.cn`（hithink-finance，urllib 直连 + envelope 转译 + 有界重试）
> §44 口径：PS/PCF 是东财零供给的唯一源，无需 cross_validate 仲裁

## ⏱ 限流策略

- 直连
- 源端未明示封禁行为，低频调用直连


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

- 🔧 [[tech-learning/concepts/data-contract|数据契约]] — 一致预期/涨停揭秘数据由契约层统一形状（S104 唯一源）
- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — hithink 无降级，失败标灰
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — 低频数据入缓存
