---
title: "盘前情绪报告"
date: <% tp.date.now("YYYY-MM-DD") %>
type: daily_pre
tags: [sentiment, pre-market, daily]
trading_date: "<% tp.date.now("YYYY-MM-DD") %>"
# 战略方向（L0+L1）
strategic_direction: 中性
strategic_horizon: 1-3月
# 战术时机（L2+L3）
tactical_signal: 观望
tactical_horizon: 1-5天
# 交叉确认（L4+L5）
confirmation_level: 0
# 综合评分
temperature_z: 0.0000
direction: neutral
confidence: 0.00
position_label: 中性
position_range: [0.5, 0.7]
# 熔断状态
circuit_breaker_level: 0
---

# 🌅 盘前情绪报告 `<% tp.date.now("YYYY-MM-DD") %>`

## 战略方向（L0宏观 + L1政策）

> **方向：`=this.strategic_direction`** | 周期：`=this.strategic_horizon`

- L0 宏观层 Z值：`=this.l0_macro_z`
  - 社融/M1-M2/PMI/DR007 状态
- L1 政策层 Z值：`=this.l1_policy_z`
  - 昨日政策事件：
  - 政策力度：

## 战术时机（L2机构 + L3资金）

> **信号：`=this.tactical_signal`** | 周期：`=this.tactical_horizon`

- L2 机构层 Z值：`=this.l2_inst_z`
  - 龙虎榜机构vs游资：
  - 融资融券变化：
- L3 资金面 Z值：`=this.l3_capital_z`
  - 北向资金（降权）：
  - 竞价异动：

## 交叉确认（L4情绪 + L5衍生品）

> **确认度：`=this.confidence * 100`%**

- L4 情绪层 Z值：`=this.l4_sentiment_z`
  - 昨日涨停池/连板/炸板率：
- L5 衍生品 Z值：`=this.l5_derivatives_z`
  - PCR/IV/基差/Skew：

## 隔夜外盘

| 市场 | 指数 | 涨跌 | 信号 |
|------|------|------|------|
| 美股 | | | |
| 日经 | | | |
| 恒生 | | | |
| 美债10Y | | | |
| 美元指数 | | | |
| 黄金/原油 | | | |

## 今日关注板块

| 板块 | 方向 | 理由 | 涨停预期 |
|------|------|------|---------|
| | | | |

## 仓位建议

> **`=this.position_label`** → 仓位 `=this.position_range`

## ⚠️ 对抗性分析

> 如果当前判断是错的，最可能因为：
> 1. [填写]
> 2. [填写]
> 3. [填写]

## 熔断状态

Level `=this.circuit_breaker_level` `=this.circuit_breaker_level == 0 ? "正常" : "⚠️ 已触发"`

---
> 评分引擎：`_data/db/sentiment_engine.py` | 配置：`_data/db/framework_config.json`
> 关联评分：[[scores/<% tp.date.now("YYYY-MM-DD") %>_score|今日情绪评分]]
