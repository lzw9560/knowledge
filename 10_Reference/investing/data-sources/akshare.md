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
