---
title: "Codex长期记忆知识库"
type: readme
created: 2026-09-07
tags: [readme, knowledge-base]
---

# 🧠 Codex 长期记忆知识库

> Obsidian管存储，Codex管调用。无限扩容，稳定控Token。

## 三层架构

```
00_Active/      ← 活跃层：当前项目、近期决策、沟通记录
10_Reference/   ← 参考层：模板、索引、跨项目知识
20_Archive/     ← 归档层：已结束项目、周复盘压缩包
```

## 调用规则（Codex必须遵守）

1. **先读索引** — 每次任务开始，只读 `00_Active/INDEX.md` 和 `10_Reference/index/MASTER_INDEX.md`
2. **按需调取** — 根据索引定位到具体项目文件夹，只读该项目的 `SUMMARY.md` 和最新更新文件
3. **禁止全库加载** — 不得一次性读取全库内容
4. **写回规范** — 新决策、沟通记录写入 `00_Active/` 对应文件夹，更新项目 `SUMMARY.md` 的「最后更新」字段
5. **归档由定时任务处理** — Codex不手动归档，由凌晨2点定时任务自动整理

## 文件命名规范

- 项目：`00_Active/projects/{项目名}/` → `SUMMARY.md` + `decisions/` + `comms/` + `notes/`
- 决策：`00_Active/decisions/{YYYY-MM-DD}_{简述}.md`
- 沟通：`00_Active/communications/{YYYY-MM-DD}_{对方}_{简述}.md`

## 定时维护

| 时间 | 任务 | 说明 |
|------|------|------|
| 每天 02:00 | 整理更新 | 合并当天笔记、更新索引、清理临时文件 |
| 每周日 02:30 | 周复盘 | 压缩一周内容、归档已结束项目、生成周报 |

---
创建时间：2026-08-29
