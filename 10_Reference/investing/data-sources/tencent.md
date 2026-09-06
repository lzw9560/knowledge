---
type: data_source
name: 腾讯行情
layer: 1
endpoint: qt.gtimg.cn
rate_limit: 不封IP
fallback: 底座层，无降级
compliance: ok
provides: [现价, 涨跌, PE, PB, 市值, 换手, 涨跌停]
created: 2026-09-06
last_synced: 2026-09-07
---

# 腾讯行情

## 提供字段
- 现价、涨跌、涨跌幅
- PE、PB
- 市值、流通市值
- 换手率
- 涨停价、跌停价

## 限流策略
- 不封 IP，HTTP GBK 编码
- 标准库 `urllib` 直连
- **永远可用**，作为 A 股底座 Layer 1

## 降级链
- 底座层，无降级
- 反而是其他数据源失败后的兜底源

## 相关实体
- 喂给实体类型：[[stocks/]] [[valuations/]] [[metrics/]]
- 对应代码：`backend/data/sources/astock.py` → `tencent_quote`
- MCP 暴露：`query_quote` 工具

## 相关 spec
- [[specs/]] 后端数据层基础（A 股全栈数据层五源分级中的 Layer 1 底座）

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**相关工具**：
- `query_quote` → `astock.tencent_quote`

**对应函数**（`backend/data/sources/`）：
- `data.sources.tencent.get_prefix`
- `data.sources.tencent.fetch_raw`
- `data.sources.tencent.index_raw`

**关联 spec**：
- [[specs/S008-后端数据层迁移]]（S008）

**喂给实体类型**：
- [[stocks/]]
- [[valuations/]]
- [[metrics/]]
