---
type: folder_index
name: 书单
created: 2026-09-07
---

# 书单

> 本目录的导航索引。父级：[[10_Reference/reading/MOC]]

## 📂 文件列表

```dataview
TABLE WITHOUT ID
  file.link AS "文件",
  file.mtime AS "修改时间"
FROM "10_Reference/reading/booklist"
SORT file.mtime DESC
```

## 🔗 关联

- **父级 MOC**：[[10_Reference/reading/MOC]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
