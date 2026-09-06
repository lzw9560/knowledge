---
type: logic
rule_id: STATIC-VALUE-BAN-001
rule_type: 校验规则
target_entity: stocks
severity: high
condition: stocks/ 实体 frontmatter 含时点数据字段（pe_ttm / pb / price / market_cap 等）→ 报违规
action_on_violation: 标记 data_suspect + 提示迁移到对应时点实体（valuations/）
source: ora-3 诊断 §2.5（frontmatter 禁止放时点数据）+ D8-9 规划
status: stub
created: 2026-09-07
---

# 规则：禁止 frontmatter 放时点数据

> ⚠️ **状态：stub（骨架）**。本规则为 ora-3 D8-9 规划，待实现。当前仅建文件以消除断链，逻辑骨架已定义，阈值与执行逻辑待数据校准后定稿。

## 规则定义

- **类型**：校验规则（时点数据隔离）
- **适用实体**：[[stocks/]]（以及任何 frontmatter 试图放时点字段的实体类型）
- **严重级**：high
- **条件**：`stocks/` 实体 frontmatter 含时点数据字段（`pe_ttm` / `pb` / `price` / `market_cap` / `dividend_yield` 等）

## 触发条件

ora-3 诊断 §2.5 硬事实：frontmatter 放时点数据（PE/PB/价格/市值）是**不可信的静态值**——这些数据随行情变化，写在 frontmatter 会立刻过时且无更新机制。时点数据应走 `valuations/` 时点实体（带 `as_of` 时间戳）。

## 执行逻辑

```
对每个 type = "stock" 的实体：
  时点字段集合 = {"pe_ttm", "pb", "price", "market_cap", "dividend_yield", ...}
  for field in frontmatter.keys():
    if field in 时点字段集合:
      报违规：stocks/xxx.md frontmatter 含时点字段 <field>
      标记 data_suspect: true
      suspect_reason: "frontmatter 禁放时点数据，应迁移到 valuations/ 实体"
      提示：迁移到 [[valuations/]] 时点实体（带 as_of）
```

## 违反处置

- `action_on_violation`：标记 `data_suspect: true` + `suspect_reason`
- 提示迁移路径：时点数据应建 `valuations/<code>-latest.md` 实体（带 `as_of` 时间戳 + `code` 关联 stocks/ 实体）
- 过渡期：[[logic/PE异常]]（PE-001）作为过渡期校验，对仍残留 frontmatter 的 pe_ttm 做值域检查

## 阈值依据

- **时点字段集合**：ora-3 诊断 §2.5 列举的字段 + 实际 vault 中观察到的违规字段。完整字段集合待数据校准后定稿。

## 关联

- 约束实体：[[stocks/]]
- 迁移目标：[[valuations/]]（时点实体，带 as_of）
- 过渡期规则：[[logic/PE异常]]（PE-001，对残留 frontmatter pe_ttm 做值域校验）
- 来源：ora-3 诊断 §2.5（`docs/knowledge-graph-improvement-vision.md` line 285）+ D8-9 规划
