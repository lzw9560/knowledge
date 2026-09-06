---
type: logic
rule_id: CONFIDENCE-DECAY-001
rule_type: 推断规则
target_entity: 全类型（以 frontmatter confidence + last_verified 字段的实体）
severity: medium
condition: 实体 confidence 字段随时间衰减——90 天未验证降一级（high→medium→low），180 天标 stale 待复审
action_on_violation: 不自动改值，只生成审查报告提醒（ora-3 §2.5 否决自动衰减算法）
source: ora-3 §2.5（时效性：用最后验证日期替代置信度衰减）+ AGENTS.md 工程底线（不臆造数据 / 参数选择需数据支撑）
created: 2026-09-07
---

# 规则：信任度衰减机制

## 规则定义

- **类型**：推断规则（生成审查提示，不自动改值）
- **适用实体**：全类型（有 `confidence` + `last_verified` frontmatter 字段的实体）
- **严重级**：medium（提示性，不阻断）
- **条件**：实体的 `last_verified` 字段距今 > 90 天 → 提示降级；> 180 天 → 标 stale

## 设计决策（ora-3 §2.5）

### 否决自动衰减算法的理由

ora-3 §2.5 明确否决了"confidence 随时间自动衰减"的算法，改为"用 `last_verified` 日期 + 审查报告提醒"。理由：

1. **语义混淆**：`confidence` 在 pipeline §4 的语义是**抽取可靠度**（L1 规则=high / L3 别名=medium / L4 LLM 语义=low），是"这条数据怎么来的"，不是"这条数据有多新"。把时间衰减混进 confidence 会让一个字段承载两个正交语义，后续无法区分"LLM 猜的"和"很久没更新的"。
2. **参数无数据支撑**：衰减速率（30 天？90 天？）是拍脑袋参数，违反 `AGENTS.md`「参数选择必须有数据支撑，不得凭直觉拍脑袋」。
3. **重算成本**：衰减需要定时重算全库，且衰减速率是任意值。

### 替代方案：双字段正交

```yaml
confidence: high              # 抽取可靠度（不变，语义纯化）
last_verified: 2026-09-06     # 最后一次人工/脚本核验日期
data_asof: 2026-09-06         # 时点数据的数据日期（pe_ttm 等的快照日期）
```

- `confidence` 不变——它回答"这条数据怎么来的"。
- `last_verified` 回答"这条数据多久没核验"。
- `data_asof` 回答"时点数据是哪天的"。

## 衰减阈值

| `last_verified` 距今 | 状态 | 提示动作 |
|---|---|---|
| ≤ 30 天 | ✅ fresh | 无 |
| 31-90 天 | 🟡 aging | 提示：建议近期核验 |
| 91-180 天 | 🟠 stale | 提示：降一级（high→medium / medium→low），**仅提示不自动改值** |
| > 180 天 | 🔴 critical-stale | 标 `stale: true`，进入季度审查必核清单 |

> 阈值依据：90 天 = 一个季度，对应季度审查周期；180 天 = 半年，对应中期报告周期。这不是"数据支撑的衰减速率"，是"审查周期对齐"——参数来源是工作流周期，非任意值。

## 执行逻辑（审查脚本实现）

`scripts/vault_audit.py` 的 `check_stale` 检查（第 8 项）已基于 git log 90 天未更新。本规则在此之上加 `last_verified` 字段判定：

```
for file in vault:
    fm = parse_frontmatter(file)
    last_verified = fm.get("last_verified")
    if not last_verified:
        continue  # 未标 last_verified 的实体跳过（不强求所有实体都有此字段）
    days_since = (today - parse_date(last_verified)).days
    if days_since > 180:
        report.append({"file": file, "level": "critical-stale", "days": days_since})
    elif days_since > 90:
        report.append({"file": file, "level": "stale", "days": days_since})
        # 提示降级，但不自动改 confidence 字段
```

## 时点数据的特殊处置

ora-3 §2.5 第 3 步：时点数据（PE/PB/市值）**禁止放 frontmatter**，改为 Dataview 查 `valuations/` 实体。

| 数据类型 | 处置 | 理由 |
|---|---|---|
| `pe_ttm` / `pb` / `market_cap` | 从 frontmatter 删除，走 `valuations/` 实体 | 时点数据放 frontmatter + 让 MCP 查出来当实时值用 = 臆造数据（[[logic/static-value-ban]]） |
| `industry` / `list_date` / `st` | 保留 frontmatter + 配 `last_verified` | 这些真的很少变 |
| `confidence` | 不变 | 语义纯化（抽取可靠度） |

## 用户行为驱动更新

ora-3 §2.5 第 4 步：盘前报告生成时（[[logic/报告图谱关联]] 规则），若命中图谱实体且其 `last_verified` > 30 天，在报告"图谱关联"段追加：

```
- [ ] 600519 贵州茅台 财务数据 45 天未核验
```

这复用了报告图谱关联的缺口清单机制，不需要新基础设施。

## 不自动改值的纪律

**核心原则**：本规则只生成审查报告提醒，不自动改 `confidence` 字段值。理由：

1. 自动改值会破坏 `confidence` 的语义（抽取可靠度 vs 新鲜度），即使加 `stale: true` 标记也混淆。
2. 自动改值需要"谁有权改"的权限模型，增加复杂度。
3. 审查报告提醒已足够驱动人工核验——核验后人工更新 `last_verified`，confidence 按核验结果人工调。

## 关联

- 时点数据禁令：[[logic/static-value-ban]]
- 审查流程：[[reviews/audit-procedure]]（第 8 项 stale_check）
- 报告图谱关联：[[logic/报告图谱关联]]（last_verified > 30 天进缺口清单）
- 实体生命周期：[[logic/entity-lifecycle]]（更新态触发 last_verified 重评）
- 方法论：[[10_Reference/meta/four-construct-ontology]]（质量门四维度之一）
