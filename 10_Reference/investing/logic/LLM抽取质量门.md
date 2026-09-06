---
type: logic
rule_id: QUALITY-GATE-001
rule_type: 校验规则
target_entity: inbox_item
severity: high
condition: confidence = low 的实体 → 必须进 inbox/ → 人工审核通过才进正式区
action_on_violation: 拒绝写入正式区（stocks/industries/concepts 等实体文件夹）
source: ora-3 诊断 §6.5 + pipeline §4（confidence 语义）
created: 2026-09-07
---

# 规则：LLM抽取质量门

## 规则定义

- **类型**：校验规则
- **适用实体**：[[inbox/]]（待审实体）
- **严重级**：high
- **条件**：`confidence = low` 的实体必须先进 inbox/，人工审核通过（`approved: true`）才可移入正式区

## 触发条件

任何 LLM 抽取的实体/关系写入图谱时触发。按 pipeline §4 的四层渐进抽取，confidence 语义为**抽取可靠度**（不是新鲜度）：

| 抽取层 | confidence | 含义 |
|---|---|---|
| L1 规则抽取 | high | 正则/词典匹配，可靠度高，可直接进正式区 |
| L3 备用键（别名表） | medium | 别名映射，需轻量审核 |
| L4 LLM 语义推断 | low | LLM 推测，必须进 inbox |

## 执行逻辑

```
触发：实体写入请求
  1. 校验 confidence：
     if confidence = "high" (L1 规则):
       允许直接写正式区（stocks/industries/concepts 等）
     elif confidence = "medium" (L3 别名):
       进 inbox/，标记 needs_light_review
     elif confidence = "low" (L4 LLM):
       强制进 inbox/
       必须 inferred_by: llm 标注
       拒绝写入正式区
  2. inbox/ 审核流程：
     if 人工审核通过:
       标记 approved: true, approved_date: <date>
       触发 [[actions/promote-from-inbox]] 移入正式区
     if 滞留 > 14 天未晋级:
       标记 rejected: true, reject_reason: 未达引用阈值
```

## 违反处置

- `action_on_violation`：拒绝 confidence=low 的实体直接写入正式区
- 外部 agent（trading-agents、daily-stock-analysis）通过 MCP `create_note` 写入时，路径必须落在 `inbox/`，不能直接写正式区（ora-3 §6.5 line 928）
- 违反 → 审查脚本报"质量门失守"critical

## confidence 语义纪律

ora-3 诊断 §6.5 line 946 明确：
> 置信度时间衰减算法 → **砍**。confidence 在 pipeline §4 里的语义是**抽取可靠度**（L1 规则=high / L3 别名=medium / L4 LLM=low），是"这条数据怎么来的"，不是"这条数据有多新"。把时间衰减混进 confidence 会让一个字段承载两个正交语义。

新鲜度用 `last_verified` 日期字段单独承载，不混入 confidence。

## 关联

- 触发动作：[[actions/promote-from-inbox]]（inbox → 正式区的 mv + approved_date）—— ora-3 D10 规划，待建
- 约束实体：[[inbox/]]
- 来源：ora-3 诊断 §6.5（`docs/knowledge-graph-improvement-vision.md` line 928-929, 946）+ pipeline §4（`docs/knowledge-graph-llm-pipeline.md` line 259-264）
- 相关规则：[[报告图谱关联]]（报告扫描出的待入图谱代码 → 进 inbox 走本规则）
