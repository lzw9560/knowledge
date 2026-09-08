---
type: spec
number: S074
title: market_phase 统一判定与盘后桩对接
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S074 market_phase 统一判定与盘后桩对接

## 摘要

盘前盘后时段统一（当日收盘→次日开盘）+ post-market 桩对接 + 前端状态机对齐（→ S092 三视图）

## 问题/目标

S074 针对当前盘中市场阶段判定与盘后固定价格交易（盘后桩）数据相互割裂的问题，统一了全时段的市场微结构阶段定义，使得盘后桩不再是孤立的数据孤岛。核心设计决策是将盘后桩拆分为“盘后参考价收集”、“盘后撮合”和“盘后闲置”三个子阶段，并纳入统一的 MarketPhase 状态机，由 PhaseCoordinator 根据撮合事件和交易所规则自动切换。该方案涉及扩展的 MarketPhase 枚举与状态迁移逻辑、盘后桩行情适配器，以及事件时间对齐与重放引擎，确保盘中与盘后数据在回测和实盘信号中具备一致的阶段语义。

## 关联

- 源文件：`specs/archive/m3-strategy/S074-market_phase统一判定/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
