# 项目上下文 — a-Plate-Sentinel

## 架构
- 模块隔离：`backend/app/modules/{sentiment_dashboard,stock_screener,stock_detail,daily_review,settings}/`，每模块 models/service/api 三件套
- 路由 main.py 统一挂载（prefix=/api/v1）
- Docker Compose：TimescaleDB + Redis + Celery worker/beat + OmniRoute AI 网关 + 前后端

## 关键约定
- STI 7 维加权（MVP sigmoid 占位 → 正式版 252 日滚动分位数）
- 席位标签"历史统计特征，不构成投资建议"；量化输出"疑似度评分"禁确定性
- AI 复盘两段式（规则判事实 + LLM 转写）
- 资金操作"建议+确认"默认，禁自动下单
- 东财走 _em_get 独立节流 1.2s

## 数据源
akshare（主）+ 新浪直连（资金流备胎）+ 东财 emappdata（概念热度，独立风控面）+ Tushare + 东财 push2（板块归属，fallback）

## 已知坑
- ⚠️ 非 git 仓库（无版本控制，改动不可追踪）
- STI 阈值硬编码占位（service.py TODO，待 252 日滚动分位数）
- README 描述 stale（称待补全，代码已实现 MVP）
