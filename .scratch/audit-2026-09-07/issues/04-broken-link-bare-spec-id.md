# 04: broken_link 断链裸编号 [[SNNN]] 无路径前缀

severity: high
status: needs-triage
source: 2026-09-06-ci-audit

## 问题描述

审查报告 §4 broken_link 检查发现部分 spec 文件用裸编号 `[[SNNN]]` 链接（无 `specs/` 路径前缀），而图谱里 spec 文件名为 `SNNN-标题.md`，裸编号无法解析：

- `[[S008]]` ← `specs/S007-契约层.md`
- `[[S018]]` ← `specs/S017-A股涨跌预测模型栈.md`
- `[[S019]]` ← `specs/S018-多源特征工程.md`

共约 19 条（审查报告 line 90, 171, 175 是此类代表）。

## 影响

与 issue 02 同类（spec 间依赖断链），但根因不同：issue 02 是路径前缀 `specs/` 有但目标文件不存在；本 issue 是缺路径前缀且文件名带标题后缀，Obsidian 无法匹配。

## 修复建议

1. **加路径前缀 + 补标题后缀**：`[[S008]]` → `[[specs/S008-后端数据层迁移]]`。需核对目标文件的真实文件名。
2. 或用 Obsidian 的别名机制：`[[specs/S008-后端数据层迁移|S008]]`。

## 关联

- 审查报告：`10_Reference/investing/reviews/2026-09-06-ci-audit.md` §4（line 90, 158, 171, 175）
- 与 issue 02 是同类问题的两种形态，建议合并 triage
