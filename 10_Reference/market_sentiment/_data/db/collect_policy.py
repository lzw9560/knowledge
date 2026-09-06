#!/usr/bin/env python3
"""
大A舆情预判框架 v2.0 - L1政策与监管层数据采集脚本
采集央行操作、监管政策、资本市场改革事件

数据源：
1. 东方财富央行公开市场操作API（逆回购/MLF/SLF）
2. web_search 搜索监管政策/资本市场改革新闻
3. 关键词规则引擎对政策事件评分(-5~+5)

依赖：python3标准库（urllib/json/sqlite3）
web_search通过本脚本的子进程方式不可用，本脚本被设计为由agent调用
agent在调用本脚本前应先通过web_search获取数据并写入临时json文件
或直接在agent层面把搜索结果传入

本脚本也支持独立运行：尝试东方财富API，失败则用本地硬编码的近期政策事件
"""

import json
import re
import sqlite3
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "sentiment.db"
EASTMONEY_API = "https://datacenter-web.eastmoney.com/api/data/v1/get"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/",
}

# ============================================================
# 关键词评分规则
# 格式: (关键词列表, 分数, policy_type)
# ============================================================
SCORING_RULES = [
    # 强利好 (+3 ~ +5)
    (["降准", "全面降准", "定向降准"], 5, "monetary_easing"),
    (["降息", "下调利率", "降低MLF利率", "降低LPR", "LPR下调"], 4, "rate_cut"),
    (["减税降费", "减税", "税收优惠", "减免税费"], 4, "fiscal_stimulus"),
    (["逆回购放量", "加大投放", "净投放", "买断式逆回购"], 2, "liquidity_injection"),
    (["支持", "鼓励", "促进", "扶持"], 3, "policy_support"),
    (["稳增长", "逆周期调节", "扩大内需"], 3, "pro_growth"),
    (["注册制改革", "全面注册制"], 2, "market_reform"),
    (["退市制度", "退市完善", "常态化退市"], 2, "market_reform"),
    (["引入长期资金", "中长期资金入市"], 3, "capital_introduction"),
    (["提高融资融券", "扩大融资标的", "降低融资保证金"], 2, "margin_relaxation"),
    (["增持回购", "鼓励回购", "股东增持"], 2, "buyback_support"),
    (["暂停新增转融券", "限制融券", "收紧融券"], 2, "short_restriction"),
    # 利空 (-2 ~ -4)
    (["严监管", "从严监管", "加强监管"], -3, "regulatory_tightening"),
    (["处罚", "行政处罚", "立案调查", "开出罚单"], -3, "enforcement"),
    (["限制", "限制减持", "规范减持"], -2, "restriction"),
    (["收紧", "收紧杠杆", "去杠杆"], -3, "leverage_control"),
    (["房地产调控", "楼市调控", "限购升级"], -2, "property_control"),
    (["IPO加速", "加快发行", "扩大IPO"], -2, "supply_pressure"),
    (["大额减持", "大规模解禁", "巨量解禁"], -3, "selling_pressure"),
    (["收紧流动性", "净回笼", "回笼资金"], -2, "liquidity_drain"),
    (["加息", "上调利率", "LPR上调"], -4, "monetary_tightening"),
    (["提高印花税", "印花税上调"], -5, "tax_hike"),
    # 中性/混合
    (["再融资新规", "定增新规", "再融资规则"], 1, "refinancing_rule"),
    (["分红新规", "强制分红"], 1, "dividend_policy"),
    (["衍生品交易监督管理", "衍生品监管"], -1, "derivatives_regulation"),
    (["分类监管", "分类评价"], -1, "broker_regulation"),
    (["房地产发展新模式", "资本市场支持"], 1, "property_reform"),
    (["非法跨境", "整治非法"], -2, "cross_border_enforcement"),
    (["合格境外投资者", "QFII", "RQFII"], 2, "qfii_reform"),
    (["央行国债期货", "人民币国债期货在港"], 1, "internationalization"),
    (["保险资金权益投资比例上限", "保险资金入市"], 3, "insurance_capital"),
    (["汇金加仓", "中央汇金"], 3, "sovereign_fund"),
    (["健全金融机构治理"], -1, "financial_governance"),
    (["证券公司分类", "券商分类评价"], -1, "broker_regulation"),
]


def score_event(title: str, description: str = "") -> tuple[int, str]:
    """基于关键词规则对政策事件评分
    返回 (sentiment_impact, policy_type)
    """
    text = (title + " " + description)

    best_score = 0
    best_type = "other"
    scores_found = []

    for keywords, score, ptype in SCORING_RULES:
        for kw in keywords:
            if kw in text:
                scores_found.append((kw, score, ptype))
                break  # 每个规则只匹配一次

    if scores_found:
        # 取所有匹配中绝对值最大的
        best_match = max(scores_found, key=lambda x: abs(x[1]))
        best_score = best_match[1]
        best_type = best_match[2]
        # 如果有利好和利空同时匹配，加权
        positive = sum(s for _, s, _ in scores_found if s > 0)
        negative = sum(abs(s) for _, s, _ in scores_found if s < 0)
        if positive and negative:
            # 互相抵消，取差值
            net = positive - negative
            best_score = max(net, -abs(net))  # 保留符号
            best_score = max(best_score, key=abs) if abs(best_score) > abs(net) else net

    return best_score, best_type


def extract_sectors(text: str) -> str:
    """从文本中提取受影响板块"""
    sectors = []
    sector_keywords = {
        "银行": ["银行", "信贷"],
        "券商": ["券商", "证券"],
        "房地产": ["房地产", "楼市", "住房"],
        "科技": ["科技", "半导体", "芯片", "AI", "人工智能", "数字经济"],
        "新能源": ["新能源", "光伏", "储能", "锂电"],
        "消费": ["消费", "零售", "白酒", "食品"],
        "医药": ["医药", "医疗", "药品"],
        "军工": ["军工", "国防"],
        "周期": ["钢铁", "煤炭", "有色", "化工"],
        "汽车": ["汽车", "新能源车"],
    }
    for sector, keywords in sector_keywords.items():
        for kw in keywords:
            if kw in text:
                if sector not in sectors:
                    sectors.append(sector)
                break
    return ",".join(sectors) if sectors else "全市场"


def fetch_eastmoney_api(report_name: str, filters: str = "", page_size: int = 30) -> list[dict]:
    """通用东方财富API请求"""
    params = {
        "reportName": report_name,
        "columns": "ALL",
        "pageSize": str(page_size),
        "pageNumber": "1",
    }
    if filters:
        params["filter"] = filters

    url = EASTMONEY_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("result") and data["result"].get("data"):
            return data["result"]["data"]
    except Exception as e:
        print(f"  ⚠️ API请求失败: {e}")
    return []


def collect_pboc_operations() -> list[dict]:
    """采集央行公开市场操作（逆回购/MLF/SLF/LPR）
    东方财富的央行操作API可能不可用，尝试多个已知reportName
    """
    print("\n📌 采集央行公开市场操作...")
    events = []

    # 尝试多个可能的reportName
    report_names = [
        "RPT_RPT_FREE_REPO_OPRLIST",
        "RPT_CENTRALBANK_OPENMARKET",
        "RPT_RPT_FREE_LPR",
        "RPT_ECONOMY_LPR",
    ]
    rows = []
    for rn in report_names:
        rows = fetch_eastmoney_api(rn, page_size=30)
        if rows:
            print(f"  ✅ 使用reportName: {rn}, 获取{len(rows)}条")
            break

    if rows:
        for row in rows[:10]:
            op_date = row.get("OPERATION_DATE", row.get("REPORT_DATE", "")).split(" ")[0]
            if not op_date:
                continue
            operation = row.get("OPERATION_TYPE", row.get("OPERATION_NAME", ""))
            amount = row.get("OPERATION_AMOUNT", row.get("AMOUNT", 0))
            rate = row.get("RATE", row.get("INTEREST_RATE", 0))

            title = f"央行{operation}操作 {amount}亿元"
            if rate:
                title += f" 利率{rate}%"

            desc = f"操作类型:{operation} 金额:{amount}亿 利率:{rate}%"
            score, ptype = score_event(title, desc)

            if "投放" in operation or "逆回购" in operation:
                if amount and float(amount) > 0:
                    score = max(score, 2)
                    ptype = "liquidity_injection"
            elif "回笼" in operation:
                score = min(score, -2)
                ptype = "liquidity_drain"

            events.append({
                "event_date": op_date,
                "event_title": title,
                "event_source": "东方财富-央行公开市场操作",
                "policy_type": ptype,
                "sentiment_impact": score,
                "affected_sectors": "全市场",
                "description": desc,
            })
    else:
        print("  ⚠️ 东方财富API无数据，使用已知近期政策事件")

    return events


def get_known_policy_events() -> list[dict]:
    """已知近期政策事件（基于web_search结果，2025-2026年）
    这些是硬编码的近期政策事件，当API不可用时作为fallback
    """
    events = [
        {
            "event_date": "2026-09-02",
            "event_title": "央行9月2日7天期逆回购操作量为零，3590亿元1天期+2395亿元7天期逆回购到期",
            "event_source": "同花顺-央行公开市场操作",
            "policy_type": "liquidity_drain",
            "sentiment_impact": -2,
            "affected_sectors": "全市场",
            "description": "央行7天期逆回购操作量为零，有大额逆回购到期，净回笼资金",
        },
        {
            "event_date": "2026-09-12",
            "event_title": "央行将于9月15日开展6000亿元买断式逆回购操作，期限6个月",
            "event_source": "人民网-央行操作",
            "policy_type": "liquidity_injection",
            "sentiment_impact": 2,
            "affected_sectors": "全市场",
            "description": "为保持银行体系流动性充裕，央行开展6000亿元买断式逆回购操作，期限182天",
        },
        {
            "event_date": "2026-09-04",
            "event_title": "央行9月5日将开展10000亿元买断式逆回购操作，期限3个月",
            "event_source": "21财经-央行操作",
            "policy_type": "liquidity_injection",
            "sentiment_impact": 3,
            "affected_sectors": "全市场",
            "description": "为保持银行体系流动性充裕，央行开展10000亿元买断式逆回购操作，期限91天",
        },
        {
            "event_date": "2026-08-28",
            "event_title": "证监会发布《关于资本市场支持构建房地产发展新模式的意见》",
            "event_source": "证监会官网",
            "policy_type": "property_reform",
            "sentiment_impact": 1,
            "affected_sectors": "房地产,券商",
            "description": "证监会发布关于资本市场支持构建房地产发展新模式的意见，支持房地产发展转型",
        },
        {
            "event_date": "2026-08-14",
            "event_title": "证监会发布上市公司2025年年度财务报告会计监管报告",
            "event_source": "证监会官网",
            "policy_type": "enforcement",
            "sentiment_impact": -1,
            "affected_sectors": "全市场",
            "description": "证监会发布上市公司年度财务报告会计监管报告，加强财务监管",
        },
        {
            "event_date": "2026-08-03",
            "event_title": "吴清主席在香港人民币国债期货上市仪式上致辞，深化资本市场高水平开放",
            "event_source": "证监会官网",
            "policy_type": "internationalization",
            "sentiment_impact": 1,
            "affected_sectors": "全市场",
            "description": "吴清主席在香港推出人民币国债期货上市仪式上的致辞，深化务实合作共创十五五资本市场高水平开放新局面",
        },
        {
            "event_date": "2026-07-31",
            "event_title": "证监会同意焦炭期权注册",
            "event_source": "证监会官网",
            "policy_type": "derivatives_regulation",
            "sentiment_impact": 1,
            "affected_sectors": "周期",
            "description": "证监会同意焦炭期权注册，丰富衍生品工具",
        },
        {
            "event_date": "2026-07-31",
            "event_title": "金融监管总局中国人民银行证监会财政部关于健全金融机构治理的实施意见",
            "event_source": "证监会官网",
            "policy_type": "financial_governance",
            "sentiment_impact": -1,
            "affected_sectors": "银行,券商",
            "description": "四部门联合发布关于健全金融机构治理的实施意见",
        },
        {
            "event_date": "2026-07-05",
            "event_title": "证监会对再融资办法及配套规则修改，八大亮点：优化小额快速融资、统一定增基准价、建立储架发行制度",
            "event_source": "每经头条",
            "policy_type": "refinancing_rule",
            "sentiment_impact": 1,
            "affected_sectors": "全市场",
            "description": "证监会对《上市公司证券发行注册管理办法》修改，优化小额快速融资制度（上限提升）、统一定增发行期首日定价、建立储架发行制度、简化控股股东定增条件、明确募集资金投向主业、加强可转债投资者保护、完善战略投资者制度",
        },
        {
            "event_date": "2026-08-25",
            "event_title": "证监会修改《证券公司分类监管规定》为《证券公司分类评价规定》，突出促进功能发挥",
            "event_source": "新华网",
            "policy_type": "broker_regulation",
            "sentiment_impact": -1,
            "affected_sectors": "券商",
            "description": "证监会修改证券公司分类监管规定，突出促进证券公司功能发挥，支持中小机构差异化发展，突出打大打恶导向",
        },
        {
            "event_date": "2026-05-22",
            "event_title": "证监会等八部门联合印发《综合整治非法跨境证券期货基金经营活动实施方案》",
            "event_source": "证监会官网",
            "policy_type": "cross_border_enforcement",
            "sentiment_impact": -2,
            "affected_sectors": "全市场",
            "description": "八部门联合整治非法跨境证券期货基金经营活动",
        },
        {
            "event_date": "2026-05-15",
            "event_title": "证监会发布《衍生品交易监督管理办法（试行）》",
            "event_source": "证监会官网",
            "policy_type": "derivatives_regulation",
            "sentiment_impact": -1,
            "affected_sectors": "全市场",
            "description": "证监会第234号令，衍生品交易监督管理办法试行",
        },
        {
            "event_date": "2026-09-05",
            "event_title": "证监会主席吴清周末发声：持续巩固资本市场回稳向好势头，中央汇金已大举加仓股票ETF",
            "event_source": "雪球-政策与监管动态",
            "policy_type": "sovereign_fund",
            "sentiment_impact": 3,
            "affected_sectors": "全市场",
            "description": "证监会主席吴清强调持续巩固资本市场回稳向好势头，透露中央汇金已大举加仓股票ETF，释放稳市信号。保险资金权益投资比例上限已上调，拟再批600亿元长期试点资金",
        },
        {
            "event_date": "2026-08-01",
            "event_title": "中国人民银行中国证监会令《金融基础设施监督管理办法》发布",
            "event_source": "证监会官网",
            "policy_type": "financial_governance",
            "sentiment_impact": -1,
            "affected_sectors": "全市场",
            "description": "央行与证监会联合发布金融基础设施监督管理办法",
        },
        {
            "event_date": "2026-02-27",
            "event_title": "证监会发布《私募投资基金信息披露监督管理办法》",
            "event_source": "证监会官网",
            "policy_type": "regulatory_tightening",
            "sentiment_impact": -1,
            "affected_sectors": "全市场",
            "description": "证监会第233号令，加强私募基金信息披露监管",
        },
        {
            "event_date": "2026-04-24",
            "event_title": "证监会发布《上市公司董事会秘书监管规则》及QFII参与国债期货交易公告",
            "event_source": "证监会官网",
            "policy_type": "qfii_reform",
            "sentiment_impact": 2,
            "affected_sectors": "全市场",
            "description": "上市公司董事会秘书监管规则发布；合格境外机构和人民币合格境外机构投资者可参与国债期货交易",
        },
    ]

    # 对每个事件用评分规则重新评分（覆盖硬编码值）
    for evt in events:
        score, ptype = score_event(evt["event_title"], evt["description"])
        if score != 0:
            evt["sentiment_impact"] = score
            evt["policy_type"] = ptype

    return events


def ensure_policy_table(db: sqlite3.Connection):
    """确保policy_events表存在"""
    db.execute("""
        CREATE TABLE IF NOT EXISTS policy_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date TEXT NOT NULL,
            event_title TEXT NOT NULL,
            event_source TEXT,
            policy_type TEXT,
            sentiment_impact INTEGER DEFAULT 0,
            affected_sectors TEXT,
            description TEXT,
            available_at TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now', '+8 hours')),
            UNIQUE(event_date, event_title)
        )
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_policy_date ON policy_events(event_date)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_policy_type ON policy_events(policy_type)")
    db.commit()


def store_events(db: sqlite3.Connection, events: list[dict]) -> int:
    """存储政策事件到数据库"""
    stored = 0
    now_iso = datetime.now().isoformat()

    for evt in events:
        try:
            evt_date = evt["event_date"]
            try:
                dt = datetime.strptime(evt_date, "%Y-%m-%d")
                available_at = dt.isoformat()
            except ValueError:
                available_at = now_iso

            db.execute("""
                INSERT OR IGNORE INTO policy_events
                (event_date, event_title, event_source, policy_type,
                 sentiment_impact, affected_sectors, description, available_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evt_date,
                evt["event_title"],
                evt["event_source"],
                evt["policy_type"],
                evt["sentiment_impact"],
                evt["affected_sectors"],
                evt["description"],
                available_at,
            ))
            stored += 1
        except Exception as e:
            print(f"  ⚠️ 存储失败: {evt.get('event_title','')[:50]} → {e}")

    db.commit()
    return stored


def collect_all():
    """采集全部L1政策数据"""
    print("=" * 60)
    print("📊 L1政策与监管层数据采集")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 60)

    db = sqlite3.connect(str(DB_PATH))
    ensure_policy_table(db)

    all_events = []

    # 1. 尝试东方财富API
    pboc_events = collect_pboc_operations()
    all_events.extend(pboc_events)
    print(f"  → 央行操作API采集 {len(pboc_events)} 条")

    # 2. 使用已知政策事件（基于web_search结果）
    known_events = get_known_policy_events()
    all_events.extend(known_events)
    print(f"  → 已知政策事件 {len(known_events)} 条")

    # 去重（按标题前30字符）
    seen_titles = set()
    unique_events = []
    for evt in all_events:
        key = evt["event_title"][:30]
        if key not in seen_titles:
            seen_titles.add(key)
            unique_events.append(evt)

    print(f"\n📌 去重后共 {len(unique_events)} 条事件（原始 {len(all_events)} 条）")

    # 存储
    stored = store_events(db, unique_events)
    print(f"✅ 存储 {stored} 条政策事件")

    # 统计评分分布
    score_dist = {}
    for evt in unique_events:
        s = evt["sentiment_impact"]
        bucket = "利好" if s > 0 else ("利空" if s < 0 else "中性")
        score_dist[bucket] = score_dist.get(bucket, 0) + 1
    print(f"\n📋 评分分布: {score_dist}")

    # 显示最新记录
    print(f"\n📋 最新15条政策事件:")
    rows = db.execute("""
        SELECT event_date, event_title, policy_type, sentiment_impact, affected_sectors
        FROM policy_events
        ORDER BY event_date DESC, id DESC
        LIMIT 15
    """).fetchall()
    for i, row in enumerate(rows):
        impact_str = f"{'+' if row[3] > 0 else ''}{row[3]}"
        title_short = row[1][:55] + ("..." if len(row[1]) > 55 else "")
        print(f"  {i+1}. [{row[0]}] {title_short}")
        print(f"     类型:{row[2]} 影响:{impact_str} 板块:{row[4]}")

    # 按类型统计
    print(f"\n📋 按政策类型统计:")
    type_rows = db.execute("""
        SELECT policy_type, COUNT(*) as cnt, ROUND(AVG(sentiment_impact), 1) as avg_score
        FROM policy_events
        GROUP BY policy_type
        ORDER BY cnt DESC
    """).fetchall()
    for row in type_rows:
        print(f"  {row[0]}: {row[1]}条 平均评分:{row[2]}")

    # L1综合指标
    print(f"\n📋 L1综合指标（最近30天）:")
    recent = db.execute("""
        SELECT
            COUNT(*) as event_count,
            ROUND(AVG(sentiment_impact), 2) as avg_strength,
            SUM(CASE WHEN sentiment_impact > 0 THEN 1 ELSE 0 END) as bullish_count,
            SUM(CASE WHEN sentiment_impact < 0 THEN 1 ELSE 0 END) as bearish_count
        FROM policy_events
        WHERE event_date >= date('now', '-30 days')
    """).fetchone()
    if recent and recent[0]:
        print(f"  政策事件数: {recent[0]}")
        print(f"  平均评分: {recent[1]}")
        print(f"  利好事件: {recent[2]} | 利空事件: {recent[3]}")
        direction = "bullish" if recent[1] > 0.5 else ("bearish" if recent[1] < -0.5 else "neutral")
        print(f"  政策方向: {direction}")
    else:
        print(f"  近30天无政策事件")

    print(f"\n{'=' * 60}")
    print(f"✅ L1政策事件采集完成: 共 {stored} 条")
    print(f"📂 脚本: {Path(__file__)}")
    print(f"📂 数据库: {DB_PATH}")

    db.close()
    return stored


if __name__ == "__main__":
    collect_all()
