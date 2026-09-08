---
type: spec
number: S001
title: 修复 chat._get_env_llm_config 缺失 → /api/chat 500
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S001 修复 chat._get_env_llm_config 缺失 → /api/chat 500

## 摘要

补全环境变量兜底函数，打通问 AI

## 问题/目标

该规范修复了在调用 /api/chat 接口时因 `chat._get_env_llm_config` 方法缺失而导致的 500 服务器内部错误，该错误源于 LLM 配置获取流程中引用了一个未定义的内部函数。核心设计决策是在 `chat` 模块中补全该辅助方法，使其从环境变量安全地提取并返回 LLM 供应商、模型名称和 API 密钥，同时保持与现有配置加载策略的兼容性。涉及的关键组件包括 vLLM 或 OpenAI 兼容的 LLM 后端、FastAPI 聊天路由以及环境变量解析逻辑。

## 关联

- 源文件：`specs/S001-fix-chat-env-llm-config/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[10_Reference/investing/data-sources/index|data-sources/]]
- 战法：[[10_Reference/investing/strategies/index|strategies/]]
