---
type: audit
audit_date: 2026-09-11
auditor: daily-audit-script
scope: 全量
findings_count: 12
critical: 0
high: 11
medium: 1
low: 15
status: 已完成
created: 2026-09-11
---

# 每日审查报告：2026-09-11

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2511 |
| stub 实体 | 15 |
| LLM 生成内容 | 0 |
| 占位符残留 | 0 |
| 断链 | 11 |
| 孤立实体 | 1 |
| confidence 覆盖 | 2480/2511 (98%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| metric | 411 | stock | 411 |
| valuation | 401 | analyst | 396 |
| report | 392 | concept | 130 |
| industry | 126 | spec | 101 |
| dragon_tiger | 41 | logic | 24 |
| event | 22 | data_source | 17 |
| strategy | 13 | agent_role | 7 |
| index | 5 | decision | 5 |
| project | 4 | action | 4 |
| strategy_index | 1 |  |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| edge-in-intraday-not-selection | 1 |
| fund-flow-verdict-2026-09-09 | 1 |
| data-source-capabilities | 1 |
| selection-candidate-pool-intraday-paradigm | 1 |
| 打板_涨停状态 | 1 |
| 打板_超短持有 | 1 |
| 打板_盘口博弈 | 1 |
| specs/S167-盘中微结构数据累积 | 1 |
| specs/S168-批量接线12harness | 1 |
| specs/S160-底座重建 | 1 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| events | ['events/2026-09-08-龙虎榜衍生品'] |

## 🔍 占位符残留分布

| 类型 | 文件数 |
|---|---|
| (无) | 0 |

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 1433 |
| medium | 1045 |
| low | 2 |
| (未标注) | 31 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 11 | ≤50 | 🟢 |
| 孤立实体 | 1 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |
| 链接残片(H_Reference) | 64 | =0 | 🔴 |
| 缺 frontmatter | 0 | =0 | 🟢 |
| markdown链接损坏 | 0 | =0 | 🟢 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
