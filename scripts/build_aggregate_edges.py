#!/usr/bin/env python3
"""
build_aggregate_edges.py — P6-3 关系稀疏改聚合入边

问题：研报覆盖只有 131/411（32%），280 个个股 0 研报关联，个股页 0 入链像信息孤岛。
方案：不硬造关联（违反 AGENTS.md「不臆造数据」）。改为聚合入边——让行业页/概念页
挂个股，个股通过行业节点获得入链。

实现：
1. 读所有 stocks 文件的 frontmatter（code/name/industry/concept/market_cap）
2. 按 industry 分组 → 给每个 industries/<name>.md 在"成分股"段后追加"成分股列表"段
3. 按 concept 分组 → 给每个 concepts/<name>.md 在"成分股"段后追加"成分股列表"段

成分股列表格式：
    ## 📋 成分股列表

    - [[10_Reference/investing/stocks/000001|平安银行（000001）]]
    - [[10_Reference/investing/stocks/000002|万科A（000002）]]

幂等：已有"## 📋 成分股列表"段则替换其内容，不会重复追加。
不修改 index.md / templates/ / .quartz/。

用法：
    python3 scripts/build_aggregate_edges.py [--dry-run] [--vault PATH]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# 默认 vault 路径
DEFAULT_VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault")

# 投研子区根
INVESTING = "10_Reference/investing"
STOCKS_DIR = "stocks"
INDUSTRIES_DIR = "industries"
CONCEPTS_DIR = "concepts"

# 聚合段标题（唯一锚点，用于幂等替换）
AGGREGATE_HEADING = "## 📋 成分股列表"

# 行业页/概念页里"成分股"段的标题（Dataview 预编译表格所在段）
COMPONENT_HEADING = "## 🏢 成分股"


# ---------------- frontmatter 解析 ----------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """解析 YAML frontmatter 为扁平 dict（仅支持简单的 key: value 行）。

    不引入 PyYAML 依赖——vault 脚本历史上一律用标准库解析 frontmatter
    （见 init_entity_dictionary.py / precompile_dataview.py），保持一致。
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        # 跳过空行/注释/多行结构（本任务只需 scalar 字段）
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # 去掉引号
        if value and value[0] in "\"'" and value[-1] == value[0]:
            value = value[1:-1]
        fm[key] = value
    return fm


# ---------------- market_cap 排序 ----------------

def parse_market_cap_num(value: str) -> float:
    """把 market_cap 字符串解析为以"亿"为单位的浮点数，用于排序。

    支持两种格式：
      - "215B"  → 215.0（B = 亿，本 vault 约定 B 即"亿"）
      - "977.58亿" → 977.58
      - "2.18万亿" → 21800.0
    无法解析返回 -1（排到末尾）。
    """
    if not value:
        return -1.0
    s = value.strip()
    try:
        if s.endswith("万亿"):
            return float(s[:-2]) * 10000.0
        if s.endswith("亿"):
            return float(s[:-1])
        if s.endswith("B"):
            return float(s[:-1])
        return float(s)
    except (ValueError, IndexError):
        return -1.0


def stock_sort_key(stock: dict) -> tuple:
    """排序键：market_cap 降序（None/空排末尾），code 升序兜底。"""
    cap = parse_market_cap_num(stock.get("market_cap", ""))
    # 负值取反实现降序（sorted reverse 不好混用，故用负数）
    return (-cap, stock.get("code", ""))


# ---------------- wikilink 生成 ----------------

def make_stock_wikilink(code: str, name: str) -> str:
    """生成 [[10_Reference/investing/stocks/<code>|<name>（<code>）]]。"""
    target = f"10_Reference/investing/stocks/{code}"
    alias = f"{name}（{code}）"
    return f"- [[{target}|{alias}]]"


def make_aggregate_section(stocks: list[dict]) -> str:
    """构造整段"成分股列表"内容（不含尾随换行由调用方控制）。"""
    lines = [AGGREGATE_HEADING, ""]
    for s in sorted(stocks, key=stock_sort_key):
        code = s.get("code", "").strip()
        name = s.get("name", "").strip()
        if not code or not name:
            continue
        lines.append(make_stock_wikilink(code, name))
    return "\n".join(lines)


# ---------------- 段落插入/替换 ----------------

def replace_or_insert_section(text: str, anchor_heading: str, new_section: str) -> tuple[str, bool]:
    """在 anchor_heading 段之后插入/替换 new_section 段。

    逻辑：
      1. 若 AGGREGATE_HEADING 段已存在 → 替换其内容（幂等更新）
      2. 否则 → 在 anchor_heading 段结束后（下一个 ## 或文件末）前插入

    返回 (新文本, 是否改动)。
    """
    # 情况 1：已有聚合段 → 替换
    if AGGREGATE_HEADING in text:
        # 匹配从 AGGREGATE_HEADING 行开始到下一个 ## 标题前或文件末
        pattern = re.compile(
            r"^" + re.escape(AGGREGATE_HEADING) + r"[^\n]*\n(.*?)(?=\n## |\Z)",
            re.DOTALL | re.MULTILINE,
        )
        m = pattern.search(text)
        if m:
            old_block = m.group(0)
            # 重组：标题行 + 空行 + 列表行
            new_block = new_section
            if old_block.rstrip() == new_block.rstrip():
                return text, False
            return text[: m.start()] + new_block + text[m.end():], True
        # 标题在但正则没匹配上（理论上不会），落到情况 2
    # 情况 2：无聚合段，在 anchor 段后插入
    # 找到 anchor_heading 行，然后找到该段的结束（下一个 ## 标题或文件末）
    anchor_pattern = re.compile(
        r"^" + re.escape(anchor_heading) + r"[^\n]*\n(.*?)(?=\n## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = anchor_pattern.search(text)
    if not m:
        # 找不到 anchor 段，追加到文件末（带分隔）
        insertion = "\n\n" + new_section + "\n"
        if text.endswith("\n"):
            return text + insertion.lstrip("\n"), True
        return text + insertion, True
    # 在 anchor 段结束后插入（anchor 段含其后的内容直到下一个 ##）
    pos = m.end()
    # m.end() 指向下一个 ## 前的 \n 位置；插入点在 anchor 段末尾内容之后
    # 找到 anchor 段内容的最后一个非空行末尾
    seg = m.group(1)
    # 插入：空行 + 新段 + 空行
    insertion = "\n" + new_section + "\n"
    # 确保插入位置前有换行
    new_text = text[:pos] + insertion + text[pos:]
    # 清理可能的多余空行（连续 3+ 换行压成 2）
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    return new_text, True


# ---------------- 主流程 ----------------

def scan_stocks(vault: Path) -> list[dict]:
    """扫描所有 stocks/*.md（排除 index.md），返回 frontmatter dict 列表。"""
    stocks_dir = vault / INVESTING / STOCKS_DIR
    out = []
    for p in sorted(stocks_dir.glob("*.md")):
        if p.name == "index.md":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if not fm:
            continue
        # 必须有 code（个股实体的最低要求）
        if not fm.get("code"):
            continue
        fm["_file"] = str(p)
        out.append(fm)
    return out


def group_by_field(stocks: list[dict], field: str) -> dict[str, list[dict]]:
    """按 field 分组。concept 字段是逗号分隔多值，需拆分。"""
    groups: dict[str, list[dict]] = {}
    for s in stocks:
        raw = s.get(field, "").strip()
        if not raw:
            continue
        # concept 是逗号分隔；industry 是单值（但兼容逗号分隔也安全）
        if field == "concept":
            vals = [v.strip() for v in raw.split(",") if v.strip()]
        else:
            vals = [raw]
        for v in vals:
            groups.setdefault(v, []).append(s)
    return groups


def update_entity_file(path: Path, stocks: list[dict], dry_run: bool) -> tuple[bool, int]:
    """给单个 industry/concept 文件插入/更新聚合段。返回 (是否改动, 成分股数)。"""
    if not path.exists():
        return False, 0
    text = path.read_text(encoding="utf-8")
    new_section = make_aggregate_section(stocks)
    new_text, changed = replace_or_insert_section(text, COMPONENT_HEADING, new_section)
    if changed and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return changed, len(stocks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="P6-3: 关系稀疏改聚合入边——行业页/概念页挂个股"
    )
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="vault 根路径")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.exists():
        print(f"[ERROR] vault 路径不存在: {vault}", file=sys.stderr)
        return 2

    print(f"[INFO] vault = {vault}")
    print(f"[INFO] dry_run = {args.dry_run}")

    # 1. 扫描 stocks
    stocks = scan_stocks(vault)
    print(f"[INFO] 扫描到 {len(stocks)} 个 stock 实体")

    # 2. 按 industry 分组 → 更新 industries/*.md
    industries_dir = vault / INVESTING / INDUSTRIES_DIR
    industry_groups = group_by_field(stocks, "industry")
    ind_changed = 0
    ind_edges = 0
    ind_missing_files: list[str] = []
    for name, group in sorted(industry_groups.items()):
        target = industries_dir / f"{name}.md"
        if not target.exists():
            ind_missing_files.append(name)
            continue
        changed, n = update_entity_file(target, group, args.dry_run)
        if changed:
            ind_changed += 1
            ind_edges += n
    print(f"[INFO] industries: 更新 {ind_changed} 个文件，新增/更新 {ind_edges} 条聚合入边")
    if ind_missing_files:
        print(f"[WARN] industry 分组里找不到对应 .md 的行业名（{len(ind_missing_files)} 个）："
              f"{', '.join(ind_missing_files[:10])}{'...' if len(ind_missing_files) > 10 else ''}")

    # 3. 按 concept 分组 → 更新 concepts/*.md
    concepts_dir = vault / INVESTING / CONCEPTS_DIR
    concept_groups = group_by_field(stocks, "concept")
    con_changed = 0
    con_edges = 0
    con_missing_files: list[str] = []
    for name, group in sorted(concept_groups.items()):
        target = concepts_dir / f"{name}.md"
        if not target.exists():
            con_missing_files.append(name)
            continue
        changed, n = update_entity_file(target, group, args.dry_run)
        if changed:
            con_changed += 1
            con_edges += n
    print(f"[INFO] concepts: 更新 {con_changed} 个文件，新增/更新 {con_edges} 条聚合入边")
    if con_missing_files:
        print(f"[WARN] concept 分组里找不到对应 .md 的概念名（{len(con_missing_files)} 个）："
              f"{', '.join(con_missing_files[:10])}{'...' if len(con_missing_files) > 10 else ''}")

    total_edges = ind_edges + con_edges
    total_files = ind_changed + con_changed
    print(f"\n[DONE] 共更新 {total_files} 个实体页，聚合入边 {total_edges} 条")
    if args.dry_run:
        print("[DRY-RUN] 未写入文件。去掉 --dry-run 实际执行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
