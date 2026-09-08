---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 动作（Actions）索引

> 本体第四构件。基于实体类型与关系生成的可执行行为——CRUD、状态流转、链接维护动作。
> 蒸馏自 nano-ontoprompt 四构件本体模型。

## 动作列表（Dataview 动态）

<!-- dataview-precompiled:32eea7897118 query:VEFCTEUK57G75Z6LIEFTICLnsbvlnosiLAogIOinpuWPkeadoeS7tiBBUyAi6Kem5Y+R5p2h5Lu2IiwKICDnm67moIflrp7kvZMgQVMgIuebruagh+WunuS9kyIKRlJPTSAiMTBfUmVmZXJlbmNlL2ludmVzdGluZy9hY3Rpb25zIgpXSEVSRSB0eXBlID0gIm1ldGhvZG9sb2d5X2luZGV4IgpTT1JUIGNvZGUgQVNDCg== -->
| 文件 | 类型 | 触发条件 | 目标实体 |
|---|---|---|---|
| [[10_Reference/investing/actions/index]] | — | — | — |
<!-- /dataview-precompiled -->

## 动作类型

| 类型 | 说明 | 示例 |
|---|---|---|
| **CRUD** | 创建/读取/更新/删除实体 | 新研报入库 → 创建 [[10_Reference/investing/reports/index|reports/]] 实体 |
| **状态流转** | 改变实体状态字段 | 候选股 → watching（工作流流转） |
| **链接维护** | 自动建立/修复 `[[]]` 链接 | 研报提到 600519 → 链接到 [[10_Reference/investing/stocks/600519]] |
| **审计快照** | 动作执行前后的状态快照 | 结算前快照 winrate 状态 |

## 新建动作

用 Templater 应用 `templates/action.md` 模板。动作必须含：触发条件 + 执行步骤 + 审计点。

## 与其他构件的关系

- 触发自 → [[10_Reference/investing/logic/index|logic/]]（规则满足时触发动作）
- 作用于 → [[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/reports/index|reports/]] 等实体
- 执行记录 → [[10_Reference/investing/reviews/index|reviews/]]（动作执行的审计追踪）

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/actions/审批实体]]
- [[10_Reference/investing/actions/研报自动链接]]
- [[10_Reference/investing/actions/inbox晋级]]
- [[10_Reference/investing/actions/实体重命名]]
- [[10_Reference/investing/actions/源同步]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/action` 新建 动作 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:6376f507f74d query:VEFCTEUK5Yqo5L2c5oC75pWwIEFTICLliqjkvZzmgLvmlbAiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmcvYWN0aW9ucyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 动作总数 |
|---|---|
| [[10_Reference/investing/actions/index]] | — |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
