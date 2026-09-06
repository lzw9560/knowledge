---
title: "盘中情绪追踪"
date: {{date:YYYY-MM-DD}}
type: daily_mid
tags: [sentiment, mid-market, daily]
trading_date: "{{date:YYYY-MM-DD}}"
temperature_z: 0
velocity_dz: 0
divergence_d: 0
direction: ""
confidence: 0
circuit_breaker_level: 0
position_label: ""
position_range: [0.5, 0.7]
l0_macro_z: 0
l1_policy_z: 0
l2_inst_z: 0
l3_capital_z: 0
l4_sentiment_z: 0
l5_derivatives_z: 0
key_signals: []
---

# 🔥 盘中情绪追踪 · {{date:YYYY-MM-DD}}

> **温度Z：`=this.temperature_z`** | **方向：`=this.direction`** | **置信度：`=this.confidence`** | **熔断：L`=this.circuit_breaker_level**
> **仓位建议：`=this.position_label`（`=this.position_range`）**
> 关联盘前：[[{{date:YYYY-MM-DD}}_pre_盘前情绪报告]]

## 三维向量实时追踪

| 维度 | 当前值 | vs 盘前 | 变化 |
|------|--------|---------|------|
| 🌡️ 温度 Z | `=this.temperature_z` | | |
| 📈 速率 ΔZ | `=this.velocity_dz` | | |
| 🔀 背离度 D | `=this.divergence_d` | | |

## 6层信号盘中变化

### L0 宏观周期（Z：`=this.l0_macro_z`）
> 盘中不更新（月频/日频数据，盘前已定）

### L1 政策监管（Z：`=this.l1_policy_z`）
> 盘中突发政策速记

| 时间 | 事件 | 影响 | Z修正 |
|------|------|------|-------|
| | | | |

### L2 机构动向（Z：`=this.l2_inst_z`）
> 午盘龙虎榜预览（如有）

| 指标 | 盘前 | 盘中观测 | 变化 |
|------|------|---------|------|
| 机构净买卖 | | | |
| 游资活跃度 | | | |

### L3 资金面（Z：`=this.l3_capital_z`）

| 指标 | 盘前预估 | 盘中实际 | 偏离 |
|------|---------|---------|------|
| 成交额(亿) | | | |
| 量能比 | | | |
| 北向资金 | | | |
| 主力净流入 | | | |

### L4 市场情绪（Z：`=this.l4_sentiment_z`）

| 指标 | 盘前 | 盘中 | 变化 |
|------|------|------|------|
| 涨停数 | | | |
| 跌停数 | | | |
| 炸板率 | | | |
| 连板最高 | | | |
| 板块轮动 | | | |

### L5 衍生品（Z：`=this.l5_derivatives_z`）
> 午盘后期权数据更新

| 指标 | 盘前 | 盘中 | 变化 |
|------|------|------|------|
| PCR | | | |
| IV | | | |
| 基差 | | | |

## 板块异动

| 板块 | 方向 | 异动原因 | 量能 | 持续性 |
|------|------|---------|------|--------|
| | | | | |

## 盘中信号修正

> 是否需要调整盘前判断？

| 层级 | 盘前Z | 盘中Z | 修正原因 |
|------|-------|-------|---------|
| L0 | | | |
| L1 | | | |
| L2 | | | |
| L3 | | | |
| L4 | | | |
| L5 | | | |

**修正后综合判断：**
- 温度Z：→ 
- 方向：→ 
- 仓位：→ 

## 三重护栏盘中检查

| 护栏 | 状态 | 说明 |
|------|------|------|
| Z在[-0.5,0.5]？ | | |
| 成交额低于均值？ | | |
| 机构净卖出？ | | |

> 若三重护栏全触发 → 仓位上限再降10%

---
> 盘中记录仅用于当晚复盘参考。  
> 关联盘后：[[{{date:YYYY-MM-DD}}_post_盘后复盘]]  
> 关联评分：[[scores/{{date:YYYY-MM-DD}}_score|情绪评分]]
