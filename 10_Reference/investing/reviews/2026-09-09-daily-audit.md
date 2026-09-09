---
type: audit
audit_date: 2026-09-09
auditor: daily-audit-script
scope: 全量
findings_count: 91
critical: 2
high: 77
medium: 14
low: 15
status: 已完成
created: 2026-09-09
---

# 每日审查报告：2026-09-09

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2511 |
| stub 实体 | 15 |
| LLM 生成内容 | 0 |
| 占位符残留 | 0 |
| 断链 | 77 |
| 孤立实体 | 14 |
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
| 打板因子集索引 | 10 |
| 龙头战法 | 5 |
| 炸板回封 | 4 |
| 弱转强接力 | 3 |
| 一字竞价选股法 | 3 |
| 连板接力 | 2 |
| 低吸龙头 | 2 |
| 暴风雨逆势涨停 | 2 |
| 平台突破 | 2 |
| 尾盘偷袭 | 2 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| events | ['events/2026-09-08-龙虎榜衍生品'] |
| metrics | ['metrics/打板_竞价量能', 'metrics/打板_题材热度', 'metrics/打板_量比换手', 'metrics/打板_封单强度比', 'metrics/打板_封板时间', 'metrics/打板_连板位置', 'metrics/打板_炸板回封', 'metrics/打板_情绪周期', 'metrics/打板_涨跌停规则', 'metrics/打板_OFI盘口'] |
| specs | ['specs/Vibe-Research项目', 'specs/a-Plate-Sentinel项目'] |
| strategies | ['strategies/打板因子集索引'] |

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
| 断链 | 77 | ≤50 | 🔴 |
| 孤立实体 | 14 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |
| 链接残片(H_Reference) | 64 | =0 | 🔴 |
| 缺 frontmatter | 0 | =0 | 🟢 |
| markdown链接损坏 | 0 | =0 | 🟢 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
