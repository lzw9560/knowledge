---
type: project
name: Vibe-Research
title: 私人投研助理
status: 活跃
github: 
created: 2026-09-07
---

# Vibe-Research

## 项目概述
私人投研助理。全栈应用：FastAPI 后端 + React/TypeScript 前端。本知识图谱 vault 就是 Vibe-Research 项目的**语义层**——把代码里的实体、spec 决策、战法、数据源链接成可导航的知识图谱。

## 技术栈
- 后端：[[10_Reference/tech-learning/frameworks/fastapi|FastAPI]] + [[10_Reference/tech-learning/languages/python|Python]]
- 前端：[[10_Reference/tech-learning/frameworks/react|React]] + [[10_Reference/tech-learning/languages/typescript|TypeScript]]
- 容器化：10_Reference/tech-learning/tools/Docker|[[Docker]]
- 版本控制：10_Reference/tech-learning/tools/Git|[[Git]]

## 架构决策
- [[10_Reference/investing/specs/S006-系统重写纲领|S006 系统重写纲领]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007 契约层]]
- [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移|S008 后端数据层迁移]]
- [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口|S011 调度收口]]（事件驱动架构，见 10_Reference/tech-learning/architecture/事件驱动架构|事件驱动]]）

## 数据源
- 10_Reference/investing/data-sources/AkShare|[[akshare]]
- [[10_Reference/investing/data-sources/mootdx|mootdx]]
- 10_Reference/investing/data-sources/东财 push2|东财 [[push2]]

## 关联项目
- [[10_Reference/projects/active/TradingAgents]] — TradingAgents fork（共享 4 数据源）
- 10_Reference/investing/specs/a-Plate-Sentinel项目|a-Plate-[[Sentinel]] — 互补项目（情绪监控 vs 全栈看板）

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/investing/MOC]] — 投研知识图谱语义层入口
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/investing/specs/S006-系统重写纲领]]
- [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口]]
- [[10_Reference/meta/四构件本体方法论]]
