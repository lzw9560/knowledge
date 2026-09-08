---
type: industry
code: 
name: IT服务
source: 东财涨停池行业分类
created: 2026-09-07
confidence: medium
---

> [!info] 🏭 行业信息
> **行业**：IT服务  **来源**：东财涨停池行业分类
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[10_Reference/investing/concepts/index|concepts/]] · [[10_Reference/investing/data-sources/index|data-sources/]]

## 📊 行业概览

- 名称：IT服务
- 分类来源：东财涨停池（push2ex hybk 字段）

IT服务行业覆盖信息系统从规划咨询、设计开发、系统集成到运维外包及云化管理的全生命周期服务环节，是连接基础软硬件与行业应用落地的关键纽带。其核心驱动逻辑源于企业数字化转型的持续投入、云原生与人工智能驱动的服务智能化升级，以及信创自主可控带来的存量系统国产化替代需求。A股市场上，IT服务公司数量众多且以项目制、人力交付为主，普遍呈现轻资产、高应收账款、业绩季节性波动明显的财务特征。行业集中度偏低，并购整合与云服务转型是龙头提升份额的主要路径，板块估值常受数据要素、人工智能等政策主题催化，行情弹性较大但内部分化显著。


## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  pe_ttm AS "PE",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND industry = this.name
SORT market_cap DESC
LIMIT 20
```

## 💰 资金流向

- 数据源：[[10_Reference/investing/data-sources/eastmoney-push2|东财 push2]]

## 📰 行业研报

```dataview
TABLE WITHOUT ID
  publish_date AS "日期",
  org AS "机构",
  researcher AS "分析师",
  title AS "标题"
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
