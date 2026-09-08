---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 待审层（Inbox）索引

> Curated 质量门——LLM 抽取的实体先落这里，带 confidence + source + quality_score，审核通过后才进正式区。
> 蒸馏自 nano-ontoprompt 质量门机制。不直接灌入是知识图谱健康的第一道防线。

## 待审实体（Dataview 动态）

<!-- dataview-precompiled:1363e647c9f6 -->
| 类型 | 名称 | 置信度 | 质量分 | 来源 |
|---|---|---|---|---|
| industry | 海工 | medium | 50 | regex:industry |
| industry | 电价下 | medium | 50 | regex:industry |
| industry | 以定力应对 | medium | 50 | regex:industry |
| industry | 期待 | medium | 50 | regex:industry |
| — | — | — | — | — |
<!-- /dataview-precompiled -->

## 质量四维度

每条待审实体必须打分（0-100）：

| 维度 | 判定 | 权重 |
|---|---|---|
| **完整度** | 必填字段齐全？缺 code/name/industry 任一即不通过 | 30% |
| **一致性** | 与已有实体冲突？同名股票已存在则检查是否同一标的 | 25% |
| **链接度** | 有至少 1 个入边或出边？孤立实体降权 | 25% |
| **溯源** | 有 source 字段标注来源？无源 = 不可信 | 20% |

## 审核流程

1. LLM 抽取 → 实体进 `inbox/`，frontmatter 带 `confidence` + `source` + `quality_score: 0`（待评）
2. 人工/规则评分 → 更新 `quality_score`
3. 通过（≥60）→ `mv` 到正式文件夹，frontmatter 加 `approved_date`
4. 拒绝（<60）→ 留 inbox 标 `rejected: true` + `reject_reason:`，定期清理

## 自动审核规则

质量门支持自动转正——评分后无需手动 `mv`，规则自动处置：

| 条件 | 动作 | 触发 |
|---|---|---|
| `quality_score ≥ 60` | 自动 `mv` 到正式区 + 加 `approved_date` | 规则 `ENTITY-PROMOTION-001` |
| `quality_score < 60` | 留 inbox，标 `rejected: true` + `reject_reason` | 规则 `ENTITY-PROMOTION-001` |
| `quality_score` 缺失 | 留 inbox 待评，不晋级 | 规则 `ENTITY-PROMOTION-001` |
| inbox 滞留 > 7 天且 ≥60 | 标滞留告警 | 规则 `ENTITY-PROMOTION-001` |

> 规则定义见 10_Reference/investing/logic/实体晋级]]。阈值 60 的依据：质量四维度中缺任一关键维度（完整度 30% + 一致性 25% + 链接度 25% + 溯源 20%）都会跌破 60。

## 批量审核命令

```bash
# 自动评分 + 自动 mv 达标实体到正式区
python3 scripts/review_inbox.py --auto

# 只评分不迁移，预览将晋级哪些实体
python3 scripts/review_inbox.py --dry-run

# 只评分指定类型（如只审 stocks）
python3 scripts/review_inbox.py --auto --type stock
```

> ⚠️ `scripts/review_inbox.py` 计划中，待实现（rule `ENTITY-PROMOTION-001` 的执行器）。当前未实现前，手动按 `审核流程` 4 步操作。

## 审核报告

最新审核报告见 [[10_Reference/investing/reviews/index|审查报告索引]]，inbox 专属晋级日志在 `reviews/inbox-promotion-<date>.md`。

<!-- dataview-precompiled:5b51d7b4a604 -->
| 日期 | 问题数 | 状态 |
|---|---|---|
| 2026-09-06 | 122 | 已完成 |
| 2026-09-07 | 636 | 已完成 |
| 2026-09-08 | 1 | 已完成 |
<!-- /dataview-precompiled -->

## 四层关系推断的落点

| 层 | 准确度 | 进 inbox？ |
|---|---|---|
| L1 精确外键 | ★★★★★ | 否，直接入库 |
| L2 值格式容错 | ★★★★ | 否，直接入库 |
| L3 备用键 | ★★★ | 是，标 confidence: medium |
| L4 LLM 语义 | ★★ | 是，标 confidence: low + `inferred_by: llm` |

## 新建待审实体

LLM 抽取脚本输出到 `inbox/`，用 `templates/inbox-item.md` 模板。不要直接往正式文件夹写。
