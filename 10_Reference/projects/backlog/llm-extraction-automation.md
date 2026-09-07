---
type: project
name: llm-extraction-automation
title: LLM 抽取自动化
status: 候选
created: 2026-09-07
---

# LLM 抽取自动化

## 项目概述
实现"非结构化数据 → 结构化实体/关系"的 LLM 抽取自动化管线。当前图谱/数据录入依赖人工提取关键信息，目标是建一套 LLM 抽取管线：原始数据（研报/公告/新闻）→ LLM 提取 → 结构化 JSON → 入库 + 图谱同步。

## 核心能力
- **多源接入**：研报（PDF/HTML）/ 公告（巨潮）/ 新闻（财联社快讯）/ 财报（XBRL）
- **抽取模板**：不同源对应不同抽取模板（研报 → 目标价/评级；公告 → 事件类型/金额）
- **LLM 调度**：批量抽取 + 重试 + 费用控制，支持多模型切换（百炼/DeepSeek/本地）
- **结构化输出**：LLM 输出约束为 JSON schema，校验后入库
- **图谱同步**：抽取出的实体/关系自动同步到 Obsidian 图谱 md

## 候选理由
- 当前 [[10_Reference/investing/valuations/|估值实体]] 等数据依赖人工录入，规模不可持续
- LLM 抽取是"非结构化 → 结构化"的杠杆，但需先验证抽取准确率
- 已有 [[10_Reference/projects/active/obsidian-mcp|obsidian-mcp]] 做图谱写入基础设施，可复用

## 与现有 llm_extract.py 的关系
- `scripts/llm_extract.py` 已有 LLM 抽取雏形（关系抽取），本项目是其产品化：
  - 从脚本化 → 服务化（API 化）
  - 从单次抽取 → 批量管线 + 调度
  - 从无校验 → JSON schema 校验 + 人工复核流程

## 与投研的跨领域链接
- [[10_Reference/investing/valuations/|估值实体]] — 研报目标价 LLM 抽取的主要产出
- [[10_Reference/investing/specs/|specs 目录]] — 抽取出的实体/关系同步到 specs 相关 md
- [[10_Reference/projects/backlog/incremental-sync-automation|增量同步自动化]] — 本项目的图谱同步部分可复用增量同步管线

## 技术栈候选
- LLM 调度：百炼 API（[[10_Reference/investing/specs/archive/m0-foundation/S015-配置与基础设施|S015 config]] 管理 key）
- 抽取模板：Jinja2 / JSON schema
- 校验：Pydantic（[[10_Reference/tech-learning/frameworks/fastapi|FastAPI]] 同栈）
- 存储：PostgreSQL + Obsidian md 双写

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/projects/backlog/incremental-sync-automation]]
- [[10_Reference/projects/active/obsidian-mcp]]
- [[10_Reference/investing/valuations/]]
- [[10_Reference/tech-learning/frameworks/fastapi]]
- [[10_Reference/meta/four-construct-ontology]]
