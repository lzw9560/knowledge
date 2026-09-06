---
type: data_source
name: 东财 reportapi（研报）
layer: 2
endpoint: reportapi.eastmoney.com
rate_limit: em_get 限流 QPS≤2
fallback: 熔断器+push2delay降级
compliance: ok
provides: [研报标题, 机构, 评级, 日期, 一致预期EPS]
created: 2026-09-06
---

# 东财 reportapi（研报）

## 提供字段
- 个股近期研报（标题/机构/评级/日期）
- 机构一致预期 EPS
- 前向 PE/PEG/PE 消化年数（待补：具体字段需对照 `astock.full_valuation`）

## 限流策略
- 统一走 `em_get()`，QPS≤2（同 push2）
- 复用 `requests.Session`、直连优先失败降级代理

## 降级链
- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`

## 相关实体
- 喂给实体类型：[[reports/]] [[valuations/]]
- 对应代码：`backend/data/sources/astock.py` → `eastmoney_reports`、`full_valuation`、`valuation_percentile`、`profit_forecast`
- MCP 暴露：`query_reports`、`query_valuation`

## 相关 spec
- [[specs/]] 后端数据层迁移 / 机构一致预期
