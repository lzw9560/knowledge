---
type: spec
number: S078
title: 涨停历史 snapshot 数据地基
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S078 涨停历史 snapshot 数据地基

## 摘要

snapshot 表 + 15日 backfill + daily task cron `0 16` 累积供 B1 复验

## 问题/目标

为解决涨停历史分析中数据缺失、口径不统一和回溯困难的问题，S078 设计了一套标准化的涨停快照数据地基。核心设计决策是采用事件溯源模式，从逐笔成交与行情快照中精确还原首次涨停时间、炸板次数和最终封单状态，并以幂等写入确保数据可重放、可追溯。该 spec 涉及基于 Flink 的实时与离线计算链路、ClickHouse 列存表存储快照，以及配套的数据质量校验组件，为后续情绪周期、龙头识别等研究提供稳固的事实基础。

## 关联

- 源文件：`specs/archive/m3-strategy/S078-涨停历史snapshot数据地基/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
