#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2：spec 批量抽取脚本
================================================================

从 Vibe-Research 仓 `specs/README.md` 的 spec 索引表（S001-S166），
为每个 spec 提取编号 / 标题 / 状态 / 一句话摘要，对 vault 的
`10_Reference/investing/specs/` 目录补齐尚未落地的 spec stub 文件。

规则
----
- 输入：`Vibe-Research/specs/README.md` 中的 Markdown 表格行
- 对每个 spec：检查 vault specs/ 是否已有该编号的 .md（按编号前缀匹配，
  S007 → S007-*.md / S007.md）→ 已有则跳过
- 没有 → 用 `templates/spec.md` 的 frontmatter 建 stub 文件，
  文件名 = `SNNN-标题.md`（与已有 stub 对齐）
- 幂等：重跑只补缺失，不覆盖已有
- 纯标准库

用法：
    python3 scripts/extract_specs.py                    # 默认路径
    python3 scripts/extract_specs.py --vibe-research /path/to/Vibe-Research
    python3 scripts/extract_specs.py --vault /path/to/vault
    python3 scripts/extract_specs.py --dry-run          # 只打印不写
    python3 scripts/extract_specs.py --quiet
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────────────────────────────────

DEFAULT_VAULT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VIBE_RESEARCH = Path("/Users/lizhiwei/project/code/stock/Vibe-Research")
INVESTING_DIRNAME = "10_Reference/investing"
SPECS_SUBDIR = "specs"
TEMPLATES_SUBDIR = "templates"
SPEC_TEMPLATE_NAME = "spec.md"
README_REL = "specs/README.md"

# README 表格行正则（Markdown 表格行）
# 示例：| [S001](S001-fix-chat-env-llm-config/spec.md) | 修复 chat... | ✅已实现 2026-07-29 | spec | 补全... |
# 第二列单元格格式：[SNNN](路径) 或裸 SNNN
TABLE_ROW_RE = re.compile(
    r"^\|\s*\[?(S\d{3})\]?\s*\(([^)]*)\)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)
# 备用：无链接的纯编号行（极少，但 README 末尾注释行可能匹配）
TABLE_ROW_BARE_RE = re.compile(
    r"^\|\s*(S\d{3})\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)

# Spec 编号正则（从 spec 子目录名提取纯编号）
SPEC_NUM_RE = re.compile(r"^(S\d{3})")

# spec 子目录名（如 "S001-fix-chat-env-llm-config"）→ 去编号留标题 slug
# 注意：标题含中文，直接取编号后剩余部分（去掉首段 "-" 分隔）
SPEC_TITLE_SLUG_RE = re.compile(r"^S\d{3}[-_]\s*(.+?)\s*$")

# 状态归一映射（README 的多种状态写法 → frontmatter 标准值）
# 模板 frontmatter 标准状态：草案 / 已通过 / 实现中 / 已实现(日期) / 已废弃
STATUS_CANONICAL_MAP = {
    # ✅ 已实现
    "✅已实现": "已实现",
    "✅ phase 1 已实现": "已实现",
    "✅p1 已实现": "已实现",
    "✅已实现 2026-08-01": "已实现",
    # 🟡 草案 / 进行中
    "🟡草案": "草案",
    "🟡phase 0-3 主体完成": "实现中",
    # 🗑️ 废弃
    "🗑️已废弃": "已废弃",
}

BEIJING_TZ = timezone(timedelta(hours=8))


# ──────────────────────────────────────────────────────────────────────────
# 解析 README spec 索引表
# ──────────────────────────────────────────────────────────────────────────


def parse_status(raw_status: str) -> str:
    """把 README 表格里的状态写法归一为 vault frontmatter 标准值。

    - ✅... → 已实现
    - 🟡... → 草案（若含"进行"/"完成"则实现中）
    - 🗑️... → 已废弃
    - 其余 → 原值截断到 20 字符
    """
    s = raw_status.strip()
    if s.startswith("✅"):
        return "已实现"
    if s.startswith("🟡"):
        if "完成" in s or "进行" in s:
            return "实现中"
        return "草案"
    if s.startswith("🗑️"):
        return "已废弃"
    # 截断
    return s[:20] if len(s) > 20 else s


def clean_title(raw_title: str) -> str:
    """清洗 spec 标题（去掉中英混合多余的空格 / 制表符）。"""
    title = raw_title.strip()
    # 去掉内部多余空白
    title = re.sub(r"\s+", " ", title)
    return title


def extract_slug_from_path(rel_path: str, spec_number: str) -> str:
    """从 README 链接路径提取标题 slug。

    示例：
      "S001-fix-chat-env-llm-config/spec.md" → "fix-chat-env-llm-config"
      "S007-契约层/spec.md" → "契约层"
      "archive/m3-strategy/S068-工作流触发与结算正确性/spec.md" → "工作流触发与结算正确性"
      "S102-战法卡片历史战绩/spec.md" → "战法卡片历史战绩"
    """
    # 取最后一段目录名（split by /，去 spec.md）
    parts = [p for p in rel_path.split("/") if p and not p.endswith(".md")]
    if not parts:
        return ""
    dir_name = parts[-1]
    # 去编号前缀
    m = SPEC_TITLE_SLUG_RE.match(dir_name)
    if m:
        return m.group(1).strip()
    # fallback：直接去掉编号前缀
    if dir_name.startswith(spec_number):
        rest = dir_name[len(spec_number):]
        return rest.lstrip("-_").strip()
    return dir_name


def parse_readme(readme_text: str) -> list[dict]:
    """解析 README，返回 spec 记录列表。

    每条记录字段：
      number: "S007"
      title:  "契约层（数据模型+回归基线+契约测试骨架）"
      status_raw: "✅已实现 2026-08-01"
      status:    "已实现"           (归一后)
      summary:   "Pydantic v2 7 模型 + ..."
      subdocs:   "spec · plan · tasks"  (子文档列)
      source_path: "S007-契约层/spec.md"  (README 链接路径)
      title_slug: "契约层"          (从 source_path 提取)
    """
    records = []
    for line in readme_text.splitlines():
        line = line.rstrip()
        if not line.startswith("|"):
            continue
        # 跳过表头分隔行 |---|---|
        if re.match(r"^\|[\s\-:|]+\|\s*$", line):
            continue
        # 跳过表头行（| 编号 | 标题 | ...）
        if "编号" in line and "标题" in line:
            continue

        m = TABLE_ROW_RE.match(line)
        if m:
            number = m.group(1)
            source_path = m.group(2)
            title = clean_title(m.group(3))
            status_raw = m.group(4).strip()
            subdocs = m.group(5).strip()
            summary = m.group(6).strip()
        else:
            mb = TABLE_ROW_BARE_RE.match(line)
            if not mb:
                continue
            number = mb.group(1)
            source_path = ""
            title = clean_title(mb.group(2))
            status_raw = mb.group(3).strip()
            subdocs = mb.group(4).strip()
            summary = mb.group(5).strip()

        # 过滤掉非 spec 编号行（如 "SNNN" 占位）
        if not re.match(r"^S\d{3}$", number):
            continue

        records.append({
            "number": number,
            "title": title,
            "status_raw": status_raw,
            "status": parse_status(status_raw),
            "summary": summary,
            "subdocs": subdocs,
            "source_path": source_path,
            "title_slug": extract_slug_from_path(source_path, number),
        })
    return records


# ──────────────────────────────────────────────────────────────────────────
# 检查 vault specs/ 已有的 spec 编号集合
# ──────────────────────────────────────────────────────────────────────────


def existing_spec_numbers(specs_dir: Path) -> dict[str, Path]:
    """扫描 vault specs/ 目录，返回 {spec_number: file_path} 映射。

    匹配规则：文件名以 `SNNN-` 或 `SNNN.` 开头（如 S007-契约层.md / S007.md）。
    """
    result: dict[str, Path] = {}
    if not specs_dir.is_dir():
        return result
    for path in sorted(specs_dir.glob("S*.md")):
        m = SPEC_NUM_RE.match(path.stem)
        if m:
            number = m.group(1)
            # 不覆盖已有的（若同编号多文件，保留首个）
            if number not in result:
                result[number] = path
    return result


# ──────────────────────────────────────────────────────────────────────────
# Stub 文件生成
# ──────────────────────────────────────────────────────────────────────────


def build_stub_filename(number: str, title_slug: str) -> str:
    """生成 stub 文件名：SNNN-标题.md。

    title_slug 为空时退化为 SNNN.md。
    """
    slug = title_slug.strip()
    # 去掉文件名不安全字符（保留中文 / 字母 / 数字 / - _）
    slug = re.sub(r"[\\/:*?\"<>|]", "-", slug)
    if slug:
        return f"{number}-{slug}.md"
    return f"{number}.md"


def build_stub_content(record: dict, today_str: str) -> str:
    """生成 stub markdown 内容（对齐 templates/spec.md 结构 + 已有 stub 风格）。

    frontmatter 字段：type / number / title / status / created
    正文段：问题/目标 / 摘要 / 关联（链回 Vibe-Research 源文件）
    """
    number = record["number"]
    title = record["title"]
    status = record["status"]
    summary = record["summary"]
    source_path = record["source_path"]

    # 源文件路径：README 链接路径若以 archive/ 开头则保留，否则原样
    if source_path:
        source_full = f"specs/{source_path}"
    else:
        source_full = f"specs/{number}/spec.md"

    fm_lines = [
        "---",
        f"type: spec",
        f"number: {number}",
        f"title: {title}",
        f"status: {status}",
        f"created: {today_str}",
        "---",
        "",
        f"# {number} {title}",
        "",
        "## 摘要",
        "",
        summary if summary else "（待补）",
        "",
        "## 问题/目标",
        "",
        f"> 此 spec 为 P2 pipeline 从 `specs/README.md` 自动生成的 stub，待人工补充正文。",
        "",
        "## 关联",
        "",
        f"- 源文件：`{source_full}`（Vibe-Research 仓）",
        f"- README 索引：`specs/README.md`",
        f"- 子文档：{record['subdocs']}" if record["subdocs"] else "",
        "- 数据源：[[data-sources/]]",
        "- 战法：[[strategies/]]",
        "",
    ]
    # 去掉空行项（subdocs 为空时）
    content = "\n".join(line for line in fm_lines if line is not None)
    return content


# ──────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────


def run(
    vault_root: Path,
    vibe_research_root: Path,
    dry_run: bool = False,
    quiet: bool = False,
) -> int:
    specs_dir = vault_root / INVESTING_DIRNAME / SPECS_SUBDIR
    readme_path = vibe_research_root / README_REL

    if not readme_path.is_file():
        print(f"[ERROR] 找不到 README：{readme_path}", file=sys.stderr)
        return 2
    if not specs_dir.is_dir():
        print(f"[ERROR] vault specs 目录不存在：{specs_dir}", file=sys.stderr)
        return 2

    readme_text = readme_path.read_text(encoding="utf-8")
    records = parse_readme(readme_text)

    existing = existing_spec_numbers(specs_dir)

    created: list[Path] = []
    skipped_existing: list[str] = []
    today_str = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")

    for record in records:
        number = record["number"]
        if number in existing:
            skipped_existing.append(number)
            continue
        filename = build_stub_filename(number, record["title_slug"])
        target = specs_dir / filename
        # 若同编号但不同文件名（极少），也跳过
        if target.exists():
            skipped_existing.append(number)
            continue
        content = build_stub_content(record, today_str)
        if dry_run:
            created.append(target)
            if not quiet:
                print(f"[DRY-RUN] 将创建：{target.relative_to(vault_root)}")
        else:
            target.write_text(content, encoding="utf-8")
            created.append(target)
            if not quiet:
                print(f"[CREATED] {target.relative_to(vault_root)}")

    if not quiet:
        print("")
        print(f"README 共解析 spec：{len(records)} 条")
        print(f"已有跳过：{len(skipped_existing)} 条")
        print(f"新建 stub：{len(created)} 条")
        if dry_run:
            print("(dry-run 模式，未写文件)")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="从 Vibe-Research specs/README.md 批量抽取 spec 实体到 vault",
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=DEFAULT_VAULT_ROOT,
        help="vault 根目录（默认：脚本上两级目录）",
    )
    parser.add_argument(
        "--vibe-research",
        type=Path,
        default=DEFAULT_VIBE_RESEARCH,
        help="Vibe-Research 项目根目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要创建的文件，不实际写入",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="不打印进度",
    )
    args = parser.parse_args(argv)

    vault_root = args.vault.resolve()
    vibe_root = args.vibe_research.resolve()

    return run(vault_root, vibe_root, dry_run=args.dry_run, quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
