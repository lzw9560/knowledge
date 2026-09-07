---
type: data_source
name: 同花顺 THS（一致预期/涨停揭秘）
layer: 4
endpoint: basic.10jqka.com.cn
rate_limit: 直连
fallback: 无
compliance: ok
provides: [一致预期, 涨停揭秘]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：同花顺 THS（一致预期/涨停揭秘）  **层级**：L4
> **接口**：`basic.10jqka.com.cn`
> **限流**：`直连`  **降级**：`无`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 直连
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

## 🔧 技术栈

- 🔧 [[tech-learning/concepts/data-contract|数据契约]] — 一致预期/涨停揭秘数据由契约层统一形状（S104 唯一源）
- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — hithink 无降级，失败标灰
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — 低频数据入缓存
