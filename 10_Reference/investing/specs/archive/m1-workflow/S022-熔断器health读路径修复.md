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

S022 修复了熔断器健康检查读路径忽略 recovery_timeout 的问题，导致在断路器打开后，即使恢复时限已过，健康端点仍持续返回不健康状态，阻断了自动化恢复流程。核心设计决策是让健康读路径实时计算当前时间与 breaker 打开时刻的差值，并与 recovery_timeout 配置比对，若已超时则允许进入半开状态并返回健康，否则保持不健康响应。该修复联动熔断器状态机、健康检查路由与 recovery_timeout 参数，确保读路径严格遵循恢复超时语义。

## 关联

- 源文件：`specs/S022-熔断器health读路径修复/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
