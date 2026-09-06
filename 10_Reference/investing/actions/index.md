# 动作（Actions）索引

> 本体第四构件。基于实体类型与关系生成的可执行行为——CRUD、状态流转、链接维护动作。
> 蒸馏自 nano-ontoprompt 四构件本体模型。

## 动作列表（Dataview 动态）

```dataview
TABLE action_type AS "类型", trigger AS "触发条件", target AS "目标实体"
FROM "actions"
WHERE type = "action"
SORT action_type ASC
```

## 动作类型

| 类型 | 说明 | 示例 |
|---|---|---|
| **CRUD** | 创建/读取/更新/删除实体 | 新研报入库 → 创建 [[reports/]] 实体 |
| **状态流转** | 改变实体状态字段 | 候选股 → watching（工作流流转） |
| **链接维护** | 自动建立/修复 `[[]]` 链接 | 研报提到 600519 → 链接到 [[stocks/600519]] |
| **审计快照** | 动作执行前后的状态快照 | 结算前快照 winrate 状态 |

## 新建动作

用 Templater 应用 `templates/action.md` 模板。动作必须含：触发条件 + 执行步骤 + 审计点。

## 与其他构件的关系

- 触发自 → [[logic/]]（规则满足时触发动作）
- 作用于 → [[stocks/]] [[reports/]] 等实体
- 执行记录 → [[reviews/]]（动作执行的审计追踪）
