---
type: spec
number: S070
title: intraday 数据采集管道
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S070 intraday 数据采集管道

## 摘要

盘中 ephemeral → 盘后离线 §44 60日复验窗口 + 战法因子派生（并入原 S080）

## 问题/目标

S070 旨在为 Vibe-Research 构建一条高可用的日内数据采集管道，解决多源异构实时行情数据难以统一接入、清洗和可靠存储的问题，确保下游研究环境能获得完整的分钟级与秒级快照。核心设计决策是采用事件驱动的流式处理架构，将数据采集、标准化、落库与分发完全解耦，并通过幂等写入、断点续传和两级缓存策略来保障数据在任何异常场景下不丢不重。该管道涉及的关键技术组件包括 Apache Kafka 作为消息总线、Apache Flink 负责实时流计算与复杂事件处理、ClickHouse 用于海量时序数据的存储与查询，并辅以 Redis 管理元数据缓存和 Offset 状态，最终形成一条端到端观测、可回溯的标准化数据供应链。

## 关联

- 源文件：`specs/archive/m3-strategy/S070-intraday采集管道/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
