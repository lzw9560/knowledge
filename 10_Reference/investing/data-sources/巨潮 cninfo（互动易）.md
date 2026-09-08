
> [!info] 📡 数据源
> **名称**：巨潮 cninfo（互动易）  **层级**：L4
> **接口**：`www.cninfo.com.cn`
> **限流**：`requests 直连`  **降级**：`无`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| company | str | 公司简称 |
| question | str | 投资者提问内容 |
| answer | str | 公司回复内容（None=未回复） |
| answerer | str | 回复人 |
| ask_time | str | 提问时间（YYYY-MM-DD HH:MM） |

> 数据源：`irm.cninfo.com.cn` 互动易（requests 直连，非东财封 IP 域）

## ⏱ 限流策略

- requests 直连
- 源端未明示封禁行为，低频调用直连


## 🔄 降级链

- 无


## 🔗 相关实体

- [[10_Reference/investing/stocks/index|stocks/]]
- [[10_Reference/investing/reports/index|reports/]]
- [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]
- [[10_Reference/investing/metrics/index|metrics/]]
- [[10_Reference/investing/valuations/index|valuations/]]
- [[10_Reference/investing/events/index|events/]]

## 📜 关联 spec

- [[10_Reference/investing/specs/index|specs/]]

## 🔗 关联

- **出链**：10 个 · **入链**：0 个

## 🔧 技术栈

- 🔧 H_Reference/tech-learning/concepts/优雅降级|优雅降级]] — 巨潮互动易无降级，失败标灰
- 🔧 H_Reference/tech-learning/concepts/数据契约|数据契约]] — 互动易数据由契约层统一形状
- 🔧 H_Reference/tech-learning/concepts/缓存策略|缓存策略]] — 低频数据入缓存
