---
type: action
action_id: 
action_type: CRUD
trigger: 
target: 
audit: true
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] ⚡ 动作
> **动作**：`action_id`  **类型**：action_type  **审计**：audit
> **触发条件**：trigger  **目标实体**：target
> 
> **触发自**：[[logic/]]

## 📋 动作定义

- **类型**：`action_type`（CRUD / 状态流转 / 链接维护 / 审计快照）
- **触发条件**：`trigger`（何时执行此动作）
- **目标实体**：`target`（作用于哪些实体类型）
- **审计**：`audit`（true/false，是否记录执行快照）

## 🔧 执行步骤

1. （步骤一）
2. （步骤二）
3. （步骤三）

## 🔍 审计点

- 执行前状态：（快照或链接）
- 执行后状态：（快照或链接）
- 异常处置：（失败时回滚/告警）

## 🔗 关联

- **触发自**：[[logic/]]（哪条规则触发此动作）
- **作用于**：[[<target>/]]
- **执行记录**：[[reviews/]]
- **出链**：0 个 · **入链**：0 个
