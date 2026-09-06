# 项目决策 索引

> SDD spec 决策实体节点。对应 `specs/` 目录下的 spec 文档。每条记录链接其问题/目标、需求、受影响文件、验收标准、关联决策。

## 实体列表（Dataview 动态）

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "spec"
SORT number ASC
```

## 关系

- defines: [[strategies/]]（spec 定义战法 match 逻辑）
- references: [[data-sources/]]（spec 引用数据源）
- depends_on: [[specs/]]（spec 间依赖/栈式关系）

## 新建实体

用 Templater 应用 `templates/spec` 新建。

> 注：阶段 0 不自动导入 `specs/` 目录。阶段 1 计划批量导入为决策实体。
