# 分析师 索引

> 研报作者节点。对应 Pydantic 契约 `Report.researcher`。每位分析师链接其覆盖领域、近期研报、历史评级胜率。

## 实体列表（Dataview 动态）

```dataview
TABLE name AS "姓名", org AS "机构", coverage_count AS "覆盖数"
FROM "analysts"
WHERE type = "analyst"
SORT name ASC
```

## 关系

- authored: [[reports/]]（该分析师的研报）
- covers: [[stocks/]]（该分析师覆盖的个股，通过研报间接关联）
- sourced_from: [[data-sources/]]（分析师排名数据来源）

## 新建实体

用 Templater 应用 `templates/analyst` 新建。
