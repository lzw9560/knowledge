#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P5：增量同步脚本
================================================

监听 Vibe-Research git commit，按变更文件类型分流到 P1-P4 的对应抽取
脚本，增量更新 vault `10_Reference/investing/` 实体。

实现（纯标准库 + 子进程调 git / 兄弟脚本）
----
1. `git -C <Vibe-Research> log --since="<窗口>" --name-only --oneline`
   取最近窗口内的变更文件清单（默认窗口 "7 days ago"）
2. 按类型分流：
   - `specs/SNNN-*/*.md` 变更 → 调 `extract_specs.py` 重抽该 spec stub
   - `backend/strategies/cards/*.md` 变更 → 标记 strategies/ 对应文件待同步
   - `backend/data/sources/*.py` 变更 → 调 `extract_relations.py` 重抽关系
   - `ARCHITECTURE.md` 变更 → 调 `extract_relations.py` 重抽数据流
   - `backend/models/*.py` 变更 → 调 `extract_code_schema.py` 重抽 schema
3. 对比已有 vault 实体，只更新变更部分（下游脚本本身幂等，重跑只补缺失）
4. 在已更新实体的 frontmatter 加 `last_synced` 字段记录同步时间
5. 生成同步报告 `docs/sync-report-YYYY-MM-DD.md`

冲突处理（设计文档 P5）
----
同一实体被多个源抽取时，优先级：spec > 代码 AST > 文档注释 > LLM 推断。
本脚本调用下游脚本时按此优先级顺序执行——后执行的不覆盖高优先级内容
（下游脚本本身做幂等 + 缺失才补）。

用法：
    python3 scripts/incremental_sync.py
    python3 scripts/incremental_sync.py --since "7 days ago"
    python3 scripts/incremental_sync.py --since "1 day ago" --quiet
    python3 scripts/incremental_sync.py --vibe-research /path/to/Vibe-Research
    python3 scripts/incremental_sync.py --vault /path/to/vault
    python3 scripts/incremental_sync.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────────────────────────────────

DEFAULT_VAULT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VIBE_RESEARCH = Path("/Users/lizhiwei/project/code/stock/Vibe-Research")
INVESTING_DIRNAME = "10_Reference/investing"
DOCS_SUBDIR = "docs"
SPECS_SUBDIR = "specs"
STRATEGIES_SUBDIR = "strategies"
DATA_SOURCES_SUBDIR = "data-sources"

# 兄弟脚本（P1-P4）
SCRIPTS_SUBDIR = "scripts"
EXTRACT_SPECS_SCRIPT = "extract_specs.py"
EXTRACT_CODE_SCHEMA_SCRIPT = "extract_code_schema.py"
EXTRACT_RELATIONS_SCRIPT = "extract_relations.py"

BEIJING_TZ = timezone(timedelta(hours=8))

# 默认同步窗口
DEFAULT_SINCE = "7 days ago"

# 变更文件分类正则（相对 Vibe-Research 仓根）
# spec 文件：specs/ 下任意 SNNN 目录的 .md（含 spec.md / plan.md / tasks.md）
SPEC_FILE_RE = re.compile(r"^specs/(?:archive/)?(?:m\d+-[^/]+/)?S\d{3}[^/]*/.+\.md$")
# 战法卡：backend/strategies/cards/*.md
STRATEGY_CARD_RE = re.compile(r"^backend/strategies/cards/[^/]+\.md$")
# 数据源模块：backend/data/sources/*.py
DATA_SOURCE_PY_RE = re.compile(r"^backend/data/sources/[^/]+\.py$")
# Pydantic 模型：backend/models/*.py
MODEL_PY_RE = re.compile(r"^backend/models/[^/]+\.py$")
# 架构文档
ARCH_FILE_RE = re.compile(r"^ARCHITECTURE\.md$")
# spec README（索引表）
SPEC_README_RE = re.compile(r"^specs/README\.md$")

# vault spec frontmatter last_synced 字段
LAST_SYNCED_KEY = "last_synced"
FM_LINE_RE = re.compile(r"^---\s*$", re.MULTILINE)

# ──────────────────────────────────────────────────────────────────────────
# git 变更文件抓取
# ──────────────────────────────────────────────────────────────────────────


def run_git(args: list[str], cwd: Path, quiet: bool = True) -> tuple[int, str, str]:
    """跑 git 子进程，返 (returncode, stdout, stderr)。"""
    full_args = ["git", "-C", str(cwd)] + args
    try:
        proc = subprocess.run(
            full_args,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return (1, "", str(e))
    return (proc.returncode, proc.stdout, proc.stderr)


def get_changed_files(vibe_root: Path, since: str, quiet: bool = True) -> list[str]:
    """取最近窗口内变更的文件清单（去重）。

    用 `git log --since=<since> --name-only --oneline --pretty=format:`，
    取每个 commit 的 name-only 输出，去重 + 去空行 + 去删除文件（"D\t前缀"）。
    """
    rc, out, err = run_git(
        ["log", f"--since={since}", "--name-only", "--pretty=format:", "--no-renames"],
        vibe_root, quiet=quiet,
    )
    if rc != 0:
        if not quiet:
            print(f"[WARN] git log 失败：{err.strip()}", file=sys.stderr)
        return []

    files: set[str] = set()
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        # git --name-only 在有状态标记时格式如 "M\tpath" / "D\tpath" / "A\tpath"
        # 无标记时纯路径
        if "\t" in line:
            status, path = line.split("\t", 1)
            # 跳过删除文件（已不存在，无法重抽）
            if status == "D":
                continue
            files.add(path.strip())
        else:
            files.add(line)

    return sorted(files)


def classify_changes(changed_files: list[str]) -> dict[str, list[str]]:
    """把变更文件按类型分流。

    返回 {
      'specs': [...],           # spec 子目录 .md（触发 extract_specs.py）
      'spec_readme': [...],     # specs/README.md（触发 extract_specs.py 全量）
      'strategy_cards': [...],  # 战法卡 .md
      'data_source_py': [...],  # 数据源 .py
      'model_py': [...],        # Pydantic 模型 .py
      'architecture': [...],    # ARCHITECTURE.md
      'other': [...],           # 其他（不触发任何下游脚本）
    }
    """
    classified: dict[str, list[str]] = {
        "specs": [],
        "spec_readme": [],
        "strategy_cards": [],
        "data_source_py": [],
        "model_py": [],
        "architecture": [],
        "other": [],
    }
    for f in changed_files:
        if SPEC_README_RE.match(f):
            classified["spec_readme"].append(f)
        elif SPEC_FILE_RE.match(f):
            classified["specs"].append(f)
        elif STRATEGY_CARD_RE.match(f):
            classified["strategy_cards"].append(f)
        elif DATA_SOURCE_PY_RE.match(f):
            classified["data_source_py"].append(f)
        elif MODEL_PY_RE.match(f):
            classified["model_py"].append(f)
        elif ARCH_FILE_RE.match(f):
            classified["architecture"].append(f)
        else:
            classified["other"].append(f)
    return classified


# ──────────────────────────────────────────────────────────────────────────
# 下游脚本调度
# ──────────────────────────────────────────────────────────────────────────


def run_sibling_script(
    script_name: str,
    vault_root: Path,
    vibe_root: Path,
    extra_args: list[str] | None = None,
    capture_summary: bool = True,
    quiet: bool = True,
) -> tuple[bool, str]:
    """跑兄弟脚本（P1-P4），返 (success, 输出)。

    脚本路径 = vault/scripts/<script_name>。传 --vault + --vibe-research。
    capture_summary=True 时不传 --quiet 给下游脚本，以便捕获其 stdout 摘要
    用于同步报告。P5 自身 quiet 时丢弃 stdout（只返末行）。
    """
    script_path = vault_root / SCRIPTS_SUBDIR / script_name
    if not script_path.is_file():
        return (False, f"脚本不存在：{script_path}")

    cmd = [
        sys.executable,
        str(script_path),
        "--vault", str(vault_root),
        "--vibe-research", str(vibe_root),
    ]
    # 捕获摘要时不静默下游；否则静默
    if not capture_summary:
        cmd.append("--quiet")
    if extra_args:
        cmd.extend(extra_args)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return (False, f"执行失败：{e}")

    success = proc.returncode == 0
    output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    return (success, output)


# ──────────────────────────────────────────────────────────────────────────
# 增量更新：战法卡同步
# ──────────────────────────────────────────────────────────────────────────


def sync_strategy_cards(
    changed_cards: list[str],
    vibe_root: Path,
    vault_root: Path,
    dry_run: bool,
    quiet: bool,
) -> list[str]:
    """同步变更的战法卡 → vault strategies/。

    简化策略：战法卡 frontmatter 由 P1-P3 未单独脚本抽取（strategies/ 已
    手工灌入 12 卡），本步只对变更的卡文件刷新 last_synced + 标记待人工核对。
    不做全量重抽（战法卡变更频率低，人工核对成本可接受）。

    返回更新的 vault strategies/ 文件名列表。
    """
    if not changed_cards:
        return []
    strategies_dir = vault_root / INVESTING_DIRNAME / STRATEGIES_SUBDIR
    if not strategies_dir.is_dir():
        return []

    updated: list[str] = []
    for card_path in changed_cards:
        # backend/strategies/cards/<slug>.md → strategies/<slug>.md
        slug = Path(card_path).stem
        vault_card = strategies_dir / f"{slug}.md"
        if not vault_card.is_file():
            # vault 无对应战法卡——记入待补（不在此创建）
            if not quiet:
                print(f"[SKIP] vault 无对应战法卡：{slug}（待人工补）")
            continue
        # 刷新 last_synced（frontmatter 追加字段）
        if update_last_synced(vault_card, dry_run=dry_run):
            updated.append(vault_card.name)
            if not quiet:
                tag = "[DRY-RUN] " if dry_run else ""
                print(f"{tag}刷新 last_synced：strategies/{vault_card.name}")
    return updated


# ──────────────────────────────────────────────────────────────────────────
# last_synced frontmatter 字段
# ──────────────────────────────────────────────────────────────────────────


def update_last_synced(file_path: Path, dry_run: bool = False) -> bool:
    """在 vault 实体文件 frontmatter 加/更新 last_synced 字段。

    返回是否实际改写。幂等：已存在且值相同则跳过。
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return False

    if not text.startswith("---"):
        return False  # 无 frontmatter，不动

    # 找第二个 ---
    second = text.find("\n---", 3)
    if second == -1:
        return False
    fm_end = second + 4  # 含 \n---
    fm_text = text[:fm_end]

    today_str = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")
    today_iso = datetime.now(BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    # 已有 last_synced 字段？
    pattern = re.compile(
        r"^(?P<key>last_synced)\s*:\s*(?P<val>.+?)\s*$",
        re.MULTILINE,
    )
    m = pattern.search(fm_text)
    if m:
        # 已存在——只刷新日期部分（保留原格式：若原是 date 就更新 date）
        old_val = m.group("val").strip()
        # 去引号
        old_val_stripped = old_val.strip("'\"")
        if old_val_stripped == today_str or old_val_stripped == today_iso:
            return False  # 今日已同步，跳过
        # 替换值（保持原引号风格）
        new_val = today_str
        if old_val.startswith("'") or old_val.startswith('"'):
            quote = old_val[0]
            new_val = f"{quote}{today_str}{quote}"
        new_fm = fm_text[:m.start("val")] + new_val + fm_text[m.end("val"):]
    else:
        # 不存在——在 frontmatter 末尾（第二个 --- 前）追加
        # fm_text 末尾形如 "...\n---"
        insert_before = fm_text.rfind("\n---")
        if insert_before == -1:
            return False
        new_line = f"\nlast_synced: {today_str}"
        new_fm = fm_text[:insert_before] + new_line + fm_text[insert_before:]

    new_text = new_fm + text[fm_end:]
    if dry_run:
        return True

    file_path.write_text(new_text, encoding="utf-8")
    return True


# ──────────────────────────────────────────────────────────────────────────
# 同步报告
# ──────────────────────────────────────────────────────────────────────────


def write_sync_report(
    docs_dir: Path,
    since: str,
    changed_files: list[str],
    classified: dict[str, list[str]],
    actions: list[dict],
    today_str: str,
    dry_run: bool,
) -> Path:
    """生成 docs/sync-report-YYYY-MM-DD.md。"""
    docs_dir.mkdir(parents=True, exist_ok=True)
    report_name = f"sync-report-{today_str}.md"
    report_path = docs_dir / report_name

    total_changed = len(changed_files)
    triggered = sum(len(v) for k, v in classified.items() if k != "other")
    skipped = len(classified["other"])

    lines: list[str] = [
        "---",
        f"type: sync-report",
        f"date: {today_str}",
        f"window: \"{since}\"",
        "---",
        "",
        f"# 增量同步报告（{today_str}）",
        "",
        f"> P5 `incremental_sync.py` 生成。同步窗口：`{since}`。",
        "",
        "## 摘要",
        "",
        f"- 变更文件总数：**{total_changed}** 个",
        f"- 触发抽取的文件：**{triggered}** 个",
        f"- 未分类（跳过）：**{skipped}** 个",
        f"- 执行动作：**{len(actions)}** 次",
        "",
        "## 变更文件分类",
        "",
        f"| 类型 | 数量 | 触发动作 |",
        f"|---|---|---|",
        f"| spec 文件（specs/SNNN-*/*.md） | {len(classified['specs'])} | 调 `extract_specs.py` 重抽 stub |",
        f"| spec README | {len(classified['spec_readme'])} | 调 `extract_specs.py` 全量补缺失 |",
        f"| 战法卡（backend/strategies/cards/*.md） | {len(classified['strategy_cards'])} | 刷新 `last_synced` + 标待核对 |",
        f"| 数据源 .py（backend/data/sources/*.py） | {len(classified['data_source_py'])} | 调 `extract_relations.py` 重抽关系 |",
        f"| Pydantic 模型（backend/models/*.py） | {len(classified['model_py'])} | 调 `extract_code_schema.py` 重抽 schema |",
        f"| ARCHITECTURE.md | {len(classified['architecture'])} | 调 `extract_relations.py` 重抽数据流 |",
        f"| 其他（未分类） | {len(classified['other'])} | — |",
        "",
    ]

    # 各类文件清单（前 10 条，超出折叠）
    lines.append("## 变更文件清单")
    lines.append("")
    for kind, label in [
        ("specs", "spec 文件"),
        ("spec_readme", "spec README"),
        ("strategy_cards", "战法卡"),
        ("data_source_py", "数据源 .py"),
        ("model_py", "Pydantic 模型"),
        ("architecture", "架构文档"),
        ("other", "其他"),
    ]:
        files = classified.get(kind, [])
        if not files:
            continue
        lines.append(f"### {label}（{len(files)} 个）")
        lines.append("")
        for f in files[:10]:
            lines.append(f"- `{f}`")
        if len(files) > 10:
            lines.append(f"- ...（省略 {len(files) - 10} 个）")
        lines.append("")

    # 执行动作
    lines.append("## 执行动作")
    lines.append("")
    if actions:
        lines.append("| # | 脚本 | 触发原因 | 成功 | 输出摘要 |")
        lines.append("|---|---|---|---|---|")
        for i, a in enumerate(actions, 1):
            success_mark = "✅" if a["success"] else "❌"
            summary = a["summary"].replace("\n", " ").strip()[:80]
            lines.append(f"| {i} | `{a['script']}` | {a['reason']} | {success_mark} | {summary} |")
    else:
        lines.append("（无下游脚本被触发——变更文件均为未分类或 dry-run）")
    lines.append("")

    # 冲突处理
    lines.append("## 冲突处理")
    lines.append("")
    lines.append("同一实体被多个源抽取时，优先级：spec > 代码 AST > 文档注释 > LLM 推断。")
    lines.append("本脚本按此优先级顺序调用下游脚本——后执行的不覆盖高优先级内容（下游脚本幂等 + 只补缺失）。")
    lines.append("")

    if dry_run:
        lines.append("> ⚠️ dry-run 模式，未实际写入任何文件。")
    else:
        lines.append("> 所有下游脚本幂等，重跑安全。`last_synced` 字段记录同步时间。")

    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ──────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────


def run(
    vault_root: Path,
    vibe_root: Path,
    since: str = DEFAULT_SINCE,
    dry_run: bool = False,
    quiet: bool = False,
) -> int:
    docs_dir = vault_root / DOCS_SUBDIR
    today_str = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")

    # 校验 Vibe-Research 是 git 仓
    if not (vibe_root / ".git").is_dir() and not (vibe_root / ".git").is_file():
        print(f"[ERROR] {vibe_root} 不是 git 仓库", file=sys.stderr)
        return 2

    # ── 1. 取变更文件 ──
    changed = get_changed_files(vibe_root, since, quiet=quiet)
    if not changed:
        if not quiet:
            print(f"窗口 {since} 内无变更文件，同步结束。")
        # 仍生成空报告（记录同步跑了）
        classified_empty: dict[str, list[str]] = {
            "specs": [], "spec_readme": [], "strategy_cards": [],
            "data_source_py": [], "model_py": [], "architecture": [], "other": [],
        }
        if not dry_run:
            write_sync_report(
                docs_dir, since, changed, classified_empty, [], today_str, dry_run,
            )
        return 0

    # ── 2. 分类 ──
    classified = classify_changes(changed)

    actions: list[dict] = []

    # ── 3. 按优先级分流（spec > 代码 AST > 文档注释） ──

    # 3a. spec 变更 → extract_specs.py（重抽 stub，幂等只补缺失）
    spec_files = classified["specs"] + classified["spec_readme"]
    if spec_files:
        # extract_specs.py 没有单 spec 重抽参数（它扫 README 全量补缺失），
        # 故直接调全量——幂等，已有 stub 不覆盖
        success, output = run_sibling_script(
            EXTRACT_SPECS_SCRIPT, vault_root, vibe_root,
            capture_summary=True, quiet=quiet,
        )
        # 取输出末行作摘要（下游 stdout 含摘要行）
        summary = output.strip().split("\n")[-1] if output.strip() else ""
        actions.append({
            "script": EXTRACT_SPECS_SCRIPT,
            "reason": f"{len(spec_files)} 个 spec 文件变更",
            "success": success,
            "summary": summary,
        })
        if not quiet:
            tag = "✅" if success else "❌"
            print(f"{tag} 调 {EXTRACT_SPECS_SCRIPT}（{len(spec_files)} spec 文件）")
            # 下游非 quiet 模式已打印进度，这里不打重复摘要

    # 3b. 代码 AST：数据源 .py + ARCHITECTURE.md → extract_relations.py
    relation_triggers = classified["data_source_py"] + classified["architecture"]
    if relation_triggers:
        success, output = run_sibling_script(
            EXTRACT_RELATIONS_SCRIPT, vault_root, vibe_root,
            capture_summary=True, quiet=quiet,
        )
        summary = output.strip().split("\n")[-1] if output.strip() else ""
        actions.append({
            "script": EXTRACT_RELATIONS_SCRIPT,
            "reason": f"{len(relation_triggers)} 个数据流相关文件变更",
            "success": success,
            "summary": summary,
        })
        if not quiet:
            tag = "✅" if success else "❌"
            print(f"{tag} 调 {EXTRACT_RELATIONS_SCRIPT}（{len(relation_triggers)} 数据流文件）")

    # 3c. 代码 AST：Pydantic 模型 .py → extract_code_schema.py
    if classified["model_py"]:
        success, output = run_sibling_script(
            EXTRACT_CODE_SCHEMA_SCRIPT, vault_root, vibe_root,
            capture_summary=True, quiet=quiet,
        )
        summary = output.strip().split("\n")[-1] if output.strip() else ""
        actions.append({
            "script": EXTRACT_CODE_SCHEMA_SCRIPT,
            "reason": f"{len(classified['model_py'])} 个 Pydantic 模型变更",
            "success": success,
            "summary": summary,
        })
        if not quiet:
            tag = "✅" if success else "❌"
            print(f"{tag} 调 {EXTRACT_CODE_SCHEMA_SCRIPT}（{len(classified['model_py'])} 模型）")

    # 3d. 战法卡：刷新 last_synced + 标待核对（无下游脚本，P5 内部处理）
    if classified["strategy_cards"]:
        updated = sync_strategy_cards(
            classified["strategy_cards"], vibe_root, vault_root, dry_run, quiet,
        )
        actions.append({
            "script": "(internal) sync_strategy_cards",
            "reason": f"{len(classified['strategy_cards'])} 个战法卡变更",
            "success": True,
            "summary": f"刷新 last_synced：{len(updated)} 个",
        })

    # ── 4. 对所有触发抽取的 spec / 数据源 vault 文件刷新 last_synced ──
    # （下游脚本重抽后，标记本次同步时间）
    if not dry_run:
        # spec stubs（extract_specs.py 跑过的）
        if spec_files:
            specs_dir = vault_root / INVESTING_DIRNAME / SPECS_SUBDIR
            if specs_dir.is_dir():
                for spec_file in specs_dir.glob("S*.md"):
                    update_last_synced(spec_file, dry_run=False)
        # data-sources（extract_relations.py 跑过的）
        if relation_triggers:
            ds_dir = vault_root / INVESTING_DIRNAME / DATA_SOURCES_SUBDIR
            if ds_dir.is_dir():
                for ds_file in ds_dir.glob("*.md"):
                    if ds_file.name == "index.md":
                        continue
                    update_last_synced(ds_file, dry_run=False)

    # ── 5. 生成同步报告 ──
    report_path: Path | None = None
    if not dry_run:
        report_path = write_sync_report(
            docs_dir, since, changed, classified, actions, today_str, dry_run,
        )
    else:
        # dry-run 也预览报告路径
        report_path = docs_dir / f"sync-report-{today_str}.md"

    if not quiet:
        print("")
        print(f"=== 增量同步完成（{today_str}）===")
        print(f"窗口：{since}")
        print(f"变更文件：{len(changed)} 个（触发抽取 {sum(len(v) for k, v in classified.items() if k != 'other')}，跳过 {len(classified['other'])}）")
        print(f"执行动作：{len(actions)} 次")
        for a in actions:
            tag = "✅" if a["success"] else "❌"
            print(f"  {tag} {a['script']}：{a['reason']}")
        if dry_run:
            print("(dry-run 模式，未写入文件 + 未生成报告)")
        else:
            print(f"报告：{report_path}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="监听 Vibe-Research git commit，增量同步 vault 实体",
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
        "--since",
        type=str,
        default=DEFAULT_SINCE,
        help=f'git 时间窗口（默认："{DEFAULT_SINCE}"）',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将执行的动作，不实际写入",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="不打印进度",
    )
    args = parser.parse_args(argv)

    vault_root = args.vault.resolve()
    vibe_root = args.vibe_research.resolve()

    return run(vault_root, vibe_root, since=args.since, dry_run=args.dry_run, quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
