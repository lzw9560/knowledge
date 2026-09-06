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
---

# 东财 datacenter（龙虎榜/解禁/融资融券等）

## 提供字段
- 龙虎榜（`dragon_tiger_board`）
- 解禁数据
- 融资融券（`margin_trading`）
- 大宗交易（`block_trade`）
- 股东户数
- 分红
- 资金流 120 日（`stock_fund_flow_120d`）
- 行业排名
- 概念板块（`concept_blocks`）

## 限流策略
- 统一走 `em_get()`，QPS≤2（同 push2）
- 复用 `requests.Session`、直连优先失败降级代理

## 降级链
- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`

## 相关实体
- 喂给实体类型：[[dragon-tiger/]] [[events/]] [[metrics/]]
- 对应代码：`backend/data/sources/astock.py` → `dragon_tiger_board`、`margin_trading`、`block_trade`、`stock_fund_flow_120d`、`concept_blocks`

## 相关 spec
- [[specs/]] 后端数据层迁移 / 龙虎榜接入 / 融资融券
