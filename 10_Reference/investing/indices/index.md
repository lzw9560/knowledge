# 指数 索引

> 宽基与行业指数节点（沪深300/中证500/创业板指等）。每个指数链接其成分股、近期走势。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "指数代码", name AS "指数名称", market AS "市场"
FROM "indices"
WHERE type = "index"
SORT code ASC
```

## 关系

- has_members: [[stocks/]]（指数成分股）
- has_events: [[events/]]（指数调整/纳入剔除事件）
- sourced_from: [[data-sources/]]（指数行情来源）

## 新建实体

用 Templater 应用 `templates/index` 新建。
