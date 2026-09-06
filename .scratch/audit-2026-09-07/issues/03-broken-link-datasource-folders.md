# 03: broken_link 断链 data-sources 指向不存在的文件夹

severity: high
status: needs-triage
source: 2026-09-06-ci-audit

## 问题描述

审查报告 §4 broken_link 检查发现 6 条 data-source 实体链接指向图谱里不存在的文件夹：

- `[[sectors/]]` ← `data-sources/akshare.md`
- `[[news/]]` ← `data-sources/cninfo.md`
- `[[news/]]` ← `data-sources/eastmoney-searchapi.md`
- `[[macro/]]` ← `data-sources/fred.md`
- `[[news/]]` ← `data-sources/rss-newsradar.md`
- `[[macro/]]` ← `data-sources/worldmonitor.md`

这些链接指向 `sectors/` `news/` `macro/` 文件夹，但图谱本体只定义了 `industries/` `concepts/` `events/` 等实体文件夹——`sectors/` `news/` `macro/` 不在本体里。

## 影响

data-source 实体的"覆盖什么数据"关系断裂，无法导航到对应实体。

## 修复建议

两种处置，需 triage：
1. **重映射到现有本体文件夹**（推荐）：
   - `[[sectors/]]` → `[[industries/]]`（sector ≈ 行业板块）
   - `[[news/]]` → `[[events/]]`（新闻 ≈ 事件实体）
   - `[[macro/]]` → 待定（图谱无 macro 实体类，ora-3 诊断未规划 macro 文件夹；可暂指向 `[[MOC]]` 或新建 `indices/macro-indices` 子类）
2. **在 data-source 实体正文用自然语言描述**，删除断链。

注意：`events/` 当前是空壳（issue 01），修链接后仍指向空文件夹，但至少不是断链。

## 关联

- 审查报告：`10_Reference/investing/reviews/2026-09-06-ci-audit.md` §4（line 71-76, 139-144）
