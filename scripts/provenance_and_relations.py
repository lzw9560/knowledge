#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""任务 1+2：LLM 内容溯源标记 + 关系稀疏治理。

任务 1：给 411 个 stocks 文件 frontmatter 加 provenance/verified/ensure confidence。
任务 2：从后端 API 拉研报/龙虎榜/新闻数据，在正文对应段补真实数据。

幂等：重复执行不会破坏已有真实数据，只补充占位段。
设计文档见 AGENTS.md / 任务说明。
"""
from __future__ import annotations

import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests

# --------------------------------------------------------------------------- #
# 路径
# --------------------------------------------------------------------------- #
VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault")
STOCKS_DIR = VAULT / "10_Reference" / "investing" / "stocks"
HOME_PAGE = VAULT / "🏠 首页.md"
API_BASE = "http://localhost:8900"

# --------------------------------------------------------------------------- #
# Frontmatter 工具
# --------------------------------------------------------------------------- #
_FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def read_fm(content: str) -> dict[str, str]:
    """读扁平 frontmatter（只取字符串值，list 不需要）。"""
    m = _FM_RE.match(content)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith(("[",)):
            continue  # 跳过 list
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            val = val[1:-1]
        fm[key] = val
    return fm


def update_fm_provenance(content: str) -> tuple[str, bool]:
    """任务 1：给 frontmatter 加 provenance/verified，确保 confidence 存在。

    返回 (新内容, 是否修改)。
    """
    m = _FM_RE.match(content)
    if not m:
        return content, False
    fm_block = m.group(1)
    changed = False
    new_lines: list[str] = []
    has_provenance = False
    has_verified = False
    has_confidence = False

    for line in fm_block.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        if ":" not in line:
            new_lines.append(line)
            continue
        key = line.split(":", 1)[0].strip()
        if key == "provenance":
            has_provenance = True
        elif key == "verified":
            has_verified = True
        elif key == "confidence":
            has_confidence = True
        new_lines.append(line)

    # 追加缺失字段（在末尾追加，保持现有顺序）
    additions: list[str] = []
    if not has_provenance:
        additions.append("provenance: llm-generated")
    if not has_confidence:
        additions.append("confidence: medium")
    if not has_verified:
        additions.append("verified: false")

    if not additions:
        return content, False

    # 在 frontmatter 末尾插入（最后一行若是空行则先补）
    new_fm = "\n".join(new_lines).rstrip() + "\n" + "\n".join(additions) + "\n"
    new_content = f"---\n{new_fm}---" + content[m.end():]
    return new_content, True


# --------------------------------------------------------------------------- #
# API 客户端
# --------------------------------------------------------------------------- #
class APIError(Exception):
    pass


def _create_session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    return s


def fetch_reports(sess: requests.Session, code: str) -> list[dict]:
    try:
        r = sess.get(f"{API_BASE}/api/reports?code={code}", timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])
        return data if isinstance(data, list) else []
    except Exception as e:
        raise APIError(f"reports {code}: {e}") from e


def fetch_dragon_tiger(sess: requests.Session, code: str) -> dict:
    """返回 {'records': [], 'institution': {...}, 'seats': {...}}。"""
    try:
        r = sess.get(f"{API_BASE}/api/dragon-tiger?code={code}", timeout=30)
        r.raise_for_status()
        data = r.json().get("data", {})
        if isinstance(data, list):
            return {"records": data, "institution": {}, "seats": {}}
        if isinstance(data, dict):
            return {
                "records": data.get("records", []) or [],
                "institution": data.get("institution", {}) or {},
                "seats": data.get("seats", {}) or {},
            }
        return {"records": [], "institution": {}, "seats": {}}
    except Exception as e:
        raise APIError(f"dragon-tiger {code}: {e}") from e


def fetch_news(sess: requests.Session, code: str, limit: int = 5) -> list[dict]:
    last_err: Exception | None = None
    for attempt in range(2):  # 重试一次
        try:
            r = sess.get(
                f"{API_BASE}/api/news?code={code}&limit={limit}", timeout=20
            )
            r.raise_for_status()
            data = r.json().get("data", [])
            return data if isinstance(data, list) else []
        except Exception as e:
            last_err = e
            if attempt == 0:
                time.sleep(0.5)
    raise APIError(f"news {code}: {last_err}") from last_err


# --------------------------------------------------------------------------- #
# 表格渲染
# --------------------------------------------------------------------------- #
def _md_escape_cell(s: str) -> str:
    """转义 markdown 表格管道符。"""
    if s is None:
        return "—"
    s = str(s).replace("\n", " ").replace("\r", " ").strip()
    return s.replace("|", "\\|") or "—"


def render_reports_table(reports: list[dict]) -> str:
    """渲染研报表格。列：日期 | 机构 | 分析师 | 评级 | 标题。"""
    lines = [
        "| 日期 | 机构 | 分析师 | 评级 | 标题 |",
        "|---|---|---|---|---|",
    ]
    if not reports:
        lines.append("| — | — | — | — | 暂无数据 |")
        return "\n".join(lines)
    for rep in reports[:10]:  # 最多 10 条
        date = _md_escape_cell(str(rep.get("publishDate", ""))[:10])
        org = _md_escape_cell(rep.get("orgSName") or rep.get("orgName") or "")
        author_raw = rep.get("author") or rep.get("researcher") or ""
        # author 可能是 ["11000440466.夏芈卬"] 或 "夏芈卬"
        if isinstance(author_raw, list):
            authors = [a.split(".")[-1] if "." in a else a for a in author_raw]
            author = ", ".join(authors)
        else:
            author = str(author_raw).split(".")[-1] if "." in str(author_raw) else str(author_raw)
        author = _md_escape_cell(author)
        rating = _md_escape_cell(
            rep.get("sRatingName") or rep.get("emRatingName") or "—"
        )
        title = _md_escape_cell(rep.get("title", ""))
        lines.append(f"| {date} | {org} | {author} | {rating} | {title} |")
    return "\n".join(lines)


def render_dragon_tiger_table(dt: dict) -> str:
    """渲染龙虎榜表格。列：日期 | 上榜原因 | 机构净额(万) | 换手率%。"""
    lines = [
        "| 日期 | 上榜原因 | 机构净额(万) | 换手率% |",
        "|---|---|---|---|",
    ]
    records = dt.get("records", [])
    if not records:
        lines.append("| — | — | — | — |")
        # 若有 institution 数据但无 records，补一行机构净额汇总
        inst = dt.get("institution", {}) or {}
        net = inst.get("net_amt")
        if net is not None and float(net) != 0:
            lines[-1] = f"| — | 机构净额汇总 | {float(net):.2f} | — |"
        else:
            lines[-1] = "| — | — | — | 暂无数据 |"
        return "\n".join(lines)
    for rec in records[:10]:
        date = _md_escape_cell(str(rec.get("date", ""))[:10])
        reason = _md_escape_cell(rec.get("reason", ""))
        net = rec.get("net_buy")
        net_str = f"{float(net):.2f}" if net is not None else "—"
        turnover = rec.get("turnover")
        turn_str = f"{float(turnover):.2f}" if turnover is not None else "—"
        lines.append(f"| {date} | {reason} | {net_str} | {turn_str} |")
    return "\n".join(lines)


def render_news_table(news: list[dict]) -> str:
    """渲染新闻/事件表格。列：日期 | 来源 | 标题。"""
    lines = [
        "| 日期 | 来源 | 标题 |",
        "|---|---|---|",
    ]
    if not news:
        lines.append("| — | — | 暂无数据 |")
        return "\n".join(lines)
    for item in news[:8]:
        date = _md_escape_cell(str(item.get("发布时间", ""))[:10])
        source = _md_escape_cell(item.get("文章来源", ""))
        title = _md_escape_cell(item.get("新闻标题", ""))
        lines.append(f"| {date} | {source} | {title} |")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 正文段替换
# --------------------------------------------------------------------------- #
# 已预编译块的正则（与 precompile_dataview.py 一致）
_PRECOMPILED_RE = re.compile(
    r"(<!-- dataview-precompiled:[a-f0-9]+ -->\n)(.*?)(\n<!-- /dataview-precompiled -->)",
    re.DOTALL,
)


def _replace_section_table(
    content: str,
    section_header: str,
    new_table: str,
    skip_if_has_data: bool = True,
) -> tuple[str, bool]:
    """替换某段（## 标题）下的第一个 precompiled 表格。

    section_header: 如 "## 📰 相关研报"
    new_table: 新表格内容（不含 precompiled 标记）
    skip_if_has_data: 若表格内已有真实数据（非占位符）则跳过，避免覆盖已有数据。

    返回 (新内容, 是否修改)。
    """
    # 定位段
    sec_re = re.compile(
        rf"({re.escape(section_header)}.*?)(?=## |\Z)",
        re.DOTALL,
    )
    sec_m = sec_re.search(content)
    if not sec_m:
        return content, False  # 段不存在（stub 文件无此段）
    sec_text = sec_m.group(1)

    # 在段内找第一个 precompiled 块
    def _replace_in_sec(m: re.Match) -> str:
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        # 判断是否占位（只有表头 + 一行全是 —）
        body_lines = body.strip().split("\n")
        if skip_if_has_data and len(body_lines) > 2:
            # 检查数据行（第三行起）是否全是占位
            data_lines = body_lines[2:]
            all_placeholder = all(
                ("—" in ln and "暂无数据" not in ln) for ln in data_lines
            )
            if not all_placeholder:
                return m.group(0)  # 有真实数据，保留
        return f"{prefix}{new_table}{suffix}"

    new_sec = _PRECOMPILED_RE.sub(_replace_in_sec, sec_text, count=1)
    if new_sec == sec_text:
        return content, False
    new_content = content[: sec_m.start()] + new_sec + content[sec_m.end():]
    return new_content, True


# --------------------------------------------------------------------------- #
# 单文件处理
# --------------------------------------------------------------------------- #
def process_stock(
    path: Path,
    sess: requests.Session,
    dry_run: bool = False,
) -> dict:
    """处理单个 stock 文件：任务1 frontmatter + 任务2 正文段。

    返回统计 dict。
    """
    name = path.name
    stats = {
        "file": name,
        "fm_changed": False,
        "reports_added": False,
        "dt_added": False,
        "news_added": False,
        "errors": [],
    }
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        stats["errors"].append(f"read: {e}")
        return stats

    original = content

    # 任务 1：frontmatter provenance
    content, fm_changed = update_fm_provenance(content)
    stats["fm_changed"] = fm_changed

    # 任务 2：从 frontmatter 取 code
    fm = read_fm(content)
    code = fm.get("code") or path.stem
    if not re.match(r"^\d{6}$", code):
        stats["errors"].append(f"invalid code: {code}")
        # 仍写 frontmatter 改动（若有）
        if content != original and not dry_run:
            path.write_text(content, encoding="utf-8")
        return stats

    # 并发拉三个 API
    reports: list[dict] = []
    dt: dict = {}
    news: list[dict] = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        f_rep = ex.submit(fetch_reports, sess, code)
        f_dt = ex.submit(fetch_dragon_tiger, sess, code)
        f_news = ex.submit(fetch_news, sess, code)
        for f in [f_rep, f_dt, f_news]:
            try:
                f.result()
            except APIError as e:
                stats["errors"].append(str(e))
        reports = f_rep.result() if not f_rep.exception() else []
        dt = f_dt.result() if not f_dt.exception() else {}
        news = f_news.result() if not f_news.exception() else []

    # 渲染并替换
    rep_table = render_reports_table(reports)
    content, rep_changed = _replace_section_table(
        content, "## 📰 相关研报", rep_table
    )
    stats["reports_added"] = rep_changed

    dt_table = render_dragon_tiger_table(dt)
    content, dt_changed = _replace_section_table(
        content, "## 🐉 龙虎榜", dt_table
    )
    stats["dt_added"] = dt_changed

    news_table = render_news_table(news)
    content, news_changed = _replace_section_table(
        content, "## ⚡ 相关事件", news_table
    )
    stats["news_added"] = news_changed

    if content != original and not dry_run:
        path.write_text(content, encoding="utf-8")
    return stats


# --------------------------------------------------------------------------- #
# 首页角标
# --------------------------------------------------------------------------- #
def update_home_page(dry_run: bool = False) -> bool:
    """在首页"关于本站"callout 加未校验内容角标。幂等。"""
    content = HOME_PAGE.read_text(encoding="utf-8")
    marker = "⚠️ 部分内容由 LLM 生成"
    if marker in content:
        return False
    # 在"关于本站" callout 的最后一行后追加
    callout_re = re.compile(
        r"(> \[!abstract\] 关于本站\n(?:>.*\n)*?>)(.*?)(\n\n)",
        re.DOTALL,
    )
    m = callout_re.search(content)
    if not m:
        # 兜底：在第一个 callout 块末尾追加
        new_line = "\n> ⚠️ 部分内容由 LLM 生成（行业地位/竞争力/风险），已标注 `provenance: llm-generated`，未经人工校验。"
        content = content.replace(
            "GitHub 私有仓同步，Codex/Claude 按 `README.md` 调用规则读取。",
            "GitHub 私有仓同步，Codex/Claude 按 `README.md` 调用规则读取。\n"
            "> ⚠️ 部分内容由 LLM 生成（行业地位/竞争力/风险），已标注 `provenance: llm-generated`，未经人工校验。",
            1,
        )
    else:
        new_line = "\n> ⚠️ 部分内容由 LLM 生成（行业地位/竞争力/风险），已标注 `provenance: llm-generated`，未经人工校验。"
        # 在 callout 块的最后一行后插入
        callout_block = m.group(0)
        # 找 callout 最后一行（> 开头）
        last_gt = callout_block.rfind("\n>", 0, callout_block.rfind("\n\n"))
        # 简单做法：在 callout 内容行后插入
        old_line = "GitHub 私有仓同步，Codex/Claude 按 `README.md` 调用规则读取。"
        new_line_text = old_line + "\n> ⚠️ 部分内容由 LLM 生成（行业地位/竞争力/风险），已标注 `provenance: llm-generated`，未经人工校验。"
        new_block = callout_block.replace(old_line, new_line_text, 1)
        content = content.replace(callout_block, new_block, 1)
    if not dry_run:
        HOME_PAGE.write_text(content, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def main():
    dry_run = "--dry-run" in sys.argv
    stats_only = "--stats-only" in sys.argv

    if stats_only:
        # 只统计现状，不调 API 不写文件
        _stats_only()
        return

    files = sorted(
        f for f in STOCKS_DIR.glob("*.md") if f.name != "index.md"
    )
    print(f"待处理 stocks 文件: {len(files)}")

    # 首页角标
    home_changed = update_home_page(dry_run=dry_run)
    print(f"首页角标: {'已加' if home_changed else '已存在跳过'}")

    # 8 线程并发处理 stocks
    total_fm = 0
    total_rep = 0
    total_dt = 0
    total_news = 0
    errors: list[str] = []
    t0 = time.time()

    # 每个线程一个 session（requests.Session 非线程安全）
    def _worker(path: Path) -> dict:
        sess = _create_session()
        return process_stock(path, sess, dry_run=dry_run)

    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(_worker, f): f for f in files}
        done = 0
        for fut in as_completed(futures):
            done += 1
            try:
                s = fut.result()
            except Exception as e:
                errors.append(f"{futures[fut].name}: {e}")
                continue
            if s["fm_changed"]:
                total_fm += 1
            if s["reports_added"]:
                total_rep += 1
            if s["dt_added"]:
                total_dt += 1
            if s["news_added"]:
                total_news += 1
            if s["errors"]:
                errors.extend(s["errors"])
            if done % 50 == 0:
                print(
                    f"  进度 {done}/{len(files)} | fm={total_fm} rep={total_rep} dt={total_dt} news={total_news} elapsed={time.time()-t0:.1f}s"
                )

    elapsed = time.time() - t0
    print("\n===== 汇总 =====")
    print(f"总文件: {len(files)}")
    print(f"frontmatter 加 provenance: {total_fm}")
    print(f"研报段补数据: {total_rep}")
    print(f"龙虎榜段补数据: {total_dt}")
    print(f"事件/新闻段补数据: {total_news}")
    print(f"首页角标: {'已加' if home_changed else '已存在'}")
    print(f"错误数: {len(errors)}")
    if errors[:10]:
        print("前10条错误:")
        for e in errors[:10]:
            print(f"  {e}")
    print(f"耗时: {elapsed:.1f}s")


def _stats_only():
    """只统计现状，不调 API。"""
    files = sorted(
        f for f in STOCKS_DIR.glob("*.md") if f.name != "index.md"
    )
    fm_no_provenance = 0
    fm_no_confidence = 0
    rep_empty = 0
    rep_has = 0
    dt_empty = 0
    dt_has = 0
    ev_empty = 0
    ev_has = 0
    no_sec = 0
    for f in files:
        content = f.read_text(encoding="utf-8")
        fm = read_fm(content)
        if "provenance" not in fm:
            fm_no_provenance += 1
        if "confidence" not in fm:
            fm_no_confidence += 1
        # 研报段
        m = re.search(r"## 📰 相关研报.*?(?=## |\Z)", content, re.DOTALL)
        if m:
            seg = m.group(0)
            if "| — | — | — |" in seg or "| — | — | 暂无" in seg:
                rep_empty += 1
            else:
                rep_has += 1
        else:
            no_sec += 1
        # 龙虎榜段
        m = re.search(r"## 🐉 龙虎榜.*?(?=## |\Z)", content, re.DOTALL)
        if m:
            seg = m.group(0)
            if "| — |" in seg:
                dt_empty += 1
            else:
                dt_has += 1
        # 事件段
        m = re.search(r"## ⚡ 相关事件.*?(?=## |\Z)", content, re.DOTALL)
        if m:
            seg = m.group(0)
            if "| — |" in seg:
                ev_empty += 1
            else:
                ev_has += 1
    print("===== 现状统计 =====")
    print(f"总 stocks: {len(files)}")
    print(f"无 provenance: {fm_no_provenance}")
    print(f"无 confidence: {fm_no_confidence}")
    print(f"研报段: 有数据={rep_has}, 占位={rep_empty}, 无段={no_sec}")
    print(f"龙虎榜段: 有数据={dt_has}, 占位={dt_empty}")
    print(f"事件段: 有数据={ev_has}, 占位={ev_empty}")


if __name__ == "__main__":
    main()
