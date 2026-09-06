# 决策记录 — daily-stock-analysis

> 从 AGENTS.md + git log + requirements 提炼（2026-09-03）

- **data_provider 策略模式 + 多源 fallback**：单源失败不拖垮主流程；每 fetcher 内置流控/指数退避防封禁
- **AGENTS.md 是 AI 协作规则唯一真源**：CLAUDE.md 软链到它，多 AI 工具（Claude/Copilot/opencode/cursor/windsurf/codebuddy）共守
- **新配置"不配置也可运行，配置后增强"**：避叠加开关/互斥模式；默认 akshare/baostock/yfinance 零配置可跑
- **统一 LiteLLM 接入所有 LLM**：锁 >=1.80.10,!=1.82.7/8,<2.0（排除隔离构建 bug）
- **value_research 拆独立 FastAPI 微服务**：funnel（行业漏斗）/single（单股）/team（团队）/checklist 四引擎 + cross_validator
- **TradingAgents-astock 作为本地依赖**：锁 langchain-core<0.4/langgraph<0.3 避 breaking changes
- **自动 tag 默认 opt-in**：仅 commit title 含 #patch/#minor/#major 才触发；手动 tag 用 annotated
- **AlphaSift（多因子选股）git+ 依赖引入**；AlphaEvo（策略进化）同系列独立项目
- **贡献质量底线**：不接受堆叠代码量/补丁式 review 替代设计收敛
