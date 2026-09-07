---
type: data_source
name: 
layer: 
endpoint: 
rate_limit: 
fallback: 
compliance: ok
provides: []
projects: []
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] 📡 数据源
> **名称**：name  **层级**：layer  **合规**：compliance
> **接口**：`endpoint`
> 
> **限流**：`rate_limit`  **降级**：`fallback`

## 📋 提供字段



## ⏱ 限流策略

- 限流：`rate_limit`

## 🔄 降级链

- 降级：`fallback`（主源失败后切到哪个备用源）

## 🔗 相关实体

> 该数据源供给哪些实体。

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
