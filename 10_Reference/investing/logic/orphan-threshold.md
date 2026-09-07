---
type: logic
rule_id: ORPHAN-001
rule_type: 校验规则
target_entity: 全类型
severity: medium
condition: 孤立实体（无反向链接、无出链）数量 > 5
action_on_violation: 触发审查工单（列出孤立体单 + 灌入/删除建议）
source: ora-3 诊断 §3（图谱连通性——孤立实体降低图谱可用性）
created: 2026-09-07
confidence: high
---

> [!info] ⚙️ 规则
> **规则**：`ORPHAN-001`  **类型**：校验规则
> **严重级**：medium  **适用实体**：全类型
>
> **违反处置**：`触发审查工单（列出孤立体单 + 灌入/删除建议）`

## 📋 规则定义

- 类型：`校验规则`
- 适用实体：`全类型`
- 严重级：`medium`


## ⚡ 触发条件

`vault_audit.py` 扫描全库后统计孤立实体（frontmatter 有 type 但正文无 `[[]]` 链接且无其他文件反向链接）。当孤立项数 > 5 触发审查。


## 🔧 执行逻辑

```
对每个实体文件：
  in_links = count(其他文件含指向本文件链接的链接)
  out_links = count(本文件正文出链数量)
  if in_links == 0 AND out_links == 0:
    孤立实体 += 1

if 孤立实体 > 5:
  生成审查工单（.scratch/orphan-audit/）
  列出每个孤立项 + 建议（灌入关系 / 删除 / 合并）
```

Dataview 查询（手动审查用）：

```dataview
TABLE type AS "类型", code AS "代码", name AS "名称"
FROM "10_Reference/investing"
WHERE type != null AND length(file.inlinks) = 0 AND length(file.outlinks) = 0
```


## ⚠️ 违反处置

- `action_on_violation`：触发审查工单，逐个判断是灌入关系还是删除
- 孤立占位实体（如 status=placeholder）→ 优先灌入关系而非删除
- 孤立真实实体（有 type 但无关系）→ 检查是否应归并到已有实体


## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[stocks/]]
- **来源决策**：[[specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
