---
type: action
action_id: APPROVE-001
action_type: 状态流转
trigger: inbox 实体通过审查，需迁移到正式区
target: inbox/, stocks/, industries/, concepts/
audit: true
created: 2026-09-07
confidence: high
source: logic_rules
---

> [!info] ⚡ 动作
> **动作**：`APPROVE-001`  **类型**：状态流转
> **触发**：`inbox 实体通过审查，需迁移到正式区`  **目标**：`inbox/, stocks/, industries/, concepts/`
>
> **触发自**：[[10_Reference/investing/logic/index|logic/]]

## 📋 动作定义

- 类型：`状态流转`
- 触发：`inbox 实体通过审查，需迁移到正式区`
- 目标：`inbox/, stocks/, industries/, concepts/`


## 🔧 执行步骤

1. 校验 inbox 实体 frontmatter 完整性（必填字段：type/code/name）
2. 调用 `move_note(old=inbox/xxx.md, new=stocks/xxx.md)` 迁移到正式区（走 [[10_Reference/investing/logic/实体改名]] 的 move_note 约束）
3. 更新实体 `status` 字段（candidate → approved）
4. 在 `reviews/` 记录审批快照（who/when/inbox_path/formal_path）


## 🔍 审计点

- 执行前状态：inbox 下的候选实体路径 + frontmatter
- 执行后状态：正式区路径 + status=approved
- 异常处置：迁移失败（目标路径已存在/必填字段缺失）→ 回滚 + 告警


## 🔗 关联

- **触发自**：[[10_Reference/investing/logic/index|logic/]]
- **作用于**：[[10_Reference/investing/stocks/index|stocks/]]
- **执行记录**：[[10_Reference/investing/reviews/index|reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
