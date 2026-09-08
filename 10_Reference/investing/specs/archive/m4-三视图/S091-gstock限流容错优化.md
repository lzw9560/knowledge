---
type: spec
number: S091
title: gstock.global_indices 限流容错优化
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S091 gstock.global_indices 限流容错优化

## 摘要

加 KOSPI/SOX + push2 间歇限流记忆 + 异常诊断

## 问题/目标

本规范针对 gstock.global_indices 在突发流量下因上游数据源限流导致的大量请求失败与数据回退问题，构建了一套自适应的限流容错机制。核心设计决策是在采集链路中引入令牌桶本地限流与分级退避重试策略，同时将原先同步穿透的实时请求改造为异步非阻塞模式，以避免反向压力堆积。方案涉及的关键技术组件包括基于 Redis 的分布式令牌桶协调器、指数退避与抖动重试调度器，以及本地多级缓存降级策略，确保在配额耗尽时仍能返回可接受的近期数据。

## 关联

- 源文件：`specs/archive/m4-三视图/S091-gstock限流容错优化/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
