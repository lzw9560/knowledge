
# Git

## 类别
- 分布式版本控制系统（DVCS）
- 配套：GitHub / GitLab（托管） / gh CLI（GitHub API 封装）

## 核心用途
- 代码版本历史追溯
- 分支协作（feature 分支 / PR / merge / rebase）
- 配套约定：commit message 规范（如 conventional commits）

## 常用命令

### 基础操作
- `git status` — 查看工作树状态
- `git add <file>` / `git add .` — 暂存改动
- `git commit -m "msg"` — 提交
- `git log --oneline -10` — 查看最近提交
- `git diff` — 未暂存改动 / `git diff --staged` — 已暂存改动

### 分支与合并
- `git checkout -b <branch>` — 新建并切换分支
- `git switch <branch>` — 切换分支（现代写法）
- `git merge --squash <branch>` — 压缩合并（一 spec 一 commit）
- `git rebase develop` — 变基到 develop
- `git branch -d <branch>` — 删除已合并分支
- `git stash` / `git stash pop` — 暂存/恢复未提交改动

### 远程协作
- `git fetch` — 拉取远程引用
- `git pull --rebase` — 拉取并变基（避免 merge commit 噪声）
- `git push origin <branch>` — 推送分支
- `gh pr create` — 用 gh CLI 创建 PR

### 历史修复
- `git checkout -- <file>` — 丢弃工作树改动（**慎用，是历次丢改动事故的元凶**）
- `git reset --hard HEAD` — 重置工作树到 HEAD（**高危**）
- `git reflog` — 找回丢失的 commit（最后救命稻草）

## 工作流（Vibe-Research 分级工作流映射）

| 场景 | 命令序列 | 对应级别 |
|---|---|---|
| small 改动 | `git add . && git commit -m "wip: ..." && git push` | 直接 develop |
| medium 改动 | 同上 + issue 层 review（`.scratch/`） | 直接 develop |
| large spec | `git checkout -b feature/SNNN-slug` → 实现 → `git merge --squash` 到 develop | feature 分支 |

**纪律**：勤 commit、最小功能提交、不留长生命未提交工作树。

## 在 Vibe-Research 中的使用
- 仓库：`lzwfirst/Vibe-Research`（私有）
- 分级工作流：见 `AGENTS.md` 分级门（small/medium/large）
- spec 体系：`specs/SNNN-*/` 一 spec 一分支（large）或直接 develop commit（medium/small）
- 配套插件：H_Reference/tech-learning/tools/Obsidian-Git插件|obsidian-git]] 同步本 vault

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- H_Reference/tech-learning/tools/Obsidian-Git插件]]
- H_Reference/tech-learning/tools/GitHub-Actions]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/investing/specs/]]
- H_Reference/meta/四构件本体方法论]]
