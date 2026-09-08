---
type: moc
created: 2026-09-07
tags: [moc, projects]
---

# 项目追踪知识图谱

> 项目/行业追踪——进行中项目/待启动/已归档。
> 与 [[00_Active/INDEX]] 活跃层互补：00_Active 管"当前在做什么"，本子区管"项目元数据与跨领域关联"。
> 方法论遵循 [[10_Reference/meta/four-construct-ontology|四构件本体]]——实体/关系/逻辑规则/动作四构件领域无关。

## 实体类导航（本体构件 1：实体）

| 实体类 | 文件夹 | 数量 | 说明 |
|---|---|---|---|
| 项目 | [active/](10_Reference/projects/active/index) | 7 | 进行中 |
| 候选 | [backlog/](10_Reference/projects/backlog/index) | 7 | 待启动 |
| 归档 | [archived/](10_Reference/projects/archived/index) | 1 | 已结束 |

> 实体合计 15 个。

## 种子实体

### 进行中
- [[10_Reference/projects/active/vibe-research]] — Vibe-Research 私人投研助理（本知识图谱的宿主项目）
- [[10_Reference/projects/active/trading-agents]] — TradingAgents A 股深度特化 fork
- [[10_Reference/projects/active/knowledge-graph]] — 本知识图谱项目本身（元项目）
- [[10_Reference/projects/active/a-plate-sentinel]] — A-Plate-Sentinel 板块情绪哨兵
- [[10_Reference/projects/active/daily-stock-analysis]] — 每日股票分析
- [[10_Reference/projects/active/obsidian-mcp]] — Obsidian MCP 连接项目
- [[10_Reference/projects/active/quartz-deploy]] — Quartz 站点部署项目

### 待启动
- [[10_Reference/projects/backlog/quartz-site]] — Quartz 静态站点（刚部署）
- [[10_Reference/projects/backlog/wechat-bot]] — 微信 bot（代码就绪待配置）
- [[10_Reference/projects/backlog/daily-stock-analysis-integration]] — daily-stock-analysis 纳入图谱
- [[10_Reference/projects/backlog/a-plate-sentinel-integration]] — a-Plate-Sentinel 纳入图谱
- [[10_Reference/projects/backlog/incremental-sync-automation]] — 增量同步自动化
- [[10_Reference/projects/backlog/realtime-data-pipeline]] — 实时数据管道（盘中信号生成基础设施）
- [[10_Reference/projects/backlog/llm-extraction-automation]] — LLM 抽取自动化（非结构化→结构化管线）

### 已归档
- [[10_Reference/projects/archived/vibe-research-bakup]] — Vibe-Research 备份仓（S006 重写后归档）

## 与投研的跨领域链接

> 跨域链接判据遵循 [[10_Reference/investing/logic/cross-domain-gate]]（待建）：跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant，否则不建。

- [[10_Reference/investing/MOC]] — Vibe-Research 的投研知识图谱语义层入口
- [[10_Reference/investing/specs/trading-agents-project|trading-agents 项目实体]] — TradingAgents 在投研子区的详细实体笔记
- [[10_Reference/investing/specs/a-plate-sentinel-project|a-Plate-Sentinel 项目实体]] — 关联项目
- [[10_Reference/meta/four-construct-ontology|四构件本体]] — 通用方法论

## 关联子区

- [[10_Reference/tech-learning/MOC]] — 技术学习（项目技术栈）
- [[10_Reference/reading/MOC]] — 读书（项目驱动的阅读）
