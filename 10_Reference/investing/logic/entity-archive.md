---
type: logic
rule_id: ENTITY-ARCHIVE-001
rule_type: 状态机
target_entity: 全类型
severity: medium
condition: "实体废弃（status: deprecated 或 90+ 天无更新且无入边）"
action_on_violation: 废弃实体未归档直接删 → 报 critical；归档未留 redirect → 报 low
source: AGENTS.md 工程底线（正式区直接删 → critical，从 git 恢复 + 归档而非删除）
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`ENTITY-ARCHIVE-001`  **类型**：状态机
> **严重级**：medium  **适用实体**：全类型
>
> **违反处置**：`废弃实体未归档直接删 → 报 critical；归档未留 redirect → 报 low`

## 📋 规则定义

- **类型**：`状态机`
- **适用实体**：全类型
- **严重级**：`medium`
- **条件**：`status: deprecated` 或 `stale_check 标记 90+ 天无更新且无入边`

## ⚡ 触发条件

实体满足以下任一条件触发归档：
1. frontmatter `status: deprecated`（人工标记废弃）
2. `stale_check` 标记 90+ 天未更新 + `orphan_check` 标记无入边（双重确认，避免误归档活跃实体）

归档 ≠ 删除：move 到 `20_Archive/`，保留可恢复性，所有指向它的反向链接需留 redirect 注记。

## 🔧 执行逻辑

```
对每个废弃候选：
  if fm.status == "deprecated" OR (stale_90d AND no_inbound):
    target = 20_Archive/<type>/<entity>.md
    move_note(current_path → target)  # 不真删
    在原路径留 stub：<entity>.md 仅含 frontmatter(status: archived, redirect: <target>)
    扫描所有指向原路径的 [[链接]]：
      不改链接文本（stub 的 redirect 字段保留可达性）
      或批量改指向 target（走 [[10_Reference/investing/actions/rename-entity]]）
    更新 fm: + archived_date: <today>
    生成归档日志
```

归档目录结构：
```
20_Archive/
  stocks/<code>.md
  industries/<slug>.md
  concepts/<slug>.md
  ...
```

Dataview 查询（待归档候选）：

```dataview
TABLE type AS "类型", status AS "状态", length(file.inlinks) AS "入边数"
FROM "10_Reference/investing"
WHERE status = "deprecated" OR (length(file.inlinks) = 0 AND status != "stub")
SORT type ASC
```

## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| 废弃实体直接删文件（未归档） | critical | 从 git 恢复 + move 到 20_Archive/ |
| 归档后未留 redirect stub | low | 补建 stub 或批量改反向链接 |
| 活跃实体被误归档（有入边） | high | 从 20_Archive/ 移回 + 撤销归档标记 |
| 归档未记 archived_date | low | 补 archived_date 字段 |

## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **前置规则**：[[10_Reference/investing/logic/entity-lifecycle]]（生命周期末端进归档）
- **相关规则**：[[10_Reference/investing/logic/stale_check]]（90 天未更新判定）
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/industries/index|industries/]] [[10_Reference/investing/concepts/index|concepts/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
