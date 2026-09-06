---
type: spec
number: S094
title: 战法分类与双 pipeline 统一底座重构
status: 已实现
created: 2026-09-06
---

# S094 战法分类与双 pipeline 重构

## 问题/目标

战法 pipeline 单一处理无法区分涨停/非涨停场景，需双 pipeline 分流 + 统一底座重构。

## 核心决策

涨停/非涨停双 pipeline + `score_candidates` 分流 + confidence 统一 + kline 扩容 + 5 根因修复。战法先分类（涨停/非涨停），再走各自 pipeline，`score_candidates` 按分类分流，confidence 统一口径，kline 数据扩容支持。

## 受影响文件

- `backend/strategies/pipeline.py`（双 pipeline）
- `backend/funnel.py`（`score_candidates` 分流）
- `backend/strategies/confidence.py`（confidence 统一）
- `backend/data/sources/kline.py`（kline 扩容）

## 验收标准

- 涨停/非涨停双 pipeline 就位
- `score_candidates` 分流
- confidence 统一口径
- kline 扩容
- 5 根因修复
- 2269 passed

## 关联

- 上游：[[specs/S066-策略特定漏斗架构重构]]（策略特定漏斗） / [[specs/S086-涨停战法pipeline统一架构]]（涨停战法 pipeline 统一架构）
- 衔接后续：[[specs/S097-逐条件因子过滤]]（逐条件因子过滤） / [[specs/S100-战法卡片对齐]]（战法卡片对齐）
- 影响实体：[[stocks/]] [[events/]]（涨停分类）
- 战法：[[strategies/platform_breakout]] [[strategies/first_plate]] [[strategies/low_absorption]] [[strategies/reverse_package]]
- 数据源：[[data-sources/akshare]] [[data-sources/eastmoney-push2]]
- 源文件：`specs/archive/m5-战法细化/S094-战法分类与双pipeline重构/spec.md`
