# 审查报告 2026-09-06 → issue 工单映射

> 来源：`10_Reference/investing/reviews/2026-09-06-ci-audit.md`
> 审查报告统计：122 项发现（critical 11 / high 101 / medium 7 / low 3）
> 聚合策略：按问题类别聚合（同类断链/同类缺失合一个工单），不每条一个文件——122 个文件无法管理，且 65 条断链本质是同类问题。

## issue 列表

| 编号 | 标题 | severity | status | 覆盖审查报告条目数 |
|---|---|---|---|---|
| 01 | coverage 完全缺失 11 类实体 | critical | needs-triage | 11 |
| 02 | broken_link 断链 specs/SNNN 编号 | high | needs-triage | ~60 |
| 03 | broken_link 断链 data-sources 指向不存在的文件夹 | high | needs-triage | 6 |
| 04 | broken_link 断链裸编号 [[SNNN]] 无路径前缀 | high | needs-triage | ~19 |
| 05 | schema_infer 战法卡误报（已修复） | high | resolved | 36 |

## 统计核对

- critical 11 → issue 01（11 条）
- high 101 → issue 02-05（101 条 = ~60 + 6 + ~19 + 36，其中 36 已修复）
- medium 7 → 未建工单（orphan 孤立 data-source，进 backlog，审查报告已标 Medium）
- low 3 → 未建工单（relation_density，知悉即可）

## 说明

- schema_infer 36 条误报已在 P0-3 修复（`vault_audit.py` 加正文标题承载豁免），issue 05 记录修复过程，status=resolved。
- critical 11 条都是 coverage 完全缺失类型——ora-3 诊断已规划修复路径（logic 规则、actions 动作、inbox 质量门），不在此 effort 重复，进 issue 01 正文引用。
