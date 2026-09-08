---
type: logic
rule_id: STUB-LIFECYCLE-001
rule_type: 状态机
target_entity: 全类型
severity: low
condition: "stub 实体（status: stub）→ 填充关键字段 → 转 status: active"
action_on_violation: stub 滞留 > 30 天未填充 → 标 stub_stale；stub 直接当 active 用 → 报 medium
source: ora-3 §1.3（inbox stub 通道）+ AGENTS.md 工程底线（不臆造数据——stub 是占位非成品）
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`STUB-LIFECYCLE-001`  **类型**：状态机
> **严重级**：low  **适用实体**：全类型
>
> **违反处置**：`stub 滞留 > 30 天未填充 → 标 stub_stale；stub 直接当 active 用 → 报 medium`

## 📋 规则定义

- **类型**：`状态机`
- **适用实体**：全类型（frontmatter 含 `status: stub` 的占位实体）
- **严重级**：`low`
- **条件**：`status: stub` 的实体需经填充流转到 `status: active`

## ⚡ 触发条件

stub 实体的状态流转三阶段：
1. **创建**：从 inbox 晋级或从断链补建时，若关键信息不全，先建 stub（`status: stub`）
2. **填充**：补全关键字段（code/name/title 等）+ 建立至少 1 个入边
3. **转正**：关键字段齐全 + 有入边 → `status: stub` 改 `status: active`

stub 是"计划中待数据源补充的占位"，允许：
- 字段不完整（schema_infer 跳过 stub，不报缺字段）
- 无入边（orphan_check 跳过 stub，不报孤立）

## 🔧 执行逻辑

```
对每个 status: stub 的实体：
  age = today - parse(fm.created)
  if age > 30:
    fm.status = "stub_stale"  # 滞留告警
    # 但不强制删除（stub 是占位，待数据源补充）

  # 转正判定
  if 关键字段齐全(code/name/title) AND inbound_count > 0:
    fm.status = "active"
    记录转正日志
```

关键：`vault_audit.py` 的 `schema_infer` 和 `orphan_check` 已对 `status: stub` 豁免（见脚本 check_orphan / check_schema），避免把占位误报为缺陷。

Dataview 查询（stub 实体待数据源补充）：

<!-- dataview-precompiled:0ed4a442adb5 query:VEFCTEUK57G75Z6LIEFTICLnsbvlnosiLAogIOeKtuaAgSBBUyAi54q25oCBIiwKICDliJvlu7rml6UgQVMgIuWIm+W7uuaXpSIKRlJPTSAiMTBfUmVmZXJlbmNlL2ludmVzdGluZy9sb2dpYyIKV0hFUkUgdHlwZSA9ICJsb2dpYyIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 类型 | 状态 | 创建日 |
|---|---|---|---|
| [[10_Reference/investing/logic/LLM抽取质量门]] | — | — | — |
| [[10_Reference/investing/logic/PE异常]] | — | — | — |
| [[10_Reference/investing/logic/stub生命周期]] | — | — | — |
| [[10_Reference/investing/logic/关系基数]] | — | — | — |
| [[10_Reference/investing/logic/去重合并]] | — | — | — |
| [[10_Reference/investing/logic/因果链]] | — | — | — |
| [[10_Reference/investing/logic/孤立阈值]] | — | — | — |
| [[10_Reference/investing/logic/实体合并]] | — | — | — |
| [[10_Reference/investing/logic/实体归档]] | — | — | — |
| [[10_Reference/investing/logic/实体改名]] | — | — | — |
| [[10_Reference/investing/logic/实体晋级]] | — | — | — |
| [[10_Reference/investing/logic/实体生命周期]] | — | — | — |
| [[10_Reference/investing/logic/情绪天气映射]] | — | — | — |
| [[10_Reference/investing/logic/战法卡漂移检测]] | — | — | — |
| [[10_Reference/investing/logic/战法天气映射]] | — | — | — |
| [[10_Reference/investing/logic/报告图谱关联]] | — | — | — |
| [[10_Reference/investing/logic/数据新鲜度]] | — | — | — |
| [[10_Reference/investing/logic/断链分级]] | — | — | — |
| [[10_Reference/investing/logic/断链告警]] | — | — | — |
| [[10_Reference/investing/logic/源漂移]] | — | — | — |
| [[10_Reference/investing/logic/置信度衰减]] | — | — | — |
| [[10_Reference/investing/logic/覆盖底线]] | — | — | — |
| [[10_Reference/investing/logic/跨域门控]] | — | — | — |
| [[10_Reference/investing/logic/静态值禁令]] | — | — | — |
<!-- /dataview-precompiled -->

## ⚠️ 违反处置

| 违反 | 严重级 | 处置 |
|---|---|---|
| stub 滞留 > 30 天未填充 | low | 标 stub_stale，提示补数据或归档 |
| stub 当 active 用于决策 | medium | 拦截 + 标 data_suspect |
| stub 缺关键字段被报 schema 违反 | low | 已豁免（stub 跳过 schema_infer） |
| stub 无入边被报 orphan | low | 已豁免（stub 跳过 orphan_check） |
| stub 被直接删 | high | 从 git 恢复 + 走 entity-archive 归档 |

## 🔗 关联

- **触发动作**：[[10_Reference/investing/actions/index|actions/]]
- **前置规则**[[10_Reference/investing/logic/实体生命周期]]（生命周期：inbox → stub → active → archive）
- **相关规则**[[10_Reference/investing/logic/实体晋级]]（inbox 晋级，stub 是晋级后的可能形态）
- **相关规则**[[10_Reference/investing/logic/实体归档]]（stub 长期不填充可归档）
- **约束实体**：[[10_Reference/investing/stocks/index|stocks/]] [[10_Reference/investing/industries/index|industries/]] [[10_Reference/investing/concepts/index|concepts/]]
- **来源决策**：[[10_Reference/investing/specs/index|specs/]]
- **出链**：24 个 · **入链**：2 个
