---
type: project
name: a-Plate-Sentinel
title: A股打板情绪监控与投研决策看板
status: MVP骨架
github:
data_source: Tushare
modules: 情绪看板/打板选股/个股深度/每日复盘/设置管理/龙虎榜席位引擎/回测系统/AI复盘Agent
created: 2026-09-07
---

# a-Plate-Sentinel 项目

## 定位
A股打板情绪监控与投研决策看板。Docker Compose 本地部署，8 大模块。面向专业短线/量化投资者，核心是"情绪量化引擎 + 龙虎榜席位行为识别"双轮驱动。

## 与 Vibe-Research 的关系
- 互补：a-Plate-Sentinel 专注情绪监控与打板，Vibe-Research 是全栈投研看板
- 数据源差异：a-Plate-Sentinel 用 [[data-sources/tushare]]，Vibe-Research 用腾讯/东财/akshare 等
- 模块重叠：两者都有"每日复盘"和"龙虎榜"，但实现不同（a-Plate-Sentinel 有席位标签引擎，Vibe-Research 有战法卡 match）

## 8 大模块

### MVP 优先级（Phase 1）
1. **情绪看板**（MVP 优先级 1）— 涨停池、连板梯队、封板率/炸板率、情绪温度指数(STI)。骨架已生成，待补全算法细节与 API/前端
2. **打板选股器**（MVP 优先级 2）— 竞价爆量扫描(09:25:01)、多因子筛选（不含龙虎榜席位引擎）
3. **个股深度分析页**（MVP 优先级 3）— K线/分时/资金/龙虎榜/AI洞察
4. **每日复盘**（MVP 优先级 4）— 自动复盘报告、资讯雷达（不含 AI Agent）
5. **设置与数据管理**（MVP 优先级 5）

### Phase 2（MVP 阶段不提前实现）
6. **龙虎榜席位引擎** — 游资风格标签（历史统计特征）、量化席位疑似度评分
7. **回测系统** — 向量化回测、因子分析
8. **AI 复盘 Agent** — 规则引擎判定 + LLM 转写两段式

## 技术栈
- 前端：React 18 + TypeScript + Zustand + ECharts + Ant Design 5.x + Vite + Socket.IO
- 后端：FastAPI + Python 3.11 + Pandas/NumPy + Celery + Redis
- 数据层：TimescaleDB（Tick级时序）+ PostgreSQL 15（元数据）+ Redis 7（缓存）
- AI层：DeepSeek API / Claude API（结构化输出，禁止自由发挥）
- 部署：Docker Compose 本地优先

## 核心算法要点
- **情绪温度 STI**（模块一）：7 维加权合成，阈值不硬编码，基于历史滚动窗口分位数动态校准
- **龙虎榜席位标签**（模块二）：游资风格标签标注"历史统计特征，不代表未来行为"；量化席位输出"疑似度评分"，UI 禁用确定性语言
- **AI 复盘 Agent**（模块四）：错误模式判定由确定性规则引擎完成，LLM 仅负责结构化事实→自然语言转写

## 数据源
- [[data-sources/tushare]] — Tushare 积分制数据源（行情/财务/指数/期货/基金/可转债）

## 源文件
- README：`/Users/lizhiwei/project/code/stock/a-Plate-Sentinel/README.md`
- AGENTS：`/Users/lizhiwei/project/code/stock/a-Plate-Sentinel/AGENTS.md`
- PRD：`docs/prd.md`（V2.0 完整产品需求文档）
- 模块设计：`docs/module-design.md`（8大模块数据模型/算法伪代码/API/组件树）

## 相关链接
- 同系列项目：[[specs/trading-agents-project]] · [[specs/daily-stock-analysis-project]]
- 上游：[[specs/]] Vibe-Research spec 体系
