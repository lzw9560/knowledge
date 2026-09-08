---
type: spec
number: S028
title: limitup-screener 修复（文案三态/trigger/因子层 conditions）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S028 limitup-screener 修复（文案三态/trigger/因子层 conditions）

## 摘要

9 测试 + 778 passed

## 问题/目标

该规格针对涨停筛选器因状态文案与底层触发逻辑、因子条件脱节导致的展示不一致问题，修复了“触发/未触发/数据缺失”三态文案的判定与显示。核心设计决策是将状态判定集中到 TriggerEvaluator 中，使其直接依据因子层定义的 conditions 实时计算并输出明确的 TriggerStatus 枚举，前端视图仅负责枚举到文案的映射，消除了分散的条件重复解析。关键组件包括 limitup-screener 前端展示组件、TriggerEvaluator 评估引擎以及因子定义库中的 conditions 配置，三者通过统一的接口契约确保筛选结果与文案的准确同步。

## 关联

- 源文件：`specs/S028-limitup-screener-fix/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
