---
type: metric
layer: active
date: 2026-09-09
description: 打板各形态§44v2 selection verdict核实图(recorder.db 83行)——0 validated,尾盘封板late_lock最接近(p=0.012 lift1.33),二板anti
---

# 打板形态 §44 verdict 核实图

> 2026-09-09 从 recorder.db（83 行，frozen 2026-09-07）核实。打板 selection 层 **0 个 validated edge**。全库仅 2 条 robust_edge 都是 overnight_gap **event 层**（非 selection）。DB 无 t_stat 字段（t/p 全在 console 未落盘）。

## 连板梯队（lianban）— 全 underpowered

| 形态 | lift | n | days | p_perm |
|---|---|---|---|---|
| first_board | 0.973 | 2091 | 40 | 0.66 |
| **二板 lianban_2** | **0.9508** | 392 | 40 | 0.67 |
| lianban_2plus | 1.0066 | 663 | 40 | 0.45 |
| 连板3+ lianban_3plus | 1.1243 | 271 | 39 | 0.22 |

二板 lift<1（略劣随机，anti-edge）。

## 首板（first_plate_h2）— 全 underpowered，late_lock 最接近 edge

| 形态 | lift | n | days | p_perm |
|---|---|---|---|---|
| early_lock | 0.7843 | 311 | 41 | 1.0 |
| open_board | 0.9924 | 548 | 41 | 0.68 |
| **late_lock（尾盘封板）** | **1.3326** | 94 | 38 | **0.012** |
| late_x_auction | 1.1064 | 44 | 29 | 0.30 |

**late_lock 是纯打板因子中 lift 最高、p 最低（0.012<0.05）的——唯一卡 R6 gate 的是 days=38<60。最值得攒样本到 60+ 天复验的候选形态。**

## 涨停池封板时间（zt_pool_seal_time）— 全 underpowered

| 形态 | lift | n | days | p_perm |
|---|---|---|---|---|
| seal_amount（封单强度比） | 1.1623 | 153 | 12 | 0.13 |
| early_lock（封板早） | 1.0461 | 451 | 13 | 0.25 |
| late_lock（封板晚·此版） | 0.6201 | 63 | 11 | 0.90 |
| miaoban（秒板） | 1.124 | 122 | 13 | 0.27 |
| broken（炸板回封） | 0.999 | 412 | 13 | 0.52 |

⚠️ **late_lock 定义敏感**：first_plate_h2 版 lift 1.33（信号）vs zt_pool_seal_time 版 lift 0.62（反信号）。两版「尾盘封板」定义不同结果相反——下注前必须锁定 first_plate_h2 版精确定义。

秒板（miaoban，另测）：lift 0.36/0.31，强 anti-edge。

## 隔夜 gap — event **FALSIFIED**（P0 fix 2026-09-09），selection anti

- overnight_gap **event**（涨停股次日开盘 gap 捕获）：原 robust_edge，**P0 接 accounting.py 真成本后 FALSIFIED**——net mean −0.48%（was +0.53%），t=−3.79（was +4.12），winrate 39.5%，status=falsified/event_falsified。根因：5 元最低佣金对低价首板灾难（真成本 1.81% vs flat 0.70%，低价股 53%），gap +1.32% gross 扛不过。t/p 现已落盘 recorder.db（pit:5），会计单测 8/8 + 全量 89/89 过。nuance：falsified 是首板 universe（低价主导），高价股成本 0.75% gap 可能活但未测。
- gap_window **selection**（gap 作选股信号）：lift 0.9127, n=169, days=14, p=0.83——**anti-edge**。gap event 也 falsified 了，整个 gap 无 edge，从 portfolio drop。

## 打板邻接（非纯打板）

- **platform_breakout:both_bull**（双牛突破）：lift 1.4156, n=97, days=39, p=0.0299——打板邻接最高，underpowered，另一候选
- platform_breakout:confirm：exploratory lift 1.08, n=944, days=109
- low_absorption_c3（低吸）：lift ~1.0, exploratory/falsified

## KG 10 因子中无 verdict 的

量比换手 / 题材热度 / OFI盘口（需 L2 未接线）/ 竞价量能 / 情绪周期——未测，不能当 edge 用（[[limitup-factor-knowledge-graph-2026-09-09]] 10 因子 5/10 无 verdict）。

## verdict：打板用什么形态

- **0 validated**（selection 层全 underpowered/exploratory/falsified）
- **最值得复验**：first_plate_h2:late_lock（尾盘封板，p=0.012 lift 1.33，days 不足）+ platform_breakout:both_bull（p=0.030 lift 1.42，days 不足）——攒 60+ 天复验过 R6 gate 才算候选
- **明确 anti-edge（别用）**：二板 0.95、秒板 0.36、封板晚(zt版) 0.62、首板层 0.87-0.92
- **gap**：只 event 捕获 robust（t/p 未落盘待重算），selection 层 anti

## §44 harness scope & holes（2026-09-09 代码核实）

查 harness 代码（`lianban_lift.py` / `zt_pool_seal_time_lift.py` / `first_plate_h2_lift.py` / `gap_window_lift.py` / `kline_returns.py`）确认 4 个方法论 hole：

- **窗口**：selection harness 全 T-1 selection→D+1 path（entry=D+1 open，stop-3%/take+8%/hold3 天；`first_plate_h2`=D+1 o2c）。**没测盘中封板 entry**。但代码 header caveat 自标「D+1-开盘→D+4 path = 隔夜正之后的反转负段，非绝对无 edge」——代码诚实标 scope，放大成「打板无 edge」的是我。
- **conditioning（最大 hole）**：三 harness 全池化，**无 regime/市值/板块分层**。`day_paired` 只防簇聚不防混杂。→ **lift<1 可能是 confounder**（late_lock 偏小盘→小盘次日反转→lift<1 反映小盘属性非 late_lock 反预测）。要证否须补「市值/regime 分层 lift」，代码没有。
- **定义**：late_lock 两版（5min kline 粗 vs akshare 精确）概念一致（首封>14:00），entry 口径错配（实战盘中封板买 vs harness D+1 open）= 窗口同源。
- **survivorship**：universe 全已涨停池（无炸板/冲板失败对照），但 selection lift 是 survivor 池内比较，survivorship 影响小于「涨停 vs 非涨停」——真正风险落回 conditioning。

**结论**：§44 测 selection 层 D+1 path（涨停已成的次日续涨力），**不是盘中封板 entry**；lift<1 在当前口径成立但 conditioning hole 意味着可能是 confounder 假象。要彻底证否须补分层 + 盘中 entry + 炸板对照。→ 触发「重新讨论战法模型」（浅模型测无 edge ≠ 战法无 edge）。

## 关联

[[00_Active/projects/vibe-research/expert-rounds/A股异常交易监管]]（late_lock 真买不撤单 legal）+ [[00_Active/projects/vibe-research/expert-rounds/A股交易成本结构]]（打板成本最差 1.0-1.5%）+ memory `expert-round-compliance` + `gap-edge-cost-never-wired`（gap t/p 未落盘）。
