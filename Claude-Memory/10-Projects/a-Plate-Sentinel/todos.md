# 待办 — a-Plate-Sentinel

> 从 known issues 提炼（2026-09-03）

- [ ] ⚠️ **初始化 git 仓库**（当前非 git，无版本控制——重大风险，改动不可追踪）
- [ ] **STI 阈值动态校准**：硬编码占位（高潮≥80/启动≥60/分歧≥40/冰点≥20/强退潮<20）→ 改近 252 交易日滚动分位数（service.py 有显式 TODO）
- [ ] README 与代码对齐（README 称"待补全 _extract_factors/_normalize"但代码已实现 MVP 版本）
- [ ] STI 回测方案落地（docs/sti-backtest-plan.md：验证极端值 <20 冰点 / >80 沸点次日信号信息含量，不优化权重不做选股）
- [ ] Phase 2：龙虎榜席位引擎 / 回测 / AI 复盘 Agent / 动态止盈止损
