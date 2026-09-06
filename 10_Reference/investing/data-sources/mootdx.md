---
type: data_source
name: mootdx
layer: 3
endpoint: TCP 7709
rate_limit: 无（惰性导入）
fallback: DependencyMissing 优雅报错
compliance: ok
provides: [K线, 财报(待补)]
created: 2026-09-06
---

# mootdx

## 提供字段
- K 线数据
- 财报数据（待补：具体三表分工与新浪重叠，待核对）

## 限流策略
- 无（惰性导入，按需调用）
- TCP 7709 通达信协议

## 降级链
- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级

## 相关实体
- 喂给实体类型：[[stocks/]] [[metrics/]]
- 对应代码：`backend/data/sources/astock.py` → `kline`、`finance`（惰性导入点）

## 相关 spec
- [[specs/]] 后端数据层迁移 / mootdx 惰性导入
