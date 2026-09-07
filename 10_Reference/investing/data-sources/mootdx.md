---
type: data_source
name: mootdx
layer: 3
endpoint: TCP 7709
rate_limit: 无（惰性导入）
fallback: DependencyMissing 优雅报错
compliance: ok
provides: [K线, 财报(待补)]
projects: [vibe-research, trading-agents, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：mootdx  **层级**：L3
> **接口**：`TCP 7709`
> **限流**：`无（惰性导入）`  **降级**：`DependencyMissing 优雅报错`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 无（惰性导入，按需调用）
- TCP 7709 通达信协议


## 🔄 降级链

- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级


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

- 🔧 [[10_Reference/tech-learning/tools/uv|uv 包管理]] — mootdx Python 包由 uv 管理锁版本
- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — 惰性导入，缺失时 DependencyMissing 优雅报错
- 🔧 [[10_Reference/tech-learning/concepts/data-contract|数据契约]] — TCP 7709 返回数据由契约层统一形状
