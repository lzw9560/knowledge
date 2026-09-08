---
type: spec
number: S046
title: fallback 空写防护（限流返空不覆盖好缓存）
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S046 fallback 空写防护（限流返空不覆盖好缓存）

## 摘要

_is_empty + save_cache 空不写 + load_cache 损坏自愈删除 + 空 fetch 降级好缓存

## 问题/目标

该规范旨在解决限流降级时因直接返回空结果导致缓存中已有有效数据被错误覆盖的问题，从而防止缓存污染引发后续请求持续获取空值。核心设计决策是引入空写防护层，通过识别降级标记或空响应，禁止这些无效数据写入缓存，并保持缓存更新逻辑仅在正常业务响应时生效。所涉及的关键技术组件包括限流器、缓存中间件（如 Redis）以及请求过滤器或 AOP 拦截器，利用上下文传递降级状态来精准阻断空写操作。

## 关联

- 源文件：`specs/S046-fallback空写防护/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
