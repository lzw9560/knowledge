---
type: logic
rule_id: COVERAGE-001
rule_type: 校验规则
target_entity: 全类型
severity: medium
condition: 任一实体类型（stocks/industries/metrics/valuations 等）实体数 < 3
action_on_violation: 触发灌入任务（从代码/数据源灌入种子数据）
source: AGENTS.md 分级工作流（图谱覆盖不足影响投研可用性）
created: 2026-09-07
---

# 规则：覆盖下限

## 规则定义

- **类型**：校验规则
- **适用实体**：全类型（按 type 分类统计）
- **严重级**：medium
- **条件**：`任一 type 的实体数 < 3`（如 metrics/ 只有 2 条记录 → 触发灌入）

## 触发条件

`vault_audit.py` 按 frontmatter `type` 字段分组统计每个类型的实体数。任一类型 < 3 触发灌入任务。

## 执行逻辑

```
type_counts = {}
for file in vault:
  if frontmatter.type:
    type_counts[type] += 1

for t, count in type_counts.items():
  if count < 3:
    生成灌入任务工单（.scratch/coverage-fill-{t}/）
    标注：该类型当前 {count} 个，目标 ≥ 3
    建议灌入源：
      - stocks: 从持仓/关注列表灌入
      - metrics/valuations: 从 stocks frontmatter 抄 PE/PB
      - reports/analysts: 从 eastmoney_reports 灌入占位
      - indices: 灌入常用宽基指数
```

Dataview 查询（类型计数）：

```dataview
TABLE length(rows) AS "实体数"
FROM "10_Reference/investing"
WHERE type != null
GROUP BY type AS "类型"
```

## 违反处置

- `action_on_violation`：触发灌入任务
- 灌入优先级：先建占位实体（status=placeholder）保证图谱连通，再逐步填充真实数据
- 占位实体必须标注 `status: placeholder`，避免被误用为真实数据源

## 阈值依据

- **3 个**：图谱可用性下限。某类型 < 3 时该类型无法支撑任何统计/对比分析。待 vault 成熟后可上调至 5 或 10。

## 关联

- 触发动作：[[actions/approve-entity]]（灌入的 inbox 实体走审批进正式区）
- 约束实体：全类型
- 来源：AGENTS.md 分级工作流（图谱覆盖是投研基础）
- 相关规则：[[logic/orphan-threshold]]（灌入后避免产生孤立项）、[[logic/duplicate-merge]]（灌入避免重复）
