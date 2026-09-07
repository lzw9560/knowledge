---
type: concept
name: 类型安全
category: 编程概念
created: 2026-09-07
---

# 类型安全（Type Safety）

## 类别
- 编程概念（静态/动态类型系统的核心维度）
- 与 [[10_Reference/tech-learning/concepts/clean-code|清洁代码]] 同源：类型安全是清洁代码的基础设施

## 核心特性
- **静态类型**：编译期检查类型，错误前置（早失败）
- **类型推断**：无需显式标注，编译器推断（如 TypeScript 的 `let x = 1` 推断为 number）
- **类型即契约**：函数签名即输入输出契约，IDE 自动补全 + 重构安全
- **渐进式类型**：TypeScript / Python(type hints) 允许动态/静态混合

## 与动态类型的对比
| 维度 | 动态类型 | 静态类型 |
|---|---|---|
| 开发速度 | 快（无标注） | 稍慢（标注） |
| 错误发现 | 运行时 | 编译期 |
| 重构安全 | 弱 | 强 |
| 大型项目 | 易失控 | 可维护 |

## 在 Vibe-Research 中的使用
- [[10_Reference/tech-learning/frameworks/pydantic|Pydantic]] 是 Python 的运行时类型安全——schema 校验 + 自动文档
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007 契约层]] 用 Pydantic 模型做前后端共享契约，类型安全跨语言传递
- [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步|S009 前后端类型同步]] — 后端 Pydantic schema 自动生成前端 TS 类型，端到端类型安全
- [[10_Reference/tech-learning/languages/typescript|TypeScript]] 前端全静态类型

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/frameworks/pydantic]]
- [[10_Reference/tech-learning/languages/typescript]]
- [[10_Reference/tech-learning/concepts/clean-code]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]]
- [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]]
- [[10_Reference/meta/four-construct-ontology]]
