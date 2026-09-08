---
type: spec
number: S149
title: vibe-astock 语义吸收（4 阶段框架 spec）
status: 草案
created: 2026-09-07
last_synced: 2026-09-07
confidence: high
source: specs/README.md
---

> [!info] 📋 项目决策
> **编号**：S149  **标题**：vibe-astock 语义吸收（4 阶段框架 spec）  **状态**：草案
>
> **关联**：[[10_Reference/investing/specs/index|specs/]] · [[10_Reference/investing/strategies/index|strategies/]] · [[10_Reference/investing/data-sources/index|data-sources/]]

## 🎯 问题/目标

S149 旨在解决 Vibe 编程中大量非结构化的设计意图与代码片段难以沉淀为可复用、可理解的结构化语义资产的问题，防止上下文信息在迭代中流失。核心设计决策是采用“提取—解析—对齐—融合”四阶段渐进式吸收框架，将原始输入逐层转化为意图摘要、规范化语义表示、资产关联，最终并入知识库，确保整个过程的透明性与可回溯性。该框架依赖的关键技术与组件包括基于大语言模型的意图识别与语义解析器、抽象语法树（AST）与向量嵌入的混合表示引擎，以及 vibe-astock 资产库存的增量式图谱更新与检索机制。


## 📝 需求

详见 spec 原文（S149-vibe-astock语义吸收）


## 📂 受影响文件

详见 spec 原文（S149-vibe-astock语义吸收）


## ✅ 验收标准

- 源文件：`specs/S149-vibe-astock语义吸收/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]


## 🔗 关联决策

> 与其他 spec 的依赖/冲突/替代关系。

- [[10_Reference/investing/specs/index|specs/]]

## 🔗 关联

- **出链**：9 个 · **入链**：2 个

## 🔗 技术参考

- 🔧 10_Reference/tech-learning/concepts/数据契约|[[数据契约]] — 语义吸收即把裸 dict + 魔法字符串吸收为 Pydantic 契约模型
- 🔧 [[10_Reference/tech-learning/frameworks/pydantic|Pydantic]] — 4 阶段框架用 Pydantic 做形状统一
- 🏗️ 10_Reference/tech-learning/architecture/分层架构|[[分层架构]] — 吸收过程遵循分层，不跨层泄漏
