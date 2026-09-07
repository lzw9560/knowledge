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

待补充


## ⏱ 限流策略

- API key 隔离
- 待补：具体 QPS 限制


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

- 🔧 [[10_Reference/tech-learning/concepts/data-contract|数据契约]] — 宏观 7 系列（DEC-002 定稿）由 Pydantic 契约层统一形状
- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — FRED 宏观无降级，失败标灰
- 🔧 [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 宏观数据低频，入缓存降低请求
