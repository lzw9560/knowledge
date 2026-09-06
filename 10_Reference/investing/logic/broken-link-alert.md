---
type: logic
rule_id: BROKEN-LINK-001
rule_type: 校验规则
target_entity: 全类型
severity: high
condition: 断链（[[xxx]] 指向不存在的文件）数量 > 3
action_on_violation: 触发修复工单（列出断链源 + 目标）
source: ora-3 诊断 §6.5（move_note 危险操作约束——直接 rename 会导致断链）
created: 2026-09-07
---

# 规则：断链告警

## 规则定义

- **类型**：校验规则
- **适用实体**：全类型（任何含 `[[]]` 链接的文件）
- **严重级**：high
- **条件**：`断链数量 > 3`（断链 = `[[]]` 指向的文件不存在）

## 触发条件

`vault_audit.py` 扫描全库所有 `[[]]` 链接，解析目标路径，若目标文件不存在则为断链。当断链数 > 3 触发修复工单。

## 执行逻辑

```
对所有 .md 文件：
  for each [[link]] in file:
    if not exists(resolve(link)):
      broken_links += (源文件, 链接文本, 目标路径)

if len(broken_links) > 3:
  生成修复工单（.scratch/broken-link-fix/）
  分组：按目标路径聚类（同一目标多个源 → 优先建目标实体）
```

Dataview 查询（Obsidian 原生不支持断链检测，需脚本）：

```dataview
TABLE file.name AS "源文件", file.outlinks AS "出链"
FROM "10_Reference/investing"
WHERE length(file.outlinks) > 0
```

## 违反处置

- `action_on_violation`：触发修复工单
- 修复优先级：
  1. 多个源指向同一不存在的目标 → 优先建目标实体（inbox stub → [[actions/approve-entity]]）
  2. 拼写错误 → 修正链接文本
  3. 目标实体已删除 → 移除断链或改指向替代实体

## 阈值依据

- **3 条**：保守初值。断链影响图谱可用性，>3 时需系统化修复。ora-3 §6.5 指出 move_note 不当使用是断链主因。

## 关联

- 触发动作：[[actions/approve-entity]]（建缺失的目标实体）、[[actions/rename-entity]]（修正链接）
- 约束实体：全类型
- 来源：ora-3 诊断 §6.5（move_note 危险操作约束）
- 相关规则：[[logic/实体改名]]（RENAME-001，防止 agent 直接 rename 导致断链）、[[logic/orphan-threshold]]
