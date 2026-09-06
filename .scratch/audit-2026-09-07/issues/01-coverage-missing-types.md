# 01: coverage 完全缺失 11 类实体

severity: critical
status: needs-triage
source: 2026-09-06-ci-audit

## 问题描述

审查报告 §2 coverage 检查发现 11 类实体完全缺失（0 个实体，只有 index.md 空壳）：

- `logic`（本体构件 3）
- `event`（新闻/公告/涨停）
- `metric`（财务指标）
- `dragon_tiger`（龙虎榜席位）
- `inbox_item`（待审实体）
- `action`（本体构件 4）
- `report`（机构研报）
- `analyst`（研报作者）
- `index`（宽基/行业指数）
- `valuation`（估值快照）
- `audit`（审查报告实体）

这是 ora-3 诊断的"四构件缺 2"硬事实的直接体现——logic/ 和 actions/ 是本体第三、四构件，空壳意味着图谱的动态层缺失，校验/状态机/推断/自动化规则无处承载。

## 影响

- 图谱只有静态实体（stocks/industries/concepts），没有动态规则层 → 无法机器执行校验
- 战法卡的"适用天气"、报告的股票关联等跨子区逻辑无规则可依
- 审查脚本无法发现 schema 偏差以外的质量问题

## 修复建议

按 ora-3 诊断的分阶段路径：
1. **logic/ 构件**（本体 3）：先填实证规则。ora-3 诊断 D8-9 规划 6 条（inbox-promotion / stub-trigger / schema-body-fallback / broken-link-grading / source-drift / static-value-ban）。本 effort P0-6 已填 6 条规则（PE异常/战法天气映射/报告图谱关联/实体改名/LLM抽取质量门/战法卡漂移检测），与 ora-3 D8-9 清单有差异，需对齐。
2. **actions/ 构件**（本体 4）：ora-3 诊断 D10 规划 3 条（promote-from-inbox / weekly-audit / sync-from-source）。
3. **valuations/ + metrics/**：ora-3 诊断 §5 line 536 "先做 valuations（最易），MOC 已定义 Pydantic 契约 Valuation + ValuationPercentile，源仓有现成数据"。
4. **events/ + dragon_tiger/ + reports/ + analysts/**：依赖外部数据源接入，按 ora-3 诊断的 inbox 质量门流程灌入。
5. **inbox/ + audit/**：质量门基础设施，ora-3 诊断 §1.3 已规划 stub 机制。

## 关联

- 审查报告：`10_Reference/investing/reviews/2026-09-06-ci-audit.md` §2
- ora-3 诊断：`docs/knowledge-graph-improvement-vision.md`
- 本 effort P0-6 已填 logic/ 6 条规则（见 `10_Reference/investing/logic/`）
