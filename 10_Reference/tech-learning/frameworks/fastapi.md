---
type: framework
name: FastAPI
language: Python
category: 后端 Web 框架
created: 2026-09-07
---

# FastAPI

## 语言
- [[10_Reference/[[tech-learning/languages/python|Python]] 3.7+
- 基于 Starlette（ASGI）+ Pydantic

## 类别
- 后端 Web 框架
- ASGI 异步，适合 IO 密集场景（投研数据采集正属此类）

## 核心特性
- 类型提示即文档：函数签名 → OpenAPI schema 自动生成
- Pydantic 模型做请求/响应校验
- 依赖注入系统（Depends）
- 异步原生（async/await，与 httpx/akshare 异步采集契合）

## 在 Vibe-Research 中的使用
- 后端主框架：`backend/app.py` FastAPI 实例
- 路由层：`backend/routers/` 各 router 模块
- 契约层：[[10_Reference/investing/specs/archive/m0-foundation/S007-契约层|S007 契约层]] 用 Pydantic 定义所有数据契约
- 数据层：[[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移|S008]] 后端数据层迁移到 Pydantic 模型
- 与前端 TS 类型对齐：[[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步|S009]] 前后端类型同步

## 相关链接
- [[10_Reference/[[tech-learning/MOC]]
- [[10_Reference/[[tech-learning/languages/python]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/investing/specs/archive/m0-foundation/S007-契约层]]
- [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移]]
- [[10_Reference/investing/specs/archive/m0-foundation/S009-前后端类型同步]]
- [[10_Reference/[[meta/四构件本体方法论]]
