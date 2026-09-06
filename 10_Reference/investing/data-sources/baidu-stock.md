---
type: data_source
name: 百度股市通（日K线）
layer: 4
endpoint: finance.pae.baidu.com
rate_limit: 不封IP
fallback: 无
compliance: ok
provides: [日K线]
created: 2026-09-06
---

# 百度股市通（日K线）

## 提供字段
- 日 K 线

## 限流策略
- 不封 IP
- 直连

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[stocks/]] [[metrics/]]
- 对应代码：`backend/data/sources/astock.py`（待补：具体函数名，可能并入 kline）

## 相关 spec
- [[specs/]] 后端数据层迁移 / 日 K 线接入
