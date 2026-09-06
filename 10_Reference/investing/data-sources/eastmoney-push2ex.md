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
---

# 东财 push2ex（涨停四池）

## 提供字段
- 涨停四池（首板/二板/三板/高度板）
- 连板梯队
- 封板率、炸板率、晋级率

## 限流策略
- 统一走 `em_get()`，QPS≤2（同 push2）
- HTTP 缓存 24h（涨停四池专用）

## 降级链
- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`
- 复用 push2→push2delay 降级链

## 相关实体
- 喂给实体类型：[[stocks/]] [[events/]]（涨停事件）
- 对应代码：`backend/data/sources/astock.py` → `em_zt_topic_pool`
- 聚合层：`market.py` → `_emotion`（涨停四池聚合为连板梯队/封板率/炸板率/晋级率）

## 相关 spec
- [[specs/]] 涨停四池接入 / market.py 情绪聚合
