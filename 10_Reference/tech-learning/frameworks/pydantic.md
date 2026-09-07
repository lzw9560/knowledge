---
type: framework
name: Pydantic
language: Python
category: 数据验证 / 契约层
created: 2026-09-07
---

# Pydantic

## 语言
- [[languages/python|Python]] 3.7+（v2 需要 3.8+）
- 核心引擎用 Rust 重写（pydantic-core），v2 性能比 v1 快 5-50x

## 类别
- 数据验证与序列化库
- 与 dataclasses 的对比：dataclasses 只定义结构，Pydantic 额外做运行时验证 + 序列化（JSON <-> 对象）

## 核心特性
- **类型提示即验证**：`age: int = Field(ge=0)` 自动验证非负整数
- **JSON 序列化**：`model_dump_json()` / `model_validate_json()` 一等公民
- **嵌套模型**：`address: Address`，递归验证
- **Custom validators**：`@field_validator` / `@model_validator` 做复杂业务规则
- **OpenAPI 生成**：FastAPI 基于 Pydantic 模型自动生成 schema

## 在 Vibe-Research 中的使用
- **契约层核心**：[[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007 契约层]] 用 Pydantic 定义所有 API 请求/响应模型
- **数据层**：[[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移|S008 后端数据层迁移]] 把 dataclass 迁到 Pydantic，统一验证 + 序列化
- **前后端类型同步**：[[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步|S009]] 从 Pydantic 模型生成 TypeScript 类型，供 [[frameworks/react|React]] 前端使用
- 配套框架：[[frameworks/fastapi|FastAPI]] 把 Pydantic 作为一等依赖

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[languages/python]]
- [[frameworks/fastapi]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]]
- [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移]]
- [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]]
- [[10_Reference/meta/four-construct-ontology]]
