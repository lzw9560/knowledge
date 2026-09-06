# 项目上下文 — trading-agents

## 架构
- 多 Agent 编排（LangGraph 状态机）：7 Analyst → Bull/Bear 辩论 → 三方风险辩论 → Research Manager（deep LLM）→ Trader（A 股 T+1/涨跌停/手数约束）→ Portfolio Manager（Buy/Hold/Sell + 仓位）
- 双 LLM：quick_think（分析师/研究员/交易员）+ deep_think（管理者）
- SQLite checkpoint 断点续跑

## 关键约定
- 东财端点走 `_em_get()` 限流（EM_MIN_INTERVAL=1.0s + 随机抖动）——防封 IP
- 内部辩论英文，输出中文
- Alpha 基准 = 沪深 300（非 SPY）
- google-genai 移可选依赖（避 httpx 冲突）

## 数据源优先级
mootdx（通达信 TCP，不封 IP）> 腾讯 > 东财（限流）> 新浪 > 同花顺 > 财联社 > 百度

## 已知坑
- 版本号 pyproject vs CLAUDE.md 不一致
- mootdx 锁 httpx 0.25.2 与 google-genai 冲突
- 部分模型 tool call 返回中文股票名而非 6 位代码（safe_ticker_component 兜底但表现不一）
- 百度 PAE 资金流接口已下线（v0.2.7 迁东财 push2）
