# 事件 索引

> 新闻/公告/涨停/异动事件节点。对应 Pydantic 契约 `News` + `Announcement` + `ZTPoolItem`。每条记录链接其影响标的、触发战法、来源。

## 实体列表（Dataview 动态）

```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要", source AS "来源"
FROM "events"
WHERE type = "event"
SORT date DESC
```

## 关系

- affects: [[stocks/]]（事件影响标的）
- triggers: [[strategies/]]（事件触发战法，如涨停池触发首板/连板/炸板回封）
- pairs_with: [[dragon-tiger/]]（涨停事件与龙虎榜配对）
- sourced_from: [[data-sources/]]（新闻/公告/涨停池数据来源）

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

> 本段手工列出实体以建立入边链接（Dataview 表格不计入边）。

- [[events/2026-09-04-竞价异动]]

- [[events/2026-09-05-涨停池]]

