---
type: project
name: obsidian-mcp
title: Obsidian MCP 连接
status: 活跃
created: 2026-09-07
---

# obsidian-mcp

## 项目概述
把 Obsidian vault 暴露为 MCP（Model Context Protocol）服务，让 AI 编码代理（Claude Code / opencode / 其他）能直接读写本知识图谱 vault，实现"代码改了实体/关系/决策，agent 直接同步更新图谱"的闭环。

## 核心能力
- **读**：列出 vault 文件 / 读单个 md / grep 全文
- **写**：创建/更新实体 md（遵循 [[10_Reference/meta/four-construct-ontology|四构件本体]] 模板）
- **结构查询**：解析 [[]] 双链关系图，返回实体邻接

## 与本知识图谱的链接
- 本 vault 即 obsidian-mcp 的数据源：`/Users/lizhiwei/Documents/Obsidian Vault/`
- [[10_Reference/tech-learning/tools/obsidian-git|obsidian-git]] 同步 + obsidian-mcp 读写 = 多 agent 共享同一知识图谱
- 设置文档：`docs/obsidian-mcp-setup.md`

## 与投研的跨领域链接
- [[10_Reference/investing/MOC|投研 MOC]] — agent 可直接查"这个 spec 改了哪些实体"
- [[10_Reference/projects/active/vibe-research|Vibe-Research]] — Vibe-Research 的语义层即本 vault

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/tech-learning/tools/obsidian]]
- [[10_Reference/tech-learning/tools/obsidian-git]]
- [[10_Reference/tech-learning/tools/git]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/meta/four-construct-ontology]]
