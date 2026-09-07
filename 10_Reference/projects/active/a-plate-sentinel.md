---
type: project
name: A-Plate-Sentinel
title: 板块情绪哨兵
status: 活跃
github: lzwfirst/a-plate-sentinel
created: 2026-09-07
---

# A-Plate-Sentinel

## 项目概述
A 股板块情绪监控工具。定时扫描板块涨跌幅/资金流向/涨停家数，输出情绪仪表盘。与 Vibe-Research 互补——Vibe-Research 是单点投研助理，A-Plate-Sentinel 是全市场情绪扫描。

详细实体笔记在投研子区：[[10_Reference/investing/specs/a-plate-sentinel-project|a-Plate-Sentinel 项目实体]]。

## 技术栈
- 语言：[[10_Reference/tech-learning/languages/python|Python]]
- 容器化：[[10_Reference/tech-learning/tools/docker|Docker]] / Docker Compose 本地部署
- 数据源：与 [[10_Reference/projects/active/vibe-research|Vibe-Research]] 共享（[[10_Reference/investing/data-sources/akshare|akshare]] / [[10_Reference/investing/data-sources/eastmoney-push2|东财]] 等）

## 与 Vibe-Research 的关系
- 定位差异：Vibe-Research = 单点深查，A-Plate-Sentinel = 全市场广扫
- 数据共享：共用 4 数据源（mootdx / 东财 / 新浪 / 同花顺）
- 情绪互通：A-Plate-Sentinel 的板块情绪可喂给 Vibe-Research 的 [[10_Reference/market_sentiment/DASHBOARD|市场情绪看板]]

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/investing/specs/a-plate-sentinel-project]]
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/projects/active/vibe-research]]
- [[10_Reference/meta/four-construct-ontology]]
