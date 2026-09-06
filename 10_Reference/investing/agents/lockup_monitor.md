---
type: agent_role
name: 解禁监控师
project: trading-agents
origin_project: trading-agents
role: lockup_watcher
data_sources: [mootdx, eastmoney, hithink-ths]
debates_with: [[agents/hot_money_tracker]], [[agents/fundamental_analyst]]
created: 2026-09-07
---

# 角色职责

限售股解禁、大股东减持、股权质押。**A 股特化新增角色**——解禁是 A 股特有的重大供给冲击因素，原版 TradingAgents 无此角色。

对应代码：`tradingagents/agents/analysts/lockup_watcher.py`

# 数据源

- [[data-sources/mootdx]]：基本面数据
- [[data-sources/eastmoney-push2]]：限售解禁数据
- [[data-sources/hithink-ths]]：一致预期
- 工具：`get_insider_transactions`、`get_news`、`get_fundamentals`

# 辩论对手

- [[agents/hot_money_tracker]]（解禁抛压 vs 游资流入）
- [[agents/fundamental_analyst]]（供给冲击 vs 基本面）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：东财（Vibe-Research 的解禁数据源）
- 互补：trading-agents 把解禁冲击纳入多空辩论，Vibe-Research 提供解禁事件查询
