---
type: logic
rule_id: 
rule_type: 校验规则
target_entity: 
severity: high
condition: 
action_on_violation: 标记 data_suspect
source: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

> [!info] ⚙️ 规则
> **规则**：`rule_id`  **类型**：rule_type  **严重级**：severity
> **适用实体**：target_entity
> 
> **违反处置**：`action_on_violation`

## 📋 规则定义

- **类型**：`rule_type`（校验规则 / 状态机 / 推断规则 / 自动化规则）
- **适用实体**：`target_entity`（如 stocks / reports / events）
- **严重级**：`severity`（critical / high / medium / low）
- **条件**：`condition`（可机器判定的表达式）

## ⚡ 触发条件

（描述规则何时触发，含示例）

## 🔧 执行逻辑

（规则满足时做什么，含伪代码或 Dataview 查询）

## ⚠️ 违反处置

- `action_on_violation`：违反时执行的动作（如标记 data_suspect / 触发 [[actions/]]）

## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[<target_entity>/]]
- **来源决策**：[[specs/]]（如适用）
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
