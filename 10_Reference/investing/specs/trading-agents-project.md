---
type: project
name: trading-agents
title: TradingAgents A股深度特化 fork
status: 活跃
github: lzwfirst/tradingagents-astock
upstream: TauricResearch/TradingAgents
created: 2026-09-07
---

# 项目概述

基于 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)（65K ⭐）的 A 股深度特化 fork。全 Apache 2.0 开源，pip install 即跑，零外部服务依赖。

## 核心改造

| 维度 | 原版 | 本 Fork |
|------|------|---------|
| 数据源 | Yahoo Finance / Alpha Vantage | mootdx + 东财 + 新浪 + 同花顺（全免费直连） |
| Analyst 角色 | 4 个 | **7 个**（+政策/游资/解禁） |
| 交易规则 | 美股（T+0、无涨跌停） | A 股（T+1、涨跌停、最小手数、交易时段） |
| 输出语言 | 英文 | 中文报告（内部辩论保持英文） |
| Alpha 基准 | SPY | 沪深 300（CSI 300） |

# 架构

```
7 Analyst 研报生成 → Bull vs Bear 投研辩论 → Research Manager 综合研判
→ Trader 交易方案（A 股约束）→ 三方风险辩论 → Portfolio Manager 最终决策
```

**双 LLM 设计**：
- `quick_think_llm`：所有 Analyst、Researcher、Trader、Risk Debater
- `deep_think_llm`：Research Manager 和 Portfolio Manager

# 7 个 Analyst 角色

详见 [[agents/]]：
- [[agents/market_analyst]] / [[agents/sentiment_analyst]] / [[agents/news_analyst]] / [[agents/fundamental_analyst]]
- [[agents/policy_analyst]] / [[agents/hot_money_tracker]] / [[agents/lockup_monitor]]

# 数据源

共享数据源（与 Vibe-Research 共用）：
- [[data-sources/mootdx]]
- [[data-sources/eastmoney-push2]]
- [[data-sources/sina-financial]]
- [[data-sources/hithink-ths]]

# 与 Vibe-Research 的关系

| 维度 | Vibe-Research | trading-agents |
|------|----------------|----------------|
| 定位 | 私人投研助理 | 多 Agent 辩论框架 |
| 输出 | 单点查询 + 弱合规研判 | 完整投资计划 + Buy/Hold/Sell |
| Agent 数 | 无独立 Agent | 7 Analyst + 多 Researcher + Trader |
| 共享 | 4 数据源（mootdx/东财/新浪/同花顺） | 同 |

# 相关链接

- GitHub：https://github.com/lzwfirst/tradingagents-astock
- 论文：[arXiv:2412.20138](https://arxiv.org/abs/2412.20138)
- 上游：[[specs/]] Vibe-Research spec 体系
