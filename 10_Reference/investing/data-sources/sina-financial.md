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
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：新浪财经（财报三表）  **层级**：L4
> **接口**：`vip.stock.finance.sina.com.cn`
> **限流**：`urllib 直连`  **降级**：`无`

## 📋 提供字段

待补充


## ⏱ 限流策略

- urllib 直连
- 待补：具体限流策略（未在 ARCHITECTURE.md 明示封禁行为）


## 🔄 降级链

- 无


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
