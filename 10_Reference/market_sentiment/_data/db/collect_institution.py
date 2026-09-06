#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - L2机构动向层数据采集脚本
采集4个信号：
  1. 龙虎榜机构vs游资分歧度 (lhb_inst_vs_retail)
  2. 融资融券余额变化 (margin_balance_change)
  3. 大宗交易折价率 (block_trade_discount)
  4. 上市公司回购/增持 (inst_buyback_repurchase)

数据源：东方财富API（主）+ hithink-finance CLI（兜底）
依赖：python3标准库 + sqlite3 + urllib/json
"""

import json
import sqlite3
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "sentiment.db"
API_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/",
}

# ============================================================
# 建表
# ============================================================
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS institution_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,              -- 交易日 YYYY-MM-DD
    available_at TEXT NOT NULL,            -- 数据可用时间（防前视偏差，T+1）
    signal_name TEXT NOT NULL,             -- 信号标识
    signal_value REAL,                     -- 信号值
    signal_detail TEXT,                    -- 附加明细JSON
    data_source TEXT NOT NULL,             -- 'eastmoney'/'hithink'
    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    UNIQUE(trade_date, signal_name)
);
CREATE INDEX IF NOT EXISTS idx_inst_flow_date ON institution_flow(trade_date);
CREATE INDEX IF NOT EXISTS idx_inst_flow_name ON institution_flow(signal_name);
"""


# ============================================================
# HTTP 请求
# ============================================================
def fetch_eastmoney(report_name: str, page_size: int = 50,
                    sort_columns: str = "TRADE_DATE", extra_params: dict = None) -> list[dict]:
    """从东方财富API获取数据，返回data列表"""
    params = {
        "reportName": report_name,
        "columns": "ALL",
        "pageSize": str(page_size),
        "pageNumber": "1",
        "sortColumns": sort_columns,
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
    }
    if extra_params:
        params.update(extra_params)

    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        if raw.get("result") and raw["result"].get("data"):
            return raw["result"]["data"]
    except Exception as e:
        print(f"  ⚠️ 东方财富API请求失败 ({report_name}): {e}")
    return []


def run_hithink(args: list[str]) -> dict | None:
    """执行 hithink-finance CLI 命令，返回解包后的data"""
    cmd = ["hithink-finance"] + args + ["--format", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  ⚠️ CLI错误: {result.stderr[:200]}")
            return None
        raw = json.loads(result.stdout)
        if not raw.get("ok"):
            err = raw.get("error", {})
            msg = err.get("message", "") if isinstance(err, dict) else str(err)
            print(f"  ⚠️ API返回错误: {msg[:100]}")
            return None
        return raw.get("data", {})
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ hithink-finance 超时")
        return None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  ❌ hithink-finance 不可用: {e}")
        return None


# ============================================================
# 信号1: 龙虎榜机构vs游资分歧度
# ============================================================
def collect_lhb_divergence(db: sqlite3.Connection) -> dict | None:
    """
    从龙虎榜明细中提取机构净买入 vs 游资（营业部）净买入，计算分歧度。
    数据源1：东方财富 RPT_RPT_LHBSTOCKDETAILS（龙虎榜明细）
    数据源2：东方财富 RPT_RPT_LHBORGANIZE（龙虎榜机构专用）
    兜底：hithink-finance special dragon-tiger
    """
    print("\n📌 [1/4] 采集龙虎榜机构vs游资分歧度...")

    # --- 尝试东方财富API ---
    lhb_details = fetch_eastmoney("RPT_RPT_LHBSTOCKDETAILS", page_size=100,
                                   sort_columns="TRADE_DATE")
    lhb_org = fetch_eastmoney("RPT_RPT_LHBORGANIZE", page_size=100,
                               sort_columns="TRADE_DATE")

    if lhb_details:
        trade_date = lhb_details[0].get("TRADE_DATE", "").split(" ")[0]
        if not trade_date:
            trade_date = datetime.now().strftime("%Y-%m-%d")

        inst_net_buy = 0.0
        retail_net_buy = 0.0
        total_amount = 0.0

        for row in lhb_details:
            buyer_type = str(row.get("BUYER_TYPE", ""))
            net_amt = float(row.get("NET_AMOUNT", 0) or 0)
            trade_amt = float(row.get("TRADE_AMT", 0) or 0)

            if "机构" in buyer_type or "ORGANIZATION" in buyer_type.upper():
                inst_net_buy += net_amt
            else:
                retail_net_buy += net_amt
            total_amount += trade_amt

        # 补充机构专用数据
        for row in lhb_org:
            net_amt = float(row.get("NET_AMOUNT", 0) or 0)
            inst_net_buy += net_amt

        if total_amount > 0:
            divergence = abs(inst_net_buy - retail_net_buy) / total_amount
        else:
            divergence = 0.0

        inst_yi = inst_net_buy / 1e8
        retail_yi = retail_net_buy / 1e8

        print(f"  日期: {trade_date}")
        print(f"  机构净买入: {inst_yi:.2f}亿")
        print(f"  游资净买入: {retail_yi:.2f}亿")
        print(f"  分歧度: {divergence:.4f}")

        detail = json.dumps({
            "inst_net_buy_yi": round(inst_yi, 2),
            "retail_net_buy_yi": round(retail_yi, 2),
            "total_amount_yi": round(total_amount / 1e8, 2),
        }, ensure_ascii=False)

        _store_signal(db, trade_date, "lhb_inst_vs_retail", divergence, detail, "eastmoney")
        return {"trade_date": trade_date, "value": divergence,
                "inst_net": inst_yi, "retail_net": retail_yi}

    # --- 兜底：hithink-finance ---
    print("  ⏳ 东方财富API无数据，尝试 hithink-finance 兜底...")
    data = run_hithink(["special", "dragon-tiger"])
    if not data:
        print("  ⚠️ hithink-finance 也无数据（可能非交易日）")
        return None

    stock_items = data.get("stock_items", [])
    trade_date = data.get("trade_date", datetime.now().strftime("%Y-%m-%d"))
    if not stock_items:
        print("  ⚠️ 龙虎榜为空")
        return None

    inst_net_total = 0.0
    hot_money_net_total = 0.0
    for record in stock_items:
        org_net = float(record.get("org_net_value", 0) or 0)
        hot_net = float(record.get("hot_money_net_value", 0) or 0)
        inst_net_total += org_net
        hot_money_net_total += hot_net

    total = abs(inst_net_total) + abs(hot_money_net_total)
    divergence = abs(inst_net_total - hot_money_net_total) / total if total > 0 else 0.0

    inst_yi = inst_net_total / 1e8
    retail_yi = hot_money_net_total / 1e8

    print(f"  日期: {trade_date}")
    print(f"  机构净买入: {inst_yi:.2f}亿 (hithink)")
    print(f"  游资净买入: {retail_yi:.2f}亿 (hithink)")
    print(f"  分歧度: {divergence:.4f}")

    detail = json.dumps({
        "inst_net_buy_yi": round(inst_yi, 2),
        "retail_net_buy_yi": round(retail_yi, 2),
    }, ensure_ascii=False)

    _store_signal(db, trade_date, "lhb_inst_vs_retail", divergence, detail, "hithink")
    return {"trade_date": trade_date, "value": divergence,
            "inst_net": inst_yi, "retail_net": retail_yi}


# ============================================================
# 信号2: 融资融券余额变化
# ============================================================
def collect_margin_change(db: sqlite3.Connection) -> dict | None:
    """
    从东方财富 RPTA_RZRQ_LSHJ 获取融资融券全市场数据。
    计算：融资余额变化 = 当日融资余额 - 前日融资余额
    """
    print("\n📌 [2/4] 采集融资融券余额变化...")

    rows = fetch_eastmoney("RPTA_RZRQ_LSHJ", page_size=30, sort_columns="DIM_DATE")
    if not rows:
        print("  ⚠️ 东方财富API无数据")
        return None

    sorted_rows = sorted(rows, key=lambda x: x.get("DIM_DATE", ""), reverse=True)
    latest = sorted_rows[0]
    trade_date = (latest.get("DIM_DATE", "") or "").split(" ")[0]
    if not trade_date:
        trade_date = datetime.now().strftime("%Y-%m-%d")

    rz_balance = float(latest.get("RZYE", 0) or 0)    # 融资余额
    rq_balance = float(latest.get("RQYE", 0) or 0)    # 融券余额
    rz_buy = float(latest.get("RZMRE", 0) or 0)       # 融资买入额
    rz_repay = float(latest.get("RZCHE", 0) or 0)     # 融资偿还额

    if len(sorted_rows) >= 2:
        prev_rz = float(sorted_rows[1].get("RZYE", 0) or 0)
        margin_change = rz_balance - prev_rz
    else:
        margin_change = 0.0

    rz_yi = rz_balance / 1e8
    rq_yi = rq_balance / 1e8
    change_yi = margin_change / 1e8
    buy_yi = rz_buy / 1e8
    repay_yi = rz_repay / 1e8

    print(f"  日期: {trade_date}")
    print(f"  融资余额: {rz_yi:.2f}亿")
    print(f"  融券余额: {rq_yi:.2f}亿")
    print(f"  融资余额变化: {change_yi:+.2f}亿")
    print(f"  融资买入: {buy_yi:.2f}亿 | 偿还: {repay_yi:.2f}亿")

    detail = json.dumps({
        "rz_balance_yi": round(rz_yi, 2),
        "rq_balance_yi": round(rq_yi, 2),
        "rz_buy_yi": round(buy_yi, 2),
        "rz_repay_yi": round(repay_yi, 2),
        "margin_change_yi": round(change_yi, 2),
    }, ensure_ascii=False)

    _store_signal(db, trade_date, "margin_balance_change", change_yi, detail, "eastmoney")
    return {"trade_date": trade_date, "value": change_yi,
            "rz_balance": rz_yi, "rq_balance": rq_yi}


# ============================================================
# 信号3: 大宗交易折价率
# ============================================================
def collect_block_trade_discount(db: sqlite3.Connection) -> dict | None:
    """
    从东方财富 RPT_DATA_BLOCKTRADE 获取大宗交易数据。
    计算：折价率 = (成交价 - 收盘价) / 收盘价，成交额加权平均
    """
    print("\n📌 [3/4] 采集大宗交易折价率...")

    rows = fetch_eastmoney("RPT_DATA_BLOCKTRADE", page_size=100, sort_columns="TRADE_DATE")
    if not rows:
        print("  ⚠️ 东方财富API无数据")
        return None

    trade_date = (rows[0].get("TRADE_DATE", "") or "").split(" ")[0]
    if not trade_date:
        trade_date = datetime.now().strftime("%Y-%m-%d")

    # 只取最新交易日
    latest_rows = [r for r in rows if (r.get("TRADE_DATE", "") or "").startswith(trade_date)]

    total_discount = 0.0
    valid_count = 0
    total_amount = 0.0

    for row in latest_rows:
        deal_price = float(row.get("DEAL_PRICE", 0) or 0)
        close_price = float(row.get("CLOSE_PRICE", 0) or 0)
        volume = float(row.get("DEAL_AMT", 0) or 0)

        if close_price > 0 and deal_price > 0 and volume > 0:
            discount = (deal_price - close_price) / close_price
            total_discount += discount * volume
            total_amount += volume
            valid_count += 1

    avg_discount = total_discount / total_amount if total_amount > 0 else 0.0

    print(f"  日期: {trade_date}")
    print(f"  大宗交易笔数: {valid_count}")
    print(f"  成交总额: {total_amount / 1e8:.2f}亿")
    print(f"  加权平均折价率: {avg_discount:.4%}")

    detail = json.dumps({
        "trade_count": valid_count,
        "total_amount_yi": round(total_amount / 1e8, 2),
        "avg_discount_pct": round(avg_discount * 100, 2),
    }, ensure_ascii=False)

    _store_signal(db, trade_date, "block_trade_discount", avg_discount, detail, "eastmoney")
    return {"trade_date": trade_date, "value": avg_discount,
            "trade_count": valid_count}


# ============================================================
# 信号4: 上市公司回购/增持
# ============================================================
def collect_buyback_repurchase(db: sqlite3.Connection) -> dict | None:
    """
    从东方财富 RPTA_WEB_GETHGLIST_NEW 获取回购数据。
    同时尝试 hithink-finance 兜底。
    """
    print("\n📌 [4/4] 采集上市公司回购/增持...")

    trade_date = datetime.now().strftime("%Y-%m-%d")
    total_buyback_amount = 0.0
    buyback_count = 0

    # 东方财富回购数据（去掉 sortColumns，避免报错）
    buyback_rows = fetch_eastmoney("RPTA_WEB_GETHGLIST_NEW", page_size=50,
                                    extra_params={"_": str(int(datetime.now().timestamp() * 1000))})
    # 去掉 sortColumns 影响：fetch_eastmoney 会传默认值，这里用 extra_params 覆盖
    # 实际上 fetch_eastmoney 固定传了 sortColumns，需要用 filter 替代
    # 但实际测试无 sortColumns 时能返回数据，所以单独调一次无 sortColumns 的请求
    buyback_rows = _fetch_eastmoney_no_sort("RPTA_WEB_GETHGLIST_NEW", page_size=50)

    if buyback_rows:
        for row in buyback_rows:
            notice_date = (row.get("DIM_DATE") or row.get("NOTICEDATE") or "").split(" ")[0]
            if not notice_date:
                continue
            try:
                nd = datetime.strptime(notice_date, "%Y-%m-%d")
                if (datetime.now() - nd).days > 7:
                    continue
            except ValueError:
                continue

            # 回购金额：取 REPURAMOUNTLIMIT（计划金额上限）或 REPURAMOUNT（已回购金额）
            amount = float(row.get("REPURAMOUNT", 0) or 0)
            if amount == 0:
                amount = float(row.get("REPURAMOUNTLIMIT", 0) or 0)
            total_buyback_amount += amount
            buyback_count += 1

    total_yi = total_buyback_amount / 1e8
    buyback_yi = total_buyback_amount / 1e8

    print(f"  回购公告: {buyback_count}条, 金额: {buyback_yi:.2f}亿")
    print(f"  合计: {total_yi:.2f}亿")

    detail = json.dumps({
        "buyback_count": buyback_count,
        "buyback_amount_yi": round(buyback_yi, 2),
        "window_days": 7,
    }, ensure_ascii=False)

    _store_signal(db, trade_date, "inst_buyback_repurchase", total_yi, detail, "eastmoney")
    return {"trade_date": trade_date, "value": total_yi,
            "buyback": buyback_yi}


def _fetch_eastmoney_no_sort(report_name: str, page_size: int = 50) -> list[dict]:
    """不带 sortColumns 的东方财富请求，用于回购数据"""
    params = {
        "reportName": report_name,
        "columns": "ALL",
        "pageSize": str(page_size),
        "pageNumber": "1",
        "source": "WEB",
        "client": "WEB",
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        if raw.get("result") and raw["result"].get("data"):
            return raw["result"]["data"]
    except Exception as e:
        print(f"  ⚠️ 东方财富API请求失败 ({report_name}): {e}")
    return []


# ============================================================
# 存储工具函数
# ============================================================
def _store_signal(db: sqlite3.Connection, trade_date: str, signal_name: str,
                  signal_value: float, signal_detail: str, data_source: str):
    """存入 institution_flow 表，available_at = trade_date + 1天（T+1防前视偏差）"""
    try:
        dt = datetime.strptime(trade_date, "%Y-%m-%d")
    except ValueError:
        dt = datetime.now()
    available_at = (dt + timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00"

    db.execute("""
        INSERT OR REPLACE INTO institution_flow
        (trade_date, available_at, signal_name, signal_value, signal_detail, data_source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (trade_date, available_at, signal_name, round(signal_value, 6),
          signal_detail, data_source))
    db.commit()
    print(f"  ✅ 已存储: {signal_name} = {round(signal_value, 6)} (available_at={available_at[:10]})")


# ============================================================
# 主函数
# ============================================================
def collect_all():
    """采集L2机构动向层全部4个信号"""
    db = sqlite3.connect(str(DB_PATH))

    # 建表
    db.executescript(CREATE_TABLE_SQL)
    db.commit()

    now = datetime.now()
    print("=" * 60)
    print("📊 L2机构动向层数据采集")
    print(f"采集时间: {now.isoformat()}")
    print("=" * 60)

    results = {}
    total_stored = 0

    r1 = collect_lhb_divergence(db)
    if r1:
        results["lhb_inst_vs_retail"] = r1
        total_stored += 1

    r2 = collect_margin_change(db)
    if r2:
        results["margin_balance_change"] = r2
        total_stored += 1

    r3 = collect_block_trade_discount(db)
    if r3:
        results["block_trade_discount"] = r3
        total_stored += 1

    r4 = collect_buyback_repurchase(db)
    if r4:
        results["inst_buyback_repurchase"] = r4
        total_stored += 1

    print(f"\n{'=' * 60}")
    print(f"✅ L2机构动向层采集完成")
    print(f"   采集信号数: {total_stored}/4")
    print(f"   数据库: {DB_PATH}")
    print(f"\n📋 各信号最新值:")

    for name, label in [
        ("lhb_inst_vs_retail", "龙虎榜机构vs游资分歧度"),
        ("margin_balance_change", "融资融券余额变化"),
        ("block_trade_discount", "大宗交易折价率"),
        ("inst_buyback_repurchase", "回购/增持合计"),
    ]:
        row = db.execute("""
            SELECT trade_date, signal_value, signal_detail, data_source, available_at
            FROM institution_flow WHERE signal_name = ?
            ORDER BY trade_date DESC LIMIT 1
        """, (name,)).fetchone()
        if row:
            print(f"  {label}:")
            print(f"    日期: {row[0]} | 值: {row[1]} | 来源: {row[3]} | 可用: {row[4][:10]}")
            if row[2]:
                try:
                    d = json.loads(row[2])
                    for k, v in d.items():
                        print(f"      {k}: {v}")
                except json.JSONDecodeError:
                    pass
        else:
            print(f"  {label}: 无数据")

    db.close()
    return total_stored


if __name__ == "__main__":
    collect_all()
