---
type: data_source
name: worldmonitor（全球宏观 MCP）
layer: 5
endpoint: MCP 远程
rate_limit: 无
fallback: 无
compliance: ok
provides: [全球宏观指标]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：worldmonitor（全球宏观 MCP）  **层级**：L5
> **接口**：`MCP 远程`
> **限流**：`无`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| symbol | str | 商品/外汇代码（市场数据） |
| price | float | 最新价 |
| change_pct | float | 涨跌幅（%） |
| currency | str | 币种 |
| country | str | 国家名（CII 31国） |
| cii | float | 国家不稳定指数 |
| trend | str | 趋势 |
| title | str | 资讯/聚类标题 |
| summary | str | 摘要 |
| category | str | 资讯分类 |
| ts | int | 时间戳 |
| bdi | float | 波罗的海干散货指数 |
| stress_indicators | dict | 供应链压力指标 |
| name | str | 热点名称 |
| level | str | 热点升级级别 |

> 数据源：`worldmonitor.app/mcp`（MCP JSON-RPC，streamable HTTP，11 fetcher）
> 聚合 65+ 外部源、500+ 资讯、CII 31国不稳定指数、Finance Radar、跨源关联
> 合成分标注 source="worldmonitor_composite"（只作输入之一，不作唯一依据）

## ⏱ 限流策略

- MCP 远程调用
- 无（源端无明示限流，MCP 远程调用）


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

- 🔧 [[10_Reference/tech-learning/concepts/data-contract|数据契约]] — 全球宏观决策因子由契约层统一形状（S020 接入）
- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — MCP 远程无降级，失败标灰
- 🔧 [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 宏观决策因子低频，入缓存
