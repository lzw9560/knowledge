# 数据源 索引

> 外部数据源节点。对应 `ARCHITECTURE.md` 数据流。16 数据源（2026-09-06 从 ARCHITECTURE.md 批量灌入）。每条记录链接其提供字段、限流策略、降级链、相关实体。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  name AS "名称", layer AS "层级", rate_limit AS "限流", fallback AS "降级", provides AS "提供字段"
FROM "10_Reference/investing/data-sources"
WHERE type = "data_source" AND file.name != "index"
SORT layer ASC, name ASC
LIMIT 50
```

## 关系

- supplies: [[stocks/]] / [[reports/]] / [[metrics/]] / [[valuations/]] / [[dragon-tiger/]] / [[events/]]（数据源供给的实体）
- defined_in: [[specs/]]（数据源接入的 spec）

## 层级说明

| layer | 说明 | 典型 |
|---|---|---|
| L1 实时 | 实时行情，秒级 | 行情推送 |
| L2 延时 | 延时行情，分钟级 | K 线/分时 |
| L3 离线 | 日级/批处理 | 财务/估值/龙虎榜 |

## 新建实体

用 Templater 应用 `templates/data-source` 新建。

> 2026-09-06 已从 `ARCHITECTURE.md` 批量灌入 16 个数据源（规则脚本，非 LLM）。ARCHITECTURE.md 未明示的字段标"待补"。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[data-sources/akshare]]
- [[data-sources/baidu-stock]]
- [[data-sources/baostock]]
- [[data-sources/cninfo]]
- [[data-sources/eastmoney-datacenter]]
- [[data-sources/eastmoney-push2]]
- [[data-sources/eastmoney-push2ex]]
- [[data-sources/eastmoney-reportapi]]
- [[data-sources/eastmoney-searchapi]]
- [[data-sources/fred]]
- [[data-sources/hithink-ths]]
- [[data-sources/mootdx]]
- [[data-sources/rss-newsradar]]
- [[data-sources/sina-financial]]
- [[data-sources/tencent]]
- [[data-sources/tushare]]
- [[data-sources/worldmonitor]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/data-source` 新建 数据源 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "数据源总数"
FROM "10_Reference/investing/data-sources"
WHERE type = "data_source" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
