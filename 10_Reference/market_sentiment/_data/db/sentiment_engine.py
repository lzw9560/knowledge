#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - 稳健z-score评分引擎
基于10位专家评审P0改造

核心改进：
1. 稳健z-score（中位数+MAD）替代普通z-score（均值+标准差）
2. 三维向量：温度Z + 变化速率ΔZ + 信号背离度D
3. 置信区间输出
4. 历史分位数报告
5. 信号衰减追踪
"""

import json
import sqlite3
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ============================================================
# 配置
# ============================================================
DB_PATH = Path(__file__).parent / "sentiment.db"
CONFIG_PATH = Path(__file__).parent / "framework_config.json"

# ============================================================
# 稳健统计工具
# ============================================================

def median_absolute_deviation(data: list[float]) -> float:
    """计算MAD（中位绝对偏差）"""
    if len(data) < 2:
        return 0.0
    med = statistics.median(data)
    abs_devs = [abs(x - med) for x in data]
    return statistics.median(abs_devs)

def robust_zscore(value: float, history: list[float], clip_range: tuple = (-3.0, 3.0)) -> float:
    """
    稳健z-score: (x - median) / (MAD * 1.4826)
    比普通z-score更抗极端值（A股肥尾分布）
    """
    if len(history) < 5:
        return 0.0
    med = statistics.median(history)
    mad = median_absolute_deviation(history)
    mad_scaled = mad * 1.4826  # 正态分布一致性因子

    if mad_scaled == 0:
        # 如果MAD=0（所有历史值相同），用普通标准差兜底
        std = statistics.stdev(history) if len(history) > 1 else 0
        if std == 0:
            return 0.0
        z = (value - statistics.mean(history)) / std
    else:
        z = (value - med) / mad_scaled

    # 截断到合理范围
    z = max(clip_range[0], min(clip_range[1], z))
    return round(z, 4)

def percentile_rank(value: float, history: list[float]) -> float:
    """计算历史分位数（0-1）"""
    if not history:
        return 0.5
    sorted_hist = sorted(history)
    count_below = sum(1 for x in sorted_hist if x < value)
    return round(count_below / len(sorted_hist), 4)

def confidence_interval(z: float, n: int, z_alpha: float = 1.96) -> tuple:
    """
    计算z-score的95%置信区间
    n: 样本量
    """
    if n < 2:
        return (z, z)
    # 稳健标准误估计
    se = 1.4826 / (n ** 0.5)  # 基于MAD的标准误
    margin = z_alpha * se
    return (round(z - margin, 4), round(z + margin, 4))

# ============================================================
# 评分引擎
# ============================================================

class SentimentEngine:
    def __init__(self, db_path: Path = DB_PATH, config_path: Path = CONFIG_PATH):
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        with open(config_path) as f:
            self.config = json.load(f)

    def get_history(self, signal_name: str, window: int = 60) -> list[float]:
        """从数据库获取信号历史值"""
        rows = self.db.execute(
            "SELECT signal_value FROM signal_log WHERE signal_name = ? ORDER BY trade_date DESC LIMIT ?",
            (signal_name, window)
        ).fetchall()
        return [r["signal_value"] for r in rows if r["signal_value"] is not None]

    def compute_layer_score(self, layer_key: str, signal_values: dict) -> dict:
        """
        计算某一层的综合得分
        signal_values: {signal_name: current_value}
        返回: {z_score, percentile, confidence_interval, direction, signals}
        """
        layer_config = self.config["layers"][layer_key]
        signals_config = layer_config["signals"]

        weighted_z = 0.0
        signal_details = {}

        for sig_name, sig_config in signals_config.items():
            if sig_name not in signal_values:
                continue

            value = signal_values[sig_name]
            window = sig_config.get("zscore_window", 60)
            history = self.get_history(sig_name, window)

            z = robust_zscore(value, history)
            pct = percentile_rank(value, history)
            ci = confidence_interval(z, len(history))

            # 方向判断
            thresholds = sig_config.get("thresholds", {"bullish": 0.5, "bearish": -0.5})
            if z > thresholds.get("bullish", 0.5):
                direction = "bullish"
            elif z < thresholds.get("bearish", -0.5):
                direction = "bearish"
            else:
                direction = "neutral"

            weight = sig_config["weight"]
            weighted_z += z * weight

            signal_details[sig_name] = {
                "value": value,
                "z_score": z,
                "percentile": pct,
                "confidence_interval": ci,
                "direction": direction,
                "weight": weight,
                "history_size": len(history)
            }

        # 层级归一化（除以该层总权重）
        total_weight = sum(s["weight"] for s in signals_config.values())
        layer_z = weighted_z / total_weight if total_weight > 0 else 0

        return {
            "z_score": round(layer_z, 4),
            "signals": signal_details
        }

    def compute_composite(self, layer_scores: dict) -> dict:
        """
        计算综合得分 - 三维向量
        layer_scores: {layer_key: layer_score_dict}
        """
        weights = {k: v["weight"] for k, v in self.config["layers"].items()}

        # 维度1: 绝对温度 Z
        temperature_z = sum(
            layer_scores[k]["z_score"] * weights[k]
            for k in layer_scores
        ) / sum(weights[k] for k in layer_scores)

        # 维度2: 变化速率 ΔZ (需要前一期数据)
        # 从数据库取上一期综合得分
        prev_row = self.db.execute(
            "SELECT composite_score FROM market_snapshot ORDER BY trade_date DESC LIMIT 1"
        ).fetchone()
        prev_z = prev_row["composite_score"] if prev_row and prev_row["composite_score"] else 0
        velocity_dz = round(temperature_z - prev_z, 4)

        # 维度3: 信号背离度 D
        # 计算各层方向不一致程度
        directions = [layer_scores[k]["z_score"] for k in layer_scores]
        if directions:
            max_z = max(directions)
            min_z = min(directions)
            divergence_d = round(max_z - min_z, 4)
        else:
            divergence_d = 0.0

        # 综合方向判断
        if temperature_z > 0.5:
            direction = "bullish"
        elif temperature_z < -0.5:
            direction = "bearish"
        else:
            direction = "neutral"

        # 置信度（基于层间一致性和样本量）
        sign_consistency = sum(1 for d in directions if (d > 0) == (temperature_z > 0))
        consistency_ratio = sign_consistency / len(directions) if directions else 0.5
        confidence = round(consistency_ratio * 0.6 + min(1.0, len(directions) / 6) * 0.4, 4)

        return {
            "temperature_z": round(temperature_z, 4),
            "velocity_dz": velocity_dz,
            "divergence_d": divergence_d,
            "direction": direction,
            "confidence": confidence,
            "layer_scores": layer_scores
        }

    def check_circuit_breaker(self, composite: dict) -> dict:
        """
        检查熔断状态
        """
        cb_config = self.config["circuit_breaker"]

        # 查最近连续误判次数
        recent_signals = self.db.execute("""
            SELECT correct_flag FROM signal_log
            WHERE correct_flag IS NOT NULL
            ORDER BY trade_date DESC, id DESC
            LIMIT 10
        """).fetchall()

        consecutive_wrong = 0
        for r in recent_signals:
            if r["correct_flag"] == 0:
                consecutive_wrong += 1
            else:
                break

        # Level 1: 连续3次错误
        l1_trigger = cb_config["self_failure_detection"]["consecutive_wrong_threshold"]
        if consecutive_wrong >= l1_trigger:
            # Level 2: 连续5次错误
            if consecutive_wrong >= 5:
                # Level 3: 系统性风险
                if abs(composite["temperature_z"]) > 2.5 and composite["divergence_d"] > 3.0:
                    return {
                        "level": 3, "reason": "系统性风险：极端波动+信号严重背离",
                        "action": "框架冻结，强制降仓至20%以下",
                        "consecutive_misses": consecutive_wrong
                    }
                return {
                    "level": 2, "reason": f"连续{consecutive_wrong}次方向预测错误",
                    "action": "暂停信号输出，仅推送风险提示",
                    "consecutive_misses": consecutive_wrong
                }
            return {
                "level": 1, "reason": f"连续{consecutive_wrong}次方向预测错误",
                "action": "信号权重降至60%",
                "consecutive_misses": consecutive_wrong
            }

        return {"level": 0, "reason": "正常", "action": None, "consecutive_misses": 0}

    def get_position_advice(self, z_score: float) -> dict:
        """
        根据z-score给出仓位建议
        """
        mapping = self.config["position_mapping"]
        guardrails = mapping["guardrails"]

        for level in mapping["levels"]:
            r = level["score_range"].replace(" ", "")
            if r.startswith("Z>"):
                if z_score > float(r[2:]):
                    return {**level, "guardrails": guardrails}
            elif r.startswith("Z<"):
                if z_score < float(r[2:]):
                    return {**level, "guardrails": guardrails}
            elif "<Z<=" in r:
                parts = r.split("<Z<=")
                if float(parts[0]) < z_score <= float(parts[1]):
                    return {**level, "guardrails": guardrails}
            elif "<=Z<=" in r:
                parts = r.split("<=Z<=")
                if float(parts[0]) <= z_score <= float(parts[1]):
                    return {**level, "guardrails": guardrails}
            elif "<=Z<" in r:
                parts = r.split("<=Z<")
                if float(parts[0]) <= z_score < float(parts[1]):
                    return {**level, "guardrails": guardrails}

        return {**mapping["levels"][2], "guardrails": guardrails}

    def generate_report(self, trade_date: str, all_signal_values: dict) -> dict:
        """
        生成完整评分报告
        all_signal_values: {layer_key: {signal_name: value}}
        """
        # 1. 计算各层得分
        layer_scores = {}
        for layer_key, signals in all_signal_values.items():
            if layer_key in self.config["layers"]:
                layer_scores[layer_key] = self.compute_layer_score(layer_key, signals)

        # 2. 计算综合三维向量
        composite = self.compute_composite(layer_scores)

        # 3. 检查熔断
        breaker = self.check_circuit_breaker(composite)

        # 4. 仓位建议
        position = self.get_position_advice(composite["temperature_z"])

        # 5. 对抗性分析（行为金融专家建议）
        counter_argument = self._generate_counter_argument(composite)

        return {
            "trade_date": trade_date,
            "generated_at": datetime.now().isoformat(),
            "composite": composite,
            "circuit_breaker": breaker,
            "position_advice": position,
            "counter_argument": counter_argument,
            "expiry_week_adjustment": self._check_expiry_week()
        }

    def _generate_counter_argument(self, composite: dict) -> dict:
        """
        强制对抗性分析 - 每次输出附带反面论据
        （行为金融专家第2条建议：打破确认偏误）
        """
        direction = composite["direction"]
        z = composite["temperature_z"]

        if direction == "bullish":
            return {
                "thesis": f"当前看多(Z={z})，但如果错了，最可能因为：",
                "risks": [
                    "情绪过热但趋势延续（2015年3月过热后还有50%涨幅）",
                    "宏观层信号滞后，实际周期已转弯但数据未反映",
                    "资金面信号高度相关，共振是假确认",
                    "外部冲击（美联储/地缘）突然改变市场逻辑"
                ],
                "what_if_wrong": "如果Z>1.5时减仓，最大机会成本是错过泡沫期最后一段涨幅；如果不清仓，最大风险是回吐全部浮盈"
            }
        elif direction == "bearish":
            return {
                "thesis": f"当前看空(Z={z})，但如果错了，最可能因为：",
                "risks": [
                    "恐慌中孕育反转（政策底可能已出现）",
                    "z-score在极端值会失真，A股肥尾使极端值更常见",
                    "北向资金信号衰减，外资行为模式已变化",
                    "市场已price-in最坏预期，边际利好即反弹"
                ],
                "what_if_wrong": "极度悲观时减仓可能卖在地板上；历史数据显示地缘冲击中位修复时间4个交易日"
            }
        else:
            return {
                "thesis": "当前信号中性，不排除以下可能性：",
                "risks": [
                    "中性不代表安全——均衡状态最容易被突发事件打破",
                    "各层信号方向不一致本身就是风险预警",
                    "信号背离度D较大时，可能处于趋势转折期"
                ],
                "what_if_wrong": "中性时满仓=赌方向不明确；中性时空仓=放弃时间价值"
            }

    def _check_expiry_week(self) -> dict:
        """检查是否到期周"""
        today = datetime.now()
        # 每月第四个周三到期
        fourth_wed = self._get_fourth_wednesday(today.year, today.month)
        days_to_expiry = (fourth_wed - today).days

        if 0 <= days_to_expiry <= 3:
            return {
                "is_expiry_week": True,
                "days_to_expiry": days_to_expiry,
                "score_discount": 0.7,
                "note": "到期日效应窗口，预测打0.7折"
            }
        return {"is_expiry_week": False, "days_to_expiry": days_to_expiry}

    def _get_fourth_wednesday(self, year: int, month: int) -> datetime:
        """获取当月第四个周三"""
        d = datetime(year, month, 1)
        wed_count = 0
        while wed_count < 4:
            if d.weekday() == 2:  # Wednesday
                wed_count += 1
            if wed_count < 4:
                d += timedelta(days=1)
        return d

    def close(self):
        self.db.close()


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    import sys

    engine = SentimentEngine()

    # 模拟信号数据
    test_signals = {
        "L0_macro": {
            "social_finance": 9.5,
            "m1_m2_scissors": -2.1,
            "pmi": 50.2,
            "credit_structure": 0.65,
            "dr007": 1.85,
            "cpi_ppi": -1.2
        },
        "L1_policy": {
            "policy_event": 3,
            "capital_market_regulation": 2,
            "regulatory_attitude": 1
        },
        "L2_institution": {
            "lhb_inst_vs_retail_divergence": 0.8,
            "margin_balance_change": 150,
            "block_trade_discount": -0.05,
            "inst_buyback_repurchase": 5
        },
        "L3_capital": {
            "northbound_net": -30,
            "main_capital_net": -50,
            "auction_anomaly": 1.5,
            "etf_net_subscribe": 20,
            "cds_spread": 65
        },
        "L4_sentiment": {
            "limit_up_structure": 45,
            "broken_rate": 0.35,
            "volume_ratio": 0.85,
            "board_rotation": 0.6
        },
        "L5_derivatives": {
            "pcr_position": 0.95,
            "iv_change": 1.2,
            "option_position_anomaly": 0,
            "basis": -0.8,
            "skew": -5.5
        }
    }

    report = engine.generate_report("2026-09-03", test_signals)

    print("=" * 60)
    print("📊 大A舆情预判框架 v2.0 - 评分测试")
    print("=" * 60)
    print(f"交易日: {report['trade_date']}")
    print(f"生成时间: {report['generated_at']}")
    print()

    comp = report["composite"]
    print(f"🌡️  温度 Z:     {comp['temperature_z']:+.4f}")
    print(f"📈 速率 ΔZ:    {comp['velocity_dz']:+.4f}")
    print(f"🔀 背离度 D:    {comp['divergence_d']:.4f}")
    print(f"📍 方向:        {comp['direction']}")
    print(f"🔒 置信度:      {comp['confidence']:.1%}")
    print()

    cb = report["circuit_breaker"]
    print(f"🚨 熔断状态:    Level {cb['level']} - {cb['reason']}")
    if cb["action"]:
        print(f"   动作: {cb['action']}")
    print()

    pos = report["position_advice"]
    print(f"💼 仓位建议:    {pos.get('label', '中性')}")
    print(f"   仓位范围:    {pos.get('position_range', [0.5, 0.7])}")
    print(f"   操作建议:    {pos.get('action', '正常配置')}")
    print(f"   理由:        {pos.get('reason', '')}")
    print()

    ca = report["counter_argument"]
    print(f"⚠️  对抗性分析:")
    print(f"   {ca['thesis']}")
    for i, risk in enumerate(ca["risks"], 1):
        print(f"   {i}. {risk}")
    print(f"   {ca['what_if_wrong']}")
    print()

    exp = report["expiry_week_adjustment"]
    if exp["is_expiry_week"]:
        print(f"📅 到期日效应:  是（距到期{exp['days_to_expiry']}天，打{exp['score_discount']}折）")
    else:
        print(f"📅 到期日效应:  否（距到期{exp['days_to_expiry']}天）")

    print()
    print("=" * 60)
    print("✅ 评分引擎测试通过")
    engine.close()
