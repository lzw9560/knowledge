#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P4：关系层灌入脚本
================================================

从 Vibe-Research 代码 + `ARCHITECTURE.md` 提取四类数据流关系，更新 vault
`10_Reference/investing/` 实体的 `[[]]` 链接段。

抽取的四类关系（对齐设计文档 P4）：
1. 函数 → 数据源：`astock.tencent_quote` → `[[data-sources/tencent]]`
   源：`backend/data/sources/*.py`（AST 扫函数名 + 模块 docstring 的源归一）
2. 工具 → 函数：`query_quote` → `astock.tencent_quote`
   源：`backend/ai/tools/stock_tools.py`（`@register_tool` 装饰器 + 函数体调用）
3. 数据源 → 实体类型：`tencent` → `stocks/`（提供行情数据）
   源：`ARCHITECTURE.md` 数据流图（正则匹配"外部源 ────► astock.py"行）
4. spec → 数据源：`S008` → `[[data-sources/akshare]]`（S008 迁移了 akshare）
   源：vault specs/ 已有"数据源"段（正则抓 `[[]]` 链接）+ spec 正文 `SNNN`

实现要点（纯标准库，对齐 P1-P3 风格）
----
- 用 `ast` 标准库扫 `data/sources/*.py`，取模块 docstring + 函数名清单
- 模块名 → 数据源实体归一表（硬编码：tencent.py → data-sources/tencent 等，
  与 `ARCHITECTURE.md` 一图概览 + 已灌入的 16 数据源对齐）
- `stock_tools.py` 走 `ast`：`@register_tool("工具名", ...)` 装饰器抓工具名，
  函数体里的 `astock.xxx` / `gstock.xxx` / `data.sources.xxx.func` 调用抓被调函数
- `ARCHITECTURE.md` 数据流图用正则抓"源名 (端点) ────►"行 → 数据源实体
- 写入策略：在 vault 实体文件正文末尾追加 `## 数据流关系` 段；data-sources
  的 `## 相关工具` 段追加工具链接；specs 的 `## 关联` 段已有数据源链接则跳过
- 幂等：先读已有内容，段已存在且内容一致则不重写（按"本脚本生成"标记定位）
- 查实体词典 `.entity-dictionary.json` 保证 `[[]]` 目标存在

输出
----
- 更新 `data-sources/*.md`（追加/刷新 `## 数据流关系` + `## 相关工具` 段）
- 更新 `specs/*.md`（`## 关联` 段缺数据源链接时补）
- 生成 `docs/relation-extraction-report.md`（提取关系数 + 更新文件清单）

用法：
    python3 scripts/extract_relations.py
    python3 scripts/extract_relations.py --vibe-research /path/to/Vibe-Research
    python3 scripts/extract_relations.py --vault /path/to/vault
    python3 scripts/extract_relations.py --dry-run
    python3 scripts/extract_relations.py --quiet
"""

from __future__ import annotations

import argparse
import ast
import json
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
DOCS_SUBDIR = "docs"
SOURCES_SUBDIR = "data-sources"
SPECS_SUBDIR = "specs"
DICTIONARY_NAME = ".entity-dictionary.json"
REPORT_NAME = "relation-extraction-report.md"

# Vibe-Research 源码相对路径
VR_SOURCES_DIR = "backend/data/sources"
VR_STOCK_TOOLS = "backend/ai/tools/stock_tools.py"
VR_ARCH = "ARCHITECTURE.md"

BEIJING_TZ = timezone(timedelta(hours=8))

# 本脚本生成段落的标记（幂等定位用）
GENERATED_TAG = "<!-- pipeline: P4 extract_relations.py 生成 -->"

# ──────────────────────────────────────────────────────────────────────────
# 模块名 → 数据源实体归一表
# 对齐已灌入的 data-sources/ 16 实体（见 ARCHITECTURE.md 一图概览）
# key: Vibe-Research backend/data/sources/<key>.py
# value: (vault 实体相对路径 stem, 数据源 code, 提供的实体类型列表)
# ──────────────────────────────────────────────────────────────────────────

# 提供的实体类型段（喂给 X）从 ARCHITECTURE.md 一图概览推断
MODULE_TO_SOURCE: dict[str, tuple[str, str, list[str]]] = {
    "tencent":            ("data-sources/tencent",            "tencent",
                           ["stocks", "valuations", "metrics"]),
    "eastmoney":          ("data-sources/eastmoney-push2",    "eastmoney-push2",
                           ["stocks", "valuations", "metrics", "dragon-tiger", "events", "reports"]),
    "akshare_src":        ("data-sources/akshare",            "akshare",
                           ["industries", "metrics"]),
    "baostock_src":       ("data-sources/baostock",           "baostock",
                           ["stocks", "valuations"]),
    "mootdx_src":         ("data-sources/mootdx",             "mootdx",
                           ["stocks", "valuations"]),
    "sina":               ("data-sources/sina-financial",     "sina-financial",
                           ["stocks", "valuations"]),
    "sina_financial":     ("data-sources/sina-financial",     "sina-financial",
                           ["stocks", "valuations", "metrics"]),
    "baidu":              ("data-sources/baidu-stock",       "baidu-stock",
                           ["stocks", "valuations"]),
    "cninfo":             ("data-sources/cninfo",            "cninfo",
                           ["stocks", "events"]),
    "hithink_src":        ("data-sources/hithink-ths",        "hithink-ths",
                           ["stocks", "valuations", "metrics", "events"]),
    "worldmonitor":       ("data-sources/worldmonitor",      "worldmonitor",
                           ["industries", "metrics", "events"]),
    "tickflow":           ("data-sources/mootdx",             "mootdx",
                           ["stocks", "valuations"]),
    "cyq_js":              (None, None, []),  # 计算层，非数据源
    "kline_resolver":     (None, None, []),  # 解耦层，非数据源
    "_common":            (None, None, []),  # 公共工具，非数据源
}

# ARCHITECTURE.md 一图概览中的外部源行（正则匹配）
# 示例：腾讯 qt.gtimg.cn (不封IP) ──────►  astock.py (A股全栈)  ──┐
ARCH_DATAFLOW_LINE_RE = re.compile(
    r"^(?P<source>[^\s─]+(?:\s+[^\s─]+)*?)\s*\((?P<endpoint>[^)]+)\)\s*[─►├└┐┘│]+\s*(?P<rest>.*)$"
)

# 端点 → 数据源 code 归一（用于 ARCHITECTURE.md 数据流图匹配后建 [[]] 链接）
ENDPOINT_TO_SOURCE_CODE: dict[str, str] = {
    "qt.gtimg.cn":                "tencent",
    "push2":                      "eastmoney-push2",
    "push2ex":                    "eastmoney-push2ex",
    "reportapi":                  "eastmoney-reportapi",
    "datacenter-web.eastmoney.com": "eastmoney-datacenter",
    "datacenter":                 "eastmoney-datacenter",
    "searchapi":                  "eastmoney-searchapi",
    "akshare":                    "akshare",
    "akshare Python 包":          "akshare",
    "mootdx TCP:7709":            "mootdx",
    "mootdx":                     "mootdx",
    "bbaostock.com":              "baostock",
    "baostock":                   "baostock",
    "finance.pae.baidu.com":      "baidu-stock",
    "百度股市通":                  "baidu-stock",
    "新浪":                       "sina-financial",
    "新浪/巨潮/同花顺":            "sina-financial",
    "巨潮 cninfo（互动易）":       "cninfo",
    "www.cninfo.com.cn":          "cninfo",
    "irm.cninfo.com.cn":          "cninfo",
    "hithink":                    "hithink-ths",
    "hithink-finance":            "hithink-ths",
    "worldmonitor":               "worldmonitor",
    "worldmonitor.app":           "worldmonitor",
    "108 RSS 源":                 "rss-newsradar",
    "RSS":                         "rss-newsradar",
    "newsradar":                  "rss-newsradar",
}

# 数据源 code → 提供的实体类型（从 ARCHITECTURE.md 数据流图 + 已灌入实体推断）
SOURCE_PROVIDES: dict[str, list[str]] = {
    "tencent":            ["stocks", "valuations", "metrics"],
    "eastmoney-push2":   ["stocks", "valuations", "metrics", "dragon-tiger", "events", "reports"],
    "eastmoney-push2ex": ["stocks", "valuations"],
    "eastmoney-datacenter": ["dragon-tiger", "events", "metrics"],
    "eastmoney-reportapi": ["reports"],
    "eastmoney-searchapi": ["stocks"],
    "akshare":            ["industries", "metrics"],
    "baostock":           ["stocks", "valuations"],
    "mootdx":             ["stocks", "valuations"],
    "baidu-stock":        ["stocks", "valuations"],
    "sina-financial":     ["stocks", "valuations", "metrics"],
    "cninfo":             ["stocks", "events"],
    "hithink-ths":        ["stocks", "valuations", "metrics", "events"],
    "worldmonitor":       ["industries", "metrics", "events"],
    "rss-newsradar":      ["events"],
    "fred":               ["metrics"],
}

# ──────────────────────────────────────────────────────────────────────────
# 实体词典辅助
# ──────────────────────────────────────────────────────────────────────────


def load_dictionary(vault_root: Path) -> dict:
    """加载实体词典，返 {aliases, by_type}（文件不存在返空结构）。"""
    dict_path = vault_root / INVESTING_DIRNAME / DICTIONARY_NAME
    if not dict_path.is_file():
        return {"aliases": {}, "by_type": {}}
    try:
        with dict_path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"aliases": {}, "by_type": {}}


def lookup_entity(dictionary: dict, alias: str) -> tuple[str, str] | None:
    """查词典：alias → (vault 相对路径 stem, type)。无则 None。

    stem 去掉 `.md` 与目录前缀，返回形如 `data-sources/tencent`。
    """
    info = dictionary.get("aliases", {}).get(alias)
    if not info:
        return None
    path = info.get("path", "")
    etype = info.get("type", "")
    if not path:
        return None
    # 词典里的 path 已是 `data-sources/tencent` 形式（无 .md）
    return (path, etype)


def resolve_source_link(dictionary: dict, code: str) -> str | None:
    """数据源 code → `[[data-sources/xxx]]` 链接字符串。查词典确认存在。"""
    # 先直接查 code（如 "tencent"）
    hit = lookup_entity(dictionary, code)
    if hit and hit[1] == "data_source":
        return f"[[{hit[0]}]]"
    # fallback：code 不在词典，用 MODULE_TO_SOURCE 表的硬编码路径
    for _mod, (stem, src_code, _provides) in MODULE_TO_SOURCE.items():
        if src_code == code and stem:
            # 验证实体文件存在（通过 by_type）
            if code in dictionary.get("by_type", {}).get("data_source", []):
                return f"[[{stem}]]"
            # 词典 by_type 无但硬编码表有——仍建链（stub 可能存在）
            return f"[[{stem}]]"
    return None


def resolve_spec_link(dictionary: dict, number: str) -> str | None:
    """spec 编号 → `[[specs/SNNN-xxx]]` 链接。查 by_type.spec 确认存在。"""
    if number in dictionary.get("by_type", {}).get("spec", []):
        # 在 aliases 里找该编号对应 path
        hit = lookup_entity(dictionary, number)
        if hit and hit[1] == "spec":
            return f"[[{hit[0]}]]"
    return None


# ──────────────────────────────────────────────────────────────────────────
# P4-1：AST 扫 data/sources/*.py → 函数 → 数据源 关系
# ──────────────────────────────────────────────────────────────────────────


def scan_source_module(file_path: Path, module_stem: str) -> dict:
    """AST 扫单个数据源模块，返 {module, docstring, functions, source_code}。

    source_code 为 None 时表示该模块非数据源（如 _common / cyq_js / kline_resolver）。
    """
    try:
        src = file_path.read_text(encoding="utf-8")
    except OSError:
        return {"module": module_stem, "docstring": "", "functions": [], "source_code": None}

    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {"module": module_stem, "docstring": "", "functions": [], "source_code": None}

    docstring = ast.get_docstring(tree) or ""
    functions = [
        n.name for n in tree.body
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")
    ]

    mapping = MODULE_TO_SOURCE.get(module_stem)
    source_code = mapping[1] if mapping else None

    return {
        "module": module_stem,
        "docstring": docstring,
        "functions": functions,
        "source_code": source_code,
    }


def scan_all_sources(vibe_root: Path) -> list[dict]:
    """扫 backend/data/sources/*.py 全部模块。"""
    src_dir = vibe_root / VR_SOURCES_DIR
    if not src_dir.is_dir():
        return []
    results: list[dict] = []
    for py_file in sorted(src_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        stem = py_file.stem
        info = scan_source_module(py_file, stem)
        results.append(info)
    return results


def extract_function_to_source_relations(scanned: list[dict], dictionary: dict) -> list[dict]:
    """从扫描结果生成 函数 → 数据源 关系列表。

    每条：{from_func, source_code, source_link, confidence, origin}
    函数名用全限定形式 `data.sources.<module>.<func>`（对齐 ARCHITECTURE.md 迁后路径）。
    """
    relations: list[dict] = []
    for mod in scanned:
        if not mod["source_code"]:
            continue
        link = resolve_source_link(dictionary, mod["source_code"])
        if not link:
            continue
        for fn in mod["functions"]:
            relations.append({
                "from_func": f"data.sources.{mod['module']}.{fn}",
                "source_code": mod["source_code"],
                "source_link": link,
                "confidence": "high",
                "origin": f"backend/data/sources/{mod['module']}.py",
            })
    return relations


# ──────────────────────────────────────────────────────────────────────────
# P4-2：AST 扫 stock_tools.py → 工具 → 函数 关系
# ──────────────────────────────────────────────────────────────────────────


def scan_stock_tools(vibe_root: Path) -> list[dict]:
    """AST 扫 stock_tools.py，提取 @register_tool 工具名 + 函数体内调用。

    返回 [{tool_name, func_name, calls: [(module, func), ...]}]
    """
    tools_path = vibe_root / VR_STOCK_TOOLS
    if not tools_path.is_file():
        return []
    try:
        src = tools_path.read_text(encoding="utf-8")
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return []

    results: list[dict] = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        # 找 @register_tool("工具名", ...) 装饰器
        tool_name = None
        for dec in node.decorator_list:
            call = dec if isinstance(dec, ast.Call) else None
            if call is None:
                continue
            func = call.func
            # register_tool（裸名）或 xxx.register_tool
            if isinstance(func, ast.Name) and func.id == "register_tool":
                pass
            elif isinstance(func, ast.Attribute) and func.attr == "register_tool":
                pass
            else:
                continue
            # 第一个位置参数是工具名
            if call.args and isinstance(call.args[0], ast.Constant):
                tool_name = call.args[0].value
                break
        if not tool_name:
            continue

        # 扫函数体内的 astock.xxx / gstock.xxx / data.sources.xxx.yyy 调用
        calls: list[tuple[str, str]] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                f = child.func
                # astock.tencent_quote → ("astock", "tencent_quote")
                if isinstance(f.value, ast.Name):
                    mod = f.value.id
                    if mod in ("astock", "gstock"):
                        calls.append((mod, f.attr))
                # data.sources.hithink_src.skyrocket → ("data.sources.hithink_src", "skyrocket")
                elif isinstance(f.value, ast.Attribute):
                    # f.value = Attribute(value=Name('sources'), attr='hithink_src')
                    if (
                        isinstance(f.value.value, ast.Name)
                        and f.value.value.id == "data"
                        and f.value.attr
                    ):
                        mod_full = f"data.sources.{f.value.attr}"
                        calls.append((mod_full, f.attr))

        results.append({
            "tool_name": tool_name,
            "func_name": node.name,
            "calls": calls,
        })
    return results


def extract_tool_to_function_relations(tools: list[dict], dictionary: dict) -> list[dict]:
    """工具 → 函数 → 数据源 关系链。

    每条：{tool_name, called_func, source_code, source_link, confidence}
    called_func 用全限定 `astock.tencent_quote` 形式。
    """
    relations: list[dict] = []
    for t in tools:
        for mod, func in t["calls"]:
            # astock.tencent_quote → 映射到 data-sources/tencent（通过函数名归一）
            source_code = map_function_to_source_code(func)
            source_link = resolve_source_link(dictionary, source_code) if source_code else None
            relations.append({
                "tool_name": t["tool_name"],
                "called_func": f"{mod}.{func}",
                "source_code": source_code or "",
                "source_link": source_link or "",
                "confidence": "high",
                "origin": VR_STOCK_TOOLS,
            })
    return relations


def map_function_to_source_code(func_name: str) -> str | None:
    """被调函数名 → 数据源 code 归一（基于 ARCHITECTURE.md 执行映射 + 函数名前缀）。

    ARCHITECTURE.md §"执行映射"段已明示：
      query_quote→astock.tencent_quote、query_valuation→astock.full_valuation、
      query_reports→astock.eastmoney_reports、query_news→astock.stock_news、
      query_global_stock→gstock.us_hk_stock
    """
    # 显式映射（ARCHITECTURE.md 明示）
    explicit = {
        "tencent_quote": "tencent",
        "full_valuation": "eastmoney-push2",   # 估值聚合东财+同花顺，主源东财
        "eastmoney_reports": "eastmoney-reportapi",
        "stock_news": "akshare",               # akshare.stock_news_em
        "us_hk_stock": "eastmoney-push2",      # 美股港股走东财 push2
        "skyrocket": "hithink-ths",
        "hot_stock": "hithink-ths",
        "anomaly_list": "hithink-ths",
    }
    if func_name in explicit:
        return explicit[func_name]
    # 前缀归一
    if func_name.startswith("tencent_") or func_name.startswith("fetch_raw") and "tencent" in func_name:
        return "tencent"
    if func_name.startswith("eastmoney_") or func_name.startswith("em_"):
        return "eastmoney-push2"
    if func_name.startswith("akshare_") or func_name == "stock_news":
        return "akshare"
    if func_name.startswith("baostock_"):
        return "baostock"
    if func_name.startswith("mootdx_"):
        return "mootdx"
    if func_name.startswith("sina_"):
        return "sina-financial"
    if func_name.startswith("baidu_"):
        return "baidu-stock"
    if func_name.startswith("cninfo_") or func_name == "investor_qa":
        return "cninfo"
    if func_name.startswith("hithink_") or func_name in ("skyrocket", "hot_stock", "anomaly_list"):
        return "hithink-ths"
    if func_name.startswith("worldmonitor_") or func_name.startswith("fetch_"):
        return "worldmonitor"
    return None


# ──────────────────────────────────────────────────────────────────────────
# P4-3：正则扫 ARCHITECTURE.md 数据流图 → 数据源 → 实体类型
# ──────────────────────────────────────────────────────────────────────────


def extract_arch_dataflow(arch_text: str, dictionary: dict) -> list[dict]:
    """从 ARCHITECTURE.md 一图概览数据流图抓外部源 → 数据源实体 关系。

    每条：{source_code, source_link, endpoint, feeds_into, confidence}
    feeds_into 是 ARCHITECTURE.md 数据流图里源行箭头右侧的 backend 模块。
    """
    relations: list[dict] = []
    # 只扫代码块内的数据流图（``` ... ``` 之间）
    in_code_block = False
    for line in arch_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            continue
        # 匹配"源名 (端点) ────► ..."行
        m = ARCH_DATAFLOW_LINE_RE.match(line)
        if not m:
            continue
        source_name = m.group("source").strip()
        endpoint = m.group("endpoint").strip()
        rest = m.group("rest").strip()

        # 源名/端点归一到数据源 code
        code = None
        # 先端点精确匹配
        for ep_key, src_code in ENDPOINT_TO_SOURCE_CODE.items():
            if ep_key == endpoint or ep_key in source_name:
                code = src_code
                break
        if not code:
            # 源名前缀归一
            for name_fragment, src_code in [
                ("腾讯", "tencent"), ("东财", "eastmoney-push2"),
                ("akshare", "akshare"), ("mootdx", "mootdx"),
                ("新浪", "sina-financial"), ("巨潮", "cninfo"),
                ("同花顺", "hithink-ths"), ("worldmonitor", "worldmonitor"),
                ("RSS", "rss-newsradar"), ("百度", "baidu-stock"),
            ]:
                if name_fragment in source_name:
                    code = src_code
                    break
        if not code:
            continue

        link = resolve_source_link(dictionary, code)
        if not link:
            continue

        # feeds_into 从 rest 抓（如 "astock.py (A股全栈)"）
        feeds_into = rest.split()[0] if rest else ""

        relations.append({
            "source_code": code,
            "source_link": link,
            "endpoint": endpoint,
            "feeds_into": feeds_into,
            "confidence": "high",
            "origin": "ARCHITECTURE.md#数据流图",
        })
    return relations


def extract_source_to_entity_relations(arch_relations: list[dict]) -> list[dict]:
    """从 ARCHITECTURE.md 关系派生 数据源 → 实体类型 关系。

    每条：{source_code, source_link, entity_type, confidence}
    entity_type 取 SOURCE_PROVIDES 表的值。
    """
    relations: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for r in arch_relations:
        code = r["source_code"]
        provides = SOURCE_PROVIDES.get(code, [])
        for etype in provides:
            key = (code, etype)
            if key in seen:
                continue
            seen.add(key)
            relations.append({
                "source_code": code,
                "source_link": r["source_link"],
                "entity_type": etype,
                "confidence": "medium",   # ARCHITECTURE.md 推断，非代码直接证明
                "origin": "ARCHITECTURE.md#数据流图(推断)",
            })
    return relations


# ──────────────────────────────────────────────────────────────────────────
# P4-4：spec → 数据源 关系（从 vault specs/*.md 的"## 关联"段抓 [[]] 链接）
# ──────────────────────────────────────────────────────────────────────────


# spec 文件 frontmatter number 提取
SPEC_FM_NUMBER_RE = re.compile(r"^number:\s*(S\d{3})\s*$", re.MULTILINE)
# ## 关联 段落定位
SPEC_RELATION_SECTION_RE = re.compile(
    r"^##\s*关联\s*$.*?(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
# [[data-sources/xxx]] 链接提取
DATA_SOURCE_LINK_RE = re.compile(r"\[\[data-sources/([^\]|]+)(?:\|[^\]]*)?\]\]")


def extract_spec_to_source_relations(specs_dir: Path, dictionary: dict) -> list[dict]:
    """扫 vault specs/*.md，从"## 关联"段抓 spec → 数据源 关系。

    每条：{spec_number, spec_link, source_code, source_link, confidence, origin}
    """
    relations: list[dict] = []
    if not specs_dir.is_dir():
        return relations
    for spec_file in sorted(specs_dir.glob("S*.md")):
        try:
            text = spec_file.read_text(encoding="utf-8")
        except OSError:
            continue
        # 提取 spec 编号
        m = SPEC_FM_NUMBER_RE.search(text)
        if not m:
            # 从文件名提取
            stem_match = re.match(r"(S\d{3})", spec_file.stem)
            if not stem_match:
                continue
            spec_number = stem_match.group(1)
        else:
            spec_number = m.group(1)

        spec_link = resolve_spec_link(dictionary, spec_number) or f"[[{specs_dir.name}/{spec_file.stem}]]"

        # 抓 ## 关联 段
        section_match = SPEC_RELATION_SECTION_RE.search(text)
        if not section_match:
            continue
        section_text = section_match.group(0)
        # 找所有 [[data-sources/xxx]] 链接
        for link_match in DATA_SOURCE_LINK_RE.finditer(section_text):
            source_stem = link_match.group(1).strip()
            # source_stem 形如 "akshare" / "tencent" / ""（目录链接）
            if not source_stem:
                continue
            # 归一：去尾斜杠
            source_code = source_stem.rstrip("/")
            source_link = f"[[data-sources/{source_code}]]"
            relations.append({
                "spec_number": spec_number,
                "spec_link": spec_link,
                "source_code": source_code,
                "source_link": source_link,
                "confidence": "high",
                "origin": str(spec_file.relative_to(specs_dir.parent.parent.parent)),
            })
    return relations


# ──────────────────────────────────────────────────────────────────────────
# vault 写入层
# ──────────────────────────────────────────────────────────────────────────


def split_frontmatter(text: str) -> tuple[str, str, str]:
    """拆 markdown 为 (frontmatter块含---, 正文, 正文后追加位置)。

    frontmatter 块含首尾 `---`；无 frontmatter 则前部为空。
    返回 (fm_text, body_text, body_end_offset)，body_end_offset 是正文末尾字符偏移。
    """
    if not text.startswith("---"):
        return ("", text, len(text))
    # 找第二个 ---
    second = text.find("\n---", 3)
    if second == -1:
        return ("", text, len(text))
    fm_text = text[: second + 4]  # 含 \n---
    body_text = text[second + 4:]
    # body_text 开头可能有 \n
    return (fm_text, body_text, len(text))


def find_generated_section(body_text: str, section_title: str) -> tuple[int, int] | None:
    """在正文中找本脚本生成的段落区间（含 GENERATED_TAG + 标题 + 内容到下个 ## 或文末）。

    返回 (start_offset_in_body, end_offset_in_body)，未找到返回 None。
    """
    tag_idx = body_text.find(GENERATED_TAG)
    if tag_idx == -1:
        return None
    # 从 tag 往后找 ## 标题
    title_idx = body_text.find(f"\n## {section_title}", tag_idx)
    if title_idx == -1:
        # 也许是文末无换行
        title_idx = body_text.find(f"## {section_title}", tag_idx)
    if title_idx == -1:
        return None
    # 找段落结束（下一个 ## 标题 或文末）
    next_section = body_text.find("\n## ", title_idx + 1)
    if next_section == -1:
        end = len(body_text)
    else:
        end = next_section
    return (tag_idx, end)


def update_data_source_file(
    file_path: Path,
    source_code: str,
    tool_relations: list[dict],
    func_relations: list[dict],
    spec_relations: list[dict],
    entity_relations: list[dict],
    dry_run: bool,
    quiet: bool,
) -> bool:
    """更新单个 data-sources/*.md 文件。

    追加/刷新 `## 数据流关系` 段（含工具链接 + 函数列表 + spec 引用 + 提供实体类型）。
    返回是否实际改写。
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return False

    # 过滤出与本数据源相关的关系
    my_tools = [r for r in tool_relations if r.get("source_code") == source_code]
    my_funcs = [r for r in func_relations if r.get("source_code") == source_code]
    my_specs = [r for r in spec_relations if r.get("source_code") == source_code]
    my_entities = [r for r in entity_relations if r.get("source_code") == source_code]

    # 构建新段内容
    lines: list[str] = [GENERATED_TAG, "", f"## 数据流关系", ""]
    has_content = False

    # 工具链接段
    if my_tools:
        has_content = True
        lines.append("**相关工具**：")
        seen_tools: set[str] = set()
        for r in my_tools:
            t = r["tool_name"]
            if t in seen_tools:
                continue
            seen_tools.add(t)
            lines.append(f"- `{t}` → `{r['called_func']}`")
        lines.append("")

    # 函数列表
    if my_funcs:
        has_content = True
        lines.append("**对应函数**（`backend/data/sources/`）：")
        for r in my_funcs:
            lines.append(f"- `{r['from_func']}`")
        lines.append("")

    # 引用该数据源的 spec
    if my_specs:
        has_content = True
        lines.append("**关联 spec**：")
        seen_specs: set[str] = set()
        for r in my_specs:
            s = r["spec_number"]
            if s in seen_specs:
                continue
            seen_specs.add(s)
            lines.append(f"- {r['spec_link']}（{s}）")
        lines.append("")

    # 提供的实体类型
    if my_entities:
        has_content = True
        lines.append("**喂给实体类型**：")
        seen_etypes: set[str] = set()
        for r in my_entities:
            e = r["entity_type"]
            if e in seen_etypes:
                continue
            seen_etypes.add(e)
            lines.append(f"- [[{e}/]]")
        lines.append("")

    if not has_content:
        return False

    new_section = "\n".join(lines)

    # 幂等：找已有生成段
    fm_text, body_text, _ = split_frontmatter(text)
    existing = find_generated_section(body_text, "数据流关系")
    if existing is not None:
        start, end = existing
        old_section = body_text[start:end]
        if old_section.strip() == new_section.strip():
            return False  # 内容一致，跳过
        # 替换
        new_body = body_text[:start] + new_section + body_text[end:]
    else:
        # 追加到文末（保证前面有换行）
        sep = "" if body_text.endswith("\n\n") or not body_text else "\n"
        if body_text and not body_text.endswith("\n"):
            sep = "\n\n"
        new_body = body_text + sep + new_section

    new_text = fm_text + new_body
    if not fm_text:
        # 无 frontmatter 的文件（不该出现，但兜底）
        new_text = new_body

    if dry_run:
        if not quiet:
            print(f"[DRY-RUN] 将更新：{file_path.name}")
        return True

    file_path.write_text(new_text, encoding="utf-8")
    return True


def update_spec_file(
    file_path: Path,
    spec_number: str,
    source_relations: list[dict],
    dictionary: dict,
    dry_run: bool,
    quiet: bool,
) -> bool:
    """更新单个 specs/*.md 的"## 关联"段，补缺失的数据源链接。

    设计原则：spec 是最高优先级源，不覆盖已有数据源链接，只补缺失。
    返回是否实际改写。
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return False

    # 过滤出与本 spec 相关的数据源关系
    my_sources = [r for r in source_relations if r.get("spec_number") == spec_number]
    if not my_sources:
        return False

    # 找 ## 关联 段
    section_match = SPEC_RELATION_SECTION_RE.search(text)
    if not section_match:
        return False  # 无关联段，不新建（spec stub 由 P2 生成，不在此扩段）

    section_text = section_match.group(0)
    # 已有的数据源链接集合
    existing_codes: set[str] = set()
    for link_match in DATA_SOURCE_LINK_RE.finditer(section_text):
        stem = link_match.group(1).strip().rstrip("/")
        if stem:
            existing_codes.add(stem)

    # 找 "数据源：" 行（如 "- 数据源：[[data-sources/akshare]] ..."）
    datasource_line_pattern = re.compile(
        r"^(-\s*数据源[：:].*)$", re.MULTILINE
    )
    ds_line_match = datasource_line_pattern.search(section_text)
    new_links: list[str] = []
    for r in my_sources:
        code = r["source_code"]
        if code in existing_codes:
            continue
        # 确认数据源实体存在
        if not resolve_source_link(dictionary, code):
            continue
        new_links.append(f"[[data-sources/{code}]]")

    if not new_links:
        return False  # 无新增

    if ds_line_match:
        # 在已有 数据源 行末尾追加新链接
        old_line = ds_line_match.group(1)
        addition = " ".join(new_links)
        new_line = old_line.rstrip() + " " + addition
        new_section = section_text.replace(old_line, new_line, 1)
    else:
        # 无 数据源 行，在 ## 关联 段首插一行
        addition = "- 数据源：" + " ".join(new_links) + "\n"
        # 在 ## 关联 标题行后插入
        new_section = re.sub(
            r"^(##\s*关联\s*\n)",
            r"\1" + addition,
            section_text,
            count=1,
        )

    new_text = text[: section_match.start()] + new_section + text[section_match.end():]
    if dry_run:
        if not quiet:
            print(f"[DRY-RUN] 将更新 spec：{file_path.name}（+{len(new_links)} 数据源链接）")
        return True

    file_path.write_text(new_text, encoding="utf-8")
    return True


# ──────────────────────────────────────────────────────────────────────────
# 报告生成
# ──────────────────────────────────────────────────────────────────────────


def write_report(
    docs_dir: Path,
    func_relations: list[dict],
    tool_relations: list[dict],
    arch_relations: list[dict],
    entity_relations: list[dict],
    spec_relations: list[dict],
    updated_sources: list[str],
    updated_specs: list[str],
    today_str: str,
) -> None:
    """生成 docs/relation-extraction-report.md。"""
    docs_dir.mkdir(parents=True, exist_ok=True)
    report_path = docs_dir / REPORT_NAME

    # 按 source_code 分组统计
    by_source: dict[str, list[dict]] = {}
    for r in func_relations + tool_relations + arch_relations + entity_relations + spec_relations:
        code = r.get("source_code", "")
        if not code:
            continue
        by_source.setdefault(code, []).append(r)

    lines: list[str] = [
        "---",
        f"type: pipeline-report",
        f"pipeline: P4-relation-extraction",
        f"date: {today_str}",
        "---",
        "",
        f"# 关系抽取报告（{today_str}）",
        "",
        "> P4 `extract_relations.py` 生成。从 Vibe-Research 代码 + ARCHITECTURE.md + vault specs 抽取数据流关系。",
        "",
        "## 摘要",
        "",
        f"- 函数→数据源 关系：**{len(func_relations)}** 条",
        f"- 工具→函数 关系：**{len(tool_relations)}** 条",
        f"- ARCHITECTURE 数据流图 关系：**{len(arch_relations)}** 条",
        f"- 数据源→实体类型 关系：**{len(entity_relations)}** 条",
        f"- spec→数据源 关系：**{len(spec_relations)}** 条",
        f"- **总计：{len(func_relations) + len(tool_relations) + len(arch_relations) + len(entity_relations) + len(spec_relations)}** 条",
        "",
        f"- 更新数据源实体文件：**{len(updated_sources)}** 个",
        f"- 更新 spec 文件：**{len(updated_specs)}** 个",
        "",
        "## 按数据源分组",
        "",
        "| 数据源 | 函数关系 | 工具关系 | spec 引用 | 实体类型 | 总计 |",
        "|---|---|---|---|---|---|",
    ]
    for code in sorted(by_source.keys()):
        rels = by_source[code]
        f_count = sum(1 for r in rels if "from_func" in r)
        t_count = sum(1 for r in rels if "tool_name" in r)
        s_count = sum(1 for r in rels if "spec_number" in r)
        e_count = sum(1 for r in rels if "entity_type" in r)
        a_count = sum(1 for r in rels if "endpoint" in r)
        total = len(rels)
        lines.append(f"| `{code}` | {f_count} | {t_count} | {s_count} | {e_count + a_count} | {total} |")

    lines.extend([
        "",
        "## 更新的文件",
        "",
        "### data-sources/ 更新",
        "",
    ])
    if updated_sources:
        for name in sorted(updated_sources):
            lines.append(f"- `data-sources/{name}`")
    else:
        lines.append("- （无更新，所有关系段已最新）")

    lines.append("")
    lines.append("### specs/ 更新")
    lines.append("")
    if updated_specs:
        for name in sorted(updated_specs):
            lines.append(f"- `specs/{name}`")
    else:
        lines.append("- （无更新，所有关联段已含数据源链接）")

    lines.extend([
        "",
        "## 关系类型说明",
        "",
        "| 关系类型 | 来源 | 置信度 | 说明 |",
        "|---|---|---|---|",
        "| 函数→数据源 | `backend/data/sources/*.py` AST | high | 模块名归一到数据源实体 |",
        "| 工具→函数 | `stock_tools.py` `@register_tool` | high | 装饰器抓工具名，函数体抓被调函数 |",
        "| ARCHITECTURE 数据流 | `ARCHITECTURE.md` 一图概览 | high | 正则匹配外部源行 |",
        "| 数据源→实体类型 | `ARCHITECTURE.md` 推断 | medium | 从数据流图 + 已灌入实体推断 |",
        "| spec→数据源 | vault `specs/*.md` 关联段 | high | 抓 `[[]]` 链接 |",
        "",
        "## 冲突处理（优先级）",
        "",
        "同一实体被多源抽取时，优先级：spec > 代码 AST > 文档注释 > LLM 推断。",
        "本脚本只处理 spec/代码/ARCHITECTURE 三个 high/medium 源，不涉及 LLM 推断。",
        "",
        f"> {GENERATED_TAG}",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────


def run(
    vault_root: Path,
    vibe_root: Path,
    dry_run: bool = False,
    quiet: bool = False,
) -> int:
    investing_dir = vault_root / INVESTING_DIRNAME
    sources_dir = investing_dir / SOURCES_SUBDIR
    specs_dir = investing_dir / SPECS_SUBDIR
    docs_dir = vault_root / DOCS_SUBDIR

    # 源文件存在性校验
    arch_path = vibe_root / VR_ARCH
    src_dir = vibe_root / VR_SOURCES_DIR
    tools_path = vibe_root / VR_STOCK_TOOLS

    if not arch_path.is_file():
        print(f"[ERROR] 找不到 ARCHITECTURE.md：{arch_path}", file=sys.stderr)
        return 2
    if not src_dir.is_dir():
        print(f"[ERROR] 找不到数据源目录：{src_dir}", file=sys.stderr)
        return 2
    if not sources_dir.is_dir():
        print(f"[ERROR] vault data-sources 目录不存在：{sources_dir}", file=sys.stderr)
        return 2

    dictionary = load_dictionary(vault_root)

    # ── P4-1：AST 扫 data/sources/*.py ──
    scanned = scan_all_sources(vibe_root)
    func_relations = extract_function_to_source_relations(scanned, dictionary)

    # ── P4-2：AST 扫 stock_tools.py ──
    if tools_path.is_file():
        tools = scan_stock_tools(vibe_root)
        tool_relations = extract_tool_to_function_relations(tools, dictionary)
    else:
        tools = []
        tool_relations = []

    # ── P4-3：正则扫 ARCHITECTURE.md 数据流图 ──
    try:
        arch_text = arch_path.read_text(encoding="utf-8")
    except OSError:
        arch_text = ""
    arch_relations = extract_arch_dataflow(arch_text, dictionary)
    entity_relations = extract_source_to_entity_relations(arch_relations)

    # ── P4-4：扫 vault specs/*.md 的 spec → 数据源 关系 ──
    spec_relations = extract_spec_to_source_relations(specs_dir, dictionary)

    total = (
        len(func_relations) + len(tool_relations)
        + len(arch_relations) + len(entity_relations)
        + len(spec_relations)
    )

    # ── 写入层：更新 data-sources/*.md ──
    updated_sources: list[str] = []
    for src_file in sorted(sources_dir.glob("*.md")):
        if src_file.name == "index.md":
            continue
        # 文件名 stem（如 tencent）→ 数据源 code
        stem = src_file.stem
        # 在 by_type.data_source 里找匹配（stem 直接是 code 的情况）
        source_code = stem
        # 校验 code 在词典或硬编码表
        known_codes = set(SOURCE_PROVIDES.keys()) | {
            m[1] for m in MODULE_TO_SOURCE.values() if m[1]
        }
        if source_code not in known_codes:
            continue
        changed = update_data_source_file(
            src_file, source_code,
            tool_relations, func_relations, spec_relations, entity_relations,
            dry_run, quiet,
        )
        if changed:
            updated_sources.append(src_file.name)

    # ── 写入层：更新 specs/*.md（补缺失数据源链接） ──
    updated_specs: list[str] = []
    if specs_dir.is_dir():
        for spec_file in sorted(specs_dir.glob("S*.md")):
            # 提取 spec 编号
            try:
                text = spec_file.read_text(encoding="utf-8")
            except OSError:
                continue
            m = SPEC_FM_NUMBER_RE.search(text)
            if not m:
                stem_match = re.match(r"(S\d{3})", spec_file.stem)
                if not stem_match:
                    continue
                spec_number = stem_match.group(1)
            else:
                spec_number = m.group(1)
            changed = update_spec_file(
                spec_file, spec_number, spec_relations, dictionary,
                dry_run, quiet,
            )
            if changed:
                updated_specs.append(spec_file.name)

    # ── 生成报告 ──
    today_str = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")
    if not dry_run:
        write_report(
            docs_dir,
            func_relations, tool_relations, arch_relations,
            entity_relations, spec_relations,
            updated_sources, updated_specs, today_str,
        )

    if not quiet:
        print("")
        print(f"=== 关系抽取完成（{today_str}）===")
        print(f"扫描数据源模块：{len(scanned)} 个（其中数据源实体：{sum(1 for s in scanned if s['source_code'])}）")
        print(f"扫描工具：{len(tools)} 个（@register_tool）")
        print(f"函数→数据源 关系：{len(func_relations)} 条")
        print(f"工具→函数 关系：{len(tool_relations)} 条")
        print(f"ARCHITECTURE 数据流图 关系：{len(arch_relations)} 条")
        print(f"数据源→实体类型 关系：{len(entity_relations)} 条")
        print(f"spec→数据源 关系：{len(spec_relations)} 条")
        print(f"总计：{total} 条")
        print(f"更新 data-sources/ 文件：{len(updated_sources)} 个")
        print(f"更新 specs/ 文件：{len(updated_specs)} 个")
        if dry_run:
            print("(dry-run 模式，未写文件 + 未生成报告)")
        else:
            print(f"报告：{docs_dir / REPORT_NAME}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="从 Vibe-Research 代码 + ARCHITECTURE.md 抽取数据流关系到 vault",
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
        help="只打印将要更新的文件，不实际写入",
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
