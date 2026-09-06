---
type: data_source
name: FRED（宏观）
layer: 5
endpoint: api.stlouisfed.org
rate_limit: API key 隔离
fallback: 无
compliance: ok
provides: [宏观指标]
created: 2026-09-06
---

# FRED（宏观）

## 提供字段
- 宏观经济指标（待补：具体字段列表需对照对应 spec/代码）

## 限流策略
- API key 隔离
- 待补：具体 QPS 限制

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[macro/]]
- 对应代码：`backend/data/sources/`（待补：具体文件名，可能为 fred.py 或并入 market.py）

## 相关 spec
- [[specs/]] S019 Fred API 接入
