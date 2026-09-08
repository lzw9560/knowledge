---
type: spec
number: S067
title: advisory 端点性能优化
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S067 advisory 端点性能优化

## 摘要

advisory P0-P3 全落地（缓存+预热+并发+批量+超时降级），>40s→0.34s

## 问题/目标

本 spec 旨在解决 advisory 端点在高并发下因实时聚合大量研究数据而导致的响应延迟和吞吐瓶颈问题。核心设计决策是放弃请求内同步计算，改为通过后台管道预计算咨询快照，并以多层缓存加 stale-while-revalidate 语义来对外服务，从而将数据生产与请求服务完全解耦。涉及的关键技术和组件包括用于分布式热缓存的 Redis、承载最新聚合结果的 PostgreSQL 物化视图，以及基于 Apache Kafka 的数据变更事件触发视图增量刷新机制，确保近乎实时的数据新鲜度并消除请求线程阻塞。

## 关联

- 源文件：`specs/S067-advisory-perf/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
