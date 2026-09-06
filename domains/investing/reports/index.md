# 研报 索引

> 机构研报节点。对应 Pydantic 契约 `Report`。每份研报链接其覆盖标的、分析师、核心观点、评级与目标价。

## 实体列表（Dataview 动态）

```dataview
TABLE title AS "标题", org AS "机构", researcher AS "分析师", publish_date AS "日期", rating_change AS "评级", target_price AS "目标价"
FROM "reports"
WHERE type = "report"
SORT publish_date DESC
```

## 关系

- covers: [[stocks/]]（研报覆盖的个股）
- authored_by: [[analysts/]]（研报作者）
- references: [[metrics/]] / [[valuations/]]（引用的财务/估值数据）
- sourced_from: [[data-sources/]]（研报数据来源）

## 新建实体

用 Templater 应用 `templates/report` 新建。模板 frontmatter 对应 `Report` Pydantic 字段（title/org/researcher/publish_date/report_type/rating_change/target_price/eps_forecast）。
