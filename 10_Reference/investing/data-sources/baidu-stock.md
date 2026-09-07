---
type: data_source
name: 百度股市通（日K线）
layer: 4
endpoint: finance.pae.baidu.com
rate_limit: 不封IP
fallback: 无
compliance: ok
provides: [日K线]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：百度股市通（日K线）  **层级**：L4
> **接口**：`finance.pae.baidu.com`
> **限流**：`不封IP`  **降级**：`无`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 不封 IP
- 直连


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
