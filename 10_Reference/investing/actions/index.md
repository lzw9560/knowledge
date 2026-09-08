# 动作（Actions）索引

> 本体第四构件。基于实体类型与关系生成的可执行行为——CRUD、状态流转、链接维护动作。
> 蒸馏自 nano-ontoprompt 四构件本体模型。

## 动作列表（Dataview 动态）

<!-- dataview-precompiled:3076fcbcc2a5 -->
| 类型 | 触发条件 | 目标实体 |
|---|---|---|
| 状态流转 | inbox 实体通过审查，需迁移到正式区 | inbox/, stocks/, industries/, concepts/ |
| 状态流转 | inbox 实体通过质量门审核（confidence=low 的 LLM 抽取实体经人工 approved）后，迁移到正式区 | inbox/, stocks/, industries/, concepts/ |
| 链接维护 | 报告入库后，扫描正文 6 位代码并建 stocks/{code} 链接 | reports/, daily/ |
| 链接维护 | 实体改名时，重写所有反向链接 | 全类型 |
| 链接维护 | 战法卡漂移检测报 drift（vault 战法卡 source_sha ≠ 源仓对应文件当前 SHA） | strategies/ |
<!-- /dataview-precompiled -->

## 动作类型

| 类型 | 说明 | 示例 |
|---|---|---|
| **CRUD** | 创建/读取/更新/删除实体 | 新研报入库 → 创建 [[10_Reference/investing/reports/index|reports/]] 实体 |
| **状态流转** | 改变实体状态字段 | 候选股 → watching（工作流流转） |
| **链接维护** | 自动建立/修复 `[[]]` 链接 | 研报提到 600519 → 链接到 [[10_Reference/investing/stocks/600519]] |
| **审计快照** | 动作执行前后的状态快照 | 结算前快照 winrate 状态 |

## 新建动作

用 Templater 应用 `templates/action.md` 模板。动作必须含：触发条件 + 执行步骤 + 审计点。

## 与其他构件的关系

- 触发自 → [[10_Reference/investing/logic/index|logic/]]（规则满足时触发动作）
- 作用于 → [[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/reports/index|reports/]] 等实体
- 执行记录 → [[10_Reference/investing/reviews/index|reviews/]]（动作执行的审计追踪）

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- H_Reference/investing/actions/审批实体]]
- H_Reference/investing/actions/研报自动链接]]
- H_Reference/investing/actions/inbox晋级]]
- H_Reference/investing/actions/实体重命名]]
- H_Reference/investing/actions/源同步]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/action` 新建 动作 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:98d7adab92bb -->
| 动作总数 |
|---|
| 5 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
