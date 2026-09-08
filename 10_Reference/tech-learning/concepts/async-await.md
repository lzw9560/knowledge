---
type: concept
name: async/await
category: 编程概念
created: 2026-09-07
---

# async/await（异步编程）

## 类别
- 异步编程语法糖（多语言通用：Python/TS/JS/Rust/C#）
- 与回调/Promise/Future/Coroutine 同族——async/await 是其中最易读的形式

## 核心特性
- **语法糖**：`async def` / `async function` 定义异步函数，`await` 暂停当前协程直到 awaitable 完成
- **非阻塞**：协程让出控制权时事件循环可调度其他任务，不阻塞线程
- **单线程并发**：async/await 在单线程内实现并发（IO 密集型高效），CPU 密集型仍需多进程
- **事件循环**：asyncio（Python）/ libuv（Node）等事件循环是底座

## 与其他并发模型的对比
| 模型 | 并发单位 | 上下文切换 | 适用 |
|---|---|---|---|
| 多进程 | 进程 | OS 调度 | CPU 密集 |
| 多线程 | 线程 | OS 调度 | 阻塞 IO 混合 |
| async/await | 协程 | 用户态 | IO 密集 |

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/archive/m1-workflow/S026-pre-market-async|S026 pre-market async]] — 盘前数据拉取从同步改 async/await，多数据源并发拉取
- [[10_Reference/tech-learning/frameworks/fastapi|FastAPI]] 基于 Starlette + async/await，路由天然异步
- 10_Reference/tech-learning/architecture/事件驱动架构|[[事件驱动]] 架构的运行时即基于 async 事件循环

## 反模式（避免）
- 在 async 函数中调同步阻塞 IO（如 `requests.get`）——会阻塞整个事件循环
- 应改用异步库（`httpx.AsyncClient` / `aiofiles`）

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/frameworks/fastapi]]
- 10_Reference/tech-[[learning/architecture/事件驱动架构]]
- [[10_Reference/investing/specs/archive/m1-workflow/S026-pre-market-async]]
- [[10_Reference/meta/四构件本体方法论]]
