# 02: broken_link 断链 specs/SNNN 编号

severity: high
status: needs-triage
source: 2026-09-06-ci-audit

## 问题描述

审查报告 §4 broken_link 检查发现大量 `[[specs/SNNN]]` 链接指向不存在的 spec 文件。源文件主要是：

- `specs/DEC-001.md` → 断链 `[[specs/S004]]` `[[specs/S008]]` `[[specs/S031]]`
- `specs/DEC-002.md` → 断链 `[[specs/S018]]` `[[specs/S019]]`
- `specs/DEC-003.md` → 断链 `[[specs/S047]]` `[[specs/S066]]` `[[specs/S017]]` `[[specs/S042]]`
- `specs/DEC-004.md` → 断链 `[[specs/S064]]` `[[specs/S066]]` `[[specs/S042]]`
- `specs/DEC-005.md` → 断链 `[[specs/S075]]`
- `specs/S007-契约层.md` → 断链 `[[specs/S006]]` `[[specs/S008]]` `[[specs/S009]]`
- `specs/S008-后端数据层迁移.md` → 断链 `[[specs/S007]]` `[[specs/S013]]` `[[specs/S015]]`
- `specs/S010-工具注册表与SYSTEM_PROMPT.md` → 断链 `[[specs/S006]]` `[[specs/S015]]`
- `specs/S011-调度收口.md` → 断链 `[[specs/S006]]` `[[specs/S031]]` `[[specs/S032]]` `[[specs/S015]]`
- `specs/S017-A股涨跌预测模型栈.md` → 断链 `[[specs/S018]]` `[[specs/S019]]` `[[specs/S020]]`
- `specs/S018-多源特征工程.md` → 断链 `[[specs/S017]]` `[[specs/S019]]` `[[specs/S020]]`
- `specs/S019-macro-Fred-API.md` → 断链 `[[specs/S017]]` `[[specs/S018]]` `[[specs/S020]]`
- `specs/S020-worldmonitor决策因子接入.md` → 断链 `[[specs/S017]]` `[[specs/S018]]` `[[specs/S019]]`
- `specs/S031-调度收口盘前多层按战法回测.md` → 断链 `[[specs/S030]]` `[[specs/S011]]` `[[specs/S032]]` `[[specs/S047]]`
- `specs/S047-基因分权重回测校准.md` → 断链 `[[specs/S031]]` `[[specs/S041]]` `[[specs/S049]]`
- `specs/S066-策略特定漏斗架构重构.md` → 断链 `[[specs/S031]]` `[[specs/S023]]` `[[specs/S086]]` `[[specs/S094]]`
- `specs/S094-战法分类与双pipeline重构.md` → 断链 `[[specs/S066]]` `[[specs/S086]]` `[[specs/S097]]` `[[specs/S100]]`
- `specs/S100-战法卡片对齐.md` → 断链 `[[specs/S094]]` `[[specs/S097]]` `[[specs/S101]]` `[[specs/S102]]`

共约 60 条断链（审查报告显示前 20，标注"共 65 条"含本类与 issue 04 的裸编号）。

## 影响

spec 之间的依赖关系（栈式依赖、决策追溯）无法通过双链导航，图谱的"决策记录层"断裂。

## 修复建议

两条路径，需 triage 决定：
1. **补建目标文件**：对每个 SNNN 在 `specs/` 下建对应 .md（从 Vibe-Research 仓库 `specs/` 同步）。需核对源仓 spec 是否存在。
2. **修正链接**：若 SNNN 已改名（如 S006 可能已并入 S007），修正源文件的链接指向正确目标。

注意：specs/ 在图谱里是"决策记录层"（MOC.md line 22），ora-3 诊断未把 spec 断链列为 P0（specs 是静态历史，不影响动态层）。但 broken_link 严重级是 high，应本周期修。

## 关联

- 审查报告：`10_Reference/investing/reviews/2026-09-06-ci-audit.md` §4（line 77-91, 139-203）
