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

## 修复跟踪

每个问题逐条跟踪，状态流转：`open` → `in_progress` → `resolved`。

| # | 检查 | 严重级 | 问题描述 | status | 负责人 | 备注 |
|---|---|---|---|---|---|---|
| 1 | broken_link | high | `[[xxx]]` 指向不存在 | open |  | 待补建或改链 |
| 2 | orphan_check | medium | `yyy/zzz` 无入边 | open |  |  |
| 3 | duplicate_check | critical | code=600519 type=stock 多份 | open |  |  |

status 取值：
- `open`：已发现未处置
- `in_progress`：正在修（建 stub / 改链 / 合并）
- `resolved`：已修复 + 验证通过

## KPI 仪表盘

| KPI | 本次值 | 阈值 | 状态 |
|---|---|---|---|
| 断链数（broken_link） |  | ≤ 3 | 🟢/🟡/🔴 |
| 孤立实体数（orphan_check） |  | ≤ 5 | 🟢/🟡/🔴 |
| 重复实体数（duplicate_check） |  | 0 | 🟢/🔴 |
| 过期实体数（stale_check，90+ 天） |  | ≤ 10 | 🟢/🟡/🔴 |
| schema 偏差数（schema_infer） |  | ≤ 5 | 🟢/🟡/🔴 |

状态判定：值 ≤ 阈值 🟢；阈值 < 值 ≤ 2×阈值 🟡；> 2×阈值 🔴。duplicate 严格 0 容忍（任一非零即 🔴）。

## 趋势对比

与上次审查对比，看治理效果走向：

| KPI | 上次（YYYY-MM-DD） | 本次 | 变化 | 趋势 |
|---|---|---|---|---|
| 断链数 |  |  |  | ↑/↓/→ |
| 孤立实体数 |  |  |  | ↑/↓/→ |
| 重复实体数 |  |  |  | ↑/↓/→ |
| 过期实体数 |  |  |  | ↑/↓/→ |
| schema 偏差数 |  |  |  | ↑/↓/→ |
| 实体总数 |  |  |  | ↑/↓/→ |

> 趋势判读：↓ 下降为改善，↑ 上升为恶化，→ 持平为稳定。

## 跟踪

- [ ] Critical 全部修复
- [ ] High 修复或进 spec
- [ ] Medium 进 backlog
- [ ] 下次审查日期：
