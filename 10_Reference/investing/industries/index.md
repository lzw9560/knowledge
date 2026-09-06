# 行业板块 索引

> 证监会行业分类节点。对应 Pydantic 契约 `IndustrySector`。每个行业链接其成分股、相关概念、近期事件、资金流向。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "行业代码", name AS "行业名称", source AS "分类来源"
FROM "industries"
WHERE type = "industry"
SORT code ASC
```

## 关系

- has_members: [[stocks/]]（行业下成分股）
- related_to: [[concepts/]]（行业相关概念题材）
- has_events: [[events/]]（行业级事件）
- covered_by: [[reports/]]（行业研报）
- sourced_from: [[data-sources/]]（行业分类来源）

## 新建实体

用 Templater 应用 `templates/industry` 新建。模板会自动填入 YAML frontmatter（code/name/source）+ 正文骨架（行业概览/成分股/资金流向/相关概念/近期事件）。

## 实体清单（入边）

> 本段手工列出实体以建立入边链接（Dataview 表格不计入边）。

- [[industries/食品饮料]]

