---
type: concept
code: BK1035
name: CPO概念
related_industry: 通信设备
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：CPO概念  **关联行业**：通信设备
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/]]

## 📊 概念概览

- 概念代码：`BK1035`
- 名称：CPO概念
- 关联行业：通信设备

CPO（光电共封装）是 AI 算力光互联下一代技术，解决高速光模块功耗瓶颈。逻辑围绕「800G/1.6T 升级+CPO 渗透+硅光」展开，是光模块细分前沿。


## 📖 题材逻辑

<!-- LLM 生成，待人工校验 -->
**题材逻辑**：CPO（共封装光学）技术通过将光引擎与交换芯片直接封装，能显著降低功耗和传输延迟，被视为突破数据中心高速互连瓶颈的关键方向。在AI算力需求爆发背景下，传统可插拔光模块面临的功耗与密度瓶颈日益突出，CPO作为下一代高带宽、低功耗的光互连方案，受到市场高度关注。
**催化因素**：英伟达、博通等头部厂商在高端交换机或AI芯片中推进CPO技术应用，以及相关产品量产或送样进展，会引发市场对CPO产业链的预期升温。同时，光通信行业展会、标准组织发布CPO相关规范等事件，也可能成为阶段性催化因素。

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

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
