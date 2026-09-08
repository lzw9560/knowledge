---
type: spec
number: S077
title: 首板流剔除层 §44 lift 验证（B1）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S077 首板流剔除层 §44 lift 验证（B1）

## 摘要

独立研究脚本 + 30天 smoke 通；剔除层 lift 1.01-1.06 待 120 天全量复验

## 问题/目标

本 spec 解决首板流剔除层中规则 §44 在 B1 阶段实盘环境下 lift 指标可能衰变、导致无效剔除的问题，急需建立一套可复现的验证闭环。核心设计决策是以滚动时间窗口累积统计量，结合自助法构建 lift 的 95% 置信区间，并设定区间下界低于 1.0 时自动触发规则失效告警，从而避免人工误判。涉及的关键组件包括基于 Flink 的首板流实时处理管道、动态规则引擎、lift 在线计算模块

## 关联

- 源文件：`specs/archive/m3-strategy/S077-首板流剔除层lift验证/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
