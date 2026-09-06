---
type: data_source
name: 新浪财经（财报三表）
layer: 4
endpoint: vip.stock.finance.sina.com.cn
rate_limit: urllib 直连
fallback: 无
compliance: ok
provides: [资产负债表, 利润表, 现金流量表]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
---

# 新浪财经（财报三表）

## 提供字段
- 财报三表（资产负债表/利润表/现金流量表）

## 限流策略
- urllib 直连
- 待补：具体限流策略（未在 ARCHITECTURE.md 明示封禁行为）

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[metrics/]] [[stocks/]]
- 对应代码：`backend/data/sources/astock.py` → `finance`、`full_valuation`

## 相关 spec
- [[specs/]] 后端数据层迁移 / 财报三表接入

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**对应函数**（`backend/data/sources/`）：
- `data.sources.sina.fetch_raw`
- `data.sources.sina_financial.fetch_raw`
- `data.sources.sina_financial.fetch_merged_periods`
