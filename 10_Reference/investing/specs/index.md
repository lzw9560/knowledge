# 项目决策 索引

> SDD spec 决策实体节点。对应 `specs/` 目录下的 spec 文档。每条记录链接其问题/目标、需求、受影响文件、验收标准、关联决策。

## Spec 实体列表（Dataview 动态）

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "spec"
SORT number ASC
```

## Decision 实体列表（Dataview 动态）

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "decision"
SORT number ASC
```

## 关系

- defines: [[strategies/]]（spec 定义战法 match 逻辑）
- references: [[data-sources/]]（spec 引用数据源）
- depends_on: [[specs/]]（spec 间依赖/栈式关系）

## 新建实体

用 Templater 应用 `templates/spec` 新建。

## 已灌入 spec（2026-09-07 第二批扩充）

> 第一批 13 spec + 5 decision（2026-09-06）。第二批补入断链修复所需的 17 spec stub（2026-09-07）。详见源 `specs/README.md`（S001-S166 全量索引）与 `specs/decision-log.md`（DEC-001~005）。

### 已实现 / 关键架构 spec（第一批 13）

- [[specs/S007-契约层]] · [[specs/S008-后端数据层迁移]] · [[specs/S010-工具注册表与SYSTEM_PROMPT]] · [[specs/S011-调度收口]] · [[specs/S017-A股涨跌预测模型栈]] · [[specs/S018-多源特征工程]] · [[specs/S019-macro-Fred-API]] · [[specs/S020-worldmonitor决策因子接入]] · [[specs/S031-调度收口盘前多层按战法回测]] · [[specs/S047-基因分权重回测校准]] · [[specs/S066-策略特定漏斗架构重构]] · [[specs/S094-战法分类与双pipeline重构]] · [[specs/S100-战法卡片对齐]]

### 断链修复 stub（第二批 17，从 README 索引灌入摘要）

- [[specs/S004-candidates-funnel-performance]] · [[specs/S006-系统重写纲领]] · [[specs/S009-前后端类型同步]] · [[specs/S013-前端数据层]] · [[specs/S015-配置与基础设施]] · [[specs/S023-漏斗可用性与因子解耦]] · [[specs/S030-pre-market-multilayer]] · [[specs/S032-调度收口第二轮]] · [[specs/S041-回测定时任务与趋势看板]] · [[specs/S042-统一持仓建议引擎]] · [[specs/S049-盘前简报漏斗重构与诊断修正]] · [[specs/S064-盯盘教练MVP]] · [[specs/S075-首板流]] · [[specs/S086-涨停战法pipeline统一架构]] · [[specs/S097-逐条件因子过滤]] · [[specs/S101-飞书多点通知]] · [[specs/S102-战法卡片历史战绩]]

### 第三批 spec stub（fix-17/18 灌入，2026-09-07）

> 以下 stub 由源仓 spec 批量抽取生成，正文为摘要级，待按需深化。列入此段以建立入边，消除孤立。

- [[specs/S001-fix-chat-env-llm-config]] · [[specs/S002-打板工作流重构]] · [[specs/S003-api-bugfix-batch]] · [[specs/S005-中长线价值选股漏斗]] · [[specs/S012-工作流标灰]] · [[specs/S014-前端UI重设计]] · [[specs/S016-测试网]] · [[specs/S022-熔断器health读路径修复]] · [[specs/S024-拓扑展示]] · [[specs/S025-补前端入口]] · [[specs/S026-pre-market-async]] · [[specs/S028-limitup-screener-fix]] · [[specs/S029-gene-screener-wireup]] · [[specs/S033-状态机前端呈现]] · [[specs/S034-结算接线]] · [[specs/S035-ai-proxy-删除]] · [[specs/S036-工作流标灰]] · [[specs/S037-gene-db-迁移]] · [[specs/S038-持仓市价自动结算]] · [[specs/S039-StockDeep接线]] · [[specs/S040-历史数据回填90天]] · [[specs/S043-次日溢价率单因子分析]] · [[specs/S044-候选池漏斗数据源补全]] · [[specs/S045-漏斗层得分排序筛选]] · [[specs/S046-fallback空写防护]] · [[specs/S048-工作流打磨]] · [[specs/S050-W0-行动闭环]] · [[specs/S051-基因筛选体验批]] · [[specs/S052-回测快照回填与缺口补跑]] · [[specs/S053-炸板后溢价因子修复]] · [[specs/S054-W0-工作流闭环呈现]] · [[specs/S055-盘中封单时序采集与炸板预警]] · [[specs/S056-天气熔断三铁律补全]] · [[specs/S057-漏斗八项标准硬约束封顶]] · [[specs/S058-战法双层卡片层与天气适配过滤]] · [[specs/S059-因子IC评估]] · [[specs/S060-明日验证条件对账卡]] · [[specs/S061-预测跟踪与自动验证]] · [[specs/S062-战法卡内容填充-反包与龙头]] · [[specs/S063-情绪管线贯通与盘中辅助决策]] · [[specs/S065-weather-history持久化]] · [[specs/S067-advisory-perf]] · [[specs/S068-工作流触发与结算正确性]] · [[specs/S069-每日forward_test管道]] · [[specs/S070-intraday采集管道]] · [[specs/S071-盘前选股谨慎部署]] · [[specs/S072-涨停叉pipeline诚实可观测]] · [[specs/S074-market_phase统一判定]] · [[specs/S076-首板流盘中多源行情实测]] · [[specs/S077-首板流剔除层lift验证]] · [[specs/S078-涨停历史snapshot数据地基]] · [[specs/S079-打板P2战法与仓位闸]] · [[specs/S081-打板P2战法匹配]] · [[specs/S082-echarts按需引入]] · [[specs/S083-工作流重构选股池分层]] · [[specs/S084-选股池战法解耦]] · [[specs/S085-因子全量补全与游资画像]] · [[specs/S087-工作流tab按pipeline重设计]] · [[specs/S088-盘前暴风雨预测]] · [[specs/S089-SQLite并发性能加固与分表分库]] · [[specs/S090-premarket选股前端接入与kline日更]] · [[specs/S091-gstock限流容错优化]] · [[specs/S092-三视图交易日锚与时段推进]] · [[specs/S093-三视图内容重组与飞书通知]] · [[specs/S095-gene_scores写路径修复与日期守卫]] · [[specs/S096-P2现象判据暴露]] · [[specs/S098-首板流选股合规修复]] · [[specs/S149-vibe-astock语义吸收]] · [[specs/S150-盘中采集堵塞修复]] · [[specs/S151-漏斗评价层]] · [[specs/S153-量化模型验证]]

### Decision 实体

- [[specs/DEC-001]] · [[specs/DEC-002]] · [[specs/DEC-003]] · [[specs/DEC-004]] · [[specs/DEC-005]]

## 关联项目实体（ora-2 方案 D 纳入的外部投研项目）

- [[specs/a-plate-sentinel-project]] — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架）
- [[specs/trading-agents-project]] — TradingAgents A股深度特化 fork（7 Analyst + 多 Agent 辩论）
- [[specs/daily-stock-analysis-project]] — 每日股票分析报告生成器（多市场、多渠道推送）
