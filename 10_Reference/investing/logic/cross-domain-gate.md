---
type: logic
rule_id: CROSS-DOMAIN-GATE-001
rule_type: 准入闸
target_entity: 跨域链接
severity: medium
condition: 跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建
action_on_violation: 跨域链接数 / 单域链接数 ≥ 20% → 报 medium（防"什么都记但什么都不深"）
source: ora-3 §4
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`CROSS-DOMAIN-GATE-001`  **类型**：准入闸
> **严重级**：medium  **适用实体**：跨域链接
>
> **违反处置**：跨域链接数 / 单域链接数 ≥ 20% → 报 medium

## 📋 规则定义

- 类型：`准入闸`
- 适用实体：`跨域链接`
- 严重级：`medium`

## ⚡ 触发条件

投研方法论与其他知识域的"同构"链接准入判据：

1. 跨域实体必须有 **≥ 2 个具体实例**（不能只有一个模糊类比）
2. 必须有 **≥ 1 条 invariant**（不变量——在两个域都成立的约束）
3. 跨域链接数 / 单域链接数 **< 20%**（防"什么都记但什么都不深"）

## 🔗 关联

- 被引用于：[[10_Reference/investing/MOC]]（跨领域链接段）
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
