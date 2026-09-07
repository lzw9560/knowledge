---
type: project
name: semantic-search
title: 知识图谱语义搜索
status: backlog
created: 2026-09-07
confidence: high
---

# semantic-search

## 项目概述
为 Obsidian 知识图谱（投研/技术/读书跨领域）加语义搜索能力——自然语言查询 → 向量召回 → 实体定位。解决"实体多了之后，纯 `[[]]` 链接 + 关键词搜索找不到'语义相近但无直接链接'的实体"问题。例如查"防封策略"应召回 em_get 限流、熔断器、优雅降级、暴风雨战法仓位×0.3 等跨领域实体。

## 技术栈
- 向量化：embedding 模型（本地 bge-m3 / 或 API）
- 向量库：可复用 Vibe-Research 的向量基础设施，或轻量 SQLite + sqlite-vec
- 索引范围：投研实体（stocks/strategies/specs/data-sources）+ 读书笔记 + 技术概念
- 查询接口：MCP tool 或 Vibe-Research API

## 与其他项目的关系
- 依赖 [[10_Reference/projects/active/knowledge-graph|knowledge-graph vault]]（被索引的语料源）
- 支撑 [[10_Reference/projects/active/knowledge-graph-bot|knowledge-graph-bot]]（飞书 Bot 的自然语言→实体路由）
- 复用 [[10_Reference/projects/active/vibe-research|Vibe-Research]] 的 LLM/embedding 基础设施
- 与现有 `[[]]` 链接互补：`[[]]` 是人工显式边，语义搜索是算法隐式边

## 方法论意义
本项目的深层意义是"知识图谱第四构件——逻辑规则"的自动化：四构件方法论（[[10_Reference/meta/four-construct-ontology|四构件本体]]）中，实体/关系/动作可人工建，但跨域"同构关系"（如"em_get 限流 ≅ 涨跌停板"）靠人工发现成本高——语义搜索可批量发现跨领域同构，作为人工补链的候选源。

## 待解决问题
- embedding 模型选型（中文投研语料的召回质量）
- 增量索引（vault 更新时只 re-embed 改动文件，见 [[10_Reference/projects/backlog/incremental-sync-automation|增量同步]]）
- 召回结果的可解释性（为什么这个实体相关）

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/projects/active/knowledge-graph]]
- [[10_Reference/projects/active/knowledge-graph-bot]]
- [[10_Reference/projects/active/vibe-research]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/meta/four-construct-ontology]]
