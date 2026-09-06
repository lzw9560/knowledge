# 打板工作流 · 盘前简报

## 页面地图

| 路由 | 页面 | 职责 |
|---|---|---|
| `/workflow` | Workflow.tsx | 工作流首页：盘前/盘中/盘后三阶段卡 |
| `/workflow/pre-market` | PreMarketBriefing.tsx | 盘前简报，纵向五段流 |
| `/candidates` | Candidates.tsx | 候选池主页 |
| `/workflow/candidates/:code` | CandidateDetail.tsx | 个股诊断卡 |
| `/workflow/topology` | Topology.tsx | 关系网/漏斗流程/连板梯队 |

## 盘前简报端到端数据流

```
GET /api/workflow/pre-market?date=
  ├─ 内存缓存 → 直接返回
  ├─ 快照文件 → done + from_snapshot=true
  ├─ 最近交易日 → idle（前端自动 POST refresh）
  └─ 其余 → no_snapshot

POST /api/workflow/pre-market/refresh
  _collect():
    ① factor_registry.afetch_all(date)  并行: limitup_screener + candidate_funnel
    ② _fetch_market_emotion(date)       ← 当前恒返 {}
    ③ _build_funnel_layers(date)        run_funnel 全跑
    ④ _save_snapshot()                  按日落盘
```

## 前端五段渲染

| 段 | 组件 | 数据 |
|---|---|---|
| ① 市场情绪 | GlassCard×2 | 综合评分 + 情绪阶段 |
| ② 涨停基因因子漏斗 | FactorSection×N | LS-1/LS-2/LS-3 三层 |
| ③ 候选池漏斗 | CandidateFunnelEmbed | R1/R2/R3/SELF 四层 |
| ④ 战法胜率对比 | WinRateComparePanel | 60日回测数据 |
| ⑤ 个股抽屉 | Sheet → CandidateDetailPanel | 诊断卡 + 工作流状态 |

## 候选池漏斗 R1/R2/R3/SELF

| 层 | 名称 | 输入 | 过滤口径 |
|---|---|---|---|
| R1 | 宽源 | 涨停基因候选 + 连板梯队 | ST/退市等名称规则剔除 |
| R2 | 收敛 | R1 输出 | 换手 ≥ 冷档阈值；北向过滤 |
| R3 | 定稿 | R2 输出 | 竞价异动 OR 公告催化 OR 概念联动 |
| SELF | 自选 | watchlist | 无过滤，并行汇入 |

## 基因因子漏斗 LS-1/2/3

| 层 | 语义 |
|---|---|
| LS-1 打分 | 基因总分 ≥ GENE_QUALIFY_THRESHOLD（50） |
| LS-2 战法 | 8 大战法匹配 |
| LS-3 仓位 | 仓位建议 |

## 工作流状态机

七态：`pending → candidate → watching → monitoring → holding → settled`，旁路 `filtered`

- 盘前采集后自动落库 candidate/filtered
- 手动流转仅抽屉状态卡一处 UI
- settled 流转即结算（写 winrate.db）
- 回退已实现：watching → candidate 允许