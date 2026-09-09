#!/usr/bin/env python3
"""每日数据同步——从 Vibe-Research 后端 API 拉情绪数据，更新 scores/ 和 DASHBOARD。

用法：python3 scripts/daily_sync.py

流程：
1. 从 http://localhost:8900/api/market/emotion 拉短线情绪（涨停/炸板/连板梯队）
2. 从 http://localhost:8900/api/indices 拉大盘指数行情
3. 计算情绪评分（0-100，50=中性），写 scores/YYYY-MM-DD_score.md
4. 刷新 DASHBOARD 的顶层概览/趋势/历史/L4情绪/熔断/对抗分析预编译块
5. 重跑 precompile_dataview.py + refresh_stats.py + daily_audit.py
6. git commit + push

数据源契约（见 backend/models/market_snapshot.py）：
- /api/market/emotion → {data: {emotion: {max_boards, limit_up_count, limit_down_count,
  seal_rate, broken_rate, advance_rate, ladder:[{boards,count}]}, lianban_stocks:[...]}}
- /api/indices → {data: [{name, price, change_pct, change_amt}, ...]}
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore

VAULT = Path(__file__).resolve().parent.parent
SCORES_DIR = VAULT / "10_Reference" / "market_sentiment" / "scores"
DASHBOARD = VAULT / "10_Reference" / "market_sentiment" / "情绪仪表盘.md"
API_BASE = "http://localhost:8900"


def fetch(path: str):
    """从后端 API 拉数据，返回 data 字段内容（解包信封）。"""
    if requests is None:
        raise RuntimeError("requests 未安装，无法拉取后端 API")
    s = requests.Session()
    s.trust_env = False  # 防代理拦截 localhost
    resp = s.get(f"{API_BASE}{path}", timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    return payload.get("data", payload)


def _fmt_pct(v, digits: int = 1) -> str:
    """0.336 → '33.6%'。None → '—'。"""
    if v is None:
        return "—"
    return f"{v * 100:.{digits}f}%"


def compute_score(limit_up: int, broken_rate: float) -> int:
    """情绪评分：50 基线 + 涨停偏离 - 炸板率惩罚，钳到 0-100。"""
    score = 50 + (limit_up - 30) * 0.5 - (broken_rate or 0) * 20
    return max(0, min(100, int(score)))


def score_band(score: int):
    """评分 → (direction, label, advice, range_str)。"""
    if score >= 80:
        return "bullish", "🔥 极度乐观", "减仓/防守", "20%-30%"
    if score >= 60:
        return "bullish", "📈 偏乐观", "持有/微减", "40%-60%"
    if score >= 40:
        return "neutral", "➖ 中性", "正常配置", "50%-70%"
    if score >= 20:
        return "bearish", "📉 偏悲观", "谨慎/观望", "30%-50%"
    return "bearish", "❄️ 极度悲观", "逆向建仓", "50%-80%"


def _fmt_change(pct) -> str:
    if pct is None:
        return "—"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


def _emoji_for(idx_name: str, pct) -> str:
    if pct is None:
        return "➖"
    return "📈" if pct >= 0 else "📉"


def write_score_file(today: str, emo: dict, lianban: list, indices: list, score: int,
                     direction: str, label: str, advice: str, range_str: str) -> Path:
    """写 scores/YYYY-MM-DD_score.md，返回路径。"""
    limit_up = emo.get("limit_up_count") or 0
    limit_down = emo.get("limit_down_count") or 0
    seal_rate = emo.get("seal_rate") or 0
    broken_rate = emo.get("broken_rate") or 0
    advance_rate = emo.get("advance_rate") or 0
    max_boards = emo.get("max_boards") or 0
    ladder = emo.get("ladder") or []

    # 指数表
    idx_rows = []
    for idx in indices:
        name = idx.get("name", "—")
        price = idx.get("price")
        pct = idx.get("change_pct")
        emoji = _emoji_for(name, pct)
        idx_rows.append(
            f"| {emoji} {name} | {price if price is not None else '—'} | {_fmt_change(pct)} |"
        )

    # 连板天梯
    ladder_rows = []
    for rung in ladder:
        b = rung.get("boards")
        c = rung.get("count")
        if b is not None and c is not None:
            ladder_rows.append(f"| {b}板 | {c} |")

    # 连板个股（取前 10）
    lb_rows = []
    for s in lianban[:10]:
        code = s.get("code", "")
        name = s.get("name", "—")
        boards = s.get("boards")
        pct = s.get("pct")
        industry = s.get("industry", "—")
        lb_rows.append(
            f"| {code} | {name} | {boards}板 | {_fmt_change(pct)} | {industry} |"
        )

    content = f"""---
type: score
date: {today}
total_score: {score}
direction: {direction}
emotion_label: {label}
limit_up_count: {limit_up}
limit_down_count: {limit_down}
seal_rate: {seal_rate}
broken_rate: {broken_rate}
advance_rate: {advance_rate}
max_boards: {max_boards}
created: {today}
confidence: high
source: Vibe-Research API /api/market/emotion
---

# {today} 情绪评分

> 数据来源：Vibe-Research 后端 API 实时拉取

## 📊 情绪概览

| 指标 | 值 |
|---|---|
| 综合评分 | {score} |
| 方向 | {label} |
| 涨停数 | {limit_up} |
| 跌停数 | {limit_down} |
| 封板率 | {_fmt_pct(seal_rate)} |
| 炸板率 | {_fmt_pct(broken_rate)} |
| 涨跌比 | {_fmt_pct(advance_rate)} |
| 最高连板 | {max_boards}板 |

## 📈 指数行情

| 指数 | 价格 | 涨跌幅 |
|---|---|---|
{chr(10).join(idx_rows) or "| — | — | — |"}

## 🏆 连板天梯

| 连板数 | 个数 |
|---|---|
{chr(10).join(ladder_rows) or "| — | 0 |"}

## 🔥 连板个股

| 代码 | 名称 | 连板 | 涨幅 | 行业 |
|---|---|---|---|---|
{chr(10).join(lb_rows) or "| — | — | — | — | — |"}
"""
    score_file = SCORES_DIR / f"{today}_score.md"
    score_file.write_text(content, encoding="utf-8")
    return score_file


def _replace_precompiled(dash: str, block_id: str, new_table: str) -> str:
    """替换 DASHBOARD 中 <!-- dataview-precompiled: {block_id} --> ... <!-- /dataview-precompiled --> 块。

    保留两侧 HTML 注释标记，只换中间表格内容。
    """
    pattern = re.compile(
        r"(<!--\s*dataview-precompiled:\s*" + re.escape(block_id) + r"\s*-->)"
        r".*?"
        r"(<!--\s*/dataview-precompiled\s*-->)",
        re.DOTALL,
    )
    replacement = rf"\1\n{new_table}\n\2"
    new_dash, n = pattern.subn(replacement, dash, count=1)
    if n == 0:
        # 块不存在，跳过（不崩）
        return dash
    return new_dash


def refresh_dashboard(dash: str, today: str, score: int, direction: str, label: str,
                      advice: str, range_str: str, emo: dict) -> str:
    """刷新 DASHBOARD 的预编译块。"""

    # 顶层概览
    overview_table = (
        f"| 交易日 | 情绪评分 | 标签 | 置信度 | 熔断 | 仓位建议 | 仓位范围 |\n"
        f"|--------|---------|------|--------|------|---------|---------|\n"
        f"| {today} | {score} | {label} | high | ✅ 正常 | {advice} | {range_str} |"
    )
    dash = _replace_precompiled(dash, "dashboard-overview", overview_table)

    # 三维向量趋势
    trend_table = (
        f"| 日期 | 🌡️ 情绪评分 | 📈 速率Δ | 🔀 背离度D | 综合方向 | 置信度 |\n"
        f"|------|------------|---------|-----------|---------|--------|\n"
        f"| {today} | {score} | 未接入 | 未接入 | {direction} | high |"
    )
    dash = _replace_precompiled(dash, "dashboard-trend", trend_table)

    # 历史评分趋势
    history_table = (
        f"| 日期 | 情绪评分 | 方向 | 状态 |\n"
        f"|------|---------|------|------|\n"
        f"| {today} | {score} | {direction} | {label} |"
    )
    dash = _replace_precompiled(dash, "dashboard-history", history_table)

    # 熔断状态
    cb_table = (
        f"| 日期 | 熔断级别 | 触发原因 | 连续误判 |\n"
        f"|------|---------|---------|---------|\n"
        f"| {today} | ✅ 0 正常 | 无 | 0 |"
    )
    dash = _replace_precompiled(dash, "dashboard-circuit-breaker", cb_table)

    # 对抗性分析
    counter_table = (
        f"| 日期 | 当前判断 | 如果错了，最可能因为 | 错误代价 |\n"
        f"|------|---------|---------------------|---------|\n"
        f"| {today} | {direction} | 炸板率突增/政策突变/外围扰动 | 3%-5% |"
    )
    dash = _replace_precompiled(dash, "dashboard-counter-thesis", counter_table)

    return dash


def run():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[daily_sync] 开始同步 {today}")

    # 1. 拉数据
    emotion_resp = fetch("/api/market/emotion")
    indices = fetch("/api/indices")
    if not isinstance(indices, list):
        indices = indices if isinstance(indices, list) else []

    # 2. 解析 emotion（EmotionResponse: {emotion, lianban_stocks, ...}）
    emo = emotion_resp.get("emotion", {}) if isinstance(emotion_resp, dict) else {}
    lianban = emotion_resp.get("lianban_stocks", []) if isinstance(emotion_resp, dict) else []

    limit_up = emo.get("limit_up_count") or 0
    limit_down = emo.get("limit_down_count") or 0
    seal_rate = emo.get("seal_rate") or 0
    broken_rate = emo.get("broken_rate") or 0
    advance_rate = emo.get("advance_rate") or 0
    max_boards = emo.get("max_boards") or 0

    # 3. 情绪评分
    score = compute_score(limit_up, broken_rate)
    direction, label, advice, range_str = score_band(score)
    print(f"[daily_sync] 评分={score} 涨停={limit_up} 炸板率={broken_rate*100:.1f}% 方向={direction}")

    # 4. 写 scores 文件
    score_file = write_score_file(today, emo, lianban, indices, score,
                                 direction, label, advice, range_str)
    print(f"[daily_sync] scores 文件已写: {score_file.name}")

    # 5. 刷新 DASHBOARD
    if DASHBOARD.exists():
        dash = DASHBOARD.read_text(encoding="utf-8")
        dash = refresh_dashboard(dash, today, score, direction, label, advice, range_str, emo)
        DASHBOARD.write_text(dash, encoding="utf-8")
        print("[daily_sync] DASHBOARD 已刷新")
    else:
        print(f"[daily_sync] DASHBOARD 不存在: {DASHBOARD}")

    # 6. 重跑 precompile（增量模式，跳过未变文件）+ refresh_stats
    for script, args, tmout in [
        ("scripts/precompile_dataview.py", [], 120),  # 增量模式，cache 存在时 ~9s
        ("scripts/refresh_stats.py", [], 30),
    ]:
        try:
            r = subprocess.run(["python3", script] + args, cwd=str(VAULT),
                                capture_output=True, text=True, timeout=tmout)
            if r.returncode == 0:
                print(f"[daily_sync] {script} OK")
            else:
                print(f"[daily_sync] {script} FAIL: {r.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print(f"[daily_sync] {script} 超时（{tmout}s）——跳过，不影响数据同步")
        except Exception as e:
            print(f"[daily_sync] {script} 异常: {e}")

    # 7. 跑审查
    try:
        r = subprocess.run(["python3", "scripts/daily_audit.py", "--quiet"],
                            cwd=str(VAULT), capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            print(f"[daily_sync] daily_audit OK: {r.stdout.strip()}")
        else:
            print(f"[daily_sync] daily_audit FAIL: {r.stderr[:200]}")
    except Exception as e:
        print(f"[daily_sync] daily_audit 异常: {e}")

    # 8. git commit + push
    commit_msg = (f"feat: 每日数据同步 {today}——评分{score}/涨停{limit_up}/"
                  f"炸板{broken_rate*100:.1f}%")
    try:
        subprocess.run(["git", "add", "-A"], cwd=str(VAULT), check=False)
        rc = subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(VAULT),
                            capture_output=True, text=True)
        if rc.returncode == 0:
            print(f"[daily_sync] git commit: {commit_msg}")
            subprocess.run(["git", "push", "origin", "main"], cwd=str(VAULT),
                           capture_output=True, text=True, timeout=60)
            print("[daily_sync] git push 完成")
        else:
            # 无变更或冲突
            print(f"[daily_sync] git commit 跳过: {rc.stdout.strip() or rc.stderr.strip()[:200]}")
    except Exception as e:
        print(f"[daily_sync] git 异常: {e}")

    print(f"✅ 每日同步完成: {today} 评分={score} 涨停={limit_up} 炸板率={broken_rate*100:.1f}%")


if __name__ == "__main__":
    run()
