---
type: concept
code: BK0840
name: OLED
related_industry: 半导体
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：OLED  **关联行业**：半导体
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[10_Reference/investing/industries/index|industries/]] · [[10_Reference/investing/data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK0840`
- 名称：OLED
- 关联行业：半导体

OLED 面板+材料+设备，受益于国产替代+柔性屏需求。


## 📖 题材逻辑
**题材逻辑**：OLED作为新一代显示技术，凭借自发光、高对比度、轻薄柔韧等特性，在智能手机、电视、可穿戴设备等领域渗透率持续提升，被视为显示产业升级的核心方向。市场关注其逐步替代传统LCD的趋势，以及国内面板厂商在全球产能份额中的提升空间，中长期技术迭代与国产替代逻辑清晰。
**催化因素**：头部品牌发布搭载OLED屏幕的旗舰新品、面板厂商披露产线满产或产品涨价信息，往往会引发市场对产业链景气度的重估。此外，关键材料或设备取得国产化突破、行业获得专项产业政策支持，也会成为短期情绪催化节点。

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

- [[10_Reference/investing/stocks/000725|000725 京东方A]]
- [[10_Reference/investing/stocks/000100|000100 TCL科技]]

## 🔄 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

- **发酵期**：政策催化 / 行业拐点 / 龙头订单
- **高潮期**：板块情绪过热，龙头翻倍
- **退潮期**：估值过高 / 业绩证伪 / 风格切换


## 💰 资金流向

- 数据源：[[10_Reference/investing/data-sources/eastmoney-push2|东财 push2]]

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

- **行业**：[[10_Reference/investing/industries/index|industries/]] · **数据源**：[[10_Reference/investing/data-sources/index|data-sources/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
