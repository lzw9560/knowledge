---
type: concept
code: BK1035
name: CPO概念
related_industry: 通信设备
created: 2026-09-07
---

# 概念概览

- 概念代码：`BK1035`
- 名称：CPO概念
- 关联行业：通信设备

CPO（光电共封装）是 AI 算力光互联下一代技术，解决高速光模块功耗瓶颈。逻辑围绕「800G/1.6T 升级+CPO 渗透+硅光」展开，是光模块细分前沿。

# 成分股

核心成分股：

- [[stocks/000938]] — 紫光股份
- [[stocks/000988]] — 华工科技
- [[stocks/002156]] — 通富微电
- [[stocks/002179]] — 中航光电
- [[stocks/002185]] — 华天科技

```dataview
TABLE code AS "代码", name AS "名称"
FROM "stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT code ASC
```

# 相关行业

- [[industries/通信设备]]

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
