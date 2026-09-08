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
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 reportapi（研报）  **层级**：L2
> **接口**：`reportapi.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| title | str | 研报标题 |
| org | str | 研究机构名称 |
| rating | str | 评级 |
| ratingChange | str | 评级变动 |
| publish_date | str | 发布日期 |
| code | str | 个股代码 |
| industryCode | str | 行业代码 |
| info_code | str | 研报信息码（PDF 拼接用） |
| beginTime | str | 检索起始时间 |
| endTime | str | 检索结束时间 |

> 数据源：`reportapi.eastmoney.com/report/list`（qType=0 个股 / qType=1 行业）
> PDF 全文链接：`pdf.dfcfw.com/pdf/H3_{info_code}_1.pdf`

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

- 🔧 [[10_Reference/tech-learning/concepts/熔断器|熔断器]] — 研报接口采集加熔断
- 🔧 [[[[10_Reference/tech-learning/concepts/限流 — 共用 em_get QPS≤2 限流防封]]
- 🔧 [[10_Reference/tech-learning/concepts/缓存策略|缓存策略]] — 研报数据低频更新，入缓存降低请求
