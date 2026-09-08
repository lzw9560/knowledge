---
type: concept
code: BK0902
name: MiniLED
related_industry: 半导体
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：MiniLED  **关联行业**：半导体
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK0902`
- 名称：MiniLED
- 关联行业：半导体

MiniLED 背光+直显，受益于电视/平板/车载渗透。


## 📖 题材逻辑
**题材逻辑**：MiniLED作为新一代显示技术背光方案，通过更小的灯珠尺寸实现更精细的局部调光，能够在成本与性能之间取得平衡，显著提升液晶显示的对比度、亮度与色域表现。该技术被视为MicroLED大规模量产前的重要过渡，可广泛应用于电视、显示器、笔记本电脑、车载显示及平板等领域，因此受到面板及LED产业链的高度关注。
**催化因素**：行业龙头品牌发布搭载MiniLED背光的新一代消费电子产品，或产业链传出MiniLED产能扩张、良率提升、成本下降等关键进展，往往会引发市场对该技术加速渗透的预期。

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

- [[stocks/000725|000725 京东方A]]
- [[stocks/000100|000100 TCL科技]]

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
