---
type: concept
code: BK1127
name: AI硬件
related_industry: 半导体
created: 2026-09-07
---

> [!info] 概念信息
> **概念**：AI硬件  **关联行业**：半导体  **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
> 
> **关联**：[[10_Reference/investing/industries/index|industries/]] · [[10_Reference/investing/data-sources/index|data-sources/]]

## 📖 题材逻辑
**题材逻辑**：AI硬件泛指为人工智能计算与应用提供基础支撑的物理设备，涵盖AI服务器、高速光模块、专用芯片及散热系统等关键环节。该方向受市场关注的核心在于，大模型训练与推理需求持续攀升，直接拉动算力基础设施的资本开支，使硬件环节成为产业链中率先兑现业绩的领域。
**催化因素**：主要催化因素包括海外科技巨头显著上调资本开支指引、国内算力基建政策加码，以及新一代AI芯片或服务器产品发布。此外，高速互联技术迭代与数据中心能效标准趋严，也会引发市场对配套硬件升级的预期。

## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT market_cap DESC
LIMIT 20
```

## 🔗 关联

- **行业**：[[10_Reference/investing/industries/index|industries/]]
- **数据源**：[[10_Reference/investing/data-sources/index|data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
