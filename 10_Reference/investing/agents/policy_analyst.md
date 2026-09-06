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

# 角色职责

监管政策、产业政策、窗口指导、证监会动态。**A 股特化新增角色**——A 股是政策市，政策变化直接影响板块轮动，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/policy_analyst.py`

# 数据源

- [[data-sources/eastmoney-push2]]：政策新闻、板块异动
- [[data-sources/worldmonitor]]：宏观政策、地缘
- 工具：`get_news`、`get_global_news`

# 辩论对手

- [[agents/fundamental_analyst]]（政策导向 vs 基本面）
- [[agents/hot_money_tracker]]（政策驱动 vs 资金驱动）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：worldmonitor（Vibe-Research 的 `worldmonitor_query` MCP 工具覆盖宏观/地缘）
- 互补：trading-agents 的政策分析能力是 Vibe-Research 当前缺失的维度
