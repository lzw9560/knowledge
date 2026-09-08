
> [!info] 📡 数据源
> **名称**：mootdx  **层级**：L3
> **接口**：`TCP 7709`
> **限流**：`无（惰性导入）`  **降级**：`DependencyMissing 优雅报错`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| date | str | 交易日 |
| open | float | 开盘价 |
| close | float | 收盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| volume | float | 成交量 |
| amount | float | 成交额 |

> 数据源：mootdx Python 包（TCP 7709 通达信协议，惰性导入）
> 注：finance() 季报财务快照数值不可靠（实测放大数倍），财务摘要走 akshare_src.financials
> category：4=日K 5=周K 6=月K 11=60分钟K

## ⏱ 限流策略

- 无（惰性导入，按需调用）
- TCP 7709 通达信协议


## 🔄 降级链

- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级


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

- 🔧 H_Reference/tech-learning/tools/uv包管理|uv 包管理]] — mootdx Python 包由 uv 管理锁版本
- 🔧 H_Reference/tech-learning/concepts/优雅降级|优雅降级]] — 惰性导入，缺失时 DependencyMissing 优雅报错
- 🔧 H_Reference/tech-learning/concepts/数据契约|数据契约]] — TCP 7709 返回数据由契约层统一形状
