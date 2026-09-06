---
type: inbox_item
entity_type: 
name: 
code: 
confidence: low
source: 
quality_score: 0
completeness: 
consistency: 
linkage: 
traceability: 
approved: false
approved_date: 
rejected: false
reject_reason: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 待审实体：<% tp.file.title %>

> 此实体在质量门待审区。审核通过后 `mv` 到对应正式文件夹，frontmatter 加 `approved_date`。

## 来源

- **抽取来源**：`source`（spec/代码/研报/LLM 推断）
- **置信度**：`confidence`（high / medium / low）
- **推断方式**（如适用）：L1 精确外键 / L2 值格式容错 / L3 备用键 / L4 LLM 语义

## 质量评分

| 维度 | 评分（0-100） | 说明 |
|---|---|---|
| 完整度 | `completeness` | 必填字段齐全度 |
| 一致性 | `consistency` | 与已有实体是否冲突 |
| 链接度 | `linkage` | 有无入边/出边 |
| 溯源 | `traceability` | source 字段是否标注 |
| **综合** | `quality_score` | 加权总分 |

## 实体内容

（实体本身的属性，参考对应实体类型的正式模板）

## 审核决策

- [ ] 通过（quality_score ≥ 60）→ `mv` 到正式文件夹 + 设 `approved: true` + `approved_date`
- [ ] 拒绝（quality_score < 60）→ 设 `rejected: true` + `reject_reason:`
- [ ] 待补信息 → 留 inbox，标注缺失字段
