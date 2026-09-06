# 数据源 索引

> 外部数据源节点。对应 `ARCHITECTURE.md` 数据流。15+ 数据源。每条记录链接其提供字段、限流策略、降级链、相关实体。

## 实体列表（Dataview 动态）

```dataview
TABLE name AS "名称", layer AS "层级", rate_limit AS "限流", fallback AS "降级"
FROM "data-sources"
WHERE type = "data_source"
SORT name ASC
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

> 注：阶段 0 不自动导入数据源清单。阶段 1 计划从 `ARCHITECTURE.md` 批量导入。
