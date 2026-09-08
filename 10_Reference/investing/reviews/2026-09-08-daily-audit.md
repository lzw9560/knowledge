---
type: audit
audit_date: 2026-09-08
auditor: daily-audit-script
scope: 全量
findings_count: 54
critical: 0
high: 2
medium: 52
low: 2
status: 已完成
created: 2026-09-08
---

# 每日审查报告：2026-09-08

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | 2498 |
| stub 实体 | 2 |
| LLM 生成内容 | 0 |
| 占位符残留 | 0 |
| 断链 | 2 |
| 孤立实体 | 52 |
| confidence 覆盖 | 1734/2498 (69%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
| unknown | 735 | metric | 401 |
| valuation | 401 | analyst | 396 |
| report | 392 | spec | 81 |
| concept | 28 | dragon_tiger | 12 |
| strategy | 11 | event | 11 |
| logic | 10 | agent_role | 7 |
| index | 5 | project | 3 |
| action | 3 | decision | 1 |
| industry | 1 |  |

## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
| actions/rename-entity | 1 |
| actions/promote-from-inbox | 1 |

## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
| actions | ['actions/研报自动链接', 'actions/审批实体', 'actions/实体重命名', 'actions/源同步'] |
| data-sources | ['data-sources/baostock（K线日更）', 'data-sources/worldmonitor（全球宏观 MCP）', 'data-sources/东财 reportapi（研报）', 'data-sources/108 RSS 源（资讯雷达）', 'data-sources/Tushare', 'data-sources/同花顺 THS（一致预期·涨停揭秘）', 'data-sources/东财 datacenter（龙虎榜·解禁·融资融券等）', 'data-sources/东财 push2', 'data-sources/AkShare', 'data-sources/FRED（宏观）', 'data-sources/腾讯行情', 'data-sources/巨潮 cninfo（互动易）', 'data-sources/东财 push2ex（涨停四池）', 'data-sources/东财 searchapi（个股新闻）', 'data-sources/百度股市通（日K线）', 'data-sources/新浪财经（财报三表）'] |
| logic | ['logic/断链告警', 'logic/断链分级', 'logic/关系基数', 'logic/实体归档', 'logic/数据新鲜度', 'logic/去重合并', 'logic/实体生命周期', 'logic/源漂移', 'logic/静态值禁令', 'logic/stub生命周期', 'logic/置信度衰减', 'logic/实体晋级', 'logic/跨域门控', 'logic/孤立阈值', 'logic/覆盖底线', 'logic/实体合并'] |
| specs | ['specs/a-Plate-Sentinel项目', 'specs/TradingAgents项目', 'specs/Vibe-Research项目', 'specs/每日股票分析项目'] |
| strategies | ['strategies/反包战法', 'strategies/弱转强接力', 'strategies/尾盘偷袭', 'strategies/低吸龙头', 'strategies/连板接力', 'strategies/龙头战法', 'strategies/暴风雨逆势涨停', 'strategies/炸板回封', 'strategies/首板挖掘', 'strategies/平台突破', 'strategies/N字反击', 'strategies/形态反包'] |

## 🔍 占位符残留分布

| 类型 | 文件数 |
|---|---|
| (无) | 0 |

## 📊 confidence 分布

| confidence | 数量 |
|---|---|
| high | 947 |
| medium | 787 |
| (未标注) | 764 |

## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | 2 | ≤50 | 🟢 |
| 孤立实体 | 52 | ≤200 | 🟢 |
| stub 实体 | 2 | ≤100 | 🟢 |
| 占位符残留 | 0 | ≤10 | 🟢 |
| confidence 覆盖 | 69% | ≥95% | 🟡 |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
