---
type: metric
name: 打板_OFI盘口
factor_category: 打板/盘口博弈
edge_status: 学术证实但需 Level2 数据（项目当前无，最大数据瓶颈）
data_source: mootdx tick（未接线，免费源最接近 Level2 但不稳）/付费 Level2 待定
created: 2026-09-09
source: wmm8z0ujn
confidence: low
---

# 打板_OFI/订单簿不平衡

## 定义
OFI（Order Flow Imbalance）/queue imbalance = bid/ask queue 不平衡。学术证实与短期价格变动强相关。

## 有效性证据
- arxiv 1512.03492 Queue Imbalance as One-Tick-Ahead Price Predictor（logistic 回归 bid/ask queue imbalance 显著预测下 tick mid-price 方向）
- arxiv 1204.1381 bid-ask liquidity balance informative for future market order direction
- arxiv 1003.0168 volume imbalance increases before extreme events（深圳高频数据）
- arxiv 1912.07165 predicting intraday jumps using liquidity measures+technical indicators（5 分钟间隔 ML）
- arxiv 2505.22678 deep learning LOB bid-ask differences 更 stable 更 predictive
- **§44 状态**：盘中高频信号学术证实，但需 tick 级盘口数据（Level2），项目当前无；"edge 在盘中"是假设非验证结论

## 数据源
- mootdx tick（通达信 tick 级盘口，未接线，需 pip + 接 Quotes.market，免费源最接近 Level2 但不稳——断连频繁需多服务器轮询+重连）
- 付费 Level2（同花顺/东财逐笔+千档封单，数千元/年）——最大数据瓶颈
- anuj1312/orderbook-tickdata-trading-strategy 盘口 ML 方法论参考（Rise Ratio/Depth Ratio+5 模型，非 A 股需适配涨跌停+T+1）

## 三问
- 买什么：盘口买盘强标的
- 何时买：盘口确认封板概率大时
- 何时卖：盘口转弱/撤单激增

## links
- 战法卡：[[弱转强接力]] [[一字竞价选股法]]
- 数据源：[[data-sources/mootdx]]
- 索引：[[打板因子集索引]]
