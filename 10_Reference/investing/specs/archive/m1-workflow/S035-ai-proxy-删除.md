---
type: spec
number: S035
title: ai_proxy 删除（死代码清理）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S035 ai_proxy 删除（死代码清理）

## 摘要

删 ai_proxy 路由 + 死代码清理

## 问题/目标

该规格旨在解决 Vibe-Research 项目中 ai_proxy 模块在多次架构演进后已成为无任何调用方的死代码，持续造成代码库膨胀与认知负担的问题。核心设计决策是通过静态引用分析与全量测试确认该模块与当前 AI 接口链路完全解耦后，执行物理删除，并同步清理关联的配置项、测试用例及构建脚本，以保证零残留且不影响现有功能。涉及的关键技术组件包括 ai_proxy 的 HTTP 请求转发逻辑、上游适配层、中间件链，以及相关的环境变量与 CI 部署描述。

## 关联

- 源文件：`specs/S035-ai-proxy-删除/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec · [plan](S035-ai-proxy-删除/plan.md) · [tasks](S035-ai-proxy-删除/tasks.md)
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
