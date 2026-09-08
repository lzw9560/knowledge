---
type: language
name: TypeScript
paradigm: 多范式（面向对象/函数式）
typing: 静态类型（结构化类型系统，gradual typing）
created: 2026-09-07
---

# TypeScript

## 范式
- JavaScript 超集，编译到 JS 运行
- 多范式：面向对象（class/interface）、函数式（type/union）
- structural typing（结构化类型，非 nominal）

## 类型系统
- 静态类型，但类型是"可选渐增"的（gradual typing）
- union types / intersection types / conditional types
- strict mode（`strict: true`）开启后类型安全接近静态语言
- 与 Python type hints 的差异：TS 是真静态检查，Python type hints 是可选 hint + mypy

## 主要应用领域
- 前端：[[10_Reference/[[tech-learning/frameworks/react|React]] / Vue / Angular
- 全栈：Next.js / NestJS / Deno
- 工具链：Vite / esbuild / tsc

## 在 Vibe-Research 中的使用
- 前端主语言：[[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步|S009]] 前后端类型同步契约
- 类型定义在 `frontend/src/types/` 与后端 Pydantic 模型对齐
- 配套框架：[[10_Reference/[[tech-learning/frameworks/react]]

## 相关链接
- [[10_Reference/[[tech-learning/MOC]]
- [[10_Reference/[[tech-learning/frameworks/react]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]]
- [[10_Reference/[[meta/四构件本体方法论]]
