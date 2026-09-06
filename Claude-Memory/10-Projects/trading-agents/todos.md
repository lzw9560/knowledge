# 待办 — trading-agents

> 从 known issues 提炼（2026-09-03）

- [ ] **版本号对齐**：pyproject.toml=0.2.13 → bump 到 0.3.0（CLAUDE.md 已标 0.3.0）
- [ ] 提交工作树未提交改动（.env.example/CLAUDE.md/Dockerfile/a_stock.py/checkpointer.py 等）
- [ ] mootdx 锁 httpx==0.25.2 与 langchain-google-genai 冲突——考虑解耦或升级路径
- [ ] main.py 默认配 yfinance+NVDA（美股），与 A 股特化定位不符——改默认 config 或移除上游残留示例
- [ ] 同花顺 EPS 接口页面 JS 渲染依赖——v0.3.0 切东财 reportapi 后仍依赖外部页面稳定性
- [ ] PR #18（hejingchi start_date+主题+Windows 字体）与 v0.2.6 冲突未合并——决定合并/rebase/关
- [ ] 开发节奏放缓（近 3 月无 commit）——决定继续维护/归档
