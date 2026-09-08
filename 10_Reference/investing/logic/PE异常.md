---
type: logic
rule_id: PE-001
rule_type: 校验规则
target_entity: stocks
severity: high
condition: pe_ttm < 0 OR pe_ttm > 500
action_on_violation: 标记 data_suspect
source: ora-3 诊断 §2.5（PE 静态值不可信）+ logic/index.md 示例
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`PE-001`  **类型**：校验规则
> **严重级**：high  **适用实体**：stocks
>
> **违反处置**：`标记 data_suspect`

## 📋 规则定义

- 类型：`校验规则`
- 适用实体：`stocks`
- 严重级：`high`


## ⚡ 触发条件

股票实体的 frontmatter `pe_ttm` 字段值为负数（公司亏损，PE 无意义）或异常高（>500，疑似数据错误或特殊股本结构）。


## 🔧 执行逻辑

```
对每个 type = "stock" 的实体：
  if pe_ttm < 0:
    标记 data_suspect: true
    suspect_reason: "PE 为负（公司亏损），PE 指标无意义"
  elif pe_ttm > 500:
    标记 data_suspect: true
    suspect_reason: "PE 异常高（>500），疑似数据错误或需人工复核"
```

Dataview 查询（在审查脚本或 MOC 渲染时用）：

```dataview
TABLE WITHOUT ID
  code AS "代码", name AS "名称", pe_ttm AS "PE(TTM)"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND file.name != "index" AND (pe_ttm < 0 OR pe_ttm > 500)
SORT pe_ttm ASC
LIMIT 50
```


## ⚠️ 违反处置

- `action_on_violation`：标记 `data_suspect: true` + `suspect_reason`
- 标记后该实体不应作为"PE 排序""估值对比"等场景的数据源
- 应触发 [[10_Reference/investing/actions/index|actions/]] 的人工复核流程（待建）


## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
