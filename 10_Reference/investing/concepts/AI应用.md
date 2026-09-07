---
type: concept
code: BK1160
name: AI应用
related_industry: 软件
created: 2026-09-07
---

# 概念概览

- 概念代码：`BK1160`
- 名称：AI应用
- 关联行业：软件

AI 大模型落地应用层，覆盖 AIGC/智能体/教育/营销/办公场景。逻辑围绕「模型能力提升+垂直场景渗透+商业化变现」展开，是 AI 产业链离 C 端最近的一环。

# 成分股

核心成分股：

- [[stocks/000034]] — 神州数码
- [[stocks/000528]] — 柳工
- [[stocks/000560]] — 我爱我家
- [[stocks/000725]] — 京东方A
- [[stocks/001330]] — 博纳影业

```dataview
TABLE code AS "代码", name AS "名称"
FROM "stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT code ASC
```

# 相关行业

- [[industries/软件]]

# 题材轮动

> 记录该概念的轮动节奏：发酵期/高潮期/退潮期标志性事件。

- **发酵期**：政策催化 / 行业拐点 / 龙头订单
- **高潮期**：板块情绪过热，龙头翻倍
- **退潮期**：估值过高 / 业绩证伪 / 风格切换

# 资金流向

链接 [[data-sources/eastmoney-push2]] 查看板块资金流入流出。

# 近期事件

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```

# 相关研报

```dataview
TABLE title AS "标题", org AS "机构", publish_date AS "日期"
FROM "reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
```
