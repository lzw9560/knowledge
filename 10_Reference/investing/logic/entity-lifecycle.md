---
type: logic
rule_id: ENTITY-LIFECYCLE-001
rule_type: 状态机
target_entity: 全类型
severity: high
condition: 实体从创建到归档/删除的状态流转，强制走 inbox 质量门 + approved 字段
action_on_violation: 不经 inbox 直接进正式区 → 报 high；正式区直接删 → 报 critical
source: ora-3 §1.3（inbox stub 通道）+ AGENTS.md 工程底线（不臆造数据 / 私有数据隔离）
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`ENTITY-LIFECYCLE-001`  **类型**：状态机
> **严重级**：high  **适用实体**：全类型
>
> **违反处置**：`不经 inbox 直接进正式区 → 报 high；正式区直接删 → 报 critical`

## 📋 规则定义

- 类型：`状态机`
- 适用实体：`全类型`
- 严重级：`high`


## ⚡ 触发条件

- 实体创建时（inbox → approved → 正式区）
- 实体更新时（frontmatter 字段变更）
- 实体归档时（从正式区 → archive）
- `daily_audit.py` 每日扫描 inbox 滞留 > 14 天的实体

## 🔧 执行逻辑

```
状态流转: inbox → approved → published → archived/deleted

for file in vault:
    state = get_entity_state(file)  # inbox / approved / published / archived
    if state == "inbox":
        age = days_since(file.created)
        if age > 14:
            mark_rejected(file)  # 标 rejected
    elif state == "published":
        if has_time_point_data_in_frontmatter(file):
            report(HIGH, "时点数据放 frontmatter", file)
    elif state == "deleted":
        report(CRITICAL, "正式区直接删文件", file)
        restore_from_git(file)
```

- inbox 通道：LLM 抽取的实体先进 inbox/，人工审核通过后才进正式区
- approved 字段：frontmatter 加 `approved: true` 标记已通过质量门
- 归档优先：正式区实体过时不再删文件，移到 archive/ 子目录


## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| 不经 inbox 直接进正式区 | high | 移回 inbox + 走晋级流程 |
| 正式区直接删文件 | critical | 从 git 恢复 + 归档而非删除 |
| inbox 滞留 > 14 天未处置 | low | 标 rejected |
| 时点数据放 frontmatter | high | 移到 valuations/ 实体（[[10_Reference/investing/logic/static-value-ban]]） |


## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：4 个 · **入链**：6 个
