---
type: concept
code: 
name: AIGC
related_industry: 
status: stub
created: 2026-09-07
---

> [!info] 概念信息
> **概念**：AIGC  **关联行业**：related_industry  **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
> 
> **关联**：[[industries/]] · [[data-sources/]]

> [!warning] Stub
> 此实体为断链修复自动生成的占位文件，正文待补充。

## 📖 题材逻辑

<!-- LLM 生成，待人工校验 -->
**题材逻辑**：AIGC（人工智能生成内容）被视为继专业生产内容、用户生产内容之后的新型内容生产方式，能够大幅降低创作门槛并提升内容生产效率。市场关注点在于其有望重塑传媒、营销、游戏、影视等多个行业的成本结构与商业模式，并被视为人工智能技术商业化落地的重要方向之一。
**催化因素**：底层大模型技术的迭代突破、头部企业发布现象级AI应用产品，以及国内外科技巨头在该领域的持续资本开支与战略布局，均可能强化市场对该概念的关注。

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

- **行业**：[[industries/]]
- **数据源**：[[data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
