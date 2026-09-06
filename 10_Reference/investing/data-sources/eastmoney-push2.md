---
type: data_source
name: 东财 push2
layer: 2
endpoint: push2/api.eastmoney.com
rate_limit: em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）
fallback: 熔断器+push2delay降级
compliance: ok
provides: [行情, K线, 分时]
created: 2026-09-06
---

# 东财 push2

## 提供字段
- A 股实时行情（主源）
- K 线数据
- 分时数据
- 美港股/韩股行情（gstock.py 复用）

## 限流策略
- 统一走 `em_get()`，串行限流：默认 1.0s + 抖动 0.1~0.5s，QPS≤2
- 复用 `requests.Session`（Keep-Alive）
- 直连会话 `trust_env=False` 忽略 HTTP_PROXY
- 直连优先、失败降级系统代理（auto 模式短超时 8s 不重试，成功 latch direct，失败 latch proxy）
- `VR_DATA_PROXY=1` 强制代理

## 降级链
- 熔断器 `circuit_breaker.get_breaker("eastmoney")`：快速失败不重复重试
- push2 失败 → `push2delay`（延时行情），latch 整进程复用
- 路由级缓存 `cache_response(ttl)`

## 相关实体
- 喂给实体类型：[[stocks/]] [[valuations/]]
- 对应代码：`backend/data/sources/astock.py` `backend/data/sources/gstock.py`
- MCP 暴露：`query_quote`（A 股）、`query_global_stock`（美港股/韩股）

## 相关 spec
- [[specs/]] 后端数据层迁移 / em_get 限流策略 / 熔断器
