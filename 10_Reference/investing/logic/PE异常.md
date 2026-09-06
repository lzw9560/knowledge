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
---

# 规则：PE异常

## 规则定义

- **类型**：校验规则
- **适用实体**：[[stocks/]]
- **严重级**：high
- **条件**：`pe_ttm < 0 OR pe_ttm > 500`

## 触发条件

股票实体的 frontmatter `pe_ttm` 字段值为负数（公司亏损，PE 无意义）或异常高（>500，疑似数据错误或特殊股本结构）。

## 执行逻辑

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
TABLE code AS "代码", name AS "名称", pe_ttm AS "PE(TTM)"
FROM "stocks"
WHERE type = "stock" AND (pe_ttm < 0 OR pe_ttm > 500)
SORT pe_ttm ASC
```

## 违反处置

- `action_on_violation`：标记 `data_suspect: true` + `suspect_reason`
- 标记后该实体不应作为"PE 排序""估值对比"等场景的数据源
- 应触发 [[actions/]] 的人工复核流程（待建）

## 阈值依据

- **PE < 0**：硬规则，公司亏损时 PE 数学上无意义。无异议。
- **PE > 500**：⚠️ **此阈值为初值，待数据校准**。ora-3 诊断未明确诊断此阈值，按 AGENTS.md「数据支撑优先」要求，应统计 A 股 PE 分布的 99 分位后再定。当前 500 是保守初值（覆盖绝大多数异常，误报率低）。

## 关联

- 触发动作：[[actions/]]（人工复核流程，待建）
- 约束实体：[[stocks/]]
- 来源：ora-3 诊断 §2.5（`docs/knowledge-graph-improvement-vision.md` line 285：PE 是不可信的静态值）
- 相关规则：[[static-value-ban]]（ora-3 D8-9 规划，frontmatter 禁止放时点数据——PE 应走 valuations/ 实体，本规则是过渡期校验）
