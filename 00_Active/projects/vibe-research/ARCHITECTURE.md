# Vibe-Research 架构总览

## 数据流

```
外部数据源                        数据层 (backend/*.py)    API 路由              前端 / AI 出口
─────────────────                ────────────────────    ──────────────         ─────────────────
腾讯 qt.gtimg.cn (不封IP) ──────► astock.py (A股全栈)  ──► stock_data ──────────► StockData / StockDeep
东财 push2/reportapi ───────────► ├ em_get 限流+熔断     │──► market / limitup ──► Sectors / LimitUp
akshare/mootdx (惰性) ──────────► ├ kline/finance       │──► kline_history ─────► 问AI / 资讯雷达
新浪/巨潮/同花顺 ───────────────► └ full_valuation      │──► workflow / risk ───► ...
                                  gstock.py (美港股)    ─┘
                                  market.py (情绪/板块)
108 RSS 源 ─────────────────────► newsradar.py (12赛道)
```

## AI 三条出口

| 出口 | 原理 | function-calling | 适用 |
|---|---|---|---|
| **订阅接入** | subprocess 调本机 CLI (claude/codex/qwen) | ❌ | 本地自托管，数据已备好场景 |
| **API 接入** | OpenAI 兼容 `/chat/completions` | ✅ | 网页问个股、多步取数 |
| **MCP** | stdio JSON-RPC，复用 chat._exec_tool | ✅ | 给 Claude Code 等 agent |

## 后端模块

| 模块 | 职责 |
|---|---|
| `astock.py` | A 股五源分级数据层（腾讯/东财/akshare/mootdx/新浪） |
| `gstock.py` | 美股/港股/韩股（东财 push2 → push2delay 降级） |
| `market.py` | 市场情绪/板块资金/全球指数 |
| `newsradar.py` | 资讯雷达（108 RSS / 12 赛道） |
| `chat.py` | 系统 AI 对话层（5 工具 + 五维投研框架） |
| `mcp_server.py` | MCP server（stdio JSON-RPC） |
| `cli_runtime.py` | 订阅接入：调本机 CLI |
| `trading_workflow.py` | 打板工作流编排 |
| `workflow_state_machine.py` | 七态状态机 |
| `scheduled_tasks.py` | SQLite 持久化 cron 调度 |
| `circuit_breaker.py` | 数据源熔断器 |
| `risk_models.py` | 一日风险量化 |
| `notification/` | 多通道通知（15+ sender） |

## 数据层核心

### astock.py — A 股五源分级
- **腾讯**（`qt.gtimg.cn`，HTTP GBK）：行情/PE/PB/市值/换手/涨跌停。标准库 `urllib`，不封 IP，**永远可用**（底座 Layer 1）
- **东财**：研报/龙虎榜/解禁/融资融券/资金流/涨停四池等。**会封 IP**，统一走 `em_get()` 限流
- **akshare/mootdx**（惰性导入）：缺失时优雅报错，不挡启动

### em_get 限流策略
1. 串行限流：默认 1.0s + 抖动 0.1~0.5s，QPS≤2
2. 直连优先、失败降级系统代理
3. 熔断器：快速失败不重复重试

## 定时任务与打板工作流

### 定时调度
- CronScheduler：每 60s tick，5 段 cron 匹配，daemon 线程
- SQLite 持久化，10 种内置任务

### 打板工作流状态机
七态：`pending → candidate → watching → monitoring → holding → settled`，旁路 `filtered`

### 工作流编排
按时段判阶段：8-9 盘前 / 9-15 盘中 / 15-22 盘后

## 前端（React 19 + Vite 6 + TS）
- 30+ 页面路由
- 图表 echarts 6，Markdown react-markdown
- 玻璃暖橙主题

## 关键环境变量
- `VR_API_KEY` — API 鉴权
- `VR_DATA_DIR` — 数据目录（默认 `~/.vibe-research/`）
- `VR_DATA_PROXY` — 强制东财走代理

## 可扩展点
| 想加 | 改哪 |
|---|---|
| 新 A 股数据端点 | `astock.py`（东财走 `em_get`） |
| 新 AI 工具 | `chat.py` 的 `TOOLS` 加项 |
| 新 API 模型供应商 | 前端 `lib/ai-models.ts` 加条目 |
| 新页面 | 前端 `pages/` + `router.tsx`；后端 `routers/` |
| 新通知通道 | `notification/senders/` 加 sender |
| 新定时任务 | `scheduled_tasks.py` 的 `TaskExecutor._executors` |
| 新战法/策略 | `strategies/` 或 `limitup_strategy.py` |