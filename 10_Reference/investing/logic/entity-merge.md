---
type: logic
rule_id: ENTITY-MERGE-001
rule_type: 校验规则
target_entity: 全类型
severity: high
condition: 同 code + 同 type 出现多份实体记录
action_on_violation: 触发合并工单（保留 confidence 最高的，合并关系后归档冗余）
source: AGENTS.md 工程底线（不臆造数据——重复实体导致数据不一致）+ ora-3 §1.3
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`ENTITY-MERGE-001`  **类型**：校验规则
> **严重级**：high  **适用实体**：全类型
>
> **违反处置**：`触发合并工单（保留 confidence 最高的，合并关系后归档冗余）`

## 📋 规则定义

- **类型**：`校验规则`
- **适用实体**：全类型
- **严重级**：`high`
- **条件**：`同 code + 同 type 多份记录`（联合键去重，跨类型共享 code 属正常关联）

## ⚡ 触发条件

`vault_audit.py` 的 `duplicate_check` 按 `(code, type)` 联合分组，同 code 不同 type 不报（如 code=600519 的 stock/metric/valuation/report 是正常跨类型关联），只有同 code + 同 type 多份才触发合并。

```dataview
TABLE length(rows) AS "文件数", rows.file.link AS "文件"
FROM "10_Reference/investing"
WHERE code != null AND type != null
GROUP BY code + "|" + type
HAVING length(rows) > 1
```

## 🔧 执行逻辑

```
# vault_audit.py duplicate_check 分组键：(code, type)
code_type_map = {}
for file in vault:
  if frontmatter.code AND frontmatter.type:
    key = (code, type)  # 联合键，同 code 不同 type 不冲突
    code_type_map[key].append(file)

for (code, type), files in code_type_map.items():
  if len(files) > 1:
    # 选定保留项：confidence 最高的，并列取 created 最新
    keeper = max(files, key=lambda f: (f.confidence, f.created))
    others = files - keeper
    for other in others:
      合并 other 的入边/出边到 keeper（避免断链）
      合并 other 的 frontmatter 非空字段到 keeper
      move_note(other → archive/duplicates/)  # 归档不真删
    生成合并日志
```

保留策略（优先级从高到低）：
1. `confidence` 最高（high > medium > low）
2. 并列时取 `created` 最新
3. 仍并列取 `quality_score` 最高
4. 都相同时取文件名 lexicographic 最小（确定性）

## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| 同 code + 同 type 多份未合并 | high | 触发合并工单，按 confidence 选 keeper |
| 合并后未迁移反向链接 | high | 走 [[10_Reference/investing/actions/rename-entity]] 批量改链 |
| 合并直接删冗余文件（未归档） | critical | 从 git 恢复 + move 到 archive/duplicates/ |
| 同 code 不同 type 误报为重复 | low | 已豁免（联合键去重，属正常关联） |

## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **相关规则**：[[10_Reference/investing/logic/duplicate-merge]]（旧名，本规则细化 confidence 保留策略）
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/metrics/index|metrics/]] [[10_Reference/investing/valuations/index|valuations/]] [[10_Reference/investing/reports/index|reports/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
