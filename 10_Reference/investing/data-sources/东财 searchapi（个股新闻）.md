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
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 searchapi（个股新闻）  **层级**：L2
> **接口**：`searchapi.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 公告日期（YYYY-MM-DD） |
| title | str | 公告标题 |
| type | str | 公告类型/栏目 |
| url | str | 公告详情链接 |
| Code | str | 搜索结果代码（搜索接口） |
| Name | str | 搜索结果名称 |
| MktNum | int | 市场编号（搜索接口） |

> 数据源：`searchapi.eastmoney.com/api/suggest/get`（搜索） + `np-anotice-stock.eastmoney.com/api/security/ann`（公告）

## ⏱ 限流策略

- 统一走 `em_get()`，QPS≤2（同 push2）
- 复用 `requests.Session`、直连优先失败降级代理


## 🔄 降级链

- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`


## 🔗 相关实体

- [[10_Reference/investing/stocks/index|stocks/]]
- [[10_Reference/investing/reports/index|reports/]]
- [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]
- [[10_Reference/investing/metrics/index|metrics/]]
- [[10_Reference/investing/valuations/index|valuations/]]
- [[10_Reference/investing/events/index|events/]]

## 📜 关联 spec

- [[10_Reference/investing/specs/index|specs/]]

## 🔗 关联

- **出链**：10 个 · **入链**：0 个

## 🔧 技术栈

- 🔧 10_Reference/tech-learning/concepts/熔断器|[[熔断器]] — 个股新闻接口采集加熔断
- 🔧 10_Reference/tech-[[learning/concepts/限流|限流]] — 共用 em_get QPS≤2 限流
- 🔧 10_Reference/tech-learning/concepts/优雅降级|[[优雅降级]] — 新闻缺失时标灰不臆造
