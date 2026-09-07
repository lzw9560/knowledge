---
type: spec
number: S019
title: 宏观特征 Fred API 接入（macro.py 第二批）
status: 已实现
created: 2026-09-06
last_synced: 2026-09-07
confidence: medium
source: scripts/extract_specs.py
---

# S019 宏观 Fred API 接入

## 问题/目标

S018 多源特征工程需要宏观信号。第一批 macro.py 缺关键系列，需接入 FRED 独立通道补齐。

## 核心决策

美债 10Y/DXY 走 Fred 独立通道 + key 隔离 `VR_DATA_DIR` + 补登 S2。7 系列（DGS10/DTWEXBGS/DFF/T10Y2Y/DEXCHUS/DCOILWTICO/PCOPPUSDM）全部 `availability_offset=1`，走 `register_macro` 循环注册，key 读 `resolve_data_dir()/fred_api_key` 永不打印。

## 受影响文件

- `backend/macro.py`（第二批 7 系列接入）
- `backend/data/sources/fred.py`（独立通道）
- `VR_DATA_DIR/fred_api_key`（key 隔离）

## 验收标准

- 7 系列 fetch+parse 非空（live 冒烟 2026-07-31 7/7 通过）
- key 隔离 `VR_DATA_DIR`，永不打印
- short_sector 从 21 增至 28

## 关联

- 上游特征层：[[specs/S018-多源特征工程]]（特征工程消费 macro）
- 下游模型：[[specs/S017-A股涨跌预测模型栈]]（ML 栈消费宏观特征）
- 衔接后续：[[specs/S020-worldmonitor决策因子接入]]（worldmonitor 另类数据互补）
- 数据源：[[data-sources/fred]]
- 决策：[[specs/DEC-002]]（7 系列定稿 + USDCNH 改 DEXCHUS）
- 源文件：`specs/archive/m0-foundation/S019-macro-Fred-API/spec.md`
