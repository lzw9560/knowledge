# 项目决策 索引

> SDD spec 决策实体节点。对应 `specs/` 目录下的 spec 文档。每条记录链接其问题/目标、需求、受影响文件、验收标准、关联决策。

## Spec 实体列表（Dataview 动态）

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "spec"
SORT number ASC
```

## Decision 实体列表（Dataview 动态）

```dataview
TABLE number AS "编号", title AS "标题", status AS "状态"
FROM "specs"
WHERE type = "decision"
SORT number ASC
```

## 关系

- defines: [[strategies/]]（spec 定义战法 match 逻辑）
- references: [[data-sources/]]（spec 引用数据源）
- depends_on: [[specs/]]（spec 间依赖/栈式关系）

## 新建实体

用 Templater 应用 `templates/spec` 新建。

## 已灌入关键 spec（2026-09-06 第一批）

> 从 `specs/README.md` 选已实现 + 影响架构的关键 spec 灌入，含 13 spec + 5 decision。详见源 `specs/README.md`（S001-S166 全量索引）与 `specs/decision-log.md`（DEC-001~005）。

- [[specs/S007-契约层]] · [[specs/S008-后端数据层迁移]] · [[specs/S010-工具注册表与SYSTEM_PROMPT]] · [[specs/S011-调度收口]] · [[specs/S017-A股涨跌预测模型栈]] · [[specs/S018-多源特征工程]] · [[specs/S019-macro-Fred-API]] · [[specs/S020-worldmonitor决策因子接入]] · [[specs/S031-调度收口盘前多层按战法回测]] · [[specs/S047-基因分权重回测校准]] · [[specs/S066-策略特定漏斗架构重构]] · [[specs/S094-战法分类与双pipeline重构]] · [[specs/S100-战法卡片对齐]]
- [[specs/DEC-001]] · [[specs/DEC-002]] · [[specs/DEC-003]] · [[specs/DEC-004]] · [[specs/DEC-005]]
