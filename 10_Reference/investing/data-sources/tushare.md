---
type: data_source
name: Tushare
layer: 3
endpoint: api.tushare.pro
rate_limit: 积分制（免费 5000 积分，高级需付费）
fallback: 无
compliance: ok
provides: [A股行情, 财务, 指数, 期货, 基金, 可转债]
projects: [a-plate-sentinel]
origin_project: a-plate-sentinel
created: 2026-09-07
last_synced: 2026-09-07
---

> [!info] 📡 数据源
> **名称**：Tushare  **层级**：L3
> **接口**：`api.tushare.pro`
> **限流**：`积分制（免费 5000 积分，高级需付费）`  **降级**：`无`

## 📋 提供字段

- A 股实时/历史行情（日线/分钟线）
- 财务三表（资产负债/利润/现金流量）
- 指数行情（沪深300/中证500 等宽基与行业指数）
- 龙虎榜明细（席位买卖明细，席位标签引擎核心输入）
- 涨跌停池（情绪看板核心输入）
- 期货/基金/可转债行情


## ⏱ 限流策略

- 积分制：免费 5000 积分，按接口积分消耗扣减
- 高级接口（如 Tick、分笔、龙虎榜明细）需更高积分
- 付费提升积分上限可解锁更多接口与更高频率


## 🔄 降级链

- 降级：`无`


## 🔗 相关实体

- [[stocks/]]
- [[reports/]]
- [[dragon-tiger/]]
- [[metrics/]]
- [[valuations/]]
- [[events/]]

## 📜 关联 spec

- [[specs/]]

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
