---
type: logic
rule_id: DUP-MERGE-001
rule_type: 校验规则
target_entity: 全类型
severity: high
condition: 同一 code 出现多份实体（不同文件同 code）
action_on_violation: 触发合并工单（保留最新/最完整，合并关系后删除冗余）
source: AGENTS.md 工程底线（不臆造数据——重复实体导致数据不一致）
created: 2026-09-07
---

> [!info] ⚙️ 规则
> **规则**：`DUP-MERGE-001`  **类型**：校验规则
> **严重级**：high  **适用实体**：全类型
>
> **违反处置**：`触发合并工单（保留最新/最完整，合并关系后删除冗余）`

## 📋 规则定义

- 类型：`校验规则`
- 适用实体：`全类型`
- 严重级：`high`


## ⚡ 触发条件

`vault_audit.py` 按 frontmatter `code` 字段分组，若同一 code 对应多个文件路径触发合并。


## 🔧 执行逻辑

```
code_files = {}
for file in vault:
  if frontmatter.code:
    code_files[code].append(file)

for code, files in code_files.items():
  if len(files) > 1:
    # 选定保留项：优先 status != placeholder 的，其次 created 最新的
    keeper = select_keeper(files)
    others = files - keeper
    for other in others:
      合并 other 的关系/正文到 keeper
      走 move_note(other → archive/duplicates/) 归档（不真删）
    生成合并日志
```

Dataview 查询（按 code 分组检测重复）：

```dataview
TABLE length(rows) AS "文件数", rows.file.link AS "文件"
FROM "10_Reference/investing"
WHERE code != null
GROUP BY code
HAVING length(rows) > 1
```


## ⚠️ 违反处置

- `action_on_violation`：触发合并工单
- 合并原则：
  1. 保留信息最完整的（非 placeholder 优先）
  2. 合并冗余文件的 frontmatter 字段（取非空值）+ 正文段
  3. 冗余文件 move_note 到 `archive/duplicates/`（可恢复，不真删）
- 合并后需更新所有指向冗余文件的反向链接（走 [[actions/rename-entity]]）


## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[stocks/]]
- **来源决策**：[[specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
