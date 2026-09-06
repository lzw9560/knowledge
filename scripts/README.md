# Vault 知识图谱审查脚本

纯标准库（Python 3.10+，无第三方依赖）实现的 Obsidian 知识图谱自动审查脚本。扫描 `10_Reference/investing/` 下的 markdown 实体文件，跑 8 项健康检查，输出 JSON（stdout）+ 人类可读报告（`reviews/<date>-ci-audit.md`）。

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
| 3 | orphan_check | medium | 未被任何 `[[链接]]` 引用过的孤立文件 |
| 4 | broken_link | high | 指向不存在文件的 `[[链接]]` 断链 |
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

- `[[stocks/600519]]` → `10_Reference/investing/stocks/600519.md`（先试加 `.md`，再试原路径）
- `[[stocks/]]` → 文件夹链接，指向 `stocks/index.md`
- `[[path|alias]]` → 别名剥离，取 `path`
- 优先在 `10_Reference/investing/` 下找，再在 vault 根找
- 过滤 ` ```dataview ... ``` ` 代码块内的伪链接（避免把 `FROM "stocks"` 当链接）

## 排除项

- `templates/` 下的模板文件（不参与实体计数/链接统计）
- `reviews/` 下的历史 `*-ci-audit.md` 报告（避免自指噪声，仅保留 `index.md`）
- `index.md` / `MOC.md` / `README.md` 等结构文件（不算实体，不算孤立）

## CI 集成

见 `.github/workflows/vault-audit.yml`：每周日 02:00 北京时间定时跑，发现 critical 问题自动创建 GitHub Issue，报告提交到 `reviews/` 文件夹。
