---
type: data_source
name: 
layer: 
endpoint: 
rate_limit: 
fallback: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 数据源说明

- 名称：`name`
- 层级：`layer`（L1 实时/L2 延时/L3 离线）
- 接口：`endpoint`

# 提供字段



# 限流策略

- 限流：`rate_limit`

# 降级链

- 降级：`fallback`（主源失败后切到哪个备用源）

# 相关实体

> 该数据源供给哪些实体（股票/研报/龙虎榜…）。

- [[stocks/]]
- [[reports/]]
- [[dragon-tiger/]]
