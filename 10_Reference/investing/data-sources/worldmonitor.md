---
type: data_source
name: worldmonitor（全球宏观 MCP）
layer: 5
endpoint: MCP 远程
rate_limit: 无
fallback: 无
compliance: ok
provides: [全球宏观指标]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：worldmonitor（全球宏观 MCP）  **层级**：L5
> **接口**：`MCP 远程`
> **限流**：`无`  **降级**：`无`

## 📋 提供字段

待补充


## ⏱ 限流策略

- MCP 远程调用
- 无（待补：是否有上游限流）


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
