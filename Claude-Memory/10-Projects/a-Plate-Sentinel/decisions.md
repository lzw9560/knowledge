# 决策记录 — a-Plate-Sentinel

> 从 AGENTS.md + README + 源码提炼（2026-09-03）

- **STI 7 维加权合成**：seal_rate/board_promotion_rate 各 0.20，3 项 +0.15，open_board_rate -0.15，big_drop_count -0.10。MVP 用 sigmoid 占位归一化，正式版须改近 252 交易日滚动分位数动态校准（禁硬编码阈值）
- **MVP 优先级**：情绪看板 → 选股器（不含席位引擎）→ 个股深度 → 复盘（不含 AI Agent）→ 设置。席位引擎/回测/AI 复盘 Agent/动态止盈止损一律 Phase 2
- **模块隔离架构**：每功能模块 `backend/app/modules/<name>/`，含 models/service/api 三件套，路由 main.py 统一挂载（prefix=/api/v1）
- **龙虎榜席位标签**：UI 须标"历史统计特征，不构成投资建议"；量化输出"疑似度评分"（0-1），禁确定性措辞
- **AI 复盘两段式**：规则引擎判事实，LLM 仅转写
- **资金操作默认"建议+确认"**：禁自动下单/清仓默认路径；AI 内容须可溯源
- **数据源分层**：akshare 主 + 新浪直连资金流备胎 + 东财 emappdata 概念热度（独立风控面）+ push2 板块归属（fallback）；东财走 _em_get 独立节流 1.2s
- **AI 层双路径**：OmniRoute 网关 sidecar（启用后忽略直连）或直连 DeepSeek/Claude；结构化输出，禁自由发挥 Prompt
