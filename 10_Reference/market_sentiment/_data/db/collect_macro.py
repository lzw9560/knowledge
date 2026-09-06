#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 宏观数据采集脚本
采集 CPI/PPI/PMI 等宏观指标（东方财富API）

已验证可用接口：
- RPT_ECONOMY_CPI (居民消费价格指数)
- RPT_ECONOMY_PPI (工业品出厂价格指数)
- RPT_ECONOMY_PMI (采购经理人指数)

已实现（见 collect_macro_extra.py）：
- ✅ 社融增量 → akshare macro_china_shrzgm()，月频，136条
- ✅ M1-M2剪刀差 → akshare macro_china_money_supply()，月频，223条
- ✅ DR007 → akshare repo_rate_query(symbol='DR007')，日频，249条
"""

import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "sentiment.db"

# ============================================================
# 已验证可用的东方财富宏观API
# ============================================================
WORKING_APIS = {
    "cpi": {
        "name": "CPI同比",
        "report_name": "RPT_ECONOMY_CPI",
        "value_field": "NATIONAL_SAME",
        "unit": "%",
        "lag_days": 10,
        "description": "居民消费价格指数同比",
    },
    "ppi": {
        "name": "PPI同比",
        "report_name": "RPT_ECONOMY_PPI",
        "value_field": "BASE_SAME",
        "unit": "%",
        "lag_days": 10,
        "description": "工业品出厂价格指数同比",
    },
    "pmi": {
        "name": "制造业PMI",
        "report_name": "RPT_ECONOMY_PMI",
        "value_field": "MAKE_INDEX",
        "unit": "",
        "lag_days": 0,
        "description": "制造业采购经理人指数",
    },
}

API_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/"
}


def fetch_indicator(report_name: str, value_field: str, page_size: int = 24) -> list[dict]:
    """从东方财富API获取数据"""
    params = {
        "reportName": report_name,
        "columns": "ALL",
        "pageSize": page_size,
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageNumber": 1,
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("result") and data["result"].get("data"):
        return data["result"]["data"]
    return []


def store_indicator(db: sqlite3.Connection, indicator_name: str, date_str: str,
                    value: float, unit: str, lag_days: int):
    """存入数据库（带防前视偏差的available_at）"""
    dt = datetime.strptime(date_str.split(" ")[0], "%Y-%m-%d")
    available_at = (dt + timedelta(days=lag_days)).isoformat()

    db.execute("""
        INSERT OR IGNORE INTO macro_indicators
        (indicator_date, available_at, indicator_name, indicator_value, indicator_unit)
        VALUES (?, ?, ?, ?, ?)
    """, (date_str.split(" ")[0], available_at, indicator_name, round(value, 4), unit))


def collect_all():
    """采集所有可用宏观指标"""
    db = sqlite3.connect(str(DB_PATH))
    total = 0

    print("=" * 50)
    print("📊 L0宏观层数据采集")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 50)

    for key, config in WORKING_APIS.items():
        print(f"\n📌 采集 {config['name']}...")
        try:
            raw = fetch_indicator(config["report_name"], config["value_field"])
            if not raw:
                print(f"  ⚠️ 无数据")
                continue

            stored = 0
            for row in raw:
                date_str = row.get("REPORT_DATE", "")
                value = row.get(config["value_field"])
                if date_str and value is not None:
                    try:
                        value = float(value)
                        store_indicator(db, config["name"], date_str, value,
                                       config["unit"], config["lag_days"])
                        stored += 1
                    except (ValueError, TypeError):
                        pass

            db.commit()
            total += stored
            print(f"  ✅ 存储 {stored} 条记录")

            # 显示最新数据
            latest = raw[0] if raw else None
            if latest:
                print(f"  最新: {latest.get('REPORT_DATE','').split(' ')[0]} → {config['name']}={latest.get(config['value_field'])}")

        except Exception as e:
            print(f"  ❌ 失败: {e}")

    # 派生指标：CPI-PPI剪刀差
    print(f"\n📌 计算派生指标: CPI-PPI剪刀差...")
    cpi_rows = db.execute("""
        SELECT indicator_date, indicator_value FROM macro_indicators
        WHERE indicator_name = 'CPI同比' ORDER BY indicator_date DESC LIMIT 24
    """).fetchall()
    ppi_rows = db.execute("""
        SELECT indicator_date, indicator_value FROM macro_indicators
        WHERE indicator_name = 'PPI同比' ORDER BY indicator_date DESC LIMIT 24
    """).fetchall()

    ppi_map = {r[0]: r[1] for r in ppi_rows}
    derived = 0
    for cpi_date, cpi_val in cpi_rows:
        if cpi_date in ppi_map:
            scissors = cpi_val - ppi_map[cpi_date]
            store_indicator(db, "CPI-PPI剪刀差", cpi_date + " 00:00:00",
                           scissors, "%", 10)
            derived += 1
    db.commit()
    total += derived
    print(f"  ✅ 派生 {derived} 条CPI-PPI剪刀差")

    print(f"\n{'=' * 50}")
    print(f"✅ 采集完成，共 {total} 条记录")

    # 数据预览
    print(f"\n📋 数据预览:")
    for name in ["CPI同比", "PPI同比", "制造业PMI", "CPI-PPI剪刀差"]:
        row = db.execute("""
            SELECT indicator_date, indicator_value, available_at
            FROM macro_indicators WHERE indicator_name = ?
            ORDER BY indicator_date DESC LIMIT 1
        """, (name,)).fetchone()
        if row:
            print(f"  {name}: {row[1]} ({row[0]}) 可用: {row[2][:10]}")
        else:
            print(f"  {name}: 无数据")

    print(f"\n⚠️ TODO: 社融/M1-M2/DR007 需用akshare或央行官网接口（待接入）")

    db.close()
    return total


if __name__ == "__main__":
    collect_all()
