---
type: logic
rule_id: SOURCE-DRIFT-001
rule_type: 漂移检测
target_entity: 全实体
severity: medium
status: stub
created: 2026-09-07
---

> [!info] ⚙️ 规则
> **规则**：`SOURCE-DRIFT-001`  **类型**：漂移检测
> **严重级**：medium  **适用实体**：全实体

## 📋 规则定义

源数据漂移检测规则：当实体 frontmatter 字段与上游数据源（如 akshare/eastmoney）当前值不一致时触发。

## ⚡ 触发条件

- 实体 `code` 字段在上游已变更（如退市/更名）
- 实体 `industry`/`concept` 分类与上游板块归属不一致

## 🔗 关联

- **来源**：[[reviews/audit-procedure]]
- **关联规则**：[[logic/static-value-ban]] / [[logic/broken-link-grading]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
