---
type: spec
number: S069
title: 每日 forward_test 管道 + T+1 收益回填
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S069 每日 forward_test 管道 + T+1 收益回填

## 摘要

forward_test 流程框架打通；待 prod baostock 验证 live 日积

## 问题/目标

S069 旨在解决当前策略研究流程中，每日生成的 forward-test 预测无法及时获得 T+1 实际收益反馈、导致策略迭代闭环断裂的问题。核心设计决策是引入一条全自动化的日频管道，将当日收盘后产出的预测信号与次一交易日结算后回填的真实收益在统一时间轴上严格对齐，并以“软删除+版本化”的方式管理收益数据的重复回填与修正。该方案深度依赖基于 Apache Airflow 的调度引擎、列式存储的收益特征库，以及与回测框架共享的持仓-收益匹配校验层，确保回填数据的完整性和可复现性。

## 关联

- 源文件：`specs/archive/m3-strategy/S069-每日forward_test管道/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
