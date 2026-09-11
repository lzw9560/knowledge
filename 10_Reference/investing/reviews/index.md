---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 审查报告（Reviews）索引

> ReAct 审查 Agent 的产出——定期对知识图谱做体检，按严重级别分类问题 + 修复建议。
> 蒸馏自 nano-ontoprompt ReAct Agent 审查机制。

## 审查报告列表

<!-- dataview-precompiled:800b37b3d95c query:VEFCTEUKY3JlYXRlZCBBUyAi5pel5pyfIiwKICDpl67popjmlbAgQVMgIumXrumimOaVsCIsCiAg5Lil6YeNIEFTICLkuKXph40iLAogIOeKtuaAgSBBUyAi54q25oCBIgpGUk9NICIxMF9SZWZlcmVuY2UvaW52ZXN0aW5nL3Jldmlld3MiCldIRVJFIHR5cGUgPSAibWV0aG9kb2xvZ3lfaW5kZXgiClNPUlQgY29kZSBBU0MK -->
| 文件 | 日期 | 问题数 | 严重 | 状态 |
|---|---|---|---|---|
| [[10_Reference/investing/reviews/index]] | 2026-09-07 | — | — | — |
<!-- /dataview-precompiled -->

## 8 个检查工具

每次审查跑这 8 项（ReAct 循环：Reason → Act → Observe → Report）：

| 检查 | 目的 | Obsidian/MCP 实现 |
|---|---|---|
| `summary` | 图谱整体摘要 | Dataview 聚合 + `get_vault_stats` |
| `coverage` | 各实体类型覆盖率 | `TABLE FROM "10_Reference/investing/stocks"` 计数对比预期 |
| `orphan_check` | 无入边实体 | `find_orphans` MCP |
| `broken_link` | wikilink 指向不存在文件 | `find_broken_links` MCP |
| `schema_infer` | 实际 schema vs 设计偏差 | Dataview 查 frontmatter 字段分布 |
| `relation_density` | 关系密度异常 | `get_backlinks` 计数 |
| `duplicate_check` | 同实体多份记录 | 按代码/名称分组查重 |
| `stale_check` | 长期未更新实体 | 按 `updated` 字段排序 |

## 审查报告模板

用 `templates/audit.md` 新建，含：
- 审查日期 + 审查人/agent
- 8 项检查的结果摘要
- 问题清单（按严重级 critical/high/medium/low 分类）
- 修复建议 + 跟踪状态

## 审查频率

- **季度审查**：全量 8 项检查
- **新 spec 落地后**：跑 `broken_link` + `orphan_check`（看是否引入新断链）
- **实体改名后**：跑 `broken_link`（确认 `move_note` 重写了反向链接）
- **大批量灌入后**：跑 `coverage` + `duplicate_check`

---

## ⚡ 快速操作

用 Templater 应用 `templates/audit` 新建 审查报告 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:49f87610b888 query:VEFCTEUK5a6h5p+l5oql5ZGK5oC75pWwIEFTICLlrqHmn6XmiqXlkYrmgLvmlbAiCkZST00gIjEwX1JlZmVyZW5jZS9pbnZlc3RpbmcvcmV2aWV3cyIKV0hFUkUgdHlwZSA9ICJtZXRob2RvbG9neV9pbmRleCIKU09SVCBjb2RlIEFTQwo= -->
| 文件 | 审查报告总数 |
|---|---|
| [[10_Reference/investing/reviews/index]] | — |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
