# 事件 索引

> 新闻/公告/涨停/异动事件节点。对应 Pydantic 契约 `News` + `Announcement` + `ZTPoolItem`。每条记录链接其影响标的、触发战法、来源。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:42839f8087b2 -->
| 日期 | 类型 | 摘要 | 来源 |
|---|---|---|---|
| 2026-09-01 | 涨停 | 2026-09-01 涨停池 83 只，连板梯队最高 7板 | astock.em_zt_topic_pool |
| 2026-09-01 | 炸板 | 2026-09-01 炸板池 6 只 | astock.em_zt_topic_pool |
| 2026-09-02 | 涨停 | 2026-09-02 涨停池 52 只，连板梯队最高 4板 | astock.em_zt_topic_pool |
| 2026-09-02 | 炸板 | 2026-09-02 炸板池 15 只 | astock.em_zt_topic_pool |
| 2026-09-03 | 涨停 | 2026-09-03 涨停池 44 只，连板梯队最高 5板 | astock.em_zt_topic_pool |
| 2026-09-03 | 炸板 | 2026-09-03 炸板池 33 只 | astock.em_zt_topic_pool |
| 2026-09-04 | 涨停 | 2026-09-04 涨停池 39 只，连板梯队最高 5板 | astock.em_zt_topic_pool |
| 2026-09-04 | 炸板 | 2026-09-04 炸板池 48 只 | astock.em_zt_topic_pool |
| 2026-09-04 | 竞价异动 | 集合竞价异动标的（楚天龙/天娱数科） | market_sentiment/daily/2026-09-04_竞价异动.md |
| 2026-09-05 | 涨停 | 盘前报告提取的涨停池标的（楚天龙/远东股份/天娱数科/国芳集团/金健米业） | daily/2026-09-05_pre_盘前情绪报告.md |
| 2026-09-07 | 异动 | 2026-09-07 盘中异动 21 只（高换手/连板/多次炸板） | astock.em_zt_topic_pool |
| 2026-09-07 | 涨停 | 2026-09-07 涨停池 67 只，连板梯队最高 6板 | astock.em_zt_topic_pool |
| 2026-09-07 | 炸板 | 2026-09-07 炸板池 17 只 | astock.em_zt_topic_pool |
| 2026-09-08 | 个股异动 | 中天科技中报净利润预增50%-60%（23.52-25.08亿元），AI算力+光通信景气验证，回购200万股均价29.75元，中标FY27集采15.18亿元 | web_search/公司公告 |
| 2026-09-08 | 个股异动 | 华天科技并购重组推进中，发行股份购买资产报告书注册稿发布，深交所并购重组审核委员会会议安排通知已收到 | web_search/公司公告 |
| 2026-09-08 | 衍生品异动 | 沪深300股指期货基差贴水-0.35%，突破-0.3%阈值，大资金做空对冲信号，短期回调概率>70% | sentiment_engine/alert_monitor |
| 2026-09-08 | 持仓追踪 | 9月8日盘中持仓追踪：5只票全部V型反弹后再次回落，光迅翻绿-0.98%，中天最强+1.41%，通信设备板块资金流出-69亿 | hithink-finance/market_snapshot |
| 2026-09-08 | 地缘政治 | 美伊冲突升级，霍尔木兹海峡航运受阻，布伦特原油$97.34，WTI$92.63，今年涨幅近60%，高盛上调油价预期，供应受阻或持续至2027年Q1 | web_search/reuters |
| 2026-09-08 | 个股异动 | 通富微电中报归母净利润17.17亿元同比+316.77%，定增落地募集净额42.09亿元，股东户数大增60%至56.1万户 | web_search/公司公告 |
| 2026-09-08 | 个股异动 | 长电科技65亿定增获批，拟增发不超5.368亿股，投向高性能计算高端先进封装平台扩产等4个项目，总投资95.7亿元 | web_search/公司公告 |
<!-- /dataview-precompiled -->

## 关系

- affects: [[10_Reference/investing/stocks/index|stocks/]]（事件影响标的）
- triggers: [[10_Reference/investing/strategies/index|strategies/]]（事件触发战法，如涨停池触发首板/连板/炸板回封）
- pairs_with: [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]（涨停事件与龙虎榜配对）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（新闻/公告/涨停池数据来源）

## 事件类型说明

| event_type | 说明 | 对应 Pydantic 契约 |
|---|---|---|
| 新闻 | 财经新闻 | `News` |
| 公告 | 公司公告 | `Announcement` |
| 涨停 | 涨停池 | `ZTPoolItem` |
| 跌停 | 跌停池 | （派生） |
| 停牌 | 停牌 | （派生） |
| 复牌 | 复牌 | （派生） |

## 新建实体

用 Templater 应用 `templates/event` 新建。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/events/2026-09-01-涨停池]]
- [[10_Reference/investing/events/2026-09-01-炸板池]]
- [[10_Reference/investing/events/2026-09-02-涨停池]]
- [[10_Reference/investing/events/2026-09-02-炸板池]]
- [[10_Reference/investing/events/2026-09-03-涨停池]]
- [[10_Reference/investing/events/2026-09-03-炸板池]]
- [[10_Reference/investing/events/2026-09-04-涨停池]]
- [[10_Reference/investing/events/2026-09-04-炸板池]]
- [[10_Reference/investing/events/2026-09-04-竞价异动]]
- [[10_Reference/investing/events/2026-09-05-涨停池]]
- [[10_Reference/investing/events/2026-09-07-异动]]
- [[10_Reference/investing/events/2026-09-07-涨停池]]
- [[10_Reference/investing/events/2026-09-07-炸板池]]
- [[10_Reference/investing/events/2026-09-08-美伊冲突升级]]
- [[10_Reference/investing/events/2026-09-08-基差异动]]
- [[10_Reference/investing/events/2026-09-08-持仓追踪]]
- [[10_Reference/investing/events/2026-09-08-长电科技定增]]
- [[10_Reference/investing/events/2026-09-08-通富微电中报定增]]
- [[10_Reference/investing/events/2026-09-08-华天科技并购重组]]
- [[10_Reference/investing/events/2026-09-08-中天科技中报回购]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/event` 新建 事件 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:8c4f4903438f -->
| 事件总数 |
|---|
| 20 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
