# 战法 索引

> 投研战法卡片节点。12 张战法卡已从 `backend/strategies/cards/` 导入。每张卡链接其入场条件、出场条件、历史战绩、匹配股票、关联事件、来源 spec。

## 实体列表（Dataview 动态）

```dataview
TABLE name AS "战法名", edge_family AS "edge 家族", entry_conditions AS "入场条件"
FROM "strategies"
WHERE type = "strategy"
SORT name ASC
```

## 关系

- matches: [[stocks/]]（战法匹配的股票）
- triggered_by: [[events/]]（战法由事件触发，如涨停池触发首板）
- defined_in: [[specs/]]（战法 match 逻辑对应的 SDD spec）
- pairs_with: [[dragon-tiger/]]（反包战法依赖游资席位加分项）

## edge 家族说明

| edge_family | 说明 | 典型战法 |
|---|---|---|
| 动量溢价 | 连板/涨停惯性博次日溢价 | consecutive_relay, first_plate, end_of_day_sneak |
| 事件溢价 | 炸板/反包等情绪转折博弈 | reverse_package, break_reseal, storm_reversal |
| 均值回归 | 回调低吸博反弹 | low_absorption |
| 形态突破 | 平台/形态突破 | platform_breakout, pattern_reversal |
| 龙头追踪 | 板块龙头识别 | dragon_head |
| 接力博弈 | 弱转强/N字接力 | weak_turn_strong, n_shape_counterattack |

## 新建实体

用 Templater 应用 `templates/strategy` 新建（12 张已导入，后续新增战法用模板）。
