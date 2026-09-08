---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 指数 索引

> 宽基与行业指数节点（沪深300/中证500/创业板指等）。每个指数链接其成分股、近期走势。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:9f64cc2c81a8 query:VEFCTEUK5oyH5pWw5Luj56CBIEFTICLmjIfmlbDku6PnoIEiLAogIOaMh+aVsOWQjeensCBBUyAi5oyH5pWw5ZCN56ewIiwKICDluILlnLogQVMgIuW4guWcuiIKRlJPTSAiMTBfUmVmZXJlbmNlL2ludmVzdGluZy9pbmRpY2VzIgpXSEVSRSB0eXBlID0gIm1ldGhvZG9sb2d5X2luZGV4IgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 指数代码 | 指数名称 | 市场 |
|---|---|---|---|
| [[10_Reference/investing/indices/index]] | — | — | — |
<!-- /dataview-precompiled -->

## 关系

- has_members: [[10_Reference/investing/stocks/index|stocks/]]（指数成分股）
- has_events: [[10_Reference/investing/events/index|events/]]（指数调整/纳入剔除事件）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（指数行情来源）

## 新建实体

用 Templater 应用 `templates/index` 新建。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/indices/000001]]
- [[10_Reference/investing/indices/000300]]
- [[10_Reference/investing/indices/000905]]
- [[10_Reference/investing/indices/399001]]
- [[10_Reference/investing/indices/399006]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/index` 新建 指数 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:aeedcd2e4575 query:VEFCTEUK5oyH5pWw5oC75pWwIEFTICLmjIfmlbDmgLvmlbAiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmcvaW5kaWNlcyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 指数总数 |
|---|---|
| [[10_Reference/investing/indices/index]] | — |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
