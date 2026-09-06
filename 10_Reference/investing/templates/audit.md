---
type: audit
audit_date: <% tp.date.now("YYYY-MM-DD") %>
auditor: 
scope: 全量
findings_count: 0
critical: 0
high: 0
medium: 0
low: 0
status: 进行中
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 审查报告：<% tp.date.now("YYYY-MM-DD") %>

> ReAct Agent 体检。跑 8 项检查，问题按严重级分类，给修复建议。

## 审查范围

- **范围**：`scope`（全量 / 增量 / 触发式）
- **审查人/Agent**：`auditor`
- **触发**：季度审查 / 新 spec 落地 / 实体改名 / 大批量灌入

## 8 项检查结果

### 1. summary（图谱摘要）
- 实体总数：
- 关系总数：
- 各类型分布：

### 2. coverage（覆盖率）
- stocks/ 实体数 vs 预期：
- industries/ 覆盖：
- 哪些类型严重缺失：

### 3. orphan_check（孤立实体）
- 无入边实体数：
- 高风险孤立：

### 4. broken_link（断链）
- `[[]]` 指向不存在文件数：
- 严重断链：

### 5. schema_infer（schema 偏差）
- 实际 frontmatter 字段 vs 设计模板：
- 新增字段：

### 6. relation_density（关系密度）
- 入边过多实体（hub 风险）：
- 入边过少实体（信息孤岛）：

### 7. duplicate_check（重复）
- 同代码多记录：
- 同名称多记录：

### 8. stale_check（过期）
- 长期未更新实体：
- 最久未更新：

## 问题清单

### Critical（阻断）
- （待填写）

### High（优先修）
- （待填写）

### Medium（进 backlog）
- （待填写）

### Low（知悉即可）
- （待填写）

## 修复建议

1. （按问题优先级给修复步骤）

## 跟踪

- [ ] Critical 全部修复
- [ ] High 修复或进 spec
- [ ] Medium 进 backlog
- [ ] 下次审查日期：
