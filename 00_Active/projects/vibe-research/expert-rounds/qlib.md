---
type: data_source
date: 2026-09-09
description: microsoft/qlib——Alpha158全是量价因子无价值因子，纠偏「qlib wrap价值」误传，只参考ML思路
---

# qlib（microsoft）

> 「社区开源实践者」备料（2026-09-09）。**纠偏**：之前记「qlib wrap 做价值因子」是误传，Alpha158 无价值因子。

## 实情

- Alpha158（`qlib/contrib/data/handler.py`）是**纯量价因子**（kbar+price+rolling 158 个），**无 EP/PB/DP/PCF 价值因子**（博客称"含 PE/PB"系误传）
- examples/ 全是 ML benchmark（LightGBM/LSTM on CSI300/500，IC≈0.03-0.04），**无现成价值/红利策略**
- 对长线价值场景偏重，非首选。只参考 ML 思路，MIT，15k+ star 活跃

## verdict

做 A 股长线价值，**别 fork qlib**（无价值因子）。fork [[00_Active/projects/vibe-research/expert-rounds/zlotus-ash-mcp]] 对路。qlib 适合做量价 ML 选股，但 A 股 [[00_Active/projects/vibe-research/expert-rounds/动量因子_A股]] 长期无效，量价动量类也受限。

## 关联

[[00_Active/projects/vibe-research/expert-rounds/红利低波复合因子]] + [[00_Active/projects/vibe-research/expert-rounds/zlotus-ash-mcp]] + [[00_Active/projects/vibe-research/expert-rounds/动量因子_A股]]。
