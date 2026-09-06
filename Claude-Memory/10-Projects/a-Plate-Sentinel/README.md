# a-Plate-Sentinel

> A 股情绪看板 + 打板选股 MVP。STI 情绪温度指数（7 维加权）+ 涨停池/连板梯队/封板率/炸板率。
> 路径：`/Users/lizhiwei/project/code/stock/a-Plate-Sentinel`

## 概述
实时情绪看板（模块一，最高优先级）+ 打板选股器（竞价爆量扫描 + 多因子 + 龙虎榜席位引擎 Phase 2）+ 个股深度 + 每日复盘 + 设置。STI = 7 维因子加权合成情绪温度（每 30s 算一次）。

## 技术栈
- 后端：FastAPI + Celery + Redis + TimescaleDB（Docker Compose 一键）
- 前端：Vite（:5173）
- 数据：akshare（主）+ 新浪直连（资金流备胎）+ 东财 emappdata（概念热度）+ Tushare
- AI：OmniRoute 网关 sidecar（259+ 供应商）或直连 DeepSeek/Claude

## 当前状态（2026-09-03）
- **wip/stale**：源文件最后修改 2026-07-18/19（~6 周未动）
- ⚠️ **非 git 仓库**（无 .git，无版本控制，改动不可追踪）——重大风险
- README 自标 MVP 阶段，5 模块骨架 + API 已挂载，但 STI 核心算法仍为 sigmoid 占位（待 252 日滚动分位数动态校准）

## 入口
- Docker：`cp .env.example .env && docker compose up -d` → 后端 :8000/health，前端 :5173
- 后端手动：`cd backend && .venv/bin/python -m uvicorn app.main:app --port 8000 --reload`
- Celery：`celery -A app.core.celery_app worker --beat -Q market_data,sentiment`
- 前端：`cd frontend && npm run dev`

## 关键约定
- 模块隔离：每模块 `backend/app/modules/<name>/{models,service,api}.py` 三件套
- 龙虎榜席位标签须标"历史统计特征，不代表未来行为，不构成投资建议"；量化席位输出"疑似度评分"（0-1），UI 禁确定性措辞
- AI 复盘两段式：规则引擎判事实，LLM 仅转写自然语言（不承担事实判定）
- 资金操作默认"生成建议 + 用户确认"，禁自动下单
- AI 内容须可溯源（前端"查看依据/数据来源"入口）

## CC 记忆
本项目无 CC memory。本目录手动策展。

## 关键决策 / 待办 / 上下文
见 `decisions.md` / `todos.md` / `context.md`
