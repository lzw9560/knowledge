# daily-stock-analysis

> 多源 A/US/HK 股票分析 + 价值投研。data_provider 策略模式多源 fallback + LiteLLM + value_research 微服务。
> 路径：`/Users/lizhiwei/project/code/stock/daily-stock-analysis`
> ⚠️ 注意：`daily-stock-analysis/` 顶层非 git 仓库，真实仓库在子目录 `daily_stock_analysis/`（967 commits，develop 分支）

## 概述
多源股票数据（A 股优先 Tushare≈efinance > akshare > pytdx > baostock；港美股 longbridge/yfinance/finnhub）→ 技术/新闻分析 → LLM（LiteLLM 统一）→ 报告。含 value_research 价值投研微服务（funnel 行业漏斗/single 单股/team 团队/checklist 四引擎 + cross_validator）。Web UI + Electron 桌面端 + GitHub Actions 每工作日 18:00 自动分析。

## 技术栈
- Python，FastAPI + SQLAlchemy + SQLite
- LiteLLM（统一 Gemini/OpenAI/DeepSeek/Claude/Ollama，锁 >=1.80.10,!=1.82.7/8,<2.0）
- data_provider 策略模式 + BaseFetcher/DataFetcherManager（多源 fallback + 流控/退避/熔断 CircuitBreaker）
- Web 前端：dsa-web（Vite）；桌面：dsa-desktop（Electron）
- 依赖 TradingAgents-astock（本地，锁 langchain 系列）

## 当前状态（2026-09-03）
- **wip 停滞**：最后 commit 2026-07-11（dc469b3，develop，~7 周前）；value_research 子系统 16 文件 +809 行未提交
- 上游 ZhuLinsen 原仓库仍活跃（PR #1973/#1967 同期合入，本地落后）
- AGENTS.md 是 AI 协作规则唯一真源（CLAUDE.md 软链到它），多 AI 工具共守（Claude/Copilot/opencode/cursor/windsurf/codebuddy）

## 入口
- `python main.py`（默认全流程：抓数据→技术/新闻→LLM→报告）
- `python main.py --webui`（Web 工作台 :8000）/ `--serve`（FastAPI 服务）
- `python services/value_research/main.py`（价值投研微服务，独立 FastAPI）
- `cd apps/dsa-web && npm run build`（Web 前端）/ `cd apps/dsa-desktop && npm run build`（桌面）
- GitHub Actions：`.github/workflows/00-daily-analysis.yml`（每工作日 18:00 北京时间）
- 测试：`python -m pytest -m 'not network'`（离线快测）/ `./scripts/ci_gate.sh`

## 数据源
- A 股：efinance（东财）+ akshare + tushare（pro）+ pytdx（通达信）+ baostock + 腾讯 + mootdx
- 港美股：longbridge（长桥 OpenAPI）+ yfinance + finnhub + alphavantage
- 龙虎榜/资金流/北向/板块：TradingAgents-astock fetcher（EM push2 + Sina 兜底）+ dragon_tiger + iwencai + ths_hotspot
- 新闻：Anspire/SerpAPI/Tavily/Bocha(博查)/Brave/MiniMax/SearXNG 自建
- 优先级：A 股 Tushare≈efinance(0) > akshare(1) > pytdx(2) > baostock(3) > yfinance(4)；港美股 longbridge(5)

## CC 记忆
本项目无 CC memory。本目录手动策展。

## 关键决策 / 待办 / 上下文
见 `decisions.md` / `todos.md` / `context.md`
