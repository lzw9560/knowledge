---
type: procedure
layer: active
date: 2026-09-09
description: 晚上S173验证清单+本轮所有DO待办核销状态——验证步骤/文件/预期结果/未完成latent
---

# 晚上验证清单 + DO 待办核销（2026-09-09）

> 用户晚上验证 S173 Trade Journal 闭环 + 本轮全部 DO 待办核销。本文件是 checklist。

---

## A. S173 Trade Journal 验证清单（晚上必做）

### A1. 后端单测（4 新模块 55 tests）
```bash
cd /Users/lizhiwei/project/code/stock/Vibe-Research/backend
.venv/bin/python -m pytest tests/test_trade_journal.py tests/test_aggregate_stats.py tests/test_journal_recorder.py tests/test_drawdown_breaker.py -v
```
**预期**：55 passed, 0 failed（3.28s）。
- test_trade_journal（16）：CRUD + 迁移幂等 + is_dead_arm 不混聚合 + MTM + coverage_rate + underpowered gate
- test_aggregate_stats（15）：day_clustered_t_test + bonferroni_bh + compute_dsr + compute_haircut + Wilson CI + daily_aggregate_sharpe + underpowered + coverage_rate
- test_journal_recorder（11）：orchestrator 顺序管线 + breakout path_return + floor MTM + gap dead_arm + Trades 不带 signal_id（C8）+ 4 臂全录 + batch 模式
- test_drawdown_breaker（13）：绝对 CNY 回撤 + 阈值触发 + floor 豁免 + underpowered + 三层乘积 + 熊市 regime

### A2. 后端端点（2 新）
```bash
# 启 backend（若没跑）
cd backend && .venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8900 --reload
# 测端点（另开终端）
curl -s http://127.0.0.1:8900/api/journal/closed-loop | python3 -m json.tool
curl -s http://127.0.0.1:8900/api/journal/drawdown-status | python3 -m json.tool
```
**预期**：两端点 200 + JSON 结构（ClosedLoopResponse / DrawdownStatusResponse）。
**注意**：`:8900` 可能被旧进程占（memory `devserver-port-occupied-use-testclient`）——若 curl 打旧进程误判，用 TestClient 或 `lsof -i:8900` 确认。

### A3. 前端 UI（JournalLedger tab）
- `cd frontend && npm run dev`（:5899，strictPort=true 不静默+1）
- 浏览器开 `http://localhost:5899/journal` → 点"闭环"tab
- **预期**：JournalLedger 组件渲染（持仓+unrealized MTM+归因+coverage_rate+drawdown 状态）；error boundary 降级（后端没数据时不崩）
- `cd frontend && npx tsc --noEmit` 零错误

### A4. ⚠️ latent 提醒（call-point wiring 未接）
S173 orchestrator 模块实现 + 单测 mock 调用点验证逻辑，**但 call-point wiring 未接**（P2 完未改 premarket_selection/index_replication_floor，接线=1 行）。
- **没接 wiring 前 journal 空**（端点返空数组/默认 drawdown status，非真数据）
- 晚上验证看**单测 + 端点结构 + 前端 tab 渲染**，真数据要等 wiring
- **接 wiring（你说接就接，1 行）**：盘后流程或 scheduled_tasks 加 `from strategies.journal_recorder import JournalRecorder; JournalRecorder().run_daily(...)`。建议先看 P6 拆完 scheduled_tasks 后接（拆分时 seed.py 是接线点）

---

## B. 本轮 DO 待办核销（13 commits on develop）

### B1. ✅ DONE committed（git log 核销）
| commit | 待办 | 文件 |
|---|---|---|
| f833e8b | gap P0 接 accounting + 落盘 t/p | accounting.py +gap_net_return / s44_gap_run_60d.py |
| e084948 | 瘦身 P0 bugs + P3 spec 卫生 | scheduled_tasks 迁移逻辑 / 10 stale spec / archive S107/S155 / MILESTONES |
| cdf9c65 | 瘦身 P1 删死代码 1737 行 | 5 死文件删 + 3 文件死函数 + 3 测试清理 |
| 70f329d | 前端 nav 4 入口 + hithink wrapper | navigation.ts + hithink_src.py（解锁 7 特征）|
| da67270 | fund-flow 3 真 bug | risk_models 方向 gate + max_abs 跨源 + sina breaker |
| c180ae3 | S172 A 臂 ETF 实现 | fetch_etf_tracking + index_replication_floor + 18 tests |
| f808e45 | 瘦身 P4 verdict 精简 | DSR/PBO/haircut/MinTRL 停算 + Bonferroni 单算 |
| 5343b58 | position_advisor v1/v2 合一 | merge v2 到 v1 删 v2，950 行 latent |
| eababe0 | S174 P6 god-module 拆分 spec | specs/S174/spec.md 260 行 |
| df6de77 | P2 DRY baostock_src 迁 | baostock_src 9 接口 + 7 文件迁 |
| e844784 | P2 DRY safe_float 抽 | safe_convert.py + 2 文件迁 |
| e9ce79f | _parse_gtimg 五档提取 | tencent.py fields 9-28 + 4 tests |
| fa25be8 + 84a5c2d | **S173 Trade Journal impl + spec v2** | 4 新模块 + 4 测试 55 绿 + 17 grill fixes |

### B2. 🔄 RUNNING（2）
- **P6 S174 god-module 拆分 impl**（ac06cde2，主菜）——3 god-module→28 新文件 + re-export 兼容
- **Layer1 kline fetch**（PID 3613，数据底座）——baostock kline 4106 股 qfq+raw

### B3. ⏳ latent / 未起（bigger）
- **S173 call-point wiring**（1 行，P6 拆完 scheduled_tasks 后接，seed.py 是接线点）
- **skill-factor-orthogonalize**（等 conditioning harness 建好，打板/趋势设计提的）
- **conditioning harness**（打板/趋势设计提的 regime 分层 lift，未实现——等 60 天 live 数据）
- **lift_to_multiplier 接线**（selection 层 falsified，部分 superseded）
- **R3 enforce**（days_robust<60 cap，新 conditioning harness 用）

---

## C. 设计/讨论产出（KG active + memory，无 commit）

- 打板战法真实模型（[[打板战法真实模型]]）+ 打板量化模型设计（[[打板量化模型设计]]，6 盘中 conditional 因子）
- 趋势波段臂量化模型设计（[[趋势波段臂量化模型设计]]，7 维题材/政策趋势）
- #6 臂间相关 + portfolio 最终版（4 臂 + 发酵期 cap≤30% 正交化 + 数据基建多臂共用）
- A 股交易成本结构 / 异常交易监管 / 红利低波复合因子 / 动量因子 A 股 / 打板形态 §44 verdict 图
- 8 专家逐个讨论 verdict（成本会计师 / 合规监管 / 社区开源实践者 + 战法模型重新讨论）

---

## D. 用户决定/降级

- hithink key 轮换——**不换**（标了风险，遵决定）
- lift_to_multiplier——selection 层 falsified，部分 superseded
- S161 §44v2 verifier / S165 mock→gap——§44 re-examined + gap falsified，降级
- 剩余专家 #3 情绪 / #5 战法史——设计 workflow 覆盖相关角度

---

## E. 验证后 follow-up（P6 完后）

- P6 拆完 scheduled_tasks → **接 S173 call-point wiring**（seed.py 加 JournalRecorder seed + cron_runner 调 run_daily）→ journal 真录数据
- P6 全量 tests pass → 报 + 落 memory
- conditioning harness（打板/趋势设计的 regime 分层 lift）→ 下个 build（等 60 天 live 数据）

---

## 关联

- S173 spec: `specs/S173-TradeJournal闭环/spec.md`（333 行 v2，17 grill fixes）
- S173 impl: `backend/engine/trade_journal.py` + `drawdown_breaker.py` + `strategies/journal_recorder.py` + `frontend/components/journal/JournalLedger.tsx`
- memory: `s173-trade-journal-impl-done-2026-09-09` + `s173-grill-verdict-2026-09-09` + `expert-round-portfolio-overlay-2026-09-09`
