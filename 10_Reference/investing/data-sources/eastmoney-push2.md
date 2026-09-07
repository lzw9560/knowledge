---
type: data_source
name: 东财 push2
layer: 2
endpoint: push2/api.eastmoney.com
rate_limit: em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）
fallback: 熔断器+push2delay降级
compliance: ok
provides: [行情, K线, 分时]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 push2  **层级**：L2
> **接口**：`push2/api.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 统一走 `em_get()`，串行限流：默认 1.0s + 抖动 0.1~0.5s，QPS≤2
- 复用 `requests.Session`（Keep-Alive）
- 直连会话 `trust_env=False` 忽略 HTTP_PROXY
- 直连优先、失败降级系统代理（auto 模式短超时 8s 不重试，成功 latch direct，失败 latch proxy）
- `VR_DATA_PROXY=1` 强制代理


## 🔄 降级链

- 熔断器 `circuit_breaker.get_breaker("eastmoney")`：快速失败不重复重试
- push2 失败 → `push2delay`（延时行情），latch 整进程复用
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

- 🔧 [[tech-learning/concepts/circuit-breaker|熔断器]] — circuit_breaker.get_breaker("eastmoney") 快速失败不重复重试
- 🔧 [[tech-learning/concepts/rate-limiting|限流]] — em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）防被东财风控识别为机器流量
- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — push2 失败 → push2delay（延时行情）→ 路由级缓存的多级回退
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — cache_response(ttl) 路由级缓存
