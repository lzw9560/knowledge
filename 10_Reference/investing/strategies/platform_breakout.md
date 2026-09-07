---
type: strategy
name: 平台突破
edge_family: 形态突破
imported_from: backend/strategies/cards/
created: 2026-09-06
confidence: high
source: manual
---

# 平台突破（platform_breakout）

## 适用天气
晴天

## 核心逻辑
横盘 ≥ 5 日后突破平台上沿，成交量放大 2 倍（量比）确认。突破后惯性上攻概率高。无 market_scan_ctx（涨停 pipeline 路径无 PatternScan）时不评估。

## 入场条件
- 横盘 ≥ 5 日（consolidation_days）
- 成交量放大 2 倍（量比 > 2，今量 / 前 5 日均量，volume_breakout_ratio）

## 退出参数
- 止损：跌破入场价 -5%
- 止盈：涨至 +12%（入场价基准）触发减仓锁利
- 最大持有：7 日

## 风险点
- 假突破回踩
- 放量可能是诱多
- 横盘期间积累的卖压

## 历史统计特征，市场有风险，研究参考。

## 📚 理论依据

- 📖 [[../../reading/notes/金融市场技术分析-笔记|形态突破（墨菲）]] — 平台突破即墨菲"形态突破"标准形态，量比>2 即"成交量是判断趋势有效性最直接证据"
- 📖 [[../../reading/notes/趋势跟踪-笔记|趋势跟踪]] — 横盘≥5 日突破即唐奇安通道突破的变体（盘整区间突破入场）
- 📖 [[../../reading/notes/道氏理论-笔记|道氏理论]] — 突破后量价确认（量比>2）即道氏"趋势需成交量配合"原则
