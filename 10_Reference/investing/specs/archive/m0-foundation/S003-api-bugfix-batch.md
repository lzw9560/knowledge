---
type: spec
number: S003
title: 后端 API 冒烟测试缺陷修复批次
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S003 后端 API 冒烟测试缺陷修复批次

## 摘要

API 缺陷批量修复（含 value_funnel 等）

## 问题/目标

本规格针对 Vibe-Research 后端 API 冒烟测试中集中暴露的缺陷进行系统性修复，旨在解决因边界条件校验缺失、异步任务处理异常及错误响应格式不一致而导致的冒烟测试通过率持续偏低的问题。核心设计决策采用缺陷分级修复策略，优先处理阻断核心研究数据检索与实验提交流程的 P0 缺陷，并同步抽取通用异常处理中间件以统一错误码和响应体结构，同时强制要求每个修复点均补充对应的自动化回归用例。涉及的关键技术组件包括基于 FastAPI 的后端服务、Pytest 与 httpx 组合的冒烟测试套件，以及通过 GitHub Actions 触发的持续集成流水线，确保修复后的接口在部署前自动通过冒烟验证。

## 关联

- 源文件：`specs/S003-api-bugfix-batch/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec · [tasks](S003-api-bugfix-batch/tasks.md)
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
