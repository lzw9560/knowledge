#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1：实体词典初始化
================================================================

扫描 vault 的 `10_Reference/investing/` 下所有 .md 文件，读 frontmatter，
把 code/name/number/endpoint/action_id/rule_id/title 及文件名 stem 收为别名，
归一到对应的实体文件路径，输出到
`10_Reference/investing/.entity-dictionary.json`。

词典结构（对齐 docs/knowledge-graph-llm-pipeline.md §2）：

    {
      "aliases": {
        "600519":   {"path": "stocks/600519",   "type": "stock"},
        "贵州茅台": {"path": "stocks/600519",   "type": "stock"},
        "S007":     {"path": "specs/S007-契约层", "type": "spec"},
        "tencent":  {"path": "data-sources/tencent", "type": "data_source"},
        "腾讯行情": {"path": "data-sources/tencent", "type": "data_source"}
      },
      "by_type": {
        "stock":      ["600519", "000858", ...],
        "spec":       ["S007", "S008", ...],
        "data_source": ["tencent", "eastmoney-push2", ...]
      },
      "stats": { ... }
    }

规则
----
- 跳过 `templates/`、`reviews/`、`inbox/` 三个目录（模板 / 历史报告 / 待审实体）
- 跳过 `index.md` / `MOC.md` / `README.md` 等结构导航文件
- 别名 = frontmatter 的 code/name/number/title/endpoint/action_id/rule_id + 文件名 stem
- 规范标识符（by_type 列表元素）按优先级取：
  code > number > action_id > rule_id > file stem
- 同别名冲突（同字符串指向不同 path）：保留先入者，记录冲突，不改写
- 纯标准库，不依赖 PyYAML

用法：
    python3 scripts/init_entity_dictionary.py            # 在 vault 根目录下运行
    python3 scripts/init_entity_dictionary.py --root /path/to/vault
    python3 scripts/init_entity_dictionary.py --quiet
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────────────────────────────────

DEFAULT_VAULT_ROOT = Path(__file__).resolve().parent.parent
INVESTING_DIRNAME = "10_Reference/investing"
OUTPUT_FILENAME = ".entity-dictionary.json"

# 不扫描的子目录（模板 / 历史报告 / 待审 inbox）
EXCLUDE_DIRS = {"templates", "reviews", "inbox"}

# 结构导航文件名，跳过（不算实体）
STRUCTURAL_FILENAMES = {"index.md", "MOC.md", "README.md"}

# frontmatter 中承载"业务别名"的键（其余如 created/type/source 是元数据）
ALIAS_KEYS = (
    "code", "name", "number", "title",
    "endpoint", "action_id", "rule_id",
)

# 规范标识符优先级（by_type 列表用）—— 取第一个非空值
CANONICAL_KEY_PRIORITY = ("code", "number", "action_id", "rule_id")

# BEIJING_TZ = timezone(timedelta(hours=8))  # 预留，created 字段写入用

# ──────────────────────────────────────────────────────────────────────────
# YAML frontmatter 解析（纯正则，不依赖 PyYAML）—— 与 vault_audit.py 同款实现
# ──────────────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
KV_LINE_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")


def parse_frontmatter(text: str) -> "OrderedDict[str, str]":
    """从 markdown 文本解析 YAML frontmatter（扁平 key:value）。

    - 不处理嵌套 mapping / 多行 list（vault 实体 frontmatter 全是扁平标量）
    - 值去两端引号；"true"/"false" 转布尔；空值保留为 ""
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return OrderedDict()
    fm: "OrderedDict[str, str]" = OrderedDict()
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        kv = KV_LINE_RE.match(line)
        if not kv:
            continue
        key = kv.group(1).strip()
        val = kv.group(2).strip()
        # 去两端配对引号
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        fm[key] = val
    return fm


# ──────────────────────────────────────────────────────────────────────────
# 收集实体
# ──────────────────────────────────────────────────────────────────────────


def collect_entity_files(investing_dir: Path) -> list[Path]:
    """返回 investing_dir 下所有应纳入词典的 .md 文件（已排序）。

    排除：EXCLUDE_DIRS 下的文件 / STRUCTURAL_FILENAMES。
    """
    files: list[Path] = []
    for path in sorted(investing_dir.rglob("*.md")):
        rel = path.relative_to(investing_dir)
        parts = rel.parts
        # 跳过 templates/ reviews/ inbox/
        if any(parts[0] == excl for excl in EXCLUDE_DIRS):
            continue
        # 跳过 index.md / MOC.md / README.md
        if path.name in STRUCTURAL_FILENAMES:
            continue
        files.append(path)
    return files


def compute_rel_path(path: Path, investing_dir: Path) -> str:
    """返回相对 investing_dir 的 POSIX 路径（去掉 .md 后缀），如 stocks/600519。

    这是词典 `path` 字段格式，与 [[链接]] 目标（[[stocks/600519]]）对齐。
    """
    rel = path.relative_to(investing_dir)
    # 去掉 .md 后缀 → 与 [[wikilink]] 目标格式一致
    return rel.with_suffix("").as_posix()


def extract_aliases(fm: dict, file_stem: str) -> list[str]:
    """从 frontmatter 提取候选别名列表（已去重，保序）。

    别名来源：
      1. 文件名 stem（始终纳入，是 [[链接]] 的主目标）
      2. frontmatter ALIAS_KEYS 中的非空值
    """
    aliases: list[str] = []
    seen: set[str] = set()

    def add(val):
        if not val:
            return
        val = val.strip()
        if not val or val.lower() in ("待补", "待实时", "待实时更新", "待核实", "待灌入"):
            return
        if val in seen:
            return
        seen.add(val)
        aliases.append(val)

    # 文件名 stem 优先（链接主目标）
    add(file_stem)
    for key in ALIAS_KEYS:
        if key in fm:
            add(fm[key])
    return aliases


def compute_canonical_id(fm: dict, file_stem: str) -> str:
    """计算规范标识符（by_type 列表元素），按优先级取第一个非空值。"""
    for key in CANONICAL_KEY_PRIORITY:
        val = fm.get(key, "").strip()
        if val and val.lower() not in ("待补", "待实时", "待实时更新", "待核实", "待灌入"):
            return val
    return file_stem


# ──────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────


def build_dictionary(vault_root: Path) -> dict:
    """扫描 investing_dir，构建实体词典。返回 dict 含 aliases/by_type/stats。"""
    investing_dir = vault_root / INVESTING_DIRNAME
    if not investing_dir.is_dir():
        raise SystemExit(f"investing dir 不存在：{investing_dir}")

    files = collect_entity_files(investing_dir)

    aliases: "OrderedDict[str, dict]" = OrderedDict()
    by_type: dict[str, list[str]] = defaultdict(list)
    conflicts: list[dict] = []
    skipped_no_type: list[str] = []

    alias_count = 0
    entity_count = 0
    type_counts: dict[str, int] = defaultdict(int)
    type_to_files: dict[str, list[str]] = defaultdict(list)

    for path in files:
        rel_path = compute_rel_path(path, investing_dir)
        file_stem = path.stem

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")

        fm = parse_frontmatter(text)
        entity_type = str(fm.get("type", "")).strip()

        if not entity_type:
            skipped_no_type.append(rel_path)
            continue

        entity_count += 1
        type_counts[entity_type] += 1
        type_to_files[entity_type].append(rel_path)

        canonical_id = compute_canonical_id(fm, file_stem)
        # by_type 去重（同 canonical_id 多实体时，保留首次出现）
        if canonical_id not in by_type[entity_type]:
            by_type[entity_type].append(canonical_id)

        entity_aliases = extract_aliases(fm, file_stem)
        for alias in entity_aliases:
            if alias in aliases:
                # 冲突：同别名已映射到另一 path
                existing = aliases[alias]
                if existing["path"] != rel_path:
                    conflicts.append({
                        "alias": alias,
                        "existing_path": existing["path"],
                        "existing_type": existing["type"],
                        "new_path": rel_path,
                        "new_type": entity_type,
                    })
                # 不论是否冲突，跳过改写（first-write-wins）
                continue
            aliases[alias] = {"path": rel_path, "type": entity_type}
            alias_count += 1

    # by_type 排序：每类内按字母/数字升序
    by_type_sorted: "OrderedDict[str, list[str]]" = OrderedDict()
    for t in sorted(by_type.keys()):
        by_type_sorted[t] = sorted(by_type[t])

    stats = {
        "entity_count": entity_count,
        "alias_count": alias_count,
        "type_counts": dict(sorted(type_counts.items())),
        "conflict_count": len(conflicts),
        "skipped_no_type_count": len(skipped_no_type),
        "skipped_no_type": sorted(skipped_no_type),
        "generated_at": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S %z"),
    }

    return {
        "aliases": aliases,
        "by_type": by_type_sorted,
        "stats": stats,
        "conflicts": conflicts,
    }


def write_dictionary(dictionary: dict, output_path: Path) -> None:
    """以 UTF-8 + 缩进 2 写 JSON。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(dictionary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="初始化 vault 实体词典（.entity-dictionary.json）",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_VAULT_ROOT,
        help="vault 根目录（默认：脚本上两级目录）",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="不打印摘要到 stdout",
    )
    args = parser.parse_args(argv)

    vault_root = args.root.resolve()
    investing_dir = vault_root / INVESTING_DIRNAME
    if not investing_dir.is_dir():
        print(f"[ERROR] investing dir 不存在：{investing_dir}", file=sys.stderr)
        return 2

    output_path = investing_dir / OUTPUT_FILENAME
    dictionary = build_dictionary(vault_root)
    write_dictionary(dictionary, output_path)

    if not args.quiet:
        stats = dictionary["stats"]
        print(f"[OK] 实体词典已写入：{output_path}")
        print(f"     实体总数：{stats['entity_count']}")
        print(f"     别名总数：{stats['alias_count']}")
        print(f"     类型分布：")
        for t, n in stats["type_counts"].items():
            print(f"       - {t}: {n}")
        if stats["conflict_count"]:
            print(f"     ⚠ 冲突别名：{stats['conflict_count']} 条（first-write-wins，见 JSON conflicts 字段）")
        if stats["skipped_no_type_count"]:
            print(f"     ⚠ 无 type 字段跳过：{stats['skipped_no_type_count']} 个文件")
            for p in stats["skipped_no_type"][:10]:
                print(f"       - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
