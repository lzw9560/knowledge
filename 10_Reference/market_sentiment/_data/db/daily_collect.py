#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 日终数据采集编排器
按依赖顺序串联所有采集器，每日盘后自动运行

运行时间：每个交易日 17:00 后
运行顺序：
1. L0 宏观（月频，日频检查是否有新数据）
2. L1 政策（事件驱动，每日检查）
3. L2 机构（T+1数据，采集前一日龙虎榜等）
4. L3 资金（当日资金面数据）
5. L4 情绪（当日涨停池等）
6. L5 衍生品（当日期权/期货）
7. 评分引擎（全量信号 → 三维向量 → 仓位建议）
8. 告警检查（8项阈值）
"""

import subprocess
import sys
import json
import sqlite3
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# 配置
# ============================================================
DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "sentiment.db"
LOG_FILE = DB_DIR / "daily_collect.log"

COLLECTORS = [
    # (层级, 脚本名, 描述, 必须成功)
    ("L0", "collect_macro.py",       "宏观采集器(CPI/PPI/PMI)",        False),
    ("L0", "collect_macro_extra.py", "宏观补充(社融/M1M2/DR007)",     False),
    ("L1", "collect_policy.py",      "政策事件采集器",                  False),
    ("L2", "collect_institution.py", "机构动向采集器(龙虎榜/融资融券)", False),
    ("L3", "collect_capital.py",     "资金面采集器(北向/主力/成交额)",  False),
    ("L4", "collect_sentiment.py",   "市场情绪采集器(涨停池/炸板)",     True),
    ("L5", "collect_derivatives.py", "衍生品采集器(PCR/IV/基差)",      False),
]

ENGINE_SCRIPT = "sentiment_engine.py"
ALERT_SCRIPT = "alert_monitor.py"

# ============================================================
# 日志
# ============================================================
def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ============================================================
# 运行采集器
# ============================================================
def run_collector(layer: str, script: str, desc: str, required: bool) -> bool:
    """运行单个采集器"""
    script_path = DB_DIR / script
    if not script_path.exists():
        log(f"{layer} {script} 不存在，跳过", "WARN")
        return False
    
    log(f"{layer} 开始采集: {desc} ({script})")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=120, cwd=str(DB_DIR)
        )
        if result.returncode == 0:
            # 提取最后几行输出作为摘要
            output_lines = result.stdout.strip().split("\n")
            summary = "\n".join(output_lines[-5:]) if output_lines else "无输出"
            log(f"{layer} 采集完成: {script}\n{summary}")
            return True
        else:
            err = result.stderr.strip().split("\n")[-3:] if result.stderr else "无错误输出"
            log(f"{layer} 采集失败: {script}\n{chr(10).join(err)}", "ERROR")
            if required:
                log(f"{layer} 是必须采集器，失败将影响评分", "ERROR")
            return False
    except subprocess.TimeoutExpired:
        log(f"{layer} 采集超时(120s): {script}", "ERROR")
        return False
    except Exception as e:
        log(f"{layer} 采集异常: {script} - {e}", "ERROR")
        return False

# ============================================================
# 运行评分引擎
# ============================================================
def run_engine(trade_date: str) -> dict:
    """运行评分引擎，生成当日评分"""
    log(f"开始运行评分引擎，交易日={trade_date}")
    
    try:
        # 导入引擎
        sys.path.insert(0, str(DB_DIR))
        from sentiment_engine import SentimentEngine
        
        engine = SentimentEngine()
        
        # 从数据库自动读取各层最新信号
        all_signals = auto_read_signals(engine.db, trade_date)
        
        if not any(all_signals.values()):
            log("数据库中无可用信号数据，跳过评分", "WARN")
            engine.close()
            return {"status": "no_data"}
        
        # 生成报告
        report = engine.generate_report(trade_date, all_signals)
        
        # 存入market_snapshot表
        save_snapshot(engine.db, report)
        
        # 存入signal_log表
        save_signal_log(engine.db, report, trade_date)
        
        engine.close()
        
        comp = report["composite"]
        log(f"评分完成: Z={comp['temperature_z']:+.4f} 方向={comp['direction']} "
            f"置信度={comp['confidence']:.1%} 熔断=L{report['circuit_breaker']['level']}")
        
        return report
    
    except Exception as e:
        log(f"评分引擎异常: {e}\n{traceback.format_exc()}", "ERROR")
        return {"status": "error", "error": str(e)}

# ============================================================
# 自动读取各层最新信号
# ============================================================
def auto_read_signals(db, trade_date: str) -> dict:
    """从数据库各表自动读取最新信号值"""
    signals = {"L0_macro": {}, "L1_policy": {}, "L2_institution": {}, 
               "L3_capital": {}, "L4_sentiment": {}, "L5_derivatives": {}}
    
    # L0 宏观 — macro_indicators 表的列名是 indicator_name
    macro_name_map = {
        "social_finance": "社融增量",
        "m1_m2_scissors": "M1-M2剪刀差",
        "pmi": "制造业PMI",
        "dr007": "DR007",
        "cpi_ppi": "CPI-PPI剪刀差",
    }
    try:
        for sig_name, indi_name in macro_name_map.items():
            row = db.execute(
                "SELECT indicator_value FROM macro_indicators WHERE indicator_name=? ORDER BY indicator_date DESC LIMIT 1",
                (indi_name,)
            ).fetchone()
            if row:
                signals["L0_macro"][sig_name] = row[0]
        # credit_structure 需要从社融和中长贷计算，暂时跳过
    except Exception as e:
        log(f"L0信号读取异常: {e}", "WARN")
    
    # L1 政策 — 从policy_events读取最新政策影响分
    try:
        row = db.execute(
            "SELECT AVG(sentiment_impact) FROM policy_events WHERE event_date >= date(?, '-5 days')",
            (trade_date,)
        ).fetchone()
        if row and row[0] is not None:
            signals["L1_policy"]["policy_event"] = float(row[0])
            signals["L1_policy"]["capital_market_regulation"] = float(row[0]) * 0.7
            signals["L1_policy"]["regulatory_attitude"] = float(row[0]) * 0.5
    except Exception:
        pass
    
    # L2 机构 — institution_flow 表
    try:
        for sig_name in ["lhb_inst_vs_retail_divergence", "margin_balance_change", 
                         "block_trade_discount", "inst_buyback_repurchase"]:
            row = db.execute(
                "SELECT signal_value FROM institution_flow WHERE signal_name=? ORDER BY available_at DESC LIMIT 1",
                (sig_name,)
            ).fetchone()
            if row:
                signals["L2_institution"][sig_name] = row[0]
    except Exception as e:
        log(f"L2信号读取异常: {e}", "WARN")
    
    # L3 资金 — capital_flow_signals 表（不是 capital_flow）
    try:
        for sig_name in ["northbound_net", "main_capital_net",
                         "etf_net_subscribe", "cds_spread", "volume_ratio"]:
            row = db.execute(
                "SELECT signal_value FROM capital_flow_signals WHERE signal_name=? ORDER BY available_at DESC LIMIT 1",
                (sig_name,)
            ).fetchone()
            if row:
                signals["L3_capital"][sig_name] = row[0]
        # auction_anomaly 暂无数据源，跳过
    except Exception as e:
        log(f"L3信号读取异常: {e}", "WARN")
    
    # L4 情绪 — 从 limit_up_pool 表读取（不是 signal_log）
    try:
        row = db.execute(
            "SELECT limit_up_count, broken_rate, volume_ratio FROM limit_up_pool ORDER BY trade_date DESC LIMIT 1"
        ).fetchone()
        if row:
            if row[0] is not None:
                signals["L4_sentiment"]["limit_up_structure"] = float(row[0])
            if row[1] is not None:
                signals["L4_sentiment"]["broken_rate"] = float(row[1])
            if row[2] is not None:
                signals["L4_sentiment"]["volume_ratio"] = float(row[2])
            # board_rotation 暂无数据源，跳过
    except Exception as e:
        log(f"L4信号读取异常: {e}", "WARN")
    
    # L5 衍生品 — derivatives_data 表
    try:
        row = db.execute(
            "SELECT hs300_pcr_position, hs300_iv_change, basis_if, hs300_skew_25d, "
            "position_anomaly_flag FROM derivatives_data ORDER BY trade_date DESC LIMIT 1"
        ).fetchone()
        if row:
            if row[0] is not None: signals["L5_derivatives"]["pcr_position"] = row[0]
            if row[1] is not None: signals["L5_derivatives"]["iv_change"] = row[1]
            if row[2] is not None: signals["L5_derivatives"]["basis"] = row[2]
            if row[3] is not None: signals["L5_derivatives"]["skew"] = row[3]
            signals["L5_derivatives"]["option_position_anomaly"] = float(row[4] or 0)
    except Exception as e:
        log(f"L5信号读取异常: {e}", "WARN")
    
    return signals

# ============================================================
# 保存评分快照
# ============================================================
def save_snapshot(db, report: dict):
    """存入market_snapshot表"""
    comp = report["composite"]
    cb = report["circuit_breaker"]
    pos = report["position_advice"]
    trade_date = report["trade_date"]
    
    # 从各层提取z_score
    layer_scores = comp.get("layer_scores", {})
    l0_z = layer_scores.get("L0_macro", {}).get("z_score", 0)
    l1_z = layer_scores.get("L1_policy", {}).get("z_score", 0)
    l2_z = layer_scores.get("L2_institution", {}).get("z_score", 0)
    l3_z = layer_scores.get("L3_capital", {}).get("z_score", 0)
    l4_z = layer_scores.get("L4_sentiment", {}).get("z_score", 0)
    l5_z = layer_scores.get("L5_derivatives", {}).get("z_score", 0)
    
    # 20列, 18个? + 2个datetime字面量 = 20个值
    db.execute(
        """
        INSERT OR REPLACE INTO market_snapshot
        (trade_date, available_at,
         l0_macro_score, l1_policy_score, l2_inst_score, l3_capital_score,
         l4_sentiment_score, l5_derivatives_score,
         composite_score, composite_direction, composite_confidence,
         circuit_breaker_level, circuit_breaker_reason,
         temperature_z, velocity_dz, divergence_d,
         position_label, position_range,
         created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','+8 hours'),datetime('now','+8 hours'))
        """,
        (
            trade_date,
            datetime.now().isoformat(),
            l0_z, l1_z, l2_z, l3_z, l4_z, l5_z,
            comp["temperature_z"],
            comp["direction"],
            comp["confidence"],
            cb["level"],
            cb.get("reason", ""),
            comp["temperature_z"],
            comp["velocity_dz"],
            comp["divergence_d"],
            pos.get("label", "中性"),
            json.dumps(pos.get("position_range", [0.5, 0.7])),
        )
    )
    db.commit()

# ============================================================
# 保存信号日志
# ============================================================
def save_signal_log(db, report: dict, trade_date: str):
    """存入signal_log表"""
    comp = report["composite"]
    
    for layer_key, layer_data in comp.get("layer_scores", {}).items():
        signals = layer_data.get("signals", {})
        
        for sig_name, sig_data in signals.items():
            # 置信度：取置信区间宽度的反义——区间越窄置信度越高
            ci = sig_data.get("confidence_interval", (0, 0))
            if isinstance(ci, (list, tuple)) and len(ci) == 2:
                ci_width = abs(ci[1] - ci[0])
                confidence_val = max(0, 1 - ci_width)
            else:
                confidence_val = 0.5
            
            db.execute("""
                INSERT INTO signal_log 
                (trade_date, signal_layer, signal_name, signal_value, 
                 signal_direction, signal_strength, signal_confidence)
                VALUES (?,?,?,?,?,?,?)
            """, (
                trade_date,
                layer_key,
                sig_name,
                sig_data.get("value"),
                sig_data.get("direction"),
                sig_data.get("z_score"),
                confidence_val
            ))
    
    db.commit()

# ============================================================
# 运行告警检查
# ============================================================
def run_alert_check() -> dict:
    """运行告警监控"""
    log("开始告警检查")
    try:
        result = subprocess.run(
            [sys.executable, str(DB_DIR / ALERT_SCRIPT)],
            capture_output=True, text=True, timeout=30, cwd=str(DB_DIR)
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                alerts = data.get("alerts", [])
                if alerts:
                    log(f"发现 {len(alerts)} 条告警")
                    for a in alerts:
                        log(f"  [{a['alert_level']}] {a['signal_name']}: {a['current_value']} (阈值:{a['threshold']})")
                else:
                    log("无告警触发")
                return data
            except json.JSONDecodeError:
                log(f"告警输出解析失败: {result.stdout[:200]}", "WARN")
                return {"status": "parse_error"}
        else:
            log(f"告警脚本执行失败: {result.stderr[:200]}", "ERROR")
            return {"status": "error"}
    except Exception as e:
        log(f"告警检查异常: {e}", "ERROR")
        return {"status": "error", "error": str(e)}

# ============================================================
# 主函数
# ============================================================
def main():
    log("=" * 60)
    log(f"📊 大A舆情预判框架 v2.0 - 日终数据采集")
    log(f"交易日: {datetime.now().strftime('%Y-%m-%d')}")
    log("=" * 60)
    
    trade_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 运行所有采集器
    log(">> 步骤1: 运行6层数据采集器")
    results = {}
    for layer, script, desc, required in COLLECTORS:
        ok = run_collector(layer, script, desc, required)
        results[layer] = ok
    
    # 2. 运行评分引擎
    log(">> 步骤2: 运行评分引擎")
    engine_result = run_engine(trade_date)
    
    # 3. 运行告警检查
    log(">> 步骤3: 运行告警检查")
    alert_result = run_alert_check()
    
    # 4. 汇总
    log("=" * 60)
    log("📊 日终采集汇总")
    log("=" * 60)
    
    for layer, script, desc, _ in COLLECTORS:
        status = "✅" if results.get(layer) else "❌"
        log(f"  {status} {layer} {desc}")
    
    if engine_result.get("status") == "no_data":
        log("  ⚠️ 评分引擎: 无可用数据")
    elif engine_result.get("status") == "error":
        log("  ❌ 评分引擎: 异常")
    else:
        comp = engine_result.get("composite", {})
        log(f"  ✅ 评分引擎: Z={comp.get('temperature_z', 0):+.4f} {comp.get('direction', '')}")
    
    alerts = alert_result.get("alerts", [])
    if alerts:
        log(f"  🚨 告警: {len(alerts)}条")
    else:
        log("  ✅ 告警: 无触发")
    
    log("=" * 60)
    log("日终采集完成")
    log("=" * 60)

if __name__ == "__main__":
    main()
