# AI 角色（Agents）索引

> trading-agents 的 7 个 Analyst 角色。区别于 [[analysts/]]（真人券商研报作者）：此处是 AI Agent，不是真人。

## 角色列表

```dataview
TABLE name AS "角色", role AS "职能", debates_with AS "辩论对手"
FROM "10_Reference/investing/agents"
WHERE type = "agent_role"
SORT name ASC
```

## 角色分类

### 原版 4 角色（A 股适配）

- [[agents/market_analyst]]：市场分析师（K 线/技术指标）
- [[agents/sentiment_analyst]]：情绪分析师（社交舆情）
- [[agents/news_analyst]]：新闻分析师（事件/公告）
- [[agents/fundamental_analyst]]：基本面分析师（财报/估值）

### A 股特化 3 角色（新增）

- [[agents/policy_analyst]]：政策分析师（监管/产业政策）
- [[agents/hot_money_tracker]]：游资追踪师（龙虎榜/资金流）
- [[agents/lockup_monitor]]：解禁监控师（限售解禁/减持）

## 辩论架构

7 个 Analyst 报告 → Bull/Bear 研究员辩论 → Research Manager 综合研判 → Trader 交易方案 → 三方风险辩论（激进/保守/中立）→ Portfolio Manager 最终决策。

详见 [[specs/trading-agents-project]]。

## 与 Vibe-Research 的关系

trading-agents 与 Vibe-Research 共享 4 个数据源（mootdx/东财/新浪/同花顺），但定位不同：
- Vibe-Research：私人投研助理，单点查询 + 弱合规研判
- trading-agents：多 Agent 辩论框架，输出完整投资计划 + Buy/Hold/Sell 决策
