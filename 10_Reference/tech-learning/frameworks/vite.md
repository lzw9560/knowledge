---
type: framework
name: Vite
language: TypeScript/JavaScript
category: 前端构建工具
created: 2026-09-07
---

# Vite

## 语言
- [[10_Reference/tech-learning/languages/typescript|TypeScript]] / JavaScript
- 底层：esbuild（Go，开发期依赖预构建）+ Rollup（JS，生产构建）+ rolldown（Rust 重写中）

## 类别
- 前端构建工具 + 开发服务器
- 与 Webpack 的对比：Vite 是 ESM-native（开发期不打包，按需编译），Webpack 是全量打包

## 核心特性
- **dev server 毫秒级启动**：基于浏览器原生 ESM，按请求编译
- **HMR（热模块替换）**：模块粒度热更新，不丢失应用状态
- **预构建（dependency pre-bundling）**：用 esbuild 把 CJS 依赖转 ESM，比 Webpack 快 10-100x
- **生产构建**：用 Rollup 输出，支持代码分割 / tree-shaking
- 插件系统：兼容 Rollup 插件 + Vite 专属插件

## 在 Vibe-Research 中的使用
- 前端构建：`frontend/` 的 `vite.config.ts` 是构建配置入口
- React Fast Refresh：[[10_Reference/tech-learning/frameworks/react|React]] 组件修改即时生效
- 与 [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计|S014 前端 UI 重设计]] 关联：Vite 的快速 HMR 让 UI 迭代效率高
- 类型检查：配合 [[10_Reference/tech-learning/languages/typescript|TypeScript]] 的 `tsc --noEmit`

## 相关链接
- [[10_Reference/reading/MOC]]
- [[10_Reference/tech-learning/frameworks/react]]
- [[10_Reference/tech-learning/languages/typescript]]
- [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计]]
- [[10_Reference/meta/四构件本体方法论]]
