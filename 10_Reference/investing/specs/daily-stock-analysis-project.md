---
type: project
name: daily-stock-analysis
title: 每日股票分析（ZhuLinsen/daily-stock-analysis）
status: 活跃
github: ZhuLinsen/daily_stock_analysis
created: 2026-09-07
---

# 项目定位

基于 AI 大模型的 A 股/港股/美股/日股/韩股/台股自选股智能分析系统，每日自动分析并推送「决策仪表盘」到企业微信/飞书/Telegram/Discord/Slack/邮箱。GitHub Trendshift Python Repository Of The Day，开源 MIT 协议，pip install 即跑或 GitHub Actions 零成本部署。

定位为**每日分析报告生成器**——输入自选股代码，输出含核心结论/评分/买卖点位/风险警报/催化因素/操作检查清单的完整决策报告，并多渠道推送。

# 核心能力

| 能力 | 覆盖内容 |
|------|------|
| AI 决策报告 | 核心结论、评分、趋势、买卖点位、风险警报、催化因素、操作检查清单 |
| 多市场数据聚合 | A 股/港股/美股/日股/韩股/台股/ETF，支持行情/K 线/技术指标/新闻/公告/基本面 |
| Web/桌面工作台 | 手动分析、任务进度、历史报告、回测、持仓、配置管理 |
| Agent 策略问股 | 多轮追问，15 种内置策略（均线/缠论/波浪/趋势/热点/事件/成长/预期等） |
| 智能导入与补全 | 图片/CSV/Excel/剪贴板导入，代码/名称/拼音/别名补全 |
| 自动化与推送 | GitHub Actions/Docker/本地定时/FastAPI，多渠道推送 |

技术栈：
- AI 模型：Anspire、AIHubMix、Gemini、OpenAI 兼容、DeepSeek、通义千问、Claude、Ollama
- 行情数据：TickFlow、AkShare、Tushare、Pytdx、Baostock、YFinance、Longbridge
- 新闻搜索：Anspire、SerpAPI、Tavily、Bocha、Brave、MiniMax、SearXNG
- 社交舆情：Stock Sentiment API（Reddit/X/Polymarket，仅美股）

# 与 Vibe-Research 的关系

Vibe-Research 的 `dragon_head` 战法已引用 daily-stock-analysis 的 yaml 配置（自选股分析输出的龙虎榜/涨停数据是龙头战法 match 的数据源之一）。两者关系：

| 维度 | Vibe-Research | daily-stock-analysis |
|------|----------------|----------------------|
| 定位 | 私人投研助理 | 自选股每日分析报告生成器 |
| 输出 | 单点查询 + 弱合规研判 | 完整决策仪表盘 + 多渠道推送 |
| 部署 | 本地后端 + MCP | GitHub Actions/Docker/本地 |
| 数据源交集 | mootdx/东财/新浪/同花顺/akshare/baostock | AkShare/Baostock/Pytdx/Tushare/YFinance/Longbridge |
| 关系 | 战法引用其 yaml 输出 | 独立项目，数据源部分共用 |

# 数据源

daily-stock-analysis 使用的行情数据源（与 Vibe-Research 共用的标注 ✅）：

- [[data-sources/akshare]] ✅ 共用
- [[data-sources/baostock]] ✅ 共用
- [[data-sources/mootdx]] ✅ 共用（Pytdx 同属通达信协议系列）
- Tushare、YFinance、Longbridge、TickFlow — 图谱暂无对应实体，待建

新闻/搜索源：SerpAPI、Tavily、Bocha、Brave、MiniMax、SearXNG、Anspire — 图谱暂无对应实体。

# 相关链接

- GitHub：https://github.com/ZhuLinsen/daily_stock_analysis
- 官方文档：`docs/full-guide.md`（完整配置与部署指南）
- 同系列项目：[AlphaSift](https://github.com/ZhuLinsen/alphasift)（多因子选股）、[AlphaEvo](https://github.com/ZhuLinsen/alphaevo)（策略回测与进化）
- 上游：[[specs/]] Vibe-Research spec 体系
