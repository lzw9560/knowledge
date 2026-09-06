# 项目上下文 — daily-stock-analysis

## 架构
- data_provider 策略模式：BaseFetcher/DataFetcherManager，A 股优先级 Tushare≈efinance > akshare > pytdx > baostock > yfinance；港美股 longbridge
- 每 fetcher 内置流控/失败切换/指数退避/熔断 CircuitBreaker
- value_research 微服务：4 引擎（funnel 行业漏斗/single 单股/team 团队/checklist）+ cross_validator
- 存储：SQLAlchemy + SQLite（共享数据卷）；报告落 reports/；缓存/限流/熔断内置
- Web：dsa-web（Vite）+ dsa-desktop（Electron）

## 关键约定
- AGENTS.md 是 AI 协作规则唯一真源（CLAUDE.md 软链），多 AI 工具共守
- 新配置"不配置也可运行"
- LiteLLM 统一所有 LLM，锁版本（>=1.80.10,!=1.82.7/8,<2.0）
- 自动 tag opt-in（#patch/#minor/#major 触发）
- 贡献底线：不接受堆叠代码量/补丁式 review

## 数据源
- A 股：efinance/akshare/tushare/pytdx/baostock/腾讯/mootdx
- 港美股：longbridge/yfinance/finnhub/alphavantage
- 龙虎榜/资金流/板块：EM push2 + Sina 兜底 + dragon_tiger + iwencai + ths_hotspot
- 新闻：Anspire/SerpAPI/Tavily/Bocha/Brave/MiniMax/SearXNG

## 已知坑
- ⚠️ `daily-stock-analysis/` 顶层非 git，真实仓库在 `daily_stock_analysis/` 子目录
- value_research 16 文件 +809 行未提交
- 落后上游（PR #1973/#1967 未同步）
- LiteLLM 排除 1.82.7/8（隔离构建 bug）
