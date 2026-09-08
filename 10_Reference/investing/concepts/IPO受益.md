---
type: concept
code: BK0697
name: IPO受益
related_industry: 证券
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：IPO受益  **关联行业**：证券
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK0697`
- 名称：IPO受益
- 关联行业：证券

IPO 受益概念，参股创投/拟上市企业。


## 📖 题材逻辑
**题材逻辑**：IPO受益概念关注的是因其他企业首次公开发行上市而可能获得股权价值重估或投资收益的上市公司，这类公司通常持有拟IPO企业的股份，一旦被投企业成功上市，其股权流动性大幅提升，所持权益的公允价值可能显著增长。市场对此类逻辑的关注，实质上是对“影子股”估值切换与潜在变现收益的提前博弈。
**催化因素**：相关催化事件主要包括拟IPO企业披露招股说明书、通过发审委审核、取得注册批文或正式挂牌交易等关键节点，这些进展会强化市场对参股方潜在收益的预期。此外，注册制改革的深化、新股发行节奏变化以及创投板块的集体活跃，也会阶段性带动该概念的关注度。

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

- [[stocks/000988|000988 华工科技]]
- [[stocks/000568|000568 泸州老窖]]

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
