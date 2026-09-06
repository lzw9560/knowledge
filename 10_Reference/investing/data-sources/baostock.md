---
type: data_source
name: baostock（K线日更）
layer: 4
endpoint: bbaostock.com
rate_limit: 无
fallback: S090 kline_refresh
compliance: ok
provides: [K线日更]
projects: [vibe-research, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
---

# baostock（K线日更）

## 提供字段
- K 线日更数据

## 限流策略
- 无（待补：是否有上游限流）

## 降级链
- 无网络降级
- 任务级：由 `scheduled_tasks.py` 的 `kline_refresh`（S090）定时执行

## 相关实体
- 喂给实体类型：[[stocks/]] [[metrics/]]
- 对应代码：`backend/data/sources/`（待补：具体文件名）+ `scheduled_tasks.py` → `kline_refresh` 任务

## 相关 spec
- [[specs/]] S090 baostock kline 日更
