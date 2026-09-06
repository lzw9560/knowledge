---
type: logic
rule_id: ENTITY-LIFECYCLE-001
rule_type: 状态机
target_entity: 全类型
severity: high
condition: 实体从创建到归档/删除的状态流转，强制走 inbox 质量门 + approved 字段
action_on_violation: 不经 inbox 直接进正式区 → 报 high；正式区直接删 → 报 critical
source: ora-3 §1.3（inbox stub 通道）+ AGENTS.md 工程底线（不臆造数据 / 私有数据隔离）
created: 2026-09-07
---

# 规则：实体生命周期管理

## 规则定义

- **类型**：状态机规则
- **适用实体**：全类型（stocks/industries/strategies/.../logic/actions）
- **严重级**：high（违反 → 阻止操作）
- **条件**：实体的状态流转必须遵循"创建 → 更新 → 合并 → 归档 → 删除"五态机

## 生命周期五态

```
       ┌──────────────────────────────────┐
       │           创建（Create）           │
       │  inbox/ → 正式区（stocks/ 等）    │
       └──────────┬───────────────────────┘
                  │ approved: false → true
                  ▼
       ┌──────────────────────────────────┐
       │           更新（Update）          │
       │  字段变更 → quality_score 重评   │
       └──────────┬───────────────────────┘
                  │ 同 code 出现重复
                  ▼
       ┌──────────────────────────────────┐
       │           合并（Merge）           │
       │  保留最新/最完整 → 链接重定向     │
       └──────────┬───────────────────────┘
                  │ 废弃
                  ▼
       ┌──────────────────────────────────┐
       │           归档（Archive）         │
       │  正式区 → 20_Archive/             │
       └──────────┬───────────────────────┘
                  │ 仅 inbox 允许
                  ▼
       ┌──────────────────────────────────┐
       │           删除（Delete）          │
       │  inbox/ 可删；正式区只能归档      │
       └──────────────────────────────────┘
```

## 1. 创建（Create）

### 入口：inbox stub

所有新实体**必须先进 `inbox/`**，不允许直接进正式区（stocks/industries/...）。

```yaml
---
type: stock
code: 003040
name: 楚天龙
confidence: medium          # L1 规则抽取 = high / L3 别名 = medium / L4 LLM 语义 = low
source: "daily-report:2026-09-05"   # 来源可追溯
quality_score: 40           # 0-100，< 60 不晋级
approved: false             # 未审核
created: 2026-09-05
---
```

> 正文只留一行 `> 由盘前报告缺口自动建档，待补充核心业务/战法关联`。

### 晋级：inbox → 正式区

触发条件（[[logic/inbox-promotion]]，需落地为脚本检查）：
- `quality_score` ≥ 60
- 有 ≥1 条战法或行业边（`[[strategies/]]` 或 `[[industries/]]`）
- **被 ≥2 份不同日期报告命中才建档**（避免一次性龙虎榜股进图谱）

动作（[[actions/promote-from-inbox]]）：
```bash
mv inbox/003040.md stocks/003040.md
# frontmatter 加 approved_date 字段
```

### 滞留处置

- inbox 滞留 > 14 天未晋级 → 自动标 `rejected: true` + `reject_reason: 未达引用阈值`
- 季度清理：rejected 实体移到 `20_Archive/inbox-rejected/`

## 2. 更新（Update）

字段变更时：
- `quality_score` 重评（按四维度：confidence / source / 完整度 / approved）
- `last_verified` 字段更新（见 [[logic/confidence-decay]]）
- 时点数据（PE/PB/市值）**禁止放 frontmatter**，走 `valuations/` 实体（[[logic/static-value-ban]]）

## 3. 合并（Merge）

详见 [[logic/duplicate-merge]]。同一 `code` 出现多份实体时：
- 保留最新 / 最完整的
- 合并关系（`[[]]` 链接去重合并）
- 冗余文件删除，链接重定向到保留文件

## 4. 归档（Archive）

废弃实体（不再被任何报告/spec/战法引用，且 stale_check 标记 180+ 天未更新）：
- `mv stocks/xxx.md 20_Archive/stocks/xxx.md`
- frontmatter 加 `archived: true` + `archived_date`
- 保留所有 `[[]]` 链接（归档不删链接，断链检测会标"指向归档"）

## 5. 删除（Delete）

**严格限制**：
- `inbox/` 允许直接删（rejected 或错误建档）
- 正式区（`stocks/` 等）**不允许删**——只能归档
- 违反 → 报 critical

理由：删除会破坏所有反向链接，产生断链。归档保留文件，断链检测能识别"指向归档"并提示。

## 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| 不经 inbox 直接进正式区 | high | 移回 inbox + 走晋级流程 |
| 正式区直接删文件 | critical | 从 git 恢复 + 归档而非删除 |
| inbox 滞留 > 14 天未处置 | low | 标 rejected |
| 时点数据放 frontmatter | high | 移到 valuations/ 实体（[[logic/static-value-ban]]） |

## 关联

- 晋级规则：[[logic/inbox-promotion]]（待落地为脚本）
- 合并规则：[[logic/duplicate-merge]]
- 时点数据禁令：[[logic/static-value-ban]]
- 信任度衰减：[[logic/confidence-decay]]
- 晋级动作：[[actions/promote-from-inbox]]
- 同步动作：[[actions/sync-from-source]]
- 审查闭环：[[reviews/audit-procedure]]
- 方法论：[[10_Reference/meta/four-construct-ontology]]（四构件：实体是构件 1）
