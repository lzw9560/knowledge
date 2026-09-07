---
type: data_source
name: 腾讯行情
layer: 1
endpoint: qt.gtimg.cn
rate_limit: 不封IP
fallback: 底座层，无降级
compliance: ok
provides: [现价, 涨跌, PE, PB, 市值, 换手, 涨跌停]
created: 2026-09-06
last_synced: 2026-09-07
---

> [!info] 📡 数据源
> **名称**：腾讯行情  **层级**：L1
> **接口**：`qt.gtimg.cn`
> **限流**：`不封IP`  **降级**：`底座层，无降级`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 不封 IP，HTTP GBK 编码
- 标准库 `urllib` 直连
- **永远可用**，作为 A 股底座 Layer 1


## 🔄 降级链

- 底座层，无降级
- 反而是其他数据源失败后的兜底源


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
