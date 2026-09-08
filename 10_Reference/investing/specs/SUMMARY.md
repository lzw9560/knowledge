---
type: summary
title: Spec 归档总结
created: 2026-09-06
updated: 2026-09-08
---

# Spec 决策总结

> 知识图谱 specs/ 目录的 109 个 spec/decision/project 实体的归档总结。
> 按里程碑分组，每组列出 spec 编号 + 标题 + 核心决策一句话。

## 统计

- 总数：109（101 spec + 5 DEC + 3 项目）
- 已实现：92（91 归档 + 1 活跃 S150）| 草案：8 | 已废弃：1
- 里程碑：M0-M7 共 8 个（全部 ✅ 已完成）
- 项目实体：4（Vibe-Research + trading-agents + daily-stock-analysis + a-Plate-Sentinel）

## 按里程碑分组

### M0 地基（S001-S020，2026-07-28 ~ 08-01）✅

系统重写：契约层/数据层/调度收口/UI 重设计/测试网/ML 预测栈/多源特征/宏观/另类数据。归档 `archive/m0-foundation/`（16 已实现 + 4 草案留根）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S001 | 修复 chat._get_env_llm_config | 补全环境变量兜底函数，打通问 AI |
| S002 | 打板工作流重构 P1 | 短线候选池漏斗 + 诊断卡，六类指标口径统一 |
| S003 | 后端 API 冒烟缺陷修复批次 | API 缺陷批量修复（含 value_funnel 等） |
| S004 | 候选池漏斗性能优化 | 缓存+预计算+top-N 限界+独立 source 并行（草案） |
| S005 | 中长线价值选股漏斗 | 价值四层漏斗 + 去劣 7 条 |
| S006 | 系统重写纲领 | 数据契约统一+调度收口+前端 UI 重设计+测试网（草案） |
| S007 | 契约层 | Pydantic v2 7 模型 + 10 只 code 基线夹具 + 前后端契约骨架 |
| S008 | 后端数据层迁移 | 返模型+response_model+T13 全批次迁 C 组 engines + 删 data_provider |
| S009 | 前后端类型同步 | dump_openapi.py+openapi-typescript+types.ts 就位 |
| S010 | AI 工具注册表 + SYSTEM_PROMPT | registry 声明式+chat/mcp/cli 解耦+SYSTEM_PROMPT 按新边界放宽 |
| S011 | 调度收口 | 扩展 cron+lifespan+WAL+去重+状态机落库（不引 APScheduler） |
| S012 | 工作流标灰 | 桩→NotImplementedError+UI 标灰，不补功能（草案） |
| S013 | 前端数据层 | client 统一+router 懒加载+QueryProvider+59 hooks+17 页接线 |
| S014 | 前端 UI 重设计 | 22 项→5 组+首页下沉+巨型 page 拆分+三态统一+移动端 |
| S015 | 配置与基础设施 | 收口 4+套缓存/限流/熔断+修 cache_response key+metrics 配置化 |
| S016 | 测试网 | 纯函数≥80%+IO 录制回放+前端快照+CI 门槛（草案） |
| S017 | A 股涨跌预测模型栈 | 短线×板块起步，LGB+CatBoost+HMM+Conformal，输出概率+分位区间 |
| S018 | 多源特征工程 | 特征注册表+可得时间对齐表+北向分段+SHAP/Boruta 选≤25 特征 |
| S019 | 宏观 Fred API | 美债 10Y/DXY 走 Fred 独立通道+key 隔离 VR_DATA_DIR |
| S020 | worldmonitor 决策因子接入 | 远程 MCP 互补另类数据层接 newsradar/market/特征栈，Fred 仍主源 |

### M1 工作流（S022-S048，2026-08-02 ~ 08-10）✅

漏斗/拓扑/状态机/结算/标灰/回测/持仓/因子补全/空写防护/权重校准/工作流打磨。归档 `archive/m1-workflow/`（25 已实现 + 1 已废弃）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S022 | 熔断器 health 读路径修复 | peek_state 只读探测 + health 读路径自愈 |
| S023 | 漏斗可用性与因子解耦 | 选股因子与工作流解耦，两套标准可插拔并存 |
| S024 | 拓扑展示 | 候选标的关系网+漏斗流向可视化+连板接力结构 |
| S025 | 补前端入口 | code review 14/14 闭环，tsc 0 + vitest 98 绿 |
| S026 | pre-market 异步化 | 盘前简报异步采集缓存 + 并发守卫（并入 S023） |
| S028 | limitup-screener 修复 | 文案三态/trigger/因子层 conditions，9 测试 + 778 passed |
| S029 | GeneScreener 接通 | 阈值可配+执行检索+多层明细，149 前端测试 + build 绿 |
| S030 | 盘前简报多层化 | 三层漏斗+抽屉+布局重整，经 grill 后合并为 S031（已废弃） |
| S031 | 调度收口+盘前多层+战法回测 | WAL/lifespan/预计算收口+因子三层漏斗+战法反筛+真实回测 WinRatePanel |
| S032 | 调度收口第二轮 | ticker/持仓刷新挂主循环+日志重试+workflow_state 落库 |
| S033 | 状态机前端呈现 | workflow_state 扩列+单股端点+列表徽标/抽屉状态卡/流转交互 |
| S034 | 结算接线 | settled 流转触发结算写 winrate_records；settled_at 幂等锚点 |
| S035 | ai_proxy 删除 | 删 ai_proxy 路由 + 死代码清理 |
| S036 | 工作流标灰（修订版） | 适配状态机/结算后的前端标灰，桩→NotImplementedError |
| S037 | gene DB 路径迁移 | gene_scores/winrate/market_data 三库统一 VR_DATA_DIR |
| S038 | 持仓市价自动结算 | settled 流转拉 tencent_quote 市价预填 exit_price |
| S039 | StockDeep 接线 | 个股深度页接已有端点，第一批核心四块 |
| S040 | 历史数据回填 90 天 | K 线重建 122 天 + eastmoney_live 27 天，DB 覆盖 149 交易日 |
| S041 | 回测定时任务+趋势看板 | daily_backtest_run task_type + backtest_daily_snapshots 表 + 趋势端点 |
| S042 | 统一持仓建议引擎 | position_advisor_v2 + advisory 路由 + Advisory.tsx 三场景页 |
| S043 | 次日溢价率单因子分析 | 因子分位端点 + 前端因子分位 Tab |
| S044 | 候选池漏斗数据源补全 | 四源补全 + 板块源 live 修复（push2delay+防封） |
| S045 | 漏斗层得分排序筛选 | FunnelLayerCard 得分显示 + 降序排序 + 多选筛选 |
| S046 | fallback 空写防护 | _is_empty + 空不写缓存 + 损坏自愈删除 + 降级好缓存 |
| S047 | 基因分权重回测校准 | full 权重改 40/25/25/0/10 + 历史 2023 行复算 |
| S048 | 工作流打磨 | 固定阶段位 + 历史视角 + 缓存 + 拓扑精简 |

### M2 闭环（S049-S065，2026-08-10 ~ 08-13）✅

行动闭环/行为对照/因子 IC/验证卡/预测跟踪/情绪管线/盯盘教练/天气持久化。归档 `archive/m2-closed-loop/`（17 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S049 | 盘前简报漏斗重构与诊断修正 | 漏斗重构与诊断修正，子项 A/B/C/D 全落地 |
| S050 | W0 行动闭环 | 票根 + 影子对照 + 独立性基线 |
| S051 | 基因筛选体验批 | 阈值复位 50/60 + sanity 警告 + 分段视图 + 动态文案 |
| S052 | 回测快照回填与缺口补跑 | as_of_date 参数化 + 60 交易日回填 + 启动缺口补跑 |
| S053 | 炸板后溢价因子修复 | 数据源+计算重定义+match 解耦，pytest 1102 passed |
| S054 | W0 工作流闭环呈现 | 盘后三问 + 简报行为卡，T1-T9 全落地 |
| S055 | 盘中封单时序采集与炸板预警 | 封单时序采集 + 炸板预警规则引擎，live 冒烟通过 |
| S056 | 天气熔断三铁律补全 | 三铁律软 gate（只提醒不锁死） |
| S057 | 漏斗八项标准硬约束封顶 | 八项硬约束封顶，三态判定 missing 不臆造 |
| S058 | 战法双层卡片层与天气适配过滤 | 战法双层卡片 + 天气适配软过滤 + query_strategy_card 三出口 |
| S059 | 因子 IC 评估 | IC 评估扩展，样本<20 返 None 诚实标注 |
| S060 | 明日验证条件对账卡 | 纯规则模板客观可测，后端 19 + 前端 4 测试 |
| S061 | 预测跟踪与自动验证 | 预测账本——判断跟踪 + 到期自动验证 + 命中率统计 |
| S062 | 战法卡内容填充：反包/龙头 | 反包/龙头战法卡实盘参数填充 |
| S063 | 情绪管线贯通与盘中辅助决策 | SentimentContext T-1 贯通 + 盘中 4 维评分 + T+1 投影 |
| S064 | W-C 盯盘教练 MVP | 盘中时刻表 10 槽位 + 条件状态清单 + attention_mode A/B/C |
| S065 | weather_history 持久化 | 盘后落 weather_state 快照 + 五因子明细 |

### M3 战法统一（S066-S086，2026-08-13 ~ 08-21）✅

策略漏斗/性能/首板流/战法 pipeline/选股池分层/暴风雨/SQLite 并发/echarts。归档 `archive/m3-strategy/`（19 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S066 | 策略特定漏斗架构重构 | 3 套权重漏斗 + 天气硬开关 + 板块周期 + 日历因子 + 前端三页统一 |
| S067 | advisory 端点性能优化 | 缓存+预热+并发+批量+超时降级，>40s→0.34s |
| S068 | 工作流触发与结算正确性 | 盘前/盘中/盘后触发点 + 结算时序对齐 |
| S069 | 每日 forward_test 管道 | forward_test 流程框架打通；待 prod baostock 验证 live 日积 |
| S070 | intraday 采集管道 | 盘中 ephemeral → 盘后离线 §44 60 日复验窗口 + 战法因子派生 |
| S071 | 盘前选股谨慎部署 | breakout 弱信号 + 风控；定位待确认未投真金 |
| S072 | 涨停叉 pipeline 诚实可观测 | weights drift 修 + 前端诚实层 + forward 基线标注 |
| S074 | market_phase 统一判定 | 盘前盘后时段统一（当日收盘→次日开盘）+ post-market 桩对接 |
| S075 | 首板流 | 首个战法工作流：从"找涨停中谁最好"转向"剔除首板中谁会亏" |
| S076 | 首板流盘中多源行情实测 | 多源行情盘中闭环实测（纯探查脚本零生产改动） |
| S077 | 首板流剔除层 lift 验证 | 独立研究脚本 + 30 天 smoke 通；lift 1.01-1.06 待 120 天全量复验 |
| S078 | 涨停历史 snapshot 数据地基 | snapshot 表 + 15 日 backfill + daily task cron `0 16` 累积 |
| S079 | 打板 P2 战法与仓位闸 | 仓位闸 + 龙虎榜黑名单（不依赖 S070/S081） |
| S081 | 打板 P2 战法匹配 | S070 R7 就绪后扩展战法匹配 |
| S082 | echarts 按需引入 | useECharts chunk 558.93KB/gzip 190.45KB + graph/tree 下沉 Topology |
| S083 | 工作流重构选股池分层 | 漏斗接入 pre_market_workflow |
| S084 | 选股池战法解耦 | 两级 tab 导航 + 因子补全 |
| S085 | 因子全量补全与游资画像 | 32 因子 5+ bug 修 + 22 backlog 透传 + 预警 5 因子 + 游资画像 + 防封 |
| S086 | 涨停战法 pipeline 统一架构 | dispatch_match 统一（S066/S072/S081/S084 衔接） |

### M4 三视图（S087-S093，2026-08-21 ~ 08-22）✅

工作流 tab 重构/暴风雨预测/SQLite 并发/premarket 接入/限流容错/交易日锚/内容重组。归档 `archive/m4-三视图/`（7 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S087 | 工作流 tab 按 pipeline 重设计 | 设计被 S093 吸收实现 |
| S088 | 盘前暴风雨预测 | 设计被 S093 吸收实现 |
| S089 | SQLite 并发性能加固与分表分库 | WAL+busy_timeout 落地；分表分库 deferred |
| S090 | premarket 选股前端接入与 kline 日更 | 接 endpoint + live kline 日更 + 风控 + 前端 |
| S091 | gstock 限流容错优化 | 加 KOSPI/SOX + push2 间歇限流记忆 + 异常诊断 |
| S092 | 三视图交易日锚与时段推进 | 设计被 S093 吸收实现（跨前后端 medium） |
| S093 | 三视图内容重组与飞书通知 | 6 阶段全闭合；后端 2215 + 前端 428 passed（large，Oracle 4 轮审查） |

### M5 战法细化（S094-S097，2026-08-22 ~ 08-26）✅

战法分类双 pipeline / gene_scores 写路径 / P2 现象判据 / 逐条件因子过滤。归档 `archive/m5-战法细化/`（4 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S094 | 战法分类与双 pipeline 重构 | 涨停/非涨停双 pipeline + score_candidates 分流 + confidence 统一（large，2269 passed） |
| S095 | gene_scores 写路径修复与日期守卫 | 6 tests 全绿 + 全量 2226 passed + 七日 7/7 code 集合全等 |
| S096 | P2 现象判据暴露 | grill Q1 完整链 + Q2 红期 override + 数据降级标注 |
| S097 | 逐条件因子过滤 | 12 战法三态 + 批次聚合 + 前端漏斗；对抗验证 2 bug 修；2275 passed |

### M6 首板流 §44 合规（S098，2026-08-26）✅

首板流 select 不 auto-rank + 确认时间序（§44 合规，raw-shadow 路径）。归档 `archive/m6-合规/`（1 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S098 | 首板流选股 §44 合规修复 | select 不 auto-rank + 确认时间序；29 测试绿，全量 2279 passed |

### M7 战法卡片对齐（S100-S101，2026-08-27）✅

S097 match 重构后 cards/*.md 卡片跟上 + fa4514e 阈值残局收拾。归档 `archive/m7-卡片对齐/`（2 已实现）。

| 编号 | 标题 | 核心决策 |
|---|---|---|
| S100 | 战法卡片对齐 match 条件 | 12 卡片 + docstring + registry entry_condition + 一致性测试；2281 passed |
| S101 | 飞书多点通知 | T-1 cron 17:15 + final=0 guard + 3 新 executor + 内容函数 + seed；2295 passed |

### 活跃 spec（S102+，留根目录）

M7 完成后的活跃/草案 spec，保留在 `specs/` 根目录。

| 编号 | 标题 | 核心决策 | 状态 |
|---|---|---|---|
| S102 | 战法卡片历史战绩 | S100 延伸；strategy_backtest 12h 缓存拼接进卡片；§44 口径 | 🟡草案 |
| S149 | vibe-astock 语义吸收 | fork 回流选择性吸收；Phase 0 审计→P4 试点→P2 冲突审查→P3 边界测试→P1 视需求 | 🟡草案 |
| S150 | 盘中采集堵塞修复 | R1 timeout+R2 reaper 防 collect_once 挂死堵 dedup；6 unit test + 2676 回归绿 | ✅已实现 |
| S151 | 漏斗评价层 | 预登记+降权梯度+回溯+诚实标注+即时处理；复用 judge_lift_four_states | 🟡草案 |
| S153 | 量化模型验证 | H1-H4 预注册+R1-R10+harness（walk-forward+day-cluster 置换+Bonferroni） | 🟡草案 |

> M0 草案 spec（留根目录）：S004（漏斗性能优化）、S006（系统重写纲领）、S012（工作流标灰）、S016（测试网）。

### DEC 决策记录（留根目录）

| 编号 | 标题 | 核心决策 |
|---|---|---|
| DEC-001 | 候选池漏斗性能优化路线 | 缓存+预计算+top-N，否决逐只并发（em_get 全局锁退化为串行） |
| DEC-002 | 宏观特征 7 系列定稿 | FRED 7 系列（DGS10/DTWEXBGS/DFF/T10Y2Y/DEXCHUS/DCOILWTICO/PCOPPUSDM）入 short_sector |
| DEC-003 | 短线胜率优化 grill 裁决 | D1-D7 全通过：weather 硬闸门+no_history/data_missing 分类+三 edge 族架构 |
| DEC-004 | 盯盘教练+降级策略+方向建议口径 | W-C 盯盘教练阶段+"有据才给"六条+C 档四铁律 |
| DEC-005 | notes/debate 路由无独立 spec | 历史遗留代码，不追溯补 spec，标 wontfix |

### 项目实体（留根目录）

| 项目 | 状态 | 图谱实体数 |
|---|---|---|
| Vibe-Research | 活跃 | 109 spec + 16 数据源 + 12 战法 + 5 DEC |
| trading-agents | 活跃 | 7 AI 角色 + 项目实体 |
| daily-stock-analysis | 活跃 | 项目实体 |
| a-Plate-Sentinel | MVP 骨架 | 项目实体 + Tushare |

## 归档建议

- M0-M7 已实现 spec（91）+ 已废弃 S030 → 移到 `archive/` 对应里程碑子目录
- M0 草案 spec（S004/S006/S012/S016）→ 保留在 `specs/` 根
- 活跃 spec（S102/S149/S150/S151/S153）→ 保留在 `specs/` 根
- DEC-001~005 + 项目实体 → 保留在 `specs/` 根

### archive/ 目录结构

```
specs/
├── archive/
│   ├── m0-foundation/   # S001-S020 已实现（16 个，草案 4 个留根）
│   ├── m1-workflow/      # S022-S048（26 个，含 S030 已废弃）
│   ├── m2-closed-loop/   # S049-S065（17 个）
│   ├── m3-strategy/      # S066-S086（19 个）
│   ├── m4-三视图/         # S087-S093（7 个）
│   ├── m5-战法细化/       # S094-S097（4 个）
│   ├── m6-合规/          # S098（1 个）
│   └── m7-卡片对齐/      # S100-S101（2 个）
├── DEC-001.md ~ DEC-005.md  # 保留在根
├── *-project.md              # 项目实体保留在根
├── SUMMARY.md                # 本总结
└── index.md                  # 索引（链接已更新）
```
