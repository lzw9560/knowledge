---
type: logic
rule_type: 推断规则
target_entity: events
severity: medium
created: 2026-09-07
---

> [!info] ⚙️ 规则
> **规则**：``  **类型**：推断规则
> **严重级**：medium  **适用实体**：events
>
> **违反处置**：``

## 📋 规则定义

| # | 链 | 类型 | 验证状态 | 验证方式 |
|---|---|---|---|---|
| 1 | `[[events/涨停池]]` → `[[stocks/*]]` 涨幅 | 因果 | 待验证 | 涨停池入选 vs 未入选次日收益对比 |
| 2 | `[[dragon-tiger/席位]]` → `[[stocks/*]]` 次日走势 | 因果（待验证） | 未验证 | 龙虎榜净买入 vs 次日涨跌幅回归 |
| 3 | `[[concepts/*]]` ↔ `[[stocks/*]]` 成分股联动 | 相关 | 已知相关 | 板块涨跌幅 vs 成分股等权平均相关系数 |
| 4 | `[[analysts/*]]` 评级调整 → `[[stocks/*]]` 股价波动 | 因果（待验证） | 未验证 | 评级变更事件研究法（CAR） |
| 5 | `[[metrics/营收]]` → `[[valuations/PE]]` 估值切换 | 因果 | 待验证 | 营收增速变化 vs PE 估值切换时点 |
| 6 | `[[strategies/战法]]` 匹配 → `[[events/涨停]]` | 因果（待验证） | 未验证 | 战法命中样本 vs 随机基准的涨停率 lift |


## ⚡ 触发条件

待补充


## 🔧 执行逻辑

待补充


## ⚠️ 违反处置

- ``


## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[stocks/]]
- **来源决策**：[[specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
