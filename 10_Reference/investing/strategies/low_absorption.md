---
type: strategy
name: 低吸龙头
edge_family: 均值回归
imported_from: backend/strategies/cards/
created: 2026-09-06
confidence: high
source: manual
---

# 低吸龙头（low_absorption）

## 适用天气
晴天 / 阴天

## 核心逻辑
个股回调至 5 日均线附近且均线多头排列时低吸，博反弹。无 market_scan_ctx（涨停 pipeline 路径无 PatternScan）时不评估（数据降级，非逻辑过滤）。

## 入场条件
- 回调至 5 日均线附近（ma5_proximity ≤ 3%）
- 均线多头排列（ma_bullish = True）

## 退出参数
- 止损：跌破入场价 -5%
- 止盈：涨至 +10%（入场价基准）触发减仓锁利
- 最大持有：5 日

## 风险点
- 龙头补跌风险
- 市场转弱时低吸变追套
- 均线多头失效则反弹失败

## 历史统计特征，市场有风险，研究参考。

## 📚 理论依据

- 📖 [[reading/notes/聪明的投资者-笔记|安全边际（格雷厄姆）]] — 回调至 5 日均线低吸即安全边际在短线场景的实例化：内在价值≈均线多头趋势价值，价格折扣≈回调 3% 容差，容错空间≈ -5% 止损
- 📖 [[reading/notes/均值回归-笔记|均值回归（马克斯）]] — 回调至均线即"短期均值回归"的短线实例，均线多头排列是回归的基准均线
- 📖 [[reading/notes/安全边际|安全边际]] — 安全边际方法论概念笔记
