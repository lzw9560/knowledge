---
type: language
name: Go
paradigm: 多范式（并发优先/面向对象/函数式）
typing: 静态类型（结构化类型，nominal）
created: 2026-09-07
---

# Go

## 范式
- 静态类型编译型语言，Google 出品（2009）
- 并发优先：goroutine + channel 是语言级原语，非库
- 显式优于隐式（gofmt 强制格式，未使用变量是编译错误）
- 接口是隐式实现（duck typing 的静态版本）

## 类型系统
- 静态类型 + nominal typing（与 [[languages/typescript|TS]] 的 structural 相反）
- 无类继承，用 struct embedding 组合
- interface 是隐式满足（struct 实现了 interface 的方法集即算实现）
- 错误处理：error 作为返回值（无异常），`if err != nil` 是惯用法

## 并发模型
- goroutine：轻量级协程（~2KB 栈，可动态增长）
- channel：类型安全的消息传递（CSP 模型）
- select 语句：多路复用 channel
- 与 Rust 的对比：Go 是 GC + runtime，Rust 是无 runtime + 所有权

## 主要应用领域
- 后端服务 / 微服务（Docker / Kubernetes / etcd 都是 Go 写的）
- 云原生基础设施（CNCF 生态主力语言）
- CLI 工具（gh / cobra 生态）
- 投研可参考场景：高性能数据采集网关、调度器（[[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口|S011]] 的备选实现语言）

## 与 Vibe-Research 的关系
- Vibe-Research 当前主语言是 Python + TypeScript，未用 Go
- 但关联基础设施（Docker/K8s）用 Go，技术学习子区记录以备未来选型
- 参考架构：[[10_Reference/tech-learning/architecture/microservices|微服务]] 模式下，Go 常被选为高性能服务节点语言

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[languages/python]]
- [[languages/rust]]
- [[10_Reference/tech-learning/architecture/microservices]]
- [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口]]
- [[10_Reference/meta/four-construct-ontology]]
