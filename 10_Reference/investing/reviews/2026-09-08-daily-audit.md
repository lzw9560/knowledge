---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 41
critical: 0
high: 4
medium: 37
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
| 断链 | 4 |
| 孤立实体 | 37 |
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
| actions/rename-entity | 1 |
| actions/promote-from-inbox | 1 |
| stocks/603228 | 1 |
| strategies/dragon_head | 1 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| actions | ['actions/源同步', 'actions/审批实体', 'actions/研报自动链接', 'actions/实体重命名'] |
| data-sources | ['data-sources/东财 reportapi（研报）', 'data-sources/108 RSS 源（资讯雷达）', 'data-sources/东财 push2', 'data-sources/东财 datacenter（龙虎榜·解禁·融资融券等）', 'data-sources/FRED（宏观）', 'data-sources/腾讯行情', 'data-sources/baostock（K线日更）', 'data-sources/百度股市通（日K线）', 'data-sources/worldmonitor（全球宏观 MCP）', 'data-sources/东财 searchapi（个股新闻）', 'data-sources/东财 push2ex（涨停四池）', 'data-sources/新浪财经（财报三表）', 'data-sources/同花顺 THS（一致预期·涨停揭秘）', 'data-sources/AkShare', 'data-sources/巨潮 cninfo（互动易）', 'data-sources/Tushare'] |
| events | ['events/2026-09-08-龙虎榜衍生品'] |
| specs | ['specs/每日股票分析项目', 'specs/TradingAgents项目', 'specs/a-Plate-Sentinel项目', 'specs/Vibe-Research项目'] |
| strategies | ['strategies/反包战法', 'strategies/龙头战法', 'strategies/尾盘偷袭', 'strategies/炸板回封', 'strategies/低吸龙头', 'strategies/首板挖掘', 'strategies/暴风雨逆势涨停', 'strategies/形态反包', 'strategies/平台突破', 'strategies/连板接力', 'strategies/弱转强接力', 'strategies/N字反击'] |

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
| 断链 | 4 | ≤50 | 🟢 |
| 孤立实体 | 37 | ≤200 | 🟢 |
| stub 实体 | 15 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 98% | ≥95% | 🟢 |
| 链接残片(H_Reference) | 0 | =0 | 🟢 |
| 缺 frontmatter | 0 | =0 | 🟢 |
| markdown链接损坏 | 7 | =0 | 🟡 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
