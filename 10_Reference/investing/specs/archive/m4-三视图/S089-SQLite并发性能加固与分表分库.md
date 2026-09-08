---
type: spec
number: S089
title: SQLite 并发性能加固与 seal_intraday 分表分库
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S089 SQLite 并发性能加固与 seal_intraday 分表分库

## 摘要

WAL+busy_timeout 落地；分表分库 deferred

## 问题/目标

S089 规范旨在解决 SQLite 在承载 seal_intraday 高频行情数据时因写锁竞争和单表数据膨胀引发的性能瓶颈。核心设计决策是实施基于交易日与证券代码的二级分库分表策略，同时将 SQLite 切换至 WAL 模式并辅以异步批量提交与连接池，以在保持轻量化的同时显著提升并发吞吐能力。该方案涉及的关键技术组件包括 SQLite WAL 与共享缓存机制、分库分表路由代理、连接

## 关联

- 源文件：`specs/archive/m4-三视图/S089-SQLite并发性能加固与分表分库/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
