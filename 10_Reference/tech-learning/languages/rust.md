---
type: language
name: Rust
paradigm: 多范式（系统编程/函数式/并发）
typing: 静态类型（nominal，强类型）
created: 2026-09-07
---

# Rust

## 范式
- 静态类型编译型系统语言，Mozilla 出品（2010，1.0 于 2015）
- 所有权（ownership）+ 借用（borrowing）+ 生命周期（lifetime）三件套，编译期保证内存安全
- 无 GC，无 runtime（except 极小 std），零成本抽象
- 显式优于隐式（编译器严格，`unwrap()` 是反模式）

## 类型系统
- 静态类型 + nominal typing（与 [[languages/go|Go]] 同类）
- 代数数据类型：enum + match（穷尽匹配，编译期保证覆盖）
- trait 系统（类似 interface 但更强大，可泛型约束）
- Result<T, E> / Option<T> 替代异常与 null

## 内存安全
- 所有权模型：每个值有唯一 owner，离开作用域自动释放
- 借用检查器：同时只能有一个可变引用或多个不可变引用
- 无数据竞争（data race）——编译期消除
- 与 C++ 的对比：同等性能，但无 UB（未定义行为）陷阱

## 主要应用领域
- 系统编程（操作系统内核 / 驱动 / 嵌入式）
- WebAssembly（前端高性能模块）
- CLI 工具（ripgrep / fd / bat 都是 Rust）
- 投研可参考场景：高频数据处理引擎、回测核心（对延迟敏感的 hot path）

## 与 Vibe-Research 的关系
- Vibe-Research 当前未用 Rust
- 但前端构建工具 [[tools/vite|Vite]] 底层依赖 esbuild（Go）/ rolldown（Rust 重写）——技术栈间接关联
- 参考架构：[[10_Reference/tech-learning/architecture/event-sourcing|事件溯源]] 的高性能 event store 可用 Rust 实现

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[languages/go]]
- [[languages/python]]
- [[10_Reference/tech-learning/tools/vite]]
- [[10_Reference/tech-learning/architecture/event-sourcing]]
- [[10_Reference/meta/four-construct-ontology]]
