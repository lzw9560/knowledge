---
type: sync-report
date: 2026-09-07
window: "7 days ago"
---

# 增量同步报告（2026-09-07）

> P5 `incremental_sync.py` 生成。同步窗口：`7 days ago`。

## 摘要

- 变更文件总数：**357** 个
- 触发抽取的文件：**61** 个
- 未分类（跳过）：**296** 个
- 执行动作：**3** 次

## 变更文件分类

| 类型 | 数量 | 触发动作 |
|---|---|---|
| spec 文件（specs/SNNN-*/*.md） | 51 | 调 `extract_specs.py` 重抽 stub |
| spec README | 1 | 调 `extract_specs.py` 全量补缺失 |
| 战法卡（backend/strategies/cards/*.md） | 0 | 刷新 `last_synced` + 标待核对 |
| 数据源 .py（backend/data/sources/*.py） | 5 | 调 `extract_relations.py` 重抽关系 |
| Pydantic 模型（backend/models/*.py） | 3 | 调 `extract_code_schema.py` 重抽 schema |
| ARCHITECTURE.md | 1 | 调 `extract_relations.py` 重抽数据流 |
| 其他（未分类） | 296 | — |

## 变更文件清单

### spec 文件（51 个）

- `specs/S107-龙虎榜hithink集成/spec.md`
- `specs/S111-真实裂缝登记册/registry.md`
- `specs/S121-tencent-num-zero-honesty/spec.md`
- `specs/S122-market-emotion-weekend-gate/spec.md`
- `specs/S123-s118-lying-ledger-cleanup/spec.md`
- `specs/S125-s124-high-lying-fix/spec.md`
- `specs/S126-frontend-render-honesty/spec.md`
- `specs/S128-orzero-contract-and-high-fix/spec.md`
- `specs/S129-risk-trio-provenance/spec.md`
- `specs/S130-非承重lying批量修/spec.md`
- ...（省略 41 个）

### spec README（1 个）

- `specs/README.md`

### 数据源 .py（5 个）

- `backend/data/sources/baostock_src.py`
- `backend/data/sources/eastmoney.py`
- `backend/data/sources/hithink_src.py`
- `backend/data/sources/sina.py`
- `backend/data/sources/sina_financial.py`

### Pydantic 模型（3 个）

- `backend/models/global_stock.py`
- `backend/models/quote.py`
- `backend/models/valuation.py`

### 架构文档（1 个）

- `ARCHITECTURE.md`

### 其他（296 个）

- `.gitignore`
- `AGENTS.md`
- `CLAUDE.md`
- `backend/ai/tools/__init__.py`
- `backend/ai/tools/kg_tools.py`
- `backend/ai/tools/stock_tools.py`
- `backend/app.py`
- `backend/astock.py`
- `backend/at_risk.py`
- `backend/attribution.py`
- ...（省略 286 个）

## 执行动作

| # | 脚本 | 触发原因 | 成功 | 输出摘要 |
|---|---|---|---|---|
| 1 | `extract_specs.py` | 52 个 spec 文件变更 | ✅ | 新建 stub：0 条 |
| 2 | `extract_relations.py` | 6 个数据流相关文件变更 | ✅ | 报告：/Users/lizhiwei/Documents/Obsidian Vault/docs/relation-extraction-report.md |
| 3 | `extract_code_schema.py` | 3 个 Pydantic 模型变更 | ✅ | 未映射：12 个模型（嵌套子模型/无独立模板） |

## 冲突处理

同一实体被多个源抽取时，优先级：spec > 代码 AST > 文档注释 > LLM 推断。
本脚本按此优先级顺序调用下游脚本——后执行的不覆盖高优先级内容（下游脚本幂等 + 只补缺失）。

> 所有下游脚本幂等，重跑安全。`last_synced` 字段记录同步时间。
