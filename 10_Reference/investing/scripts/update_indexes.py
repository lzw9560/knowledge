#!/usr/bin/env python3
"""批量更新各实体文件夹的 index.md——加"快速操作"段 + "Dataview 实时统计"段 + "相关子区"链接。

在各实体文件夹的 index.md 末尾追加：
  1. ⚡ 快速操作——Templater 新建实体的命令提示
  2. 📊 Dataview 实时统计——该类型实体的实时计数
  3. 🔗 相关子区——与其他实体文件夹的关联

用法:
    python3 scripts/update_indexes.py            # 全量更新
    python3 scripts/update_indexes.py --dry-run  # 只预览不写盘
"""
import argparse
import re
import sys
from pathlib import Path

VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault/10_Reference/investing")

# 各文件夹配置：(文件夹名, type值, emoji, 模板名, 中文名)
INDEX_CONFIGS = {
    "stocks":       ("stock",        "📈", "stock",       "股票"),
    "industries":   ("industry",     "🏭", "industry",    "行业板块"),
    "concepts":     ("concept",      "💡", "concept",     "概念板块"),
    "indices":      ("index",        "📊", "index",       "指数"),
    "reports":      ("report",       "📰", "report",      "研报"),
    "analysts":     ("analyst",      "👤", "analyst",      "分析师"),
    "metrics":      ("metric",       "💰", "metric",      "财务指标"),
    "valuations":   ("valuation",    "📈", "valuation",   "估值"),
    "dragon-tiger": ("dragon_tiger",  "🐉", "dragon-tiger", "龙虎榜"),
    "events":       ("event",        "⚡", "event",       "事件"),
    "strategies":   ("strategy",     "⚔️", "strategy",    "战法"),
    "specs":        ("spec",         "📋", "spec",        "项目决策"),
    "data-sources": ("data_source",  "📡", "data-source", "数据源"),
    "agents":       ("agent_role",   "🤖", "agent",       "AI 角色"),
    "logic":        ("logic",        "⚙️", "logic",       "逻辑规则"),
    "actions":      ("action",       "⚡", "action",      "动作"),
    "reviews":      ("audit",        "🔍", "audit",       "审查报告"),
}

FOOTER_TEMPLATE = """

---

## ⚡ 快速操作

用 Templater 应用 `templates/{template}` 新建 {cn} 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "{cn}总数"
FROM "10_Reference/investing/{folder}"
WHERE type = "{type}" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
"""


def update_index(filepath: Path, folder_name: str, fm_type: str, emoji: str,
                 template: str, cn: str, dry_run: bool = False) -> bool:
    """更新单个 index.md 文件。"""
    content = filepath.read_text(encoding="utf-8")

    # 检查是否已有快速操作段（避免重复追加）
    if "快速操作" in content:
        return False

    footer = FOOTER_TEMPLATE.format(
        template=template,
        cn=cn,
        folder=folder_name,
        type=fm_type,
    )

    new_content = content.rstrip() + footer

    if dry_run:
        return True

    filepath.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="批量更新各 index.md 文件")
    parser.add_argument("--dry-run", action="store_true", help="只预览不写盘")
    args = parser.parse_args()

    count = 0
    for folder_name, (fm_type, emoji, template, cn) in INDEX_CONFIGS.items():
        index_path = VAULT / folder_name / "index.md"
        if not index_path.exists():
            print(f"⚠️  跳过（无 index.md）: {folder_name}")
            continue

        try:
            if update_index(index_path, folder_name, fm_type, emoji, template, cn, dry_run=args.dry_run):
                count += 1
                print(f"✅ {folder_name}/index.md")
            else:
                print(f"  ⏭️  {folder_name}/index.md（已有快速操作段，跳过）")
        except Exception as e:
            print(f"  ❌ 错误 {folder_name}/index.md: {e}")

    print(f"\n总计更新 {count} 个 index.md" + ("（dry-run）" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
