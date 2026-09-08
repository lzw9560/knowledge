
# MOC 方法论（Maps of Content）

> 领域无关的导航层方法论。本 vault 的 `MOC.md` 是 MOC 的实例化。

## 核心定义

MOC 是**领域入口 + 导航索引**，不是数据存储。一个 MOC 文件回答三个问题：
1. **这是什么领域**（一句话定义）
2. **这里有什么**（实体类导航表 + Dataview 动态统计）
3. **怎么用**（新建/链接/查询/视图操作指南）

## 与 PARA 的关系

| 方法论 | 职责 | 本 vault 实例 |
|---|---|---|
| PARA | **横向分层**（按可行动性分 Project/Area/Resource/Archive） | `00_Active` / `10_Reference/investing` / `10_Reference/meta` / `20_Archive` |
| MOC | **纵向导航**（每个 Area 内的入口索引） | `10_Reference/investing/MOC.md` / `10_Reference/market_sentiment/DASHBOARD.md` |

两者互补：PARA 管"这文件该放哪一层"，MOC 管"这一层怎么找到具体文件"。

## MOC 的四要素（本 vault 实例化情况）

1. **领域定义段**：`[[10_Reference/investing/MOC]]` 第 1-3 行——"Vibe-Research 项目的语义层"
2. **实体类导航表**：MOC 第 9-24 行——14 类实体 × 文件夹 × 说明 × 数量
3. **关系层说明**：MOC 第 36-39 行——10 个谓词 + 双链 + frontmatter 标注
4. **使用说明**：MOC 第 77-108 行——新建/链接/查询/视图四步操作

## 关键纪律

1. **MOC 不存数据**：MOC.md 只放导航和定义，实体放各自的 `stocks/` `strategies/` 目录。违反此条 → MOC 变成"什么都有"的杂烩。
2. **MOC 链接靠 Dataview 动态**：实体数用 Dataview 长度查询（`length(filter(...))`）而非手写数字（MOC 第 11 行），避免腐化。
3. **每个 Area 一个 MOC**：投研子区一个 `investing/MOC.md`，情绪子区一个 `market_sentiment/DASHBOARD.md`，不交叉。

## 跨领域实例

- [[10_Reference/investing/MOC]] — 投研子区 MOC（实例化最完整）
- H_Reference/market_sentiment/情绪仪表盘]] — 情绪子区 MOC（带 6 层 z-score + 三维向量 + 仓位映射）
- H_Reference/meta/PARA 方法论]] — PARA 方法论（与 MOC 互补的横向分层）

## 来源

- 链接笔记法（Niklas Luhmann Zettelkasten 的现代化变体）
- Nick Milo 的 Linking Your Thinking（LYT）框架
