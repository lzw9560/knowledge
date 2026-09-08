# 龙虎榜 索引

> 游资席位与机构买卖明细节点。对应 Pydantic 契约 `Seat` + `BillboardDetail` + `DragonTiger`。每条记录链接其所属股票、席位明细、游资画像、相关事件。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  date AS "日期", code AS "股票代码", institution_net AS "机构净额(亿)", seats AS "席位"
FROM "10_Reference/investing/dragon-tiger"
WHERE type = "dragon_tiger" AND file.name != "index"
SORT date DESC, code ASC
LIMIT 50
```

## 关系

- belongs_to: [[10_Reference/investing/stocks/index|stocks/]]（每条龙虎榜记录所属股票）
- relates_to: [[10_Reference/investing/events/index|events/]]（龙虎榜上榜当日的涨停/异动事件）
- triggers: [[10_Reference/investing/strategies/index|strategies/]]（游资席位数据是反包战法等加分项）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（龙虎榜数据来源，如东方财富）

## 新建实体

用 Templater 应用 `templates/dragon-tiger` 新建。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/dragon-tiger/000019-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/000505-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/000560-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/000635-2026-09-03]]
- [[10_Reference/investing/dragon-tiger/000703-2026-08-20]]
- [[10_Reference/investing/dragon-tiger/000892-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/000977-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/001366-2026-08-20]]
- [[10_Reference/investing/dragon-tiger/002028-2026-08-27]]
- [[10_Reference/investing/dragon-tiger/002084-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/002104-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/002156-2026-08-17]]
- [[10_Reference/investing/dragon-tiger/002172-2026-08-27]]
- [[10_Reference/investing/dragon-tiger/002202-2026-08-11]]
- [[10_Reference/investing/dragon-tiger/002679-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/002696-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/002855-2026-09-03]]
- [[10_Reference/investing/dragon-tiger/003005-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/2026-09-05]]
- [[10_Reference/investing/dragon-tiger/300413-2026-09-01]]
- [[10_Reference/investing/dragon-tiger/600108-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600127-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600313-2026-08-20]]
- [[10_Reference/investing/dragon-tiger/600354-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600371-2026-09-02]]
- [[10_Reference/investing/dragon-tiger/600540-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600551-2026-09-01]]
- [[10_Reference/investing/dragon-tiger/600693-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600828-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600865-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/600892-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/601086-2026-09-04]]
- [[10_Reference/investing/dragon-tiger/603083-2026-08-14]]
- [[10_Reference/investing/dragon-tiger/603118-2026-08-24]]
- [[10_Reference/investing/dragon-tiger/603221-2026-09-03]]
- [[10_Reference/investing/dragon-tiger/603533-2026-09-01]]
- [[10_Reference/investing/dragon-tiger/603626-2026-08-21]]
- [[10_Reference/investing/dragon-tiger/603696-2026-08-14]]
- [[10_Reference/investing/dragon-tiger/603721-2026-09-01]]
- [[10_Reference/investing/dragon-tiger/605188-2026-09-01]]
- [[10_Reference/investing/dragon-tiger/605577-2026-09-03]]


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
