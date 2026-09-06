#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 历史数据引导脚本
将 macro_indicators / institution_flow / capital_flow_signals / derivatives_data / limit_up_pool
中的历史数据灌入 signal_log，使评分引擎能计算z-score

运行方式：python3 bootstrap_signal_log.py
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "sentiment.db"

# ============================================================
# 信号名映射：各源表 → signal_log 标准名
# ============================================================

# macro_indicators.indicator_name → signal_log.signal_name
MACRO_MAP = {
    "社融增量": "social_finance",
    "M1-M2剪刀差": "m1_m2_scissors",
    "制造业PMI": "pmi",
    "DR007": "dr007",
    "CPI-PPI剪刀差": "cpi_ppi",
}

# institution_flow.signal_name → signal_log.signal_name (同名直接映射)
INST_MAP = {
    "lhb_inst_vs_retail": "lhb_inst_vs_retail_divergence",
    "margin_balance_change": "margin_balance_change",
    "block_trade_discount": "block_trade_discount",
    "inst_buyback_repurchase": "inst_buyback_repurchase",
}

# capital_flow_signals.signal_name → signal_log.signal_name
CAPITAL_MAP = {
    "northbound_net": "northbound_net",
    "main_capital_net": "main_capital_net",
    "cds_spread": "cds_spread",
    "volume_ratio": "volume_ratio",
}

# L4 涨停池字段 → signal_log
LIMIT_UP_MAP = {
    "limit_up_count": "limit_up_structure",
    "broken_rate": "broken_rate",
}

# L5 衍生品字段 → signal_log
DERIV_MAP = {
    "hs300_pcr_position": "pcr_position",
    "hs300_iv_change": "iv_change",
    "basis_if": "basis",
    "hs300_skew_25d": "skew",
}


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 清空 signal_log 中旧数据
    c.execute("DELETE FROM signal_log")
    print(f"清空 signal_log")

    total = 0

    # ============================================================
    # L0 宏观层
    # ============================================================
    for indi_name, sig_name in MACRO_MAP.items():
        rows = c.execute(
            "SELECT indicator_date, indicator_value FROM macro_indicators WHERE indicator_name=? AND indicator_value IS NOT NULL ORDER BY indicator_date",
            (indi_name,)
        ).fetchall()
        for r in rows:
            c.execute("""
                INSERT INTO signal_log (trade_date, signal_layer, signal_name, signal_value, signal_direction, signal_strength, signal_confidence)
                VALUES (?, 'L0_macro', ?, ?, 'neutral', 0, 0.5)
            """, (r["indicator_date"], sig_name, r["indicator_value"]))
            total += 1
        if rows:
            print(f"  L0 {sig_name}: {len(rows)} 条")

    # ============================================================
    # L2 机构层
    # ============================================================
    for src_name, sig_name in INST_MAP.items():
        rows = c.execute(
            "SELECT trade_date, signal_value FROM institution_flow WHERE signal_name=? AND signal_value IS NOT NULL ORDER BY trade_date",
            (src_name,)
        ).fetchall()
        for r in rows:
            c.execute("""
                INSERT INTO signal_log (trade_date, signal_layer, signal_name, signal_value, signal_direction, signal_strength, signal_confidence)
                VALUES (?, 'L2_institution', ?, ?, 'neutral', 0, 0.5)
            """, (r["trade_date"], sig_name, r["signal_value"]))
            total += 1
        if rows:
            print(f"  L2 {sig_name}: {len(rows)} 条")

    # ============================================================
    # L3 资金面层
    # ============================================================
    for src_name, sig_name in CAPITAL_MAP.items():
        rows = c.execute(
            "SELECT trade_date, signal_value FROM capital_flow_signals WHERE signal_name=? AND signal_value IS NOT NULL ORDER BY trade_date",
            (src_name,)
        ).fetchall()
        for r in rows:
            c.execute("""
                INSERT INTO signal_log (trade_date, signal_layer, signal_name, signal_value, signal_direction, signal_strength, signal_confidence)
                VALUES (?, 'L3_capital', ?, ?, 'neutral', 0, 0.5)
            """, (r["trade_date"], sig_name, r["signal_value"]))
            total += 1
        if rows:
            print(f"  L3 {sig_name}: {len(rows)} 条")

    # ============================================================
    # L4 情绪层
    # ============================================================
    for field, sig_name in LIMIT_UP_MAP.items():
        rows = c.execute(
            f"SELECT trade_date, {field} FROM limit_up_pool WHERE {field} IS NOT NULL ORDER BY trade_date"
        ).fetchall()
        for r in rows:
            c.execute("""
                INSERT INTO signal_log (trade_date, signal_layer, signal_name, signal_value, signal_direction, signal_strength, signal_confidence)
                VALUES (?, 'L4_sentiment', ?, ?, 'neutral', 0, 0.5)
            """, (r["trade_date"], sig_name, r[field]))
            total += 1
        if rows:
            print(f"  L4 {sig_name}: {len(rows)} 条")

    # ============================================================
    # L5 衍生品层
    # ============================================================
    for field, sig_name in DERIV_MAP.items():
        rows = c.execute(
            f"SELECT trade_date, {field} FROM derivatives_data WHERE {field} IS NOT NULL ORDER BY trade_date"
        ).fetchall()
        for r in rows:
            c.execute("""
                INSERT INTO signal_log (trade_date, signal_layer, signal_name, signal_value, signal_direction, signal_strength, signal_confidence)
                VALUES (?, 'L5_derivatives', ?, ?, 'neutral', 0, 0.5)
            """, (r["trade_date"], sig_name, r[field]))
            total += 1
        if rows:
            print(f"  L5 {sig_name}: {len(rows)} 条")

    conn.commit()

    # 统计
    print(f"\n=== 灌入完成 ===")
    print(f"总计: {total} 条")

    # 验证
    print(f"\n=== signal_log 统计 ===")
    rows = c.execute("""
        SELECT signal_layer, signal_name, COUNT(*), MIN(trade_date), MAX(trade_date)
        FROM signal_log GROUP BY signal_layer, signal_name ORDER BY signal_layer, signal_name
    """).fetchall()
    for r in rows:
        print(f"  {r[0]} | {r[1]}: {r[2]}条 | {r[3]} ~ {r[4]}")

    conn.close()
    print(f"\n✅ 引导完成，评分引擎现在可以使用历史数据计算z-score")


if __name__ == "__main__":
    main()
