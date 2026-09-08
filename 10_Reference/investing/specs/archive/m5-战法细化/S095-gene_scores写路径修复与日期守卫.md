---
type: spec
number: S095
title: gene_scores 写路径修复与日期自证守卫
status: 已实现
created: 2026-09-07
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S095 gene_scores 写路径修复与日期自证守卫

## 摘要

6 tests 全绿 + 全量 2226 passed + 七日 7/7 code 集合全等（medium）

## 问题/目标

该规范旨在解决 gene_scores 计算结果写入时因路径未固定日期标识而导致的输出相互覆盖与历史版本混淆问题。核心设计决策是强制所有写路径采用包含生成日期的标准化目录与文件名模板，并在写入动作前插入“日期自证守卫”，该守卫通过比对当前系统日期与文件名内嵌日期，若不一致则终止写入并抛出明确错误，从而杜绝伪造或误置日期文件的可能性。涉及的关键技术组件包括基因评分计算管线、基于约定结构的路径构建器以及日期自证守卫模块，后者依赖命名模式校验与文件系统原子操作，确保输出具备可审计的时效性。

## 关联

- 源文件：`specs/archive/m5-战法细化/S095-gene_scores写路径修复与日期守卫/spec.md`（Vibe-Research 仓）
- README 索引：`specs/README.md`
- 子文档：spec
- 数据源：[[data-sources/]]
- 战法：[[strategies/]]
