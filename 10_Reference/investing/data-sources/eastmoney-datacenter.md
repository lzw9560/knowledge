---
type: data_source
name: 东财 datacenter（龙虎榜/解禁/融资融券等）
layer: 2
endpoint: datacenter-web.eastmoney.com
rate_limit: em_get 限流 QPS≤2
fallback: 熔断器+push2delay降级
compliance: ok
provides: [龙虎榜, 解禁, 融资融券, 大宗交易, 股东户数, 分红, 资金流, 行业排名]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 datacenter（龙虎榜/解禁/融资融券等）  **层级**：L2
> **接口**：`datacenter-web.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 统一走 `em_get()`，QPS≤2（同 push2）
- 复用 `requests.Session`、直连优先失败降级代理


## 🔄 降级链

- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`


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

- 🔧 [[../../tech-learning/concepts/circuit-breaker|熔断器]] — datacenter（龙虎榜/解禁/融资融券）采集加熔断
- 🔧 [[../../tech-learning/concepts/rate-limiting|限流]] — 共用 em_get QPS≤2 限流
- 🔧 [[../../tech-learning/concepts/caching-strategy|缓存策略]] — 低频数据入缓存降低重复请求
