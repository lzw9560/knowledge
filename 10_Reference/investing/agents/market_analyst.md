---
type: agent_role
name: 市场分析师
project: trading-agents
origin_project: trading-agents
role: market_analyst
data_sources: [mootdx, eastmoney, sina]
debates_with: "[[10_Reference/investing/agents/sentiment_analyst]], [[10_Reference/investing/agents/news_analyst]]"
created: 2026-09-07
confidence: high
source: trading-agents/README.md
---

> [!info] 🤖 AI 角色
> **角色**：市场分析师  **职能**：`market_analyst`
> **来源项目**：trading-agents
> **辩论对手**：[[10_Reference/investing/agents/sentiment_analyst]], [[10_Reference/investing/agents/news_analyst]]

## 🎯 角色职责

K 线形态、技术指标（MACD/RSI/KDJ/布林带）、量价分析、支撑压力位研判。原版 4 角色之一，A 股适配后继承通用技术分析框架。

对应代码：`tradingagents/agents/analysts/market_analyst.py`


## 📡 数据源

- [[10_Reference/investing/data-sources/index|data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[10_Reference/investing/agents/index|agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：4 个 · **入链**：0 个
