---
type: architecture
name: Saga 模式
category: 架构模式
created: 2026-09-07
---

# Saga 模式（分布式事务）

## 类别
- 架构模式（Hector Garcia-Molina & Kenneth Salem，1987）
- 解决跨服务长事务问题——替代两阶段提交（2PC）

## 核心特性
- **拆分长事务**：一个分布式事务拆为 N 个本地事务（T1..Tn）
- **补偿事务**：每步 Ti 配补偿 Ci（撤销 Ti 的副作用）
- **编排 vs 协同**：
  - 编排式（Orchestration）：中央协调器按顺序调度 Ti，失败时按逆序跑 Ci
  - 协同式（Choreography）：各服务监听事件自治，无中央协调器
- **最终一致性**：放弃 ACID，换 A + 最终一致

## 与其他模式的关系
- 与 [[10_Reference/tech-learning/architecture/event-driven|事件驱动]] 天然搭配：协同式 Saga 即事件链
- 与 [[10_Reference/tech-learning/architecture/event-sourcing|事件溯源]] 互补：事件溯源记"发生过什么"，Saga 管"当前事务怎么补偿"
- 与 [[10_Reference/tech-learning/architecture/microservices|微服务]]：跨服务事务的标配

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/S011-调度收口|S011 调度收口]] 的多层调度本质是编排式 Saga：盘前准备 → 盘中扫描 → 盘后复盘，每步失败需回滚前序（如盘前数据源失败，盘中扫描跳过 + 标灰）
- [[10_Reference/investing/specs/S033-状态机前端呈现|S033]] 工作流状态机即 Saga 的状态机视图——每步状态 = Ti，失败路径 = Ci
- [[10_Reference/investing/specs/S012-工作流标灰|S012 工作流标灰]] 即失败时的"补偿可视化"

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/architecture/event-driven]]
- [[10_Reference/tech-learning/architecture/event-sourcing]]
- [[10_Reference/tech-learning/architecture/microservices]]
- [[10_Reference/investing/specs/S011-调度收口]]
- [[10_Reference/investing/specs/S033-状态机前端呈现]]
- [[10_Reference/meta/four-construct-ontology]]
