---
type: concept
name: 清洁代码
category: 编程概念
created: 2026-09-07
---

# 清洁代码（Clean Code）

## 类别
- 编程方法论（Robert C. Martin / Uncle Bob，《Clean Code》2008）
- 与 [[10_Reference/tech-learning/architecture/clean-architecture|清洁架构]] 同源——代码层的清洁是架构层清洁的基础

## 核心原则
1. **有意义命名**：变量/函数/类名要自解释（`calculateRiskScore` 优于 `calc`）
2. **单一职责**：一个函数只做一件事（SRP），函数长度控制在 20 行内
3. **无注释化**：好代码自解释，注释只用于"为什么"不写"是什么"
4. **错误处理**：用异常/Result 类型而非错误码，避免深层嵌套 if
5. **DRY**：Don't Repeat Yourself——抽象公共逻辑
6. **YAGNI**：You Aren't Gonna Need It——不过度设计

## 与 SOLID 原则的对应
| SOLID | 清洁代码体现 |
|---|---|
| S - 单一职责 | 函数/类只做一件事 |
| O - 开闭原则 | 通过扩展而非修改添加功能 |
| L - 里氏替换 | 子类可替换父类不破坏行为 |
| I - 接口隔离 | 小接口优于胖接口 |
| D - 依赖反转 | 依赖抽象不依赖具体 |

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/S006-系统重写纲领|S006 系统重写纲领]] 即遵循清洁代码 + [[10_Reference/tech-learning/architecture/clean-architecture|清洁架构]] 重写
- 契约层 [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007]] 的 Pydantic 模型职责单一——纯数据契约不含业务逻辑
- AGENTS.md 的"工程底线不降级"是清洁代码的项目治理化

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/architecture/clean-architecture]]
- [[10_Reference/tech-learning/concepts/type-safety]]
- [[10_Reference/investing/specs/S006-系统重写纲领]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]]
- [[10_Reference/meta/four-construct-ontology]]
