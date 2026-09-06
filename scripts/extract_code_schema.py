#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3：代码 AST 提取 → Pydantic 模型 schema → 模板字段差异报告
================================================================

用 Python `ast` 标准库扫描 Vibe-Research `backend/models/*.py` 的 Pydantic
模型，提取每个 `BaseModel` 子类的字段名 + 类型注解字符串，输出 JSON schema。
然后对比 vault `templates/*.md` 模板的 frontmatter 字段，输出差异报告
到 `docs/schema-diff-report.md`。

输出两份产出：
  1. `docs/code-schema.json` —— {ModelName: {field: type_str}}
  2. `docs/schema-diff-report.md` —— 模板 vs 代码字段差异

规则
----
- 纯标准库（ast / re / json，无 pydantic / 不 import 模型文件）
- 扫描所有 `class Xxx(BaseModel):` 类节点
- 字段 = 赋值节点 `field_name: Type = ...`（含类型注解）
- 类型注解用 `ast.unparse` 还原字符串（Python 3.9+），剥掉 `Optional[...]` /
  `| None` 等可选包装到核心类型
- 嵌套模型字段（如 `quote: Quote`）保留模型名作类型
- 模板字段 = `templates/*.md` frontmatter 的 key 列表（复用 vault_audit 的正则）
- 差异分类：
    - 模板有但代码无 → 冗余字段（template_only）
    - 代码有但模板无 → 缺失字段（code_only）
- 模型 ↔ 模板映射：硬编码（见 MODEL_TO_TEMPLATE）

用法：
    python3 scripts/extract_code_schema.py
    python3 scripts/extract_code_schema.py --vibe-research /path/to/Vibe-Research
    python3 scripts/extract_code_schema.py --vault /path/to/vault
    python3 scripts/extract_code_schema.py --quiet
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# 常量
# ──────────────────────────────────────────────────────────────────────────

DEFAULT_VAULT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VIBE_RESEARCH = Path("/Users/lizhiwei/project/code/stock/Vibe-Research")
MODELS_SUBDIR = "backend/models"
TEMPLATES_SUBDIR = "10_Reference/investing/templates"
DOCS_SUBDIR = "docs"
SCHEMA_JSON_NAME = "code-schema.json"
DIFF_REPORT_NAME = "schema-diff-report.md"

BEIJING_TZ = timezone(timedelta(hours=8))

# 扫描的模型文件列表（对齐设计文档 §P3）
MODEL_FILES = [
    "quote.py",
    "valuation.py",
    "financials.py",
    "report.py",
    "kline.py",
    "fund_flow.py",
    "news.py",
    "seat.py",
    "global_stock.py",
    "market_snapshot.py",
    # enums.py 不含 BaseModel 字段，但扫了也无害（只提取 BaseModel 子类）
]

# Pydantic 模型 → vault 模板 frontmatter 映射
# None = 无对应模板（差异报告里单列"未映射模型"段）
MODEL_TO_TEMPLATE: dict[str, str | None] = {
    # quote.py
    "Quote": "stock",
    # valuation.py
    "Valuation": "valuation",
    # financials.py
    "Financials": "metric",
    "FinancialPeriod": "metric",
    "ValuationPercentile": "valuation",
    "CompanyInfo": None,        # 无模板（公司基本信息并入 stock）
    "ConceptBlock": "concept",
    "Announcement": "event",
    # report.py
    "Report": "report",
    # kline.py
    "KLine": None,
    "KLineBar": None,
    # fund_flow.py
    "FundFlow": None,
    # news.py
    "News": "event",
    # seat.py
    "DragonTiger": "dragon-tiger",
    "DragonTigerRecord": "dragon-tiger",
    "Seat": "dragon-tiger",
    "BillboardDetail": "dragon-tiger",
    # global_stock.py
    "GlobalStock": None,
    "GlobalMetrics": "metric",
    # market_snapshot.py
    "Emotion": None,
    "Sector": None,
    "IndustrySector": None,
    "MarketSnapshot": None,
    "LianbanStock": None,
    "EmotionResponse": None,
    "ZTPoolItem": None,
}

# 模板 frontmatter 元字段（不算业务字段，差异比对时排除）
TEMPLATE_META_KEYS = {"type", "created"}


# ──────────────────────────────────────────────────────────────────────────
# AST 扫描 Pydantic 模型
# ──────────────────────────────────────────────────────────────────────────

BASEMODEL_NAMES = {"BaseModel", "str", "Enum"}


def is_basemodel_subclass(class_node: ast.ClassDef) -> bool:
    """判断 ClassDef 是否继承自 BaseModel（含间接，但实际项目是直接继承）。

    基类名匹配：BaseModel / 包含 BaseModel 的基类（如 `class X(BaseModel):`）
    """
    for base in class_node.bases:
        name = _unparse_node(base)
        if name == "BaseModel" or "BaseModel" in name:
            return True
    return False


def _unparse_node(node: ast.AST) -> str:
    """安全调用 ast.unparse（Python 3.9+），失败时 fallback 到 ast.dump。"""
    try:
        return ast.unparse(node)
    except Exception:
        return ast.dump(node)


def simplify_type(type_str: str) -> str:
    """把复杂类型注解简化为核心类型字符串。

    - `str | None` → `str`
    - `Optional[str]` → `str`
    - `int | None = None`（剥默认值已在字段提取时处理，但保险） → `int`
    - `tuple[KLineBar, ...]` → `tuple[KLineBar, ...]`（保留，是契约信息）
    - `list[dict] | None` → `list[dict]`
    - `Quote` → `Quote`（嵌套模型保留模型名）
    - `Market` → `Market`（枚举保留）
    """
    s = type_str.strip()
    # 去掉默认值部分（= ...）
    if "=" in s:
        s = s.split("=", 1)[0].strip()
    # Optional[X] → X
    m = re.match(r"^Optional\[(.+)\]$", s)
    if m:
        s = m.group(1).strip()
    # X | None → X  （非对称联合类型也剥 None 分支）
    if "|" in s:
        parts = [p.strip() for p in s.split("|")]
        non_none = [p for p in parts if p != "None"]
        if non_none:
            s = " | ".join(non_none)
            # 若剥完只剩一个，去掉 |
            if " | " not in s:
                s = s.strip()
    return s


def extract_model_fields(class_node: ast.ClassDef) -> "dict[str, str]":
    """从 ClassDef 提取 Pydantic 字段：{field_name: type_str}。

    字段识别规则：AnnAssign 节点，target 是 Name，annotation 是类型。
    - 跳过 model_config（Pydantic ConfigDict 赋值，非字段）
    - 跳过 @property 装饰的方法
    - 类型剥 Optional / | None 简化
    """
    fields: "dict[str, str]" = {}
    for node in class_node.body:
        # 字段：AnnAssign（带类型注解的赋值）
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id
            # 跳过 model_config（Pydantic 配置，非业务字段）
            if field_name == "model_config":
                continue
            type_str = simplify_type(_unparse_node(node.annotation))
            fields[field_name] = type_str
        # @property 不算字段（如 market_cap_yi）
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Name) and dec.id == "property":
                    break
    return fields


def scan_models_file(file_path: Path) -> "dict[str, dict[str, str]]":
    """扫描单个 .py 文件，返回 {ModelName: {field: type}}。"""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    result: "dict[str, dict[str, str]]" = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        if not is_basemodel_subclass(node):
            continue
        fields = extract_model_fields(node)
        # 空字段的 BaseModel 子类（如纯 enum）跳过
        if not fields:
            continue
        result[node.name] = fields
    return result


def scan_models_dir(models_dir: Path) -> "dict[str, dict[str, str]]":
    """扫描 models 目录下所有目标文件，合并返回 {ModelName: {field: type}}。"""
    all_models: "dict[str, dict[str, str]]" = {}
    for fname in MODEL_FILES:
        fpath = models_dir / fname
        if not fpath.is_file():
            continue
        try:
            models = scan_models_file(fpath)
        except SyntaxError as e:
            print(f"[WARN] {fname} 语法错误跳过：{e}", file=sys.stderr)
            continue
        for name, fields in models.items():
            # 同名模型后覆盖前（实际项目无重名）
            all_models[name] = fields
    return all_models


# ──────────────────────────────────────────────────────────────────────────
# 模板 frontmatter 解析（复用 vault_audit.py 的正则）
# ──────────────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
KV_LINE_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")


def parse_template_fields(template_text: str) -> "list[str]":
    """从模板文件 frontmatter 提取字段名列表（去掉 type/created 元字段）。"""
    m = FRONTMATTER_RE.match(template_text)
    if not m:
        return []
    fields: list[str] = []
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        kv = KV_LINE_RE.match(line)
        if kv:
            key = kv.group(1).strip()
            if key not in TEMPLATE_META_KEYS:
                fields.append(key)
    return fields


def load_templates(templates_dir: Path) -> "dict[str, list[str]]":
    """加载所有模板的 frontmatter 字段列表。返回 {template_stem: [fields]}。"""
    result: "dict[str, list[str]]" = {}
    if not templates_dir.is_dir():
        return result
    for path in sorted(templates_dir.glob("*.md")):
        # 跳过 audit/dataviewjs/quickadd 等非实体模板
        if path.stem in {"vault-audit-dataviewjs", "vault-audit-quickadd", "audit"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        fields = parse_template_fields(text)
        if fields:
            result[path.stem] = fields
    return result


# ──────────────────────────────────────────────────────────────────────────
# 差异计算
# ──────────────────────────────────────────────────────────────────────────


def compute_diff(code_fields: dict[str, str], template_fields: list[str]) -> dict:
    """计算单个模型 vs 单个模板的字段差异。

    返回：
      {
        "template_only": [...],   # 模板有代码无（冗余）
        "code_only": [...],       # 代码有模板无（缺失）
        "matched": [...]          # 两边都有
      }
    """
    code_keys = set(code_fields.keys())
    tmpl_keys = set(template_fields)
    template_only = sorted(tmpl_keys - code_keys)
    code_only = sorted(code_keys - tmpl_keys)
    matched = sorted(code_keys & tmpl_keys)
    return {
        "template_only": template_only,
        "code_only": code_only,
        "matched": matched,
    }


def build_diff_report(
    code_schema: dict[str, dict[str, str]],
    templates: dict[str, list[str]],
    today_str: str,
) -> str:
    """生成 schema-diff-report.md 内容。"""
    lines: list[str] = []
    lines.append("---")
    lines.append("type: report")
    lines.append("title: 代码 schema vs vault 模板字段差异报告")
    lines.append(f"created: {today_str}")
    lines.append("source: scripts/extract_code_schema.py (P3)")
    lines.append("---")
    lines.append("")
    lines.append("# 代码 Schema vs Vault 模板字段差异报告")
    lines.append("")
    lines.append("> 本报告由 `scripts/extract_code_schema.py` 自动生成。")
    lines.append("> 数据源：Vibe-Research `backend/models/*.py`（Pydantic 模型 AST 扫描）"
                 " + vault `templates/*.md`（frontmatter 字段）。")
    lines.append(">")
    lines.append("> **用途**：识别模板字段与代码契约的偏移，驱动模板字段对齐"
                 "（设计文档 §P3 验收：模板字段数 = Pydantic 模型字段数）。")
    lines.append("")
    lines.append(f"- 生成时间：{today_str}")
    lines.append(f"- 扫描模型文件：{', '.join(MODEL_FILES)}")
    lines.append(f"- 扫描 Pydantic 模型数：{len(code_schema)}")
    lines.append(f"- vault 模板数：{len(templates)}")
    lines.append("")

    # ── 已映射模型差异表 ──
    lines.append("## 已映射模型差异")
    lines.append("")
    lines.append("Pydantic 模型 ↔ vault 模板的字段对齐情况。")
    lines.append("")
    diff_rows: list[str] = []
    unmapped_models: list[str] = []
    for model_name in sorted(code_schema.keys()):
        template_stem = MODEL_TO_TEMPLATE.get(model_name)
        if template_stem is None:
            unmapped_models.append(model_name)
            continue
        if template_stem not in templates:
            diff_rows.append(
                f"| {model_name} | `{template_stem}` | ⚠ 模板缺失 | — | — | — |"
            )
            continue
        code_fields = code_schema[model_name]
        tmpl_fields = templates[template_stem]
        diff = compute_diff(code_fields, tmpl_fields)
        # 跳过完全对齐的（差异为空）—— 只列有差异的
        if not diff["template_only"] and not diff["code_only"]:
            continue
        tmpl_only_str = ", ".join(diff["template_only"]) if diff["template_only"] else "—"
        code_only_str = ", ".join(diff["code_only"]) if diff["code_only"] else "—"
        diff_rows.append(
            f"| {model_name} | `{template_stem}` | {len(diff['matched'])} | "
            f"{tmpl_only_str} | {code_only_str} |"
        )

    lines.append("")
    lines.append("| 模型 | 模板 | 匹配字段数 | 模板有代码无（冗余） | 代码有模板无（缺失） |")
    lines.append("|---|---|---|---|---|")
    if diff_rows:
        lines.extend(diff_rows)
    else:
        lines.append("| _（所有已映射模型字段完全对齐）_ | | | | |")
    lines.append("")

    # ── 完全对齐列表（便于核验）──
    lines.append("### 完全对齐的模型（参考）")
    lines.append("")
    aligned: list[str] = []
    for model_name in sorted(code_schema.keys()):
        template_stem = MODEL_TO_TEMPLATE.get(model_name)
        if not template_stem or template_stem not in templates:
            continue
        diff = compute_diff(code_schema[model_name], templates[template_stem])
        if not diff["template_only"] and not diff["code_only"]:
            aligned.append(
                f"- `{model_name}` ↔ `{template_stem}`（{len(diff['matched'])} 字段全匹配）"
            )
    if aligned:
        lines.extend(aligned)
    else:
        lines.append("_（无完全对齐的模型）_")
    lines.append("")

    # ── 未映射模型 ──
    lines.append("## 未映射到模板的模型")
    lines.append("")
    lines.append("这些 Pydantic 模型在 vault 无对应模板（设计上嵌套子模型或无独立实体文件夹）。")
    lines.append("字段列出来作参考，供后续决定是否需要新建模板或并入已有模板。")
    lines.append("")
    if unmapped_models:
        for name in unmapped_models:
            fields = code_schema[name]
            lines.append(f"### `{name}`（{len(fields)} 字段）")
            lines.append("")
            lines.append("| 字段 | 类型 |")
            lines.append("|---|---|")
            for fname, ftype in fields.items():
                lines.append(f"| {fname} | {ftype} |")
            lines.append("")
    else:
        lines.append("_（无）_")
        lines.append("")

    # ── 完整 schema 速览 ──
    lines.append("## 完整 Schema 速览")
    lines.append("")
    lines.append("所有 Pydantic 模型的字段+类型一览（完整 JSON 见 `docs/code-schema.json`）。")
    lines.append("")
    for model_name in sorted(code_schema.keys()):
        fields = code_schema[model_name]
        lines.append(f"### `{model_name}`（{len(fields)} 字段）")
        lines.append("")
        lines.append("| 字段 | 类型 |")
        lines.append("|---|---|")
        for fname, ftype in fields.items():
            lines.append(f"| {fname} | {ftype} |")
        lines.append("")

    # ── 模板字段清单 ──
    lines.append("## Vault 模板字段清单（参考）")
    lines.append("")
    lines.append("所有实体模板的 frontmatter 字段（去掉 type/created 元字段）。")
    lines.append("")
    for tmpl_stem in sorted(templates.keys()):
        fields = templates[tmpl_stem]
        lines.append(f"- **{tmpl_stem}**: {', '.join(fields) if fields else '（无字段）'}")
    lines.append("")

    # ── 修复建议 ──
    lines.append("## 修复建议")
    lines.append("")
    lines.append("### 模板有代码无（冗余字段）")
    lines.append("")
    lines.append("- **处置**：从模板 frontmatter 删掉代码契约已不承载的字段，"
                 "或在模板注释标注「由 frontmatter 以外的段落承载」。")
    lines.append("- 典型场景：strategy 模板的 `entry_conditions`/`exit_conditions`/"
                 "`match_conditions` 实际由正文标题承载（vault_audit.py 的 "
                 "BODY_HEADING_FOR_FIELD 机制），frontmatter 字段是冗余的。")
    lines.append("")
    lines.append("### 代码有模板无（缺失字段）")
    lines.append("")
    lines.append("- **处置**：在模板 frontmatter 补上代码契约实际承载的字段。")
    lines.append("- 优先级：先补 code/name 等规范标识符字段，再补业务字段。")
    lines.append("- 注意：并非所有代码字段都要进模板——嵌套子模型（如 KLineBar）"
                 "无独立 vault 实体，不需要模板。")
    lines.append("")
    lines.append("### 未映射模型")
    lines.append("")
    lines.append("- 若该模型对应独立 vault 实体类型，考虑新建模板。")
    lines.append("- 若为嵌套子模型（如 KLineBar、Seat、GlobalMetrics），"
                 "并入父实体模板或单独建模板均可，按是否需要独立查询决定。")
    lines.append("")

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────


def run(
    vault_root: Path,
    vibe_research_root: Path,
    quiet: bool = False,
) -> int:
    models_dir = vibe_research_root / MODELS_SUBDIR
    templates_dir = vault_root / TEMPLATES_SUBDIR
    docs_dir = vault_root / DOCS_SUBDIR

    if not models_dir.is_dir():
        print(f"[ERROR] models 目录不存在：{models_dir}", file=sys.stderr)
        return 2
    if not templates_dir.is_dir():
        print(f"[ERROR] templates 目录不存在：{templates_dir}", file=sys.stderr)
        return 2

    # 扫描代码 schema
    code_schema = scan_models_dir(models_dir)
    if not code_schema:
        print(f"[ERROR] 未扫到任何 Pydantic 模型（检查 {MODELS_SUBDIR}）", file=sys.stderr)
        return 3

    # 加载模板
    templates = load_templates(templates_dir)

    today_str = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")

    # 写 code-schema.json
    docs_dir.mkdir(parents=True, exist_ok=True)
    schema_json_path = docs_dir / SCHEMA_JSON_NAME
    schema_json_path.write_text(
        json.dumps(code_schema, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    # 写 schema-diff-report.md
    report = build_diff_report(code_schema, templates, today_str)
    report_path = docs_dir / DIFF_REPORT_NAME
    report_path.write_text(report, encoding="utf-8")

    if not quiet:
        print(f"[OK] 扫描 {len(code_schema)} 个 Pydantic 模型")
        print(f"     加载 {len(templates)} 个 vault 模板")
        print(f"     schema JSON：{schema_json_path.relative_to(vault_root)}")
        print(f"     差异报告：{report_path.relative_to(vault_root)}")
        # 差异统计
        aligned_count = 0
        diff_count = 0
        unmapped_count = 0
        for model_name in code_schema:
            tmpl_stem = MODEL_TO_TEMPLATE.get(model_name)
            if not tmpl_stem:
                unmapped_count += 1
                continue
            if tmpl_stem not in templates:
                diff_count += 1
                continue
            diff = compute_diff(code_schema[model_name], templates[tmpl_stem])
            if diff["template_only"] or diff["code_only"]:
                diff_count += 1
            else:
                aligned_count += 1
        print(f"     已映射对齐：{aligned_count} 个模型")
        print(f"     已映射有差异：{diff_count} 个模型")
        print(f"     未映射：{unmapped_count} 个模型（嵌套子模型/无独立模板）")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="从 Vibe-Research Pydantic 模型提取 schema，对比 vault 模板字段",
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
        "--quiet",
        action="store_true",
        help="不打印摘要到 stdout",
    )
    args = parser.parse_args(argv)

    vault_root = args.vault.resolve()
    vibe_root = args.vibe_research.resolve()

    return run(vault_root, vibe_root, quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
