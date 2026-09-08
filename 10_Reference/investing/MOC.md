
# Vibe-Research 投研知识图谱

> [!abstract] 关于本图谱
> 这个 vault 是 Vibe-Research 项目的**语义层**，把代码里的实体（Pydantic 契约模型）、spec 决策、战法、数据源链接成可导航的知识图谱。代码层管"数据怎么流"，本 vault 管"知识怎么连"——个股属于哪个行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来，都在这里通过 `[[]]` 双链和 Dataview 查询织成网。

> [!tip] 🔍 快速搜索
> 在特定类型里找内容？按 `Ctrl/Cmd + K` 打开搜索，支持按标题/正文/标签匹配。下方「热门查询」段直接展示 5 个最常用查询的结果。

---

## 📊 图谱健康摘要

> [!abstract] 实时统计——总实体数、各类型分布、最近更新、孤立节点。

<!-- dataview-precompiled:a6d4be462c4a -->
| 实体总数 |
|---|
| 2526 |
<!-- /dataview-precompiled -->

### 各类型实体计数

<!-- dataview-precompiled:e123ff43d395 -->
| 类型 | 数量 | 样本 |
|---|---|---|
| action | 6 | H_Reference/investing/actions/审批实体]], H_Reference/investing/actions/研报自动链接]], H_Reference/investing/actions/inbox晋级]], H_Reference/investing/actions/实体重命名]], H_Reference/investing/actions/源同步]], [[10_Reference/investing/templates/action]] |
<!-- /dataview-precompiled -->

<!-- dataview-precompiled:c649e86810b8 -->
| 类型 | 实体数 |
|---|---|
| action | 6 |
| agent_role | 8 |
| analyst | 397 |
| audit | 6 |
| concept | 131 |
| data_source | 18 |
| decision | 5 |
| dragon_tiger | 42 |
| event | 21 |
| inbox_item | 5 |
| index | 5 |
| industry | 127 |
| logic | 25 |
| metric | 402 |
| procedure | 1 |
| project | 4 |
| report | 393 |
| spec | 102 |
| stock | 412 |
| strategy | 14 |
| valuation | 402 |
<!-- /dataview-precompiled -->

---

## 🕐 最近更新

> [!note] 最近 7 天修改的 10 个文件——追踪图谱最新活动。侧边栏「最近更新」组件同步显示。

<!-- dataview-precompiled:f6b70dbba98f -->
| 文件 | 类型 | 修改时间 |
|---|---|---|
| — | — | — |
<!-- /dataview-precompiled -->

---

## 🔥 热门查询

> [!example] 5 个最常用的查询——直接展示结果，复制查询代码到其他笔记即可复用。

### 1. 白酒行业股票 PE 排序

<!-- dataview-precompiled:cc10cd28033f -->
| 代码 | 名称 | PE(TTM) | 市值 |
|---|---|---|---|
| 600809 | 山西汾酒 | 14.63 | 1489.58亿 |
| 000568 | 泸州老窖 | 15.55 | 1166B |
| 600519 | 贵州茅台 | 20.42 | 1.66T |
| 000858 | 五粮液 | 21.36 | 2793.91亿 |
| 000596 | 古井贡酒 | 25.91 | 411B |
| 002304 | 洋河股份 | 127.5 | 592B |
<!-- /dataview-precompiled -->

### 2. PE < 15 低估值股票

<!-- dataview-precompiled:d43427c99ade -->
| 代码 | 名称 | PE(TTM) | PB | 市值 |
|---|---|---|---|---|
| 600015 | 华夏银行 | 3.96 | 0.31 | 960.16亿 |
| 601336 | 新华保险 | 4.29 | 1.54 | 1268.99亿 |
| 601628 | 中国人寿 | 4.38 | 1.63 | 7998.32亿 |
| 601186 | 中国铁建 | 5.03 | 0.30 | 697.10亿 |
| 601166 | 兴业银行 | 5.07 | 0.46 | 3826.24亿 |
| 000001 | 平安银行 | 5.22 | 0.48 | 2267B |
| 601390 | 中国中铁 | 5.40 | 0.33 | 882.06亿 |
| 601818 | 光大银行 | 5.42 | 0.35 | 1401.49亿 |
| 600016 | 民生银行 | 5.47 | 0.27 | 1273.09亿 |
| 601169 | 北京银行 | 5.52 | 0.41 | 1156.52亿 |
| 601229 | 上海银行 | 5.54 | 0.52 | 1344.18亿 |
| 601601 | 中国太保 | 5.66 | 1.00 | 2272.55亿 |
| 601668 | 中国建筑 | 5.68 | 0.36 | 1797.44亿 |
| 000415 | 渤海租赁 | 5.74 | 0.89 | 241B |
| 600000 | 浦发银行 | 6.03 | 0.41 | 3087.45亿 |
| 601077 | 渝农商行 | 6.06 | 0.55 | 593.93亿 |
| 601838 | 成都银行 | 6.06 | 0.89 | 821.83亿 |
| 600926 | 杭州银行 | 6.09 | 0.85 | 1227.98亿 |
| 601319 | 中国人保 | 6.14 | 1.03 | 2800.77亿 |
| 600919 | 江苏银行 | 6.16 | 0.82 | 2226.02亿 |
<!-- /dataview-precompiled -->

### 3. 近期涨停池事件

<!-- dataview-precompiled:a9d6729774b8 -->
| 日期 | 类型 | 摘要 |
|---|---|---|
| 2026-09-01 | 涨停 | 2026-09-01 涨停池 83 只，连板梯队最高 7板 |
| 2026-09-01 | 炸板 | 2026-09-01 炸板池 6 只 |
| 2026-09-02 | 涨停 | 2026-09-02 涨停池 52 只，连板梯队最高 4板 |
| 2026-09-02 | 炸板 | 2026-09-02 炸板池 15 只 |
| 2026-09-03 | 涨停 | 2026-09-03 涨停池 44 只，连板梯队最高 5板 |
| 2026-09-03 | 炸板 | 2026-09-03 炸板池 33 只 |
| 2026-09-04 | 涨停 | 2026-09-04 涨停池 39 只，连板梯队最高 5板 |
| 2026-09-04 | 炸板 | 2026-09-04 炸板池 48 只 |
| 2026-09-04 | 竞价异动 | 集合竞价异动标的（楚天龙/天娱数科） |
| 2026-09-05 | 涨停 | 盘前报告提取的涨停池标的（楚天龙/远东股份/天娱数科/国芳集团/金健米业） |
<!-- /dataview-precompiled -->

### 4. 最近研报

<!-- dataview-precompiled:d8acd5fcd246 -->
| 日期 | 机构 | 分析师 | 标题 |
|---|---|---|---|
| 2026-04-26 | 国信证券 | 陈俊良,王剑 | 2025年报及2026一季报点评：收入利润增速均回正 |
| 2026-08-16 | 国信证券 | 王剑,陈俊良 | 2026年中报点评：资产质量改善 |
| 2026-08-25 | 太平洋 | 夏芈卬 | 平安银行2026年中报点评：净息差企稳，财富管理带动中收增长 |
| 2026-05-04 | 东吴证券 | 王紫敬,黄诗涛 | 2025年报&2026一季报点评：聚焦核心赛道，云数业务快速成长 |
| 2026-04-30 | 开源证券 | 刘逍遥 | 公司信息更新报告：收入快速增长，AI相关业务高质量发展 |
| 2026-09-01 | 开源证券 | 张越,刘逍遥 | 公司信息更新报告：业绩稳健增长，全域算力与Token生产能力增强 |
| 2026-08-30 | 国金证券 | 满在朋,房灵聪 | 海工景气度上行，1H26海工业绩改善 |
| 2026-09-02 | 东吴证券 | 周尔双,韦译捷 | 2026年半年报点评：Q2营收同比+15%增速稳健，海工板块订单、利润高增 |
| 2026-09-03 | 华鑫证券 | 尤少炜 | 公司动态研究报告：海工订单创历史高位、能源装备订单上行 |
| 2026-05-13 | 中邮证券 | 李帅华,魏欣 | 高纯金属镓锗铟产量大增，参股金洲精工受益PCB钻针需求爆发 |
| 2026-03-10 | 开源证券 | 蒋颖,杜致远 | 公司信息更新报告：算力业务跨越式增长，研发投入夯实长期竞争力 |
| 2026-05-05 | 国金证券 | 张真桢 | 连接+算力双轮驱动，利润筑底回升 |
| 2026-08-23 | 国金证券 | 张真桢 | 算力业务加速放量，AI布局持续深化 |
| 2026-04-27 | 中邮证券 | 吴文吉,陈天瑜 | 质效双升 |
| 2026-08-19 | 开源证券 | 吕明,陈蓉芳,马宇轩 | 公司深度报告：面板主业迎来收获期，玻璃基板业务有潜力 |
<!-- /dataview-precompiled -->

### 5. 龙虎榜游资席位

<!-- dataview-precompiled:06a27ea3322c -->
| 日期 | 股票 | 机构净额 | 席位 |
|---|---|---|---|
| 2026-09-02 | 000019 | -0.06亿 | 深股通专用 / 东方财富证券股份有限公司拉萨东环路第一证券营业部 / 财通证券股份有限公司宁波奉化大成路证券营业部 |
| 2026-09-02 | 000505 | -0.32亿 | 机构专用 / 华福证券股份有限公司广州花城大道证券营业部 / 机构专用 |
| 2026-09-04 | 000560 | 0.00亿 | 国新证券股份有限公司北京分公司 / 开源证券股份有限公司西安西大街证券营业部 / 深股通专用 |
| 2026-09-03 | 000635 | -0.25亿 | 国泰海通证券股份有限公司上海杨浦区周家嘴路证券营业部 / 东方财富证券股份有限公司拉萨江苏东路证券营业部 / 国元证券股份有限公司厦门莲岳路证券营业部 |
| 2026-08-20 | 000703 | -3.46亿 | 深股通专用 / 机构专用 / 机构专用 |
| 2026-09-04 | 000892 | -0.37亿 | 深股通专用 / 深股通专用 / 深股通专用 |
| 2026-09-04 | 000977 | -5.97亿 | 深股通专用 / 机构专用 / 中信证券股份有限公司深圳分公司 |
| 2026-08-20 | 001366 | -0.13亿 | 机构专用 / 机构专用 |
| 2026-08-27 | 002028 | -1.32亿 | 深股通专用 / 招商证券股份有限公司北京分公司 / 中信建投证券股份有限公司北京金融大街证券营业部 |
| 2026-09-02 | 002084 | -0.37亿 | 机构专用 / 中国银河证券股份有限公司北京中关村大街证券营业部 / 机构专用 |
<!-- /dataview-precompiled -->

---

## 🗂 实体类导航（本体构件 1：实体）

> 四构件本体模型蒸馏自 nano-ontoprompt。构件 1-2 为静态层，3-4 为动态层。

| 实体类 | 文件夹 | 说明 |
|---|---|---|
| 📈 股票 | [stocks/](10_Reference/investing/stocks/index) | A 股/美股/港股个股，对应 `Quote` + `CompanyInfo` |
| 🏭 行业板块 | [industries/](10_Reference/investing/industries/index) | 证监会行业分类，对应 `IndustrySector` |
| 💡 概念板块 | [concepts/](10_Reference/investing/concepts/index) | 概念题材板块，对应 `ConceptBlock` + `Sector` |
| 📊 指数 | [indices/](10_Reference/investing/indices/index) | 沪深300/中证500等宽基与行业指数 |
| 📰 研报 | [reports/](10_Reference/investing/reports/index) | 机构研报，对应 `Report` 契约 |
| 👤 分析师 | [analysts/](10_Reference/investing/analysts/index) | 研报作者，对应 `Report.researcher` |
| 💰 财务指标 | [metrics/](10_Reference/investing/metrics/index) | 营收/ROE/毛利率等，对应 `Financials` + `FinancialPeriod` |
| 📈 估值 | [valuations/](10_Reference/investing/valuations/index) | PE/PB/PEG/分位，对应 `Valuation` + `ValuationPercentile` |
| 🐉 龙虎榜 | [dragon-tiger/](10_Reference/investing/dragon-tiger/index) | 游资席位，对应 `Seat` + `BillboardDetail` + `DragonTiger` |
| ⚡ 事件 | [events/](10_Reference/investing/events/index) | 新闻/公告/涨停，对应 `News` + `Announcement` + `ZTPoolItem` |
| ⚔️ 战法 | [strategies/](10_Reference/investing/strategies/index) | 战法卡（从 `backend/strategies/cards/` 导入） |
| 📋 项目决策 | [specs/](10_Reference/investing/specs/index) | SDD spec 决策实体，对应 `specs/` 目录 |
| 📡 数据源 | [data-sources/](10_Reference/investing/data-sources/index) | 外部数据源，对应 `ARCHITECTURE` 数据流 |
| 🤖 AI 角色 | [agents/](10_Reference/investing/agents/index) | trading-agents 的 7 Analyst（区别于 analysts 真人） |


<!-- index 入边段 -->
> 各类型 index.md 入边——确保每个类型索引页至少有 1 个入边。

- [[10_Reference/investing/actions/index]]
- [[10_Reference/investing/agents/index]]
- [[10_Reference/investing/analysts/index]]
- [[10_Reference/investing/concepts/index]]
- [[10_Reference/investing/data-sources/index]]
- [[10_Reference/investing/dragon-tiger/index]]
- [[10_Reference/investing/events/index]]
- [[10_Reference/investing/indices/index]]
- [[10_Reference/investing/industries/index]]
- [[10_Reference/investing/logic/index]]
- [[10_Reference/investing/metrics/index]]
- [[10_Reference/investing/reports/index]]
- [[10_Reference/investing/specs/index]]
- [[10_Reference/investing/stocks/index]]
- [[10_Reference/investing/strategies/index]]
- [[10_Reference/investing/valuations/index]]

### 各类型实体计数（Dataview 动态）

<!-- dataview-precompiled:c649e86810b8 -->
| 类型 | 实体数 |
|---|---|
| action | 6 |
| agent_role | 8 |
| analyst | 397 |
| audit | 6 |
| concept | 131 |
| data_source | 18 |
| decision | 5 |
| dragon_tiger | 42 |
| event | 21 |
| inbox_item | 5 |
| index | 5 |
| industry | 127 |
| logic | 25 |
| metric | 402 |
| procedure | 1 |
| project | 4 |
| report | 393 |
| spec | 102 |
| stock | 412 |
| strategy | 14 |
| valuation | 402 |
<!-- /dataview-precompiled -->

---

## 🔗 关系层（本体构件 2：关系）

关系通过 `[[]]` 双向链接 + frontmatter 谓词标注实现。预定义关系谓词：
`belongs_to` / `tagged` / `covered_by` / `has_metric` / `valued_at` / `involves` / `affects` / `matches` / `authored_by` / `triggered_by`

## ⚙️ 动态层（本体构件 3-4）

| 构件 | 文件夹 | 说明 |
|---|---|---|
| **⚙️ 逻辑规则** | [logic/](10_Reference/investing/logic/index) | schema 约束/校验/状态机/推断规则 |
| **⚡ 动作** | [actions/](10_Reference/investing/actions/index) | CRUD/状态流转/链接维护/审计快照 |

## 🛡 质量门（Curated）

| 层 | 文件夹 | 作用 |
|---|---|---|
| **📥 待审** | [inbox/](10_Reference/investing/inbox/index) | LLM 抽取实体先进此，带 confidence + source + quality_score，审核通过才进正式区 |
| **🔍 审查** | [reviews/](10_Reference/investing/reviews/index) | ReAct Agent 定期体检报告（8 项检查） |

> 不直接灌入是知识图谱健康的第一道防线。详见 [[10_Reference/investing/inbox/index]] 质量四维度。

### ⚔️ 战法卡统计

<!-- dataview-precompiled:9a939da0f746 -->
| 战法 | edge 家族 | 详情 |
|---|---|---|
| N字反击 | 动量溢价 | H_Reference/investing/strategies/N字反击]] |
| 一字竞价选股法 | 动量溢价 | [[10_Reference/investing/strategies/一字竞价选股法]] |
| 低吸龙头 | 均值回归 | H_Reference/investing/strategies/低吸龙头]] |
| 反包战法 | 事件溢价 | H_Reference/investing/strategies/反包战法]] |
| 尾盘偷袭 | 动量溢价 | H_Reference/investing/strategies/尾盘偷袭]] |
| 平台突破 | 形态突破 | H_Reference/investing/strategies/平台突破]] |
| 弱转强接力 | 事件溢价 | H_Reference/investing/strategies/弱转强接力]] |
| 形态反包 | 形态突破 | H_Reference/investing/strategies/形态反包]] |
| 暴风雨逆势涨停 | 事件溢价 | H_Reference/investing/strategies/暴风雨逆势涨停]] |
| 炸板回封 | 事件溢价 | H_Reference/investing/strategies/炸板回封]] |
| 连板接力 | 动量溢价 | H_Reference/investing/strategies/连板接力]] |
| 首板挖掘 | 动量溢价 | H_Reference/investing/strategies/首板挖掘]] |
| 龙头战法 | 龙头追踪 | H_Reference/investing/strategies/龙头战法]] |
<!-- /dataview-precompiled -->

### 📋 项目决策统计

<!-- dataview-precompiled:e42015199fcb -->
| 编号 | 标题 | 状态 | 详情 |
|---|---|---|---|
| S001 | 修复 chat._get_env_llm_config 缺失 → /api/chat 500 | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S001-fix-chat-env-llm-config]] |
| S002 | 打板工作流重构 · P1 候选池诊断统一 | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S002-打板工作流重构]] |
| S003 | 后端 API 冒烟测试缺陷修复批次 | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S003-api-bugfix-batch]] |
| S004 | 候选池漏斗 run_funnel 性能优化 | 草案 | [[10_Reference/investing/specs/S004-candidates-funnel-performance]] |
| S005 | 中长线价值选股漏斗（与短线 S002 并列） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S005-中长线价值选股漏斗]] |
| S006 | 系统重写纲领（渐进式长分支） | 草案 | [[10_Reference/investing/specs/S006-系统重写纲领]] |
| S007 | 契约层（数据模型+回归基线+契约测试骨架） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]] |
| S008 | 后端数据层迁移（astock/gstock/market→模型） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移]] |
| S009 | 前后端类型同步（openapi-codegen） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]] |
| S010 | AI 工具注册表 + SYSTEM_PROMPT 新边界 | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S010-工具注册表与SYSTEM_PROMPT]] |
| S011 | 调度收口（删 scheduler.py+重写 scheduled_tasks+状态机接线） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口]] |
| S012 | 工作流标灰（realtime/post 桩+pre 清理） | 草案 | [[10_Reference/investing/specs/S012-工作流标灰]] |
| S013 | 前端数据层（统一 client+TanStack Query+懒加载+apiKey 代理） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S013-前端数据层]] |
| S014 | 前端 UI 重设计（信息架构+交互统一+视觉+AI 对话） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计]] |
| S015 | 配置与基础设施（config 拆分+infra 收口+路由自动发现） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S015-配置与基础设施]] |
| S016 | 测试网（后端覆盖率+IO 录制回放+前端 vitest+CI） | 草案 | [[10_Reference/investing/specs/S016-测试网]] |
| S017 | A股涨跌预测模型栈（四头解耦） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S017-A股涨跌预测模型栈]] |
| S018 | 多源特征工程（预测模型特征供给） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S018-多源特征工程]] |
| S019 | 宏观特征 Fred API 接入（macro.py 第二批） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S019-macro-Fred-API]] |
| S020 | worldmonitor 决策因子接入（全球宏观/地缘/另类数据） | 已实现 | [[10_Reference/investing/specs/archive/m0-foundation/S020-worldmonitor决策因子接入]] |
| S022 | 熔断器 health 读路径修复（尊重 recovery_timeout） | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S022-熔断器health读路径修复]] |
| S023 | 漏斗可用性与因子解耦（P1 打磨：盘前简报接因子+候选详情依据链+漏斗每层可观测可调参+真实数据不静默返空） | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S023-漏斗可用性与因子解耦]] |
| S024 | 拓扑展示（关系网+漏斗流程+连板梯队树，EdgeProvider 扩展位） | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S024-拓扑展示]] |
| S025 | 补前端入口 | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S025-补前端入口]] |
| S026 | pre-market 异步化 | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S026-pre-market-async]] |
| S028 | limitup-screener 修复（文案三态/trigger/因子层 conditions） | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S028-limitup-screener-fix]] |
| S029 | GeneScreener 接通（阈值可配+执行检索+多层明细） | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S029-gene-screener-wireup]] |
| S030 | 盘前简报多层化 + UX 收敛 | 已废弃 | [[10_Reference/investing/specs/archive/m1-workflow/S030-pre-market-multilayer]] |
| S031 | 调度收口 + 盘前简报多层 + 交互式战法 + 按战法回测 | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S031-调度收口盘前多层按战法回测]] |
| S032 | 调度收口第二轮（S011b）：主循环收口 + portfolio 日志重试 + 状态机接线落库 | 已实现 | [[10_Reference/investing/specs/archive/m1-workflow/S032-调度收口第二轮]] |
<!-- /dataview-precompiled -->

---

## 📖 使用说明

### 1. 新建实体（Templater）

1. 在 Obsidian 中安装 **Templater** 插件并启用。
2. 设置 → Templater → Template folder location 填 `templates`。
3. 在任意实体文件夹下新建笔记 → 命令面板 `Ctrl/Cmd+P` → `Templater: Create new note from template` → 选对应模板（如 `stock`）。
4. 模板会自动填入 YAML frontmatter + 正文骨架，`<% tp.date.now("YYYY-MM-DD") %>` 自动替换为当日日期。

### 2. 链接（`[[]]` 双链）

- 在任意笔记正文中输入 `[[10_Reference/investing/stocks/600519]]` 即可链接到个股笔记；若笔记不存在，Obsidian 会高亮提示并支持一键创建。
- **双向**：在股票笔记里写 `[[10_Reference/investing/industries/食品饮料]]`，行业笔记的"反向链接"区会自动出现该股票。
- 文件夹链接用 `[[10_Reference/investing/stocks/index|stocks/]]` 形式，Obsidian 会指向该文件夹的 `index.md`。

### 3. 查询（Dataview）

- 安装 **Dataview** 插件后，所有 `index.md` 里的 ```dataview 代码块会动态渲染。
- 查询语法：`TABLE 字段 FROM "文件夹" WHERE 条件 SORT 字段`。
- 示例——查所有 PE < 15 的股票：

<!-- dataview-precompiled:06cd9327e597 -->
| 文件 | 代码 | 名称 | PE(TTM) | PB |
|---|---|---|---|---|
| [[10_Reference/investing/stocks/600371]] | 600371 | 万向德农 | -727.72 | 7.71 |
| [[10_Reference/investing/stocks/003040]] | 003040 | 楚天龙 | -640.55 | 7.03 |
| [[10_Reference/investing/stocks/688167]] | 688167 | 炬光科技 | -506.06 | 17.96 |
| [[10_Reference/investing/stocks/600127]] | 600127 | 金健米业 | -451.85 | 11.93 |
| [[10_Reference/investing/stocks/002104]] | 002104 | 恒宝股份 | -444.18 | 4.78 |
| [[10_Reference/investing/stocks/002354]] | 002354 | 天娱数科 | -440.37 | 8.1 |
| [[10_Reference/investing/stocks/600698]] | 600698 | 湖南天雁 | -277.77 | 11.41 |
| [[10_Reference/investing/stocks/000009]] | 000009 | 中国宝安 | -258.73 | 1.87 |
| [[10_Reference/investing/stocks/002714]] | 002714 | 牧原股份 | -225.29 | 3.19 |
| [[10_Reference/investing/stocks/600048]] | 600048 | 保利发展 | -195.72 | 0.32 |
| [[10_Reference/investing/stocks/002564]] | 002564 | 天沃科技 | -195.11 | 38.74 |
| [[10_Reference/investing/stocks/603122]] | 603122 | 合富中国 | -159.67 | 5.20 |
| [[10_Reference/investing/stocks/603533]] | 603533 | 掌阅科技 | -158.51 | 4.63 |
| [[10_Reference/investing/stocks/000039]] | 000039 | 中集集团 | -157.11 | 1.09 |
| [[10_Reference/investing/stocks/600540]] | 600540 | 新赛股份 | -149.48 | 7.59 |
| [[10_Reference/investing/stocks/000560]] | 000560 | 我爱我家 | -136.80 | 0.79 |
| [[10_Reference/investing/stocks/688521]] | 688521 | 芯原股份 | -118.76 | 33.29 |
| [[10_Reference/investing/stocks/600865]] | 600865 | 百大集团 | -116.92 | 1.86 |
| [[10_Reference/investing/stocks/688047]] | 688047 | 龙芯中科 | -104.87 | 17.56 |
| [[10_Reference/investing/stocks/003005]] | 003005 | 竞业达 | -91.36 | 2.45 |
| [[10_Reference/investing/stocks/002909]] | 002909 | 集泰股份 | -84.97 | 3.28 |
| [[10_Reference/investing/stocks/000661]] | 000661 | 长春高新 | -84.36 | 1.33 |
| [[10_Reference/investing/stocks/000592]] | 000592 | 平潭发展 | -73.25 | 8.49 |
| [[10_Reference/investing/stocks/002702]] | 002702 | 海欣食品 | -72.53 | 3.09 |
| [[10_Reference/investing/stocks/000032]] | 000032 | 深桑达A | -71.79 | 2.36 |
| [[10_Reference/investing/stocks/600029]] | 600029 | 南方航空 | -69.79 | 3.03 |
| [[10_Reference/investing/stocks/600611]] | 600611 | 大众交通 | -68.87 | 1.25 |
| [[10_Reference/investing/stocks/688506]] | 688506 | 百利天恒 | -66.07 | 22.54 |
| [[10_Reference/investing/stocks/688141]] | 688141 | 杰华特 | -57.30 | 49.52 |
| [[10_Reference/investing/stocks/002868]] | 002868 | 绿康生化 | -54.71 | 56.58 |
| [[10_Reference/investing/stocks/601111]] | 601111 | 中国国航 | -53.18 | 2.00 |
| [[10_Reference/investing/stocks/300498]] | 300498 | 温氏股份 | -39.60 | 2.91 |
| [[10_Reference/investing/stocks/688126]] | 688126 | 沪硅产业 | -36.05 | 3.92 |
| [[10_Reference/investing/stocks/002084]] | 002084 | 海鸥住工 | -34.75 | 3.61 |
| [[10_Reference/investing/stocks/600115]] | 600115 | 中国东航 | -32.38 | 7.72 |
| [[10_Reference/investing/stocks/600892]] | 600892 | 大晟文化 | -31.84 | -201.94 |
| [[10_Reference/investing/stocks/603123]] | 603123 | 翠微股份 | -25.51 | 5.63 |
| [[10_Reference/investing/stocks/000428]] | 000428 | 华天酒店 | -22.05 | 3.90 |
| [[10_Reference/investing/stocks/000050]] | 000050 | 深天马A | -21.04 | 0.61 |
| [[10_Reference/investing/stocks/600828]] | 600828 | 茂业商业 | -18.36 | 1.31 |
| [[10_Reference/investing/stocks/002059]] | 002059 | 云南旅游 | -15.43 | 6.03 |
| [[10_Reference/investing/stocks/000892]] | 000892 | 欢瑞世纪 | -14.08 | 10.85 |
| [[10_Reference/investing/stocks/001330]] | 001330 | 博纳影业 | -13.73 | 2.14 |
| [[10_Reference/investing/stocks/002855]] | 002855 | 捷荣技术 | -13.35 | 23.90 |
| [[10_Reference/investing/stocks/002403]] | 002403 | 爱仕达 | -12.27 | 2.93 |
| [[10_Reference/investing/stocks/601012]] | 601012 | 隆基绿能 | -11.89 | 1.86 |
| [[10_Reference/investing/stocks/600802]] | 600802 | 福建水泥 | -11.01 | 2.85 |
| [[10_Reference/investing/stocks/600121]] | 600121 | 郑州煤电 | -5.98 | 10.37 |
| [[10_Reference/investing/stocks/688223]] | 688223 | 晶科能源 | -5.89 | 1.78 |
| [[10_Reference/investing/stocks/600438]] | 600438 | 通威股份 | -5.37 | 1.62 |
| [[10_Reference/investing/stocks/000635]] | 000635 | 英 力 特 | -4.70 | 3.08 |
| [[10_Reference/investing/stocks/600657]] | 600657 | 信达地产 | -1.81 | 0.68 |
| [[10_Reference/investing/stocks/002124]] | 002124 | 天邦食品 | -1.68 | 6.53 |
| [[10_Reference/investing/stocks/000002]] | 000002 | 万科A | -0.41 | 0.37 |
| [[10_Reference/investing/stocks/600015]] | 600015 | 华夏银行 | 3.96 | 0.31 |
| [[10_Reference/investing/stocks/601336]] | 601336 | 新华保险 | 4.29 | 1.54 |
| [[10_Reference/investing/stocks/601628]] | 601628 | 中国人寿 | 4.38 | 1.63 |
| [[10_Reference/investing/stocks/601186]] | 601186 | 中国铁建 | 5.03 | 0.30 |
| [[10_Reference/investing/stocks/601166]] | 601166 | 兴业银行 | 5.07 | 0.46 |
| [[10_Reference/investing/indices/000001]] | 000001 | 平安银行 | 5.22 | 0.48 |
| [[10_Reference/investing/stocks/601390]] | 601390 | 中国中铁 | 5.40 | 0.33 |
| [[10_Reference/investing/stocks/601818]] | 601818 | 光大银行 | 5.42 | 0.35 |
| [[10_Reference/investing/stocks/600016]] | 600016 | 民生银行 | 5.47 | 0.27 |
| [[10_Reference/investing/stocks/601169]] | 601169 | 北京银行 | 5.52 | 0.41 |
| [[10_Reference/investing/stocks/601229]] | 601229 | 上海银行 | 5.54 | 0.52 |
| [[10_Reference/investing/stocks/601601]] | 601601 | 中国太保 | 5.66 | 1.00 |
| [[10_Reference/investing/stocks/601668]] | 601668 | 中国建筑 | 5.68 | 0.36 |
| [[10_Reference/investing/stocks/000415]] | 000415 | 渤海租赁 | 5.74 | 0.89 |
| [[10_Reference/investing/stocks/600000]] | 600000 | 浦发银行 | 6.03 | 0.41 |
| [[10_Reference/investing/stocks/601077]] | 601077 | 渝农商行 | 6.06 | 0.55 |
| [[10_Reference/investing/stocks/601838]] | 601838 | 成都银行 | 6.06 | 0.89 |
| [[10_Reference/investing/stocks/600926]] | 600926 | 杭州银行 | 6.09 | 0.85 |
| [[10_Reference/investing/stocks/601319]] | 601319 | 中国人保 | 6.14 | 1.03 |
| [[10_Reference/investing/stocks/600919]] | 600919 | 江苏银行 | 6.16 | 0.82 |
| [[10_Reference/investing/stocks/601916]] | 601916 | 浙商银行 | 6.17 | 0.44 |
| [[10_Reference/investing/stocks/601009]] | 601009 | 南京银行 | 6.39 | 0.76 |
| [[10_Reference/investing/stocks/601318]] | 601318 | 中国平安 | 6.41 | 0.99 |
| [[10_Reference/investing/stocks/601328]] | 601328 | 交通银行 | 6.64 | 0.55 |
| [[10_Reference/investing/stocks/601998]] | 601998 | 中信银行 | 6.74 | 0.65 |
| [[10_Reference/investing/stocks/600036]] | 600036 | 招商银行 | 6.84 | 0.91 |
| [[10_Reference/investing/stocks/601117]] | 601117 | 中国化学 | 6.89 | 0.64 |
| [[10_Reference/investing/stocks/000623]] | 000623 | 吉林敖东 | 6.9 | 0.68 |
| [[10_Reference/investing/stocks/601825]] | 601825 | 沪农商行 | 6.90 | 0.64 |
| [[10_Reference/investing/stocks/600741]] | 600741 | 华域汽车 | 6.98 | 0.73 |
| [[10_Reference/investing/stocks/002142]] | 002142 | 宁波银行 | 7.18 | 0.94 |
| [[10_Reference/investing/stocks/601658]] | 601658 | 邮储银行 | 7.19 | 0.62 |
| [[10_Reference/investing/stocks/601398]] | 601398 | 工商银行 | 7.59 | 0.72 |
| [[10_Reference/investing/stocks/601800]] | 601800 | 中国交建 | 7.73 | 0.33 |
| [[10_Reference/investing/stocks/000651]] | 000651 | 格力电器 | 7.81 | 1.47 |
| [[10_Reference/investing/stocks/601288]] | 601288 | 农业银行 | 8.01 | 0.84 |
| [[10_Reference/investing/stocks/601939]] | 601939 | 建设银行 | 8.10 | 0.78 |
| [[10_Reference/investing/stocks/601988]] | 601988 | 中国银行 | 8.33 | 0.75 |
| [[10_Reference/investing/stocks/000807]] | 000807 | 云铝股份 | 8.45 | 2.43 |
| [[10_Reference/investing/stocks/601688]] | 601688 | 华泰证券 | 8.53 | 0.98 |
| [[10_Reference/investing/stocks/002532]] | 002532 | 天山铝业 | 8.64 | 1.86 |
| [[10_Reference/investing/stocks/600999]] | 600999 | 招商证券 | 8.86 | 1.25 |
| [[10_Reference/investing/stocks/600018]] | 600018 | 上港集团 | 8.98 | 0.86 |
| [[10_Reference/investing/stocks/000776]] | 000776 | 广发证券 | 9.05 | 1.24 |
| [[10_Reference/investing/stocks/002736]] | 002736 | 国信证券 | 9.11 | 1.07 |
| [[10_Reference/investing/stocks/600011]] | 600011 | 华能国际 | 9.11 | 1.66 |
| [[10_Reference/investing/stocks/601919]] | 601919 | 中远海控 | 9.18 | 1.05 |
| [[10_Reference/investing/stocks/601600]] | 601600 | 中国铝业 | 9.34 | 1.93 |
| [[10_Reference/investing/stocks/601669]] | 601669 | 中国电建 | 9.49 | 0.55 |
| [[10_Reference/investing/stocks/601211]] | 601211 | 国泰海通 | 9.53 | 0.93 |
| [[10_Reference/investing/stocks/601881]] | 601881 | 中国银河 | 9.71 | 1.11 |
| [[10_Reference/investing/stocks/600233]] | 600233 | 圆通速递 | 10.10 | 1.54 |
| [[10_Reference/investing/stocks/002648]] | 002648 | 卫星化学 | 10.35 | 2.39 |
| [[10_Reference/investing/stocks/000166]] | 000166 | 申万宏源 | 10.36 | 0.99 |
| [[10_Reference/investing/stocks/000598]] | 000598 | 兴蓉环境 | 10.39 | 1.06 |
| [[10_Reference/investing/stocks/603799]] | 603799 | 华友钴业 | 10.40 | 1.41 |
| [[10_Reference/investing/stocks/601898]] | 601898 | 中煤能源 | 10.41 | 1.15 |
| [[10_Reference/investing/stocks/600039]] | 600039 | 四川路桥 | 10.47 | 1.58 |
| [[10_Reference/investing/stocks/600027]] | 600027 | 华电国际 | 10.53 | 1.12 |
| [[10_Reference/investing/stocks/601877]] | 601877 | 正泰电器 | 10.90 | 1.20 |
| [[10_Reference/investing/stocks/600030]] | 600030 | 中信证券 | 10.91 | 1.46 |
| [[10_Reference/investing/stocks/600061]] | 600061 | 国投资本 | 10.94 | 0.77 |
| [[10_Reference/investing/stocks/000708]] | 000708 | 中信特钢 | 11.05 | 1.54 |
| [[10_Reference/investing/stocks/600938]] | 600938 | 中国海油 | 11.20 | 1.81 |
| [[10_Reference/investing/stocks/600989]] | 600989 | 宝丰能源 | 11.21 | 3.30 |
| [[10_Reference/investing/stocks/600690]] | 600690 | 海尔智家 | 11.24 | 1.68 |
| [[10_Reference/investing/stocks/000528]] | 000528 | 柳工 | 11.29 | 0.87 |
| [[10_Reference/investing/stocks/000703]] | 000703 | 恒逸石化 | 11.34 | 2.26 |
| [[10_Reference/investing/stocks/002001]] | 002001 | 新和成 | 11.34 | 2.33 |
| [[10_Reference/investing/stocks/601857]] | 601857 | 中国石油 | 11.34 | 1.22 |
| [[10_Reference/investing/stocks/600066]] | 600066 | 宇通客车 | 11.40 | 4.82 |
| [[10_Reference/investing/stocks/600346]] | 600346 | 恒力石化 | 11.53 | 1.80 |
| [[10_Reference/investing/stocks/000792]] | 000792 | 盐湖股份 | 11.55 | 2.92 |
| [[10_Reference/investing/stocks/600958]] | 600958 | 东方证券 | 11.66 | 0.96 |
| [[10_Reference/investing/stocks/600023]] | 600023 | 浙能电力 | 11.76 | 0.88 |
| [[10_Reference/investing/stocks/601995]] | 601995 | 中金公司 | 11.81 | 1.55 |
| [[10_Reference/investing/stocks/601225]] | 601225 | 陕西煤业 | 12.08 | 2.44 |
| [[10_Reference/investing/stocks/601901]] | 601901 | 方正证券 | 12.43 | 1.07 |
| [[10_Reference/investing/stocks/601058]] | 601058 | 赛轮轮胎 | 12.46 | 2.12 |
| [[10_Reference/investing/stocks/000999]] | 000999 | 华润三九 | 12.47 | 1.79 |
| [[10_Reference/investing/stocks/600019]] | 600019 | 宝钢股份 | 12.48 | 0.61 |
| [[10_Reference/investing/stocks/601766]] | 601766 | 中国中车 | 12.74 | 1.00 |
| [[10_Reference/investing/stocks/301308]] | 301308 | 江波龙 | 12.79 | 6.89 |
| [[10_Reference/investing/stocks/601607]] | 601607 | 上海医药 | 12.79 | 0.78 |
| [[10_Reference/investing/stocks/600219]] | 600219 | 南山铝业 | 12.81 | 1.12 |
| [[10_Reference/investing/stocks/000027]] | 000027 | 深圳能源 | 12.96 | 0.89 |
| [[10_Reference/investing/stocks/600104]] | 600104 | 上汽集团 | 13.02 | 0.40 |
| [[10_Reference/investing/stocks/601899]] | 601899 | 紫金矿业 | 13.11 | 4.65 |
| [[10_Reference/investing/stocks/601018]] | 601018 | 宁波港 | 13.13 | 0.82 |
| [[10_Reference/investing/stocks/600551]] | 600551 | 时代出版 | 13.55 | 0.91 |
| [[10_Reference/investing/stocks/600426]] | 600426 | 华鲁恒升 | 13.62 | 1.60 |
| [[10_Reference/investing/stocks/600362]] | 600362 | 江西铜业 | 13.64 | 1.80 |
| [[10_Reference/investing/stocks/000157]] | 000157 | 中联重科 | 13.69 | 1.0 |
| [[10_Reference/investing/stocks/600803]] | 600803 | 新奥股份 | 13.69 | 2.55 |
| [[10_Reference/investing/stocks/000963]] | 000963 | 华东医药 | 13.74 | 1.87 |
| [[10_Reference/investing/stocks/002074]] | 002074 | 国轩高科 | 13.83 | 1.57 |
| [[10_Reference/investing/stocks/601377]] | 601377 | 兴业证券 | 13.84 | 0.90 |
| [[10_Reference/investing/stocks/001965]] | 001965 | 招商公路 | 13.96 | 0.96 |
| [[10_Reference/investing/stocks/601872]] | 601872 | 招商轮船 | 13.98 | 3.24 |
| [[10_Reference/investing/stocks/002236]] | 002236 | 大华股份 | 14.12 | 1.36 |
| [[10_Reference/investing/stocks/603993]] | 603993 | 洛阳钼业 | 14.14 | 4.39 |
| [[10_Reference/investing/stocks/000513]] | 000513 | 丽珠集团 | 14.32 | 1.79 |
| [[10_Reference/investing/stocks/600309]] | 600309 | 万华化学 | 14.54 | 2.11 |
| [[10_Reference/investing/stocks/600795]] | 600795 | 国电电力 | 14.54 | 1.57 |
| [[10_Reference/investing/stocks/600809]] | 600809 | 山西汾酒 | 14.63 | 3.91 |
| [[10_Reference/investing/stocks/688009]] | 688009 | 中国通号 | 14.72 | 1.11 |
| [[10_Reference/investing/stocks/000333]] | 000333 | 美的集团 | 14.8 | 3.1 |
| [[10_Reference/investing/stocks/601878]] | 601878 | 浙商证券 | 14.80 | 1.15 |
| [[10_Reference/investing/stocks/000019]] | 000019 | 深粮控股 | — | — |
| [[10_Reference/investing/stocks/000505]] | 000505 | 京粮控股 | — | — |
| [[10_Reference/investing/stocks/002172]] | 002172 | 省广集团 | — | — |
| [[10_Reference/investing/stocks/002696]] | 002696 | 郑州银行 | — | — |
| [[10_Reference/investing/stocks/600313]] | 600313 | 农发种业 | — | — |
| [[10_Reference/investing/stocks/600693]] | 600693 | 东百集团 | — | — |
| [[10_Reference/investing/stocks/603118]] | 603118 | 共进股份 | — | — |
| [[10_Reference/investing/stocks/603221]] | 603221 | 梦网科技 | — | — |
| [[10_Reference/investing/stocks/603626]] | 603626 | 科森科技 | — | — |
| [[10_Reference/investing/stocks/605188]] | 605188 | 国邦医药 | — | — |
<!-- /dataview-precompiled -->

### 4. 图谱视图

左侧栏图标 → Graph View（快捷键 `Ctrl/Cmd+G`），可看到所有实体的双链网络。建议按 `type` 字段染色区分股票/行业/研报/战法。

## 🔍 分析工具

> 知识图谱深度分析层——图算法/时间线/因果链，从"实体+关系"两层扩展到可计算的图结构。

- **图算法分析**：`scripts/graph_analysis.py` → `docs/graph-analysis-report.md`
  - 社区发现（LPA 标签传播）/ 入度中心性（hub 节点）/ 桥节点（跨社区连接者）/ BFS 最短路径
- **时间线视图**：`scripts/timeline_view.py` → `docs/timeline-report.md`
  - 按 frontmatter date 字段排列所有事件实体，按月分组
- **因果链规则**：[[10_Reference/investing/logic/因果链]] — 因果（→）vs 相关（↔）vs 待验证（?>）标注规范

---

## 🏗 与项目代码的关系

| 层 | 位置 | 职责 |
|---|---|---|
| 代码契约层 | `backend/models/` | Pydantic 模型定义数据结构（Quote/Valuation/Financials…） |
| 数据流层 | `backend/` + `ARCHITECTURE.md` | 数据采集/加工/存储管线 |
| 战法执行层 | `backend/strategies/` | 战法 match 逻辑 + cards/ 战法卡 |
| **语义层（本 vault）** | `knowledge/` | 实体关系导航、研报笔记、投研知识沉淀 |
| 决策记录层 | `specs/` | SDD spec 决策文档 |

本 vault 不复制代码逻辑，只做**知识表征**：一个股票笔记链接它的行业、研报、财务、估值、龙虎榜、相关战法，形成可回溯的投研上下文。代码改了模型字段，来这里改对应模板的 frontmatter 即可。

---

## 🔗 关联子区

- H_Reference/market_sentiment/情绪仪表盘]] — 市场情绪追踪（每日 pre/mid/post 报告 + z-score 温度）
- 战法卡有"适用天气：阴天"，market_sentiment 有温度 Z 值——但定义"阴天 = 哪个 Z 区间"的逻辑待建（见 [[10_Reference/investing/logic/战法天气映射]]）

### 关联项目（ora-2 方案 D 纳入的外部投研项目）

- H_Reference/investing/specs/a-Plate-Sentinel项目]] — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架阶段）
- H_Reference/investing/specs/TradingAgents项目]] — TradingAgents A股深度特化 fork（7 Analyst + 多 Agent 辩论）
- H_Reference/investing/specs/每日股票分析项目]] — 每日股票分析报告生成器（多市场、多渠道推送）

关联项目使用的数据源：
- H_Reference/investing/data-sources/Tushare]]（a-Plate-Sentinel 专用，积分制）
- H_Reference/investing/data-sources/AkShare]] / H_Reference/investing/data-sources/baostock（K线日更）]] / [[10_Reference/investing/data-sources/mootdx]]（与 Vibe-Research 共用）

## 🌐 跨领域链接（ora-3 §4）

> 投研方法论与其他知识域的"同构"链接。判据（H_Reference/investing/logic/跨域门控]]，待建）：
> 跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

### 已建链接

- H_Reference/investing/strategies/龙头战法]] §方法论链接 — 「板块轮动识别龙头」↔ 时间序列状态识别（🚧 待建）
- H_Reference/meta/四构件本体方法论]] — 四构件本体方法论（领域无关模板）

### 待建领域

- **技术学习领域**（智驾/时序模型/世界模型）：与投研的同构点见 ora-3 §4.2 表（时序模型↔情绪温度 ΔZ / 世界模型↔反事实推演 / 端到端 vs 模块化↔规则+LLM 兜底 / 多传感器融合↔6 层 z-score+三重护栏 / corner case↔熔断机制）
- **元知识层**：[[10_Reference/meta/index]] — 通用方法论（PARA/MOC/四构件本体）

> 跨域链接数 / 单域链接数 < 20%（防"什么都记但什么都不深"）。当前投研子区跨域链接 = 0，远未到风险，待跨域实体落地后监控。
