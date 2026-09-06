#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 事件驱动告警监控
路径: _data/db/alert_monitor.py

功能:
  1. 查询数据库最新数据
  2. 检查是否触发告警条件（涨停/炸板/龙虎榜/DR007/PMI/M1-M2/基差/PCR）
  3. 如果触发告警，输出JSON格式告警信息
  4. 如果没有触发，输出 "NO_ALERT"

用法:
  python3 alert_monitor.py
  python3 alert_monitor.py --json
  python3 alert_monitor.py --db /path/to/sentiment.db --config /path/to/framework_config.json

告警条件:
  - 涨停数 > 80 或 < 20（极端情绪）
  - 炸板率 > 30%（恐慌信号）
  - 龙虎榜机构净卖出 > 20亿（机构出逃）
  - DR007 > 3.0 或 < 1.0（流动性异常）
  - PMI < 49 或 > 51（宏观极端）
  - M1-M2剪刀差 < -8（资金活化极低）
  - 沪深300基差 < -30（期货大幅贴水）
  - PCR > 1.3 或 < 0.5（期权极端偏空/偏多）

依赖: python3标准库 + sqlite3
"""

import json
import sqlite3
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# 默认路径
# ============================================================
SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB = SCRIPT_DIR / "sentiment.db"
DEFAULT_CONFIG = SCRIPT_DIR / "framework_config.json"

# ============================================================
# 默认阈值（可被config覆盖）
# ============================================================
DEFAULT_THRESHOLDS = {
    # L4 市场情绪
    "limit_up_count_high": 80,       # 涨停数过高
    "limit_up_count_low": 20,        # 涨停数过低
    "broken_rate_high": 0.30,        # 炸板率过高(30%)

    # L2 机构动向
    "lhb_inst_net_sell_high": 20,    # 龙虎榜机构净卖出(亿)

    # L0 宏观
    "dr007_high": 3.0,               # DR007过高(流动性紧张)
    "dr007_low": 1.0,                # DR007过低(流动性泛滥)
    "pmi_low": 49,                   # PMI低于荣枯线附近
    "pmi_high": 51,                  # PMI高于荣枯线附近
    "m1_m2_scissors_low": -8,        # M1-M2剪刀差极低

    # L5 衍生品
    "basis_low": -0.3,                # 基差大幅贴水(%)，-0.3表示-0.3%
    "pcr_high": 1.3,                # PCR偏空
    "pcr_low": 0.5,                 # PCR偏多
}


# ============================================================
# 数据库查询
# ============================================================

def get_db_path(arg_db=None):
    """获取数据库路径"""
    if arg_db:
        return Path(arg_db)
    return DEFAULT_DB


def get_config_path(arg_config=None):
    """获取配置路径"""
    if arg_config:
        return Path(arg_config)
    return DEFAULT_CONFIG


def query_latest_snapshot(conn):
    """查询最新市场快照"""
    cursor = conn.execute("""
        SELECT * FROM market_snapshot
        ORDER BY trade_date DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))
    return None


def query_latest_limit_up(conn):
    """查询最新涨停池数据"""
    cursor = conn.execute("""
        SELECT * FROM limit_up_pool
        ORDER BY trade_date DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))
    return None


def query_latest_macro(conn, indicator_name, limit=1):
    """查询最新宏观指标"""
    cursor = conn.execute("""
        SELECT indicator_name, indicator_value, indicator_date, available_at
        FROM macro_indicators
        WHERE indicator_name = ?
        ORDER BY indicator_date DESC
        LIMIT ?
    """, (indicator_name, limit))
    rows = cursor.fetchall()
    if rows:
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, r)) for r in rows]
    return []


def query_latest_derivatives(conn):
    """查询最新衍生品数据"""
    cursor = conn.execute("""
        SELECT * FROM derivatives_data
        ORDER BY trade_date DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))
    return None


def query_latest_capital_flow(conn):
    """查询最新资金流数据"""
    cursor = conn.execute("""
        SELECT * FROM capital_flow
        ORDER BY trade_date DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))
    return None


def query_circuit_breaker_status(conn):
    """查询当前熔断状态"""
    cursor = conn.execute("""
        SELECT * FROM circuit_breaker_log
        ORDER BY trigger_date DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        cols = [d[0] for d in cursor.description]
        result = dict(zip(cols, row))
        # 如果有恢复日期，说明已恢复
        if result.get("recovery_date") and result["recovery_date"] <= datetime.now().strftime("%Y-%m-%d"):
            return {"level": 0, "active": False}
        return {"level": result.get("level", 0), "active": True, **result}
    return {"level": 0, "active": False}


# ============================================================
# 告警检查
# ============================================================

def check_alerts(thresholds, snapshot=None, limit_up=None, macro_data=None,
                 derivatives=None, capital_flow=None, cb_status=None):
    """
    检查所有告警条件，返回告警列表
    """
    alerts = []

    # ----------------------------------------------------------
    # L4: 涨停数极端
    # ----------------------------------------------------------
    if limit_up:
        lu_count = limit_up.get("limit_up_count")
        if lu_count is not None:
            if lu_count > thresholds["limit_up_count_high"]:
                alerts.append({
                    "alert_level": "warning",
                    "layer": "L4",
                    "signal_name": "涨停数过高",
                    "current_value": lu_count,
                    "threshold": thresholds["limit_up_count_high"],
                    "message": f"涨停数 {lu_count} 家 > {thresholds['limit_up_count_high']}，情绪极度乐观，注意过热回调风险"
                })
            elif lu_count < thresholds["limit_up_count_low"]:
                alerts.append({
                    "alert_level": "critical",
                    "layer": "L4",
                    "signal_name": "涨停数过低",
                    "current_value": lu_count,
                    "threshold": thresholds["limit_up_count_low"],
                    "message": f"涨停数仅 {lu_count} 家 < {thresholds['limit_up_count_low']}，市场情绪冰点，可能触发恐慌"
                })

        # 炸板率
        broken_rate = limit_up.get("broken_rate")
        if broken_rate is not None:
            if broken_rate > thresholds["broken_rate_high"]:
                alerts.append({
                    "alert_level": "critical",
                    "layer": "L4",
                    "signal_name": "炸板率过高",
                    "current_value": f"{broken_rate:.1%}",
                    "threshold": f"{thresholds['broken_rate_high']:.0%}",
                    "message": f"炸板率 {broken_rate:.1%} > {thresholds['broken_rate_high']:.0%}，打板资金大面积亏损，恐慌信号"
                })

    # ----------------------------------------------------------
    # L2: 龙虎榜机构净卖出
    # ----------------------------------------------------------
    if snapshot:
        lhb_inst_net = snapshot.get("l2_lhb_inst_net_buy")
        if lhb_inst_net is not None and lhb_inst_net < -thresholds["lhb_inst_net_sell_high"]:
            alerts.append({
                "alert_level": "critical",
                "layer": "L2",
                "signal_name": "龙虎榜机构净卖出",
                "current_value": f"{lhb_inst_net:.1f}亿",
                "threshold": f"-{thresholds['lhb_inst_net_sell_high']}亿",
                "message": f"龙虎榜机构净卖出 {abs(lhb_inst_net):.1f} 亿 > {thresholds['lhb_inst_net_sell_high']} 亿，机构大幅出逃"
            })

    # ----------------------------------------------------------
    # L0: DR007 流动性异常
    # ----------------------------------------------------------
    # 优先从macro_indicators表查
    dr007_value = None
    if macro_data:
        for item in macro_data:
            if item.get("indicator_name") == "DR007":
                dr007_value = item.get("indicator_value")
                break

    # 如果macro表没有，从snapshot查
    if dr007_value is None and snapshot:
        # snapshot存的是z-score，不是原始值，需要从其他来源
        pass

    if dr007_value is not None:
        if dr007_value > thresholds["dr007_high"]:
            alerts.append({
                "alert_level": "critical",
                "layer": "L0",
                "signal_name": "DR007流动性紧张",
                "current_value": f"{dr007_value:.2f}%",
                "threshold": f"{thresholds['dr007_high']}%",
                "message": f"DR007 = {dr007_value:.2f}% > {thresholds['dr007_high']}%，银行间流动性紧张，利空股市"
            })
        elif dr007_value < thresholds["dr007_low"]:
            alerts.append({
                "alert_level": "warning",
                "layer": "L0",
                "signal_name": "DR007流动性泛滥",
                "current_value": f"{dr007_value:.2f}%",
                "threshold": f"{thresholds['dr007_low']}%",
                "message": f"DR007 = {dr007_value:.2f}% < {thresholds['dr007_low']}%，流动性极度宽松，可能催生泡沫"
            })

    # ----------------------------------------------------------
    # L0: PMI 宏观极端
    # ----------------------------------------------------------
    pmi_value = None
    if macro_data:
        for item in macro_data:
            if item.get("indicator_name") == "制造业PMI":
                pmi_value = item.get("indicator_value")
                break

    if pmi_value is not None:
        if pmi_value < thresholds["pmi_low"]:
            alerts.append({
                "alert_level": "critical",
                "layer": "L0",
                "signal_name": "PMI低于荣枯线",
                "current_value": pmi_value,
                "threshold": thresholds["pmi_low"],
                "message": f"制造业PMI = {pmi_value} < {thresholds['pmi_low']}，经济收缩信号，战略性看空"
            })
        elif pmi_value > thresholds["pmi_high"]:
            alerts.append({
                "alert_level": "warning",
                "layer": "L0",
                "signal_name": "PMI过热",
                "current_value": pmi_value,
                "threshold": thresholds["pmi_high"],
                "message": f"制造业PMI = {pmi_value} > {thresholds['pmi_high']}，经济过热，紧缩政策预期升温"
            })

    # ----------------------------------------------------------
    # L0: M1-M2剪刀差极低
    # ----------------------------------------------------------
    m1_m2_value = None
    if macro_data:
        for item in macro_data:
            if item.get("indicator_name") == "M1-M2剪刀差":
                m1_m2_value = item.get("indicator_value")
                break

    if m1_m2_value is not None:
        if m1_m2_value < thresholds["m1_m2_scissors_low"]:
            alerts.append({
                "alert_level": "critical",
                "layer": "L0",
                "signal_name": "M1-M2剪刀差极低",
                "current_value": f"{m1_m2_value}%",
                "threshold": f"{thresholds['m1_m2_scissors_low']}%",
                "message": f"M1-M2剪刀差 = {m1_m2_value}% < {thresholds['m1_m2_scissors_low']}%，资金活化极度低迷，企业投资意愿极低"
            })

    # ----------------------------------------------------------
    # L5: 沪深300基差大幅贴水
    # ----------------------------------------------------------
    # basis_if 在数据库中以 % 存储（如 -0.35 表示 -0.35%）
    # 阈值 basis_low 也改为百分比（-0.3 表示 -0.3%）
    basis_value = None
    if derivatives:
        basis_value = derivatives.get("basis_if")
    if basis_value is None and snapshot:
        basis_value = snapshot.get("l5_basis_if")

    if basis_value is not None:
        # 直接以百分比比较，不做点数换算
        if basis_value < thresholds["basis_low"]:
            alerts.append({
                "alert_level": "critical",
                "layer": "L5",
                "signal_name": "沪深300基差贴水",
                "current_value": f"{basis_value:.2f}%",
                "threshold": f"{thresholds['basis_low']:.1f}%",
                "message": f"IF基差 = {basis_value:.2f}% < {thresholds['basis_low']:.1f}%，期货大幅贴水，套保/做空力量极强"
            })

    # ----------------------------------------------------------
    # L5: PCR 极端
    # ----------------------------------------------------------
    pcr_value = None
    if derivatives:
        pcr_value = derivatives.get("hs300_pcr_position")
    if pcr_value is None and snapshot:
        pcr_value = snapshot.get("l5_pcr_position")

    if pcr_value is not None:
        if pcr_value > thresholds["pcr_high"]:
            alerts.append({
                "alert_level": "warning",
                "layer": "L5",
                "signal_name": "PCR极度偏空",
                "current_value": pcr_value,
                "threshold": thresholds["pcr_high"],
                "message": f"沪深300持仓量PCR = {pcr_value} > {thresholds['pcr_high']}，Put持仓远超Call，市场极度看跌"
            })
        elif pcr_value < thresholds["pcr_low"]:
            alerts.append({
                "alert_level": "warning",
                "layer": "L5",
                "signal_name": "PCR极度偏多",
                "current_value": pcr_value,
                "threshold": thresholds["pcr_low"],
                "message": f"沪深300持仓量PCR = {pcr_value} < {thresholds['pcr_low']}，Call持仓远超Put，市场极度看涨，注意拥挤"
            })

    # ----------------------------------------------------------
    # 熔断状态检查
    # ----------------------------------------------------------
    if cb_status and cb_status.get("level", 0) > 0:
        level = cb_status["level"]
        level_names = {1: "降权", 2: "暂停", 3: "冻结"}
        alerts.append({
            "alert_level": "critical" if level >= 2 else "warning",
            "layer": "SYSTEM",
            "signal_name": f"熔断Level{level}",
            "current_value": f"Level {level} ({level_names.get(level, '未知')})",
            "threshold": "Level 0 (正常)",
            "message": f"框架处于熔断状态 Level {level}：{cb_status.get('reason', '未知原因')}。{cb_status.get('action_taken', '')}"
        })

    return alerts


# ============================================================
# 主流程
# ============================================================

def load_config(config_path):
    """加载配置文件，合并阈值"""
    with open(config_path) as f:
        config = json.load(f)

    # 尝试从配置文件中提取阈值
    thresholds = dict(DEFAULT_THRESHOLDS)

    # 如果配置文件中有自定义阈值，覆盖默认值
    # 目前config中没有显式的alert字段，使用默认值
    return config, thresholds


def run_alert_check(db_path=None, config_path=None):
    """执行告警检查，返回告警结果"""
    db_path = get_db_path(db_path)
    config_path = get_config_path(config_path)

    # 检查文件是否存在
    if not db_path.exists():
        return {"error": f"数据库文件不存在: {db_path}"}
    if not config_path.exists():
        return {"error": f"配置文件不存在: {config_path}"}

    # 加载配置
    config, thresholds = load_config(config_path)

    # 连接数据库
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    try:
        # 查询最新数据
        snapshot = query_latest_snapshot(conn)
        limit_up = query_latest_limit_up(conn)
        macro_names = ["DR007", "制造业PMI", "M1-M2剪刀差"]
        macro_data = []
        for name in macro_names:
            macro_data.extend(query_latest_macro(conn, name, 1))
        derivatives = query_latest_derivatives(conn)
        capital_flow = query_latest_capital_flow(conn)
        cb_status = query_circuit_breaker_status(conn)

        # 检查告警
        alerts = check_alerts(
            thresholds=thresholds,
            snapshot=snapshot,
            limit_up=limit_up,
            macro_data=macro_data,
            derivatives=derivatives,
            capital_flow=capital_flow,
            cb_status=cb_status
        )

        # 构建输出
        result = {
            "check_time": datetime.now().isoformat(),
            "db_path": str(db_path),
            "snapshot_date": snapshot["trade_date"] if snapshot else None,
            "limit_up_date": limit_up["trade_date"] if limit_up else None,
            "alerts_count": len(alerts),
            "alerts": alerts,
        }

        return result

    finally:
        conn.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="大A舆情预判框架 - 事件驱动告警监控"
    )
    parser.add_argument("--db", help="数据库路径", default=None)
    parser.add_argument("--config", help="配置文件路径", default=None)
    parser.add_argument("--json", action="store_true", help="以JSON格式输出（默认）")
    parser.add_argument("--quiet", action="store_true", help="无告警时也输出NO_ALERT")
    args = parser.parse_args()

    result = run_alert_check(args.db, args.config)

    # 如果有错误
    if "error" in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 输出结果
    if result["alerts_count"] > 0:
        # JSON格式输出告警
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 无告警
        if args.quiet or args.json:
            result["alerts"] = []
            result["status"] = "NO_ALERT"
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("NO_ALERT")


if __name__ == "__main__":
    main()
