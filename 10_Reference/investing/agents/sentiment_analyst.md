---
type: agent_role
name: 情绪分析师
project: trading-agents
origin_project: trading-agents
role: social_media_analyst
data_sources: [eastmoney]
debates_with: "[[agents/market_analyst]], [[agents/news_analyst]]"
created: 2026-09-07
---

> [!info] 🤖 AI 角色
> **角色**：情绪分析师  **职能**：`social_media_analyst`
> **来源项目**：trading-agents
> **辩论对手**：[[agents/market_analyst]], [[agents/news_analyst]]

## 🎯 角色职责

社交媒体情绪、散户讨论热度、股吧/论坛舆情、A 股散户情绪指标。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/social_media_analyst.py`


## 📡 数据源

- [[data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
