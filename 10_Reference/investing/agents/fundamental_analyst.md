---
type: agent_role
name: 基本面分析师
project: trading-agents
origin_project: trading-agents
role: fundamentals_analyst
data_sources: [mootdx, sina, hithink-ths]
debates_with: [[agents/news_analyst]], [[agents/policy_analyst]]
created: 2026-09-07
---

# 角色职责

财报三表（资产负债表/利润表/现金流量表）、盈利能力、估值、机构一致预期。原版 4 角色之一。

对应代码：`tradingagents/agents/analysts/fundamentals_analyst.py`

# 数据源

- [[data-sources/mootdx]]：财务快照
- [[data-sources/sina-financial]]：财报三表
- [[data-sources/hithink-ths]]：机构一致预期（EPS 前向估值）
- 工具：`get_fundamentals`、`get_balance_sheet`、`get_cashflow`、`get_income_statement`

# 辩论对手

- [[agents/news_analyst]]（基本面 vs 事件催化）
- [[agents/policy_analyst]]（基本面 vs 政策导向）
- 报告流入后续 Bull/Bear 研究员辩论

# 与 Vibe-Research 的关系

- 数据源共享：mootdx/新浪/同花顺（Vibe-Research `full_valuation` / `finance`）
- 工具复用：Vibe-Research 的 `query_valuation` 提供同类估值数据
- 互补：trading-agents 把基本面纳入多空辩论，Vibe-Research 提供单点查询
