#!/usr/bin/env python3
"""批量更新股票实体格式——应用新模板的 callout+emoji 样式。

转换规则见 specs/S029 或任务说明：
- frontmatter 保持不变
- 基本信息 → [!info] callout
- 各段标题加 emoji（📊/💰/📰/🐉/⚡/🎯/🔗）
- Dataview 加 WITHOUT ID + 全路径 FROM + LIMIT
- 估值 → [!tip] callout 包裹
- 匹配战法 → contains(file.outlinks, this.file.link) 反向匹配
- 核心业务段正文保留（去除旧的"所属行业/概念"链接行，已并入 callout）
- 关系网段新增（所有股票统一加）

用法:
    python3 scripts/update_stock_format.py            # 全量更新
    python3 scripts/update_stock_format.py --dry-run  # 只预览不写盘
    python3 scripts/update_stock_format.py 600519     # 仅更新指定文件
"""
import argparse
import re
import sys
from pathlib import Path

VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault/10_Reference/investing")
STOCKS_DIR = VAULT / "stocks"

# 段落定义（顺序即输出顺序）
SECTION_DEFS = [
    ("metrics", "💰 财务速览", """```dataview
TABLE WITHOUT ID
  period AS "周期",
  revenue AS "营收(亿)",
  net_profit AS "净利(亿)",
  roe AS "ROE%",
  gross_margin AS "毛利率%",
  net_margin AS "净利率%"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND code = this.code
SORT period DESC
LIMIT 5
```"""),
    ("valuations", None, """> [!tip] 估值快照
> ```dataview
> TABLE WITHOUT ID
>   pe_ttm AS "PE(TTM)",
>   pb AS "PB",
>   peg AS "PEG",
>   pe_percentile AS "PE分位%",
>   pb_percentile AS "PB分位%"
> FROM "10_Reference/investing/valuations"
> WHERE type = "valuation" AND code = this.code
> SORT created DESC
> LIMIT 1
> ```"""),
    ("reports", "📰 相关研报", """```dataview
TABLE WITHOUT ID
  publish_date AS "日期",
  org AS "机构",
  researcher AS "分析师",
  report_type AS "评级",
  title AS "标题"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
LIMIT 10
```"""),
    ("dragon-tiger", "🐉 龙虎榜", """```dataview
TABLE WITHOUT ID
  date AS "日期",
  institution_net AS "机构净额",
  seats AS "席位"
FROM "10_Reference/investing/dragon-tiger"
WHERE type = "dragon_tiger" AND code = this.code
SORT date DESC
LIMIT 5
```"""),
    ("events", "⚡ 相关事件", """```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```"""),
    ("strategies", "🎯 匹配战法", """```dataview
TABLE WITHOUT ID
  name AS "战法",
  edge_family AS "edge 家族",
  file.link AS "详情"
FROM "10_Reference/investing/strategies"
WHERE type = "strategy" AND contains(file.outlinks, this.file.link)
SORT name ASC
```"""),
]

RELATION_NET = """## 🔗 关系网

- **数据源**：[[data-sources/tencent|腾讯行情]] · [[data-sources/eastmoney-push2|东财 push2]]
- **关联实体**：`=(length(this.file.outlinks))` 个出链 · `=(length(this.file.inlinks))` 个入链
"""


def parse_file(filepath: Path) -> tuple[str | None, str]:
    """分离 frontmatter 与正文。返回 (fm_text, body)。"""
    content = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)\Z", content, re.DOTALL)
    if not m:
        return None, content
    return m.group(1), m.group(2)


def get_fm_field(fm: str, key: str) -> str:
    """提取 frontmatter 标量字段值。支持 `key: value` 与 `key: "value"`。"""
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", fm, re.MULTILINE)
    if not m:
        return ""
    v = m.group(1).strip()
    # 去掉引号
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


def extract_core_business(body: str) -> str:
    """提取核心业务段正文，剔除"所属行业/概念"链接行（已并入 callout）。

    兼容旧格式（`# 核心业务`）与新格式（`## 📊 核心业务`）。
    """
    # 同时匹配旧 # 标题与新 ## emoji 标题；group(2) 为正文
    pattern = r"^#{1,2}\s*(📊\s*)?核心业务\s*\n(.*?)(?=\n#{1,2}\s|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.MULTILINE)
    if not m:
        return "待补充"
    section = m.group(2).strip()
    # 去除旧的 "- 所属行业：" / "- 所属概念：" 链接行
    section = re.sub(
        r"^\s*-\s*所属(行业|概念).*\n?",
        "",
        section,
        flags=re.MULTILINE,
    )
    # 去除空行残留
    section = re.sub(r"\n{3,}", "\n\n", section).strip()
    return section or "待补充"


def build_callout(fm: str) -> str:
    """构建 [!info] 基本信息 callout。"""
    code = get_fm_field(fm, "code")
    name = get_fm_field(fm, "name")
    market = get_fm_field(fm, "market") or "A"
    industry = get_fm_field(fm, "industry")
    concept = get_fm_field(fm, "concept")
    list_date = get_fm_field(fm, "list_date")
    pe_ttm = get_fm_field(fm, "pe_ttm")
    pb = get_fm_field(fm, "pb")
    market_cap = get_fm_field(fm, "market_cap")

    industry_link = f"[[industries/{industry}]]" if industry else "待核实"
    # concept 是逗号分隔字符串，如 "高端白酒, 白酒龙头, 食品饮料"
    concept_links = []
    if concept:
        for c in re.split(r"[,，、]", concept):
            c = c.strip()
            if c:
                concept_links.append(f"[[concepts/{c}]]")
    concept_link = " · ".join(concept_links) if concept_links else "待核实"

    return f"""> [!info] 基本信息
> **代码**：`{code}`  **名称**：{name}  **市场**：{market}
> **行业**：`{industry or "待核实"}`  **上市**：{list_date}
> **PE(TTM)**：`{pe_ttm}`  **PB**：`{pb}`  **市值**：`{market_cap}`
> 
> **行业**：{industry_link}  **概念**：{concept_link}"""


def build_new_content(fm: str, body: str) -> str:
    """组装新格式全文。"""
    callout = build_callout(fm)
    core_business = extract_core_business(body)

    parts: list[str] = [
        f"---\n{fm}\n---",
        "",
        callout,
        "",
        "## 📊 核心业务",
        "",
        core_business,
        "",
    ]

    for idx, (key, title, block) in enumerate(SECTION_DEFS):
        if title:
            parts.append(f"## {title}")
            parts.append("")
        parts.append(block)
        parts.append("")

    parts.append(RELATION_NET)

    # 确保文件以换行结尾
    return "\n".join(parts).rstrip() + "\n"


def update_stock(filepath: Path, dry_run: bool = False) -> bool:
    """更新单个股票文件。返回是否实际更新。"""
    fm, body = parse_file(filepath)
    if fm is None:
        print(f"⚠️  跳过（无 frontmatter）: {filepath.name}")
        return False

    new_content = build_new_content(fm, body)

    if dry_run:
        print(f"[DRY] 将更新: {filepath.name}")
        return True

    filepath.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="批量更新股票实体格式")
    parser.add_argument("--dry-run", action="store_true", help="只预览不写盘")
    parser.add_argument("files", nargs="*", help="指定文件名（不含路径），默认全量")
    args = parser.parse_args()

    if args.files:
        targets = [STOCKS_DIR / f for f in args.files]
        # 允许传 600519 或 600519.md
        targets = [
            STOCKS_DIR / (f if f.endswith(".md") else f + ".md") for f in args.files
        ]
    else:
        targets = sorted(STOCKS_DIR.glob("*.md"))

    count = 0
    skipped = 0
    for f in targets:
        if not f.exists():
            print(f"⚠️  文件不存在: {f.name}")
            skipped += 1
            continue
        if f.name == "index.md":
            continue
        if update_stock(f, dry_run=args.dry_run):
            count += 1
            print(f"✅ {f.name}")

    print(f"\n总计更新 {count} 只股票" + ("（dry-run，未写盘）" if args.dry_run else ""))
    if skipped:
        print(f"跳过 {skipped} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
