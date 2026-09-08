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
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`COVERAGE-001`  **类型**：校验规则
> **严重级**：medium  **适用实体**：全类型
>
> **违反处置**：`触发灌入任务（从代码/数据源灌入种子数据）`

## 📋 规则定义

- 类型：`校验规则`
- 适用实体：`全类型`
- 严重级：`medium`


## ⚡ 触发条件

`vault_audit.py` 按 frontmatter `type` 字段分组统计每个类型的实体数。任一类型 < 3 触发灌入任务。


## 🔧 执行逻辑

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

<!-- dataview-precompiled:9c9945e86630 -->
| 文件 | 实体数 |
|---|---|
| [[10_Reference/investing/actions/approve-entity]] | 6 |
| [[10_Reference/investing/agents/fundamental_analyst]] | 8 |
| [[10_Reference/investing/analysts/Austin Liang-招银国际]] | 397 |
| [[10_Reference/investing/concepts/5G概念]] | 131 |
| [[10_Reference/investing/data-sources/akshare]] | 18 |
| [[10_Reference/investing/dragon-tiger/000019-2026-09-02]] | 42 |
| [[10_Reference/investing/events/2026-09-01-涨停池]] | 21 |
| [[10_Reference/investing/inbox/20260907-122605-industry-海工]] | 5 |
| [[10_Reference/investing/indices/000001]] | 6 |
| [[10_Reference/investing/industries/IT服务]] | 127 |
| [[10_Reference/investing/logic/LLM抽取质量门]] | 25 |
| [[10_Reference/investing/metrics/000001-latest]] | 402 |
| [[10_Reference/investing/reports/000001-2026-04-26-2025年报及2026一季报点评：收入利]] | 393 |
| [[10_Reference/investing/reviews/2026-09-06-ci-audit]] | 6 |
| [[10_Reference/investing/reviews/audit-procedure]] | 1 |
| [[10_Reference/investing/specs/DEC-001]] | 5 |
| [[10_Reference/investing/specs/S004-candidates-funnel-performance]] | 102 |
| [[10_Reference/investing/specs/a-plate-sentinel-project]] | 4 |
| [[10_Reference/investing/indices/000001]] | 412 |
| [[10_Reference/investing/strategies/break_reseal]] | 14 |
| [[10_Reference/investing/templates/valuation]] | 402 |
<!-- /dataview-precompiled -->


## ⚠️ 违反处置

- `action_on_violation`：触发灌入任务
- 灌入优先级：先建占位实体（status=placeholder）保证图谱连通，再逐步填充真实数据
- 占位实体必须标注 `status: placeholder`，避免被误用为真实数据源


## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
