---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 1432
critical: 18
high: 1429
medium: 3
low: 15
status: 已完成
created: 2026-09-08
---

# 每日审查报告：2026-09-08

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2500 |
| stub 实体 | 15 |
| LLM 生成内容 | 0 |
| 占位符残留 | 0 |
| 断链 | 1429 |
| 孤立实体 | 3 |
| confidence 覆盖 | 2469/2500 (98%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| stock | 411 | metric | 401 |
| valuation | 401 | analyst | 396 |
| report | 392 | concept | 130 |
| industry | 126 | spec | 101 |
| dragon_tiger | 41 | logic | 24 |
| event | 22 | data_source | 17 |
| strategy | 13 | agent_role | 7 |
| index | 5 | decision | 5 |
| project | 4 | action | 4 |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| push2 | 677 |
| 腾讯行情 | 411 |
| 10_Reference/[[tech-learning/concepts/优雅降级 | 22 |
| 优雅降级 | 22 |
| 10_Reference/[[tech-learning/concepts/缓存策略 | 21 |
| 缓存策略 | 21 |
| 10_Reference/[[tech-learning/concepts/数据契约 | 20 |
| 数据契约 | 19 |
| 10_Reference/[[reading/notes/均值回归-笔记 | 16 |
| 10_Reference/[[reading/notes/趋势跟踪-笔记 | 15 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| events | ['events/2026-09-08-龙虎榜衍生品'] |
| specs | ['specs/Vibe-Research项目', 'specs/a-Plate-Sentinel项目'] |

## 🔍 占位符残留分布

| 类型 | 文件数 |
|---|---|
| (无) | 0 |

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 1432 |
| medium | 1037 |
| (未标注) | 31 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 1429 | ≤50 | 🔴 |
| 孤立实体 | 3 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |
| 链接残片(H_Reference) | 0 | =0 | 🟢 |
| 缺 frontmatter | 0 | =0 | 🟢 |
| markdown链接损坏 | 64 | =0 | 🟡 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
