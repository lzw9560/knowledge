---
type: concept
code: BK0948
name: MicroLED
related_industry: 半导体
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：MicroLED  **关联行业**：半导体
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[10_Reference/investing/industries/index|industries/]] · [[10_Reference/investing/data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK0948`
- 名称：MicroLED
- 关联行业：半导体

MicroLED 显示技术，下一代显示方向。受益于苹果/三星布局。


## 📖 题材逻辑
**题材逻辑**：MicroLED被视为下一代显示技术的核心方向，其具备自发光、高亮度、长寿命及低功耗等特性，理论上能在显示效果上超越现有的OLED与LCD。市场关注其在高阶电视、可穿戴设备及AR/VR等微显示领域的应用潜力，认为该技术有望重塑显示产业格局。
**催化因素**：苹果、三星等头部消费电子品牌加速推进MicroLED技术产品化进程，相关量产或商用落地传闻会显著提振市场情绪。此外，核心制造环节如巨量转移技术的良率突破或成本下降，也会成为板块行情的关键催化剂。

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
