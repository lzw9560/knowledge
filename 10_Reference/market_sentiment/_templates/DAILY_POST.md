---
title: "盘后复盘报告"
date: <% tp.date.now("YYYY-MM-DD") %>
type: daily_post
tags: [sentiment, post-market, daily]
trading_date: "<% tp.date.now("YYYY-MM-DD") %>"
# 预测验证
predicted_direction: neutral
actual_direction: 
prediction_correct: 
# 评分变化
morning_z: 0.0000
closing_z: 0.0000
z_change: 0.0000
# 市场数据
limit_up_count: 0
broken_count: 0
max_consecutive: 0
volume_ratio: 0.00
# 熔断检查
circuit_breaker_level: 0
---

# 🌙 盘后复盘报告 `<% tp.date.now("YYYY-MM-DD") %>`

## 预测验证

> 盘前预测：<!-- predicted_direction -->
> 实际走势：<!-- actual_direction -->
> 预测准确：<!-- prediction_correct -->

| 维度 | 盘前 | 盘后 | 变化 |
|------|------|------|------|
| 温度 Z | <!-- morning_z --> | <!-- closing_z --> | <!-- z_change --> |

## 大盘概况

| 指数 | 收盘 | 涨跌 | 信号 |
|------|------|------|------|
| 上证指数 | | | |
| 创业板指 | | | |
| 科创50 | | | |

## 涨停池分析

| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 涨停数 | <!-- limit_up_count --> | | |
| 炸板数 | <!-- broken_count --> | | |
| 最高连板 | <!-- max_consecutive -->板 | | |
| 量能比 | <!-- volume_ratio --> | | |

连板天梯：

## 六层信号复盘

| 层级 | 今日Z | 方向 | 评价 |
|------|-------|------|------|
| L0 宏观周期 | | | |
| L1 政策监管 | | | |
| L2 机构动向 | | | |
| L3 资金面 | | | |
| L4 市场情绪 | | | |
| L5 衍生品 | | | |

## 信号准确率追踪

| 信号 | 预测方向 | 实际方向 | 正确 | 备注 |
|------|---------|---------|------|------|
| | | | | |

## 明日展望

- 战略方向：
- 战术信号：
- 仓位建议：

## 信号衰减检查

- 今日信号衰减率：
- 连续误判次数：<!-- circuit_breaker_level -->
- 是否需要降权：

---
> 关联盘前：[[daily/<% tp.date.now("YYYY-MM-DD") %>_pre|盘前报告]]
> 关联评分：[[scores/<% tp.date.now("YYYY-MM-DD") %>_score|情绪评分]]
> 框架是决策辅助，不是决策者。
