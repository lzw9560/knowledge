---
type: concept
code: BK1160
name: AI应用
related_industry: 软件
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：AI应用  **关联行业**：软件
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[10_Reference/investing/industries/index|industries/]] · [[10_Reference/investing/data-sources/index|data-sources/]]

## 📊 概念概览

- 概念代码：`BK1160`
- 名称：AI应用
- 关联行业：软件

AI 大模型落地应用层，覆盖 AIGC/智能体/教育/营销/办公场景。逻辑围绕「模型能力提升+垂直场景渗透+商业化变现」展开，是 AI 产业链离 C 端最近的一环。


## 📖 题材逻辑
**题材逻辑**：AI应用概念聚焦人工智能技术在具体场景的落地与商业化，涵盖办公、教育、医疗、金融等垂直领域。市场关注其从模型能力突破转向产品变现的潜力，随着基础大模型逐步成熟，应用层企业有望率先实现收入增长，成为产业链中市场空间最被看好的环节。
**催化因素**：海外头部AI应用企业用户量与收入超预期，以及国内厂商密集发布AI原生应用或功能迭代，常成为板块情绪催化点。此外，重大模型能力升级、算力成本显著下降及行业政策支持，也会推动市场对应用端加速渗透的预期。

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

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
