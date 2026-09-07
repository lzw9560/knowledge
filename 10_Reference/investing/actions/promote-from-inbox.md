---
type: action
action_id: PROMOTE-001
action_type: 状态流转
trigger: inbox 实体通过质量门审核（confidence=low 的 LLM 抽取实体经人工 approved）后，迁移到正式区
target: inbox/, stocks/, industries/, concepts/
audit: true
status: stub
created: 2026-09-07
---

> [!info] ⚡ 动作
> **动作**：`PROMOTE-001`  **类型**：状态流转
> **触发**：`inbox 实体通过质量门审核（confidence=low 的 LLM 抽取实体经人工 approved）后，迁移到正式区`  **目标**：`inbox/, stocks/, industries/, concepts/`
>
> **触发自**：[[logic/]]

## 📋 动作定义

- **类型**：状态流转
- **触发条件**：`inbox/` 下的实体通过审查（人工/LLM 质量门），需迁移到正式区
- **目标实体**：`inbox/` 下的候选实体 → 对应正式类型文件夹（`stocks/`/`industries/`/`concepts/` 等）
- **审计**：true（记录迁移前后快照 + approved_date）


## 🔧 执行步骤

1. 校验 inbox 实体 frontmatter 完整性（必填字段：type/code/name）
2. 调用 `move_note(old=inbox/xxx.md, new=stocks/xxx.md)` 迁移到正式区（走 [[logic/实体改名]] 的 move_note 约束）
3. 更新实体 `status` 字段（candidate → approved）+ 写入 `approved_date`
4. 在 `reviews/` 记录审批快照（who/when/inbox_path/formal_path）


## 🔍 审计点

- 执行前状态：inbox 下的候选实体路径 + frontmatter
- 执行后状态：正式区路径 + status=approved + approved_date
- 异常处置：迁移失败（目标路径已存在/必填字段缺失）→ 回滚 + 告警


## 🔗 关联

- **触发自**：[[logic/]]
- **作用于**：[[stocks/]]
- **执行记录**：[[reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
