---
type: agent_role
name: 情绪分析师
project: trading-agents
origin_project: trading-agents
role: social_media_analyst
data_sources: [eastmoney]
debates_with: [[agents/market_analyst]], [[agents/news_analyst]]
created: 2026-09-07
---

# 角色职责

社交媒体情绪、散户讨论热度、股吧/论坛舆情、A 股散户情绪指标。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/social_media_analyst.py`

# 数据源

- [[data-sources/eastmoney-push2]]：股吧情绪、热度榜
- 待补：具体社交数据源函数

# 辩论对手

- [[agents/market_analyst]]（情绪 vs 技术）
- [[agents/news_analyst]]（舆情 vs 事件）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：东财 push2
- 互补：Vibe-Research 目前无独立情绪分析模块，trading-agents 补这块能力
