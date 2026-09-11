---
type: spec
number: S010
title: AI 工具注册表 + SYSTEM_PROMPT 新边界
status: 已实现
created: 2026-09-06
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S010 AI 工具注册表 + SYSTEM_PROMPT

## 问题/目标

AI 工具调用入口散落 chat/mcp/cli 三处，每处各自维护工具清单。需统一为声明式 registry，三出口共享同一注册表。

## 核心决策

registry 声明式 + chat/mcp/cli 解耦 + SYSTEM_PROMPT 按新边界放宽。工具以声明式注册表登记，三出口（chat / MCP / CLI）消费同一注册表，SYSTEM_PROMPT 按 S006 §1 合规边界放宽（允许给研判/推荐，工程底线保留）。

## 受影响文件

- `backend/ai/registry.py`（声明式注册表）
- `backend/ai/chat.py` / `mcp.py` / `cli.py`（三出口解耦）
- `backend/ai/system_prompt.py`（SYSTEM_PROMPT 新边界）

## 验收标准

- 声明式 registry 就位
- chat/mcp/cli 三出口消费同一注册表
- SYSTEM_PROMPT 按新边界放宽

## 关联

- 上游纲领：[[10_Reference/investing/specs/S006-系统重写纲领]]（§1 合规边界调整）
- 衔接后续：[[10_Reference/investing/specs/archive/m0-foundation/S015-配置与基础设施]]（配置与基础设施）
- 影响实体：[[10_Reference/investing/analysts/index|analysts/]]（AI agent 角色）
- 数据源：[[10_Reference/investing/data-sources/同花顺 THS（一致预期·涨停揭秘）]]
- 源文件：`specs/archive/m0-foundation/S010-工具注册表与SYSTEM_PROMPT/spec.md`
