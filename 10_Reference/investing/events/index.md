---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 事件 索引

> 新闻/公告/涨停/异动事件节点。对应 Pydantic 契约 `News` + `Announcement` + `ZTPoolItem`。每条记录链接其影响标的、触发战法、来源。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:c64bfa07934d query:VEFCTEUKY3JlYXRlZCBBUyAi5pel5pyfIiwKICDnsbvlnosgQVMgIuexu+WeiyIsCiAg5pGY6KaBIEFTICLmkZjopoEiLAogIOadpea6kCBBUyAi5p2l5rqQIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nL2V2ZW50cyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 日期 | 类型 | 摘要 | 来源 |
|---|---|---|---|---|
| [[10_Reference/investing/events/index]] | 2026-09-07 | — | — | — |
<!-- /dataview-precompiled -->

## 关系

- affects: [[10_Reference/investing/stocks/index|stocks/]]（事件影响标的）
- triggers: [[10_Reference/investing/strategies/index|strategies/]]（事件触发战法，如涨停池触发首板/连板/炸板回封）
- pairs_with: [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]（涨停事件与龙虎榜配对）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（新闻/公告/涨停池数据来源）

## 事件类型说明

| event_type | 说明 | 对应 Pydantic 契约 |
|---|---|---|
| 新闻 | 财经新闻 | `News` |
| 公告 | 公司公告 | `Announcement` |
| 涨停 | 涨停池 | `ZTPoolItem` |
| 跌停 | 跌停池 | （派生） |
| 停牌 | 停牌 | （派生） |
| 复牌 | 复牌 | （派生） |

## 新建实体

用 Templater 应用 `templates/event` 新建。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/events/2026-09-01-涨停池]]
- [[10_Reference/investing/events/2026-09-01-炸板池]]
- [[10_Reference/investing/events/2026-09-02-涨停池]]
- [[10_Reference/investing/events/2026-09-02-炸板池]]
- [[10_Reference/investing/events/2026-09-03-涨停池]]
- [[10_Reference/investing/events/2026-09-03-炸板池]]
- [[10_Reference/investing/events/2026-09-04-涨停池]]
- [[10_Reference/investing/events/2026-09-04-炸板池]]
- [[10_Reference/investing/events/2026-09-04-竞价异动]]
- [[10_Reference/investing/events/2026-09-05-涨停池]]
- [[10_Reference/investing/events/2026-09-07-异动]]
- [[10_Reference/investing/events/2026-09-07-涨停池]]
- [[10_Reference/investing/events/2026-09-07-炸板池]]
- [[10_Reference/investing/events/2026-09-08-美伊冲突升级]]
- [[10_Reference/investing/events/2026-09-08-基差异动]]
- [[10_Reference/investing/events/2026-09-08-持仓追踪]]
- [[10_Reference/investing/events/2026-09-08-长电科技定增]]
- [[10_Reference/investing/events/2026-09-08-通富微电中报定增]]
- [[10_Reference/investing/events/2026-09-08-华天科技并购重组]]
- [[10_Reference/investing/events/2026-09-08-中天科技中报回购]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/event` 新建 事件 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:cf9b59925fed query:VEFCTEUK5LqL5Lu25oC75pWwIEFTICLkuovku7bmgLvmlbAiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmcvZXZlbnRzIgpXSEVSRSB0eXBlID0gIm1ldGhvZG9sb2d5X2luZGV4IgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 事件总数 |
|---|---|
| [[10_Reference/investing/events/index]] | — |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
