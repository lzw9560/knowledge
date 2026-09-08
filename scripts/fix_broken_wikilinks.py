#!/usr/bin/env python3
"""修复损坏的 wikilink（fix-19 引用更新脚本遗留的损坏）。

四种损坏模式：
  A：裸路径+`]]` 但缺 `[[`
  B：路径中间插入 `[[`
  C：路径+`|[[alias]]`
  D：裸 `[[` 在路径中间

用法：python3 scripts/fix_broken_wikilinks.py [--apply]
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = ("templates", ".quartz", ".git", ".obsidian")

# 模式 A：裸路径 + 可选 alias + ]]，但缺 [[ 前缀
# 例：10_Reference/xxx/yyy]] 或 10_Reference/xxx|alias]]
PAT_A = re.compile(r"(?<!\[\[)(10_Reference/[^\]|]+?)(\|([^\]]+))?\]\]")

# 模式 B：路径中间插入 [[
# 例：10_Reference/xxx/yyy-[[zzz]] -> [[10_Reference/xxx/yyy-zzz]]
PAT_B = re.compile(r"(10_Reference/[^\s\[]+)\[\[([^\]]+)\]\]")

# 模式 C：路径 + |[[alias]]
# 例：10_Reference/xxx|[[alias]] -> [[10_Reference/xxx|alias]]
PAT_C = re.compile(r"(10_Reference/[^\]|]+)\|\[\[([^\]]+)\]\]")

# 模式 D：裸 [[ 在路径中间（[[ 不在路径开头）
# 例：10_Reference/xxx-[[yyy]]/zzz -> [[10_Reference/xxx-yyy/zzz]]
# 先把路径中插入的 [[ ]] 抹平，再交给 A/B/C 处理
PAT_D = re.compile(r"(10_Reference/[^\s\[]+?)\[\[([^\]]+?)\]\]([^\s\]\[]*)")


def is_excluded(path: Path) -> bool:
    parts = path.parts
    for ex in EXCLUDE_DIRS:
        if ex in parts:
            return True
    return False


def fix_content(content: str):
    """对单个文件内容应用所有修复，返回 (新内容, 修复次数)。"""
    fixes = 0

    def repl_d(m):
        nonlocal fixes
        fixes += 1
        # 把 [[ ]] 中间内容拼到路径上
        return m.group(1) + m.group(2) + (m.group(3) or "")

    # 先处理 D：[[ 在路径中间，把 [[ ]] 抹平成普通文本（合并到路径）
    # 注意 D 与 B 的正则非常接近——B 要求整个 [[xxx]] 紧跟路径段，D 更通用。
    # 实际上 B 的正则已经能处理 10_Reference/xxx-[[yyy]] 的形式，但
    # 如果 [[yyy]] 后面还跟了 /zzz，B 不会匹配（因为 B 替换后路径被切断）。
    # 所以先用 D 把插入的 [[ ]] 抹平，留下裸路径，再交给 A。
    new = PAT_D.sub(repl_d, content)

    def repl_b(m):
        nonlocal fixes
        fixes += 1
        return f"[[{m.group(1)}{m.group(2)}]]"

    new = PAT_B.sub(repl_b, new)

    def repl_c(m):
        nonlocal fixes
        fixes += 1
        return f"[[{m.group(1)}|{m.group(2)}]]"

    new = PAT_C.sub(repl_c, new)

    def repl_a(m):
        nonlocal fixes
        fixes += 1
        alias = m.group(2) or ""
        return f"[[{m.group(1)}{alias}]]"

    new = PAT_A.sub(repl_a, new)

    return new, fixes


def main():
    apply = "--apply" in sys.argv
    total_files = 0
    total_fixes = 0
    changed_files = []

    for f in VAULT.rglob("*.md"):
        if is_excluded(f):
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️  读取失败 {f}: {e}", file=sys.stderr)
            continue
        new, fixes = fix_content(content)
        if fixes > 0 and new != content:
            total_files += 1
            total_fixes += fixes
            changed_files.append((f, fixes))
            if apply:
                f.write_text(new, encoding="utf-8")
                print(f"✅ {f.relative_to(VAULT)}  ({fixes} 处)")
            else:
                print(f"[DRY] {f.relative_to(VAULT)}  ({fixes} 处)")

    mode = "APPLY" if apply else "DRY-RUN"
    print(f"\n=== {mode} 完成 ===")
    print(f"修改文件数: {total_files}")
    print(f"修复链接数: {total_fixes}")
    if not apply:
        print("\n(dry-run，加 --apply 实际写入)")


if __name__ == "__main__":
    main()
