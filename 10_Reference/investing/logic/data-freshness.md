---
type: logic
rule_id: DATA-FRESHNESS-001
rule_type: 校验规则
target_entity: metrics, valuations, reports
severity: medium
condition: 时点数据的 last_synced 超 7 天 → 标 stale；超 30 天 → 标 data_suspect
action_on_violation: "标记 frontmatter + status: stale，触发刷新工单"
source: AGENTS.md 数据支撑优先（过时数据不得作为定稿依据）+ ora-3 §4（数据时效性）
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`DATA-FRESHNESS-001`  **类型**：校验规则
> **严重级**：medium  **适用实体**：metrics, valuations, reports
>
> **违反处置**：`标记 frontmatter + status: stale，触发刷新工单`

## 📋 规则定义

- **类型**：`校验规则`
- **适用实体**：metrics, valuations, reports（含时点数据的实体）
- **严重级**：`medium`
- **条件**：`last_synced 超 7 天`

## ⚡ 触发条件

时点数据实体的 `last_synced` 字段（ISO 日期）与当前日期的差值：
- `> 7 天` → 标 `status: stale`（轻度过期，需刷新）
- `> 30 天` → 标 `status: stale` + `data_suspect: true`（严重过期，不得作为定稿依据）
- `last_synced` 缺失 → 标 `data_suspect: true`（无时效标注 = 不可信）

阈值依据：A 股财报季披露周期约 90 天，但价格/估值高频数据应周级刷新；7 天阈值覆盖周级数据，30 天覆盖月级数据。

## 🔧 执行逻辑

```
today = date.now()
for entity in [metrics, valuations, reports]:
  if fm.last_synced is None:
    fm.data_suspect = true  # 无时效标注
    continue
  age = today - parse(fm.last_synced)
  if age > 30:
    fm.status = "stale"
    fm.data_suspect = true
    触发刷新工单（.scratch/data-freshness/）
  elif age > 7:
    fm.status = "stale"
    # 轻度过期，记录但不上工单
```

Dataview 查询（stale 实体）：

<!-- dataview-precompiled:109a02f1c731 -->
| 文件 | 类型 | 最后同步 | 状态 |
|---|---|---|---|
| — | — | — | — |
<!-- /dataview-precompiled -->

## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| last_synced 超 7 天未标 stale | low | 补 status: stale |
| last_synced 超 30 天未标 data_suspect | medium | 补 data_suspect: true |
| last_synced 缺失 | medium | 补字段 or 标 data_suspect |
| 过时数据用于定稿决策 | high | 拦截 + 强制刷新后重评 |

## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **相关规则**：[[10_Reference/investing/logic/confidence-decay]]（置信度随时间衰减）
- **约束实体**：[[10_Reference/investing/metrics/index|metrics/]] [[10_Reference/investing/valuations/index|valuations/]] [[10_Reference/investing/reports/index|reports/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
