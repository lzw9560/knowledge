#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 宏观数据采集脚本（补充）
采集 社融增量、M1-M2剪刀差、DR007 等宏观指标

数据源（akshare）：
- macro_china_shrzgm() → 社融增量（月频）
- macro_china_money_supply() → M1/M2同比（月频）
- repo_rate_query(symbol='DR007') → FDR007日频（DR007定盘价，日频）
- rate_interbank(market='上海银行同业拆借市场', symbol='Shibor人民币', indicator='1周') → Shibor 1W（补充，日频）

入库表：macro_indicators
字段：indicator_date, available_at, indicator_name, indicator_value, indicator_unit
"""

import sqlite3
import akshare as ak
from datetime import datetime, timedelta, date
from pathlib import Path
import re

DB_PATH = Path(__file__).parent / "sentiment.db"


# ============================================================
# 数据源配置
# ============================================================
SOURCES = {
    "社融增量": {
        "func": "macro_china_shrzgm",
        "date_col": "月份",
        "value_col": "社会融资规模增量",
        "unit": "亿元",
        "lag_days": 15,       # 社融通常月中公布上月数据
        "freq": "monthly",
        "min_records": 24,
    },
    "M1同比": {
        "func": "macro_china_money_supply",
        "date_col": "月份",
        "value_col": "货币(M1)-同比增长",
        "unit": "%",
        "lag_days": 15,
        "freq": "monthly",
        "min_records": 24,
    },
    "M2同比": {
        "func": "macro_china_money_supply",
        "date_col": "月份",
        "value_col": "货币和准货币(M2)-同比增长",
        "unit": "%",
        "lag_days": 15,
        "freq": "monthly",
        "min_records": 24,
    },
    "DR007": {
        "func": "repo_rate_query",
        "func_kwargs": {"symbol": "DR007"},
        "date_col": "date",
        "value_col": "FDR007",
        "unit": "%",
        "lag_days": 0,          # 日频数据，当日可用
        "freq": "daily",
        "min_records": 60,
    },
}


def normalize_month(date_str: str) -> str:
    """将 '202604' 或 '2026年04月份' 转为 '2026-04-01' 格式"""
    date_str = str(date_str).strip()
    # 纯数字 YYYYMM
    if re.match(r'^\d{6}$', date_str):
        y, m = date_str[:4], date_str[4:]
        return f"{y}-{m}-01"
    # 中文格式 '2026年04月份'
    m = re.match(r'(\d{4})年(\d{2})月份?', date_str)
    if m:
        return f"{m.group(1)}-{m.group(2)}-01"
    # 已是日期格式
    return date_str.split(" ")[0]


def compute_available_at(date_str: str, lag_days: int) -> str:
    """计算数据可用时间（防前视偏差）"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt + timedelta(days=lag_days)).isoformat()


def store_indicator(db, indicator_name, date_str, value, unit, lag_days):
    """存入 macro_indicators 表"""
    available_at = compute_available_at(date_str, lag_days)
    db.execute("""
        INSERT OR IGNORE INTO macro_indicators
        (indicator_date, available_at, indicator_name, indicator_value, indicator_unit)
        VALUES (?, ?, ?, ?, ?)
    """, (date_str, available_at, indicator_name, round(float(value), 4), unit))


def collect_social_finance(db):
    """采集社融增量"""
    print("📌 采集 社融增量...")
    df = ak.macro_china_shrzgm()
    stored = 0
    for _, row in df.iterrows():
        date_str = normalize_month(str(row["月份"]))
        value = row.get("社会融资规模增量")
        if date_str and value is not None:
            try:
                store_indicator(db, "社融增量", date_str, float(value), "亿元", 15)
                stored += 1
            except (ValueError, TypeError):
                pass
    db.commit()
    print(f"  ✅ 存储 {stored} 条")
    if stored > 0:
        latest = df.iloc[-1] if len(df) > 0 else None
        if latest is not None:
            print(f"  最新: {normalize_month(str(latest['月份']))} → 社融增量={latest['社会融资规模增量']}亿元")
    return stored


def collect_money_supply(db):
    """采集M1/M2同比并计算剪刀差"""
    print("📌 采集 M1/M2同比...")
    df = ak.macro_china_money_supply()
    stored_m1 = 0
    stored_m2 = 0

    m1_data = []  # (date, value)
    m2_data = []  # (date, value)

    for _, row in df.iterrows():
        date_str = normalize_month(str(row["月份"]))
        m1_val = row.get("货币(M1)-同比增长")
        m2_val = row.get("货币和准货币(M2)-同比增长")

        if m1_val is not None:
            try:
                store_indicator(db, "M1同比", date_str, float(m1_val), "%", 15)
                stored_m1 += 1
                m1_data.append((date_str, float(m1_val)))
            except (ValueError, TypeError):
                pass

        if m2_val is not None:
            try:
                store_indicator(db, "M2同比", date_str, float(m2_val), "%", 15)
                stored_m2 += 1
                m2_data.append((date_str, float(m2_val)))
            except (ValueError, TypeError):
                pass

    db.commit()
    print(f"  ✅ M1同比: {stored_m1} 条, M2同比: {stored_m2} 条")

    # 计算M1-M2剪刀差
    m2_map = {d: v for d, v in m2_data}
    derived = 0
    for m1_date, m1_val in m1_data:
        if m1_date in m2_map:
            scissors = m1_val - m2_map[m1_date]
            store_indicator(db, "M1-M2剪刀差", m1_date, scissors, "%", 15)
            derived += 1
    db.commit()
    print(f"  ✅ M1-M2剪刀差: {derived} 条（派生）")

    if m1_data:
        latest_m1 = sorted(m1_data, key=lambda x: x[0], reverse=True)[0]
        print(f"  最新M1: {latest_m1[0]} → {latest_m1[1]}%")
    if m2_data:
        latest_m2 = sorted(m2_data, key=lambda x: x[0], reverse=True)[0]
        print(f"  最新M2: {latest_m2[0]} → {latest_m2[1]}%")
    if m1_data and m2_data:
        latest = sorted(m1_data, key=lambda x: x[0], reverse=True)[0]
        if latest[0] in m2_map:
            print(f"  最新剪刀差: {latest[0]} → {latest[1] - m2_map[latest[0]]}%")

    return stored_m1 + stored_m2 + derived


def collect_dr007(db):
    """采集DR007（FDR007定盘利率）"""
    print("📌 采集 DR007 (FDR007)...")
    df = ak.repo_rate_query(symbol="DR007")
    stored = 0
    for _, row in df.iterrows():
        date_str = str(row["date"])
        value = row.get("FDR007")
        if date_str and value is not None:
            try:
                store_indicator(db, "DR007", date_str, float(value), "%", 0)
                stored += 1
            except (ValueError, TypeError):
                pass
    db.commit()
    print(f"  ✅ 存储 {stored} 条")
    if stored > 0:
        latest_row = df.iloc[-1]
        print(f"  最新: {latest_row['date']} → DR007(FDR007)={latest_row['FDR007']}%")
    return stored


def collect_all():
    """采集所有宏观补充指标"""
    db = sqlite3.connect(str(DB_PATH))
    total = 0

    print("=" * 60)
    print("📊 L0宏观层补充数据采集（社融/M1-M2/DR007）")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 60)

    # 1. 社融增量
    total += collect_social_finance(db)

    # 2. M1/M2/剪刀差
    total += collect_money_supply(db)

    # 3. DR007
    total += collect_dr007(db)

    print(f"\n{'=' * 60}")
    print(f"✅ 采集完成，共 {total} 条记录")
    print(f"{'=' * 60}")

    # 数据预览
    print(f"\n📋 数据预览:")
    for name in ["社融增量", "M1同比", "M2同比", "M1-M2剪刀差", "DR007"]:
        row = db.execute("""
            SELECT indicator_date, indicator_value, available_at
            FROM macro_indicators WHERE indicator_name = ?
            ORDER BY indicator_date DESC LIMIT 1
        """, (name,)).fetchone()
        if row:
            print(f"  {name}: {row[1]} ({row[0]}) 可用: {row[2][:10]}")
        else:
            print(f"  {name}: 无数据")

    # 统计总量
    for name in ["社融增量", "M1同比", "M2同比", "M1-M2剪刀差", "DR007"]:
        count = db.execute("""
            SELECT COUNT(*) FROM macro_indicators WHERE indicator_name = ?
        """, (name,)).fetchone()[0]
        print(f"  {name} 总记录数: {count}")

    db.close()
    return total


if __name__ == "__main__":
    collect_all()
