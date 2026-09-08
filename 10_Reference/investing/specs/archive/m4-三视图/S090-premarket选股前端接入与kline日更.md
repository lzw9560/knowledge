---
type: spec
number: S090
title: premarket_selection 前端接入 + kline 日更
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S090 premarket_selection 前端接入 + kline 日更

## 摘要

接 endpoint + live kline 日更 + 风控 + 前端

## 问题/目标

本规范旨在解决盘前选股模块缺少前端交互界面与K线数据无法每日自动更新的问题，使研究成果能够以直观、可操作的方式交付给用户。核心设计决策是将选股策略封装为参数化的RESTful API，前端通过动态筛选面板驱动异步请求并分页展示结果，同时为K线数据建立独立的日更调度流水线，实现盘后自动拉取与增量存储。涉及的关键技术组件包括基于FastAPI的选股引擎、Vue3与ECharts构建的可视化前端，以及由APScheduler和MySQL组成的定时数据同步与持久化方案。

## 关联

- 源文件：`specs/archive/m4-三视图/S090-premarket选股前端接入与kline日更/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
