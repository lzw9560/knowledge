---
type: data_source
name: 108 RSS 源（资讯雷达）
layer: 资讯层
endpoint: 108 源
rate_limit: 40线程并发
fallback: 单源失败不拖垮整体
compliance: ok
provides: [资讯, 12赛道分类, 合规过滤]
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：108 RSS 源（资讯雷达）  **层级**：L资讯层
> **接口**：`108 源`
> **限流**：`40线程并发`  **降级**：`单源失败不拖垮整体`

## 📋 提供字段

| 字段 | 类型 | 说明 |
|---|---|---|
| title | str | 资讯标题 |
| url | str | 资讯链接 |
| time | str | 发布时间（MM-DD HH:MM 北京时间） |
| ts | int | 发布时间戳（Unix 秒） |
| summary | str | 摘要（≤160字，HTML 已剥离） |
| source | str | RSS 源名称 |
| track | str | 12 赛道分类 |

> 数据源：108 个公开 RSS 源（urllib + xml.etree，ThreadPoolExecutor 40 线程并发）
> 零 key、零个股字段；合规红线过滤（赌/预测市场/加密/色情）

## ⏱ 限流策略

- `ThreadPoolExecutor(40)` 并发
- 单源失败不拖垮整体


## 🔄 降级链

- 单源失败 → 跳过该源，不影响整体
- 缓存原子写（tmp + `os.replace`）
- `force` 参数强制刷新


## 🔗 相关实体

- [[stocks/]]
- [[reports/]]
- [[dragon-tiger/]]
- [[metrics/]]
- [[valuations/]]
- [[events/]]

## 📜 关联 spec

- [[specs/]]

## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个

## 🔧 技术栈

- 🔧 [[tech-learning/concepts/graceful-degradation|优雅降级]] — 108 源单源失败不拖垮整体，聚合层容错
- 🔧 [[tech-learning/concepts/circuit-breaker|熔断器]] — 单源连续失败可加熔断
- 🔧 [[tech-learning/concepts/caching-strategy|缓存策略]] — 资讯入缓存降低重复抓取
