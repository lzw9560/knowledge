---
type: agent_role
name: 游资追踪师
project: trading-agents
origin_project: trading-agents
role: hot_money_tracker
data_sources: [mootdx, eastmoney]
debates_with: [[agents/policy_analyst]], [[agents/lockup_monitor]]
created: 2026-09-07
---

# 角色职责

龙虎榜、大单流向、主力资金动态、游资席位画像。**A 股特化新增角色**——游资是 A 股短线定价的核心力量，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/hot_money_tracker.py`

# 数据源

- [[data-sources/mootdx]]：行情数据
- [[data-sources/eastmoney-push2]]：龙虎榜、资金流
- 工具：`get_stock_data`、`get_news`、`get_insider_transactions`

# 辩论对手

- [[agents/policy_analyst]]（资金驱动 vs 政策驱动）
- [[agents/lockup_monitor]]（游资流入 vs 解禁抛压）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：东财龙虎榜（Vibe-Research `dragon-tiger` 实体对应）
- 互补：trading-agents 把游资行为纳入多空辩论，Vibe-Research 提供 `[[dragon-tiger/]]` 实体查询
