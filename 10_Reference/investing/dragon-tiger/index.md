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
- [[dragon-tiger/600108-2026-09-04]]
- [[dragon-tiger/001366-2026-08-20]]
- [[dragon-tiger/600865-2026-09-04]]
- [[dragon-tiger/603083-2026-08-14]]
- [[dragon-tiger/603696-2026-08-14]]
- [[dragon-tiger/605577-2026-09-03]]
- [[dragon-tiger/601086-2026-09-04]]
- [[dragon-tiger/603118-2026-08-24]]
- [[dragon-tiger/600354-2026-09-04]]
- [[dragon-tiger/603626-2026-08-21]]
- [[dragon-tiger/002156-2026-08-17]]

---

## ⚡ 快速操作

用 Templater 应用 `templates/dragon-tiger` 新建 龙虎榜 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "龙虎榜总数"
FROM "10_Reference/investing/dragon-tiger"
WHERE type = "dragon_tiger" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
