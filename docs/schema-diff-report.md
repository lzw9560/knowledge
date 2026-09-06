---
type: report
title: 代码 schema vs vault 模板字段差异报告
created: 2026-09-07
source: scripts/extract_code_schema.py (P3)
---

# 代码 Schema vs Vault 模板字段差异报告

> 本报告由 `scripts/extract_code_schema.py` 自动生成。
> 数据源：Vibe-Research `backend/models/*.py`（Pydantic 模型 AST 扫描） + vault `templates/*.md`（frontmatter 字段）。
>
> **用途**：识别模板字段与代码契约的偏移，驱动模板字段对齐（设计文档 §P3 验收：模板字段数 = Pydantic 模型字段数）。

- 生成时间：2026-09-07
- 扫描模型文件：quote.py, valuation.py, financials.py, report.py, kline.py, fund_flow.py, news.py, seat.py, global_stock.py, market_snapshot.py
- 扫描 Pydantic 模型数：26
- vault 模板数：17

## 已映射模型差异

Pydantic 模型 ↔ vault 模板的字段对齐情况。


| 模型 | 模板 | 匹配字段数 | 模板有代码无（冗余） | 代码有模板无（缺失） |
|---|---|---|---|---|
| Announcement | `event` | 1 | codes, event_type, source, summary | title, type |
| BillboardDetail | `dragon-tiger` | 0 | code, date, institution_net, seats | buy, net, operate_dept_code, operate_dept_name, security_code, sell, trade_date |
| ConceptBlock | `concept` | 1 | code, related_industry | — |
| DragonTiger | `dragon-tiger` | 1 | code, date, seats | buy_seats, records, sell_seats |
| DragonTigerRecord | `dragon-tiger` | 0 | code, date, institution_net, seats | net_buy |
| FinancialPeriod | `metric` | 3 | bvps, code, eps, gross_margin, net_margin, op_cf_ps, roe | accounts_receivable, admin_expense, capex, cash_and_equivalents, eps_basic, eps_diluted, financial_expense, financing_cash_flow, fixed_assets, goodwill, gross_profit, income_tax_expense, inventory, investing_cash_flow, net_change_in_cash, net_profit_attr_parent, net_profit_excluding_nonrecurring, operating_cash_flow, operating_cost, operating_profit, r_and_d_expense, selling_expense, share_capital, shareholders_equity, total_assets, total_current_assets, total_current_liabilities, total_liabilities, total_noncurrent_assets, total_noncurrent_liabilities, total_profit |
| Financials | `metric` | 6 | bvps, code, eps, op_cf_ps | — |
| GlobalMetrics | `metric` | 6 | bvps, code, op_cf_ps, period | debt_ratio, report_date, revenue_yoy |
| News | `event` | 1 | codes, date, event_type, summary | code, content, keywords, market, publish_time, title |
| Quote | `stock` | 6 | concept, industry, list_date, st | amplitude, change_amount, change_pct, float_market_cap, high, is_delayed, last_close, limit_down_price, limit_up_price, low, open, pe_static, price, turnover, turnover_rate, updated_at, vol_ratio, volume |
| Report | `report` | 9 | — | market, updated_at |
| Seat | `dragon-tiger` | 0 | code, date, institution_net, seats | buy_amt, name, net, sell_amt |
| Valuation | `valuation` | 9 | pb_percentile, pe_percentile | analyst_count, cagr_pct, data_status, digest_years, discrepancy, forecast_status, market, market_cap, name, price, updated_at |
| ValuationPercentile | `valuation` | 1 | code, consensus_eps, dividend_yield, forward_pe, pb, pcf_ttm, pe_percentile, pe_ttm, peg, ps_ttm | pe_ttm_percentile |

### 完全对齐的模型（参考）

_（无完全对齐的模型）_

## 未映射到模板的模型

这些 Pydantic 模型在 vault 无对应模板（设计上嵌套子模型或无独立实体文件夹）。
字段列出来作参考，供后续决定是否需要新建模板或并入已有模板。

### `CompanyInfo`（2 字段）

| 字段 | 类型 |
|---|---|
| industry | str |
| listing_date | str |

### `Emotion`（7 字段）

| 字段 | 类型 |
|---|---|
| max_boards | int |
| limit_up_count | int |
| limit_down_count | int |
| seal_rate | float |
| broken_rate | float |
| advance_rate | float |
| ladder | tuple[dict, ...] |

### `EmotionResponse`（8 字段）

| 字段 | 类型 |
|---|---|
| emotion | Emotion |
| lianban_stocks | tuple[LianbanStock, ...] |
| date | str |
| lianban_count | int |
| zb_count | int |
| yzt_count | int |
| cross_source | dict |
| data_source | str |

### `FundFlow`（8 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| date | str |
| main_net | float |
| super_large_net | float |
| large_net | float |
| medium_net | float |
| small_net | float |

### `GlobalStock`（6 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| market | str |
| quote | Quote |
| quote_status | str |
| metrics | GlobalMetrics |

### `IndustrySector`（4 字段）

| 字段 | 类型 |
|---|---|
| name | str |
| change_pct | float |
| up_count | int |
| down_count | int |

### `KLine`（3 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| bars | tuple[KLineBar, ...] |

### `KLineBar`（11 字段）

| 字段 | 类型 |
|---|---|
| date | str |
| open | float |
| close | float |
| high | float |
| low | float |
| volume | int |
| turnover | float |
| amplitude | float |
| ma5 | float |
| ma10 | float |
| ma20 | float |

### `LianbanStock`（8 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| boards | int |
| price | float |
| pct | float |
| amount | float |
| float_cap | float |
| industry | str |

### `MarketSnapshot`（3 字段）

| 字段 | 类型 |
|---|---|
| emotion | Emotion |
| sectors | tuple[Sector, ...] |
| updated | str |

### `Sector`（6 字段）

| 字段 | 类型 |
|---|---|
| name | str |
| pct | float |
| net | float |
| inflow | float |
| outflow | float |
| firms | int |

### `ZTPoolItem`（13 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| boards | float |
| seal_time | float |
| broken_count | float |
| limit_price | float |
| open | float |
| seal_amount | float |
| float_shares | float |
| prev_close | float |
| limit_pct | float |
| industry | str |
| pool_date | str |

## 完整 Schema 速览

所有 Pydantic 模型的字段+类型一览（完整 JSON 见 `docs/code-schema.json`）。

### `Announcement`（3 字段）

| 字段 | 类型 |
|---|---|
| title | str |
| date | str |
| type | str |

### `BillboardDetail`（7 字段）

| 字段 | 类型 |
|---|---|
| buy | float |
| sell | float |
| net | float |
| security_code | str |
| trade_date | str |
| operate_dept_name | str |
| operate_dept_code | str |

### `CompanyInfo`（2 字段）

| 字段 | 类型 |
|---|---|
| industry | str |
| listing_date | str |

### `ConceptBlock`（1 字段）

| 字段 | 类型 |
|---|---|
| name | str |

### `DragonTiger`（4 字段）

| 字段 | 类型 |
|---|---|
| records | tuple[DragonTigerRecord, ...] |
| institution_net | float |
| buy_seats | tuple[Seat, ...] |
| sell_seats | tuple[Seat, ...] |

### `DragonTigerRecord`（1 字段）

| 字段 | 类型 |
|---|---|
| net_buy | float |

### `Emotion`（7 字段）

| 字段 | 类型 |
|---|---|
| max_boards | int |
| limit_up_count | int |
| limit_down_count | int |
| seal_rate | float |
| broken_rate | float |
| advance_rate | float |
| ladder | tuple[dict, ...] |

### `EmotionResponse`（8 字段）

| 字段 | 类型 |
|---|---|
| emotion | Emotion |
| lianban_stocks | tuple[LianbanStock, ...] |
| date | str |
| lianban_count | int |
| zb_count | int |
| yzt_count | int |
| cross_source | dict |
| data_source | str |

### `FinancialPeriod`（34 字段）

| 字段 | 类型 |
|---|---|
| period | str |
| revenue | float |
| net_profit | float |
| net_profit_attr_parent | float |
| net_profit_excluding_nonrecurring | float |
| operating_cost | float |
| gross_profit | float |
| selling_expense | float |
| admin_expense | float |
| financial_expense | float |
| r_and_d_expense | float |
| operating_profit | float |
| total_profit | float |
| income_tax_expense | float |
| eps_basic | float |
| eps_diluted | float |
| total_assets | float |
| total_liabilities | float |
| shareholders_equity | float |
| total_current_assets | float |
| total_noncurrent_assets | float |
| total_current_liabilities | float |
| total_noncurrent_liabilities | float |
| cash_and_equivalents | float |
| accounts_receivable | float |
| inventory | float |
| fixed_assets | float |
| goodwill | float |
| share_capital | float |
| operating_cash_flow | float |
| investing_cash_flow | float |
| financing_cash_flow | float |
| net_change_in_cash | float |
| capex | float |

### `Financials`（6 字段）

| 字段 | 类型 |
|---|---|
| revenue | float |
| net_profit | float |
| roe | float |
| gross_margin | float |
| net_margin | float |
| period | str |

### `FundFlow`（8 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| date | str |
| main_net | float |
| super_large_net | float |
| large_net | float |
| medium_net | float |
| small_net | float |

### `GlobalMetrics`（9 字段）

| 字段 | 类型 |
|---|---|
| report_date | str |
| revenue | float |
| revenue_yoy | float |
| net_profit | float |
| eps | float |
| roe | float |
| gross_margin | float |
| net_margin | float |
| debt_ratio | float |

### `GlobalStock`（6 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| market | str |
| quote | Quote |
| quote_status | str |
| metrics | GlobalMetrics |

### `IndustrySector`（4 字段）

| 字段 | 类型 |
|---|---|
| name | str |
| change_pct | float |
| up_count | int |
| down_count | int |

### `KLine`（3 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| bars | tuple[KLineBar, ...] |

### `KLineBar`（11 字段）

| 字段 | 类型 |
|---|---|
| date | str |
| open | float |
| close | float |
| high | float |
| low | float |
| volume | int |
| turnover | float |
| amplitude | float |
| ma5 | float |
| ma10 | float |
| ma20 | float |

### `LianbanStock`（8 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| boards | int |
| price | float |
| pct | float |
| amount | float |
| float_cap | float |
| industry | str |

### `MarketSnapshot`（3 字段）

| 字段 | 类型 |
|---|---|
| emotion | Emotion |
| sectors | tuple[Sector, ...] |
| updated | str |

### `News`（7 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| title | str |
| content | str |
| publish_time | str |
| source | str |
| keywords | str |

### `Quote`（24 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| name | str |
| price | float |
| change_pct | float |
| change_amount | float |
| volume | int |
| turnover | float |
| market_cap | float |
| float_market_cap | float |
| pe_ttm | float |
| pb | float |
| turnover_rate | float |
| amplitude | float |
| limit_up_price | float |
| limit_down_price | float |
| last_close | float |
| open | float |
| high | float |
| low | float |
| vol_ratio | float |
| pe_static | float |
| updated_at | str |
| is_delayed | bool |

### `Report`（11 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| title | str |
| org | str |
| researcher | str |
| publish_date | str |
| report_type | ReportType |
| rating_change | str |
| target_price | float |
| eps_forecast | float |
| updated_at | str |

### `Seat`（4 字段）

| 字段 | 类型 |
|---|---|
| name | str |
| buy_amt | float |
| sell_amt | float |
| net | float |

### `Sector`（6 字段）

| 字段 | 类型 |
|---|---|
| name | str |
| pct | float |
| net | float |
| inflow | float |
| outflow | float |
| firms | int |

### `Valuation`（20 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| market | Market |
| name | str |
| price | float |
| market_cap | float |
| pe_ttm | float |
| pb | float |
| ps_ttm | float |
| pcf_ttm | float |
| dividend_yield | float |
| peg | float |
| forward_pe | float |
| consensus_eps | float |
| cagr_pct | float |
| digest_years | float |
| analyst_count | int |
| updated_at | str |
| discrepancy | list[dict] |
| data_status | str |
| forecast_status | str |

### `ValuationPercentile`（2 字段）

| 字段 | 类型 |
|---|---|
| pe_ttm_percentile | float |
| pb_percentile | float |

### `ZTPoolItem`（13 字段）

| 字段 | 类型 |
|---|---|
| code | str |
| name | str |
| boards | float |
| seal_time | float |
| broken_count | float |
| limit_price | float |
| open | float |
| seal_amount | float |
| float_shares | float |
| prev_close | float |
| limit_pct | float |
| industry | str |
| pool_date | str |

## Vault 模板字段清单（参考）

所有实体模板的 frontmatter 字段（去掉 type/created 元字段）。

- **action**: action_id, action_type, trigger, target, audit
- **agent**: name, project, origin_project, role, data_sources, debates_with
- **analyst**: name, org, coverage_count
- **concept**: code, name, related_industry
- **data-source**: name, layer, endpoint, rate_limit, fallback
- **dragon-tiger**: code, date, institution_net, seats
- **event**: date, event_type, codes, source, summary
- **inbox-item**: entity_type, name, code, confidence, source, quality_score, completeness, consistency, linkage, traceability, approved, approved_date, rejected, reject_reason
- **index**: code, name, market
- **industry**: code, name, source
- **logic**: rule_id, rule_type, target_entity, severity, condition, action_on_violation, source
- **metric**: code, period, revenue, net_profit, roe, gross_margin, net_margin, eps, bvps, op_cf_ps
- **report**: code, title, org, researcher, publish_date, report_type, rating_change, target_price, eps_forecast
- **spec**: number, title, status
- **stock**: code, name, market, industry, concept, list_date, st, pe_ttm, pb, market_cap
- **strategy**: name, edge_family, match_conditions, entry_conditions, exit_conditions
- **valuation**: code, pe_ttm, pb, ps_ttm, pcf_ttm, dividend_yield, peg, forward_pe, consensus_eps, pe_percentile, pb_percentile

## 修复建议

### 模板有代码无（冗余字段）

- **处置**：从模板 frontmatter 删掉代码契约已不承载的字段，或在模板注释标注「由 frontmatter 以外的段落承载」。
- 典型场景：strategy 模板的 `entry_conditions`/`exit_conditions`/`match_conditions` 实际由正文标题承载（vault_audit.py 的 BODY_HEADING_FOR_FIELD 机制），frontmatter 字段是冗余的。

### 代码有模板无（缺失字段）

- **处置**：在模板 frontmatter 补上代码契约实际承载的字段。
- 优先级：先补 code/name 等规范标识符字段，再补业务字段。
- 注意：并非所有代码字段都要进模板——嵌套子模型（如 KLineBar）无独立 vault 实体，不需要模板。

### 未映射模型

- 若该模型对应独立 vault 实体类型，考虑新建模板。
- 若为嵌套子模型（如 KLineBar、Seat、GlobalMetrics），并入父实体模板或单独建模板均可，按是否需要独立查询决定。
