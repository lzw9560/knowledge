---
type: project
name: vibe-research
title: Vibe-Research 个人 AI 投研看板
status: 活跃
github: lzw9560/Vibe-Research
tech_stack: FastAPI + React 19 + Vite + TypeScript
data_sources: 16
spec_count: 109
strategy_count: 12
created: 2026-09-07
---

# Vibe-Research 项目

## 定位

个人 AI 投研看板（A股/美股/港股/韩股）。本地自托管，FastAPI 后端(:8900) + React 19/Vite 前端(:5899)。

定位：把客观数据配齐摆好看板，三条出口接用户自己的 AI 做分析。

## 核心能力

- **数据层**：15+ 公开数据源，五层回退架构，em_get 统一限流防封
- **模型层**：12 个 Pydantic 契约模型（Quote/Valuation/Financials/Report/...）
- **策略层**：12 战法 + 双 pipeline（涨停/非涨停）+ 候选池漏斗 + 价值漏斗
- **AI 层**：三出口（订阅/API/MCP）共用工具注册表，多空辩论/反思审计
- **前端层**：30+ 投研视图，玻璃暖橙主题
- **治理层**：109 SDD spec，分级工作流，弱合规框架

## 与其他项目的关系

- [[specs/trading-agents-project]] — 多 Agent 辩论框架，互补
- [[specs/daily-stock-analysis-project]] — 每日股票分析，dragon_head 战法引用它
- [[specs/a-plate-sentinel-project]] — 情绪监控看板，Tushare 数据源互补

## 核心产出（图谱内）

- 109 个 spec 决策实体（本图谱默认归属项目）
- 16 数据源实体
- 12 战法卡
- 5 DEC 决策记录
- 7 AI 角色（trading-agents 纳入时灌入）

## 源文件

- 仓库：`/Users/lizhiwei/project/code/stock/Vibe-Research`
- ARCHITECTURE：`ARCHITECTURE.md`
- VISION：`VISION.md`
- 决策日志：`specs/decision-log.md`
- Spec 索引：`specs/README.md`
