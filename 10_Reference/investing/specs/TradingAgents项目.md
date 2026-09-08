---
type: project
name: trading-agents
title: TradingAgents A股深度特化 fork
status: 活跃
github: lzwfirst/tradingagents-astock
upstream: TauricResearch/TradingAgents
created: 2026-09-07
confidence: high
source: README.md
---

> [!info] 📋 项目决策
> **名称**：trading-agents  **标题**：TradingAgents A股深度特化 fork  **状态**：活跃
> **GitHub**：`lzwfirst/tradingagents-astock`
>
> **关联**：[[10_Reference/investing/specs/index|specs/]] · [[10_Reference/investing/data-sources/index|data-sources/]] · [[10_Reference/investing/agents/index|agents/]]

## 📋 项目概述

基于 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)（65K ⭐）的 A 股深度特化 fork。全 Apache 2.0 开源，pip install 即跑，零外部服务依赖。


## 🏗 架构

```
7 Analyst 研报生成 → Bull vs Bear 投研辩论 → Research Manager 综合研判
→ Trader 交易方案（A 股约束）→ 三方风险辩论 → Portfolio Manager 最终决策
```

**双 LLM 设计**：
- `quick_think_llm`：所有 Analyst、Researcher、Trader、Risk Debater
- `deep_think_llm`：Research Manager 和 Portfolio Manager


## 🔗 关联

- GitHub：https://github.com/lzwfirst/tradingagents-astock
- 论文：[arXiv:2412.20138](https://arxiv.org/abs/2412.20138)
- 上游：[[10_Reference/investing/specs/index|specs/]] Vibe-Research spec 体系


## 🔗 关联

- **出链**：6 个 · **入链**：5 个
