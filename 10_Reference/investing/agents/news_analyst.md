---
type: agent_role
name: 新闻分析师
project: trading-agents
origin_project: trading-agents
role: news_analyst
data_sources: [eastmoney, worldmonitor]
debates_with: "[[agents/market_analyst]], [[agents/fundamental_analyst]]"
created: 2026-09-07
---

> [!info] 🤖 AI 角色
> **角色**：新闻分析师  **职能**：`news_analyst`
> **来源项目**：trading-agents
> **辩论对手**：[[agents/market_analyst]], [[agents/fundamental_analyst]]

## 🎯 角色职责

行业新闻、公司公告、宏观事件、全球财经快讯。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/news_analyst.py`


## 📡 数据源

- [[data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
