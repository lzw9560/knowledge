---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 386
critical: 12
high: 193
medium: 193
low: 43
status: 已完成
created: 2026-09-08
---

# 每日审查报告：2026-09-08

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2490 |
| stub 实体 | 43 |
| LLM 生成内容 | 524 |
| 断链 | 193 |
| 孤立实体 | 193 |
| confidence 覆盖 | 2449/2490 (98%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| stock | 411 | metric | 401 |
| valuation | 401 | analyst | 396 |
| report | 392 | concept | 130 |
| industry | 126 | spec | 101 |
| dragon_tiger | 41 | logic | 24 |
| data_source | 17 | event | 13 |
| strategy | 12 | agent_role | 7 |
| index | 5 | decision | 5 |
| project | 4 | action | 4 |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| 10_Reference/tech-learning/concepts/graceful-degradation | 22 |
| 10_Reference/tech-learning/concepts/caching-strategy | 21 |
| 10_Reference/tech-learning/concepts/data-contract | 20 |
| 10_Reference/reading/notes/均值回归-笔记 | 16 |
| 10_Reference/reading/notes/趋势跟踪-笔记 | 14 |
| 10_Reference/tech-learning/architecture/layered-architecture | 12 |
| 10_Reference/tech-learning/concepts/circuit-breaker | 11 |
| 10_Reference/tech-learning/concepts/rate-limiting | 11 |
| 10_Reference/reading/notes/道氏理论-笔记 | 11 |
| 10_Reference/reading/notes/周期定位-笔记 | 11 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| actions | ['actions/auto-link-report'] |
| concepts | ['concepts/白酒'] |
| data-sources | ['data-sources/sina-financial', 'data-sources/eastmoney-searchapi', 'data-sources/eastmoney-reportapi', 'data-sources/mootdx', 'data-sources/cninfo', 'data-sources/tushare', 'data-sources/eastmoney-push2ex', 'data-sources/baidu-stock'] |
| dragon-tiger | ['dragon-tiger/603118-2026-08-24', 'dragon-tiger/600127-2026-09-04', 'dragon-tiger/000892-2026-09-04', 'dragon-tiger/600892-2026-09-04', 'dragon-tiger/601086-2026-09-04', 'dragon-tiger/002084-2026-09-02', 'dragon-tiger/603083-2026-08-14', 'dragon-tiger/605577-2026-09-03', 'dragon-tiger/000635-2026-09-03', 'dragon-tiger/002104-2026-09-04', 'dragon-tiger/002172-2026-08-27', 'dragon-tiger/605188-2026-09-01', 'dragon-tiger/002028-2026-08-27', 'dragon-tiger/600313-2026-08-20', 'dragon-tiger/002202-2026-08-11', 'dragon-tiger/002696-2026-09-02', 'dragon-tiger/603533-2026-09-01', 'dragon-tiger/603696-2026-08-14', 'dragon-tiger/600108-2026-09-04', 'dragon-tiger/000560-2026-09-04', 'dragon-tiger/002855-2026-09-03', 'dragon-tiger/000019-2026-09-02', 'dragon-tiger/003005-2026-09-04', 'dragon-tiger/603626-2026-08-21', 'dragon-tiger/600865-2026-09-04', 'dragon-tiger/600693-2026-09-04', 'dragon-tiger/600371-2026-09-02', 'dragon-tiger/2026-09-05', 'dragon-tiger/600354-2026-09-04', 'dragon-tiger/603721-2026-09-01', 'dragon-tiger/002679-2026-09-02', 'dragon-tiger/000977-2026-09-04', 'dragon-tiger/603221-2026-09-03', 'dragon-tiger/000505-2026-09-02', 'dragon-tiger/600828-2026-09-04', 'dragon-tiger/002156-2026-08-17', 'dragon-tiger/600551-2026-09-01', 'dragon-tiger/001366-2026-08-20', 'dragon-tiger/600540-2026-09-04', 'dragon-tiger/000703-2026-08-20', 'dragon-tiger/300413-2026-09-01'] |
| events | ['events/2026-09-02-涨停池', 'events/2026-09-04-竞价异动', 'events/2026-09-03-炸板池', 'events/2026-09-02-炸板池', 'events/2026-09-03-涨停池', 'events/2026-09-01-炸板池', 'events/2026-09-07-炸板池', 'events/2026-09-07-涨停池', 'events/2026-09-01-涨停池', 'events/2026-09-04-涨停池', 'events/2026-09-07-异动', 'events/2026-09-05-涨停池', 'events/2026-09-04-炸板池'] |
| indices | ['indices/399006', 'indices/399001', 'indices/000001'] |
| industries | ['industries/待核实', 'industries/保健护理产品', 'industries/网络媒体', 'industries/电力设备', 'industries/其他非银行金融'] |
| logic | ['logic/entity-merge', 'logic/relation-cardinality', 'logic/source-drift', 'logic/报告图谱关联', 'logic/cross-domain-gate', 'logic/data-freshness', 'logic/stub-lifecycle', 'logic/coverage-floor', 'logic/causal-chains', 'logic/orphan-threshold'] |
| reports | ['reports/000166-2020-03-30-机构及交易业务良性发展，业绩实现较快增长', 'reports/000001-2026-08-25-平安银行2026年中报点评：净息差企稳，', 'reports/000157-2026-08-28-汇兑扰动利润端，新兴板块高增长', 'reports/000039-2026-08-30-海工景气度上行，1H26海工业绩改善', 'reports/000063-2026-05-05-连接+算力双轮驱动，利润筑底回升', 'reports/000032-2024-09-01-2024半年报点评：经营质量持续改善，云', 'reports/000050-2021-08-26-突破上半年行业重压，扎实成长落地有声', 'reports/000166-2019-09-02-低基数下业绩大增，H股发行增强资本实力', 'reports/000062-2021-08-26-公司信息更新报告：产业互联网平台进入高增', 'reports/000062-2021-07-06-公司首次覆盖报告：电子产业互联网平台蓄势', 'reports/000021-2023-11-23-深度报告：EMS龙头再出发，存储封测打开', 'reports/000155-2026-08-28-锂矿放量驱动业绩高增，风光扩容打开中长期', 'reports/000021-2021-08-26-沛顿项目顺利推进，Q2业绩主要受消费电子', 'reports/000034-2026-04-30-公司信息更新报告：收入快速增长，AI相关', 'reports/000034-2026-09-01-公司信息更新报告：业绩稳健增长，全域算力', 'reports/000301-2026-04-30-2025年年报&2026年一季报点评：地', 'reports/000100-2026-09-01-公司信息更新报告：归母净利润翻倍增长，A', 'reports/000001-2026-08-16-2026年中报点评：资产质量改善', 'reports/000050-2023-11-30-3Q23归母净利润环比减亏，手机面板价格', 'reports/000027-2022-08-29-2022年半年报点评：煤电毛利率大幅改善', 'reports/000002-2025-04-30-短期压力犹存，持续融资及盘活存量', 'reports/000039-2026-09-03-公司动态研究报告：海工订单创历史高位、能', 'reports/000301-2026-09-03-2026年半年报点评：地缘冲突推升炼化景', 'reports/000088-2025-11-06-2025年三季报点评：引战中远加强港航协', 'reports/000157-2026-08-31-2026年中报点评：汇率波动导致盈利能力', 'reports/000155-2026-04-20-区域优质新能源发电运营商，锂矿达产+算电', 'reports/000060-2025-04-20-2024年归母净利同增57%，矿端加速增', 'reports/000027-2023-04-24-年度点评报告：收入增长超预期，绿色能源转', 'reports/000032-2025-04-28-2024年报和2025一季报点评：聚焦自', 'reports/000002-2025-08-27-公司信息更新报告：业绩继续承压，关注后续', 'reports/000063-2026-03-10-公司信息更新报告：算力业务跨越式增长，研', 'reports/000060-2026-05-13-高纯金属镓锗铟产量大增，参股金洲精工受益', 'reports/000100-2026-08-19-公司深度报告：面板主业迎来收获期，玻璃基'] |
| specs | ['specs/archive/m1-workflow/S034-结算接线', 'specs/DEC-005', 'specs/S151-漏斗评价层', 'specs/archive/m3-strategy/S072-涨停叉pipeline诚实可观测', 'specs/archive/m3-strategy/S082-echarts按需引入', 'specs/archive/m1-workflow/S039-StockDeep接线', 'specs/S012-工作流标灰', 'specs/archive/m1-workflow/S029-gene-screener-wireup', 'specs/archive/m1-workflow/S033-状态机前端呈现', 'specs/archive/m1-workflow/S028-limitup-screener-fix', 'specs/S153-量化模型验证', 'specs/archive/m2-closed-loop/S061-预测跟踪与自动验证', 'specs/S150-盘中采集堵塞修复', 'specs/archive/m2-closed-loop/S055-盘中封单时序采集与炸板预警', 'specs/archive/m5-战法细化/S096-P2现象判据暴露', 'specs/archive/m4-三视图/S088-盘前暴风雨预测', 'specs/archive/m3-strategy/S067-advisory-perf', 'specs/archive/m1-workflow/S040-历史数据回填90天', 'specs/archive/m1-workflow/S036-工作流标灰', 'specs/archive/m2-closed-loop/S062-战法卡内容填充-反包与龙头', 'specs/archive/m3-strategy/S083-工作流重构选股池分层', 'specs/archive/m2-closed-loop/S059-因子IC评估', 'specs/archive/m4-三视图/S091-gstock限流容错优化', 'specs/archive/m6-合规/S098-首板流选股合规修复', 'specs/archive/m2-closed-loop/S063-情绪管线贯通与盘中辅助决策', 'specs/archive/m1-workflow/S035-ai-proxy-删除', 'specs/archive/m3-strategy/S068-工作流触发与结算正确性', 'specs/archive/m0-foundation/S003-api-bugfix-batch', 'specs/archive/m2-closed-loop/S065-weather-history持久化', 'specs/archive/m4-三视图/S093-三视图内容重组与飞书通知', 'specs/archive/m1-workflow/S024-拓扑展示', 'specs/archive/m0-foundation/S014-前端UI重设计', 'specs/archive/m3-strategy/S079-打板P2战法与仓位闸', 'specs/archive/m2-closed-loop/S056-天气熔断三铁律补全', 'specs/archive/m3-strategy/S085-因子全量补全与游资画像', 'specs/archive/m3-strategy/S084-选股池战法解耦', 'specs/archive/m3-strategy/S074-market_phase统一判定', 'specs/archive/m3-strategy/S071-盘前选股谨慎部署', 'specs/S149-vibe-astock语义吸收', 'specs/S016-测试网', 'specs/archive/m1-workflow/S037-gene-db-迁移', 'specs/archive/m3-strategy/S078-涨停历史snapshot数据地基', 'specs/archive/m3-strategy/S070-intraday采集管道', 'specs/archive/m1-workflow/S048-工作流打磨', 'specs/archive/m2-closed-loop/S052-回测快照回填与缺口补跑', 'specs/vibe-research-project', 'specs/archive/m2-closed-loop/S054-W0-工作流闭环呈现', 'specs/archive/m3-strategy/S069-每日forward_test管道', 'specs/archive/m3-strategy/S077-首板流剔除层lift验证', 'specs/archive/m1-workflow/S045-漏斗层得分排序筛选', 'specs/archive/m0-foundation/S002-打板工作流重构', 'specs/archive/m4-三视图/S089-SQLite并发性能加固与分表分库', 'specs/archive/m4-三视图/S090-premarket选股前端接入与kline日更', 'specs/archive/m2-closed-loop/S058-战法双层卡片层与天气适配过滤', 'specs/DEC-004', 'specs/archive/m4-三视图/S092-三视图交易日锚与时段推进', 'specs/archive/m1-workflow/S046-fallback空写防护', 'specs/archive/m0-foundation/S001-fix-chat-env-llm-config', 'specs/archive/m1-workflow/S026-pre-market-async', 'specs/archive/m3-strategy/S081-打板P2战法匹配', 'specs/archive/m2-closed-loop/S057-漏斗八项标准硬约束封顶', 'specs/archive/m0-foundation/S010-工具注册表与SYSTEM_PROMPT', 'specs/archive/m3-strategy/S076-首板流盘中多源行情实测', 'specs/archive/m2-closed-loop/S060-明日验证条件对账卡', 'specs/archive/m4-三视图/S087-工作流tab按pipeline重设计', 'specs/a-plate-sentinel-project', 'specs/archive/m0-foundation/S005-中长线价值选股漏斗', 'specs/archive/m2-closed-loop/S050-W0-行动闭环', 'specs/archive/m5-战法细化/S095-gene_scores写路径修复与日期守卫', 'specs/archive/m1-workflow/S022-熔断器health读路径修复', 'specs/archive/m1-workflow/S043-次日溢价率单因子分析', 'specs/archive/m1-workflow/S025-补前端入口', 'specs/archive/m2-closed-loop/S053-炸板后溢价因子修复', 'specs/archive/m1-workflow/S044-候选池漏斗数据源补全', 'specs/archive/m2-closed-loop/S051-基因筛选体验批', 'specs/archive/m1-workflow/S038-持仓市价自动结算'] |
| stocks | ['stocks/600611', 'stocks/605580'] |

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 1422 |
| medium | 1027 |
| (未标注) | 41 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 193 | ≤50 | 🔴 |
| 孤立实体 | 193 | ≤200 | 🟢 |
| stub 实体 | 43 | ≤100 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |

## 📈 趋势

> 与上次审查对比（如有 reviews/ 前一份报告）

待填充（需要读前一份报告对比）
