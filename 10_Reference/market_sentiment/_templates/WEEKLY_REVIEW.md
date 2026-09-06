---
title: "周复盘"
date: {{date:YYYY-MM-DD}}
type: weekly_review
tags: [sentiment, review, weekly]
period: "{{date:YYYY-MM-DD minus 7 days}} ~ {{date:YYYY-MM-DD minus 1 days}}"
week_avg_temp_z: 0
week_avg_confidence: 0
week_signal_accuracy: 0
circuit_breaker_triggers: 0
---

# 📊 周复盘 · {{date:YYYY-MM-DD}}

> 复盘周期：`=this.period`
> 本周均温Z：`=this.week_avg_temp_z` | 均置信度：`=this.week_avg_confidence` | 信号准确率：`=this.week_signal_accuracy` | 熔断触发：`=this.circuit_breaker_triggers`次

---

## 一、本周情绪走势

```dataview
TABLE
  temperature_z AS "温度Z",
  direction AS "方向",
  confidence AS "置信度",
  position_label AS "仓位建议",
  circuit_breaker_level AS "熔断"
FROM "10_Reference/market_sentiment/scores"
WHERE date >= date(today) - dur(7 days)
SORT date ASC
```

### 温度Z折线图

```dataviewjs
const scores = dv.pages('"10_Reference/market_sentiment/scores"')
  .where(p => p.date)
  .sort(p => p.date, 'asc');

const labels = scores.map(p => p.date);
const tempZ = scores.map(p => p.temperature_z || 0);
const velocityDz = scores.map(p => p.velocity_dz || 0);
const divergenceD = scores.map(p => p.divergence_d || 0);

const canvas = dv.container.appendChild(Object.assign(document.createElement('canvas'), {
  style: 'width:100%;max-width:700px;margin:1rem auto;'
}));

new Chart(canvas, {
  type: 'line',
  data: {
    labels,
    datasets: [
      { label: '🌡️ 温度Z', data: tempZ, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true, tension: 0.3 },
      { label: '📈 速率ΔZ', data: velocityDz, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', fill: false, tension: 0.3 },
      { label: '🔀 背离度D', data: divergenceD, borderColor: '#eab308', backgroundColor: 'rgba(234,179,8,0.1)', fill: false, tension: 0.3 }
    ]
  },
  options: {
    scales: { y: { min: -3, max: 3 } },
    plugins: { legend: { display: true } }
  }
});
```

### 方向分布

| 方向 | 天数 | 占比 |
|------|------|------|
| 🟢 bullish | | |
| 🟡 neutral | | |
| 🔴 bearish | | |

---

## 二、6层信号准确率

| 层级 | 预测方向 | 正确次数 | 错误次数 | 准确率 | 最大连错 |
|------|---------|---------|---------|--------|---------|
| L0 宏观 | | | | | |
| L1 政策 | | | | | |
| L2 机构 | | | | | |
| L3 资金 | | | | | |
| L4 情绪 | | | | | |
| L5 衍生品 | | | | | |
| **综合** | | | | | |

> 参考基准：平安7信号月胜率75%，华泰7维度情绪指数绝对收益97%

### 熔断触发记录

| 日期 | 级别 | 触发原因 | 持续时间 | 恢复方式 |
|------|------|---------|---------|---------|
| | | | | |

---

## 三、各层Z值周分布

### L0 宏观周期

| 日期 | PMI Z | CPI Z | PPI Z | 社融 Z | M1M2 Z | DR007 Z | 层级Z |
|------|-------|-------|-------|--------|--------|---------|-------|
| | | | | | | | |

**趋势观察：** 

### L1 政策监管

| 日期 | 政策事件 | 影响分 | 层级Z |
|------|---------|--------|-------|
| | | | |

### L2 机构动向

| 日期 | 机构净买(亿) | 游资净买(亿) | 分歧度 | 层级Z |
|------|-------------|-------------|--------|-------|
| | | | | |

### L3 资金面

| 日期 | 成交额(亿) | 量比 | 北向(亿) | 层级Z |
|------|-----------|------|---------|-------|
| | | | | |

### L4 市场情绪

| 日期 | 涨停数 | 连板最高 | 炸板率 | 层级Z |
|------|--------|---------|--------|-------|
| | | | | |

### L5 衍生品

| 日期 | PCR | IV | 基差 | 层级Z |
|------|-----|-----|------|-------|
| | | | | |

---

## 四、仓位管控有效性

| 日期 | 方向 | 建议仓位 | 实操作位 | 是否违规 | 违规原因 |
|------|------|---------|---------|---------|---------|
| | | | | | |

> 违规 = 实际仓位超出建议区间上限

**本周三重护栏触发统计：**

| 护栏 | 触发天数 |
|------|---------|
| Z在[-0.5,0.5] | |
| 成交额低于均值 | |
| 机构净卖出 | |
| **三重全触发** | |

---

## 五、对抗性分析回顾

> 本周哪些"如果判断错了"的假设实际发生了？

| 日期 | 原判断 | 对抗假设 | 实际发生？ | 教训 |
|------|--------|---------|-----------|------|
| | | | | |

---

## 六、板块情绪周报

| 板块 | 周涨停 | 周跌停 | 情绪方向 | L4 Z | 持续性 |
|------|--------|--------|---------|------|--------|
| | | | | | |

---

## 七、下周展望

### L0 宏观日历

| 日期 | 事件 | 预期影响 |
|------|------|---------|
| | | |

### 关键变量

- 
- 
- 

### 仓位策略预判

- 下周建议仓位区间：
- 重点关注板块：
- 需要警惕的信号：

---

## 八、框架改进

- [ ] 
- [ ] 
- [ ] 

---
> 本周生成时间：{{date:YYYY-MM-DD HH:mm}}  
> 框架版本：v2.0（6层稳健z-score）  
> 关联：[[_README|框架说明]] | [[DASHBOARD|仪表盘]]
