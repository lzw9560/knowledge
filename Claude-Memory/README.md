# Claude-Memory（跨项目 / 跨工具记忆库）

本目录是 Obsidian 下的跨项目记忆浏览 + 手动策展层。**CC 的任务记忆仍由 Claude Code
自动管理**（`~/.claude/projects/<scope>/memory/`，会话自动加载）；本目录不替代它。

## 结构

- `claude-memory/` → **软链** 指向 CC 的 Vibe-Research memory（53 条，Obsidian 直接浏览 / 别的工具读）
- `00-Profile/` — 长期偏好、工作习惯、技术栈、沟通风格（手动策展）
- `10-Projects/<项目>/` — 各项目 README / decisions / todos / context（手动策展）
- `20-Daily/<YYYY-MM-DD>.md` — 当日沟通摘要、决策、临时上下文
- `30-Weekly/` — 每周复盘、经验沉淀、冗余清理记录
- `40-Archive/` — 已归档项目与过期笔记

## 读写策略（重要）

- **CC 不自动读本目录**（避双读双写 drift）。CC 任务记忆 = `~/.claude` store（自动加载）。
- 本目录**手动策展**：你或周期性复盘时写。要 CC 参考某条，任务里指明文件路径。
- 跨工具读：别的工具读 `claude-memory/` 软链即可访问 CC 记忆。
- 敏感信息（密码/密钥/Token/凭证/隐私）一律不存；疑似只写 `[REDACTED]`。

## 笔记模板

见 `00-Profile/note-template.md`。
