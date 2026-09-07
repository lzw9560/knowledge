---
type: data_source
name: 巨潮 cninfo（互动易）
layer: 4
endpoint: www.cninfo.com.cn
rate_limit: requests 直连
fallback: 无
compliance: ok
provides: [公告, 互动易问答]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：巨潮 cninfo（互动易）  **层级**：L4
> **接口**：`www.cninfo.com.cn`
> **限流**：`requests 直连`  **降级**：`无`

## 📋 提供字段

待补充


## ⏱ 限流策略

- requests 直连
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

- 🔧 [[10_Reference/tech-learning/concepts/graceful-degradation|优雅降级]] — 巨潮互动易无降级，失败标灰
- 🔧 [[10_Reference/tech-learning/concepts/data-contract|数据契约]] — 互动易数据由契约层统一形状
- 🔧 [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 低频数据入缓存
