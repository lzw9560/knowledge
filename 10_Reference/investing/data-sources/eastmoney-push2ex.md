---
type: data_source
name: 东财 push2ex（涨停四池）
layer: 2
endpoint: push2ex.eastmoney.com
rate_limit: em_get 限流 QPS≤2
fallback: 熔断器+push2delay降级
compliance: ok
provides: [涨停四池, 连板梯队, 封板率, 炸板率, 晋级率]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 push2ex（涨停四池）  **层级**：L2
> **接口**：`push2ex.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 统一走 `em_get()`，QPS≤2（同 push2）
- HTTP 缓存 24h（涨停四池专用）


## 🔄 降级链

- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`
- 复用 push2→push2delay 降级链


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

- 🔧 [[10_Reference/tech-learning/concepts/circuit-breaker|熔断器]] — 涨停四池采集加熔断，连续失败快速失败
- 🔧 [[10_Reference/tech-learning/concepts/rate-limiting|限流]] — 共用 em_get QPS≤2 限流防封
- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — push2ex 失败 → push2delay 降级
