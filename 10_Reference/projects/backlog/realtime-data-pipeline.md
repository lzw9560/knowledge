---
type: project
name: realtime-data-pipeline
title: 实时数据管道
status: 候选
created: 2026-09-07
---

# 实时数据管道

## 项目概述
实现 A 股行情/资金/题材的实时数据管道，替代当前的批处理拉取模式。目标是建一套从数据源 → 流处理 → 缓存 → 消费方的实时管线，支撑盘中实时信号生成与战法监控。

## 核心能力
- **实时行情接入**：WebSocket / 长连接接入东方财富/同花顺 Level-1 行情，毫秒级延迟
- **流处理**：实时计算技术指标（MA/MACD/量能）+ 战法触发判定（突破/反包/破位）
- **增量缓存**：实时数据写入 Redis，按股票/指标维度索引，TTL 控制过期
- **信号推送**：战法触发即推送到飞书/微信机器人 + 前端 WebSocket 推送
- **回放能力**：历史数据可"回放"到流处理管线，用于战法回测与模型训练

## 候选理由
- 当前 [[10_Reference/investing/specs/archive/m1-workflow/S026-pre-market-async|S026]] 是盘前批量拉取，盘中无法实时监控
- 实时管道是"盘中战法监控"的基础设施，但工程复杂度高，需先验证数据源稳定性
- [[10_Reference/investing/specs/archive/m1-workflow/S022-熔断器health读路径修复|S022]] 防封熔断是实时管道的前置依赖——实时拉取风控更严

## 技术栈候选
- 接入层：WebSocket / SSE / 长轮询
- 流处理：自研 asyncio 管道 / Kafka（若规模大）
- 缓存：Redis（[[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]]）
- 推送：飞书 webhook + 前端 WS

## 与投研的跨领域链接
- [[10_Reference/investing/strategies/|战法卡体系]] — 实时管道的核心消费方：战法触发判定
- [[10_Reference/investing/specs/archive/m1-workflow/S022-熔断器health读路径修复|S022 em_get 防封]] — 数据源风控前置依赖
- [[10_Reference/investing/specs/archive/m0-foundation/S017-A股涨跌预测模型栈|S017 预测模型栈]] — 实时特征喂给预测模型，盘中实时预测
- [[10_Reference/tech-learning/concepts/async-await|async/await]] — 流处理底层依赖 async 事件循环

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/projects/backlog/incremental-sync-automation]]
- [[10_Reference/tech-learning/architecture/event-driven]]
- [[10_Reference/tech-learning/concepts/async-await]]
- [[10_Reference/tech-learning/concepts/caching-strategy]]
- [[10_Reference/investing/strategies/]]
- [[10_Reference/meta/four-construct-ontology]]
