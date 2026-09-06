# 待审层（Inbox）索引

> Curated 质量门——LLM 抽取的实体先落这里，带 confidence + source + quality_score，审核通过后才进正式区。
> 蒸馏自 nano-ontoprompt 质量门机制。不直接灌入是知识图谱健康的第一道防线。

## 待审实体（Dataview 动态）

```dataview
TABLE entity_type AS "类型", name AS "名称", confidence AS "置信度", quality_score AS "质量分", source AS "来源"
FROM "inbox"
WHERE type != "index"
SORT quality_score ASC, confidence ASC
```

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

## 四层关系推断的落点

| 层 | 准确度 | 进 inbox？ |
|---|---|---|
| L1 精确外键 | ★★★★★ | 否，直接入库 |
| L2 值格式容错 | ★★★★ | 否，直接入库 |
| L3 备用键 | ★★★ | 是，标 confidence: medium |
| L4 LLM 语义 | ★★ | 是，标 confidence: low + `inferred_by: llm` |

## 新建待审实体

LLM 抽取脚本输出到 `inbox/`，用 `templates/inbox-item.md` 模板。不要直接往正式文件夹写。
