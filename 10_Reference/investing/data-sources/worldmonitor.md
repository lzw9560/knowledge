---
type: data_source
name: worldmonitor（全球宏观 MCP）
layer: 5
endpoint: MCP 远程
rate_limit: 无
fallback: 无
compliance: ok
provides: [全球宏观指标]
created: 2026-09-06
last_synced: 2026-09-07
---

# worldmonitor（全球宏观 MCP）

## 提供字段
- 全球宏观指标（待补：具体字段列表需对照对应 MCP 服务）

## 限流策略
- MCP 远程调用
- 无（待补：是否有上游限流）

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[data-sources/]]
- 对应代码：待补（MCP 远程服务，可能不在本仓库内）

## 相关 spec
- [[specs/]] 待补（worldmonitor 接入 spec）

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**对应函数**（`backend/data/sources/`）：
- `data.sources.worldmonitor.get_worldmonitor_api_key`
- `data.sources.worldmonitor.fetch_market_data`
- `data.sources.worldmonitor.fetch_country_risk`
- `data.sources.worldmonitor.fetch_news_intelligence`
- `data.sources.worldmonitor.fetch_news_clusters`
- `data.sources.worldmonitor.fetch_economic_data_china`
- `data.sources.worldmonitor.fetch_country_macro`
- `data.sources.worldmonitor.fetch_tariff_trends`
- `data.sources.worldmonitor.fetch_supply_chain`
- `data.sources.worldmonitor.fetch_energy_intelligence`
- `data.sources.worldmonitor.fetch_china_decision_signals`
- `data.sources.worldmonitor.fetch_hotspot_escalation`
- `data.sources.worldmonitor.parse_market_data`
- `data.sources.worldmonitor.parse_country_risk`
- `data.sources.worldmonitor.parse_news_clusters`
- `data.sources.worldmonitor.parse_news_intelligence`
- `data.sources.worldmonitor.parse_hotspot_escalation`
- `data.sources.worldmonitor.parse_supply_chain`

**关联 spec**：
- [[specs/S020-worldmonitor决策因子接入]]（S020）
