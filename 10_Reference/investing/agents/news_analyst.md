---
type: agent_role
name: 新闻分析师
project: trading-agents
origin_project: trading-agents
role: news_analyst
data_sources: [eastmoney, worldmonitor]
debates_with: [[agents/market_analyst]], [[agents/fundamental_analyst]]
created: 2026-09-07
---

# 角色职责

行业新闻、公司公告、宏观事件、全球财经快讯。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/news_analyst.py`

# 数据源

- [[data-sources/eastmoney-push2]]：个股新闻、公告
- [[data-sources/worldmonitor]]：全球宏观/地缘事件
- 工具：`get_news`、`get_global_news`、`get_insider_transactions`

# 辩论对手

- [[agents/market_analyst]]（事件 vs 技术）
- [[agents/fundamental_analyst]]（事件催化 vs 基本面）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：worldmonitor（Vibe-Research 的 `worldmonitor_query` MCP 工具）
- 互补：trading-agents 把新闻纳入多空辩论框架，Vibe-Research 提供 `query_news` 单点查询
