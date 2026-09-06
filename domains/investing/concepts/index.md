# 概念板块 索引

> 概念题材板块节点。对应 Pydantic 契约 `ConceptBlock` + `Sector`。每个概念链接其成分股、题材轮动节奏、相关研报、近期事件。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "概念代码", name AS "概念名称", related_industry AS "关联行业"
FROM "concepts"
WHERE type = "concept"
SORT name ASC
```

## 关系

- has_members: [[stocks/]]（概念下成分股）
- related_to: [[industries/]]（概念关联的行业）
- has_events: [[events/]]（概念级催化事件）
- covered_by: [[reports/]]（概念研报）
- triggers_strategies: [[strategies/]]（题材轮动触发的战法，如龙头战法）

## 新建实体

用 Templater 应用 `templates/concept` 新建。模板侧重题材轮动节奏记录。
