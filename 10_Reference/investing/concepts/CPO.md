---
type: concept
code: 
name: CPO
related_industry: 
status: stub
created: 2026-09-07
---

> [!info] 概念信息
> **概念**：CPO  **关联行业**：related_industry  **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
> 
> **关联**：[[industries/]] · [[data-sources/]]

> [!warning] Stub
> 此实体为断链修复自动生成的占位文件，正文待补充。

## 📖 题材逻辑
**题材逻辑**：CPO（共封装光学）技术将光引擎与交换芯片进行高密度集成，能大幅缩短电信号传输距离，被认为是突破数据中心高带宽、低功耗互联瓶颈的关键路径，因此在算力基础设施持续升级的背景下备受市场关注。
**催化因素**：英伟达、博通等头部厂商推进CPO交换机或光互连方案的产业化进度，以及大型数据中心开启CPO技术路线的规模部署，是形成板块催化的重要事件。

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
