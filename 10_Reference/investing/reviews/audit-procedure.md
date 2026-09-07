---
type: procedure
name: 知识图谱季度审查流程
domain: 投研知识图谱治理
created: 2026-09-07
source: ora-3 §2.1（审查报告 → 可执行工单）+ §2.2（脚本降噪）+ AGENTS.md 审查闭环要求
---

# 知识图谱季度审查流程

> 定义季度审查的标准流程：跑 8 项检查 → 问题分类 + 修复优先级 → 审查报告 → 跟踪闭环。
> 这是周度 CI 自动审查的**季度深度复盘**——周度跑脚本 + 关闭工单，季度做方法论层面的体检。
>
> 关联：周度审查由 `.github/workflows/vault-audit.yml` 自动跑（每周日 02:00），产出 `reviews/YYYY-MM-DD-ci-audit.md`。季度审查在此之上加人工分析 + 修复决策。

## 1. 8 项检查（与 `scripts/vault_audit.py` 对齐）

| # | 检查项 | 严重级默认 | 含义 | 修复路径 |
|---|---|---|---|---|
| 1 | summary | — | 图谱摘要：实体总数 + 各类型分布 | 无（信息性） |
| 2 | coverage | critical/medium | 覆盖率：四构件核心类型（logic/action）为 0 → critical；其余类型为 0 → medium | 填充实体 / 标"待建"占位 |
| 3 | orphan_check | medium | 孤立实体：零入边零出边的实体 | 加链接 or 归档 |
| 4 | broken_link | high/medium/low | 断链：三级分流（未导入悬空=low / 目录未建=medium / 真错链=high） | 导入实体 / 建目录 / 修链接 |
| 5 | schema_infer | high/low | schema 偏差：frontmatter 缺字段但正文有对应 H2 → low(body_only)；两者都无 → high | 提字段到 frontmatter / 补字段 |
| 6 | relation_density | low | 关系密度：hub 入边异常多（排除 index.md/MOC.md/README.md） | 拆分枢纽 |
| 7 | orphan_threshold | low | 孤立阈值：入边 < 阈值的实体 | 加链接 |
| 8 | stale_check | low | 过期：git log 90+ 天未更新 | 验证 + 更新 / 归档 |

> 第 9 项 source_drift（战法卡漂移检测，ora-3 §2.3）待落地——比对 vault frontmatter 的 `source_sha` 与源仓 `git rev-parse HEAD`。

## 2. 问题分类 + 修复优先级

### 严重级分类

| 级别 | 含义 | 处置时限 | 责任方 |
|---|---|---|---|
| **critical** | 四构件核心类型（logic/action）为 0；或方法论结构缺陷 | 本季度内修 | 人工（写规则/动作） |
| **high** | 真错链；frontmatter + 正文都缺关键字段 | 本季度内修或进 spec | 人工修 |
| **medium** | 目录未建；orphan 实体；hub 入边过多 | 进 backlog | 人工 or 脚本 |
| **low** | 未导入悬空；body_only；stale 过期；入边少 | 知悉即可 | 按需 |

### 修复责任方分流

| 责任方 | 适用问题 | 示例 |
|---|---|---|
| **脚本修** | 脚本误报 / 可机械修复的 | 36 项 schema 误报（ora-3 §2.2a 已修） |
| **人工补** | 需要新建实体 / 修规则 / 修链接 | 补 logic 规则、补 inbox stub |
| **规则豁免** | 已知缺口，不算缺陷 | 未导入 spec 悬空（标 `not_imported`） |

## 3. 审查报告模板

每份季度审查报告结构（周度 CI 报告同构，但季度版加人工分析段）：

```markdown
---
type: audit
audit_date: YYYY-MM-DD
auditor: human-or-ci
scope: 全量 | 季度深度
findings_count: N
critical: N
high: N
medium: N
low: N
status: 进行中 | 已完成
created: YYYY-MM-DD
---

# 审查报告：YYYY-MM-DD

## 审查范围
- 范围：全量（10_Reference/investing/ 下所有 .md）
- 审查人：[人工 / ci-github-actions]
- 触发：[定时 / 手动 / 季度复盘]

## 8 项检查结果
### 1. summary（图谱摘要）
### 2. coverage（覆盖率）
### 3. orphan_check（孤立实体）
### 4. broken_link（断链）
### 5. schema_infer（schema 偏差）
### 6. relation_density（关系密度）
### 7. orphan_threshold（孤立阈值）
### 8. stale_check（过期）

## 本期关闭（ora-3 §2.1 要求）
- [x] 上期 critical N 项 → 已修复 M 项，剩 K 项进 spec
- [x] 上期 high N 项 → 脚本修 X 项 / 人工修 Y 项
- 说明：[关闭记录，无关闭 = 无效审查]

## 本期新增发现
[新发现的问题清单]

## 季度深度分析（仅季度版）
- 图谱健康度趋势：findings_count 环比 [上升/下降/持平]
- 四构件填充度：[N/4]
- 消费指标：daily/ 报告双链数 [N/份]、stocks 与热点重叠率 [N%]
- 方法论偏离：[是否有违反 MOC.md 自定原则的情况]

## 跟踪清单
- [ ] Critical 全部修复（N）
- [ ] High 修复或进 spec（N）→ 见 .scratch/kg-audit/map.md#high
- [ ] Medium 进 backlog（N）
- 下次审查日期：YYYY-MM-DD
```

## 4. 跟踪闭环（issue → 修复 → 验证）

> ora-3 §2.1：审查报告的 KPI 不是"检出多少"，是"**关闭多少 + 剩余多少**"。

### 闭环流程

```
1. 跑审查脚本
   scripts/vault_audit.py
   ↓ 产出
2. 生成工单
   critical/high 发现 → .scratch/kg-audit/issues/NN-<slug>.md
   ↓ 每条含
   发现类型 / 实体路径 / 修复动作 / 建议责任方（脚本修/人工补/规则豁免）
   ↓
3. 人工分派
   按 .scratch/kg-audit/map.md 领取工单
   ↓
4. 修复执行
   脚本修 → commit + 关闭工单
   人工补 → 新建实体 + commit + 关闭工单
   规则豁免 → 标 not_imported + 关闭工单
   ↓
5. 验证
   重跑 scripts/vault_audit.py，确认 findings_count 下降
   ↓
6. 周期复盘
   周日 CI 自动跑 → 产出本周报告
   季度末人工深度复盘 → 产出季度报告
```

### 工单文件结构（对齐 AGENTS.md `.scratch/` issue tracker）

```
.scratch/kg-audit/
├── issues/
│   ├── 01-broken-link-spec-s004.md
│   ├── 02-schema-missing-entry-conditions.md
│   └── ...
└── map.md  # 工单索引 + 状态（needs-triage / ready-for-agent / ready-for-human / wontfix）
```

### 工单模板

```markdown
# KG-AUDIT-NN: <slug>

- **发现类型**: broken_link / schema_infer / orphan / ...
- **实体路径**: stocks/600519.md
- **严重级**: critical / high / medium / low
- **修复动作**: [具体修复步骤]
- **建议责任方**: 脚本修 / 人工补 / 规则豁免
- **状态**: needs-triage → ready-for-agent → [已关闭]
- **来源**: reviews/2026-09-07-ci-audit.md §4.broken_link
```

## 5. 验收指标（季度）

| 指标 | 基线（Week 0） | 季度目标 |
|---|---|---|
| 审查报告 high 级发现数 | 101（含 36 误报） | < 15（真实问题） |
| 审查跟踪清单关闭率 | 0%（4/4 复选框空） | > 60% |
| 四构件填充度 | 2/4 | 4/4 |
| 空壳实体目录数 | 9 | ≤ 6 |
| `stocks/` 与盘前报告 Top 榜重叠率 | 0% | > 30% |
| `.entity-dictionary.json` | 不存在 | 存在且覆盖源仓 spec |
| 战法卡副本漂移风险 | 12/12 暴露 | 0（去副本化 + 检测） |

## 6. 纪律

1. **没有"本期关闭"段的审查 = 无效审查**（ora-3 §2.1）。即使本期无关闭，也要显式写"本期无关闭，原因：[...]"。
2. **不修脚本不闭环**（ora-3 §2.2）。脚本误报不关闭工单，先修脚本再关。
3. **季度审查必须有人工分析段**——脚本只统计"检出多少"，人要看"为什么这么多 + 怎么系统性降"。
4. **工单不跨季度滞留**——季度末未关闭的工单要么执行要么 wontfix，不留"待办"暗债。

## 关联

- 脚本：`scripts/vault_audit.py`（8 项检查 + 工单输出）
- 周度报告：`reviews/YYYY-MM-DD-ci-audit.md`（CI 自动生成）
- 工单目录：`.scratch/kg-audit/`（对齐 AGENTS.md issue tracker）
- 规则来源：[[logic/broken-link-grading]] / [[logic/source-drift]] / [[logic/static-value-ban]]
- 方法论：[[../../meta/four-construct-ontology]]（四构件填充度判定）
