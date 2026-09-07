---
type: concept
code: BK0877
name: PCB
related_industry: 半导体
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：PCB  **关联行业**：半导体
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK0877`
- 名称：PCB
- 关联行业：半导体

印制电路板产业链，受益于 5G/服务器/新能源车需求。


## 📖 题材逻辑

<!-- LLM 生成，待人工校验 -->
**题材逻辑**：PCB（印制电路板）作为电子产品的关键互连件，受益于AI服务器、高速网络和汽车电子等下游需求升级，高多层板、HDI及封装基板等高端产品占比提升，驱动行业结构性成长。市场关注点集中在算力硬件迭代带来的价值量跃升，以及供应链向国内龙头集中的趋势。
**催化因素**：海外科技巨头持续加大AI基础设施资本开支，英伟达等新一代算力芯片及配套方案发布，会强化高速PCB的订单预期。国内算力产业政策扶持与国产替代进程加速，同样构成情绪催化。

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

### 成分股链接

- [[stocks/000100|000100 TCL科技]]
- [[stocks/000988|000988 华工科技]]
- [[stocks/000657|000657 中钨高新]]

## 🔄 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

- **发酵期**：政策催化 / 行业拐点 / 龙头订单
- **高潮期**：板块情绪过热，龙头翻倍
- **退潮期**：估值过高 / 业绩证伪 / 风格切换


## 💰 资金流向

- 数据源：[[data-sources/eastmoney-push2|东财 push2]]

## 📰 相关研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  org AS "机构",
  publish_date AS "日期"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
LIMIT 10
```

## ⚡ 近期事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```

## 🔗 关联

- **行业**：[[industries/]] · **数据源**：[[data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
