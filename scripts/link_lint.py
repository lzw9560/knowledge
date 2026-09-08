#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立链接检查器——CI 第二只眼。

用纯正则扫所有损坏模式，不依赖 precompile_dataview.py 的解析逻辑。
precompile 关注"能渲染的查 query"，本脚本关注"链接本身是否健康"——
两者正交，precompile 漏掉的损坏这里能兜底。

用法：
    python3 scripts/link_lint.py [--max-samples N] [--json]

退出码：
    0 = 无问题
    1 = 发现问题（CI 应阻断）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

# 跳过的目录名（模板/生成物/隐藏目录）
SKIP_PARTS = {"templates", ".quartz", ".git", ".obsidian", ".trash", "node_modules"}


def should_skip(path: Path) -> bool:
    """跳过模板、生成物、隐藏目录。"""
    return any(part in SKIP_PARTS for part in path.parts)


def strip_frontmatter(content: str) -> str:
    """剥掉 YAML frontmatter（---...---）。"""
    return re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)


def strip_codeblocks_and_comments(body: str) -> str:
    """剥掉代码块（```...```）、HTML 注释（<!--...-->）、行内代码（`...`）。"""
    clean = re.sub(r"```[\s\S]*?```", "", body)
    clean = re.sub(r"<!--[\s\S]*?-->", "", clean)
    # 行内代码：`...`（非贪婪，单行内）——含 `[[]]` 字面量也会被剥
    clean = re.sub(r"`[^`\n]+`", "", clean)
    return clean


# --------------------------------------------------------------------------- #
# 检查项
# --------------------------------------------------------------------------- #
# 先把完整 wikilink [[...]] 全部占位成空，剩下的 ]] / [[ 才是真损坏。
# 这样 broken_wikilink / orphan_open / orphan_close 都不会误报 wikilink 内部。
# 空链接 [[]] 也一并占位（文档里常出现的字面量，不算损坏）。
WIKILINK_RE = re.compile(r"\[\[([^\]]*)\]\]")
# 占位 token：足够特殊，不与任何 markdown 冲突
_PLACEHOLDER = "\x00WIKILINK\x00"

# 1. 裸 ]] 无配对 [[——占位后还在的 ]] 就是真损坏
BARE_CLOSE_RE = re.compile(r"\]\]")
# 2. 路径中间插入 [[——形如 "10_Reference/investing[[xxx"（wikilink 开括号被嵌进路径中）
INSERTED_OPEN_RE = re.compile(
    r"(10_Reference|tech-learning)[^\]\[ ]+\[\["
)
# 3. 裸短路径 [[stem]] 但目标不存在（在完整 wikilink 上检测，不用占位法）
SHORT_LINK_RE = re.compile(r"\[\[([^\]|/]+)\]\]")
# 4. markdown 链接 [text](path) 路径不存在
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _resolve_short_link_stem(target: str) -> bool:
    """[[stem]] 短链接目标是否存在。

    Obsidian 短链接按 stem（文件名无扩展）解析。本函数扫 vault 子树确认。
    跳过 http(s)/#锚点/含<的（HTML 残片）。
    """
    if target.startswith("http") or target.startswith("#") or "<" in target:
        return True  # 不算 missing
    if target in ("today", "yesterday", "tomorrow", "current", "this"):
        return True  # Dataview 保留字
    # 先看 vault 根
    if (VAULT / (target + ".md")).exists():
        return True
    # 扫常见子目录
    for sub in (
        "10_Reference/investing",
        "10_Reference/investing/stocks",
        "10_Reference/investing/indices",
        "10_Reference/investing/metrics",
        "10_Reference/investing/valuations",
        "10_Reference/investing/strategies",
        "10_Reference/investing/reviews",
        "10_Reference/tech-learning",
        "10_Reference/reading",
        "10_Reference/projects",
        "10_Reference/meta",
    ):
        if (VAULT / sub / (target + ".md")).exists():
            return True
    # 全 vault rglob 兜底（按 stem 匹配）
    for p in VAULT.rglob(target + ".md"):
        if not should_skip(p):
            return True
    return False


def lint_file(f: Path) -> list[tuple[str, str, str]]:
    """扫单个文件，返回 (issue_type, rel_path, snippet) 列表。"""
    issues: list[tuple[str, str, str]] = []
    try:
        content = f.read_text(encoding="utf-8")
    except Exception:
        return issues
    rel = str(f.relative_to(VAULT))
    body = strip_frontmatter(content)
    clean = strip_codeblocks_and_comments(body)

    # 先把完整 wikilink [[...]] 占位掉——剩下的 [[ / ]] 才是真损坏
    # 但先在占位前收集完整 wikilink 用于检查 3（短路径目标不存在）
    all_wikilinks = WIKILINK_RE.findall(clean)
    placeholdered = WIKILINK_RE.sub(_PLACEHOLDER, clean)

    # 1. 裸 ]] 无配对 [[（占位后还在的 ]] 就是真损坏）
    for m in BARE_CLOSE_RE.finditer(placeholdered):
        # 还原上下文：取占位后的前后各 30 字符
        start = max(0, m.start() - 30)
        end = min(len(placeholdered), m.end() + 10)
        ctx = placeholdered[start:end].replace(_PLACEHOLDER, "[[...]]")
        issues.append(("broken_wikilink", rel, ctx[:80]))

    # 2. 路径中间插入 [[（不需要占位——这是 wikilink 没被占位前就匹配的）
    for m in INSERTED_OPEN_RE.finditer(clean):
        issues.append(("inserted_brackets", rel, m.group(0)[:80]))

    # 3. 裸短路径 [[stem]] 目标不存在（在完整 wikilink 上检测）
    for target in all_wikilinks:
        target = target.split("|")[0].split("#")[0].strip()
        if not target or "/" in target:
            # 空目标（[[]]）或含路径分隔符的跳过
            continue
        if target.startswith("http") or "<" in target or target.startswith("#"):
            continue
        if not _resolve_short_link_stem(target):
            issues.append(("missing_target", rel, target))

    # 4. markdown 链接路径不存在
    for m in MD_LINK_RE.finditer(clean):
        path = m.group(2).strip()
        if path.startswith("http") or path.startswith("#") or path.startswith("mailto:"):
            continue
        clean_path = path.split("#")[0].split("?")[0].strip()
        if not clean_path:
            continue
        # 试 .md 或原路径
        if (VAULT / (clean_path + ".md")).exists():
            continue
        if (VAULT / clean_path).exists():
            continue
        # 相对当前文件目录解析
        try:
            rel_p = (f.parent / clean_path).resolve()
            if rel_p.exists():
                continue
        except Exception:
            pass
        issues.append(("broken_mdlink", rel, clean_path))

    # 5. 残片：[[ 无配对 ]]（占位后还在的 [[）
    for m in re.finditer(r"\[\[", placeholdered):
        start = max(0, m.start() - 10)
        end = min(len(placeholdered), m.end() + 40)
        ctx = placeholdered[start:end].replace(_PLACEHOLDER, "[[...]]")
        issues.append(("orphan_open", rel, ctx[:80]))

    return issues


def lint() -> list[tuple[str, str, str]]:
    """扫全 vault，返回所有问题。"""
    issues: list[tuple[str, str, str]] = []
    for f in VAULT.rglob("*.md"):
        if should_skip(f):
            continue
        issues.extend(lint_file(f))
    return issues


def main():
    ap = argparse.ArgumentParser(description="独立链接检查器——CI 第二只眼")
    ap.add_argument("--max-samples", type=int, default=20,
                    help="每类问题最多打印的样本数（默认 20）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 格式")
    ap.add_argument("--quiet", "-q", action="store_true", help="只输出统计")
    args = ap.parse_args()

    issues = lint()
    by_type = Counter(t for t, _, _ in issues)

    if args.json:
        out = {
            "total": len(issues),
            "by_type": dict(by_type.most_common()),
            "samples": [
                {"type": t, "file": f, "snippet": s}
                for t, f, s in issues[: args.max_samples]
            ],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"总问题: {len(issues)}")
        if by_type:
            print("分类:")
            for t, c in by_type.most_common():
                print(f"  {t}: {c}")
        if issues and not args.quiet:
            print(f"\n样本（前 {args.max_samples}）:")
            shown = 0
            seen_types: set[str] = set()
            for t, f, desc in issues:
                if t not in seen_types:
                    seen_types.add(t)
                    print(f"  [{t}]")
                if shown >= args.max_samples:
                    break
                print(f"    {desc[:60]}  ← {f}")
                shown += 1

    # CI 退出码：有问题 → 1
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
