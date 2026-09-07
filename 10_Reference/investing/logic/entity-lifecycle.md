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

待补充


## 🔧 执行逻辑

待补充


## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| 不经 inbox 直接进正式区 | high | 移回 inbox + 走晋级流程 |
| 正式区直接删文件 | critical | 从 git 恢复 + 归档而非删除 |
| inbox 滞留 > 14 天未处置 | low | 标 rejected |
| 时点数据放 frontmatter | high | 移到 valuations/ 实体（[[logic/static-value-ban]]） |


## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[stocks/]]
- **来源决策**：[[specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
