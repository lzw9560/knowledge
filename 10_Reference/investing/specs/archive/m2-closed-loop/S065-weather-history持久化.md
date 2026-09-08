---
type: spec
number: S065
title: weather_history 持久化
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S065 weather_history 持久化

## 摘要

盘后落 weather_state 快照 + 五因子明细（W1 证据层前置，零 em_get）

## 问题/目标

S065 为 Vibe-Research 平台引入天气历史数据的持久化能力，解决当前实时天气数据无留存、无法进行趋势分析、回溯验证与模型训练的问题。核心设计决策采用以城市和小时为粒度的时序存储模型，基于时间窗口实现自动分层归档与过期清理，同时利用预聚合的物化视图加速常见粒度的统计查询。该方案以 PostgreSQL 搭配 TimescaleDB 超表作为存储引擎，通过计划任务从外部天气 API 持续摄取并转换数据，结合 Hypertable 的分区与压缩策略来平衡查询性能与长期存储成本。

## 关联

- 源文件：`specs/S065-weather-history持久化/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
