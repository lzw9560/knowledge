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
last_synced: 2026-09-07
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
- 喂给实体类型：[[data-sources/]]
- 对应代码：`backend/data/sources/`（待补：具体文件名，可能为 fred.py 或并入 market.py）

## 相关 spec
- [[specs/]] S019 Fred API 接入

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**关联 spec**：
- [[specs/S017-A股涨跌预测模型栈]]（S017）
- [[specs/S018-多源特征工程]]（S018）
- [[specs/S019-macro-Fred-API]]（S019）
- [[specs/S020-worldmonitor决策因子接入]]（S020）
