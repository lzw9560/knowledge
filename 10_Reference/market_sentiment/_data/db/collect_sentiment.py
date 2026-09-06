#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - L4市场情绪层数据采集脚本
使用 hithink-finance CLI 采集涨停池/炸板/连板天梯等数据

hithink-finance CLI 输出格式：
{"ok":true,"command":"...","data":{"item":[...]}} 或 {"ok":true,"data":{"stock_items":[...]}}
本脚本负责解包并提取关键数据存入SQLite
"""

import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "sentiment.db"


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
            print(f"  ⚠️ API返回错误: {raw.get('error', {}).get('message', '')[:100]}")
            return None
        return raw.get("data", {})
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ 超时")
        return None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  ❌ {e}")
        return None


class SentimentDataCollector:
    def __init__(self, db_path: Path = DB_PATH):
        self.db = sqlite3.connect(str(db_path))
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.available_at = datetime.now().isoformat()

    def collect_limit_up_pool(self):
        """采集涨停池数据"""
        print("\n📌 采集涨停池数据...")
        data = run_hithink(["special", "limit-up-pool"])
        if not data:
            print("  ⚠️ 无数据（可能非交易日）")
            return None

        items = data.get("item", [])
        total = len(items)
        if total == 0:
            print("  ⚠️ 涨停池为空")
            return None

        first_board = 0
        second_board = 0
        third_plus = 0
        one_word = 0
        turnover_board = 0
        max_consecutive = 0

        for stock in items:
            consecutive = stock.get("continue_day_cnt", 1)
            if consecutive == 1:
                first_board += 1
            elif consecutive == 2:
                second_board += 1
            else:
                third_plus += 1

            if consecutive > max_consecutive:
                max_consecutive = consecutive

            # 一字板判断：开盘=收盘=最高=最低
            last_price = stock.get("last_price", 0)
            # 无法直接判断一字板，用 limit_up_time == 09:25 近似
            if stock.get("limit_up_time", "") == "09:25":
                one_word += 1
            else:
                turnover_board += 1

        print(f"  涨停数: {total} (首板:{first_board} 二板:{second_board} 三板+:{third_plus})")
        print(f"  最高连板: {max_consecutive}板 | 一字板: {one_word} 换手板: {turnover_board}")

        # 打印连板天梯
        ladder = {}
        for stock in items:
            cnt = stock.get("continue_day_cnt", 1)
            ladder[cnt] = ladder.get(cnt, 0) + 1
        ladder_str = " → ".join(f"{k}板:{v}只" for k, v in sorted(ladder.items()))
        print(f"  连板天梯: {ladder_str}")

        return {
            "limit_up_count": total,
            "first_board": first_board,
            "second_board": second_board,
            "third_plus": third_plus,
            "one_word": one_word,
            "turnover_board": turnover_board,
            "max_consecutive": max_consecutive,
            "ladder": ladder,
        }

    def collect_hot_stocks(self):
        """采集热榜数据"""
        print("\n📌 采集热榜数据...")
        data = run_hithink(["special", "hot-stock"])
        if not data:
            print("  ⚠️ 无数据")
            return []

        items = data.get("item", [])
        print(f"  热榜股票数: {len(items)}")
        for i, stock in enumerate(items[:5]):
            name = stock.get("name", "")
            code = stock.get("thscode", "")
            heat = stock.get("heat", 0)
            rank = stock.get("rank", i+1)
            print(f"    {rank}. {name}({code}) 热度:{heat}")
        return items

    def collect_dragon_tiger(self):
        """采集龙虎榜数据"""
        print("\n📌 采集龙虎榜数据...")
        data = run_hithink(["special", "dragon-tiger"])
        if not data:
            print("  ⚠️ 无数据")
            return []

        stock_items = data.get("stock_items", [])
        trade_date = data.get("trade_date", "")
        print(f"  龙虎榜日期: {trade_date}")
        print(f"  龙虎榜记录数: {len(stock_items)}")

        # 分析机构 vs 游资
        inst_net_total = 0
        hot_money_net_total = 0
        for record in stock_items:
            org_net = record.get("org_net_value", 0) or 0
            hot_net = record.get("hot_money_net_value", 0) or 0
            inst_net_total += org_net
            hot_money_net_total += hot_net

        print(f"  机构净买入: {inst_net_total/1e8:.2f}亿")
        print(f"  游资净买入: {hot_money_net_total/1e8:.2f}亿")
        total = abs(inst_net_total) + abs(hot_money_net_total)
        if total > 0:
            divergence = abs(inst_net_total - hot_money_net_total) / total
            print(f"  机构vs游资分歧度: {divergence:.2%}")

        # 打印Top5
        print(f"  Top5龙虎榜个股:")
        for i, stock in enumerate(stock_items[:5]):
            name = stock.get("name", "")
            code = stock.get("thscode", "")
            net = stock.get("net_value", 0) or 0
            change = stock.get("change", 0) or 0
            print(f"    {i+1}. {name}({code}) 净额:{net/1e8:.2f}亿 涨跌:{change*100:.2f}%")

        return stock_items

    def collect_market_snapshot(self):
        """采集市场快照"""
        print("\n📌 采集市场快照...")
        # 用 --thscodes (复数)
        data = run_hithink(["market", "snapshot", "--thscodes", "000001.SH"])
        if not data:
            print("  ⚠️ 无数据")
            return

        # 数据可能是 dict 或 list
        if isinstance(data, dict):
            items = data.get("item", [data]) if "item" in data else [data]
        elif isinstance(data, list):
            items = data
        else:
            items = []

        for idx in items:
            name = idx.get("name", "")
            code = idx.get("thscode", idx.get("ts_code", ""))
            close = idx.get("last_price", idx.get("close", 0))
            pct = idx.get("price_change_ratio_pct", idx.get("pct_chg", 0))
            print(f"  {name}({code}): {close} ({pct:+.2f}%)")

    def store_limit_up_data(self, limit_up_data: dict):
        """存入涨停池数据"""
        if not limit_up_data:
            return

        try:
            ladder_json = json.dumps(limit_up_data.get("ladder", {}))
            
            # 计算炸板率
            broken_count = limit_up_data.get("broken_count")
            limit_up_count = limit_up_data.get("limit_up_count", 0)
            broken_rate = None
            if broken_count is not None and limit_up_count > 0:
                broken_rate = broken_count / (limit_up_count + broken_count)
            
            # 计算连板晋级率
            ladder = limit_up_data.get("ladder", {})
            two_count = ladder.get(2, 0)
            three_count = ladder.get(3, 0)
            two_to_three = (three_count / two_count) if two_count > 0 else None
            four_count = ladder.get(4, 0)
            three_to_four = (four_count / three_count) if three_count > 0 else None
            
            self.db.execute("""
                INSERT OR REPLACE INTO limit_up_pool
                (trade_date, available_at, limit_up_count, limit_up_first_board,
                 limit_up_second_board, limit_up_third_plus,
                 limit_up_one_word, limit_up_turnover_board,
                 max_consecutive_boards, consecutive_ladder,
                 broken_limit_count, broken_rate,
                 two_to_three_success_rate, three_to_four_success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.today, self.available_at,
                limit_up_data.get("limit_up_count", 0),
                limit_up_data.get("first_board", 0),
                limit_up_data.get("second_board", 0),
                limit_up_data.get("third_plus", 0),
                limit_up_data.get("one_word", 0),
                limit_up_data.get("turnover_board", 0),
                limit_up_data.get("max_consecutive", 0),
                ladder_json,
                broken_count,
                broken_rate,
                two_to_three,
                three_to_four
            ))
            self.db.commit()
            print(f"\n  ✅ 涨停池数据已存入数据库")
            if broken_rate is not None:
                print(f"  炸板率: {broken_rate:.1%}")
            if two_to_three is not None:
                print(f"  二进三成功率: {two_to_three:.1%}")
        except Exception as e:
            print(f"\n  ❌ 存储失败: {e}")

    def collect_all(self):
        """采集全部L4情绪数据"""
        print("=" * 50)
        print("📊 L4市场情绪层数据采集")
        print(f"日期: {self.today}")
        print(f"时间: {self.available_at}")
        print("=" * 50)

        limit_up = self.collect_limit_up_pool()
        hot_stocks = self.collect_hot_stocks()
        dragon_tiger = self.collect_dragon_tiger()
        self.collect_market_snapshot()

        if limit_up:
            self.store_limit_up_data(limit_up)

        print(f"\n{'=' * 50}")
        print(f"✅ L4情绪数据采集完成")

        # 数据库预览
        print(f"\n📋 数据库最新记录:")
        row = self.db.execute("""
            SELECT trade_date, limit_up_count, limit_up_first_board,
                   limit_up_second_board, limit_up_third_plus,
                   max_consecutive_boards, consecutive_ladder
            FROM limit_up_pool ORDER BY trade_date DESC LIMIT 1
        """).fetchone()
        if row:
            print(f"  日期: {row[0]}")
            print(f"  涨停: {row[1]} (首板:{row[2]} 二板:{row[3]} 三板+:{row[4]})")
            print(f"  最高连板: {row[5]}板")
            if row[6]:
                ladder = json.loads(row[6])
                ladder_str = " → ".join(f"{k}板:{v}只" for k, v in sorted(ladder.items(), key=lambda x: int(x[0])))
                print(f"  连板天梯: {ladder_str}")

        self.db.close()

    def close(self):
        self.db.close()


if __name__ == "__main__":
    collector = SentimentDataCollector()
    collector.collect_all()
