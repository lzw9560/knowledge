---
type: spec
number: S022
title: 熔断器 health 读路径修复（尊重 recovery_timeout）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S022 熔断器 health 读路径修复（尊重 recovery_timeout）

## 摘要

peek_state 只读探测 + health 读路径自愈，修体检 🔴 circuit_breaker_open

## 问题/目标

> 此 spec 为 P2 pipeline 从 `specs/README.md` 自动生成的 stub，待人工补充正文。

## 关联

- 源文件：`specs/S022-熔断器health读路径修复/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
