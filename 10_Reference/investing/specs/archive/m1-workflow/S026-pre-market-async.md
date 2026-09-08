---
type: spec
number: S026
title: pre-market 异步化
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S026 pre-market 异步化

## 摘要

盘前简报异步采集缓存 + 并发守卫

## 问题/目标

S026 旨在解决 pre-market 阶段因同步执行外部数据采集与因子计算而导致的延迟抖动和资源瓶颈问题，将原本串行阻塞的盘前流程改造为事件驱动、异步非阻塞的流水线。核心设计决策是引入任务队列与调度器，将行情快照拉取、财务数据补全、因子计算等环节解耦为独立的消息驱动任务，通过声明式工作流定义编排依赖关系，并采用背压控制保障系统在数据洪峰下的稳定性。关键技术组件包括基于 Apache Kafka 的异步消息总线、Redis 任务状态存储、Kubernetes Job 动态扩缩容的因子计算集群，以及一个轻量级的 DAG 执行引擎来调度和监控整个 pre-market 管道的进度。

## 关联

- 源文件：`specs/S026-pre-market-async/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
