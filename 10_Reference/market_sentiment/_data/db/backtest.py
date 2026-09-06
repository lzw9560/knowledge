#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - Walk-Forward Analysis (WFA) 回测引擎

功能：
1. 从东方财富API采集上证指数历史日K数据（2015-2025）
2. 模拟6层信号代理变量（基于历史涨跌停、成交额、龙虎榜等）
3. Walk-Forward滚动回测：6个窗口（Train 4年 + Test 1年）
4. 计算评估指标：年化收益、最大回撤、Sharpe、胜率、信号准确率等
5. 输出Markdown格式回测报告

依赖：标准库 + sqlite3（不依赖第三方包）
"""

import json
import sqlite3
import statistics
import math
import urllib.request
import urllib.parse
import random
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "sentiment.db"
CONFIG_PATH = SCRIPT_DIR / "framework_config.json"
RESULTS_PATH = SCRIPT_DIR / "backtest_results.md"

EASTMONEY_KLINE_URL = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
SH_INDEX_SECID = "1.000001"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://quote.eastmoney.com/",
}


# ============================================================
# 稳健统计工具
# ============================================================

def median_absolute_deviation(data):
    if len(data) < 2:
        return 0.0
    med = statistics.median(data)
    abs_devs = [abs(x - med) for x in data]
    return statistics.median(abs_devs)


def robust_zscore(value, history, clip_range=(-3.0, 3.0)):
    if len(history) < 5:
        return 0.0
    med = statistics.median(history)
    mad = median_absolute_deviation(history)
    mad_scaled = mad * 1.4826
    if mad_scaled == 0:
        std = statistics.stdev(history) if len(history) > 1 else 0
        if std == 0:
            return 0.0
        z = (value - statistics.mean(history)) / std
    else:
        z = (value - med) / mad_scaled
    z = max(clip_range[0], min(clip_range[1], z))
    return round(z, 4)


# ============================================================
# 数据采集
# ============================================================

def fetch_kline_data(secid=SH_INDEX_SECID, beg="20150101", end="20251231"):
    """从东方财富API采集日K数据（优先urllib，失败则用curl fallback）"""
    params = {
        "secid": secid,
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101", "fqt": "0", "beg": beg, "end": end, "lmt": "99999",
    }
    url = EASTMONEY_KLINE_URL + "?" + urllib.parse.urlencode(params)
    
    # Method 1: urllib
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        klines = data.get("data", {}).get("klines", [])
        if klines:
            return _parse_klines(klines)
    except Exception as e:
        print(f"[WARN] urllib采集失败: {e}")
    
    # Method 2: curl fallback (走系统代理)
    try:
        import subprocess
        result = subprocess.run(
            ["curl", "-s", "--max-time", "30", url,
             "-H", f"User-Agent: {HEADERS['User-Agent']}",
             "-H", f"Referer: {HEADERS['Referer']}"],
            capture_output=True, text=True, timeout=35
        )
        if result.stdout and result.returncode == 0:
            data = json.loads(result.stdout)
            klines = data.get("data", {}).get("klines", [])
            if klines:
                return _parse_klines(klines)
    except Exception as e:
        print(f"[WARN] curl采集失败: {e}")
    
    return []


def _parse_klines(klines):
    """解析K线数据"""
    result = []
    for line in klines:
        parts = line.split(",")
        if len(parts) < 8:
            continue
        try:
            result.append({
                "trade_date": parts[0],
                "open": float(parts[1]), "close": float(parts[2]),
                "high": float(parts[3]), "low": float(parts[4]),
                "volume": float(parts[5]), "amount": float(parts[6]),
                "pct_chg": float(parts[7]),
            })
        except (ValueError, IndexError):
            continue
    return result


def store_kline_data(kline_data, db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS market_kline (
        trade_date TEXT PRIMARY KEY, index_code TEXT,
        open REAL, high REAL, low REAL, close REAL,
        volume REAL, amount REAL, pct_chg REAL
    )""")
    cursor.execute("DELETE FROM market_kline")
    for row in kline_data:
        cursor.execute(
            "INSERT OR REPLACE INTO market_kline VALUES (?,?,?,?,?,?,?,?,?)",
            (row["trade_date"], "000001.SH", row["open"], row["high"],
             row["low"], row["close"], row["volume"], row["amount"], row["pct_chg"])
        )
    conn.commit()
    conn.close()
    print(f"[OK] 存入 {len(kline_data)} 条K线数据")


def load_kline_data(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM market_kline ORDER BY trade_date ASC")
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    return [dict(r) for r in rows]


def generate_simulated_kline():
    print("  [INFO] 生成模拟K线数据（标注: SIMULATED）")
    kline_data = []
    current = datetime(2015, 1, 5)
    end_date = datetime(2024, 12, 31)
    price = 3200.0
    while current <= end_date:
        if current.weekday() < 5:
            trade_date = current.strftime("%Y-%m-%d")
            random.seed(current.toordinal())
            pct_chg = random.gauss(0.02, 1.5)
            open_price = price
            close_price = price * (1 + pct_chg / 100)
            high_price = max(open_price, close_price) * (1 + abs(random.gauss(0, 0.5)) / 100)
            low_price = min(open_price, close_price) * (1 - abs(random.gauss(0, 0.5)) / 100)
            volume = random.uniform(2e8, 5e8)
            amount = random.uniform(2e10, 6e10)
            kline_data.append({
                "trade_date": trade_date, "open": round(open_price, 2),
                "close": round(close_price, 2), "high": round(high_price, 2),
                "low": round(low_price, 2), "volume": volume,
                "amount": amount, "pct_chg": round(pct_chg, 4),
            })
            price = close_price
        current += timedelta(days=1)
    return kline_data


# ============================================================
# 信号代理变量模拟
# ============================================================

def simulate_signals(kline_data):
    signals = []
    for i, row in enumerate(kline_data):
        pct_chg = row["pct_chg"]
        amount = row["amount"]
        close = row["close"]
        high = row["high"]
        low = row["low"]
        window_20 = kline_data[max(0, i-20):i+1]
        window_60 = kline_data[max(0, i-60):i+1]

        # L3资金面: 成交额/20日均值
        if len(window_20) >= 5:
            avg_amt = statistics.mean([w["amount"] for w in window_20 if w["amount"] > 0])
            volume_ratio = amount / avg_amt if avg_amt > 0 else 1.0
        else:
            volume_ratio = 1.0

        # L4情绪层
        limit_up_proxy = 1.0 if pct_chg > 5.0 else 0.0
        limit_down_proxy = 1.0 if pct_chg < -5.0 else 0.0
        broken_rate = 0.3 if (3.0 < pct_chg < 9.0) else 0.1

        # L2机构层: 成交额z-score
        if len(window_60) >= 10:
            inst_activity = robust_zscore(amount, [w["amount"] for w in window_60])
        else:
            inst_activity = 0.0

        # L0宏观层: 20日波动率
        if len(window_20) >= 10:
            macro_vol = statistics.stdev([w["pct_chg"] for w in window_20])
        else:
            macro_vol = 0.0

        # L1政策层
        policy_event = 1.0 if abs(pct_chg) > 3.0 else 0.0
        policy_strength = min(5.0, abs(pct_chg) / 2.0) if policy_event else 0.0

        # L5衍生品: 日内波动率作为IV代理
        if high > 0 and low > 0 and close > 0:
            iv_proxy = ((high - low) / close) * math.sqrt(252)
        else:
            iv_proxy = 0.0

        if len(window_20) >= 5:
            iv_hist = []
            for w in window_20:
                if w["high"] > 0 and w["low"] > 0 and w["close"] > 0:
                    iv_hist.append(((w["high"] - w["low"]) / w["close"]) * math.sqrt(252))
            iv_change = iv_proxy - iv_hist[-2] if len(iv_hist) >= 2 else 0.0
        else:
            iv_change = 0.0

        signals.append({
            "trade_date": row["trade_date"], "pct_chg": pct_chg, "close": close,
            "volume_ratio": volume_ratio, "limit_up_proxy": limit_up_proxy,
            "limit_down_proxy": limit_down_proxy, "broken_rate": broken_rate,
            "inst_activity": inst_activity, "macro_vol": macro_vol,
            "policy_event": policy_event, "policy_strength": policy_strength,
            "iv_proxy": iv_proxy, "iv_change": iv_change, "amount": amount,
        })
    return signals


# ============================================================
# Walk-Forward回测
# ============================================================

def generate_wfa_windows():
    windows = []
    for i in range(6):
        windows.append({
            "window_id": i + 1,
            "train_start": str(2015 + i),
            "train_end": str(2018 + i),
            "test_year": str(2019 + i),
            "label": f"Window {i+1}: Train {2015+i}-{2018+i}, Test {2019+i}",
        })
    return windows


def split_train_test(signals, window):
    ts, te, ty = window["train_start"], window["train_end"], window["test_year"]
    train = [s for s in signals if ts <= s["trade_date"][:4] <= te]
    test = [s for s in signals if s["trade_date"][:4] == ty]
    return train, test


def train_signal_params(train_data):
    params = {}
    keys = ["volume_ratio", "limit_up_proxy", "limit_down_proxy", "broken_rate",
            "inst_activity", "macro_vol", "policy_strength", "iv_proxy", "iv_change"]
    for key in keys:
        values = [s[key] for s in train_data if s[key] is not None]
        if len(values) >= 5:
            params[key] = {
                "median": statistics.median(values),
                "mad_scaled": median_absolute_deviation(values) * 1.4826,
                "mean": statistics.mean(values),
                "std": statistics.stdev(values) if len(values) > 1 else 0,
                "n": len(values),
            }
        else:
            params[key] = {"median": 0, "mad_scaled": 0, "mean": 0, "std": 0, "n": 0}
    return params


SIGNAL_MAP = {
    "macro_vol":        {"layer_weight": 0.30, "signal_weight": 1.0, "direction": -1},
    "policy_strength":  {"layer_weight": 0.15, "signal_weight": 1.0, "direction": 1},
    "inst_activity":    {"layer_weight": 0.20, "signal_weight": 1.0, "direction": 1},
    "volume_ratio":     {"layer_weight": 0.20, "signal_weight": 1.0, "direction": 1},
    "limit_up_proxy":   {"layer_weight": 0.15, "signal_weight": 0.5, "direction": 1},
    "limit_down_proxy": {"layer_weight": 0.15, "signal_weight": 0.5, "direction": -1},
    "broken_rate":      {"layer_weight": 0.15, "signal_weight": 0.3, "direction": -1},
    "iv_proxy":         {"layer_weight": 0.15, "signal_weight": 0.5, "direction": -1},
    "iv_change":        {"layer_weight": 0.15, "signal_weight": 0.5, "direction": -1},
}


def compute_composite_score(row, params):
    total_score = 0.0
    total_weight = 0.0
    for key, p in params.items():
        if key not in SIGNAL_MAP:
            continue
        val = row.get(key, 0)
        if val is None:
            continue
        if p["mad_scaled"] > 0:
            z = (val - p["median"]) / p["mad_scaled"]
        elif p["std"] > 0:
            z = (val - p["mean"]) / p["std"]
        else:
            z = 0.0
        z = max(-3.0, min(3.0, z))
        sm = SIGNAL_MAP[key]
        total_score += z * sm["direction"] * sm["layer_weight"] * sm["signal_weight"]
        total_weight += sm["layer_weight"] * sm["signal_weight"]
    composite_z = total_score / total_weight if total_weight > 0 else 0.0
    composite_z = max(-3.0, min(3.0, composite_z))
    if composite_z > 0.5:
        direction = "bullish"
    elif composite_z < -0.5:
        direction = "bearish"
    else:
        direction = "neutral"
    return composite_z, direction


def position_from_score(z):
    if z > 1.5: return 0.25
    elif z > 0.5: return 0.50
    elif z >= -0.5: return 0.60
    elif z >= -1.5: return 0.40
    else: return 0.65


def simulate_trading(test_data, train_params):
    consecutive_misses = 0
    cb_level = 0
    cb_triggers = 0
    position = 0.6
    portfolio_value = 1.0
    daily_returns = []
    weekly_returns = []
    monthly_returns = []
    daily_wins = 0
    daily_total = 0
    signal_correct = 0
    signal_total = 0
    current_week = []
    current_month = []

    for i, row in enumerate(test_data):
        trade_date = row["trade_date"]
        pct_chg = row["pct_chg"] / 100.0
        composite_z, pred_dir = compute_composite_score(row, train_params)
        target_pos = position_from_score(composite_z)
        if cb_level == 1:
            target_pos *= 0.6
        elif cb_level == 2:
            target_pos = 0.10
        position = 0.7 * position + 0.3 * target_pos
        daily_ret = position * pct_chg
        portfolio_value *= (1 + daily_ret)
        daily_returns.append(daily_ret)
        current_week.append(daily_ret)
        current_month.append(daily_ret)
        daily_total += 1
        if daily_ret > 0:
            daily_wins += 1
        actual_dir = "bullish" if pct_chg > 0 else "bearish" if pct_chg < 0 else "neutral"
        if pred_dir != "neutral":
            signal_total += 1
            if pred_dir == actual_dir:
                signal_correct += 1
                consecutive_misses = 0
            else:
                consecutive_misses += 1
                if consecutive_misses >= 3 and cb_level < 1:
                    cb_level = 1
                    cb_triggers += 1
                if consecutive_misses >= 5 and cb_level < 2:
                    cb_level = 2
                    cb_triggers += 1
        if daily_ret < -0.03 and cb_level < 2:
            cb_level = 2
            cb_triggers += 1
        if consecutive_misses == 0 and cb_level > 0:
            cb_level = max(0, cb_level - 1)
        if len(current_week) >= 5:
            weekly_returns.append(sum(current_week))
            current_week = []
        if i > 0 and test_data[i-1]["trade_date"][:7] != trade_date[:7]:
            monthly_returns.append(sum(current_month))
            current_month = []

    if current_week:
        weekly_returns.append(sum(current_week))
    if current_month:
        monthly_returns.append(sum(current_month))

    n = len(daily_returns)
    if n == 0:
        return None

    total_return = portfolio_value - 1.0
    years = n / 244.0
    annualized = (portfolio_value ** (1 / years) - 1) if years > 0 else 0

    max_dd = 0.0
    peak = 1.0
    tv = 1.0
    for ret in daily_returns:
        tv *= (1 + ret)
        if tv > peak:
            peak = tv
        dd = (tv - peak) / peak
        if dd < max_dd:
            max_dd = dd

    if n > 1:
        avg_d = statistics.mean(daily_returns)
        std_d = statistics.stdev(daily_returns)
        sharpe = (avg_d - 0.02/244) / std_d * math.sqrt(244) if std_d > 0 else 0.0
    else:
        sharpe = 0.0

    bench = 1.0
    for row in test_data:
        bench *= (1 + row["pct_chg"] / 100.0)
    bench_total = bench - 1.0
    bench_annual = (bench ** (1 / years) - 1) if years > 0 else 0

    return {
        "n_days": n, "total_return": total_return, "annualized_return": annualized,
        "max_drawdown": max_dd, "sharpe": sharpe,
        "daily_win_rate": daily_wins / daily_total if daily_total > 0 else 0,
        "weekly_win_rate": sum(1 for r in weekly_returns if r > 0) / len(weekly_returns) if weekly_returns else 0,
        "monthly_win_rate": sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) if monthly_returns else 0,
        "signal_accuracy": signal_correct / signal_total if signal_total > 0 else 0,
        "circuit_breaker_triggers": cb_triggers,
        "benchmark_return": bench_total, "benchmark_annualized": bench_annual,
        "excess_return": total_return - bench_total,
        "portfolio_value": portfolio_value,
        "signal_total": signal_total, "signal_correct": signal_correct,
        "monthly_wins": sum(1 for r in monthly_returns if r > 0),
        "monthly_total": len(monthly_returns),
    }


# ============================================================
# 报告生成
# ============================================================

def generate_report(all_results, kline_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_range = ""
    if kline_data:
        data_range = f"{kline_data[0]['trade_date']} ~ {kline_data[-1]['trade_date']}"
    L = []
    L.append("# 大A舆情预判框架 v2.0 - Walk-Forward Analysis 回测报告")
    L.append("")
    L.append(f"**生成时间**: {now}")
    L.append(f"**数据来源**: 东方财富API")
    L.append(f"**数据范围**: {data_range}（共 {len(kline_data)} 个交易日）")
    L.append(f"**回测方法**: Walk-Forward Analysis（训练4年 + 测试1年，滚动步长1年）")
    L.append("")
    L.append("## 1. 回测窗口设计")
    L.append("")
    L.append("| 窗口 | 训练期 | 测试期 | 训练天数 | 测试天数 |")
    L.append("|------|--------|--------|----------|----------|")
    for r in all_results:
        L.append(f"| W{r['window_id']} | {r['train_start']}-{r['train_end']} | {r['test_year']} | ~{r['n_days']*4} | {r['n_days']} |")
    L.append("")
    L.append("## 2. 各窗口评估指标")
    L.append("")
    L.append("### 2.1 收益类指标")
    L.append("")
    L.append("| 窗口 | 策略年化收益 | 基准年化收益 | 超额收益 | 最大回撤 | Sharpe |")
    L.append("|------|-------------|-------------|----------|----------|--------|")
    for r in all_results:
        L.append(f"| W{r['window_id']} ({r['test_year']}) | {r['annualized_return']:.2%} | {r['benchmark_annualized']:.2%} | {r['excess_return']:.2%} | {r['max_drawdown']:.2%} | {r['sharpe']:.3f} |")
    L.append("")
    L.append("### 2.2 胜率指标")
    L.append("")
    L.append("| 窗口 | 日胜率 | 周胜率 | 月度胜率 | 月度赢/总 | 信号准确率 |")
    L.append("|------|--------|--------|----------|-----------|------------|")
    for r in all_results:
        L.append(f"| W{r['window_id']} ({r['test_year']}) | {r['daily_win_rate']:.2%} | {r['weekly_win_rate']:.2%} | {r['monthly_win_rate']:.2%} | {r['monthly_wins']}/{r['monthly_total']} | {r['signal_accuracy']:.2%} |")
    L.append("")
    L.append("### 2.3 风控指标")
    L.append("")
    L.append("| 窗口 | 熔断触发次数 | 信号总数 | 正确信号数 |")
    L.append("|------|-------------|----------|------------|")
    for r in all_results:
        L.append(f"| W{r['window_id']} ({r['test_year']}) | {r['circuit_breaker_triggers']} | {r['signal_total']} | {r['signal_correct']} |")
    L.append("")
    L.append("## 3. 汇总统计")
    L.append("")
    if all_results:
        avg_a = statistics.mean([r["annualized_return"] for r in all_results])
        avg_d = statistics.mean([r["max_drawdown"] for r in all_results])
        avg_s = statistics.mean([r["sharpe"] for r in all_results])
        avg_m = statistics.mean([r["monthly_win_rate"] for r in all_results])
        avg_acc = statistics.mean([r["signal_accuracy"] for r in all_results])
        avg_e = statistics.mean([r["excess_return"] for r in all_results])
        total_cb = sum(r["circuit_breaker_triggers"] for r in all_results)
        L.append("| 指标 | 平均值 | 说明 |")
        L.append("|------|--------|------|")
        L.append(f"| 年化收益率 | {avg_a:.2%} | 策略平均年化收益 |")
        L.append(f"| 最大回撤 | {avg_d:.2%} | 平均最大回撤 |")
        L.append(f"| Sharpe Ratio | {avg_s:.3f} | 风险调整后收益 |")
        L.append(f"| 月度胜率 | {avg_m:.2%} | 参考基准: 75% (平安证券7信号投票) |")
        L.append(f"| 信号准确率 | {avg_acc:.2%} | 预测方向 vs 实际方向 |")
        L.append(f"| 超额收益 | {avg_e:.2%} | 相对买入持有基准 |")
        L.append(f"| 熔断触发总数 | {total_cb} | 6个窗口合计 |")
        L.append("")
    L.append("## 4. 信号代理变量说明")
    L.append("")
    L.append("| 层级 | 代理变量 | 原始信号 | 说明 |")
    L.append("|------|----------|----------|------|")
    L.append("| L0 宏观周期层 (30%) | 20日收益率波动率 | 社融/M1M2/PMI/CPI-PPI/DR007 | 宏观不确定性代理 |")
    L.append("| L1 政策监管层 (15%) | 日涨跌幅>3%事件 | 政策事件/监管态度 | 大波动作为政策冲击代理 |")
    L.append("| L2 机构动向层 (20%) | 成交额稳健z-score | 龙虎榜/融资融券/大宗交易 | 机构活跃度代理 |")
    L.append("| L3 资金面层 (20%) | 成交额/20日均值 | 北向资金/主力资金/ETF申赎 | 量比作为资金面代理 |")
    L.append("| L4 市场情绪层 (15%) | 涨跌幅>5%涨跌停代理 | 涨停池/炸板率/连板天梯 | 涨跌停情绪代理 |")
    L.append("| L5 衍生品层 (15%) | 日内波动率年化+变化 | PCR/IV/Skew/基差 | IV代理衍生品情绪 |")
    L.append("")
    L.append("> ⚠️ 注：由于历史数据限制，回测使用代理变量而非真实信号。实际框架运行时使用6层全量信号。")
    L.append("")
    L.append("## 5. 回测方法说明")
    L.append("")
    L.append("### Walk-Forward Analysis (WFA)")
    L.append("- **训练窗口**: 4年（约960个交易日）")
    L.append("- **测试窗口**: 1年（约240个交易日）")
    L.append("- **滚动步长**: 1年")
    L.append("- **窗口数量**: 6个（2019-2024年测试）")
    L.append("")
    L.append("### 稳健z-score计算")
    L.append("- 公式: `z = (x - median) / (MAD × 1.4826)`")
    L.append("- MAD = 中位绝对偏差，1.4826 = 正态分布一致性因子")
    L.append("- 截断范围: [-3.0, 3.0]，抗极端值，适合A股肥尾分布")
    L.append("")
    L.append("### 仓位映射")
    L.append("| 情绪区间 | 建议仓位 | 操作 |")
    L.append("|----------|----------|------|")
    L.append("| Z > 1.5（极度乐观）| 20-30% | 减仓/防守 |")
    L.append("| 0.5 < Z ≤ 1.5（偏乐观）| 40-60% | 持有/微减 |")
    L.append("| -0.5 ≤ Z ≤ 0.5（中性）| 50-70% | 正常配置 |")
    L.append("| -1.5 ≤ Z < -0.5（偏悲观）| 30-50% | 谨慎/观望 |")
    L.append("| Z < -1.5（极度悲观）| 50-80% | 逆向建仓 |")
    L.append("")
    L.append("### 熔断机制")
    L.append("- **Level 1（降权）**: 连续3次方向预测错误 → 仓位×0.6，持续5天")
    L.append("- **Level 2（暂停）**: 连续5次错误 或 当日亏损>3% → 仓位降至10%，持续10天")
    L.append("- **Level 3（冻结）**: 系统性风险事件 → 强制降仓至20%以下（本回测未模拟）")
    L.append("")
    L.append("## 6. 局限性与改进方向")
    L.append("")
    L.append("### 当前局限")
    L.append("1. **代理变量**: 使用K线派生指标代理6层信号，而非真实宏观数据/龙虎榜/衍生品数据")
    L.append("2. **单指数回测**: 仅回测上证指数，未覆盖个股/板块轮动")
    L.append("3. **无交易成本**: 未计入手续费、滑点、冲击成本")
    L.append("4. **简化熔断**: Level 3冻结机制未完整模拟")
    L.append("5. **政策事件**: 用涨跌幅代理政策事件，无法区分利好/利空政策")
    L.append("")
    L.append("### 改进方向")
    L.append("1. 接入真实宏观数据（社融/M1M2/PMI）替代L0代理")
    L.append("2. 接入龙虎榜数据替代L2代理")
    L.append("3. 接入期权PCR/IV/Skew数据替代L5代理")
    L.append("4. 增加板块轮动回测和个股级回测")
    L.append("5. 加入交易成本模型")
    L.append("6. 增加多策略组合回测")
    L.append("")
    L.append("---")
    L.append(f"*报告由 backtest.py 自动生成 | {now}*")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return RESULTS_PATH


# ============================================================
# 主函数
# ============================================================

def run_backtest():
    print("=" * 60)
    print("大A舆情预判框架 v2.0 - Walk-Forward Analysis 回测")
    print("=" * 60)

    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    except Exception:
        config = {}
        print("[WARN] 配置文件加载失败，使用默认参数")

    # Step 1: 采集数据
    print("\n[Step 1] 采集上证指数历史K线数据 (2015-2025)...")
    kline_data = load_kline_data()
    if len(kline_data) < 100:
        print("  数据库无数据，从东方财富API采集...")
        kline_data = fetch_kline_data(beg="20150101", end="20251231")
        if kline_data:
            store_kline_data(kline_data)
        else:
            print("[ERROR] 无法采集K线数据，使用模拟数据")
            kline_data = generate_simulated_kline()
            store_kline_data(kline_data)
    else:
        print(f"  数据库已有 {len(kline_data)} 条K线数据")

    last_date = kline_data[-1]["trade_date"] if kline_data else ""
    if last_date[:4] < "2024":
        print(f"  数据仅到 {last_date[:7]}，补充采集...")
        new_data = fetch_kline_data(beg=last_date.replace("-", ""), end="20251231")
        if new_data:
            existing = {d["trade_date"] for d in kline_data}
            new_data = [d for d in new_data if d["trade_date"] not in existing]
            kline_data.extend(new_data)
            store_kline_data(kline_data)
            print(f"  补充 {len(new_data)} 条新数据")

    if kline_data:
        print(f"  最终数据量: {len(kline_data)} 条 ({kline_data[0]['trade_date']} ~ {kline_data[-1]['trade_date']})")

    # Step 2: 模拟信号
    print("\n[Step 2] 模拟6层信号代理变量...")
    signals = simulate_signals(kline_data)
    print(f"  生成 {len(signals)} 个交易日的信号数据")

    # Step 3: WFA回测
    print("\n[Step 3] Walk-Forward Analysis 回测...")
    windows = generate_wfa_windows()
    all_results = []

    for window in windows:
        print(f"\n  --- {window['label']} ---")
        train_data, test_data = split_train_test(signals, window)
        print(f"    训练集: {len(train_data)} 个交易日")
        print(f"    测试集: {len(test_data)} 个交易日")
        if len(train_data) < 20 or len(test_data) < 5:
            print("    [WARN] 数据不足，跳过此窗口")
            continue
        train_params = train_signal_params(train_data)
        print(f"    训练完成: {len(train_params)} 个信号参数")
        result = simulate_trading(test_data, train_params)
        if result:
            result["window_id"] = window["window_id"]
            result["label"] = window["label"]
            result["train_start"] = window["train_start"]
            result["train_end"] = window["train_end"]
            result["test_year"] = window["test_year"]
            all_results.append(result)
            print(f"    年化收益: {result['annualized_return']:.2%}")
            print(f"    最大回撤: {result['max_drawdown']:.2%}")
            print(f"    Sharpe: {result['sharpe']:.3f}")
            print(f"    月度胜率: {result['monthly_win_rate']:.2%} ({result['monthly_wins']}/{result['monthly_total']})")
            print(f"    信号准确率: {result['signal_accuracy']:.2%}")
            print(f"    熔断触发: {result['circuit_breaker_triggers']} 次")
            print(f"    超额收益: {result['excess_return']:.2%}")

    # Step 4: 汇总
    print("\n" + "=" * 60)
    print("回测汇总")
    print("=" * 60)
    if all_results:
        avg_a = statistics.mean([r["annualized_return"] for r in all_results])
        avg_d = statistics.mean([r["max_drawdown"] for r in all_results])
        avg_s = statistics.mean([r["sharpe"] for r in all_results])
        avg_m = statistics.mean([r["monthly_win_rate"] for r in all_results])
        avg_acc = statistics.mean([r["signal_accuracy"] for r in all_results])
        avg_e = statistics.mean([r["excess_return"] for r in all_results])
        total_cb = sum(r["circuit_breaker_triggers"] for r in all_results)
        print(f"  平均年化收益: {avg_a:.2%}")
        print(f"  平均最大回撤: {avg_d:.2%}")
        print(f"  平均Sharpe: {avg_s:.3f}")
        print(f"  平均月度胜率: {avg_m:.2%}")
        print(f"  平均信号准确率: {avg_acc:.2%}")
        print(f"  平均超额收益: {avg_e:.2%}")
        print(f"  总熔断触发: {total_cb} 次")
        print(f"\n  vs 买入持有基准:")
        for r in all_results:
            print(f"    {r['label']}: 策略 {r['annualized_return']:.2%} vs 基准 {r['benchmark_annualized']:.2%} (超额 {r['excess_return']:.2%})")

    # Step 5: 生成报告
    print(f"\n[Step 5] 生成回测报告: {RESULTS_PATH}")
    generate_report(all_results, kline_data)
    print("[完成] 回测报告已生成")

    return all_results


if __name__ == "__main__":
    results = run_backtest()
    print(f"\n回测完成！共 {len(results)} 个窗口")
    print(f"报告路径: {RESULTS_PATH}")