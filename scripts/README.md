# Vault 知识图谱审查脚本

本目录脚本均为纯标准库（Python 3.10+，无第三方依赖）实现。除 `vault_audit.py` 跑 8 项健康检查外，另有 LLM 知识抽取 pipeline 的 P1-P3 阶段脚本（设计文档 `docs/knowledge-graph-llm-pipeline.md`）。

## 脚本一览

| 脚本 | 阶段 | 用途 |
|---|---|---|
| `vault_audit.py` | — | 8 项知识图谱健康检查，输出 JSON + 报告 |
| `init_entity_dictionary.py` | P1 | 扫 vault .md frontmatter 建 `.entity-dictionary.json` 实体词典 |
| `extract_specs.py` | P2 | 从 Vibe-Research `specs/README.md` 批量抽取 spec 实体到 vault |
| `extract_code_schema.py` | P3 | 从 Pydantic 模型 AST 提 schema，对比模板字段输出差异报告 |

所有脚本在 vault 根目录运行：`python3 scripts/<script>.py`。

---

## vault_audit.py

扫描 `10_Reference/investing/` 下的 markdown 实体文件，跑 8 项健康检查，输出 JSON（stdout）+ 人类可读报告（`reviews/<date>-ci-audit.md`）。

## 运行方式

```bash
# 在 vault 根目录下运行
python scripts/vault_audit.py

# 不输出 JSON（仅写报告文件）
python scripts/vault_audit.py --quiet

# 指定 vault 根目录
python scripts/vault_audit.py --root /path/to/vault
```

## 退出码

- `0`：无 critical 级问题
- `1`：有 critical 级问题（coverage 完全缺失类型 / duplicate 同 code 多份）

## 8 项检查

| # | 检查 | 严重级 | 说明 |
|---|---|---|---|
| 1 | summary | — | 实体总数 + 各类型分布 + 各文件夹分布 |
| 2 | coverage | critical | 各实体类型数量对比，标完全缺失（0 个）的类型 |
| 3 | orphan_check | medium | 未被任何 `链接` 引用过的孤立文件 |
| 4 | broken_link | high | 指向不存在文件的 `链接` 断链 |
| 5 | schema_infer | high | 实体 frontmatter 字段 vs `templates/` 模板字段，标缺失 |
| 6 | relation_density | low | 每个文件被引用次数（入边数），标异常多的 hub |
| 7 | duplicate_check | critical | 按 frontmatter `code` 字段分组，同 code 多份记录 |
| 8 | stale_check | low | `git log` 取最后提交时间，标 90 天未更新 |

## 严重级判定

- **critical**：coverage 某类型 0 个 / duplicate 同 code 多份
- **high**：broken_link 断链 / schema 缺失必填字段
- **medium**：orphan 孤立实体 / coverage 严重不均衡（>10x 且最小 <5）
- **low**：stale 90+ 天未更新 / relation_density 入边异常多（>mean+3σ 且 ≥20）

## 输出

### 1. JSON（stdout）

```json
{
  "audit_date": "2026-09-06",
  "report_path": "10_Reference/investing/reviews/2026-09-06-ci-audit.md",
  "findings_summary": { "total": {"critical": N, "high": N, ...}, "by_check": {...} },
  "checks": { "summary": {...}, "coverage": {...}, ... },
  "findings": [{"check": "...", "severity": "...", "message": "...", "entity": "..."}]
}
```

### 2. 人类可读报告

写到 `10_Reference/investing/reviews/<YYYY-MM-DD>-ci-audit.md`，格式对齐 `templates/audit.md`：
- frontmatter（含 `type: audit` + 各严重级计数）
- 8 项检查结果
- 问题清单（按严重级分组）
- 修复建议
- 跟踪 checklist

## 链接解析规则

- `[[10_Reference/investing/stocks/600519]]` → `10_Reference/investing/stocks/600519.md`（先试加 `.md`，再试原路径）
- `[[10_Reference/investing/stocks/index|stocks/]]` → 文件夹链接，指向 `stocks/index.md`
- `[[scripts/README.md|alias]]` → 别名剥离，取 `path`
- 优先在 `10_Reference/investing/` 下找，再在 vault 根找
- 过滤 ` ```dataview ... ``` ` 代码块内的伪链接（避免把 `FROM "stocks"` 当链接）

## 排除项

- `templates/` 下的模板文件（不参与实体计数/链接统计）
- `reviews/` 下的历史 `*-ci-audit.md` 报告（避免自指噪声，仅保留 `index.md`）
- `index.md` / `MOC.md` / `README.md` 等结构文件（不算实体，不算孤立）

## CI 集成

见 `.github/workflows/vault-audit.yml`：每周日 02:00 北京时间定时跑，发现 critical 问题自动创建 GitHub Issue，报告提交到 `reviews/` 文件夹。

---

## init_entity_dictionary.py（P1）

扫描 vault 的 `10_Reference/investing/` 下所有 .md 文件 frontmatter，把 code/name/number/endpoint/action_id/rule_id/title + 文件名 stem 收为别名，归一到对应实体文件路径，输出到 `10_Reference/investing/.entity-dictionary.json`。

```bash
python3 scripts/init_entity_dictionary.py            # 在 vault 根目录下运行
python3 scripts/init_entity_dictionary.py --quiet
```

- 跳过 `templates/`、`reviews/`、`inbox/` 与 `index.md` / `MOC.md` / `README.md`
- 同别名冲突：first-write-wins，记录到 `conflicts` 字段
- 产出：`.entity-dictionary.json`（含 `aliases` / `by_type` / `stats` / `conflicts`）

## extract_specs.py（P2）

从 Vibe-Research `specs/README.md` 的 spec 索引表（S001-S166）批量抽取 spec 实体到 vault `specs/`。

```bash
python3 scripts/extract_specs.py
python3 scripts/extract_specs.py --dry-run          # 只打印不写
```

- 对每个 spec 提取编号/标题/状态/一句话摘要
- 检查 vault specs/ 是否已有该编号（按 SNNN 前缀匹配）→ 已有则跳过
- 没有则用 `templates/spec.md` 的 frontmatter 建 stub 文件（`SNNN-标题.md`）
- 幂等：重跑只补缺失，不覆盖已有

## extract_code_schema.py（P3）

从 Vibe-Research `backend/models/*.py` 的 Pydantic 模型用 `ast` 标准库提取字段名+类型注解，对比 vault `templates/*.md` 的 frontmatter 字段，输出差异报告。

```bash
python3 scripts/extract_code_schema.py
```

- 扫描 10 个模型文件：quote/valuation/financials/report/kline/fund_flow/news/seat/global_stock/market_snapshot
- 类型注解用 `ast.unparse` 还原，剥 `Optional` / `| None` 简化
- 模型 ↔ 模板映射硬编码（`MODEL_TO_TEMPLATE`）
- 差异分类：模板有代码无（冗余）/ 代码有模板无（缺失）
- 产出：`docs/code-schema.json` + `docs/schema-diff-report.md`
