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

| 字段 | 类型 | 说明 |
|---|---|---|
| code | str | 股票代码 |
| name | str | 股票名称 |
| latest | float | 最新价（五档买卖盘） |
| prev_close | float | 昨收价 |
| buy | list | 五档买盘 [{level,price,vol}] |
| sell | list | 五档卖盘 [{level,price,vol}] |
| pct | float | 涨跌幅（成交额榜） |
| amount | float | 成交额（元，成交额榜） |
| mcap | float | 总市值（元） |
| float_cap | float | 流通市值（元） |
| industry | str | 所属行业 |
| net | float | 行业板块主力净额（亿） |
| inflow | float | 行业流入额（亿） |
| outflow | float | 行业流出额（亿） |
| firms | int | 行业涨跌家数合计 |
| change_pct | float | 板块涨跌幅（概念归属） |
| lead_stock | str | 板块领涨股 |
| concept | str | 热门概念名（hot_concepts） |
| bk | str | 概念板块代码 |
| hit | int | 热度命中次数 |

> 数据源：`push2/api.eastmoney.com` + push2delay 降级镜像

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

- [[10_Reference/investing/stocks/index|stocks/]]
- [[10_Reference/investing/reports/index|reports/]]
- [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]
- [[10_Reference/investing/metrics/index|metrics/]]
- [[10_Reference/investing/valuations/index|valuations/]]
- [[10_Reference/investing/events/index|events/]]

## 📜 关联 spec

- [[10_Reference/investing/specs/index|specs/]]

## 🔗 关联

- **出链**：11 个 · **入链**：0 个

## 🔧 技术栈

- 🔧 10_Reference/tech-learning/concepts/熔断器|熔断器]] — circuit_breaker.get_breaker("eastmoney") 快速失败不重复重试
- 🔧 10_Reference/tech-learning/concepts/限流|限流]] — em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s）防被东财风控识别为机器流量
- 🔧 10_Reference/tech-learning/concepts/优雅降级|优雅降级]] — push2 失败 → push2delay（延时行情）→ 路由级缓存的多级回退
- 🔧 10_Reference/tech-learning/concepts/缓存策略|缓存策略]] — cache_response(ttl) 路由级缓存
