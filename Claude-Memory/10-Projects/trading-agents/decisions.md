# 决策记录 — trading-agents

> 关键决策（从 git log + CLAUDE.md + README 提炼，2026-09-03）

- **2026-05-13**：Fork TauricResearch/TradingAgents 做 A 股深度特化——数据层/Agent 角色/交易规则三维改造（非简单翻译）
- **v0.2.5**：完全移除 akshare，所有数据直连 HTTP API，零第三方库依赖
- **v0.2.6**：langchain-google-genai 移至可选依赖 `[google]`，解 mootdx 锁 httpx==0.25.2 与 google-genai(httpx>=0.28.1) 冲突
- **v0.2.11**：东财请求统一走 `_em_get()` 限流入口（串行 ≥1s + 随机抖动 + Keep-Alive），防多 Agent 批量分析触发临时封 IP
- **v0.3.0**：新增量化研究平台五大模块（分析/追踪/打板/推荐/风控）+ 30+ 策略库 + 分布式批量扫描（Celery+Redis）。但 pyproject 版本号未同步仍标 0.2.13
- **双 LLM 设计**：quick_think_llm 跑所有 Analyst/Researcher/Trader/Risk Debater，deep_think_llm 只跑 Research Manager + Portfolio Manager（需全局综合决策）
- **内部辩论英文**（保推理质量），输出报告中文（output_language=Chinese）
- **Alpha 基准**用沪深 300（CSI 300）替代原版 SPY，反思机制对比基准收益
- **default_config 默认 llm_provider='agnes' model='agnes-2.0-flash'**（Agnes AI），非 README 推荐的 MiniMax
