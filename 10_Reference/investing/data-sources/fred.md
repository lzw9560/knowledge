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
