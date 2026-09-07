---
type: agent_role
name: 基本面分析师
project: trading-agents
origin_project: trading-agents
role: fundamentals_analyst
data_sources: [mootdx, sina, hithink-ths]
debates_with: "[[agents/news_analyst]], [[agents/policy_analyst]]"
created: 2026-09-07
confidence: high
source: trading-agents/README.md
---

> [!info] 🤖 AI 角色
> **角色**：基本面分析师  **职能**：`fundamentals_analyst`
> **来源项目**：trading-agents
> **辩论对手**：[[agents/news_analyst]], [[agents/policy_analyst]]

## 🎯 角色职责

财报三表（资产负债表/利润表/现金流量表）、盈利能力、估值、机构一致预期。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/fundamentals_analyst.py`


## 📡 数据源

- [[data-sources/]]

## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[agents/]]

## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
