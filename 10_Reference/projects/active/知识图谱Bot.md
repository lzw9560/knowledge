---
type: project
name: knowledge-graph-bot
title: 知识图谱飞书 Bot（投研问答接入飞书）
status: backlog
created: 2026-09-07
confidence: high
---

# knowledge-graph-bot

## 项目概述
将 Vibe-Research 投研能力 + Obsidian 知识图谱通过飞书 Bot 接入日常沟通流。目标是"在飞书里自然语言问投研问题，Bot 查知识图谱 + 实时数据回答"。复用 10_Reference/projects/active/Vibe-Research|Vibe-Research]] 后端 API + 10_Reference/projects/active/知识图谱|knowledge-graph vault]] 作为知识源，飞书侧只做消息桥接。

## 技术栈
- 飞书侧：飞书开放平台 Bot（长连接 WebSocket / Webhook）
- 后端：[[10_Reference/tech-learning/frameworks/fastapi|FastAPI]]（复用 Vibe-Research API）
- 知识源：10_Reference/projects/active/知识图谱|Obsidian 知识图谱]]（投研实体/战法/数据源/spec）
- 实时数据：10_Reference/investing/data-sources/东财 push2|东财 push2]] / 10_Reference/investing/data-sources/腾讯行情|腾讯行情]]
- 限流：10_Reference/tech-learning/concepts/限流|em_get 限流]] QPS≤2 防封
- 降级：10_Reference/tech-learning/concepts/优雅降级|优雅降级]]——数据源失败时返回知识图谱历史数据 + 诚实标注"数据延迟"

## 与其他项目的关系
- 依赖 10_Reference/projects/active/Vibe-Research|Vibe-Research]]（后端 API + 数据源层）
- 依赖 10_Reference/projects/active/知识图谱|knowledge-graph vault]]（投研语义层）
- 复用 Vibe-Research 的 [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|契约层]]（Pydantic 模型可直接序列化为飞书卡片 JSON）
- 对照 10_Reference/projects/backlog/微信Bot|wechat-bot]]——飞书 Bot 是企业侧入口，微信 Bot 是个人社交侧入口

## 待解决问题
- 飞书 Bot 长连接 vs Webhook 选型
- 自然语言 → 知识图谱实体路由（需 10_Reference/projects/backlog/语义搜索|语义搜索]] 支撑）
- 卡片消息的投研数据可视化（复用 Vibe-Research 前端 echarts 配置）

## 相关链接
- [[10_Reference/projects/MOC]]
- 10_Reference/projects/active/Vibe-Research]]
- 10_Reference/projects/active/知识图谱]]
- 10_Reference/projects/backlog/语义搜索]]
- [[10_Reference/investing/MOC]]
- 10_Reference/tech-learning/concepts/限流]]
- 10_Reference/meta/四构件本体方法论]]
