---
type: folder_index
name: 每日情绪日报
created: 2026-09-07
---

# 每日情绪日报

> 盘前/盘中/盘后情绪记录归档。父级：[[10_Reference/market_sentiment/DASHBOARD]]

## 📂 文件列表

```dataview
TABLE WITHOUT ID
  file.link AS "日报",
  file.mtime AS "修改时间"
FROM "10_Reference/market_sentiment/daily"
SORT file.mtime DESC
```
