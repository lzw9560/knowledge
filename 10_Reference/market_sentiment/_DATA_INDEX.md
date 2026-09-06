---
title: "市场情绪数据索引"
date: 2026-09-03
type: reference
tags: [sentiment, meta, data-index]
---

# 原始数据索引

> `_data/` 目录下结构化数据的总索引，供程序读写，Dataview 可关联查询。
> 框架版本：v2.0（6层稳健z-score）

---

## 数据库总览

**主数据库**：`_data/db/sentiment.db`（SQLite）

| 表名 | 层级 | 用途 | 记录数 | 采集脚本 |
|------|------|------|--------|---------|
| `macro_indicators` | L0 | 宏观经济指标 | 1150+ | collect_macro.py + collect_macro_extra.py |
| `policy_events` | L1 | 政策事件 | 16 | collect_policy.py |
| `institution_flow` | L2 | 机构动向 | 建设中 | collect_institution.py |
| `capital_flow` | L3 | 资金面 | 建设中 | collect_capital.py |
| `market_snapshot` | 综合 | 日度综合快照 | 1 | sentiment_engine.py |
| `signal_log` | 全层 | 信号历史记录 | 累积中 | sentiment_engine.py |
| `derivatives_data` | L5 | 衍生品数据 | 1 | collect_derivatives.py |
| `limit_up_pool` | L4 | 涨停池 | 已有 | collect_sentiment.py |

---

## 采集脚本索引

| 脚本 | 层级 | 信号 | 数据源 | 更新频率 |
|------|------|------|--------|---------|
| `collect_macro.py` | L0 | CPI/PPI/PMI | 东方财富API | 月频 |
| `collect_macro_extra.py` | L0 | 社融/M1M2/DR007 | 东方财富API | 月频/日频 |
| `collect_policy.py` | L1 | 央行操作/监管政策/资本市场改革 | 东方财富API+搜索 | 事件驱动 |
| `collect_institution.py` | L2 | 龙虎榜/融资融券/大宗交易/回购 | 东方财富API+hithink | 日频(T+1) |
| `collect_capital.py` | L3 | 北向/主力/成交额/ETF/CDS | 东方财富API+搜索 | 日频 |
| `collect_sentiment.py` | L4 | 涨停池/炸板/连板/热榜 | hithink CLI | 日频 |
| `collect_derivatives.py` | L5 | PCR/IV/基差/Skew | 东方财富API | 日频 |
| `alert_monitor.py` | 全层 | 8项阈值告警 | DB查询 | 盘中每小时 |
| `sentiment_engine.py` | 综合 | 三维向量+熔断+仓位 | DB计算 | 日频 |
| `backtest.py` | 回测 | Walk-Forward Analysis | DB+模拟 | 按需 |

---

## JSON数据目录

| 子目录 | 格式 | 更新频率 | 保留策略 |
|--------|------|---------|---------|
| `lhb/` | JSON | 每日盘后 | 90天归档，gzip压缩 |
| `zt_pool/` | JSON | 每日盘后 | 90天归档，gzip压缩 |
| `backtest/` | JSON | 按需 | 按策略版本归档 |

---

## 龙虎榜数据（`lhb/`）

### 文件格式

```json
{
  "date": "2026-09-03",
  "source": "hithink-finance special dragon-tiger",
  "count": 50,
  "records": [
    {
      "code": "600519",
      "name": "贵州茅台",
      "seat_buy": ["中国国际金融上海分公司", "招商证券深圳招商证券大厦"],
      "seat_sell": ["机构专用"],
      "buy_amount_top5": 88000000,
      "sell_amount_top5": 45000000,
      "net_amount": 43000000,
      "reason": "涨幅偏离值达7%",
      "blacklist_hit": true,
      "blacklist_seats": ["中国国际金融上海分公司"],
      "blacklist_ratio": 0.18,
      "risk_flag": "REJECT"
    }
  ]
}
```

### Dataview 关联

情绪评分 frontmatter 可通过 `lhb_file` 字段关联对应日期数据文件：

```yaml
lhb_file: "_data/lhb/2026-09-03.json"
lhb_blacklist_hit: true
lhb_risk_flag: "REJECT"
```

---

## 涨停池 / 炸板池（`zt_pool/`）

### 文件格式

```json
{
  "date": "2026-09-03",
  "type": "zt_pool",
  "count": 65,
  "stocks": [
    {
      "code": "002415",
      "name": "海康威视",
      "price": 28.50,
      "change_pct": 10.04,
      "limit_up_days": 3,
      "lhb_reason": "连续三个交易日内收盘价格涨幅偏离值累计达到异常波动标准",
      "strategy_signal": "weak_to_strong",
      "seat_risk": "PASS"
    }
  ]
}
```

炸板池 `zb.json` 结构类似，`type` 字段改为 `"zb_pool"`，`zb_count` 字段替换 `zt_count`。

---

## 衍生品数据（`derivatives_data` 表）

### 表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | TEXT | 交易日 |
| hs300_pcr_volume | REAL | 沪深300期权PCR（成交量比） |
| hs300_pcr_position | REAL | 沪深300期权PCR（持仓量比） |
| hs300_iv_near | REAL | 近月IV（隐含波动率） |
| hs300_iv_far | REAL | 远月IV |
| hs300_iv_change | REAL | IV日变化 |
| hs300_skew_25d | REAL | 25Delta Skew |
| basis_if/if_ic/im_ih | REAL | 股指期货基差 |
| days_to_expiry | INTEGER | 距到期日天数 |
| expiry_week_flag | INTEGER | 是否到期周 |

---

## 回测数据（`backtest/`）

```json
{
  "date": "2026-09-03",
  "strategy": "weak_to_strong",
  "period": "2026-08-01 to 2026-08-31",
  "total_signals": 23,
  "win_rate": 0.652,
  "avg_profit_pct": 4.2,
  "max_drawdown_pct": -8.5,
  "sharpe_ratio": 1.34,
  "notes": "震荡分歧期胜率明显下降，红色期应暂停触发"
}
```

---

## 告警阈值配置

`alert_monitor.py` 检查的8项阈值：

| 信号 | 阈值 | 级别 |
|------|------|------|
| 涨停数 | >80 或 <20 | critical |
| 炸板率 | >30% | warning |
| 龙虎榜机构净卖出 | >20亿 | warning |
| DR007 | >3.0 或 <1.0 | critical |
| PMI | <49 或 >51 | warning |
| M1-M2剪刀差 | <-8% | warning |
| 沪深300基差 | <-30点 | critical |
| PCR | >1.3 或 <0.5 | warning |

---

> 数据采集遵循前视偏差防护：所有available_at时间戳不早于数据实际公开时间。
> 月频数据+15天lag，日频数据+0天lag（盘后数据次日才可用）。
