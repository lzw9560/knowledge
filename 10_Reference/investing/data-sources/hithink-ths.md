---
type: data_source
name: 同花顺 THS（一致预期/涨停揭秘）
layer: 4
endpoint: basic.10jqka.com.cn
rate_limit: 直连
fallback: 无
compliance: ok
provides: [一致预期, 涨停揭秘]
projects: [vibe-research, trading-agents]
origin_project: vibe-research
created: 2026-09-06
---

# 同花顺 THS（一致预期/涨停揭秘）

## 提供字段
- 机构一致预期
- 涨停揭秘

## 限流策略
- 直连
- 待补：具体限流策略（未在 ARCHITECTURE.md 明示封禁行为）

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[valuations/]] [[events/]] [[stocks/]]
- 对应代码：`backend/data/sources/astock.py` → `profit_forecast`（一致预期，待补：涨停揭秘具体函数）

## 相关 spec
- [[specs/]] 后端数据层迁移 / 一致预期接入
