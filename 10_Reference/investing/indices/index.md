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

## 实体清单（入边）

> 本段手工列出实体以建立入边链接（Dataview 表格不计入边）。

- [[indices/000001]]

- [[indices/000300]]

- [[indices/000905]]

- [[indices/399001]]

- [[indices/399006]]

---

## ⚡ 快速操作

用 Templater 应用 `templates/index` 新建 指数 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "指数总数"
FROM "10_Reference/investing/indices"
WHERE type = "index" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
