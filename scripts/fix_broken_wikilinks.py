#!/usr/bin/env python3
"""修复损坏的 wikilink（fix-19 引用更新脚本遗留的损坏）。

损坏模式（基于实际 vault 内容归纳）：

  1. 路径|[[alias]]：        10_Reference/xxx|[[alias]]
                            → [[10_Reference/xxx|alias]]
  2. 路径|alias嵌[[ ]]：     10_Reference/xxx|Vibe-[[Research]]  (可能含空格)
                            → [[10_Reference/xxx|Vibe-Research]]
  3. 路径|alias后跟[[ ]]：   10_Reference/xxx|knowledge-graph [[vault]]
                            → [[10_Reference/xxx|knowledge-graph vault]]
  4. 路径-[[yyy]]/zzz：      10_Reference/xxx-[[yyy]]/zzz
                            → [[10_Reference/xxx-yyy/zzz]]
  5. 路径|aliasA]][[aliasB]]：10_Reference/xxx|甲]][[乙]]  (链式紧邻)
                            → [[10_Reference/xxx|乙]]
  6. 裸路径+]]残尾：         10_Reference/xxx/yyy]]  或  10_Reference/xxx|alias]]
                            → [[10_Reference/xxx/yyy]] / [[10_Reference/xxx|alias]]
  7. 路径含空格：            10_Reference/.../东财 push2|东财 [[push2]]
                            → [[10_Reference/.../东财 push2|东财 push2]]
  8. 多余括号 [[[[ ：        [[[[10_Reference/xxx|甲]]  (fix-19 累积残留)
                            → [[10_Reference/xxx|甲]]
  9. 链中残尾补 ]]：        [[path1|甲]]、[[path2|乙、[[path3|丙]]
                            → [[path1|甲]]、[[path2|乙]]、[[path3|丙]]

关键设计：
  - 路径正则用 [^\[\]|] 排除 [ ] |，但允许空格——修复类型 7
  - alias 部分允许含 [[ ]]，剥离后重组——修复类型 1/2/3
  - 链式正则专门匹配 aliasA]][[aliasB]] 紧邻——修复类型 5
  - 预处理去多余括号 [[[[ → [[ ——修复类型 8
  - 链中残尾补 ]] 在 、[[ 前——修复类型 9
  - 多轮迭代处理链式——修复类型 5/9
  - 按行处理避免跨行误匹配；表格行跳过（任务验证脚本也跳过）

用法：python3 scripts/fix_broken_wikilinks.py [--apply]
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = ("templates", ".quartz", ".git", ".obsidian")


def is_excluded(path: Path) -> bool:
    parts = path.parts
    for ex in EXCLUDE_DIRS:
        if ex in parts:
            return True
    return False


def strip_brackets(s: str) -> str:
    """把字符串里的 [[ 和 ]] 全部去掉，返回纯文本。"""
    return s.replace("[[", "").replace("]]", "").strip()


# ── 正则定义 ──

# 路径段：不含 [ ] |，允许空格、中文、字母数字、/、-、_、（）、.、：
PATH_SEG = r"10_Reference/[^\[\]|]+"

# alias 部分里的 [[ ]] 块
ALIAS_WITH_BRACKETS = r"(?:[^\[\]]|\[\[[^\[\]]+\]\])*?"


def fix_line(line: str):
    """对单行应用所有修复，返回 (新行, 修复次数)。

    不跳过表格行——正则只匹配 wikilink 片段，不影响表格分隔符结构。
    （任务验证脚本跳过 | 开头行是为了避免贪婪正则跨单元格误匹配，
     但本脚本的正则严格排除 [ ] |，不会误匹配表格分隔符。）
    """
    fixes = 0
    prev = None

    for _ in range(12):  # 多轮迭代
        if line == prev:
            break
        prev = line

        # ── 预处理 0：去掉多余的 [[ 前缀（[[[[ → [[）
        pat_multi_open = re.compile(r"\[\[(\[\[)+")
        def repl_multi_open(m):
            nonlocal fixes
            fixes += 1
            return "[["
        line_new = pat_multi_open.sub(repl_multi_open, line)
        if line_new != line:
            line = line_new
            # 不 continue——去掉多余 [[ 后会暴露链中残尾，继续后续正则

        # ── 预处理 0b：去掉多余的 ]] 残尾（]]]] → ]]）
        pat_multi_close = re.compile(r"(\]\])\]\]+")
        def repl_multi_close(m):
            nonlocal fixes
            fixes += 1
            return "]]"
        line_new = pat_multi_close.sub(repl_multi_close, line)
        if line_new != line:
            line = line_new

        # ── 优先 1：路径|aliasA]][[aliasB]]  (链式紧邻)
        # 例：10_Reference/...|四构件本体方法论]][[四构件本体]]
        # 合并成 [[path|aliasB]]（aliasB 是别名）
        pat_chain = re.compile(
            r"(?<!\[)"
            r"(" + PATH_SEG + r")"                 # path
            r"\|([^\[\]\|]*?)"                      # aliasA（到 ]][[ 前，不含 [ ] |）
            r"\]\]\[\[([^\[\]]+)\]\]"               # ]][[aliasB]]
        )

        def repl_chain(m):
            nonlocal fixes
            path = m.group(1)
            alias_b = m.group(3)
            if "|" in alias_b:
                alias_b = alias_b.split("|", 1)[1]
            fixes += 1
            return f"[[{path}|{alias_b}]]"

        line_new = pat_chain.sub(repl_chain, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 2：路径|alias部分（含 [[ ]]）+ 可选 ]] 残尾 + 边界
        pat_alias_block = re.compile(
            r"(?<!\[)"
            r"(" + PATH_SEG + r")"                          # path
            r"\|"
            r"(" + ALIAS_WITH_BRACKETS + r")"                # alias 部分（含 [[ ]]）
            r"(?:\]\])?"                                     # 可选 ]] 残尾
            r"(?=\s*\[\[|\s*$|[\u3001\uff0c\u3002\uff1b;])" # 边界
        )

        def repl_alias_block(m):
            nonlocal fixes
            path = m.group(1)
            alias_raw = m.group(2)
            alias_clean = strip_brackets(alias_raw)
            if not alias_clean:
                seg = path.rsplit("/", 1)[-1].strip()
                alias_clean = seg
            fixes += 1
            return f"[[{path}|{alias_clean}]]"

        line_new = pat_alias_block.sub(repl_alias_block, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 3：路径|alias前段 [[alias后段]]（无边界锚点版）
        # 例：10_Reference/xxx|knowledge-graph [[vault]]
        pat_alias_followed = re.compile(
            r"(?<!\[)"
            r"(" + PATH_SEG + r")"
            r"\|"
            r"([^\[\]]*?)"                        # alias 前段（无 [ ]）
            r"\s*\[\[([^\[\]]+)\]\]"               # 后跟 [[alias]]
        )

        def repl_alias_followed(m):
            nonlocal fixes
            path = m.group(1)
            alias_pre = m.group(2).strip()
            embedded = m.group(3)
            if "|" in embedded:
                emb_alias = embedded.split("|", 1)[1]
            else:
                emb_alias = embedded
            new_alias = f"{alias_pre} {emb_alias}".strip() if alias_pre else emb_alias
            fixes += 1
            return f"[[{path}|{new_alias}]]"

        line_new = pat_alias_followed.sub(repl_alias_followed, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 4：路径中间插入 [[ ]]（无 |）
        # 例：10_Reference/xxx-[[yyy]]  或  10_Reference/xxx-[[yyy]]/zzz
        pat_embedded_in_path = re.compile(
            r"(?<!\[)"
            r"(10_Reference/[^\[\]\|]+?)"         # 路径前段
            r"\[\[([^\[\]]+)\]\]"                 # 嵌入 [[yyy]]
            r"([^\[\]\|]*)"                        # 路径后段
        )

        def repl_embedded_in_path(m):
            nonlocal fixes
            prefix = m.group(1)
            embedded = m.group(2)
            tail = m.group(3) or ""
            emb_target = embedded.split("|")[0]
            full_path = prefix + emb_target + tail
            fixes += 1
            return f"[[{full_path}]]"

        line_new = pat_embedded_in_path.sub(repl_embedded_in_path, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 5：裸路径+alias+]] 残尾（无 [[ ]]）
        pat_bare_tail = re.compile(
            r"(?<!\[)"
            r"(10_Reference/[^\[\]\|]+)"           # 路径
            r"(?:\|([^\[\]\|]*?))?"                # 可选 alias（无 [ ] |）
            r"\]\]"
        )

        def repl_bare_tail(m):
            nonlocal fixes
            path = m.group(1)
            alias = m.group(2)
            fixes += 1
            if alias and alias.strip():
                return f"[[{path}|{alias.strip()}]]"
            return f"[[{path}]]"

        line_new = pat_bare_tail.sub(repl_bare_tail, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 6：链中残尾 wikilink 补 ]] 残尾
        # 例：[[path1|甲]]、[[path2|乙、[[path3|丙]]
        # 中间的 "[[path2|乙" 缺 ]], 直接 "、[[path3"
        # 修复：在 "、[[" 前补 ]]
        pat_mid_wikilink = re.compile(
            r"(\[\[10_Reference/[^\[\]\|]+\|[^\[\]\|、，\s]+?)"
            r"([、，])\[\["
        )

        def repl_mid_wikilink(m):
            nonlocal fixes
            prefix_wikilink = m.group(1)
            sep = m.group(2)
            fixes += 1
            return f"{prefix_wikilink}]]{sep}[["

        line_new = pat_mid_wikilink.sub(repl_mid_wikilink, line)
        if line_new != line:
            line = line_new
            continue

        # ── 优先 7：短路径（meta|reading|tech-learning|projects|market_sentiment）残尾损坏
        # 这类是 fix-19 残留的另一形态：子目录相对路径 wikilink 被砍 [[
        # 例：meta/四构件本体方法论]]                  → [[meta/四构件本体方法论]]
        #     meta/四构件本体方法论|四构件本体]]        → [[meta/四构件本体方法论|四构件本体]]
        #     reading/booklist/周期]]                  → [[reading/booklist/周期]]
        # 前不紧邻 [[（避免误匹配正常 [[meta/xxx]] 的尾部]]
        # 前不紧邻 ]（避免误匹配相邻 [[10_Reference/...]] 的后续 [[meta/xxx]]）
        pat_short = re.compile(
            r"(?<!\[\[)(?<![\]])"
            r"((?:meta|reading|tech-learning|projects|market_sentiment)"
            r"/[^\[\]\|]+)"                              # 短路径
            r"(?:\|([^\[\]]+))?"                         # 可选 alias
            r"\]\]"
        )

        def repl_short(m):
            nonlocal fixes
            path = m.group(1)
            alias = m.group(2)
            fixes += 1
            if alias and alias.strip():
                return f"[[{path}|{alias.strip()}]]"
            return f"[[{path}]]"

        line_new = pat_short.sub(repl_short, line)
        if line_new != line:
            line = line_new
            continue

    return line, fixes


def fix_content(content: str):
    """对单文件应用修复，返回 (新内容, 修复次数)。"""
    fixes = 0
    new_lines = []
    for line in content.split("\n"):
        new_line, n = fix_line(line)
        fixes += n
        new_lines.append(new_line)
    return "\n".join(new_lines), fixes


def main():
    apply = "--apply" in sys.argv
    total_files = 0
    total_fixes = 0

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
