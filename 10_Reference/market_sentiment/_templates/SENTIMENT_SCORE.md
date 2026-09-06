---
title: "情绪评分"
date: <% tp.date.now("YYYY-MM-DD") %>
type: score
tags: [sentiment, score]
trading_date: "<% tp.date.now("YYYY-MM-DD") %>"
# 三维向量评分（稳健z-score）
temperature_z: 0.0000
velocity_dz: 0.0000
divergence_d: 0.0000
direction: neutral
confidence: 0.00
circuit_breaker_level: 0
# 仓位建议
position_label: 中性
position_range: [0.5, 0.7]
position_action: 正常配置
# 各层得分
l0_macro_z: 0.0000
l1_policy_z: 0.0000
l2_inst_z: 0.0000
l3_capital_z: 0.0000
l4_sentiment_z: 0.0000
l5_derivatives_z: 0.0000
# 关键子指标
limit_up_count: 0
max_consecutive: 0
broken_rate: 0.00
northbound_net: 0
volume_ratio: 0.00
---

# 📊 情绪评分 `<% tp.date.now("YYYY-MM-DD") %>`

## 三维向量

| 维度 | Z值 | 含义 |
|------|-----|------|
| 🌡️ 温度 Z | `=this.temperature_z` | 当前状态 vs 历史分位 |
| 📈 速率 ΔZ | `=this.velocity_dz` | 5日变化率 |
| 🔀 背离度 D | `=this.divergence_d` | 层间方向不一致程度 |

**方向**: `=this.direction` | **置信度**: `=this.confidence * 100`% | **熔断**: Level `=this.circuit_breaker_level`

## 六层信号

| 层级 | Z值 | 方向 | 关键信号 |
|------|-----|------|---------|
| L0 宏观周期 | `=this.l0_macro_z` | — | 社融/PMI/DR007 |
| L1 政策监管 | `=this.l1_policy_z` | — | 政策事件/监管态度 |
| L2 机构动向 | `=this.l2_inst_z` | — | 龙虎榜席位博弈 |
| L3 资金面 | `=this.l3_capital_z` | — | 主力资金/竞价异动 |
| L4 市场情绪 | `=this.l4_sentiment_z` | — | 涨停池/连板天梯 |
| L5 衍生品 | `=this.l5_derivatives_z` | — | PCR/IV/基差/Skew |

## 仓位建议

> **`=this.position_label`** → 仓位 `=this.position_range` | `=this.position_action`

| Z-Score区间 | 状态 | 仓位 | 操作 |
|-------------|------|------|------|
| Z > 1.5 | 极度乐观 | 20-30% | 减仓防守 |
| 0.5 < Z ≤ 1.5 | 偏乐观 | 40-60% | 持有微减 |
| -0.5 ≤ Z ≤ 0.5 | **← 当前** | 50-70% | 正常配置 |
| -1.5 ≤ Z < -0.5 | 偏悲观 | 30-50% | 谨慎观望 |
| Z < -1.5 | 极度悲观 | 50-80% | 逆向建仓 |

## 核心子指标

| 指标 | 今日值 | 说明 |
|------|--------|------|
| 涨停数 | `=this.limit_up_count` | 涨停池总量 |
| 最高连板 | `=this.max_consecutive`板 | 连板天梯顶端 |
| 炸板率 | `=this.broken_rate * 100`% | 炸板/涨停+炸板 |
| 北向资金 | `=this.northbound_net`亿 | 降权后信号 |
| 量能比 | `=this.volume_ratio` | 成交额/20日均值 |

## ⚠️ 对抗性分析

> 如果当前判断是错的，最可能因为：
> - [盘后人工填写反面论据]
> - [盘后人工填写]
> - [盘后人工填写]

## 决策流程

```
第一步：L0+L1 → 战略方向（多/空/中性，1-3月）
第二步：L2+L3 → 战术时机（入场/出场，1-5天）
第三步：L4+L5 → 交叉确认（置信度调整，0-3天）
```

---
> 评分引擎：`_data/db/sentiment_engine.py` | 配置：`_data/db/framework_config.json`
> 框架是决策辅助，不是决策者。框架占40%，盘感占30%，纪律占30%。
