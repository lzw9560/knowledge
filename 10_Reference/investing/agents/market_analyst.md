---
type: agent_role
name: 市场分析师
project: trading-agents
origin_project: trading-agents
role: market_analyst
data_sources: [mootdx, eastmoney, sina]
debates_with: "[[agents/sentiment_analyst]], [[agents/news_analyst]]"
created: 2026-09-07
---

# 角色职责

K 线形态、技术指标（MACD/RSI/KDJ/布林带）、量价分析、支撑压力位研判。原版 4 角色之一，A 股适配后继承通用技术分析框架。

对应代码：`tradingagents/agents/analysts/market_analyst.py`

# 数据源

- [[data-sources/mootdx]]：K 线数据（OHLCV）
- [[data-sources/eastmoney-push2]]：实时行情、分时
- [[data-sources/sina-financial]]：K 线历史

# 辩论对手

- [[agents/sentiment_analyst]]（情绪面与技术面交叉验证）
- [[agents/news_analyst]]（事件驱动 vs 技术形态）
- 报告流入后续 Bull/Bear 研究员辩论与三方风险辩论

# 与 Vibe-Research 的关系

- 数据源共享：Vibe-Research 的 `backend/data/sources/astock.py` 同样走 mootdx/东财/新浪
- 工具复用：Vibe-Research 的 `query_quote` / `query_valuation` MCP 工具提供同类行情估值数据
- 互补：trading-agents 输出多空辩论后的方向性研判，Vibe-Research 提供单点查询
