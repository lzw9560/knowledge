# 概念板块 索引

> 概念题材板块节点。对应 Pydantic 契约 `ConceptBlock` + `Sector`。每个概念链接其成分股、题材轮动节奏、相关研报、近期事件。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  code AS "概念代码", name AS "概念名称", related_industry AS "关联行业"
FROM "10_Reference/investing/concepts"
WHERE type = "concept" AND file.name != "index"
SORT name ASC
LIMIT 50
```

## 关系

- has_members: [[stocks/]]（概念下成分股）
- related_to: [[industries/]]（概念关联的行业）
- has_events: [[events/]]（概念级催化事件）
- covered_by: [[reports/]]（概念研报）
- triggers_strategies: [[strategies/]]（题材轮动触发的战法，如龙头战法）

## 新建实体

用 Templater 应用 `templates/concept` 新建。模板侧重题材轮动节奏记录。

---

## ⚡ 快速操作

用 Templater 应用 `templates/concept` 新建 概念板块 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "概念板块总数"
FROM "10_Reference/investing/concepts"
WHERE type = "concept" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
