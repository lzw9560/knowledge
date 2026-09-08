---
type: logic
rule_type: 推断规则
target_entity: events
severity: medium
created: 2026-09-07
confidence: high
source: ora-3_diagnosis
---

> [!info] ⚙️ 规则
> **规则**：``  **类型**：推断规则
> **严重级**：medium  **适用实体**：events
>
> **违反处置**：``

## 📋 规则定义

| # | 链 | 类型 | 验证状态 | 验证方式 |
|---|---|---|---|---|
| 1 | `events/涨停池` → `stocks/*` 涨幅 | 因果 | 待验证 | 涨停池入选 vs 未入选次日收益对比 |
| 2 | `dragon-tiger/席位` → `stocks/*` 次日走势 | 因果（待验证） | 未验证 | 龙虎榜净买入 vs 次日涨跌幅回归 |
| 3 | `concepts/*` ↔ `stocks/*` 成分股联动 | 相关 | 已知相关 | 板块涨跌幅 vs 成分股等权平均相关系数 |
| 4 | `analysts/*` 评级调整 → `stocks/*` 股价波动 | 因果（待验证） | 未验证 | 评级变更事件研究法（CAR） |
| 5 | `metrics/营收` → `valuations/PE` 估值切换 | 因果 | 待验证 | 营收增速变化 vs PE 估值切换时点 |
| 6 | `strategies/战法` 匹配 → `events/涨停` | 因果（待验证） | 未验证 | 战法命中样本 vs 随机基准的涨停率 lift |
| 6a | `strategies/一字竞价选股法` F1（竞价一字板≥2）→ `events/竞价异动` | 因果（待验证） | 未验证 | 竞价一字板数 ≥2 的板块 vs 其他板块当日涨幅对比 |
| 6b | `strategies/一字竞价选股法` F2（辨识度龙头）→ `stocks/*` 次日溢价 | 因果（待验证） | 未验证 | 高辨识度龙头 vs 板块平均次日溢价对比 |
| 6c | `strategies/一字竞价选股法` F3（旧主线回流）→ 卖出信号有效性 | 因果（待验证） | 未验证 | 旧主线回流时卖出 vs 持有收益对比 |


## ⚡ 触发条件

- 每日收盘后 `daily_audit.py` 扫描 events/ + dragon-tiger/ 新增实体
- 当 events/ 新增涨停池记录时，触发链 1（涨停池 → 个股涨幅）
- 当 dragon-tiger/ 新增席位记录时，触发链 2（席位 → 次日走势）
- 当 analysts/ 新增评级调整时，触发链 4（评级 → 股价波动）
- 当 metrics/ 营收字段更新时，触发链 5（营收 → PE 估值切换）

## 🔧 执行逻辑

```
for chain in causal_chains:
    source_entities = scan(chain.source_path, new_since=last_run)
    for src in source_entities:
        target = resolve_link(src, chain.edge_type)
        if target:
            correlation = compute_correlation(src, target, window=30)
            if abs(correlation) > chain.threshold:
                report(f"{chain.id}: {src} → {target} r={correlation:.2f}")
```

- 链 1/2/4/5 标注"待验证"——需 ≥30 个样本 + 显著性 p<0.05 才转"已验证"
- 链 3 已知相关——板块联动是 A 股常识，无需再验
- 验证方式见规则定义表第 5 列


## ⚠️ 违反处置

- ``


## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
