---
type: framework
name: Tailwind CSS
language: CSS（原子化生成）
category: 前端样式框架
created: 2026-09-07
---

# Tailwind CSS

## 语言
- CSS（通过 PostCSS 处理）
- 配置文件用 JS/TS（`tailwind.config.ts`）

## 类别
- 原子化 CSS 框架（utility-first）
- 与 Bootstrap / Material UI 的对比：那些是"组件库"，Tailwind 是"原子类组合系统"——不提供 `.btn`，提供 `bg-blue-500 px-4 py-2 rounded`

## 核心特性
- **原子工具类**：`flex`、`pt-4`、`text-center`、`rotate-90` 等单一职责类
- **JIT 模式**：按需生成，最终 CSS 体积通常 < 10KB（vs 全量 100KB+）
- **设计令牌**：颜色 / 间距 / 字体在 config 中定义，全站统一
- **响应式前缀**：`md:`、`lg:` 等断点前缀，移动优先
- **暗色模式**：`dark:` 前缀，配合 `class` 策略切换

## 在 Vibe-Research 中的使用
- 前端样式方案：`frontend/` 用 Tailwind 替代手写 CSS
- 与 [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计|S014 前端 UI 重设计]] 关联：S014 的视觉重构基于 Tailwind 原子类实现
- 配合 [[10_Reference/tech-learning/frameworks/react|React]]：组件样式直接写在 className，无 CSS-in-JS 运行时开销
- 配合 [[10_Reference/tech-learning/frameworks/vite|Vite]]：PostCSS 插件链处理

## 相关链接
- [[10_Reference/reading/MOC]]
- [[10_Reference/tech-learning/frameworks/react]]
- [[10_Reference/tech-learning/frameworks/vite]]
- [[10_Reference/investing/specs/archive/m0-foundation/S014-前端UI重设计]]
- [[10_Reference/meta/四构件本体方法论]]
