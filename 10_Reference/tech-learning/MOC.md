---
type: moc
created: 2026-09-07
tags: [moc, tech-learning]
---

# 技术学习知识图谱

> 技术学习领域——编程语言/框架/工具链/架构笔记。
> 与 [[10_Reference/investing/MOC]] 投研子区互为补充：投研子区管"业务知识怎么连"，本子区管"技术栈怎么选与怎么学"。
> 方法论遵循 [[10_Reference/[[meta/四构件本体方法论|四构件本体方法论]][[四构件本体]]——实体/关系/逻辑规则/动作四构件领域无关。

## 实体类导航（本体构件 1：实体）

| 实体类 | 文件夹 | 数量 | 说明 |
|---|---|---|---|
| 语言 | [languages/]([[10_Reference/[[tech-learning/languages/index) |4 | 编程语言（Python/TS/Go/Rust） |]]
| 框架 | [frameworks/]([[10_Reference/[[tech-learning/frameworks/index) |5 | 前后端框架（FastAPI/React/Vite/Tailwind/Pydantic） |]]
| 工具 | [tools/]([[10_Reference/[[tech-learning/tools/index) |8 | 工具链（Docker/Git/uv/Obsidian + Compose/GH Actions/obsidian-git/cron） |]]
| 架构 | [architecture/]([[10_Reference/[[tech-learning/architecture/index) |8 | 架构模式（事件驱动/清洁架构/分层架构/微服务/事件溯源 + CQRS/六边形/Saga） |]]
| 概念 | [concepts/]([[10_Reference/investing/concepts/index) |6 | 编程概念（async-await/类型安全/清洁代码/依赖注入/熔断器/缓存策略） |]]
| 项目 | [projects/]([[10_Reference/[[projects/MOC) |— | 技术项目笔记（区别于]] [[10_Reference/projects/]] 项目追踪元数据） |

> 实体合计 31 个 + 3 个模板 = 34 文件。

## 种子实体

### 语言
- [[10_Reference/[[tech-learning/languages/python]] — Python：动态类型/多范式/数据科学+后端
- [[10_Reference/[[tech-learning/languages/typescript]] — TypeScript：静态类型/前端+全栈
- [[10_Reference/[[tech-learning/languages/go]] — Go：静态类型/并发优先/云原生
- [[10_Reference/[[tech-learning/languages/rust]] — Rust：所有权模型/内存安全/系统编程

### 框架
- [[10_Reference/[[tech-learning/frameworks/fastapi]] — FastAPI：Python/后端/Vibe-Research 用
- [[10_Reference/[[tech-learning/frameworks/react]] — React：JS/前端/Vibe-Research 前端
- [[10_Reference/[[tech-learning/frameworks/vite]] — Vite：前端构建工具/Vibe-Research 用
- [[10_Reference/[[tech-learning/frameworks/tailwindcss]] — Tailwind CSS：原子化 CSS/Vibe-Research 用
- [[10_Reference/[[tech-learning/frameworks/pydantic]] — Pydantic：数据验证/Vibe-Research S007 契约层用

### 工具
- [[10_Reference/[[tech-learning/tools/Docker — Docker：容器化]]
- [[10_Reference/[[tech-learning/tools/Git — Git：版本控制]]
- [[10_Reference/[[tech-learning/tools/uv包管理 — uv：Python 包管理器/Vibe-Research 用]]
- [[10_Reference/[[tech-learning/tools/Obsidian — Obsidian：知识管理工具/本 vault 用]]
- [[10_Reference/[[tech-learning/tools/Docker-Compose — Docker Compose：多容器编排]]
- [[10_Reference/[[tech-learning/tools/GitHub-Actions — GitHub Actions：CI/CD]]
- [[10_Reference/[[tech-learning/tools/Obsidian-Git插件 — obsidian-git：Obsidian git 同步插件]]
- [[10_Reference/[[tech-learning/tools/定时任务 — cron：定时任务]]

### 架构
- [[10_Reference/[[tech-learning/architecture/事件驱动架构 — 事件驱动：S011 调度收口参考]]
- [[10_Reference/[[tech-learning/architecture/清洁架构 — 清洁架构：分层模式/S006 系统重写参考]]
- [[10_Reference/[[tech-learning/architecture/分层架构 — 分层架构：经典 N 层/S006 重写纲领参考]]
- [[10_Reference/[[tech-learning/architecture/微服务架构 — 微服务：S011 调度收口边界参考]]
- [[10_Reference/[[tech-learning/architecture/事件溯源 — 事件溯源：工作流状态机参考]]
- [[10_Reference/[[tech-learning/architecture/cqrs]] — CQRS：命令查询职责分离/S007 契约层读路径参考
- [[10_Reference/[[tech-learning/architecture/六边形架构 — 六边形架构：端口适配器/数据源抽象参考]]
- [[10_Reference/[[tech-learning/architecture/saga]] — Saga：分布式事务/S011 多层调度补偿参考

### 概念
- [[10_Reference/[[tech-learning/concepts/async-await]] — async/await：异步编程/S026 异步化参考
- [[10_Reference/[[tech-learning/concepts/类型安全 — 类型安全：静态类型/S007 Pydantic 契约参考]]
- [[10_Reference/[[tech-learning/concepts/清洁代码 — 清洁代码：代码层清洁/S006 重写参考]]
- [[10_Reference/[[tech-learning/concepts/依赖注入 — 依赖注入：IoC 实现/S015 config 拆分参考]]
- [[10_Reference/[[tech-learning/concepts/熔断器 — 熔断器：容错模式/S022 防封熔断参考]]
- [[10_Reference/[[tech-learning/concepts/缓存策略 — 缓存策略：性能优化/S004 性能优化参考]]

## 与投研的跨领域链接

> 跨域链接判据遵循 [[10_Reference/investing/logic/跨域门控]]（待建）：跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

- [[10_Reference/investing/data-sources/AkShare|AkShare]][[akshare]] — 数据源库，技术学习 + 投研共享
- [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移|S008 后端数据层迁移]] — 架构决策，技术学习参考
- [[10_Reference/[[meta/四构件本体方法论|四构件本体方法论]][[四构件本体]] — 通用方法论，本子区同样遵循

## 关联子区

- [[10_Reference/[[projects/active/Vibe-Research — Vibe-Research 项目追踪（技术栈详情）]]
- [[10_Reference/[[projects/active/TradingAgents]] — TradingAgents 项目追踪
- [[10_Reference/[[reading/MOC]] — 读书笔记（技术书籍）
