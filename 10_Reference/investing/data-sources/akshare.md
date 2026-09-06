---
type: data_source
name: akshare
layer: 3
endpoint: akshare Python 包
rate_limit: 无（惰性导入）
fallback: DependencyMissing 优雅报错
compliance: ok
provides: [legu行业资金流, 行业资金流, 财报三表(待补)]
projects: [vibe-research, trading-agents, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
---

# akshare

## 提供字段
- legu 行业资金流（`_sentiment/_sectors` 用）
- 行业资金流
- 财报三表（待补：与新浪/巨潮职责重叠，具体分工待核对）

## 限流策略
- 无（惰性导入，按需调用）
- Python 包，无网络层限流

## 降级链
- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级

## 相关实体
- 喂给实体类型：[[industries/]] [[metrics/]]
- 对应代码：`backend/data/sources/astock.py`（惰性导入点）、`market.py` → `_sentiment/_sectors`

## 相关 spec
- [[specs/]] 后端数据层迁移 / akshare 惰性导入

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**相关工具**：
- `query_news` → `astock.stock_news`

**对应函数**（`backend/data/sources/`）：
- `data.sources.akshare_src.profit_forecast`
- `data.sources.akshare_src.stock_news`
- `data.sources.akshare_src.individual_info`
- `data.sources.akshare_src.disclosure`
- `data.sources.akshare_src.financials`
- `data.sources.akshare_src.valuation_percentile`
- `data.sources.akshare_src.chip_distribution`

**关联 spec**：
- [[specs/S007-契约层]]（S007）
- [[specs/S008-后端数据层迁移]]（S008）
- [[specs/S011-调度收口]]（S011）
- [[specs/S017-A股涨跌预测模型栈]]（S017）
- [[specs/S018-多源特征工程]]（S018）
- [[specs/S031-调度收口盘前多层按战法回测]]（S031）
- [[specs/S066-策略特定漏斗架构重构]]（S066）
- [[specs/S094-战法分类与双pipeline重构]]（S094）

**喂给实体类型**：
- [[industries/]]
- [[metrics/]]
