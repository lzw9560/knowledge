---
type: project
name: trading-agents
title: TradingAgents A 股深度特化 fork
status: 活跃
github: lzwfirst/tradingagents-astock
upstream: TauricResearch/TradingAgents
created: 2026-09-07
---

# trading-agents

## 项目概述
基于 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)（65K ⭐）的 A 股深度特化 fork。全 Apache 2.0 开源，pip install 即跑，零外部服务依赖。

详细实体笔记在投研子区：10_Reference/investing/specs/TradingAgents项目|trading-agents 项目实体]]。

## 技术栈
- 语言：[[10_Reference/tech-learning/languages/python|Python]]
- 架构：多 Agent 辩论框架（7 Analyst + Researcher + Trader + Portfolio Manager）
- LLM：双 LLM 设计（quick_think + deep_think）

## 核心改造
| 维度 | 原版 | 本 Fork |
|---|---|---|
| 数据源 | Yahoo Finance / Alpha Vantage | mootdx + 东财 + 新浪 + 同花顺 |
| Analyst | 4 个 | 7 个（+政策/游资/解禁） |
| 交易规则 | 美股 T+0 | A 股 T+1 + 涨跌停 |
| 输出 | 英文 | 中文报告 |

## 与 Vibe-Research 的关系
- 共享 4 数据源（mootdx/东财/新浪/同花顺）
- 定位差异：10_Reference/projects/active/Vibe-Research|Vibe-Research]] 是私人助理单点查询，trading-agents 是完整投资计划生成

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/investing/MOC]]
- 10_Reference/investing/specs/TradingAgents项目]] — 投研子区详细实体笔记
- [[10_Reference/tech-learning/MOC]]
- 10_Reference/meta/四构件本体方法论]]
