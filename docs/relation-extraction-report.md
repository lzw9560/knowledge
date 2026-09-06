---
type: pipeline-report
pipeline: P4-relation-extraction
date: 2026-09-07
---

# 关系抽取报告（2026-09-07）

> P4 `extract_relations.py` 生成。从 Vibe-Research 代码 + ARCHITECTURE.md + vault specs 抽取数据流关系。

## 摘要

- 函数→数据源 关系：**66** 条
- 工具→函数 关系：**5** 条
- ARCHITECTURE 数据流图 关系：**4** 条
- 数据源→实体类型 关系：**13** 条
- spec→数据源 关系：**29** 条
- **总计：117** 条

- 更新数据源实体文件：**0** 个
- 更新 spec 文件：**0** 个

## 按数据源分组

| 数据源 | 函数关系 | 工具关系 | spec 引用 | 实体类型 | 总计 |
|---|---|---|---|---|---|
| `akshare` | 7 | 1 | 8 | 3 | 19 |
| `baidu-stock` | 1 | 0 | 0 | 0 | 1 |
| `baostock` | 2 | 0 | 1 | 0 | 3 |
| `cninfo` | 1 | 0 | 0 | 0 | 1 |
| `eastmoney-datacenter` | 0 | 0 | 5 | 0 | 5 |
| `eastmoney-push2` | 20 | 2 | 7 | 7 | 36 |
| `eastmoney-reportapi` | 0 | 1 | 0 | 0 | 1 |
| `fred` | 0 | 0 | 4 | 0 | 4 |
| `hithink-ths` | 7 | 0 | 1 | 0 | 8 |
| `mootdx` | 4 | 0 | 0 | 3 | 7 |
| `rss-newsradar` | 0 | 0 | 1 | 0 | 1 |
| `sina-financial` | 3 | 0 | 0 | 0 | 3 |
| `tencent` | 3 | 1 | 1 | 4 | 9 |
| `worldmonitor` | 18 | 0 | 1 | 0 | 19 |

## 更新的文件

### data-sources/ 更新

- （无更新，所有关系段已最新）

### specs/ 更新

- （无更新，所有关联段已含数据源链接）

## 关系类型说明

| 关系类型 | 来源 | 置信度 | 说明 |
|---|---|---|---|
| 函数→数据源 | `backend/data/sources/*.py` AST | high | 模块名归一到数据源实体 |
| 工具→函数 | `stock_tools.py` `@register_tool` | high | 装饰器抓工具名，函数体抓被调函数 |
| ARCHITECTURE 数据流 | `ARCHITECTURE.md` 一图概览 | high | 正则匹配外部源行 |
| 数据源→实体类型 | `ARCHITECTURE.md` 推断 | medium | 从数据流图 + 已灌入实体推断 |
| spec→数据源 | vault `specs/*.md` 关联段 | high | 抓 `[[]]` 链接 |

## 冲突处理（优先级）

同一实体被多源抽取时，优先级：spec > 代码 AST > 文档注释 > LLM 推断。
本脚本只处理 spec/代码/ARCHITECTURE 三个 high/medium 源，不涉及 LLM 推断。

> <!-- pipeline: P4 extract_relations.py 生成 -->
