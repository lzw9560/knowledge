#!/usr/bin/env python3
"""刷新首页/MOC/导航的统计表格——从 frontmatter 实时算。

单一真相源：遍历 10_Reference/investing/ 下所有 .md，读 frontmatter 的 type 字段，
重算总实体数 + 各类型计数 + 各文件夹计数，写回三处统计表。

用法：
    python3 scripts/refresh_stats.py            # 写回
    python3 scripts/refresh_stats.py --dry-run  # 仅预览不写文件
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault")
INVESTING = VAULT / "10_Reference" / "investing"

# 跳过模板与索引类文件（不参与实体计数）
EXCLUDE_NAMES = {"index.md", "MOC.md", "SUMMARY.md", "README.md"}

# 投研子层分组（导航统计概览用）
SENTIMENT_DIR = VAULT / "10_Reference" / "market_sentiment"


def parse_frontmatter_type(content: str) -> str | None:
    """从 markdown frontmatter 提取 type 字段值。"""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    for line in m.group(1).split("\n"):
        if line.startswith("type:"):
            return line.split(":", 1)[1].strip().strip("\"'` ")
    return None


def count_investing_entities() -> tuple[Counter, Counter, int]:
    """遍历 investing 子区，按 frontmatter type 与所在文件夹计数。

    返回 (type_counts, folder_counts, total)。
    """
    type_counts: Counter = Counter()
    folder_counts: Counter = Counter()
    total = 0
    for f in INVESTING.rglob("*.md"):
        rel = f.relative_to(INVESTING)
        if "templates" in rel.parts:
            continue
        if f.name in EXCLUDE_NAMES:
            continue
        content = f.read_text(encoding="utf-8")
        t = parse_frontmatter_type(content)
        if t is None:
            continue
        type_counts[t] += 1
        total += 1
        # 所在文件夹 = investing/ 下第一级目录
        if rel.parts:
            folder_counts[rel.parts[0]] += 1
    return type_counts, folder_counts, total


def count_dir_md(folder: str) -> int:
    """统计某目录下 .md 数（排除模板与索引文件）。"""
    d = VAULT / folder
    if not d.exists():
        return 0
    n = 0
    for f in d.rglob("*.md"):
        if "templates" in str(f.relative_to(d)):
            continue
        if f.name in EXCLUDE_NAMES:
            continue
        n += 1
    return n


def count_sentiment_entities() -> int:
    """统计 market_sentiment 下实体数（排除索引/模板/数据子目录）。"""
    if not SENTIMENT_DIR.exists():
        return 0
    n = 0
    for f in SENTIMENT_DIR.rglob("*.md"):
        rel = f.relative_to(SENTIMENT_DIR)
        # 排除 _data / _  开头的内部目录、reviews、daily、索引文件
        if rel.parts and rel.parts[0].startswith("_"):
            continue
        if "templates" in rel.parts:
            continue
        if f.name in EXCLUDE_NAMES:
            continue
        n += 1
    return n


# ──────────────────────────────────────────────────────────────
# 统计表格渲染
# ──────────────────────────────────────────────────────────────


def render_total_table(total: int) -> str:
    """单行"实体总数"表。"""
    return f"| 实体总数 |\n|---|\n| {total} |"


def render_type_counts_table(type_counts: Counter) -> str:
    """类型 | 数量 表（按数量降序）。"""
    lines = ["| 类型 | 数量 |", "|---|---|"]
    for t, c in sorted(type_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {t} | {c} |")
    return "\n".join(lines)


def render_folder_counts_table(folder_counts: Counter) -> str:
    """首页"全局统计"表——投研各文件夹 + 非投研领域 + Active/Archive + 合计。

    全部实时计数，无 ~ 近似值。
    """
    lines = ["| 文件夹 | 笔记数 |", "|---|---|"]
    # 投研各文件夹（按数量降序）
    for fld, c in sorted(folder_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| 10_Reference/investing/{fld} | {c} |")
    # 非投研领域
    tech = count_dir_md("10_Reference/tech-learning")
    reading = count_dir_md("10_Reference/reading")
    projects = count_dir_md("10_Reference/projects")
    meta = count_dir_md("10_Reference/meta")
    lines.append(f"| 10_Reference/tech-learning | {tech} |")
    lines.append(f"| 10_Reference/reading | {reading} |")
    lines.append(f"| 10_Reference/projects | {projects} |")
    lines.append(f"| 10_Reference/meta | {meta} |")
    # Active / Archive
    active = count_dir_md("00_Active")
    archive = count_dir_md("20_Archive")
    lines.append(f"| 00_Active | {active} |")
    lines.append(f"| 20_Archive | {archive} |")
    grand = sum(folder_counts.values()) + tech + reading + projects + meta + active + archive
    lines.append(f"| **合计** | **{grand}** |")
    return "\n".join(lines)


def render_nav_stats_table(type_counts: Counter, total: int) -> str:
    """导航.md 统计概览表。"""
    tech = count_dir_md("10_Reference/tech-learning")
    reading = count_dir_md("10_Reference/reading")
    projects = count_dir_md("10_Reference/projects")
    meta = count_dir_md("10_Reference/meta")
    sentiment = count_sentiment_entities()
    grand_total = total + tech + reading + projects + meta + sentiment
    lines = [
        "| 领域 | 子层数 | 子分类数 | 实体数 | 状态 |",
        "|---|---|---|---|---|",
        f"| 📊 投研 | 5 层 | {len(type_counts)} 类 | {total} | ✅ 活跃 |",
        f"| 🌡️ 市场情绪 | 2 层 | 3 类 | {sentiment} | ✅ 运行中 |",
        f"| 💻 技术学习 | 1 层 | 5 类 | {tech} | ✅ 已建 |",
        f"| 📚 读书/学习 | 1 层 | 3 类 | {reading} | ✅ 已建 |",
        f"| 📋 项目追踪 | 1 层 | 3 类 | {projects} | ✅ 已建 |",
        f"| 🧠 元知识 | — | — | {meta} | ✅ 已建 |",
        f"| **合计** | **5 层** | **{len(type_counts) + 8}+** | **{grand_total}** | |",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# precompiled 块替换
# ──────────────────────────────────────────────────────────────

# 匹配 <!-- dataview-precompiled:ID -->...<!-- /dataview-precompiled -->
PRECOMPILED_RE = re.compile(
    r"(<!--\s*dataview-precompiled:[a-f0-9-]+\s*-->\n)"  # group 1: open tag
    r"(.*?)"  # group 2: inner content
    r"(\n<!--\s*/dataview-precompiled\s*-->)",  # group 3: close tag
    re.DOTALL,
)


def replace_precompiled(content: str, block_id_substring: str, new_inner: str) -> str:
    """替换 precompiled 块内容。block_id_substring 用于定位匹配的块。

    保留原 open/close 标签，仅替换中间内容。若未匹配到块则原样返回。
    """
    def repl(m: re.Match) -> str:
        full = m.group(0)
        if block_id_substring in full:
            return f"{m.group(1)}{new_inner}{m.group(3)}"
        return full

    return PRECOMPILED_RE.sub(repl, content)


# 锚点注释——稳定标识，不随 hash 漂移
# 在 MOC.md 等文件的统计表格上方加 <!-- stats-anchor:xxx --> 注释，
# refresh_stats 按锚点定位表格，而非易漂移的 dataview-precompiled hash ID。
ANCHOR_RE = re.compile(
    r"(<!--\s*stats-anchor:([a-z0-9_-]+)\s*-->\n)"  # group 1: anchor comment, group 2: anchor name
    r"(.*?)"  # group 3: content until close
    r"(\n<!--\s*/stats-anchor\s*-->)",
    re.DOTALL,
)


def replace_by_anchor(content: str, anchor_name: str, new_inner: str) -> str:
    """按锚点注释 <!-- stats-anchor:name -->...<!-- /stats-anchor --> 替换内容。

    保留锚点注释，仅替换中间内容。若未匹配到锚点则原样返回。
    """
    def repl(m: re.Match) -> str:
        if m.group(2) == anchor_name:
            return f"{m.group(1)}{new_inner}{m.group(4)}"
        return m.group(0)

    return ANCHOR_RE.sub(repl, content)


def replace_precompiled_or_anchor(
    content: str, anchor_name: str, old_hash: str, new_inner: str
) -> str:
    """优先按锚点注释定位，回退到旧 hash ID。

    锚点注释存在时用锚点（稳定）；不存在时回退到旧 hash（向后兼容）。
    """
    # 优先锚点
    if f"stats-anchor:{anchor_name}" in content:
        content = replace_by_anchor(content, anchor_name, new_inner)
        return content
    # 回退旧 hash（向后兼容未加锚点的旧 MOC）
    return replace_precompiled(content, old_hash, new_inner)


def replace_plain_table(content: str, header_marker: str, new_table: str) -> str:
    """替换非 precompiled 的普通 markdown 表格段（首页用）。

    header_marker: 用于定位的表头行（如 "| 类型 | 数量 |"）。
    替换范围 = header_marker 前的表头分界到下一个空行/分隔符。
    为稳健起见，用 header_marker 到其后连续表格行为止的区间替换。
    """
    lines = content.split("\n")
    out: list[str] = []
    i = 0
    replaced = False
    while i < len(lines):
        if not replaced and header_marker in lines[i]:
            # 写入新表
            out.append(new_table)
            replaced = True
            # 跳过原表的连续行（以 | 开头或空行——空行不跳，留给新表）
            i += 1
            # 跳过表头分隔行 |---|
            while i < len(lines) and (
                lines[i].strip().startswith("|")
                and "---" in lines[i]
            ):
                i += 1
            # 跳过数据行
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


# ──────────────────────────────────────────────────────────────
# 三个目标文件更新
# ──────────────────────────────────────────────────────────────


def update_home(total: int, type_counts: Counter, folder_counts: Counter, dry: bool) -> bool:
    """更新 🏠 首页.md。"""
    path = VAULT / "🏠 首页.md"
    content = path.read_text(encoding="utf-8")
    orig = content

    # 1) 实体总数表（普通表，非 precompiled）
    content = replace_plain_table(content, "| 实体总数 |", render_total_table(total))

    # 2) 各类型计数表（普通表）
    content = replace_plain_table(content, "| 类型 | 数量 |", render_type_counts_table(type_counts))

    # 3) 全局统计表（普通表，表头 | 文件夹 | 笔记数 |）
    content = replace_plain_table(content, "| 文件夹 | 笔记数 |", render_folder_counts_table(folder_counts))

    # 4) 散落的旧硬编码数字——替换正文里的 "2400+ 实体" / "2400+ 实体，16 实体类"
    content = content.replace("2400+ 实体，16 实体类 + 12 战法卡", f"{total}+ 实体，{len(type_counts)} 实体类 + 12 战法卡")
    content = content.replace("投研知识图谱入口（2400+ 实体）", f"投研知识图谱入口（{total}+ 实体）")
    content = content.replace("16 实体类 + 16 模板 + 12 战法卡 + 2400+ 实体", f"{len(type_counts)} 实体类 + 16 模板 + 12 战法卡 + {total}+ 实体")

    changed = content != orig
    if changed and not dry:
        path.write_text(content, encoding="utf-8")
    return changed


def update_moc(total: int, type_counts: Counter, dry: bool) -> bool:
    """更新 10_Reference/investing/MOC.md。

    统计表格按 <!-- stats-anchor:total --> / <!-- stats-anchor:type-counts -->
    锚点定位（稳定，不随 dataview-precompiled hash 漂移）。无锚点时回退旧 hash。
    """
    path = INVESTING / "MOC.md"
    content = path.read_text(encoding="utf-8")
    orig = content

    # 1) 实体总数表——锚点 stats-anchor:total，回退 hash a6d4be462c4a
    content = replace_precompiled_or_anchor(
        content, "total", "a6d4be462c4a", render_total_table(total)
    )

    # 2) 各类型实体计数表——锚点 stats-anchor:type-counts，回退 hash c649e86810b8
    content = replace_precompiled_or_anchor(
        content, "type-counts", "c649e86810b8", render_type_counts_table(type_counts)
    )

    # 3) 正文里硬编码的 "2400+ 实体" / "16 实体类"
    content = content.replace(
        "16 实体类，2400+ 实体，12 战法卡",
        f"{len(type_counts)} 实体类，{total}+ 实体，12 战法卡",
    )

    changed = content != orig
    if changed and not dry:
        path.write_text(content, encoding="utf-8")
    return changed


def update_nav(total: int, type_counts: Counter, dry: bool) -> bool:
    """更新 导航.md 统计概览表。"""
    path = VAULT / "导航.md"
    content = path.read_text(encoding="utf-8")
    orig = content

    content = replace_plain_table(
        content, "| 领域 | 子层数 | 子分类数 | 实体数 | 状态 |",
        render_nav_stats_table(type_counts, total),
    )

    changed = content != orig
    if changed and not dry:
        path.write_text(content, encoding="utf-8")
    return changed


# ──────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="仅预览不写文件")
    args = ap.parse_args()

    type_counts, folder_counts, total = count_investing_entities()

    print(f"[refresh_stats] 投研子区总实体数: {total}")
    print(f"[refresh_stats] 类型数: {len(type_counts)}")
    for t, c in sorted(type_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {t}: {c}")

    home_changed = update_home(total, type_counts, folder_counts, args.dry_run)
    moc_changed = update_moc(total, type_counts, args.dry_run)
    nav_changed = update_nav(total, type_counts, args.dry_run)

    tag = "[dry-run] " if args.dry_run else ""
    print(f"{tag}🏠 首页.md: {'已更新' if home_changed else '无变化'}")
    print(f"{tag}MOC.md: {'已更新' if moc_changed else '无变化'}")
    print(f"{tag}导航.md: {'已更新' if nav_changed else '无变化'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
