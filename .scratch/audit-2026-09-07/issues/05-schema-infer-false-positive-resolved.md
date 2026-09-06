# 05: schema_infer 战法卡误报（已修复）

severity: high
status: resolved
source: 2026-09-06-ci-audit
resolved_at: 2026-09-07
resolved_by: P0-3 (vault_audit.py 正文标题承载豁免)

## 问题描述

审查报告 §5 schema_infer 检查报 12 张战法卡各缺 3 个 frontmatter 字段（`entry_conditions` / `exit_conditions` / `match_conditions`），共 36 条 high 级 finding。

根因（ora-3 诊断硬事实 4）：战法卡是**卡片风格**，用正文 `## 入场条件` / `## 退出参数` / `## 核心逻辑` 标题承载这些信息，而非 frontmatter 字段。审查脚本 `vault_audit.py` 的 `check_schema` 只查 frontmatter，导致 36 条误报。

实证（12 张战法卡正文标题扫描）：
- 全部 12 张都有 `## 入场条件`（承载 `entry_conditions`）
- 全部 12 张都有 `## 退出参数`（承载 `exit_conditions`）
- 全部 12 张都有 `## 核心逻辑`（承载 `match_conditions`）

## 修复

`scripts/vault_audit.py` 新增正文标题承载豁免逻辑：

1. 新增常量 `BODY_HEADING_FOR_FIELD`：映射实体 type → { 缺失字段 → 正文标题正则 }。当前只对 `strategy` 类型定义：
   - `entry_conditions` → `^##\s*入场条件\b`
   - `exit_conditions` → `^##\s*(?:退出参数|出场条件|退出条件)\b`（兼容多种标题写法）
   - `match_conditions` → `^##\s*核心逻辑\b`

2. 新增 helper `has_body_heading(body_text, heading_re)` 和 `strip_frontmatter(text)`。

3. `check_schema` 在判定 missing 后，对有正文标题映射的类型，检查正文是否有对应标题，有则从 missing 列表移除。

## 验证

修复后跑 `python3 scripts/vault_audit.py`：
- schema_infer findings: 36 → 0
- schema_infer deviations: 12 → 0
- 总 findings: 122 → 85（critical 11 + high 65 + medium 7 + low 2）

误报全消，无新误报。

## 关联

- 审查报告：`10_Reference/investing/reviews/2026-09-06-ci-audit.md` §5（line 96-107, 204-239）
- 修复脚本：`scripts/vault_audit.py`（check_schema 函数 + BODY_HEADING_FOR_FIELD 常量）
- ora-3 诊断硬事实 4：36 条误报（战法卡正文有 ## 入场条件 但脚本只查 frontmatter）
