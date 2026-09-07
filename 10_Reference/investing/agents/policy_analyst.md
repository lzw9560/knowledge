---
type: agent_role
name: 政策分析师
project: trading-agents
origin_project: trading-agents
role: policy_analyst
data_sources: [eastmoney, worldmonitor]
debates_with: "[[agents/fundamental_analyst]], [[agents/hot_money_tracker]]"
created: 2026-09-07
---

> [!info] 🤖 AI 角色
> **角色**：政策分析师  **职能**：`policy_analyst`
> **来源项目**：trading-agents
> **辩论对手**：[[agents/fundamental_analyst]], [[agents/hot_money_tracker]]

## 🎯 角色职责

监管政策、产业政策、窗口指导、证监会动态。**A 股特化新增角色**——A 股是政策市，政策变化直接影响板块轮动，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/policy_analyst.py`


## 📡 数据源

- [[data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
