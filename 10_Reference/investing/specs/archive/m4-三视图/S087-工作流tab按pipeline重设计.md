---
type: spec
number: S087
title: 工作流 tab 按 pipeline 步骤重设计
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S087 工作流 tab 按 pipeline 步骤重设计

## 摘要

设计被 S093 吸收实现

## 问题/目标

为改变研究人员在复杂实验工作流中迷失上下文、难以追溯步骤进度的问题，S087 提出将工作流标签页从简单的任务列表重构为按流水线阶段组织的递进式视图。核心设计决策是以阶段卡片承载步骤节点，在每个阶段内显式展示输入、关键处理与输出，并利用依赖边与状态高亮让当前进展一目了然。实现这一设计需要依赖前端可编排的步骤组件库、基于有向无环图的工作流状态管理模块，以及与后端 Pipeline 执行引擎的同步接口，确保界面定义与运行时执行结果实时联动。

## 关联

- 源文件：`specs/archive/m4-三视图/S087-工作流tab按pipeline重设计/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
