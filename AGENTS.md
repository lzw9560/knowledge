# 📖 Obsidian 知识库 — AI Agent 调用规范

> 本文件为所有 AI Agent（Claude Code、OpenCode、Codex）的统一入口。
> **Obsidian管存储，Agent管调用。** 不直接管理文件结构，只按规范读写内容。

## 每次任务的标准启动流程

```
Step 0: 读 00_Active/PROFILE.md           → 了解用户长期偏好、工作习惯、技术栈
Step 1: 读 00_Active/INDEX.md            → 了解当前活跃项目列表
Step 2: 读 10_Reference/index/MASTER_INDEX.md → 了解全局项目目录
Step 3: 根据当前任务，定位到目标项目文件夹
Step 4: 只读该项目的 SUMMARY.md + 最新更新文件
  按需读取：
    - decisions/ 下相关决策
    - comms/ 下相关沟通
    - notes/ 下相关笔记
Step 5: 如任务跨项目，读取所有相关项目笔记并做合并摘要
Step 6: 执行任务
Step 7: 按写入规范写回记忆
```

## 三层架构说明

### 00_Active/ — 活跃层
- **用途**：当前进行中的项目、近30天的决策和沟通、用户画像、每日摘要
- **结构**：
  ```
  00_Active/
  ├── INDEX.md              ← 活跃层索引（Agent入口）
  ├── PROFILE.md            ← 用户长期偏好与工作习惯（每次任务先读）
  ├── PATTERNS.md           ← 常见偏好与反模式（周复盘更新）
  ├── daily/               ← 每日沟通摘要
  │   └── {YYYY-MM-DD}.md
  ├── projects/
  │   └── {项目名}/
  │       ├── SUMMARY.md    ← 项目摘要（必读）
  │       ├── decisions/    ← 项目内决策记录
  │       ├── comms/        ← 项目内沟通记录
  │       └── notes/       ← 项目内笔记
  ├── decisions/            ← 跨项目全局决策
  └── communications/       ← 跨项目沟通记录
  ```

### 10_Reference/ — 参考层
- **用途**：模板、全局索引、跨项目知识库
- **Agent访问**：仅读INDEX和模板，不全量加载

### 20_Archive/ — 归档层
- **用途**：已结束项目、周复盘压缩包
- **Agent访问**：默认不读。仅在明确需要历史上下文时，按索引定位读取

## Token控制策略

| 操作 | Token预算 | 说明 |
|------|-----------|------|
| 任务启动 | ~3K | 读PROFILE + INDEX + MASTER_INDEX |
| 项目定位 | ~2K | 读目标项目SUMMARY + 最新笔记 |
| 任务执行 | 按需 | 只调取相关文件，不读全项目 |
| 写回 | ~1K | 更新SUMMARY + 写新文件 + 每日摘要 |

**单次任务总读取预算：~5-8K tokens**（不含任务本身产出）

## 写入规范

### 任务后写回规则

每次任务完成后，按以下顺序写回：

1. **更新项目 todos** — 完成/新增/阻塞项，更新 SUMMARY.md 的「最后更新」
2. **如有重要决策** — 追加到 `decisions/`，写明日期、选项、理由
3. **当天沟通摘要** — 追加到 `00_Active/daily/{YYYY-MM-DD}.md`（一天一个文件，追加不覆盖）
4. **不重复写入** — 已有内容不重复写；如冲突，保留最新并标注差异
5. **提醒缺失元数据** — 如发现项目缺少 SUMMARY 或关键信息，提醒用户补全

### 新项目
1. 在 `00_Active/projects/{项目名}/` 下创建 `SUMMARY.md`（从 `10_Reference/templates/PROJECT_SUMMARY.md` 复制模板）
2. 创建 `decisions/`、`comms/`、`notes/` 子文件夹
3. 更新 `00_Active/INDEX.md` 和 `10_Reference/index/MASTER_INDEX.md`

### 决策记录
```
文件名：{YYYY-MM-DD}_{简述}.md
路径：00_Active/decisions/ 或 00_Active/projects/{项目名}/decisions/
模板：10_Reference/templates/DECISION.md
```

### 沟通记录
```
文件名：{YYYY-MM-DD}_{对方}_{简述}.md
路径：00_Active/communications/ 或 00_Active/projects/{项目名}/comms/
模板：10_Reference/templates/COMMUNICATION.md
```

### 每日摘要
```
文件名：{YYYY-MM-DD}.md
路径：00_Active/daily/
模板：10_Reference/templates/DAILY_NOTE.md
```
- 每天一个文件，追加写入，不覆盖
- 提炼3-5条可复用记忆
- 清理重复、无信息价值的片段

## 敏感信息处理

- ❌ **禁止写入**：密码、密钥、Token、凭证、个人隐私、客户机密
- 如内容疑似敏感，只写 `[REDACTED]` 并提醒用户手动确认
- 如遇不确定的路径或权限问题，立即告知用户，不强行写入

## 笔记模板规范

所有新建笔记自动套用 YAML Front Matter：
```yaml
---
title:
date: {{date}}
tags: []
status: wip|done|blocked
related: []
---
```

## 定时维护（自动执行，Agent 不需干预）

| 时间 | 任务 | 说明 |
|------|------|------|
| 每天 02:00 | 每日整理 | 更新索引、归档30天前决策/沟通、提炼当日摘要到daily/ |
| 每周日 02:30 | 每周复盘 | 压缩周内容、归档已结束项目、更新PATTERNS.md、生成周报 |

## 禁止事项

- ❌ 一次性读取整个知识库
- ❌ 读取非当前任务相关的项目文件
- ❌ 手动移动文件到归档层（由定时任务处理）
- ❌ 修改架构目录结构（由维护脚本处理）
- ❌ 原样保存敏感信息

## Vault 路径

`/Users/lizhiwei/Documents/Obsidian Vault`
