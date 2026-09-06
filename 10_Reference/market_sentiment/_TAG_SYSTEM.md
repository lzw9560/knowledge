---
title: "标签体系"
date: 2026-09-03
type: reference
tags: [sentiment, meta, tag-system]
---

# 标签体系

> 大A舆情预判框架 — 统一标签定义。所有页面在 frontmatter 中使用以下标签。

---

## 情绪状态（sentiment/state/）

```yaml
sentiment/state/green     # 主升浪 — 赚钱效应极强，敢于重仓
sentiment/state/yellow    # 震荡分歧 — 有局部亏钱效应，控制仓位
sentiment/state/red       # 退潮期 — 亏钱效应爆炸，强制防守
```

## 情绪方向（sentiment/direction/）

```yaml
sentiment/direction/up       # 情绪升温
sentiment/direction/stable   # 情绪平稳
sentiment/direction/down     # 情绪降温
```

## 时间段（period/）

```yaml
period/morning   # 盘前
period/midday    # 盘中
period/evening   # 盘后
```

## 信号类型（signal/）

```yaml
signal/weak_to_strong     # 弱转强接力
signal/cover              # 形态反包
signal/limit_up           # 涨停
signal/break_limit        # 炸板
signal/dragon_tiger       # 龙虎榜
signal/anomaly            # 异动监控
```

## 板块（sector/）

```yaml
sector/finance     # 金融
sector/tech        # 科技
sector/consumer    # 消费
sector/new_energy  # 新能源
sector/biotech     # 生物医药
sector/defense     # 军工
sector/culture     # 文化传媒
sector/materials   # 周期材料
sector/others      # 其他
```

> 板块标签与 `quant-limit-up` 项目保持一致，标签值可直接迁移。

## 来源类型（source/）

```yaml
source/akshare     # AkShare 自动采集
source/eastmoney   # 东方财富
source/manual      # 人工录入
source/script      # 脚本生成
source/policy      # 政策文件
```

## 文件类型（type/）

```yaml
type/daily_pre      # 盘前情绪报告
type/daily_mid      # 盘中情绪记录
type/daily_post     # 盘后复盘报告
type/score          # 情绪评分
type/policy         # 政策摘要
type/sentiment      # 舆情热度记录
type/weekly_review  # 周复盘
type/anomaly        # 异动监控记录
type/backtest       # 回测数据
```

---

## 标签组合惯例

```yaml
# 盘前情绪报告
type/daily_pre, period/morning, sentiment/state/yellow

# 弱转强信号日
sentiment/state/green, signal/weak_to_strong, sector/tech

# 退潮期政策压制
sentiment/state/red, source/policy
```
