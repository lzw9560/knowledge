#!/usr/bin/env python3
"""每日知识图谱深度审查脚本。

轻量版——不调 git log（慢），纯文件扫描，5 秒内完成。

用法：python3 scripts/daily_audit.py [--quiet]
"""
import re
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

VAULT = Path(__file__).resolve().parent.parent / "10_Reference" / "investing"
# 跨领域搜索根——用于解析跨子目录的 [[]] 链接
REFERENCE_ROOT = Path(__file__).resolve().parent.parent / "10_Reference"
VAULT_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(content):
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip("'\"")
            val = re.sub(r"<%.*%>", "", val).strip()
            if val:
                fm[key.strip()] = val
    return fm


def strip_frontmatter(content):
    return re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)


def extract_links(content):
    links = []
    for m in re.finditer(r"\[\[([^\]]+)\]\]", content):
        target = m.group(1).split("|")[0].strip()
        if target and not target.startswith("http") and "<" not in target:
            links.append(target)
    return links


def resolve_link(target):
    # Obsidian [[]] 短路径——在 vault 全局搜索
    # 先试 investing/ 内
    candidates = [
        VAULT / (target + ".md"),
        VAULT / target,
    ]
    if any(c.exists() for c in candidates):
        return True
    # 再试 10_Reference/ 下其他子目录（tech-learning/reading/projects/meta/market_sentiment）
    candidates = [
        REFERENCE_ROOT / (target + ".md"),
        REFERENCE_ROOT / target,
    ]
    if any(c.exists() for c in candidates):
        return True
    # 最后试 vault 根（如 🏠 首页）
    candidates = [
        VAULT_ROOT / (target + ".md"),
        VAULT_ROOT / target,
    ]
    return any(c.exists() for c in candidates)


def run_audit():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 扫描所有实体
    all_entities = {}
    in_degree = Counter()
    broken_links = []
    type_counts = Counter()
    stub_count = 0
    llm_count = 0
    placeholder_count = 0
    placeholder_by_type = defaultdict(list)
    confidence_dist = Counter()
    no_confidence = 0
    
    # 占位符模式
    placeholder_patterns = [
        r"待补", r"待人工补充", r"待人工校验",
        r"TODO", r"占位符", r"待填充", r"待完善",
        r"暂无数据", r"待接入", r"待查",
    ]
    
    for f in VAULT.rglob("*.md"):
        if "templates" in str(f) or ".quartz" in str(f):
            continue
        # index.md / MOC.md / README.md 不作为实体，但它们的 [[]] 链接计入入边
        is_index = f.name in ("index.md", "MOC.md", "README.md", "SUMMARY.md")
        if "reviews" in str(f) or "scripts" in str(f):
            continue
        if "inbox" in str(f) and not is_index:
            continue
        
        content = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        body = strip_frontmatter(content)
        
        # index.md/MOC.md 不作为实体，但其 [[]] 链接计入入边
        if is_index:
            links = extract_links(body)
            for target in links:
                in_degree[target] += 1
                if not resolve_link(target):
                    broken_links.append(target)
            continue
        
        rel = str(f.relative_to(VAULT)).replace(".md", "")
        all_entities[rel] = fm
        
        # 类型计数
        entity_type = fm.get("type", "unknown")
        type_counts[entity_type] += 1
        
        # stub 计数
        if fm.get("status") == "stub":
            stub_count += 1
        
        # LLM 生成计数
        if "LLM 生成" in content:
            llm_count += 1
        
        # 占位符检测
        for pat in placeholder_patterns:
            if re.search(pat, body):
                placeholder_count += 1
                folder = f.parent.name
                placeholder_by_type[folder].append(f.name)
                break  # 每个文件只计一次
        
        # confidence 分布
        conf = fm.get("confidence", "")
        if conf:
            confidence_dist[conf] += 1
        else:
            no_confidence += 1
        
        # 入边 + 断链
        links = extract_links(body)
        for target in links:
            in_degree[target] += 1
            if not resolve_link(target):
                broken_links.append(target)
    
    # 孤立实体
    orphan = set(all_entities.keys()) - set(in_degree.keys())
    
    # 统计
    total = len(all_entities)
    broken_count = len(broken_links)
    orphan_count = len(orphan)
    
    # 断链去重 Top 10
    broken_counter = Counter(broken_links)
    
    # 孤立按类型
    orphan_by_type = defaultdict(list)
    for o in orphan:
        folder = o.split("/")[0] if "/" in o else "root"
        orphan_by_type[folder].append(o)
    
    # 输出 JSON
    result = {
        "audit_date": today,
        "total_entities": total,
        "type_distribution": dict(type_counts.most_common()),
        "stub_count": stub_count,
        "llm_generated_count": llm_count,
        "placeholder_count": placeholder_count,
        "placeholder_by_type": {k: len(v) for k, v in sorted(placeholder_by_type.items())},
        "confidence_distribution": dict(confidence_dist),
        "no_confidence_count": no_confidence,
        "broken_links": broken_count,
        "broken_links_top10": broken_counter.most_common(10),
        "orphan_count": orphan_count,
        "orphan_by_type": {k: len(v) for k, v in sorted(orphan_by_type.items())},
    }
    
    # 写审查报告
    report_path = VAULT / "reviews" / f"{today}-daily-audit.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = f"""---
type: audit
audit_date: {today}
auditor: daily-audit-script
scope: 全量
findings_count: {broken_count + orphan_count}
critical: {sum(1 for t, c in broken_counter.items() if c >= 5)}
high: {len(broken_links)}
medium: {orphan_count}
low: {stub_count}
status: 已完成
created: {today}
---

# 每日审查报告：{today}

> 自动审查（daily_audit.py 轻量版，纯文件扫描）。

## 📊 图谱统计

| 指标 | 值 |
|---|---|
| 总实体数 | {total} |
| stub 实体 | {stub_count} |
| LLM 生成内容 | {llm_count} |
| 占位符残留 | {placeholder_count} |
| 断链 | {broken_count} |
| 孤立实体 | {orphan_count} |
| confidence 覆盖 | {total - no_confidence}/{total} ({(total-no_confidence)*100//total}%) |

## 📋 各类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---|---|---|
"""
    items = list(type_counts.most_common())
    for i in range(0, len(items), 2):
        left = f"{items[i][0]} | {items[i][1]}"
        right = f"{items[i+1][0]} | {items[i+1][1]}" if i+1 < len(items) else ""
        report += f"| {left} | {right} |\n"
    
    report += f"""
## 🔗 断链 Top 10

| 断链目标 | 次数 |
|---|---|
"""
    for target, count in broken_counter.most_common(10):
        report += f"| {target} | {count} |\n"
    
    report += f"""
## 🏝️ 孤立实体分布

| 类型 | 数量 |
|---|---|
"""
    for folder, count in sorted(orphan_by_type.items()):
        report += f"| {folder} | {count} |\n"
    
    report += f"""
## 🔍 占位符残留分布

| 类型 | 文件数 |
|---|---|
"""
    if placeholder_by_type:
        for folder, files in sorted(placeholder_by_type.items()):
            report += f"| {folder} | {len(files)} |\n"
    else:
        report += "| (无) | 0 |\n"
    
    report += f"""
## 📊 confidence 分布

| confidence | 数量 |
|---|---|
"""
    for conf, count in confidence_dist.most_common():
        report += f"| {conf} | {count} |\n"
    report += f"| (未标注) | {no_confidence} |\n"
    
    report += f"""
## 📅 KPI 仪表盘

| KPI | 当前值 | 阈值 | 状态 |
|---|---|---|---|
| 断链 | {broken_count} | ≤50 | {'🟢' if broken_count <= 50 else '🔴'} |
| 孤立实体 | {orphan_count} | ≤200 | {'🟢' if orphan_count <= 200 else '🟡' if orphan_count <= 500 else '🔴'} |
| stub 实体 | {stub_count} | ≤100 | {'🟢' if stub_count <= 100 else '🟡'} |
| 占位符残留 | {placeholder_count} | ≤10 | {'🟢' if placeholder_count <= 10 else '🟡' if placeholder_count <= 50 else '🔴'} |
| confidence 覆盖 | {(total-no_confidence)*100//total}% | ≥95% | {'🟢' if (total-no_confidence)*100//total >= 95 else '🟡'} |

## 📈 趋势

> 审查脚本已自动检测占位符残留。如需与上次审查对比，读 reviews/ 前一份报告。
"""
    
    report_path.write_text(report, encoding="utf-8")
    
    # 输出 JSON
    json_path = VAULT / "reviews" / f"{today}-daily-audit.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    
    if "--quiet" not in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 审查完成: {total} 实体, {broken_count} 断链, {orphan_count} 孤立, {llm_count} LLM生成")
        print(f"📄 报告: {report_path}")


if __name__ == "__main__":
    run_audit()
