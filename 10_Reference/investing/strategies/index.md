---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 战法 索引

> 投研战法卡片节点。12 张战法卡已从 `backend/strategies/cards/` 导入，另有淘股吧战法补充。每张卡链接其入场条件、出场条件、历史战绩、匹配股票、关联事件、来源 spec。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:525346134346 query:VEFCTEUK5oiY5rOV5ZCNIEFTICLmiJjms5XlkI0iLAogIGVkZ2Ug5a625pePIEFTICJlZGdlIOWutuaXjyIsCiAg5YWl5Zy65p2h5Lu2IEFTICLlhaXlnLrmnaHku7YiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3Rpbmcvc3RyYXRlZ2llcyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 战法名 | edge 家族 | 入场条件 |
|---|---|---|---|
| [[10_Reference/investing/strategies/index]] | — | — | — |
<!-- /dataview-precompiled -->

## 关系

- matches: [[10_Reference/investing/stocks/index|stocks/]]（战法匹配的股票）
- triggered_by: [[10_Reference/investing/events/index|events/]]（战法由事件触发，如涨停池触发首板）
- defined_in: [[10_Reference/investing/specs/index|specs/]]（战法 match 逻辑对应的 SDD spec）
- pairs_with: [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]（反包战法依赖游资席位加分项）

## edge 家族说明

| edge_family | 说明 | 典型战法 |
|---|---|---|
| 动量溢价 | 连板/涨停惯性博次日溢价 | consecutive_relay, first_plate, end_of_day_sneak, 一字竞价选股法 |
| 事件溢价 | 炸板/反包等情绪转折博弈 | reverse_package, break_reseal, storm_reversal |
| 均值回归 | 回调低吸博反弹 | low_absorption |
| 形态突破 | 平台/形态突破 | platform_breakout, pattern_reversal |
| 龙头追踪 | 板块龙头识别 | dragon_head |
| 接力博弈 | 弱转强/N字接力 | weak_turn_strong, n_shape_counterattack |

## 新建实体

用 Templater 应用 `templates/strategy` 新建（12 张已导入，后续新增战法用模板）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/strategy` 新建 战法 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:a19545651e8a query:VEFCTEUK5oiY5rOV5oC75pWwIEFTICLmiJjms5XmgLvmlbAiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3Rpbmcvc3RyYXRlZ2llcyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 战法总数 |
|---|---|
| [[10_Reference/investing/strategies/index]] | — |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
