---
type: audit
audit_date: <% tp.date.now("YYYY-MM-DD") %>
auditor: obsidian-quickadd
scope: 快速
findings_count: 0
critical: 0
high: 0
medium: 0
low: 0
status: 自动审查
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 快速审查：<% tp.date.now("YYYY-MM-DD") %>

> QuickAdd 一键触发，只跑 3 项关键检查：summary / orphan_check / broken_link。
> 完整 8 项见 `templates/vault-audit-dataviewjs`。

## 1. summary（图谱摘要）

```dataviewjs
const base = "10_Reference/investing";
const folders = ["stocks","industries","concepts","indices","reports","analysts","metrics","valuations","dragon-tiger","events","strategies","specs","data-sources","logic","actions","inbox","reviews"];
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const totalLinks = all.reduce((sum, p) => sum + p.file.outlinks.length, 0);
dv.paragraph("**实体笔记总数**：" + all.length + " ｜ **关系总数（出边累计）**：" + totalLinks);
dv.table(["文件夹", "笔记数"], folders.map(f => [f, dv.pages('"' + base + "/" + f + '"').where(p => !p.file.path.includes("/templates/")).length]));
```

## 2. orphan_check（孤立实体）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const orphans = all.where(p => p.file.inlinks.length === 0).sort(p => p.file.path);
dv.paragraph("**无入边实体数**：" + orphans.length);
if (orphans.length === 0) {
  dv.paragraph("✓ 无孤立实体。");
} else {
  dv.table(["文件", "路径", "类型"], orphans.map(p => [p.file.link, p.file.folder, p.type || "—"]));
}
```

## 3. broken_link（断链）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const norm = (s) => String(s).replace(/\.md$/, "").toLowerCase();
const allPaths = new Set(all.map(p => norm(p.file.path)));
const broken = [];
for (const p of all) {
  for (const link of p.file.outlinks) {
    if (!allPaths.has(norm(link.path))) {
      broken.push([p.file.link, link.path, link.display || link.path]);
    }
  }
}
dv.paragraph("**断链数**：" + broken.length);
if (broken.length === 0) {
  dv.paragraph("✓ 无断链。");
} else {
  dv.table(["源文件", "断链目标", "显示文本"], broken);
}
```

## 问题清单

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const norm = (s) => String(s).replace(/\.md$/, "").toLowerCase();
const allPaths = new Set(all.map(p => norm(p.file.path)));
let broken = 0;
for (const p of all) {
  for (const link of p.file.outlinks) {
    if (!allPaths.has(norm(link.path))) broken++;
  }
}
const orphans = all.where(p => p.file.inlinks.length === 0).length;
dv.table(["级别","计数","来源"], [
  ["Critical（断链）", broken, "broken_link"],
  ["High（孤立）", orphans, "orphan_check"]
]);
dv.paragraph("**合计**：" + (broken + orphans) + " ｜ 完整 8 项见 vault-audit-dataviewjs 模板。");
```

## 修复建议

1. **断链（Critical）**：见上 broken_link 表，目标不存在则创建或改链接。
2. **孤立（High）**：见上 orphan_check 表，补入边或确认删除。
