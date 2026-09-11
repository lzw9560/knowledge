---
type: data_source
date: 2026-09-09
description: github zlotus/ash-mcp——baostock+akshare MCP，自带长线价值因子评分+低估筛选+再平衡，最对路fork候选
---

# zlotus/ash-mcp

> 「社区开源实践者」备料（2026-09-09）。10 万个人做长线价值选股，**最短 fork 路径**候选。

## 是什么

github.com/zlotus/ash-mcp — baostock + akshare 的 MCP server，自带**长期持有量化层**：
- `get_long_term_factor_score`：估值/质量/成长/分红 评分
- `get_value_candidates_and_grid`：低估筛选
- 再平衡逻辑

## forkable 程度

**直接用**——是 MCP，与本项目 MCP 栈（vibe-research MCP）天然合拍；baostock+akshare 数据源本项目已集成。license MIT（README 自述，未逐个核实 star/活跃度）。

## 短板

- baostock 分红数据薄 → 叠 [[10_Reference/investing/data-sources/Tushare]] `daily_basic` 补股息率
- 继承其因子选择/rebalance 逻辑（需 review 是否符合 [[00_Active/projects/vibe-research/expert-rounds/红利低波复合因子]] 结论，警惕价值陷阱）

## 退路

fork `hb4ch/tushare-etl`（Tushare→Parquet ETL 当数据骨干，含 daily_basic 全字段+股息率，增量并发，真能跑）+ port 聚宽「红利价值策略」逻辑（股息率排序+PE/ROE/营收增速/净利润四过滤，前5等权月调，宣年化37%未核实）。

## 关联

[[10_Reference/investing/data-sources/baostock（K线日更）]] + [[10_Reference/investing/data-sources/AkShare]] + [[10_Reference/investing/data-sources/Tushare]] + [[00_Active/projects/vibe-research/expert-rounds/红利低波复合因子]] + [[00_Active/projects/vibe-research/expert-rounds/qlib]]（qlib 无价值因子，别 fork 做价值）。
