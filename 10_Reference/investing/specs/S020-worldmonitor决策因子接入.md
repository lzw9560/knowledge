---
type: spec
number: S020
title: worldmonitor 决策因子接入（全球宏观/地缘/另类数据）
status: 已实现
created: 2026-09-06
---

# S020 worldmonitor 决策因子接入

## 问题/目标

S018 特征层缺另类数据层（全球宏观/地缘/另类）。需通过远程 MCP 互补另类数据层，FRED 仍主源。

## 核心决策

远程 MCP 互补另类数据层接 newsradar/market/特征栈，Fred 仍主源。worldmonitor 作为 MCP 服务端，提供 newsradar（新闻雷达）/ market（全球指数）/ 特征栈（另类指标），与本地 FRED macro 互补不替代。

## 受影响文件

- `backend/data/sources/worldmonitor.py`（MCP 客户端）
- `backend/macro.py`（互补接入）
- `backend/ml/features/`（特征栈消费）

## 验收标准

- P0–P6 落地（P7 live 冒烟待联网）
- MCP 互补层接 newsradar/market/特征栈
- FRED 仍主源

## 关联

- 上游特征层：[[specs/S018]]
- 宏观主源：[[specs/S019]]（FRED 7 系列，worldmonitor 互补不替代）
- 下游模型：[[specs/S017]]
- 数据源：[[data-sources/worldmonitor]] [[data-sources/rss-newsradar]] [[data-sources/fred]]
- 影响实体：[[indices/]]（全球指数） [[events/]]（地缘新闻）
- 源文件：`specs/archive/m0-foundation/S020-worldmonitor决策因子接入/spec.md`
