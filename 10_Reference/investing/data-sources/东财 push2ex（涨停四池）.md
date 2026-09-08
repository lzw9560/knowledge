
> [!info] 📡 数据源
> **名称**：东财 push2ex（涨停四池）  **层级**：L2
> **接口**：`push2ex.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| code | str | 股票代码（原始池含） |
| name | str | 股票名称 |
| lbc | int | 连板数 |
| zbc | int | 炸板次数 |
| hybk | str | 所属行业板块 |
| fbt | float | 首次封板时间（sort 字段） |

> 数据源：`push2ex.eastmoney.com` 端点 getTopicZTPool/getTopicZBPool/getTopicDTPool/getYesterdayZTPool
> ⚠️ 原始池含个股 code/name，仅供 market.py 聚合成无个股的短线情绪指标，切勿直接接 API/UI（破零标的红线）

## ⏱ 限流策略

- 统一走 `em_get()`，QPS≤2（同 push2）
- HTTP 缓存 24h（涨停四池专用）


## 🔄 降级链

- 熔断器 `circuit_breaker.get_breaker("eastmoney")`
- 路由级缓存 `cache_response(ttl)`
- 复用 push2→push2delay 降级链


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

- 🔧 H_Reference/tech-learning/concepts/熔断器|熔断器]] — 涨停四池采集加熔断，连续失败快速失败
- 🔧 H_Reference/tech-learning/concepts/限流|限流]] — 共用 em_get QPS≤2 限流防封
- 🔧 H_Reference/tech-learning/concepts/优雅降级|优雅降级]] — push2ex 失败 → push2delay 降级
