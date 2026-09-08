---
type: data_source
name: akshare
layer: 3
endpoint: akshare Python 包
rate_limit: 无（惰性导入）
fallback: DependencyMissing 优雅报错
compliance: ok
provides: [legu行业资金流, 行业资金流, 财报三表]
projects: [vibe-research, trading-agents, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：akshare  **层级**：L3
> **接口**：`akshare Python 包`
> **限流**：`无（惰性导入）`  **降级**：`DependencyMissing 优雅报错`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| period | str | 报告期（财务摘要） |
| revenue | float | 营业总收入 |
| revenue_yoy | float | 营收同比增长率 |
| net_profit | float | 净利润 |
| net_profit_yoy | float | 净利同比增长率 |
| eps | float | 基本每股收益 |
| bvps | float | 每股净资产 |
| roe | float | 净资产收益率 |
| gross_margin | float | 销售毛利率 |
| net_margin | float | 销售净利率 |
| op_cf_ps | float | 每股经营现金流 |
| current | float | 估值当前值（PE/PB） |
| percentile | float | 历史分位（%） |
| min | float | 历史最小值 |
| max | float | 历史最大值 |
| p20 | float | 20分位 |
| p50 | float | 50分位 |
| p80 | float | 80分位 |
| chip_profit_ratio | float | 获利比例（筹码分布，0-1） |
| avg_cost | float | 平均成本 |
| concentration | float | 90%集中度 |
| 90_cost | str | 90%成本区间（low-high） |
| 70_cost | str | 70%成本区间（low-high） |

> 数据源：akshare Python 包（stock_profit_forecast_ths/stock_news_em/stock_individual_info_em/stock_zh_a_disclosure_report_cninfo/stock_financial_abstract_ths/stock_zh_valuation_baidu + 自建东财 CYQ 筹码）

## ⏱ 限流策略

- 无（惰性导入，按需调用）
- Python 包，无网络层限流


## 🔄 降级链

- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级


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

- 🔧 [[10_Reference/tech-learning/tools/uv|uv 包管理]] — akshare Python 包由 uv 统一管理与锁版本（pyproject.toml + uv.lock）
- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — 惰性导入，缺失时 DependencyMissing 优雅报错不挡启动
- 🔧 [[10_Reference/tech-learning/frameworks/pydantic|Pydantic]] — akshare 返回的裸 dict 由契约层吸收为 Pydantic 模型
