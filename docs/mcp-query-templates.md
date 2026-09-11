# 知识图谱 MCP 查询模板

> 10 个常用自然语言查询 → MCP 工具调用 + Dataview 查询对照。
> 配合 `docs/obsidian-mcp-setup.md` 使用。ora-3 §1.4 落地后，agent 会话中遇个股/战法/数据源问题**先 `query_dataview` 再回答**。
>
> 状态：✅ 模板就绪（ora-3 §1.4 MCP 配置执行中）。
> 创建：2026-09-07（Week 2-3）。

---

## 约定

- **MCP 工具**：指 `yanxue06/obsidian-mcp` 提供的 25 个工具（见 `docs/obsidian-mcp-setup.md`）。最常用 3 个：
  - `query_dataview(query)` — 跑 Dataview DQL
  - `find_broken_links()` — 找断链
  - `traverse_graph(path, depth)` — 影响范围分析
- **本仓自带工具**（`backend/ai/tools/kg_tools.py`，不依赖 Obsidian 运行）：
  - `query_kg_entities(entity_type, filter_field?, filter_value?)` — 查实体
  - `query_kg_relations(entity_code, entity_type?)` — 查关系
  - `kg_audit()` — 图谱健康
- **Dataview 查询**：在 Obsidian 里用（需装 Dataview 插件），MCP 侧用 `query_dataview` 工具跑同一 DQL。

---

## 模板 1：查白酒行业所有股票的 PE 排序

**自然语言**：「白酒行业有哪些股票？按 PE 从低到高排」

**MCP 调用**：
```
query_dataview('TABLE code AS "代码", name AS "名称", pe_ttm AS "PE(TTM)" FROM "stocks" WHERE type = "stock" AND industry = "白酒" SORT pe_ttm ASC')
```

**本仓工具**：
```
query_kg_entities(entity_type="stock", filter_field="industry", filter_value="白酒")
```

**备注**：ora-3 §1.4 指出 `pe_ttm` 是静态常识值，MCP 查出的 PE 不可信当实时值。需接 `valuations/` 实体或实时源。

---

## 模板 2：600519 关联哪些战法和数据源

**自然语言**：「贵州茅台关联了哪些战法？数据从哪些源来？」

**MCP 调用**：
```
traverse_graph("10_Reference/investing/stocks/600519", depth=2)
```

**本仓工具**：
```
query_kg_relations(entity_code="600519", entity_type="stock")
```
返回的 `relations` 列表里 `target` 前缀 `strategies/` 即战法，`data-sources/` 即数据源。

**Dataview**（查战法反向匹配，依赖 `matched_strategies` 字段，ora-3 §1.2 已回填）：
```dataview
TABLE name AS "战法", edge_family AS "edge 家族"
FROM "strategies"
WHERE type = "strategy" AND contains(matched_stocks, "600519")
SORT name ASC
```

---

## 模板 3：本周图谱新增了什么

**自然语言**：「这一周知识图谱新增了哪些实体？」

**MCP 调用**：
```
# 先取全量实体，按 created 字段过滤本周
query_dataview('TABLE file.name AS "实体", type AS "类型", created AS "创建日期" FROM "10_Reference/investing" WHERE created >= date(today) - dur(7 days) SORT created DESC')
```

**本仓工具**：
```
kg_audit()  # 返回各类型实体数 + 总数，与上周对比看增量
```

**备注**：CI 审查报告（`reviews/YYYY-MM-DD-ci-audit.md`）每周日自动生成，含本周实体数变化。

---

## 模板 4：找孤立实体

**自然语言**：「图谱里有没有没有任何链接的孤立实体？」

**MCP 调用**：
```
find_broken_links()  # 找断链（含指向不存在目标的链接）
```

**本仓工具 + Dataview 混合**（找零入边零出边的实体）：
```dataview
TABLE file.name AS "实体", type AS "类型"
FROM "10_Reference/investing"
WHERE file.name != "index" AND file.name != "MOC"
  AND length(file.inlinks) = 0 AND length(file.outlinks) = 0
SORT type ASC
```

**备注**：CI 审查第 7 项 `orphan_check`（ora-3 §2.2 已优化）每周日自动跑此检查。

---

## 模板 5：查所有半导体封测的股票

**自然语言**：「半导体封测板块有哪些股票？」

**MCP 调用**：
```
query_dataview('TABLE code AS "代码", name AS "名称", market AS "市场" FROM "stocks" WHERE type = "stock" AND industry = "半导体封测" SORT code ASC')
```

**本仓工具**：
```
query_kg_entities(entity_type="stock", filter_field="industry", filter_value="半导体封测")
```

**备注**：行业分类按证监会口径（`industries/` 目录），`industry` 字段值需与 `industries/*.md` 的 `name` 对齐。

---

## 模板 6：某战法历史匹配过哪些股票

**自然语言**：「首板战法（first_plate）历史上匹配过哪些票？」

**MCP 调用**：
```
query_dataview('TABLE code AS "代码", name AS "名称", industry AS "行业" FROM "stocks" WHERE type = "stock" AND contains(matched_strategies, "first_plate") SORT code ASC')
```

**本仓工具**：
```
query_kg_relations(entity_code="first_plate", entity_type="strategy")
```
返回的 `relations` 里 `target` 前缀 `stocks/` 的即匹配过的股票。

**备注**：依赖 `matched_strategies` frontmatter 字段（ora-3 §1.2 已修复——从正文 `strategies/` 提取回填）。

---

## 模板 7：哪些数据源被最多 spec 依赖（枢纽/单点故障风险）

**自然语言**：「哪些数据源被最多 spec 引用？单点故障风险高的有哪些？」

**Dataview**（按入边数排序）：
```dataview
TABLE length(file.inlinks) AS "被引数", file.name AS "数据源"
FROM "data-sources"
WHERE file.name != "index"
SORT length(file.inlinks) DESC
LIMIT 10
```

**备注**：ora-3 §3.5 的度中心性——入边 Top10 = 真实知识枢纽。审查脚本 `relation_density` 已排除 `index.md`（§2.2 修复）。

---

## 模板 8：查某概念板块的成分股 + 关联战法

**自然语言**：「国产芯片概念有哪些股票？关联哪些战法？」

**MCP 调用**：
```
query_dataview('TABLE code AS "代码", name AS "名称" FROM "stocks" WHERE type = "stock" AND contains(concept, "国产芯片") SORT code ASC')
```

**本仓工具**：
```
query_kg_relations(entity_code="国产芯片", entity_type="concept")
```

**备注**：概念板块在 `concepts/` 目录，股票的 `concept` frontmatter 字段是列表。

---

## 模板 9：查图谱健康度（8 项检查摘要）

**自然语言**：「知识图谱现在健康吗？有多少实体？断链多少？」

**本仓工具**：
```
kg_audit()  # 返回 total_entities + by_type（各类型实体数）
```

**CI 报告**（每周日自动生成）：
```
# 读最新审查报告
read_file("10_Reference/investing/reviews/YYYY-MM-DD-ci-audit.md")
```

**MCP 调用**：
```
find_broken_links()  # 断链数 + 列表
query_dataview('TABLE type, length(rows) AS "数" FROM "10_Reference/investing" WHERE type != null GROUP BY type SORT type')
```

---

## 模板 10：影响范围分析（某数据源/战法变更，影响哪些实体）

**自然语言**：「如果我改了 eastmoney 数据源的接口，会影响哪些 spec 和实体？」

**MCP 调用**：
```
traverse_graph("10_Reference/investing/data-sources/eastmoney-push2", depth=2)
```

**本仓工具**：
```
query_kg_relations(entity_code="eastmoney-push2", entity_type="data_source")
```
返回的 `relations` 是直接关联；`traverse_graph` 的 depth=2 能拿到间接关联（关联的关联）。

**备注**：这是 ora-3 §3.5 的最短路径——改基础设施前做影响范围分析，避免单点故障。审查脚本的第 10/11 项检查（度中心性 + 最短路径，待落地）会算全图。

---

## 使用纪律（ora-3 §1.4 + AGENTS.md）

1. **会话中遇个股/战法/数据源问题，先 `query_dataview` 再回答**，不凭记忆（已写入 AGENTS.md 会话开始协议）。
2. **MCP 查出的 `pe_ttm` / `pb` / `market_cap` 是静态常识值**，不当实时值用（ora-3 §2.5）。时点数据走 `valuations/` 实体或实时源。
3. **agent 通过 MCP 写入只能写 `inbox/`**，不能直接写正式区（ora-3 §6.5）。`move_note` 只对人工开放。
4. **首次会话先调 `get_vault_guide()`** 学规范再写（pipeline §7）。
