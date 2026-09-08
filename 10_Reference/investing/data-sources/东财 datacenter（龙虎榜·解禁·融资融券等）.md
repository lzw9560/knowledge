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
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：东财 datacenter（龙虎榜/解禁/融资融券等）  **层级**：L2
> **接口**：`datacenter-web.eastmoney.com`
> **限流**：`em_get 限流 QPS≤2`  **降级**：`熔断器+push2delay降级`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 交易日期（YYYY-MM-DD） |
| rzye | float | 融资余额（融资融券） |
| rzmre | float | 融资买入额 |
| rzche | float | 融资偿还额 |
| rqye | float | 融券余额 |
| rqmcl | float | 融券卖出量 |
| rzrqye | float | 两融合计余额 |
| price | float | 成交价（大宗交易） |
| close | float | 收盘价（大宗交易） |
| premium_pct | float | 折溢价率（%，大宗交易） |
| vol | float | 成交量（大宗交易） |
| amount | float | 成交额（大宗交易） |
| buyer | str | 买方营业部 |
| seller | str | 卖方营业部 |
| holder_num | int | 股东户数 |
| change_ratio | float | 户数环比变化 |
| avg_shares | float | 户均持股 |
| bonus_rmb | float | 每股派息（税前，分红） |
| transfer_ratio | float | 每10股转增（分红） |
| bonus_ratio | float | 每10股送股（分红） |
| plan | str | 分红进度 |
| reason | str | 龙虎榜上榜原因 |
| net_buy | float | 龙虎榜净买入（万元） |
| turnover | float | 龙虎榜换手率 |
| type | str | 解禁类型（限售解禁） |
| shares | float | 解禁股数 |
| able_shares | float | 实际可流通股数 |
| ratio | float | 解禁比例 |
| main_net | float | 主力净流入（资金流，元） |
| small_net | float | 小单净流入 |
| mid_net | float | 中单净流入 |
| large_net | float | 大单净流入 |
| super_net | float | 超大单净流入 |
| source | str | 数据来源标识（eastmoney/sina_fallback） |

> 数据源：`datacenter-web.eastmoney.com` 统一查询（reportName：RPTA_WEB_RZRQ_GGMX/RPT_DATA_BLOCKTRADE/RPT_HOLDERNUMLATEST/RPT_SHAREBONUS_DET/RPT_DAILYBILLBOARD_DETAILSNEW/RPT_LIFT_STAGE）

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

- 🔧 10_Reference/tech-learning/concepts/熔断器|熔断器]] — datacenter（龙虎榜/解禁/融资融券）采集加熔断
- 🔧 10_Reference/tech-learning/concepts/限流|限流]] — 共用 em_get QPS≤2 限流
- 🔧 10_Reference/tech-learning/concepts/缓存策略|缓存策略]] — 低频数据入缓存降低重复请求
