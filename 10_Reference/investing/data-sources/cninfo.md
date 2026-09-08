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

| 字段 | 类型 | 说明 |
|---|---|---|
| company | str | 公司简称 |
| question | str | 投资者提问内容 |
| answer | str | 公司回复内容（None=未回复） |
| answerer | str | 回复人 |
| ask_time | str | 提问时间（YYYY-MM-DD HH:MM） |

> 数据源：`irm.cninfo.com.cn` 互动易（requests 直连，非东财封 IP 域）

## ⏱ 限流策略

- requests 直连
- 源端未明示封禁行为，低频调用直连


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

- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — 巨潮互动易无降级，失败标灰
- 🔧 [[tech-learning/concepts/data-contract|数据契约]] — 互动易数据由契约层统一形状
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — 低频数据入缓存
