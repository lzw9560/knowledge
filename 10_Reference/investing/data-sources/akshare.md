---
type: data_source
name: akshare
layer: 3
endpoint: akshare Python 包
rate_limit: 无（惰性导入）
fallback: DependencyMissing 优雅报错
compliance: ok
provides: [legu行业资金流, 行业资金流, 财报三表(待补)]
projects: [vibe-research, trading-agents, daily-stock-analysis]
origin_project: vibe-research
created: 2026-09-06
last_synced: 2026-09-07
confidence: high
source: ARCHITECTURE.md
---

> [!info] 📡 数据源
> **名称**：akshare  **层级**：L3
> **接口**：`akshare Python 包`
> **限流**：`无（惰性导入）`  **降级**：`DependencyMissing 优雅报错`

## 📋 提供字段

待补充


## ⏱ 限流策略

- 无（惰性导入，按需调用）
- Python 包，无网络层限流


## 🔄 降级链

- 惰性导入：缺失时 `DependencyMissing` 优雅报错，不挡启动
- 无进一步降级


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

- 🔧 [[../../tech-learning/tools/uv|uv 包管理]] — akshare Python 包由 uv 统一管理与锁版本（pyproject.toml + uv.lock）
- 🔧 [[../../tech-learning/concepts/graceful-degradation|优雅降级]] — 惰性导入，缺失时 DependencyMissing 优雅报错不挡启动
- 🔧 [[../../tech-learning/frameworks/pydantic|Pydantic]] — akshare 返回的裸 dict 由契约层吸收为 Pydantic 模型
