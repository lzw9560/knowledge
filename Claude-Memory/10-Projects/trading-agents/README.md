# trading-agents (TradingAgents-Astock)

> Fork of TauricResearch/TradingAgents（65K Star）做 A 股深度特化。多 Agent LLM 投研框架。
> 路径：`/Users/lizhiwei/project/code/stock/trading-agents`

## 概述
7 个 Analyst 角色（市场/情绪/新闻/基本面 + A 股特化的政策/游资/解禁）并行生成研报 → Bull vs Bear 辩论 → 三方风险辩论（激进/保守/中立）→ Portfolio Manager 输出 Buy/Hold/Sell + 仓位。v0.3.0 起加量化研究平台（30+ 策略库、回测引擎、自适应权重、分布式批量扫描）。

## 技术栈
- Python 3.10+，LangGraph + LangChain（多 Agent 编排）
- Streamlit Web UI（:8501）、Typer CLI
- Celery + Redis（分布式批量扫描）
- mootdx（通达信 TCP 协议）、requests 直连各财经 API
- backtrader（回测）、SQLite（断点续跑）、Pydantic

## 当前状态（2026-09-03）
- **wip→趋 stale**：最后 commit 2026-06-09（距今 ~3 月），工作树有未提交改动
- 版本号不一致：pyproject=0.2.13 vs CLAUDE.md=0.3.0（v0.3.0 功能已写但版本号未 bump）
- mootdx 锁 httpx==0.25.2 与 langchain-google-genai 冲突（google-genai 移至可选依赖）

## 入口
- `pip install -e .`（Google 模型 `pip install -e '.[google]'`）
- CLI：`tradingagents`（typer 交互式）
- Web：`tradingagents-web` 或 `streamlit run web/app.py` → :8501
- 批量：`tradingagents batch-scan 600519 000858 -d 2026-06-09 -w 4`（local）/ `--mode celery`（需 Redis）

## 数据源
mootdx（通达信）/ 腾讯（PE/PB/市值）/ 东财（龙虎榜/解禁/板块/资金流，走 `_em_get` 限流防封）/ 新浪（K 线历史/财报）/ 同花顺（EPS 一致预期，v0.3.0 切东财 reportapi）/ 财联社 / 百度股市通

## CC 记忆
本项目无 CC memory（`~/.claude/projects/` 下无此 scope 的 memory）。本目录手动策展。

## 关键决策 / 待办 / 上下文
见 `decisions.md` / `todos.md` / `context.md`
