---
type: agent_role
name: 解禁监控师
project: trading-agents
origin_project: trading-agents
role: lockup_watcher
data_sources: [mootdx, eastmoney, hithink-ths]
debates_with: "[[agents/hot_money_tracker]], [[agents/fundamental_analyst]]"
created: 2026-09-07
confidence: high
source: trading-agents/README.md
---

> [!info] 🤖 AI 角色
> **角色**：解禁监控师  **职能**：`lockup_watcher`
> **来源项目**：trading-agents
> **辩论对手**：[[10_Reference/investing/agents/hot_money_tracker]], [[10_Reference/investing/agents/fundamental_analyst]]

## 🎯 角色职责

限售股解禁、大股东减持、股权质押。**A 股特化新增角色**——解禁是 A 股特有的重大供给冲击因素，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/lockup_watcher.py`


## 📡 数据源

- [[10_Reference/investing/data-sources/index|data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[10_Reference/investing/agents/index|agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
