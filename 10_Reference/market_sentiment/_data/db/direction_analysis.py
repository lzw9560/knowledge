#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 关注/回避方向分析
基于涨停池结构、机构动向、资金面、衍生品信号 + 板块热度
输出结构化JSON供报告生成器调用

用法: python3 direction_analysis.py
输出: JSON格式 {watch_directions: [...], avoid_directions: [...], market_signals: {...}}
"""

import json
import sqlite3
import sys
import subprocess
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "sentiment.db"

def run_hithink(args):
    """执行 hithink-finance CLI"""
    cmd = ["hithink-finance"] + args + ["--format", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
        raw = json.loads(result.stdout)
        if not raw.get("ok"):
            return None
        return raw.get("data", {})
    except Exception:
        return None

def query_latest(conn, table, *cols):
    """查最新一行"""
    col_str = ", ".join(cols)
    row = conn.execute(f"SELECT {col_str} FROM {table} ORDER BY trade_date DESC LIMIT 1").fetchone()
    return dict(zip(cols, row)) if row else {}

def analyze_limit_up_structure(conn):
    """分析涨停池结构"""
    row = query_latest(conn, "limit_up_pool",
        "limit_up_count", "limit_up_first_board", "limit_up_second_board",
        "limit_up_third_plus", "limit_up_one_word", "limit_up_turnover_board",
        "broken_limit_count", "broken_rate", "max_consecutive_boards",
        "consecutive_ladder")

    if not row or not row.get("limit_up_count"):
        return {"available": False}

    count = row["limit_up_count"] or 0
    broken = row.get("broken_limit_count")
    broken_rate = row.get("broken_rate")
    ladder_raw = row.get("consecutive_ladder", "{}")
    try:
        ladder = json.loads(ladder_raw) if isinstance(ladder_raw, str) else (ladder_raw or {})
    except Exception:
        ladder = {}

    # 封板率
    seal_rate = None
    if broken is not None and count > 0:
        seal_rate = count / (count + broken) if (count + broken) > 0 else None

    # 情绪判断
    if count >= 80:
        mood = "overheat"
    elif count >= 50:
        mood = "hot"
    elif count >= 30:
        mood = "normal"
    elif count >= 15:
        mood = "cold"
    else:
        mood = "freezing"

    return {
        "available": True,
        "limit_up_count": count,
        "first_board": row.get("limit_up_first_board"),
        "second_board": row.get("limit_up_second_board"),
        "third_plus": row.get("limit_up_third_plus"),
        "one_word": row.get("limit_up_one_word"),
        "turnover_board": row.get("limit_up_turnover_board"),
        "broken_count": broken,
        "broken_rate": broken_rate,
        "seal_rate": seal_rate,
        "max_consecutive": row.get("max_consecutive_boards"),
        "ladder": ladder,
        "mood": mood,
    }

def analyze_hot_stocks():
    """从热榜提取板块热度"""
    data = run_hithink(["special", "hot-stock"])
    if not data:
        return []
    items = data.get("item", [])
    # 提取板块关键词
    sectors = {}
    for stock in items[:20]:
        name = stock.get("name", "")
        code = stock.get("thscode", "")
        heat = stock.get("heat", 0)
        # hithink热榜可能带板块标签
        sector = stock.get("industry", stock.get("sector", ""))
        if sector:
            sectors[sector] = sectors.get(sector, 0) + heat
    return sorted(sectors.items(), key=lambda x: -x[1])[:5]

def analyze_institution_flow(conn):
    """分析机构动向"""
    rows = conn.execute(
        "SELECT signal_name, signal_value, signal_detail FROM institution_flow ORDER BY trade_date DESC LIMIT 10"
    ).fetchall()

    result = {}
    for r in rows:
        name, value, detail = r[0], r[1], r[2]
        detail_dict = json.loads(detail) if detail else {}
        result[name] = {"value": value, "detail": detail_dict}

    # 机构vs游资分歧
    lhb = result.get("lhb_inst_vs_retail", {})
    inst_net = lhb.get("detail", {}).get("inst_net_buy_yi")
    retail_net = lhb.get("detail", {}).get("retail_net_buy_yi")

    # 融资余额变化
    margin = result.get("margin_balance_change", {})
    margin_change = margin.get("value")

    # 大宗折价
    block = result.get("block_trade_discount", {})
    block_discount = block.get("value")

    # 回购
    buyback = result.get("inst_buyback_repurchase", {})

    signals = {}
    if margin_change is not None:
        signals["margin_direction"] = "bullish" if margin_change > 0 else "bearish"
    if block_discount is not None:
        signals["block_discount"] = f"{block_discount*100:.1f}%"
    if inst_net is not None:
        signals["inst_net"] = f"{inst_net}亿"
    if retail_net is not None:
        signals["retail_net"] = f"{retail_net}亿"

    return {
        "available": bool(result),
        "margin_change": margin_change,
        "block_discount": block_discount,
        "inst_net_buy": inst_net,
        "retail_net_buy": retail_net,
        "buyback_amount": buyback.get("value"),
        "signals": signals,
    }

def analyze_capital_flow(conn):
    """分析资金面"""
    rows = conn.execute(
        "SELECT signal_name, signal_value, extra_data FROM capital_flow_signals ORDER BY trade_date DESC LIMIT 10"
    ).fetchall()

    result = {}
    for r in rows:
        name, value, extra = r[0], r[1], r[2]
        extra_dict = json.loads(extra) if extra else {}
        result[name] = {"value": value, "extra": extra_dict}

    main_net = result.get("main_capital_net", {}).get("value")
    north = result.get("northbound_net", {}).get("value")
    cds = result.get("cds_spread", {}).get("value")

    return {
        "available": bool(result),
        "main_capital_net": main_net,
        "northbound_net": north,
        "cds_spread": cds,
        "main_direction": "bullish" if (main_net or 0) > 0 else "bearish" if main_net else "neutral",
    }

def analyze_derivatives(conn):
    """分析衍生品信号"""
    row = query_latest(conn, "derivatives_data",
        "hs300_pcr_position", "hs300_iv_change", "basis_if", "hs300_skew_25d")

    if not row:
        return {"available": False}

    pcr = row.get("hs300_pcr_position")
    iv = row.get("hs300_iv_change")
    basis = row.get("basis_if")
    skew = row.get("hs300_skew_25d")

    # PCR > 1 偏空, < 0.5 偏多
    pcr_signal = "neutral"
    if pcr:
        if pcr > 1.3:
            pcr_signal = "bearish"
        elif pcr < 0.5:
            pcr_signal = "bullish"

    # 基差贴水 = 看空
    basis_signal = "neutral"
    if basis:
        if basis < -0.3:
            basis_signal = "bearish"
        elif basis > 0.1:
            basis_signal = "bullish"

    return {
        "available": True,
        "pcr": pcr,
        "pcr_signal": pcr_signal,
        "iv_change": iv,
        "basis_if": basis,
        "basis_signal": basis_signal,
        "skew": skew,
    }

def generate_directions(limit_up, institution, capital, derivatives, hot_sectors):
    """综合各层信号生成关注/回避方向"""

    watch = []
    avoid = []
    reasons_watch = []
    reasons_avoid = []

    # === 从涨停池结构判断 ===
    if limit_up.get("available"):
        mood = limit_up.get("mood", "normal")
        count = limit_up.get("limit_up_count", 0)
        seal_rate = limit_up.get("seal_rate")
        broken_rate = limit_up.get("broken_rate")

        # 炸板率高 → 回避打板
        if broken_rate and broken_rate > 0.3:
            avoid.append({"direction": "高位连板打板", "reason": f"炸板率{broken_rate:.0%}，封板率仅{seal_rate:.0%}，打板亏钱效应明显"})
        # 涨停数极低 → 回避全市场
        if count < 20:
            avoid.append({"direction": "短线题材股", "reason": f"涨停仅{count}家，情绪冰点，题材股流动性差"})

    # === 从机构动向判断 ===
    if institution.get("available"):
        inst_net = institution.get("inst_net_buy")
        margin_change = institution.get("margin_change")
        block_discount = institution.get("block_discount")

        # 机构净卖出 → 回避
        if inst_net is not None and inst_net < -10:
            avoid.append({"direction": "机构抛售的个股", "reason": f"龙虎榜机构净卖出{abs(inst_net):.1f}亿"})

        # 融资余额下降 → 回避融资盘重的板块
        if margin_change is not None and margin_change < -20:
            avoid.append({"direction": "融资盘重的板块", "reason": f"融资余额净减少{abs(margin_change):.1f}亿，杠杆资金在撤"})

        # 大宗折价大 → 回避
        if block_discount is not None and block_discount < -0.05:
            avoid.append({"direction": "大宗交易折价大的个股", "reason": f"大宗平均折价{block_discount*100:.1f}%，机构大宗出货"})

        # 回购增加 → 关注
        buyback = institution.get("buyback_amount")
        if buyback and buyback > 10:
            watch.append({"direction": "有增持/回购的个股", "reason": f"近7日回购金额{buyback:.1f}亿，产业资本看好"})

    # === 从资金面判断 ===
    if capital.get("available"):
        main_net = capital.get("main_capital_net")
        if main_net is not None:
            if main_net > 50:
                watch.append({"direction": "主力资金净流入的板块", "reason": f"主力净流入{main_net:.1f}亿"})
            elif main_net < -50:
                avoid.append({"direction": "主力资金净流出的板块", "reason": f"主力净流出{abs(main_net):.1f}亿"})

    # === 从衍生品判断 ===
    if derivatives.get("available"):
        pcr_sig = derivatives.get("pcr_signal", "neutral")
        basis_sig = derivatives.get("basis_signal", "neutral")
        basis = derivatives.get("basis_if")

        if basis_sig == "bearish":
            avoid.append({"direction": "大盘权重股（IF贴水）", "reason": f"IF基差{basis:.2f}%，期货贴水，套保压力"})
        if pcr_sig == "bullish":
            watch.append({"direction": "期权偏多的方向", "reason": f"PCR={derivatives.get('pcr')}，Call远超Put"})

    # === 从热榜判断 ===
    if hot_sectors:
        top_sectors = [s[0] for s in hot_sectors[:3]]
        watch.append({"direction": f"热榜Top板块: {', '.join(top_sectors)}", "reason": "资金关注度最高的板块"})

    # === 通用规则 ===
    # 情绪退潮期通用建议
    if limit_up.get("available"):
        mood = limit_up.get("mood", "normal")
        if mood in ("cold", "freezing"):
            avoid.append({"direction": "纯题材高位小票", "reason": "情绪退潮期，无业绩支撑的题材股是重灾区"})
            watch.append({"direction": "有业绩支撑的主线赛道", "reason": "退潮期资金向确定性高的主线集中"})
        elif mood == "overheat":
            avoid.append({"direction": "过热板块追高", "reason": "涨停数过多，情绪过热，均值回归概率高"})

    return {
        "watch_directions": watch,
        "avoid_directions": avoid,
        "market_mood": limit_up.get("mood", "unknown"),
        "limit_up_count": limit_up.get("limit_up_count"),
        "seal_rate": limit_up.get("seal_rate"),
        "data_sources": {
            "limit_up": limit_up.get("available", False),
            "institution": institution.get("available", False),
            "capital": capital.get("available", False),
            "derivatives": derivatives.get("available", False),
        },
    }

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # 1. 涨停池结构
    limit_up = analyze_limit_up_structure(conn)

    # 2. 热榜板块
    hot_sectors = analyze_hot_stocks()

    # 3. 机构动向
    institution = analyze_institution_flow(conn)

    # 4. 资金面
    capital = analyze_capital_flow(conn)

    # 5. 衍生品
    derivatives = analyze_derivatives(conn)

    # 6. 综合生成方向
    result = generate_directions(limit_up, institution, capital, derivatives, hot_sectors)

    result["generated_at"] = datetime.now().isoformat()
    result["trade_date"] = datetime.now().strftime("%Y-%m-%d")

    conn.close()

    # 输出JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
