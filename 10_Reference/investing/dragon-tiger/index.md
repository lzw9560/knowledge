# 龙虎榜 索引

> 游资席位与机构买卖明细节点。对应 Pydantic 契约 `Seat` + `BillboardDetail` + `DragonTiger`。每条记录链接其所属股票、席位明细、游资画像、相关事件。

## 实体列表（Dataview 动态）

```dataview
TABLE date AS "日期", code AS "股票代码", institution_net AS "机构净额(亿)", seats AS "席位"
FROM "dragon-tiger"
WHERE type = "dragon_tiger"
SORT date DESC, code ASC
```

## 关系

- belongs_to: [[stocks/]]（每条龙虎榜记录所属股票）
- relates_to: [[events/]]（龙虎榜上榜当日的涨停/异动事件）
- triggers: [[strategies/]]（游资席位数据是反包战法等加分项）
- sourced_from: [[data-sources/]]（龙虎榜数据来源，如东方财富）

## 新建实体

用 Templater 应用 `templates/dragon-tiger` 新建。

## 实体清单（入边）

> 本段手工列出实体以建立入边链接（Dataview 表格不计入边）。

- [[dragon-tiger/2026-09-05]]

