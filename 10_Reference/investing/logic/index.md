# 逻辑规则（Logic）索引

> 本体第三构件。从 schema 约束、质量报告、状态字段和图关系中发现的规则——校验/状态机/推断/自动化规则。
> 蒸馏自 nano-ontoprompt 四构件本体模型。

## 规则列表（Dataview 动态）

<!-- dataview-precompiled:c5c1841443c6 -->
| 类型 | 适用实体 | 严重级 |
|---|---|---|
| 推断规则 | events | medium |
| 推断规则 | 全类型（以 frontmatter confidence + last_verified 字段的实体） | medium |
| 校验规则 | 全类型 | medium |
| 准入闸 | 跨域链接 | medium |
| 校验规则 | metrics, valuations, reports | medium |
| 状态机 | 全类型 | medium |
| 校验规则 | 全类型 | medium |
| 校验规则 | stocks, industries, concepts | medium |
| 别名 | strategies | medium |
| 漂移检测 | 全实体 | medium |
| 校验规则 | strategies | medium |
| 推断规则 | strategies | medium |
| 自动化规则 | reports | medium |
| 分级规则 | 全实体 | low |
| 状态机 | 全类型 | low |
| 校验规则 | inbox_item | high |
| 校验规则 | stocks | high |
| 校验规则 | 全类型 | high |
| 校验规则 | 全类型 | high |
| 状态机 | 全类型 | high |
| 校验规则 | 全类型 | high |
| 状态机 | inbox_item | high |
| 校验规则 | stocks | high |
| 自动化规则 | 全类型 | high |
<!-- /dataview-precompiled -->

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

- 触发 → [[10_Reference/investing/actions/index|actions/]]（规则满足时执行的动作）
- 约束 → [[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/industries/index|industries/]] 等实体（规则作用于哪些实体类型）
- 来源 → [[10_Reference/investing/specs/index|specs/]]（项目 spec 决策是规则的重要来源）

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/logic/LLM抽取质量门]]
- [[10_Reference/investing/logic/PE异常]]
- [[10_Reference/investing/logic/broken-link-alert]]
- [[10_Reference/investing/logic/broken-link-grading]]
- [[10_Reference/investing/logic/causal-chains]]
- [[10_Reference/investing/logic/confidence-decay]]
- [[10_Reference/investing/logic/coverage-floor]]
- [[10_Reference/investing/logic/cross-domain-gate]]
- [[10_Reference/investing/logic/data-freshness]]
- [[10_Reference/investing/logic/duplicate-merge]]
- [[10_Reference/investing/logic/entity-archive]]
- [[10_Reference/investing/logic/entity-lifecycle]]
- [[10_Reference/investing/logic/entity-merge]]
- [[10_Reference/investing/logic/entity-promotion]]
- [[10_Reference/investing/logic/orphan-threshold]]
- [[10_Reference/investing/logic/relation-cardinality]]
- [[10_Reference/investing/logic/sentiment-weather-mapping]]
- [[10_Reference/investing/logic/source-drift]]
- [[10_Reference/investing/logic/static-value-ban]]
- [[10_Reference/investing/logic/stub-lifecycle]]
- [[10_Reference/investing/logic/实体改名]]
- [[10_Reference/investing/logic/战法卡漂移检测]]
- [[10_Reference/investing/logic/战法天气映射]]
- [[10_Reference/investing/logic/报告图谱关联]]

---

## ⚡ 快速操作

用 Templater 应用 `templates/logic` 新建 逻辑规则 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:8c37937ea480 -->
| 逻辑规则总数 |
|---|
| 24 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
