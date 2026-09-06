# 逻辑规则（Logic）索引

> 本体第三构件。从 schema 约束、质量报告、状态字段和图关系中发现的规则——校验/状态机/推断/自动化规则。
> 蒸馏自 nano-ontoprompt 四构件本体模型。

## 规则列表（Dataview 动态）

```dataview
TABLE rule_type AS "类型", target_entity AS "适用实体", severity AS "严重级"
FROM "logic"
WHERE type = "logic"
SORT severity DESC, rule_type ASC
```

## 规则类型

| 类型 | 说明 | 示例 |
|---|---|---|
| **校验规则** | 数据合法性约束 | `PE < 0` → 标记 data_suspect |
| **状态机** | 实体状态流转 | 工作流 pending→candidate→watching |
| **推断规则** | 从已有关系推出新关系 | 同行业 + 同概念 → 推断"竞争关系" |
| **自动化规则** | 触发动作的条件 | 研报入库 → 自动建链接 |

## 新建规则

用 Templater 应用 `templates/logic.md` 模板。规则要可机器执行，不是描述性文字。

## 与其他构件的关系

- 触发 → [[actions/]]（规则满足时执行的动作）
- 约束 → [[stocks/]] [[industries/]] 等实体（规则作用于哪些实体类型）
- 来源 → [[specs/]]（项目 spec 决策是规则的重要来源）
