# 项目决策 索引

> SDD spec 决策实体节点。对应 `specs/` 目录下的 spec 文档。每条记录链接其问题/目标、需求、受影响文件、验收标准、关联决策。
> 里程碑归档总结见 [[10_Reference/investing/specs/SUMMARY]]；已实现 spec 已移至 `specs/archive/mN-xxx/` 子目录，草案/活跃 spec 留根目录。

## Spec 实体列表（Dataview 动态）

<!-- dataview-precompiled:61df89bc78b3 -->
| 编号 | 标题 | 状态 |
|---|---|---|
| S001 | 修复 chat._get_env_llm_config 缺失 → /api/chat 500 | 已实现 |
| S002 | 打板工作流重构 · P1 候选池诊断统一 | 已实现 |
| S003 | 后端 API 冒烟测试缺陷修复批次 | 已实现 |
| S004 | 候选池漏斗 run_funnel 性能优化 | 草案 |
| S005 | 中长线价值选股漏斗（与短线 S002 并列） | 已实现 |
| S006 | 系统重写纲领（渐进式长分支） | 草案 |
| S007 | 契约层（数据模型+回归基线+契约测试骨架） | 已实现 |
| S008 | 后端数据层迁移（astock/gstock/market→模型） | 已实现 |
| S009 | 前后端类型同步（openapi-codegen） | 已实现 |
| S010 | AI 工具注册表 + SYSTEM_PROMPT 新边界 | 已实现 |
| S011 | 调度收口（删 scheduler.py+重写 scheduled_tasks+状态机接线） | 已实现 |
| S012 | 工作流标灰（realtime/post 桩+pre 清理） | 草案 |
| S013 | 前端数据层（统一 client+TanStack Query+懒加载+apiKey 代理） | 已实现 |
| S014 | 前端 UI 重设计（信息架构+交互统一+视觉+AI 对话） | 已实现 |
| S015 | 配置与基础设施（config 拆分+infra 收口+路由自动发现） | 已实现 |
| S016 | 测试网（后端覆盖率+IO 录制回放+前端 vitest+CI） | 草案 |
| S017 | A股涨跌预测模型栈（四头解耦） | 已实现 |
| S018 | 多源特征工程（预测模型特征供给） | 已实现 |
| S019 | 宏观特征 Fred API 接入（macro.py 第二批） | 已实现 |
| S020 | worldmonitor 决策因子接入（全球宏观/地缘/另类数据） | 已实现 |
| S022 | 熔断器 health 读路径修复（尊重 recovery_timeout） | 已实现 |
| S023 | 漏斗可用性与因子解耦（P1 打磨：盘前简报接因子+候选详情依据链+漏斗每层可观测可调参+真实数据不静默返空） | 已实现 |
| S024 | 拓扑展示（关系网+漏斗流程+连板梯队树，EdgeProvider 扩展位） | 已实现 |
| S025 | 补前端入口 | 已实现 |
| S026 | pre-market 异步化 | 已实现 |
| S028 | limitup-screener 修复（文案三态/trigger/因子层 conditions） | 已实现 |
| S029 | GeneScreener 接通（阈值可配+执行检索+多层明细） | 已实现 |
| S030 | 盘前简报多层化 + UX 收敛 | 已废弃 |
| S031 | 调度收口 + 盘前简报多层 + 交互式战法 + 按战法回测 | 已实现 |
| S032 | 调度收口第二轮（S011b）：主循环收口 + portfolio 日志重试 + 状态机接线落库 | 已实现 |
| S033 | 状态机前端呈现（状态徽标+流转按钮+holding 价格采集） | 已实现 |
| S034 | SettlementEngine 接线（settled 流转即结算写 winrate.db） | 已实现 |
| S035 | ai_proxy 删除（死代码清理） | 已实现 |
| S036 | 工作流标灰（S012 修订版：适配 S033/S034 后的前端结构） | 已实现 |
| S037 | gene DB 路径迁移（三库 + winrate 统一到 .vibe-research/） | 已实现 |
| S038 | 持仓市价自动结算（holding 流转 settled 时自动拉价填 exit_price） | 已实现 |
| S039 | StockDeep 个股深度页面接线（消费已有端点，第一批核心四块） | 已实现 |
| S040 | 历史涨停池数据 K 线重建 + 双轨累积（v2） | 已实现 |
| S041 | 回测定时任务 + 趋势看板 | 已实现 |
| S042 | 统一持仓建议引擎（推荐标的 + 自选 + 持仓，三场景） | 已实现 |
| S043 | 次日溢价率单因子分位分析 | 已实现 |
| S044 | 候选池漏斗数据源补全（北向 + 板块联动 + 龙虎榜游资频次 + 公告类型化） | 已实现 |
| S045 | 漏斗层得分显示 + 得分排序 + 多选筛选 | 已实现 |
| S046 | fallback 空写防护（限流返空不覆盖好缓存） | 已实现 |
| S047 | 基因分权重口径回测校准 | 已实现 |
| S048 | 工作流打磨（固定阶段位 + 历史视角 + 缓存 + 拓扑精简） | 已实现 |
| S049 | 盘前简报漏斗重构与诊断修正 | 已实现 |
| S050 | W0 行为闭环（票根 + 影子对照 + 独立性基线） | 已实现 |
| S051 | 基因筛选体验批 | 已实现 |
| S052 | 回测快照回填与缺口补跑 | 已实现 |
<!-- /dataview-precompiled -->

## Decision 实体列表（Dataview 动态）

<!-- dataview-precompiled:4204334238cb -->
| 编号 | 标题 | 状态 |
|---|---|---|
| DEC-001 | 候选池漏斗性能优化技术路线 | 已采纳 |
| DEC-002 | 宏观特征 7 系列定稿 | 已采纳 |
| DEC-003 | 短线胜率优化 grill 裁决 | 已采纳 |
| DEC-004 | 盯盘教练 + 降级策略 + 方向建议口径 | 已采纳 |
| DEC-005 | notes/debate 路由无独立 spec | 已采纳 |
<!-- /dataview-precompiled -->

## 关系

- defines: [[10_Reference/investing/strategies/index|strategies/]]（spec 定义战法 match 逻辑）
- references: [[10_Reference/investing/data-sources/index|data-sources/]]（spec 引用数据源）
- depends_on: [[10_Reference/investing/specs/index|specs/]]（spec 间依赖/栈式关系）

## 新建实体

用 Templater 应用 `templates/spec` 新建。

## 已灌入 spec（2026-09-07 第二批扩充）

> 第一批 13 spec + 5 decision（2026-09-06）。第二批补入断链修复所需的 17 spec stub（2026-09-07）。详见源 `specs/README.md`（S001-S166 全量索引）与 `specs/decision-log.md`（DEC-001~005）。

### 已实现 / 关键架构 spec（第一批 13）

- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]] · [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移]] · [[10_Reference/investing/specs/archive/m0-foundation/S010-工具注册表与SYSTEM_PROMPT]] · [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口]] · [[10_Reference/investing/specs/archive/m0-foundation/S017-A股涨跌预测模型栈]] · [[10_Reference/investing/specs/archive/m0-foundation/S018-多源特征工程]] · [[10_Reference/investing/specs/archive/m0-foundation/S019-macro-Fred-API]] · [[10_Reference/investing/specs/archive/m0-foundation/S020-worldmonitor决策因子接入]] · [[10_Reference/investing/specs/archive/m1-workflow/S031-调度收口盘前多层按战法回测]] · [[10_Reference/investing/specs/archive/m1-workflow/S047-基因分权重回测校准]] · [[10_Reference/investing/specs/archive/m3-strategy/S066-策略特定漏斗架构重构]] · [[10_Reference/investing/specs/archive/m5-战法细化/S094-战法分类与双pipeline重构]] · [[10_Reference/investing/specs/archive/m7-卡片对齐/S100-战法卡片对齐]]

### 断链修复 stub（第二批 17，从 README 索引灌入摘要）

- [[10_Reference/investing/specs/S004-candidates-funnel-performance]] · [[10_Reference/investing/specs/S006-系统重写纲领]] · [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]] · [[10_Reference/investing/specs/archive/m0-foundation/S013-前端数据层]] · [[10_Reference/investing/specs/archive/m0-foundation/S015-配置与基础设施]] · [[10_Reference/investing/specs/archive/m1-workflow/S023-漏斗可用性与因子解耦]] · [[10_Reference/investing/specs/archive/m1-workflow/S030-pre-market-multilayer]] · [[10_Reference/investing/specs/archive/m1-workflow/S032-调度收口第二轮]] · [[10_Reference/investing/specs/archive/m1-workflow/S041-回测定时任务与趋势看板]] · [[10_Reference/investing/specs/archive/m1-workflow/S042-统一持仓建议引擎]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S049-盘前简报漏斗重构与诊断修正]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S064-盯盘教练MVP]] · [[10_Reference/investing/specs/archive/m3-strategy/S075-首板流]] · [[10_Reference/investing/specs/archive/m3-strategy/S086-涨停战法pipeline统一架构]] · [[10_Reference/investing/specs/archive/m5-战法细化/S097-逐条件因子过滤]] · [[10_Reference/investing/specs/archive/m7-卡片对齐/S101-飞书多点通知]] · [[10_Reference/investing/specs/S102-战法卡片历史战绩]]

### 第三批 spec stub（fix-17/18 灌入，2026-09-07）

> 以下 stub 由源仓 spec 批量抽取生成，正文为摘要级，待按需深化。列入此段以建立入边，消除孤立。

- [[10_Reference/investing/specs/archive/m0-foundation/S001-fix-chat-env-llm-config]] · [[10_Reference/investing/specs/archive/m0-foundation/S002-打板工作流重构]] · [[10_Reference/investing/specs/archive/m0-foundation/S003-api-bugfix-batch]] · [[10_Reference/investing/specs/archive/m0-foundation/S005-中长线价值选股漏斗]] · [[10_Reference/investing/specs/S012-工作流标灰]] · [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计]] · [[10_Reference/investing/specs/S016-测试网]] · [[10_Reference/investing/specs/archive/m1-workflow/S022-熔断器health读路径修复]] · [[10_Reference/investing/specs/archive/m1-workflow/S024-拓扑展示]] · [[10_Reference/investing/specs/archive/m1-workflow/S025-补前端入口]] · [[10_Reference/investing/specs/archive/m1-workflow/S026-pre-market-async]] · [[10_Reference/investing/specs/archive/m1-workflow/S028-limitup-screener-fix]] · [[10_Reference/investing/specs/archive/m1-workflow/S029-gene-screener-wireup]] · [[10_Reference/investing/specs/archive/m1-workflow/S033-状态机前端呈现]] · [[10_Reference/investing/specs/archive/m1-workflow/S034-结算接线]] · [[10_Reference/investing/specs/archive/m1-workflow/S035-ai-proxy-删除]] · [[10_Reference/investing/specs/archive/m1-workflow/S036-工作流标灰]] · [[10_Reference/investing/specs/archive/m1-workflow/S037-gene-db-迁移]] · [[10_Reference/investing/specs/archive/m1-workflow/S038-持仓市价自动结算]] · [[10_Reference/investing/specs/archive/m1-workflow/S039-StockDeep接线]] · [[10_Reference/investing/specs/archive/m1-workflow/S040-历史数据回填90天]] · [[10_Reference/investing/specs/archive/m1-workflow/S043-次日溢价率单因子分析]] · [[10_Reference/investing/specs/archive/m1-workflow/S044-候选池漏斗数据源补全]] · [[10_Reference/investing/specs/archive/m1-workflow/S045-漏斗层得分排序筛选]] · [[10_Reference/investing/specs/archive/m1-workflow/S046-fallback空写防护]] · [[10_Reference/investing/specs/archive/m1-workflow/S048-工作流打磨]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S050-W0-行动闭环]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S051-基因筛选体验批]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S052-回测快照回填与缺口补跑]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S053-炸板后溢价因子修复]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S054-W0-工作流闭环呈现]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S055-盘中封单时序采集与炸板预警]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S056-天气熔断三铁律补全]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S057-漏斗八项标准硬约束封顶]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S058-战法双层卡片层与天气适配过滤]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S059-因子IC评估]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S060-明日验证条件对账卡]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S061-预测跟踪与自动验证]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S062-战法卡内容填充-反包与龙头]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S063-情绪管线贯通与盘中辅助决策]] · [[10_Reference/investing/specs/archive/m2-closed-loop/S065-weather-history持久化]] · [[10_Reference/investing/specs/archive/m3-strategy/S067-advisory-perf]] · [[10_Reference/investing/specs/archive/m3-strategy/S068-工作流触发与结算正确性]] · [[10_Reference/investing/specs/archive/m3-strategy/S069-每日forward_test管道]] · [[10_Reference/investing/specs/archive/m3-strategy/S070-intraday采集管道]] · [[10_Reference/investing/specs/archive/m3-strategy/S071-盘前选股谨慎部署]] · [[10_Reference/investing/specs/archive/m3-strategy/S072-涨停叉pipeline诚实可观测]] · [[10_Reference/investing/specs/archive/m3-strategy/S074-market_phase统一判定]] · [[10_Reference/investing/specs/archive/m3-strategy/S076-首板流盘中多源行情实测]] · [[10_Reference/investing/specs/archive/m3-strategy/S077-首板流剔除层lift验证]] · [[10_Reference/investing/specs/archive/m3-strategy/S078-涨停历史snapshot数据地基]] · [[10_Reference/investing/specs/archive/m3-strategy/S079-打板P2战法与仓位闸]] · [[10_Reference/investing/specs/archive/m3-strategy/S081-打板P2战法匹配]] · [[10_Reference/investing/specs/archive/m3-strategy/S082-echarts按需引入]] · [[10_Reference/investing/specs/archive/m3-strategy/S083-工作流重构选股池分层]] · [[10_Reference/investing/specs/archive/m3-strategy/S084-选股池战法解耦]] · [[10_Reference/investing/specs/archive/m3-strategy/S085-因子全量补全与游资画像]] · [[10_Reference/investing/specs/archive/m4-三视图/S087-工作流tab按pipeline重设计]] · [[10_Reference/investing/specs/archive/m4-三视图/S088-盘前暴风雨预测]] · [[10_Reference/investing/specs/archive/m4-三视图/S089-SQLite并发性能加固与分表分库]] · [[10_Reference/investing/specs/archive/m4-三视图/S090-premarket选股前端接入与kline日更]] · [[10_Reference/investing/specs/archive/m4-三视图/S091-gstock限流容错优化]] · [[10_Reference/investing/specs/archive/m4-三视图/S092-三视图交易日锚与时段推进]] · [[10_Reference/investing/specs/archive/m4-三视图/S093-三视图内容重组与飞书通知]] · [[10_Reference/investing/specs/archive/m5-战法细化/S095-gene_scores写路径修复与日期守卫]] · [[10_Reference/investing/specs/archive/m5-战法细化/S096-P2现象判据暴露]] · [[10_Reference/investing/specs/archive/m6-合规/S098-首板流选股合规修复]] · [[10_Reference/investing/specs/S149-vibe-astock语义吸收]] · [[10_Reference/investing/specs/S150-盘中采集堵塞修复]] · [[10_Reference/investing/specs/S151-漏斗评价层]] · [[10_Reference/investing/specs/S153-量化模型验证]]

### Decision 实体

- [[10_Reference/investing/specs/DEC-001]] · [[10_Reference/investing/specs/DEC-002]] · [[10_Reference/investing/specs/DEC-003]] · [[10_Reference/investing/specs/DEC-004]] · [[10_Reference/investing/specs/DEC-005]]

## 关联项目实体（ora-2 方案 D 纳入的外部投研项目）

- H_Reference/investing/specs/Vibe-Research项目]] — Vibe-Research 个人 AI 投研看板（本图谱主体，109 spec + 16 数据源 + 12 战法）
- H_Reference/investing/specs/a-Plate-Sentinel项目]] — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架）
- H_Reference/investing/specs/TradingAgents项目]] — TradingAgents A股深度特化 fork（7 Analyst + 多 Agent 辩论）
- H_Reference/investing/specs/每日股票分析项目]] — 每日股票分析报告生成器（多市场、多渠道推送）

---

## ⚡ 快速操作

用 Templater 应用 `templates/spec` 新建 项目决策 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:f9118402d164 -->
| 项目决策总数 |
|---|
| 101 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
