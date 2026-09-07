# 技术学习知识图谱

> 技术学习领域——编程语言/框架/工具链/架构笔记。
> 与 [[10_Reference/investing/MOC]] 投研子区互为补充：投研子区管"业务知识怎么连"，本子区管"技术栈怎么选与怎么学"。
> 方法论遵循 [[10_Reference/meta/four-construct-ontology|四构件本体]]——实体/关系/逻辑规则/动作四构件领域无关。

## 实体类导航（本体构件 1：实体）

| 实体类 | 文件夹 | 数量 | 说明 |
|---|---|---|---|
| 语言 | [[languages/]] | 4 | 编程语言（Python/TS/Go/Rust） |
| 框架 | [[frameworks/]] | 5 | 前后端框架（FastAPI/React/Vite/Tailwind/Pydantic） |
| 工具 | [[tools/]] | 8 | 工具链（Docker/Git/uv/Obsidian + Compose/GH Actions/obsidian-git/cron） |
| 架构 | [[architecture/]] | 7 | 架构模式（事件驱动/清洁架构/微服务/事件溯源 + CQRS/六边形/Saga） |
| 概念 | [[concepts/]] | 3 | 编程概念（async-await/类型安全/清洁代码） |
| 项目 | [[projects/]] | — | 技术项目笔记（区别于 [[10_Reference/projects/]] 项目追踪元数据） |

> 实体合计 27 个 + 3 个模板 = 30 文件。

## 种子实体

### 语言
- [[languages/python]] — Python：动态类型/多范式/数据科学+后端
- [[languages/typescript]] — TypeScript：静态类型/前端+全栈
- [[languages/go]] — Go：静态类型/并发优先/云原生
- [[languages/rust]] — Rust：所有权模型/内存安全/系统编程

### 框架
- [[frameworks/fastapi]] — FastAPI：Python/后端/Vibe-Research 用
- [[frameworks/react]] — React：JS/前端/Vibe-Research 前端
- [[frameworks/vite]] — Vite：前端构建工具/Vibe-Research 用
- [[frameworks/tailwindcss]] — Tailwind CSS：原子化 CSS/Vibe-Research 用
- [[frameworks/pydantic]] — Pydantic：数据验证/Vibe-Research S007 契约层用

### 工具
- [[tools/docker]] — Docker：容器化
- [[tools/git]] — Git：版本控制
- [[tools/uv]] — uv：Python 包管理器/Vibe-Research 用
- [[tools/obsidian]] — Obsidian：知识管理工具/本 vault 用
- [[tools/docker-compose]] — Docker Compose：多容器编排
- [[tools/github-actions]] — GitHub Actions：CI/CD
- [[tools/obsidian-git]] — obsidian-git：Obsidian git 同步插件
- [[tools/cron]] — cron：定时任务

### 架构
- [[architecture/event-driven]] — 事件驱动：S011 调度收口参考
- [[architecture/clean-architecture]] — 清洁架构：分层模式/S006 系统重写参考
- [[architecture/microservices]] — 微服务：S011 调度收口边界参考
- [[architecture/event-sourcing]] — 事件溯源：工作流状态机参考
- [[architecture/cqrs]] — CQRS：命令查询职责分离/S007 契约层读路径参考
- [[architecture/hexagonal]] — 六边形架构：端口适配器/数据源抽象参考
- [[architecture/saga]] — Saga：分布式事务/S011 多层调度补偿参考

### 概念
- [[concepts/async-await]] — async/await：异步编程/S026 异步化参考
- [[concepts/type-safety]] — 类型安全：静态类型/S007 Pydantic 契约参考
- [[concepts/clean-code]] — 清洁代码：代码层清洁/S006 重写参考

## 与投研的跨领域链接

> 跨域链接判据遵循 [[10_Reference/investing/logic/cross-domain-gate]]（待建）：跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

- [[10_Reference/investing/data-sources/akshare|akshare]] — 数据源库，技术学习 + 投研共享
- [[10_Reference/investing/specs/S008-后端数据层迁移|S008 后端数据层迁移]] — 架构决策，技术学习参考
- [[10_Reference/meta/four-construct-ontology|四构件本体]] — 通用方法论，本子区同样遵循

## 关联子区

- [[10_Reference/projects/active/vibe-research]] — Vibe-Research 项目追踪（技术栈详情）
- [[10_Reference/projects/active/trading-agents]] — TradingAgents 项目追踪
- [[10_Reference/reading/MOC]] — 读书笔记（技术书籍）
