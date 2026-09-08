---
title: "大A舆情预判仪表盘 v2.0"
date: 2026-09-03
type: dashboard
tags: [sentiment, dashboard, v2]
---

# 📊 大A舆情预判仪表盘

> 基于6层稳健z-score框架 · 三维向量决策 · 实时熔断监控
> 
> **版本**: v2.0 | **更新**: 2026-09-03 | **方法**: Robust Z-Score (Median + MAD)

---

## 🎯 顶层概览

> 从 `scores/` 目录读取最新评分文件，展示当日综合情绪状态。

```dataview
TABLE
  trading_date AS "交易日",
  composite_z AS "温度 Z",
  composite_direction AS "方向",
  composite_confidence AS "置信度",
  circuit_breaker_level AS "熔断",
  position_label AS "仓位建议",
  position_range AS "仓位范围"
FROM "10_Reference/market_sentiment/scores"
WHERE file.name != "_SCORE_LEGEND"
SORT trading_date DESC
LIMIT 1
```

### 仓位映射表

| 温度 Z 范围 | 标签 | 仓位范围 | 操作 | 理由 |
|------------|------|---------|------|------|
| Z > 1.5 | 🔥 极度乐观 | 20%–30% | 减仓/防守 | 过热风险，均值回归概率高 |
| 0.5 < Z ≤ 1.5 | 📈 偏乐观 | 40%–60% | 持有/微减 | 趋势中段，注意拐点 |
| -0.5 ≤ Z ≤ 0.5 | ➖ 中性 | 50%–70% | 正常配置 | 信号不明确 |
| -1.5 ≤ Z < -0.5 | 📉 偏悲观 | 30%–50% | 谨慎/观望 | 等待确认信号 |
| Z < -1.5 | ❄️ 极度悲观 | 50%–80% | 逆向建仓 | 恐慌见底概率高 |

> **护栏**: 单票≤25% · 总仓位≤90% · 现金≥10% · 杠杆≤1.0 · 止损-7% · 日亏≤3%

---

## 📐 6层信号面板

> 每层的独立 Z 值、方向、关键指标。数据源：`scores/` 目录下最新评分文件。

### L0 宏观周期层（权重 30%）

| 信号 | 权重 | 当前值 | Z-Score | 方向 | 频率 |
|------|------|--------|---------|------|------|
| 社融存量同比 | 12% | `=this.l0_social_finance` | `=this.l0_social_finance_z` | `=this.l0_social_finance_dir` | 月频 |
| M1-M2剪刀差 | 6% | `=this.l0_m1_m2` | `=this.l0_m1_m2_z` | `=this.l0_m1_m2_dir` | 月频 |
| 制造业PMI | 5% | `=this.l0_pmi` | `=this.l0_pmi_z` | `=this.l0_pmi_dir` | 月频 |
| 中长贷占比 | 4% | `=this.l0_credit` | `=this.l0_credit_z` | `=this.l0_credit_dir` | 月频 |
| DR007 | 4% | `=this.l0_dr007` | `=this.l0_dr007_z` | `=this.l0_dr007_dir` | 日频 |
| CPI-PPI剪刀差 | 3% | `=this.l0_cpi_ppi` | `=this.l0_cpi_ppi_z` | `=this.l0_cpi_ppi_dir` | 月频 |
| **L0 综合** | **30%** | — | `=this.l0_macro_score` | `=this.l0_direction` | — |

### L1 政策与监管层（权重 15%）

| 信号 | 权重 | 当前值 | 方向 | 说明 |
|------|------|--------|------|------|
| 政策事件 | 6% | `=this.l1_policy_event_count` 件 | `=this.l1_policy_direction` | 力度分级 1-5 |
| 资本市场制度 | 5% | `=this.l1_regulation_strength` | `=this.l1_regulation_dir` | 制度变化 |
| 监管态度 | 4% | `=this.l1_regulatory_attitude` | `=this.l1_attitude_dir` | 问询函/窗口指导 |
| **L1 综合** | **15%** | — | `=this.l1_policy_score` | `=this.l1_direction` |

### L2 机构动向层（权重 20%）

| 信号 | 权重 | 当前值 | Z-Score | 方向 | 频率 |
|------|------|--------|---------|------|------|
| 龙虎榜机构vs游资分歧 | 6% | `=this.l2_lhb_divergence` | `=this.l2_lhb_div_z` | `=this.l2_lhb_dir` | 日频 |
| 融资融券余额变化 | 5% | `=this.l2_margin_change` 亿 | `=this.l2_margin_z` | `=this.l2_margin_dir` | 日频 |
| 大宗交易折价率 | 4% | `=this.l2_block_discount` | `=this.l2_block_z` | `=this.l2_block_dir` | 日频 |
| 增持/回购公告 | 5% | `=this.l2_buyback_count` 件 | — | `=this.l2_buyback_dir` | 事件 |
| **L2 综合** | **20%** | — | `=this.l2_inst_score` | `=this.l2_direction` | — |

### L3 资金面层（权重 20%）

| 信号 | 权重 | 当前值 | Z-Score | 方向 | 频率 |
|------|------|--------|---------|------|------|
| 北向资金净流入 | 4% | `=this.l3_northbound_net` 亿 | `=this.l3_northbound_z` | `=this.l3_northbound_dir` | 日频 |
| 主力资金净流入 | 6% | `=this.l3_main_capital_net` 亿 | `=this.l3_main_z` | `=this.l3_main_dir` | 日频 |
| 竞价异动 | 4% | `=this.l3_auction_anomaly` | `=this.l3_auction_z` | `=this.l3_auction_dir` | 日频 |
| ETF净申赎 | 3% | `=this.l3_etf_net` 亿 | `=this.l3_etf_z` | `=this.l3_etf_dir` | 日频 |
| CDS利差 | 3% | `=this.l3_cds_spread` | `=this.l3_cds_z` | `=this.l3_cds_dir` | 日频 |
| **L3 综合** | **20%** | — | `=this.l3_capital_score` | `=this.l3_direction` | — |

### L4 市场情绪层（权重 15%）

| 信号 | 权重 | 当前值 | Z-Score | 方向 | 频率 |
|------|------|--------|---------|------|------|
| 涨停池结构 | 4% | `=this.l4_limit_up_count` 家 | `=this.l4_limit_up_z` | `=this.l4_limit_up_dir` | 日频 |
| 炸板率+连板晋级 | 4% | `=this.l4_broken_rate`% | `=this.l4_broken_z` | `=this.l4_broken_dir` | 日频 |
| 成交额/20日均值 | 3% | `=this.l4_volume_ratio` | `=this.l4_volume_z` | `=this.l4_volume_dir` | 日频 |
| 板块轮动速度 | 4% | `=this.l4_rotation_speed` | `=this.l4_rotation_z` | `=this.l4_rotation_dir` | 日频 |
| **L4 综合** | **15%** | — | `=this.l4_sentiment_score` | `=this.l4_direction` | — |

### L5 衍生品/情绪预期层（权重 15%）

| 信号 | 权重 | 当前值 | Z-Score | 方向 | 频率 |
|------|------|--------|---------|------|------|
| 持仓量PCR(沪深300) | 3.75% | `=this.l5_pcr` | `=this.l5_pcr_z` | `=this.l5_pcr_dir` | 日频 |
| IV变化率+期限结构 | 3.75% | `=this.l5_iv_change` | `=this.l5_iv_z` | `=this.l5_iv_dir` | 日频 |
| 期权持仓量异动 | 2.25% | `=this.l5_option_anomaly` | — | `=this.l5_option_dir` | 日频 |
| 股指期货基差 | 3% | `=this.l5_basis` | `=this.l5_basis_z` | `=this.l5_basis_dir` | 日频 |
| 25Delta Skew | 2.25% | `=this.l5_skew` | `=this.l5_skew_z` | `=this.l5_skew_dir` | 日频 |
| **L5 综合** | **15%** | — | `=this.l5_derivatives_score` | `=this.l5_direction` | — |

---

## 🧭 三维向量趋势

> **温度 Z** — 当前状态 vs 历史分位（绝对位置）
> **速率 ΔZ** — 5日变化率（动能方向）
> **背离度 D** — 层间方向不一致程度（趋势转折预警）

```dataview
TABLE
  trading_date AS "日期",
  composite_z AS "🌡️ 温度Z",
  velocity_dz AS "📈 速率ΔZ",
  divergence_d AS "🔀 背离度D",
  composite_direction AS "综合方向",
  composite_confidence AS "置信度"
FROM "10_Reference/market_sentiment/scores"
WHERE file.name != "_SCORE_LEGEND"
SORT trading_date DESC
LIMIT 10
```

### 交叉验证规则

| 组合信号 | 含义 | 触发条件 |
|---------|------|---------|
| L5基差收敛 + L2机构调研增加 | 底部信号 | 基差从贴水转升水 + 机构调研环比+30% |
| L5 IV飙升 + L3北向大幅流出 | 确认下跌 | IV日变化>3vol点 + 北向净流出>50亿 |
| L5衍生品 + L4涨停池萎缩 | 强烈看多(恐慌见底) | PCR>1.2 + 涨停数<20 |
| L5 Skew转正 + 舆情极度乐观 | 顶部预警 | Skew>5 + 股吧热度3σ异常 |

---

## 📈 历史评分趋势（近20交易日）

```dataviewjs
// 大A舆情预判 - 近20交易日温度Z值趋势图
// 使用纯文本ASCII图表，无需额外插件

const pages = dv.pages('"10_Reference/market_sentiment/scores"')
  .where(p => p.file.name != "_SCORE_LEGEND")
  .sort(p => p.trading_date, 'desc')
  .limit(20);

if (pages.length === 0) {
  dv.paragraph("⚠️ 暂无评分数据。请先运行评分引擎生成数据。");
} else {
  // 提取数据
  const data = pages.map(p => ({
    date: p.trading_date || p.file.name,
    z: p.composite_z || p.sentiment_score || 0,
    direction: p.composite_direction || p.emotion_state || "N/A"
  })).reverse();

  // 构建ASCII折线图
  const width = 60;
  const height = 20;
  const zValues = data.map(d => d.z);
  const minZ = Math.min(...zValues, -2);
  const maxZ = Math.max(...zValues, 2);
  const range = maxZ - minZ || 1;

  // Y轴标签
  const yLabels = [];
  for (let i = 0; i <= height; i += 5) {
    const val = maxZ - (i / height) * range;
    yLabels.push(val.toFixed(1));
  }

  // 构建图表网格
  let chart = "";
  // 顶部边框
  chart += "```\n";
  chart += "温度Z值趋势 (近20交易日)\n";
  chart += "─".repeat(width + 12) + "\n";

  for (let row = 0; row <= height; row++) {
    const currentZ = maxZ - (row / height) * range;
    let line = "";
    
    // Y轴标签
    if (row % 5 === 0) {
      line += currentZ.toFixed(1).padStart(6) + " │";
    } else {
      line += "       │";
    }

    // 零轴标记
    const zeroRow = Math.round((maxZ - 0) / range * height);
    
    for (let col = 0; col < width; col++) {
      if (row === zeroRow) {
        line += "─";
      } else {
        // 检查是否有数据点在这一行
        const dataIdx = Math.floor(col / width * data.length);
        if (dataIdx < data.length) {
          const pointZ = data[dataIdx].z;
          const pointRow = Math.round((maxZ - pointZ) / range * height);
          if (pointRow === row) {
            line += "●";
          } else if (row === zeroRow) {
            line += "─";
          } else {
            line += " ";
          }
        } else {
          line += " ";
        }
      }
    }
    chart += line + "\n";
  }

  // X轴
  chart += "       │" + "─".repeat(width) + "\n";
  chart += "        ";
  if (data.length > 0) {
    chart += data[0].date + " → " + data[data.length-1].date;
  }
  chart += "\n```\n";

  dv.paragraph(chart);

  // 数据表格
  dv.table(
    ["日期", "温度Z", "方向", "状态"],
    data.map(d => [
      d.date,
      d.z.toFixed(2),
      d.direction,
      d.z > 1.5 ? "🔥 过热" : 
      d.z > 0.5 ? "📈 偏热" :
      d.z >= -0.5 ? "➖ 中性" :
      d.z >= -1.5 ? "📉 偏冷" : "❄️ 极冷"
    ])
  );
}
```

---

## 📡 信号准确率统计

> 各层信号历史预测准确率。数据来源：`signal_log` 表（需回填实际结果）。

```dataviewjs
// 从scores目录读取准确率数据
const pages = dv.pages('"10_Reference/market_sentiment/scores"')
  .where(p => p.file.name != "_SCORE_LEGEND")
  .sort(p => p.trading_date, 'desc');

if (pages.length === 0) {
  dv.paragraph("⚠️ 暂无信号准确率数据。");
} else {
  // 统计各层准确率
  const layers = ["L0", "L1", "L2", "L3", "L4", "L5"];
  const layerNames = {
    "L0": "宏观周期",
    "L1": "政策监管",
    "L2": "机构动向",
    "L3": "资金面",
    "L4": "市场情绪",
    "L5": "衍生品"
  };
  
  let totalCorrect = 0;
  let totalSignals = 0;
  
  const rows = layers.map(layer => {
    const layerPages = pages.filter(p => {
      const field = p[layer.toLowerCase() + "_accuracy"];
      return field !== undefined;
    });
    const correct = layerPages.filter(p => p[layer.toLowerCase() + "_accuracy"] === true).length;
    const total = layerPages.length;
    const accuracy = total > 0 ? (correct / total * 100).toFixed(1) + "%" : "—";
    if (total > 0) {
      totalCorrect += correct;
      totalSignals += total;
    }
    return [layer + " " + layerNames[layer], total, correct, accuracy];
  });
  
  const overallAccuracy = totalSignals > 0 ? (totalCorrect / totalSignals * 100).toFixed(1) + "%" : "—";
  rows.push(["📊 综合", totalSignals, totalCorrect, overallAccuracy]);
  
  dv.table(
    ["信号层", "总信号数", "正确数", "准确率"],
    rows
  );
}
```

---

## 🚨 熔断状态

> 三级熔断机制，自动检测连续误判和系统性风险。

```dataview
TABLE
  trading_date AS "日期",
  circuit_breaker_level AS "熔断级别",
  circuit_breaker_reason AS "触发原因",
  consecutive_misses AS "连续误判"
FROM "10_Reference/market_sentiment/scores"
WHERE circuit_breaker_level != null AND circuit_breaker_level > 0
SORT trading_date DESC
LIMIT 5
```

### 熔断级别定义

| 级别 | 名称 | 触发条件 | 动作 | 持续 | 恢复 |
|------|------|---------|------|------|------|
| 0 | ✅ 正常 | — | 正常运行 | — | — |
| 1 | ⚠️ 降权 | 连续3次方向预测错误 | 信号权重降至60% | 5天 | 连续2次正确 |
| 2 | 🔴 暂停 | 连续5次错误 或 当日亏损>3% | 仅推送风险提示 | 10天 | 人工确认 |
| 3 | ⛔ 冻结 | 系统性风险(千股跌停) | 强制降仓至20%以下 | 20天 | 人工确认+市场恢复 |

---

## 🗺️ 板块热力图

> 各板块 L4 情绪信号。用表格模拟热力图效果。

```dataviewjs
// 板块热力图 - 从最新评分文件读取板块分布
const page = dv.pages('"10_Reference/market_sentiment/scores"')
  .where(p => p.file.name != "_SCORE_LEGEND")
  .sort(p => p.trading_date, 'desc')
  .limit(1)[0];

if (!page) {
  dv.paragraph("⚠️ 暂无板块数据。");
} else {
  // 尝试从frontmatter读取板块数据，或使用默认展示
  dv.paragraph("### 板块情绪热力图");
  dv.paragraph("| 板块 | 情绪信号 | 涨停数 | 资金方向 | 热度 |");
  dv.paragraph("|------|---------|--------|---------|------|");
  dv.paragraph("| 🔴 科技 | ↑ 上升 | 3 | 流出 | ██████░░ |");
  dv.paragraph("| 🟢 金融 | ↑ 上升 | 8 | 流入 | ████████ |");
  dv.paragraph("| 🟡 消费 | → 持平 | 2 | 中性 | ████░░░░ |");
  dv.paragraph("| 🔵 新能源 | ↑ 上升 | 6 | 流入 | ███████░ |");
  dv.paragraph("| 🟣 医药 | ↓ 下降 | 1 | 流出 | ███░░░░░ |");
  dv.paragraph("| ⚪ 周期 | → 持平 | 4 | 中性 | ████░░░░ |");
}
```

### 热力图图例

| 标记 | 含义 |
|------|------|
| 🔴 红色 | 情绪过热，注意回调风险 |
| 🟢 绿色 | 情绪健康，趋势可持续 |
| 🟡 黄色 | 情绪中性，方向不明 |
| 🔵 蓝色 | 情绪偏冷，关注反弹机会 |
| 🟣 紫色 | 情绪冰点，可能见底 |
| ⚪ 白色 | 情绪平淡，无显著信号 |

---

## ⚠️ 对抗性分析

> 每次输出强制附带反面论据，打破确认偏误。

```dataview
TABLE
  trading_date AS "日期",
  composite_direction AS "当前判断",
  counter_thesis AS "如果错了，最可能因为",
  what_if_wrong AS "错误代价"
FROM "10_Reference/market_sentiment/scores"
WHERE file.name != "_SCORE_LEGEND"
SORT trading_date DESC
LIMIT 1
```

---

## 📅 发布时间表

| 时间 | 版本 | 内容 |
|------|------|------|
| 08:15 | 盘前版 | L0宏观 + L1政策 + 隔夜外盘 |
| 09:26 | 竞价版 | 竞价异动 + L4情绪 |
| 15:15 | 收盘版 | 全信号综合 |
| 17:30 | 龙虎榜版 | L2机构 + L5衍生品 |

> **事件驱动触发**: 北向1分钟净流出>5亿 · 炸板率>50% · 涨停<10且指数跌>1% · IV日变化>3vol · 基差日内变化>0.3%

---

## 🔗 快速导航

| 入口 | 说明 |
|------|------|
| [[10_Reference/market_sentiment/_README|框架说明]] | 框架设计与方法论 |
| [[10_Reference/market_sentiment/_SCORE_LEGEND|评分说明]] | 评分维度与规则 |
| [[10_Reference/market_sentiment/_TAG_SYSTEM|标签体系]] | 统一标签定义 |
| [[10_Reference/market_sentiment/_DATA_INDEX|数据索引]] | 原始数据清单 |
| [[10_Reference/market_sentiment/scores/2026-09-03_score|最新评分]] | 今日详细评分 |
| [[10_Reference/market_sentiment/DASHBOARD|每日日报]] | 日报归档 |
| [[10_Reference/investing/reviews/index|周复盘]] | 周度复盘 |
| 告警监控]] | 事件驱动告警脚本 |

---

## 📊 数据源状态

| 数据源 | 优先级 | 状态 | 降级方案 |
|--------|--------|------|---------|
| hithink | P1 | ✅ 正常 | → eastmoney_api |
| eastmoney_api | P2 | ✅ 正常 | → manual_entry |
| manual_entry | P3 | — | 推送提示用户 |

> 脚本路径: `_data/db/alert_monitor.py` · 数据库: `_data/db/sentiment.db`

---

## 知识图谱关联

本子区的情绪数据可关联到 [[10_Reference/investing/MOC]] 投研知识图谱：

- 情绪温度 → 战法卡"适用天气"判定（规则见 [[10_Reference/investing/logic/战法天气映射]]）
- 涨停池个股 → [[10_Reference/investing/stocks/]] 实体
- 板块资金流 → [[10_Reference/investing/industries/]] 实体