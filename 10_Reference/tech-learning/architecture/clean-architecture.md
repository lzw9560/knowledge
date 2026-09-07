---
type: architecture
name: 清洁架构
category: 架构模式
created: 2026-09-07
---

# 清洁架构

## 类别
- 分层架构模式（Robert C. Martin / Uncle Bob，2012）
- 与 MVC / 三层架构的对比：清洁架构强调**依赖方向**——外层依赖内层，内层不感知外层

## 核心特性
- **同心圆分层**：实体（Entity）→ 用例（Use Case）→ 接口适配器（Adapter）→ 框架/驱动（Web/DB）
- **依赖反转**：内层不依赖外层，外层依赖内层（通过接口）
- **领域核心独立**：业务规则不感知数据库 / Web 框架 / UI
- **跨层边界**：数据穿越边界时用 DTO（Data Transfer Object），不直接传 ORM 实体

## 分层映射（Vibe-Research 示例）
| 清洁架构层 | Vibe-Research 对应 | 说明 |
|---|---|---|
| Entity | 战法卡 / 数据源抽象 | [[10_Reference/investing/strategies/|战法卡]] 业务规则 |
| Use Case | `backend/services/` | 调度 / 战法执行编排 |
| Adapter | `backend/routers/` + Pydantic 模型 | [[10_Reference/investing/specs/S007-契约层\|S007 契约层]] |
| Framework | FastAPI / React / Docker | 外层框架 |

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/S006-系统重写纲领|S006 系统重写纲领]] 遵循清洁架构思想：领域层独立于框架
- 契约层（[[10_Reference/investing/specs/S007-契约层|S007]]）是"接口适配器"层，用 [[frameworks/pydantic|Pydantic]] 模型隔离领域与传输
- 前端数据层（[[10_Reference/investing/specs/S013-前端数据层|S013]]）也遵循同构——TanStack Query 是前端的"适配器"

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/architecture/microservices]]
- [[10_Reference/investing/specs/S006-系统重写纲领]]
- [[10_Reference/investing/specs/S007-契约层]]
- [[10_Reference/meta/four-construct-ontology]]
