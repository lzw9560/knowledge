#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vault Knowledge Graph Audit
===========================

纯标准库实现的 Obsidian 知识图谱审查脚本。扫描 vault 下的 markdown 文件，
跑 8 项检查，输出 JSON（stdout）+ 人类可读报告（reviews/<date>-ci-audit.md）。

8 项检查：
  1. summary         — 实体总数 + 各类型分布
  2. coverage        — 各实体类型数量对比，标出严重缺失
  3. orphan_check    — 没有被任何 [[链接]] 引用过的孤立文件
  4. broken_link     — 指向不存在文件的 [[链接]] 断链
  5. schema_infer    — 实体 frontmatter 字段 vs 模板字段，标缺失
  6. relation_density— 每个文件被引用次数（入边数），标 0 / 异常多
  7. duplicate_check — 按 frontmatter code 分组，找同 code 多份
  8. stale_check     — git log 取最后提交时间，标 90 天未更新

退出码：有 critical 级问题返回 1，否则 0。

用法：
    python scripts/vault_audit.py           # 在 vault 根目录下运行
    python scripts/vault_audit.py --quiet   # 不输出 JSON 到 stdout
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────────────────────────────────

INVESTING_DIR = Path("10_Reference/investing")
TEMPLATES_DIR = INVESTING_DIR / "templates"
REVIEWS_DIR = INVESTING_DIR / "reviews"

# 严重级排序
SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}

# 实体类型 → 模板文件名映射（templates/ 下）
# type 字段值 → 模板 stem
TYPE_TO_TEMPLATE = {
    "stock": "stock",
    "industry": "industry",
    "concept": "concept",
    "index": "index",
    "report": "report",
    "analyst": "analyst",
    "metric": "metric",
    "valuation": "valuation",
    "dragon_tiger": "dragon-tiger",
    "event": "event",
    "strategy": "strategy",
    "spec": "spec",
    "data_source": "data-source",
    "action": "action",
    "logic": "logic",
    "inbox_item": "inbox-item",
    "audit": "audit",
}

# 被排除出实体计数的文件（非实体，属结构/导航文件）
def is_structural_file(rel_path: str) -> bool:
    """index.md / MOC.md / README.md 等结构文件不算实体"""
    name = Path(rel_path).name
    return name in ("index.md", "MOC.md", "README.md")


# ──────────────────────────────────────────────────────────────────────────
# YAML frontmatter 解析（纯正则，不依赖 PyYAML）
# ──────────────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# 匹配 key: value 行（key 不含空白/冒号；value 可为空、可含冒号）
KV_LINE_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")


def parse_frontmatter(text: str) -> dict:
    """从 markdown 文本解析 YAML frontmatter。返回 {} 表示无 frontmatter。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        # 跳过空行和注释
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        kv = KV_LINE_RE.match(line)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip()
            # 去掉值两端的引号
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            # 布尔值
            if val.lower() in ("true", "false"):
                val = val.lower() == "true"
            fm[key] = val
    return fm


def extract_template_fields(template_text: str) -> list:
    """从模板文件提取 frontmatter 字段名列表（含 Templater 占位的也算字段）。"""
    return list(parse_frontmatter(template_text).keys())


# ──────────────────────────────────────────────────────────────────────────
# [[链接]] 解析
# ──────────────────────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def extract_wikilinks(text: str) -> list:
    """提取所有 [[链接]]，返回原始目标（去掉 |别名 后的路径部分）。
    过滤掉 dataview 代码块内的伪链接——dataview 块内的 FROM/WHERE 不是链接。
    """
    # 先去掉 ```dataview ... ``` 代码块
    cleaned = re.sub(r"```dataview\b.*?```", "", text, flags=re.DOTALL | re.IGNORECASE)
    # 去掉普通 ``` 代码块
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    # 去掉行内 `code` 中的潜在干扰
    cleaned = re.sub(r"`[^`]*`", "", cleaned)

    links = []
    for m in WIKILINK_RE.finditer(cleaned):
        target = m.group(1)
        # 处理别名 [[path|alias]]
        if "|" in target:
            target = target.split("|", 1)[0]
        target = target.strip()
        if target:
            links.append(target)
    return links


def resolve_link_target(link_target: str, vault_root: Path) -> Path | None:
    """把 [[链接]] 目标解析为实际文件路径。返回相对于 vault_root 的 Path 或 None。

    链接可能是：
      - [[stocks/600519]]      → 10_Reference/investing/stocks/600519.md
      - [[stocks/600519|茅台]]  → 同上（别名已在 extract 时剥离）
      - [[stocks/]]            → 文件夹链接，指向 stocks/index.md
      - [[strategies/dragon_head]] → 10_Reference/investing/strategies/dragon_head.md
      - [[MOC]]                 → 10_Reference/investing/MOC.md 或根目录

    优先在 investing/ 下找，再在 vault 根找。
    返回绝对路径（基于 vault_root 拼接）。
    """
    investing_abs = vault_root / INVESTING_DIR
    # 文件夹链接（以 / 结尾）→ index.md
    if link_target.endswith("/"):
        folder = link_target.rstrip("/")
        candidates = [
            investing_abs / folder / "index.md",
            vault_root / folder / "index.md",
        ]
    else:
        # 普通链接：先试加 .md，再试原路径（可能是带扩展名的）
        candidates = [
            investing_abs / f"{link_target}.md",
            investing_abs / link_target,
            vault_root / f"{link_target}.md",
            vault_root / link_target,
        ]

    for cand in candidates:
        if cand.is_file():
            return cand
    return None


# ──────────────────────────────────────────────────────────────────────────
# git log 取最后提交时间
# ──────────────────────────────────────────────────────────────────────────

def get_git_last_commit_iso(path: str) -> str | None:
    """取文件最后提交的 ISO 时间（UTC）。失败返回 None。"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", path],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    return None


# ──────────────────────────────────────────────────────────────────────────
# 主审查器
# ──────────────────────────────────────────────────────────────────────────

class VaultAudit:
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.investing = vault_root / INVESTING_DIR
        # 收集所有 .md 文件（investing 目录下，排除 templates/）
        self.all_files: list[Path] = []
        # 相对路径 → 文件内容快照
        self.file_contents: dict[str, str] = {}
        # 相对路径 → frontmatter
        self.file_frontmatter: dict[str, dict] = {}
        # 相对路径(investing 下，正斜杠) → 绝对路径，用于链接解析
        self.path_index: dict[str, Path] = {}
        # 入边计数：被引用文件相对路径 → 次数
        self.inbound_count: Counter[str] = Counter()
        # 所有链接：源文件相对路径 → [链接目标原始串]
        self.links_by_source: dict[str, list[str]] = defaultdict(list)

        self.findings: list[dict] = []
        self.report_data: dict = {}
        self.quiet = False

    # ── 收集阶段 ──────────────────────────────────────────────────────

    def collect_files(self):
        """扫描 investing/ 下所有 .md（排除 templates/ 和 reviews/ 旧报告）"""
        for p in sorted(self.investing.rglob("*.md")):
            # 排除 templates/
            if "templates" in p.parts:
                continue
            # reviews/ 下只保留 index.md，排除历史 ci-audit 报告（避免自指噪声）
            if "reviews" in p.parts and p.name != "index.md":
                continue
            self.all_files.append(p)
            rel = p.relative_to(self.vault_root).as_posix()
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                text = ""
            self.file_contents[rel] = text
            self.file_frontmatter[rel] = parse_frontmatter(text)
            # 构建路径索引：investing 相对路径 → 绝对路径
            investing_rel = p.relative_to(self.investing).as_posix()
            self.path_index[investing_rel] = p

    def collect_links(self):
        """从所有文件提取 [[链接]]，统计入边"""
        for rel, text in self.file_contents.items():
            links = extract_wikilinks(text)
            self.links_by_source[rel] = links
            for target in links:
                resolved = resolve_link_target(target, self.vault_root)
                if resolved is not None:
                    resolved_rel = resolved.relative_to(self.vault_root).as_posix()
                    self.inbound_count[resolved_rel] += 1

    # ── 8 项检查 ────────────────────────────────────────────────────

    def check_summary(self) -> dict:
        """1. summary — 实体总数 + 各类型分布"""
        type_counter = Counter()
        folder_counter = Counter()
        entity_total = 0

        for p in self.all_files:
            rel = p.relative_to(self.investing).as_posix()
            # 跳过结构文件
            if is_structural_file(rel):
                continue
            # 统计所属文件夹（investing 下一级）
            parts = p.relative_to(self.investing).parts
            if len(parts) >= 1:
                folder_counter[parts[0]] += 1
            # 统计 type
            fm = self.file_frontmatter.get(p.relative_to(self.vault_root).as_posix(), {})
            t = fm.get("type", "(无 type)")
            type_counter[t] += 1
            entity_total += 1

        result = {
            "entity_total": entity_total,
            "type_distribution": dict(type_counter.most_common()),
            "folder_distribution": dict(folder_counter.most_common()),
        }
        self.report_data["summary"] = result
        return result

    def check_coverage(self) -> dict:
        """2. coverage — 各实体类型数量对比，标严重缺失"""
        type_counter = Counter()
        for p in self.all_files:
            rel = p.relative_to(self.investing).as_posix()
            if is_structural_file(rel):
                continue
            fm = self.file_frontmatter.get(p.relative_to(self.vault_root).as_posix(), {})
            t = fm.get("type", "(无 type)")
            type_counter[t] += 1

        # 各类型数量
        type_counts = dict(type_counter.most_common())
        # 期望类型（来自模板定义的 type 值）
        expected_types = set(TYPE_TO_TEMPLATE.keys())
        present_types = set(type_counts.keys())
        missing_types = sorted(expected_types - present_types - {"(无 type)"})

        # 严重缺失判定：某类型 0 个 → critical
        zero_types = [t for t in expected_types if type_counts.get(t, 0) == 0]
        for t in zero_types:
            self.findings.append({
                "check": "coverage",
                "severity": "critical",
                "message": f"实体类型 '{t}' 数量为 0（完全缺失）",
                "entity": None,
            })

        # 严重不均衡：最大类型数 vs 最小非零类型数，差距 > 10x 且最小 < 5
        nonzero_counts = [c for c in type_counts.values() if c > 0]
        if len(nonzero_counts) >= 2:
            mx, mn = max(nonzero_counts), min(nonzero_counts)
            if mx > 0 and mn < 5 and mx / mn > 10:
                # 找出最小的那个类型
                min_type = min(type_counts.items(), key=lambda x: x[1] if x[1] > 0 else 9999)
                self.findings.append({
                    "check": "coverage",
                    "severity": "medium",
                    "message": f"类型分布严重不均衡：最大 {mx} vs 最小 {mn}（类型 '{min_type[0]}'）",
                    "entity": None,
                })

        result = {
            "type_counts": type_counts,
            "missing_types": missing_types,
            "zero_types": zero_types,
        }
        self.report_data["coverage"] = result
        return result

    def check_orphan(self) -> dict:
        """3. orphan_check — 未被任何 [[链接]] 引用的孤立文件"""
        orphans = []
        for p in self.all_files:
            rel = p.relative_to(self.investing).as_posix()
            if is_structural_file(rel):
                continue  # 结构文件不算孤立
            full_rel = p.relative_to(self.vault_root).as_posix()
            if self.inbound_count.get(full_rel, 0) == 0:
                # 例外：MOC.md / index.md 本身是导航枢纽，不算 orphan
                orphans.append({
                    "path": rel,
                    "type": self.file_frontmatter.get(full_rel, {}).get("type", "?"),
                })
                self.findings.append({
                    "check": "orphan_check",
                    "severity": "medium",
                    "message": f"孤立实体（无入边）：{rel}",
                    "entity": rel,
                })
        result = {"orphans": orphans, "count": len(orphans)}
        self.report_data["orphan_check"] = result
        return result

    def check_broken_links(self) -> dict:
        """4. broken_link — 指向不存在文件的断链"""
        broken = []
        seen_targets = set()  # 去重同一目标
        for src_rel, targets in self.links_by_source.items():
            for target in targets:
                resolved = resolve_link_target(target, self.vault_root)
                if resolved is None:
                    key = (src_rel, target)
                    if key in seen_targets:
                        continue
                    seen_targets.add(key)
                    broken.append({"source": src_rel, "target": target})
                    self.findings.append({
                        "check": "broken_link",
                        "severity": "high",
                        "message": f"断链：[[{target}]]（源：{src_rel}）",
                        "entity": src_rel,
                    })
        result = {"broken_links": broken, "count": len(broken)}
        self.report_data["broken_link"] = result
        return result

    def check_schema(self) -> dict:
        """5. schema_infer — 实体 frontmatter 字段 vs 模板字段"""
        # 加载所有模板字段
        template_fields: dict[str, list[str]] = {}
        templates_path = self.vault_root / TEMPLATES_DIR
        if templates_path.is_dir():
            for tp in templates_path.glob("*.md"):
                try:
                    text = tp.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                template_fields[tp.stem] = extract_template_fields(text)

        # 按 type 字段匹配模板
        # type 值 → 模板 stem 映射（TYPE_TO_TEMPLATE）
        deviations = []
        for p in self.all_files:
            rel = p.relative_to(self.vault_root).as_posix()
            investing_rel = p.relative_to(self.investing).as_posix()
            if is_structural_file(investing_rel):
                continue
            fm = self.file_frontmatter.get(rel, {})
            t = fm.get("type")
            if not t:
                continue  # 无 type 的不查 schema
            template_stem = TYPE_TO_TEMPLATE.get(t)
            if not template_stem:
                continue  # 无对应模板
            expected = template_fields.get(template_stem, [])
            if not expected:
                continue
            actual_keys = set(fm.keys())
            expected_set = set(expected)
            # 必填字段缺失（排除 created，created 通常由 Templater 自动填）
            missing = sorted(expected_set - actual_keys - {"created"})
            # 多余字段（实际有但模板没有，仅记录不报错）
            extra = sorted(actual_keys - expected_set)
            if missing:
                # 必填字段缺失 → high
                for field in missing:
                    # created 之外，code/name/title 是关键标识字段，缺失直接 high
                    self.findings.append({
                        "check": "schema_infer",
                        "severity": "high",
                        "message": f"字段缺失：{investing_rel} 缺少 '{field}'（模板 {template_stem} 定义）",
                        "entity": investing_rel,
                    })
                deviations.append({
                    "path": investing_rel,
                    "type": t,
                    "missing_fields": missing,
                    "extra_fields": extra,
                })
        result = {"deviations": deviations, "count": len(deviations)}
        self.report_data["schema_infer"] = result
        return result

    def check_relation_density(self) -> dict:
        """6. relation_density — 入边数统计，标 0 或异常多"""
        # 异常多阈值：超过所有入边的 mean + 3*std，或硬阈值 > 20
        counts = list(self.inbound_count.values())
        if counts:
            mean_c = sum(counts) / len(counts)
            std_c = (sum((c - mean_c) ** 2 for c in counts) / len(counts)) ** 0.5
            threshold = mean_c + 3 * std_c if std_c > 0 else 20
            threshold = max(threshold, 20)  # 硬下限 20
        else:
            threshold = 20

        hubs = []  # 入边异常多
        # 孤立的已在 orphan_check 报，这里只报 hub
        for full_rel, cnt in self.inbound_count.items():
            if cnt >= threshold:
                investing_rel = full_rel.replace("10_Reference/investing/", "", 1)
                hubs.append({"path": investing_rel, "inbound": cnt})
                self.findings.append({
                    "check": "relation_density",
                    "severity": "low",
                    "message": f"入边异常多（{cnt} 次）：{investing_rel}",
                    "entity": investing_rel,
                })
        result = {
            "hub_threshold": round(threshold, 1),
            "hubs": sorted(hubs, key=lambda x: -x["inbound"]),
            "total_links": sum(self.inbound_count.values()),
        }
        self.report_data["relation_density"] = result
        return result

    def check_duplicates(self) -> dict:
        """7. duplicate_check — 按 code 字段分组，同 code 多份"""
        code_map: dict[str, list[str]] = defaultdict(list)
        for p in self.all_files:
            rel = p.relative_to(self.investing).as_posix()
            if is_structural_file(rel):
                continue
            full_rel = p.relative_to(self.vault_root).as_posix()
            fm = self.file_frontmatter.get(full_rel, {})
            code = fm.get("code")
            if code and str(code).strip():
                code_map[str(code).strip()].append(rel)

        duplicates = []
        for code, paths in code_map.items():
            if len(paths) > 1:
                duplicates.append({"code": code, "paths": paths, "count": len(paths)})
                self.findings.append({
                    "check": "duplicate_check",
                    "severity": "critical",
                    "message": f"重复 code='{code}'：{len(paths)} 份记录 {paths}",
                    "entity": code,
                })
        result = {"duplicates": duplicates, "count": len(duplicates)}
        self.report_data["duplicate_check"] = result
        return result

    def check_stale(self, days: int = 90) -> dict:
        """8. stale_check — git log 取最后提交，标 90 天未更新"""
        threshold = datetime.now(timezone.utc) - timedelta(days=days)
        stale = []
        for p in self.all_files:
            rel = p.relative_to(self.vault_root).as_posix()
            investing_rel = p.relative_to(self.investing).as_posix()
            if is_structural_file(investing_rel):
                continue
            iso = get_git_last_commit_iso(rel)
            if not iso:
                # 无 git 记录（新文件未提交）→ 跳过，不报 stale
                continue
            try:
                dt = datetime.fromisoformat(iso)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if dt < threshold:
                age_days = (datetime.now(timezone.utc) - dt).days
                stale.append({
                    "path": investing_rel,
                    "last_commit": iso,
                    "age_days": age_days,
                })
                self.findings.append({
                    "check": "stale_check",
                    "severity": "low",
                    "message": f"90+ 天未更新（{age_days} 天）：{investing_rel}",
                    "entity": investing_rel,
                })
        result = {"stale": sorted(stale, key=lambda x: x["age_days"], reverse=True), "count": len(stale)}
        self.report_data["stale_check"] = result
        return result

    # ── 报告生成 ──────────────────────────────────────────────────────

    def generate_findings_summary(self) -> dict:
        """按 severity 汇总 findings"""
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        by_check: dict[str, dict[str, int]] = defaultdict(lambda: {"critical": 0, "high": 0, "medium": 0, "low": 0})
        for f in self.findings:
            sev = f["severity"]
            summary[sev] = summary.get(sev, 0) + 1
            by_check[f["check"]][sev] += 1
        return {"total": summary, "by_check": dict(by_check)}

    def generate_report_markdown(self) -> str:
        """生成人类可读的审查报告 markdown"""
        today = datetime.now().strftime("%Y-%m-%d")
        fs = self.generate_findings_summary()
        total = fs["total"]

        # 按 severity 分组 findings
        by_sev: dict[str, list] = {"critical": [], "high": [], "medium": [], "low": []}
        for f in self.findings:
            by_sev[f["severity"]].append(f)

        lines = []
        lines.append("---")
        lines.append("type: audit")
        lines.append(f"audit_date: {today}")
        lines.append("auditor: ci-github-actions")
        lines.append("scope: 全量")
        lines.append(f"findings_count: {len(self.findings)}")
        lines.append(f"critical: {total['critical']}")
        lines.append(f"high: {total['high']}")
        lines.append(f"medium: {total['medium']}")
        lines.append(f"low: {total['low']}")
        lines.append("status: 已完成")
        lines.append(f"created: {today}")
        lines.append("---")
        lines.append("")
        lines.append(f"# 审查报告：{today}")
        lines.append("")
        lines.append("> CI 自动审查（github-actions[bot]）。每周日定时跑 8 项检查，问题按严重级分类。")
        lines.append("")
        lines.append("## 审查范围")
        lines.append("")
        lines.append("- **范围**：全量（`10_Reference/investing/` 下所有 .md，排除 templates/ 和历史报告）")
        lines.append("- **审查人**：ci-github-actions[bot]")
        lines.append("- **触发**：定时（每周日 02:00 北京时间）/ 手动 workflow_dispatch")
        lines.append("")
        lines.append("## 8 项检查结果")
        lines.append("")

        # 1. summary
        s = self.report_data.get("summary", {})
        lines.append("### 1. summary（图谱摘要）")
        lines.append(f"- 实体总数：{s.get('entity_total', 0)}")
        lines.append("- 各类型分布：")
        for t, c in s.get("type_distribution", {}).items():
            lines.append(f"  - `{t}`：{c}")
        lines.append("- 各文件夹分布：")
        for f, c in s.get("folder_distribution", {}).items():
            lines.append(f"  - `{f}/`：{c}")
        lines.append("")

        # 2. coverage
        c = self.report_data.get("coverage", {})
        lines.append("### 2. coverage（覆盖率）")
        tc = c.get("type_counts", {})
        if tc:
            lines.append("- 各类型数量：")
            for t, n in tc.items():
                lines.append(f"  - `{t}`：{n}")
        mt = c.get("missing_types", [])
        if mt:
            lines.append(f"- 缺失类型（模板定义但无实体）：{', '.join(mt)}")
        zt = c.get("zero_types", [])
        if zt:
            lines.append(f"- ⚠️ 完全缺失（0 个）：{', '.join(zt)}")
        lines.append("")

        # 3. orphan_check
        o = self.report_data.get("orphan_check", {})
        lines.append("### 3. orphan_check（孤立实体）")
        lines.append(f"- 无入边实体数：{o.get('count', 0)}")
        if o.get("orphans"):
            lines.append("- 孤立实体列表：")
            for x in o["orphans"][:20]:
                lines.append(f"  - `{x['path']}`（type: {x['type']}）")
            if len(o["orphans"]) > 20:
                lines.append(f"  - … 共 {len(o['orphans'])} 个，仅显示前 20")
        lines.append("")

        # 4. broken_link
        b = self.report_data.get("broken_link", {})
        lines.append("### 4. broken_link（断链）")
        lines.append(f"- 断链数：{b.get('count', 0)}")
        if b.get("broken_links"):
            lines.append("- 断链列表：")
            for x in b["broken_links"][:20]:
                lines.append(f"  - `[[{x['target']}]]` ← {x['source']}")
            if len(b["broken_links"]) > 20:
                lines.append(f"  - … 共 {len(b['broken_links'])} 条，仅显示前 20")
        lines.append("")

        # 5. schema_infer
        si = self.report_data.get("schema_infer", {})
        lines.append("### 5. schema_infer（schema 偏差）")
        lines.append(f"- 字段缺失的实体数：{si.get('count', 0)}")
        if si.get("deviations"):
            lines.append("- 偏差列表：")
            for x in si["deviations"][:20]:
                lines.append(f"  - `{x['path']}`（{x['type']}）缺少：{', '.join(x['missing_fields'])}")
            if len(si["deviations"]) > 20:
                lines.append(f"  - … 共 {len(si['deviations'])} 个，仅显示前 20")
        lines.append("")

        # 6. relation_density
        rd = self.report_data.get("relation_density", {})
        lines.append("### 6. relation_density（关系密度）")
        lines.append(f"- 链接总数（入边合计）：{rd.get('total_links', 0)}")
        lines.append(f"- hub 阈值（mean+3σ，硬下限 20）：{rd.get('hub_threshold', 20)}")
        if rd.get("hubs"):
            lines.append("- 入边异常多实体：")
            for x in rd["hubs"]:
                lines.append(f"  - `{x['path']}`：{x['inbound']} 次入边")
        lines.append("")

        # 7. duplicate_check
        d = self.report_data.get("duplicate_check", {})
        lines.append("### 7. duplicate_check（重复）")
        lines.append(f"- 重复 code 数：{d.get('count', 0)}")
        if d.get("duplicates"):
            lines.append("- 重复列表：")
            for x in d["duplicates"]:
                lines.append(f"  - code=`{x['code']}`（{x['count']} 份）：{', '.join(x['paths'])}")
        lines.append("")

        # 8. stale_check
        sc = self.report_data.get("stale_check", {})
        lines.append("### 8. stale_check（过期）")
        lines.append(f"- 90+ 天未更新实体数：{sc.get('count', 0)}")
        if sc.get("stale"):
            lines.append("- 过期列表：")
            for x in sc["stale"][:20]:
                lines.append(f"  - `{x['path']}`（{x['age_days']} 天，最后提交 {x['last_commit'][:10]})")
            if len(sc["stale"]) > 20:
                lines.append(f"  - … 共 {len(sc['stale'])} 个，仅显示前 20")
        lines.append("")

        # 问题清单
        lines.append("## 问题清单")
        lines.append("")
        for sev, label in [("critical", "Critical（阻断）"), ("high", "High（优先修）"),
                           ("medium", "Medium（进 backlog）"), ("low", "Low（知悉即可）")]:
            lines.append(f"### {label}")
            items = by_sev.get(sev, [])
            if not items:
                lines.append("- （无）")
            else:
                for f in items:
                    lines.append(f"- [{f['check']}] {f['message']}")
            lines.append("")

        # 修复建议
        lines.append("## 修复建议")
        lines.append("")
        if total["critical"] > 0:
            lines.append("1. **Critical**：立即处理——coverage 完全缺失类型需导入实体；duplicate 同 code 多份需合并去重。")
        if total["high"] > 0:
            lines.append("2. **High**：本周期内修——broken_link 断链需补建目标文件或修正链接；schema 缺失必填字段需补全。")
        if total["medium"] > 0:
            lines.append("3. **Medium**：进 backlog——orphan 孤立实体需建立入边链接。")
        if total["low"] > 0:
            lines.append("4. **Low**：知悉即可——stale 过期实体视情况更新或归档；hub 入边过多的拆分枢纽。")
        if not self.findings:
            lines.append("1. 图谱健康，无需修复。")
        lines.append("")

        # 跟踪
        lines.append("## 跟踪")
        lines.append("")
        lines.append(f"- [ ] Critical 全部修复（{total['critical']}）")
        lines.append(f"- [ ] High 修复或进 spec（{total['high']}）")
        lines.append(f"- [ ] Medium 进 backlog（{total['medium']}）")
        lines.append("- [ ] 下次审查日期：下周日")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"> 本报告由 `scripts/vault_audit.py` 生成于 {today}，CI 自动提交。")

        return "\n".join(lines)

    def write_report(self) -> Path:
        """写报告到 reviews/<date>-ci-audit.md，返回路径"""
        reviews_path = self.vault_root / REVIEWS_DIR
        reviews_path.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        report_path = reviews_path / f"{today}-ci-audit.md"
        report_path.write_text(self.generate_report_markdown(), encoding="utf-8")
        return report_path

    # ── 主流程 ────────────────────────────────────────────────────────

    def run(self) -> int:
        """跑全部 8 项检查，返回退出码（1=有 critical，0=无）"""
        self.collect_files()
        self.collect_links()
        self.check_summary()
        self.check_coverage()
        self.check_orphan()
        self.check_broken_links()
        self.check_schema()
        self.check_relation_density()
        self.check_duplicates()
        self.check_stale()

        report_path = self.write_report()

        fs = self.generate_findings_summary()
        has_critical = fs["total"]["critical"] > 0

        # 输出 JSON 到 stdout
        output = {
            "audit_date": datetime.now().strftime("%Y-%m-%d"),
            "report_path": str(report_path.relative_to(self.vault_root).as_posix()),
            "findings_summary": fs,
            "checks": self.report_data,
            "findings": self.findings,
        }
        if not self.quiet:
            print(json.dumps(output, ensure_ascii=False, indent=2))

        return 1 if has_critical else 0


def main():
    parser = argparse.ArgumentParser(description="Vault knowledge graph audit")
    parser.add_argument("--quiet", action="store_true", help="不输出 JSON 到 stdout")
    parser.add_argument("--root", default=".", help="vault 根目录（默认当前目录）")
    args = parser.parse_args()

    vault_root = Path(args.root).resolve()
    audit = VaultAudit(vault_root)
    audit.quiet = args.quiet
    return audit.run()


if __name__ == "__main__":
    sys.exit(main())
