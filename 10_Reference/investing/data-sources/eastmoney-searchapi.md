---
type: data_source
name: 东财 searchapi（个股新闻）
layer: 2
endpoint: searchapi.eastmoney.com
rate_limit: em_get 限流 QPS≤2
fallback: 熔断器+push2delay降级
compliance: ok
provides: [个股新闻标题, 时间, 来源]
created: 2026-09-06
---

# 东财 searchapi（个股新闻）

## 提供字段
- 个股近期新闻（标题/时间/来源）

## 限流策略
- 统一走 `em_get()`，QPS≤2（同 push2）
- 复用 `requests.Session`、直连优先失败降级代理

## 降级链
- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`

## 相关实体
- 喂给实体类型：[[events/]] [[stocks/]]
- 对应代码：`backend/data/sources/astock.py` → `stock_news`
- MCP 暴露：`query_news`

## 相关 spec
- [[specs/]] 后端数据层迁移 / 个股新闻接入
