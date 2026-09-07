---
type: data_source
name: baostock（K线日更）
layer: 4
endpoint: bbaostock.com
rate_limit: 无
fallback: S090 kline_refresh
compliance: ok
provides: [K线日更]
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

待补充


## ⏱ 限流策略

- 无（待补：是否有上游限流）


## 🔄 降级链

- 无网络降级
- 任务级：由 `scheduled_tasks.py` 的 `kline_refresh`（S090）定时执行


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

- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — K线日更失败时 S090 kline_refresh 降级
- 🔧 [[10_Reference/tech-learning/tools/uv|uv 包管理]] — baostock Python 包由 uv 管理锁版本
- 🔧 [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 历史日 K 入缓存
