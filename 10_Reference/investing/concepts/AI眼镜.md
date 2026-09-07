---
type: concept
code: BK1178
name: AI眼镜
related_industry: 消费电子
created: 2026-09-07
confidence: medium
source: astock.concept_blocks
---

> [!info] 💡 概念信息
> **概念**：AI眼镜  **关联行业**：消费电子
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/eastmoney-push2|东财 push2]]

## 📊 概念概览

- 概念代码：`BK1178`
- 名称：AI眼镜
- 关联行业：消费电子

AI 眼镜是下一代智能终端入口，融合大模型语音助手+视觉感知+实时翻译。受益于 Ray-Ban Meta 爆款+国产大模型落地+端侧 AI 芯片成熟。


## 📖 题材逻辑

<!-- LLM 生成，待人工校验 -->
**题材逻辑**：AI眼镜被视为AI大模型端侧落地的重要硬件载体，能在第一视角实现语音交互、图像识别与信息叠加，有望复刻TWS耳机集成化替代传统眼镜的渗透路径。市场关注其开启新智能穿戴品类的潜力，硬件供应链与AI应用生态可能因此带来增量机会。
**催化因素**：产业催化主要来自头部科技厂商发布或展示AI眼镜新品，以及相关技术突破或生态合作动向；消费电子展会和行业标准推进也会提升市场对该题材的关注度。

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
- [[stocks/002230|002230 科大讯飞]]

## 🔄 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

- **发酵期**：海外爆款发布 / 国内大模型开放 / 大厂入局
- **高潮期**：板块情绪过热，龙头翻倍
- **退潮期**：销量不及预期 / 估值过高 / 风格切换


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
