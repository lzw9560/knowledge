---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 数据源 索引

> 外部数据源节点。对应 `ARCHITECTURE.md` 数据流。16 数据源（2026-09-06 从 ARCHITECTURE.md 批量灌入）。每条记录链接其提供字段、限流策略、降级链、相关实体。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:5198ef84b75b -->
| 名称 | 层级 | 限流 | 降级 | 提供字段 |
|---|---|---|---|---|
| 腾讯行情 | 1 | 不封IP | 底座层，无降级 | 现价, 涨跌, PE, PB, 市值, 换手, 涨跌停 |
| 东财 datacenter（龙虎榜/解禁/融资融券等） | 2 | em_get 限流 QPS≤2 | 熔断器+push2delay降级 | 龙虎榜, 解禁, 融资融券, 大宗交易, 股东户数, 分红, 资金流, 行业排名 |
| 东财 push2 | 2 | em_get 限流 QPS≤2（1.0s+抖动0.1~0.5s） | 熔断器+push2delay降级 | 行情, K线, 分时 |
| 东财 push2ex（涨停四池） | 2 | em_get 限流 QPS≤2 | 熔断器+push2delay降级 | 涨停四池, 连板梯队, 封板率, 炸板率, 晋级率 |
| 东财 reportapi（研报） | 2 | em_get 限流 QPS≤2 | 熔断器+push2delay降级 | 研报标题, 机构, 评级, 日期, 一致预期EPS |
| 东财 searchapi（个股新闻） | 2 | em_get 限流 QPS≤2 | 熔断器+push2delay降级 | 个股新闻标题, 时间, 来源 |
| akshare | 3 | 无（惰性导入） | DependencyMissing 优雅报错 | legu行业资金流, 行业资金流, 财报三表 |
| mootdx | 3 | 无（惰性导入） | DependencyMissing 优雅报错 | K线, 财报原始快照 |
| Tushare | 3 | 积分制（免费 5000 积分，高级需付费） | 无 | A股行情, 财务, 指数, 期货, 基金, 可转债 |
| 百度股市通（日K线） | 4 | 不封IP | 无 | 日K线 |
| baostock（K线日更） | 4 | 无 | S090 kline_refresh | K线日更, 5minK线 |
| 巨潮 cninfo（互动易） | 4 | requests 直连 | 无 | 公告, 互动易问答 |
| 同花顺 THS（一致预期/涨停揭秘） | 4 | 直连 | 无 | 一致预期, 涨停揭秘 |
| 新浪财经（财报三表） | 4 | urllib 直连 | 无 | 资产负债表, 利润表, 现金流量表 |
| FRED（宏观） | 5 | API key 隔离 | 无 | 宏观指标 |
| worldmonitor（全球宏观 MCP） | 5 | 无 | 无 | 全球宏观指标 |
| 108 RSS 源（资讯雷达） | 资讯层 | 40线程并发 | 单源失败不拖垮整体 | 资讯, 12赛道分类, 合规过滤 |
<!-- /dataview-precompiled -->

## 关系

- supplies: [[10_Reference/investing/stocks/index|stocks/]] / [[10_Reference/investing/reports/index|reports/]] / [[10_Reference/investing/metrics/index|metrics/]] / [[10_Reference/investing/valuations/index|valuations/]] / [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]] / [[10_Reference/investing/events/index|events/]]（数据源供给的实体）
- defined_in: [[10_Reference/investing/specs/index|specs/]]（数据源接入的 spec）

## 层级说明

| layer | 说明 | 典型 |
|---|---|---|
| L1 实时 | 实时行情，秒级 | 行情推送 |
| L2 延时 | 延时行情，分钟级 | K 线/分时 |
| L3 离线 | 日级/批处理 | 财务/估值/龙虎榜 |

## 新建实体

用 Templater 应用 `templates/data-source` 新建。

> 2026-09-06 已从 `ARCHITECTURE.md` 批量灌入 16 个数据源（规则脚本，非 LLM）。字段已从源码提取并填充。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- 10_Reference/investing/data-sources/AkShare]]
- 10_Reference/investing/data-sources/百度股市通（日K线）]]
- 10_Reference/investing/data-sources/baostock（K线日更）]]
- 10_Reference/investing/data-sources/巨潮 cninfo（互动易）]]
- 10_Reference/investing/data-sources/东财 datacenter（龙虎榜·解禁·融资融券等）]]
- 10_Reference/investing/data-sources/东财 push2]]
- 10_Reference/investing/data-sources/东财 push2ex（涨停四池）]]
- 10_Reference/investing/data-sources/东财 reportapi（研报）]]
- 10_Reference/investing/data-sources/东财 searchapi（个股新闻）]]
- 10_Reference/investing/data-sources/FRED（宏观）]]
- 10_Reference/investing/data-sources/同花顺 THS（一致预期·涨停揭秘）]]
- [[10_Reference/investing/data-sources/mootdx]]
- 10_Reference/investing/data-sources/108 RSS 源（资讯雷达）]]
- 10_Reference/investing/data-sources/新浪财经（财报三表）]]
- 10_Reference/investing/data-sources/腾讯行情]]
- 10_Reference/investing/data-sources/Tushare]]
- 10_Reference/investing/data-sources/worldmonitor（全球宏观 MCP）]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/data-source` 新建 数据源 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:f97614620104 -->
| 数据源总数 |
|---|
| 17 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
