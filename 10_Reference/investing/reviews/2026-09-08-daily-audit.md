---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 244
critical: 15
high: 244
medium: 0
low: 43
status: 已完成
created: 2026-09-08
---

# 每日审查报告：2026-09-08

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2490 |
| stub 实体 | 43 |
| LLM 生成内容 | 576 |
| 断链 | 244 |
| 孤立实体 | 0 |
| confidence 覆盖 | 2449/2490 (98%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| stock | 411 | metric | 401 |
| valuation | 401 | analyst | 396 |
| report | 392 | concept | 130 |
| industry | 126 | spec | 101 |
| dragon_tiger | 41 | logic | 24 |
| data_source | 17 | event | 13 |
| strategy | 12 | agent_role | 7 |
| index | 5 | decision | 5 |
| project | 4 | action | 4 |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| 10_Reference/tech-learning/concepts/graceful-degradation | 22 |
| 10_Reference/tech-learning/concepts/caching-strategy | 21 |
| 10_Reference/tech-learning/concepts/data-contract | 20 |
| 10_Reference/investing/MOC | 16 |
| 10_Reference/investing/reviews/index | 16 |
| 10_Reference/investing/inbox/index | 16 |
| 10_Reference/reading/notes/均值回归-笔记 | 16 |
| 10_Reference/reading/notes/趋势跟踪-笔记 | 14 |
| 10_Reference/tech-learning/architecture/layered-architecture | 12 |
| 10_Reference/tech-learning/concepts/circuit-breaker | 11 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 1422 |
| medium | 1027 |
| (未标注) | 41 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 244 | ≤50 | 🔴 |
| 孤立实体 | 0 | ≤200 | 🟢 |
| stub 实体 | 43 | ≤100 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |

## 📈 趋势

> 与上次审查对比（如有 reviews/ 前一份报告）

待填充（需要读前一份报告对比）
