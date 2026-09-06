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
