---
type: architecture
name: CQRS
category: 架构模式
created: 2026-09-07
---

# CQRS（命令查询职责分离）

## 类别
- 架构模式（Greg Young，2010）
- 与 10_Reference/tech-learning/architecture/清洁架构|[[清洁架构]] 互补：CQRS 把"读"和"写"彻底分离，清洁架构只分层不分离读写

## 核心特性
- **命令（Command）**：改变状态，无返回值（或仅返回 id）—— create/update/delete
- **查询（Query）**：读取数据，不改变状态——只读
- **模型分离**：写模型面向业务一致性（聚合根/事务），读模型面向查询性能（物化视图/缓存/宽表）
- **数据存储可分离**：写库规范化，读库反规范化（甚至异构——MySQL 写 + ES 读）

## 与传统 CRUD 的对比
| 维度 | CRUD | CQRS |
|---|---|---|
| 模型 | 读写共用一模型 | 读写分离 |
| 复杂度 | 低 | 高（需同步两模型） |
| 扩展性 | 读写耦合，难独立扩展 | 读写独立扩展 |
| 适用 | 简单业务 | 读多写少 / 读写模型差异大 |

## 与事件驱动的天然搭配
- CQRS 常配 10_Reference/tech-learning/architecture/事件驱动架构|[[事件驱动]]：写模型发事件，读模型订阅事件更新物化视图
- 进一步即 10_Reference/tech-learning/architecture/事件溯源|[[事件溯源]] + CQRS 的经典组合

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007 契约层]] 的读路径（前端查询战法/候选/快照）与写路径（调度器写状态）天然是 CQRS 雏形
- [[10_Reference/investing/specs/archive/m0-foundation/S013-前端数据层|S013]] TanStack Query 是前端的"读模型适配器"——只读 + 缓存
- [[10_Reference/investing/specs/archive/m1-workflow/S033-状态机前端呈现|S033]] 工作流状态机读路径独立于调度写路径

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- 10_Reference/tech-[[learning/architecture/清洁架构]]
- 10_Reference/tech-[[learning/architecture/事件驱动架构]]
- 10_Reference/tech-[[learning/architecture/事件溯源]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]]
- [[10_Reference/meta/四构件本体方法论]]
