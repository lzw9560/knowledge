# Vibe-Research

> 个人 AI 投研看板（A股/美股/港股）。FastAPI 后端(:8900) + React 19 前端(:5899)。
> 路径：`/Users/lizhiwei/project/code/stock/Vibe-Research`

## CC 记忆（自动）
本项目的 Claude Code 任务记忆在 `../../claude-memory/` 软链（指向
`~/.claude/projects/-Users-lizhiwei-project-code-stock-Vibe-Research/memory/`，
53 条，会话自动加载，CC 写）。**本目录手动策展**，不与 CC 记忆重复——放跨会话提炼的稳定结论。

## 当前状态（2026-09-03）
- §44 verdict：breakout 选股 path_lift<1 robust，不能交易（已降级研究）
- §1.2 诚实收口：strategy winrate 重命名（S147）、C3 嵌套 loop 缓解（run_coro_sync）
- 数据地基：gene_scores / forward_test / limitup_screener

## 关键决策
见 `decisions.md`。
