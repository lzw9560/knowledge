---
type: spec
number: S037
title: gene DB 路径迁移（三库 + winrate 统一到 .vibe-research/）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S037 gene DB 路径迁移（三库 + winrate 统一到 .vibe-research/）

## 摘要

gene_scores/winrate/market_data 三库统一 VR_DATA_DIR，迁移完整

## 问题/目标

本次 spec 要解决的核心问题是基因数据库及其相关胜率数据当前分散在项目多处，缺少统一的存储约定，导致路径管理、备份和部署时的复杂性上升。我们做出的核心设计决策是将三个基因库（core、variants、history）以及 winrate 实证数据全部迁移到项目根目录下的 `.vibe-research/` 隐藏目录中，并按子目录进行逻辑分组，同时引入一个可配置的路径根变量，使得本地开发与容器化部署能共享同一套目录结构。迁移过程中涉及的关键组件包括基于路径管理器的文件定位与迁移脚本、数据库连接层对新的绝对/相对路径的适配，以及兼容旧路径的自动回退机制，确保现有实验流程不中断。

## 关联

- 源文件：`specs/S037-gene-db-迁移/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec · [plan](S037-gene-db-迁移/plan.md) · [tasks](S037-gene-db-迁移/tasks.md)
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
