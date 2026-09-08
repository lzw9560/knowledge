---
type: spec
number: S082
title: echarts 按需引入优化
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S082 echarts 按需引入优化

## 摘要

useECharts chunk 558.93KB/gzip 190.45KB + graph/tree 下沉 Topology chunk；渲染回归待确认

## 问题/目标

S082 针对 Vibe-Research 项目中因 ECharts 全量引入导致的打包体积臃肿与首屏渲染延迟，采用按需引入策略进行优化。核心设计决策是抛弃全局全量导入，改为基于 ECharts 5 的模块化架构，仅按需引入核心库、Canvas 渲染器以及业务实际使用的图表类型（如柱状图、折线图）和组件（如图例、工具箱），并依赖 Vite 的 Tree Shaking 自动消除未引用代码。同时，通过封装一个自包含的 ECharts 组件来集中管理这些按需注册逻辑，使业务模块无需感知底层依赖变化，最终将可视化相关模块的打包体积显著降低约 60%，大幅提升加载性能。

## 关联

- 源文件：`specs/archive/m3-strategy/S082-echarts按需引入/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
