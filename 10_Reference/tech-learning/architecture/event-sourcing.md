---
type: architecture
name: 事件溯源
category: 架构模式
created: 2026-09-07
---

# 事件溯源

## 类别
- 状态管理架构模式（Martin Fowler，2005）
- 与 CRUD 的对比：CRUD 直接覆盖当前状态，事件溯源**追加**事件日志，状态由重放事件得出
- 与 [[10_Reference/tech-learning/architecture/event-driven|事件驱动]] 的关系：事件驱动是"通信模式"，事件溯源是"存储模式"——可叠加但不同概念

## 核心特性
- **事件日志是真相源**：所有状态变更记录为不可变事件（append-only log）
- **当前状态 = fold(events)**：当前态是事件日志的归约结果
- **时间旅行**：可重放到任意历史时刻，支持审计与回溯
- **CQRS 配对**：写模型是事件追加，读模型是物化视图（projection）——读写分离
- **不可变**：事件永不修改，错误用补偿事件（compensation）而非删除

## 投研工作流状态机的同构
- [[10_Reference/investing/specs/archive/m1-workflow/S033-状态机前端呈现|S033 状态机前端呈现]]：盘前工作流的状态推进（idle → fetching → analyzing → ready）本质是状态机
- 事件溯源视角：每次状态迁移记录为事件，当前态 = 重放事件序列
- [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口|S011 调度收口]] 的多层调度（盘前/盘中/盘后）可参考事件溯源——调度任务作为事件，执行结果追加到日志
- 与 [[10_Reference/investing/logic/战法天气映射|战法天气映射]]（待建）的同构：战法适用天气是状态，市场事件触发天气变更

## 在 Vibe-Research 中的潜在应用
- 当前 Vibe-Research 未完整实现事件溯源，但 S011 / S033 的状态机是其简化形态
- 决策审计：投研决策（战法触发 / 信号生成）若记录为事件日志，可回溯任意时刻的决策依据
- 参考 [[10_Reference/tech-learning/architecture/event-driven|事件驱动架构]] 的基础设施（事件总线）

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/architecture/event-driven]]
- [[10_Reference/tech-learning/architecture/clean-architecture]]
- [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口]]
- [[10_Reference/investing/specs/archive/m1-workflow/S033-状态机前端呈现]]
- [[10_Reference/meta/four-construct-ontology]]
