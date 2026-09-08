# Obsidian 自动审查配置说明

> 知识图谱 skill 的 Obsidian 内实现——"自动触发 C 方案"。
> 用 DataviewJS + Templater 跑 8 项检查，生成审查报告到 `10_Reference/investing/reviews/`。
> 本文档面向 vault 用户，说明如何配置已装插件，让审查一键可跑。

## 前置条件（已装，不重装）

| 插件 | 用途 |
|---|---|
| obsidian-dataview | DataviewJS 引擎，跑 8 项检查 |
| templater-obsidian | 模板引擎，`<% tp.* %>` 替换 + 创建新笔记 |
| obsidian-git | 自动 commit 备份 |
| quickadd | 一键命令触发模板 |

## 1. Templater 配置（模板引擎）

1. 设置 → Templater
2. **Template folder location**：`10_Reference/investing/templates`
3. **Trigger Templater on new file creation**：开启（可选，让新建文件自动套模板）
4. 验证：在 `templates/` 下应能看到 `vault-audit-dataviewjs` 和 `vault-audit-quickadd` 两个模板。

## 2. QuickAdd 配置（一键触发快速审查）

把 `vault-audit-quickadd.md` 注册为 QuickAdd 命令，一键生成快速审查报告：

1. 设置 → QuickAdd
2. **Template Folder**：`10_Reference/investing/templates`（若该项已设则跳过）
3. 在 **Templates** 区点 `Add Template`，命名 `快速审查`，选 `vault-audit-quickadd`
4. 点该模板右侧 ⚙️（齿轮）→ Template Path 填：`10_Reference/investing/templates/vault-audit-quickadd.md`
5. **File Name Format**：开，填 `{date:YYYY-MM-DD}-quick-audit`
6. **Create Folder Path**：`10_Reference/investing/reviews`
7. 回到 QuickAdd 主面板，把 `快速审查` 从 Template 切为 **Macro**（可选，若要绑定多步）——通常 Template 模式即可
8. 关闭设置，命令面板 `Ctrl/Cmd+P` → `QuickAdd: 快速审查` → 回车，报告自动生成到 reviews/

## 3. obsidian-git 自动 commit 配置

设置 → obsidian-git：

| 项 | 值 |
|---|---|
| Auto backup | 开启 |
| Auto backup interval (minutes) | 30 |
| Commit message | `chore: auto-backup ${date}` |
| Auto pull on startup | 开启 |
| Vault backup interval (status bar) | 开启（可选，状态栏显示倒计时） |

> 生成的审查报告会随 obsidian-git 自动提交，无需手动 commit。
> `${date}` 是 obsidian-git 内置变量，会替换为 ISO 日期时间。

## 4. 手动触发完整审查（8 项）

命令面板 → `Templater: Create new note from template` → 选 `vault-audit-dataviewjs`

- 新文件创建位置：当前活动文件夹（建议先打开 `reviews/` 再触发，或配合下面的"自动落盘"设置）
- **推荐：让完整审查自动落到 reviews/**：设置 → Templater → **New file folder** 填 `10_Reference/investing/reviews`
- 文件名建议手动改为 `YYYY-MM-DD-obsidian-audit`

## 5. 审查报告去哪了

| 触发方式 | 落盘位置 | 文件名 |
|---|---|---|
| QuickAdd 快速审查 | `10_Reference/investing/reviews/` | `YYYY-MM-DD-quick-audit.md` |
| Templater 完整审查 | `10_Reference/investing/reviews/`（需设 New file folder） | `YYYY-MM-DD-obsidian-audit.md`（手动改名） |

两类报告的 frontmatter 均 `type: audit`，会被 `reviews/index.md` 的 Dataview 表自动收录：

```dataview
TABLE audit_date AS "日期", findings_count AS "问题数", critical AS "严重", status AS "状态"
FROM "reviews"
WHERE type = "audit"
SORT audit_date DESC
```

## 6. 8 项检查速查

| # | 检查 | 严重级 | 实现 |
|---|---|---|---|
| 1 | summary | — | 各文件夹笔记数统计 + 关系总数 |
| 2 | coverage | low | 标出空/偏少文件夹（<3 条） |
| 3 | orphan_check | high | 无入边的实体 |
| 4 | broken_link | critical | `目标` 不存在的链接 |
| 5 | schema_infer | medium | 实际 frontmatter vs 设计模板偏差 + 必填缺失 |
| 6 | relation_density | medium | 入边 ≥10 的 hub / 0 入 0 出的孤岛 |
| 7 | duplicate_check | medium | 同 code / 同 name 多记录 |
| 8 | stale_check | low | 90 天未更新的实体 |

## 7. 注意事项

- **frontmatter 计数字段保持 0**：DataviewJS 渲染时不回写文件 frontmatter，机器可判计数见报告内"问题清单"区的 DataviewJS 表。
- **DataviewJS 代码块在阅读视图渲染**：编辑视图不渲染，切到阅读视图（`Ctrl/Cmd+E`）才看到表格。
- **首次跑可能慢**：全量扫描所有笔记，大 vault 3-5 秒。
- **`p.file.mtime` 是 Luxon DateTime**：用 `.toMillis()` / `.toFormat("yyyy-MM-dd")`，不要直接比较。
- **链接路径比较需归一化**：Dataview 的 `link.path` 带/不带 `.md` 不一致，代码里用 `.replace(/\.md$/, "").toLowerCase()` 归一化后再比。
- **obsidian-git 自动 commit 与手动改文件冲突**：若审查报告刚生成还没保存完，obsidian-git 就 commit 了，可能漏几秒的改动。建议手动审查后立即 `Ctrl/Cmd+S` 保存，或等下一个 30 分钟周期。
