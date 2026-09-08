---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 1
critical: 0
high: 1
medium: 0
low: 15
status: 已完成
created: 2026-09-08
---

# 每日审查报告：2026-09-08

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2498 |
| stub 实体 | 15 |
| LLM 生成内容 | 0 |
| 占位符残留 | 0 |
| 断链 | 1 |
| 孤立实体 | 0 |
| confidence 覆盖 | 2457/2498 (98%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| stock | 411 | metric | 401 |
| valuation | 401 | analyst | 396 |
| report | 392 | concept | 130 |
| industry | 126 | spec | 101 |
| dragon_tiger | 41 | logic | 24 |
| event | 20 | data_source | 17 |
| strategy | 13 | agent_role | 7 |
| index | 5 | decision | 5 |
| project | 4 | action | 4 |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| 链接 | 1 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|

## 🔍 占位符残留分布

| 类型 | 文件数 |
|---|---|
| (无) | 0 |

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 1430 |
| medium | 1027 |
| (未标注) | 41 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 1 | ≤50 | 🟢 |
| 孤立实体 | 0 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
