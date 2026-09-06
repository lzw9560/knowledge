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

# Tushare

## 数据源说明
Tushare 是 A 股量化领域最常用的积分制数据 API。通过 HTTP 接口提供行情、财务、指数、期货、基金、可转债等全品类金融数据，免费用户有 5000 积分基础额度，高级数据（如 Tick 级、龙虎榜明细、分笔）需付费提升积分。

a-Plate-Sentinel 项目的主要数据源，用于情绪看板的涨停池/连板数据、打板选股器的竞价扫描、龙虎榜席位引擎的明细数据。

## 提供字段
- A 股实时/历史行情（日线/分钟线）
- 财务三表（资产负债/利润/现金流量）
- 指数行情（沪深300/中证500 等宽基与行业指数）
- 龙虎榜明细（席位买卖明细，席位标签引擎核心输入）
- 涨跌停池（情绪看板核心输入）
- 期货/基金/可转债行情

## 限流策略
- 积分制：免费 5000 积分，按接口积分消耗扣减
- 高级接口（如 Tick、分笔、龙虎榜明细）需更高积分
- 付费提升积分上限可解锁更多接口与更高频率

## 与其他数据源对比

| 维度 | Tushare | [[data-sources/akshare]] | [[data-sources/eastmoney-push2]] |
|------|---------|-------------------------|--------------------------------|
| 接入方式 | HTTP API（积分制） | Python 包（惰性导入） | HTTP 接口（免费直连） |
| 限流 | 积分制，免费额度有限 | 无 | 无（需自行控频） |
| 龙虎榜明细 | ✅ 积分制接口 | ✅ 部分接口 | ❌ |
| 涨跌停池 | ✅ | ✅ 部分 | ❌ |
| Tick 级 | ✅ 需高级积分 | ❌ | ❌ |
| 项目归属 | a-Plate-Sentinel | Vibe-Research 共用 | Vibe-Research |

## 相关实体
- 喂给实体类型：[[stocks/]] [[industries/]] [[dragon-tiger/]] [[events/]]
- 项目归属：[[specs/a-plate-sentinel-project]]

## 相关 spec
- a-Plate-Sentinel `docs/module-design.md` 1.3 节（STI 数据源含 Tushare 涨跌停池）
