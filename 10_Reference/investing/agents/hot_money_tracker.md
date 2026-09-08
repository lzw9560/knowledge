---
type: agent_role
name: 游资追踪师
project: trading-agents
origin_project: trading-agents
role: hot_money_tracker
data_sources: [mootdx, eastmoney]
debates_with: "[[agents/policy_analyst]], [[agents/lockup_monitor]]"
created: 2026-09-07
confidence: high
source: trading-agents/README.md
---

> [!info] 🤖 AI 角色
> **角色**：游资追踪师  **职能**：`hot_money_tracker`
> **来源项目**：trading-agents
> **辩论对手**：[[10_Reference/investing/agents/policy_analyst]], [[10_Reference/investing/agents/lockup_monitor]]

## 🎯 角色职责

龙虎榜、大单流向、主力资金动态、游资席位画像。**A 股特化新增角色**——游资是 A 股短线定价的核心力量，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/hot_money_tracker.py`


## 📡 数据源

- [[10_Reference/investing/data-sources/index|data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[10_Reference/investing/agents/index|agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
