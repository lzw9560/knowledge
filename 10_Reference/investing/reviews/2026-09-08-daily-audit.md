---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 22
critical: 0
high: 19
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
| 断链 | 19 |
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
| data-sources/同花顺 THS（一致预期·涨停揭秘）（LLM 服务） | 2 |
| [[10_Reference/tech-learning/concepts/限流 — 共用 em_get QPS≤2 限流 | 2 |
| [[10_Reference/tech-learning/concepts/限流 — 共用 em_get QPS≤2 限流防封 | 2 |
| specs/a-Plate-Sentinel项目 — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架阶段） | 1 |
| [[10_Reference/tech-learning/concepts/限流 — stale-run 堵塞的根因之一是限流队列积压 | 1 |
| specs/Vibe-Research项目 — Vibe-Research 个人 AI 投研看板（本图谱主体，109 spec + 16 数据源 + 12 战法） | 1 |
| specs/a-Plate-Sentinel项目 — A股打板情绪监控与投研决策看板（8 大模块，Tushare 数据源，MVP 骨架） | 1 |
| actions/rename-entity | 1 |
| actions/promote-from-inbox | 1 |
| [[10_Reference/tech-learning/concepts/限流 — 光伏/风能/氢能多概念聚合，数据源限流防封 | 1 |

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
| 断链 | 19 | ≤50 | 🟢 |
| 孤立实体 | 3 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |
| 链接残片(H_Reference) | 64 | =0 | 🔴 |
| 缺 frontmatter | 0 | =0 | 🟢 |
| markdown链接损坏 | 0 | =0 | 🟢 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
