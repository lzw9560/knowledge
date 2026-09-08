---
type: tool
name: obsidian-git
category: Obsidian 插件
created: 2026-09-07
---

# obsidian-git

## 类别
- Obsidian 社区插件
- 把 [[10_Reference/[[tech-learning/tools/Git|Git]][[Git]] 集成进 Obsidian，实现 vault 自动同步

## 核心特性
- **自动 commit/push**：定时或文件变更时自动提交
- **vault 版本化**：Obsidian vault 作为 Git 仓库托管（本 vault 在 GitHub `lzw9560/knowledge`）
- **冲突可视化**：在 Obsidian 内解决 merge 冲突
- **多设备同步**：通过 GitHub 中转多设备 vault 一致

## 典型配置
- 自动 commit 间隔：5-10 分钟（避免高频噪声）
- 自动 pull on startup：开启（多设备启动时先同步）
- commit message：可配置模板（如 `vault: auto-save {timestamp}`）
- 忽略：`.obsidian/workspace.json` 等设备态文件

## 在 Vibe-Research 生态中的使用
- 本知识图谱 vault（`/Users/lizhiwei/Documents/Obsidian Vault/`）即用 obsidian-git 同步
- 与 [[10_Reference/[[tech-learning/tools/GitHub-Actions|GitHub]] [[Actions]] 配合：push 后触发 vault-audit / quartz-deploy workflow
- 是知识图谱"代码改了实体/关系/决策，同步更新图谱"承诺的**执行层**——多设备改 vault 不冲突

## 相关链接
- [[10_Reference/[[tech-learning/MOC]]
- [[10_Reference/[[tech-learning/tools/Git]]
- [[10_Reference/[[tech-learning/tools/Obsidian]]
- [[10_Reference/[[tech-learning/tools/GitHub-Actions]]
- [[10_Reference/[[meta/四构件本体方法论]]
