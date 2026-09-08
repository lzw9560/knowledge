#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""预编译 Dataview 查询为静态 Markdown 表格。

Quartz 是静态站点生成器，不执行 Dataview 查询。本脚本读 vault 中所有 .md 文件的
frontmatter，执行 Dataview TABLE 查询逻辑，生成静态 Markdown 表格替换原始
```dataview 代码块，让 Quartz 站点直接显示数据。

用法：
    python3 scripts/precompile_dataview.py [--dry-run] [--stats-only] [--path PATH]

可重算（recalculate）：预编译块在 HTML 注释里保留 query 原文（base64 编码），
每次运行解码 query 重新执行——frontmatter 变了表格自动更新。第二次运行幂等：
表格内容不变则跳过。旧格式块（无 query 标记）用 hash 反查模板 query 原文升级
为新格式；反查失败则保留原表格。无法解析的查询保留原代码块，前面加注释标记。

设计文档见 AGENTS.md / 任务说明。覆盖 vault 实测的 58 种 WHERE 变体 + 6 种 GROUP BY 变体。
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import os
import re
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# 路径
# --------------------------------------------------------------------------- #
VAULT = Path(__file__).resolve().parent.parent
INVESTING = VAULT / "10_Reference" / "investing"
# --------------------------------------------------------------------------- #
# Frontmatter 解析（手写，无需 pyyaml）
# --------------------------------------------------------------------------- #
_FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_INLINE_LIST_RE = re.compile(r"^\[(.*)\]$")


def parse_frontmatter(content: str) -> dict[str, Any]:
    """解析 YAML frontmatter。支持扁平 key: value 与 inline list [a, b]。

    不支持嵌套映射/多行块——vault 实测 frontmatter 均为扁平结构，足够覆盖。
    """
    m = _FM_RE.match(content)
    if not m:
        return {}
    fm: dict[str, Any] = {}
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not val:
            fm[key] = ""
            continue
        # 去引号
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            val = val[1:-1]
        # inline list
        lm = _INLINE_LIST_RE.match(val)
        if lm:
            inner = lm.group(1).strip()
            if inner:
                fm[key] = [
                    x.strip().strip("'\"") for x in inner.split(",") if x.strip()
                ]
            else:
                fm[key] = []
            continue
        # 逗号分隔字符串当列表候选？不——保留原值，contains() 时再判类型
        fm[key] = val
    return fm


# --------------------------------------------------------------------------- #
# 文件系统扫描 + frontmatter 缓存
# --------------------------------------------------------------------------- #
class FileRecord:
    __slots__ = ("path", "stem", "name", "content", "fm", "mtime", "ctime", "vault_key")

    def __init__(self, path: Path, content: str):
        self.path = path
        self.stem = path.stem
        self.name = path.stem  # file.name
        self.content = content
        self.fm = parse_frontmatter(content)
        st = path.stat()
        self.mtime = datetime.fromtimestamp(st.st_mtime).replace(microsecond=0)
        self.ctime = datetime.fromtimestamp(st.st_ctime).replace(microsecond=0)
        try:
            self.vault_key = path.resolve().relative_to(VAULT).with_suffix("").as_posix()
        except ValueError:
            # 不在 vault 下——用绝对路径 stem 兜底
            self.vault_key = path.resolve().with_suffix("").as_posix()


class VaultIndex:
    """扫描 vault 的 investing 子树，缓存 frontmatter，构建双链图。"""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.records: list[FileRecord] = []
        self.by_dir: dict[str, list[FileRecord]] = defaultdict(list)
        self.by_path: dict[str, FileRecord] = {}
        # 双链：key = 标准化文件路径（相对 vault，无 .md）
        self.outlinks: dict[str, set[str]] = defaultdict(set)
        self.inlinks: dict[str, set[str]] = defaultdict(set)
        # FROM 路径缓存
        self._from_cache: dict[str, list[FileRecord]] = {}
        self._scan()
        self._build_links()

    def _scan(self) -> None:
        if not self.root.exists():
            return
        for p in sorted(self.root.rglob("*.md")):
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue
            rec = FileRecord(p, content)
            self.records.append(rec)
            rel = p.resolve().relative_to(VAULT).parent.as_posix()
            self.by_dir[rel].append(rec)
            self.by_path[p.resolve().relative_to(VAULT).with_suffix("").as_posix()] = rec

    @staticmethod
    def _norm_link(target: str) -> str:
        """标准化 [[target|alias]] / [[target#section]] 到无 .md 的相对路径。

        返回相对 vault 的路径（无扩展名）。无法解析时返回原 target。
        """
        target = target.split("|")[0].split("#")[0].strip()
        if not target:
            return target
        if target.endswith(".md"):
            target = target[:-3]
        return target

    @staticmethod
    def _resolve_stem_collision(keys: list[str]) -> str:
        """stem 碰撞时择优——股票优先于指数，再按字母序兜底。

        背景：000001 股票与指数同名（stocks/000001.md 与 indices/000001.md），
        短链接 [[000001]] 历史被解析到 indices/，导致 metrics/valuations 的
        "所属股票" 表格错链到指数。修复后优先 stocks/。
        """
        for k in keys:
            if "/stocks/" in k:
                return k
        for k in keys:
            if "/indices/" in k:
                return k
        return sorted(keys)[0]

    def _build_links(self) -> None:
        link_re = re.compile(r"\[\[([^\]]+)\]\]")
        # stem → vault_key 索引（碰撞时择优），用于解析短链接 [[000001]]
        stem_index: dict[str, str] = {}
        stem_collisions: dict[str, list[str]] = defaultdict(list)
        for key, rec in self.by_path.items():
            stem_collisions[rec.stem].append(key)
        for stem, keys in stem_collisions.items():
            stem_index[stem] = self._resolve_stem_collision(keys)
        for rec in self.records:
            src_key = rec.vault_key
            body = _FM_RE.sub("", rec.content)
            for m in link_re.finditer(body):
                raw = VaultIndex._norm_link(m.group(1))
                # 解析为标准路径：若已是路径形式命中则直接用；否则按 stem 查
                target = ""
                if raw in self.by_path:
                    target = raw
                elif raw in stem_index:
                    target = stem_index[raw]
                if target and target != src_key:
                    self.outlinks[src_key].add(target)
                    self.inlinks[target].add(src_key)

    def records_from(self, from_spec: str) -> list[FileRecord]:
        """FROM "path" → 该目录下所有 .md 记录（递归）。FROM "文件名" 形式也兜底。"""
        # 命中缓存
        if from_spec in self._from_cache:
            return self._from_cache[from_spec]
        target = VAULT / from_spec
        result: list[FileRecord] = []
        if target.is_file():
            key = target.resolve().relative_to(VAULT).with_suffix("").as_posix()
            rec = self.by_path.get(key)
            result = [rec] if rec else []
        elif target.is_dir():
            t_prefix = from_spec
            for rec in self.records:
                try:
                    rp = rec.path.resolve().relative_to(VAULT).parent.as_posix()
                except ValueError:
                    continue
                if rp == t_prefix or rp.startswith(t_prefix + "/"):
                    result.append(rec)
        self._from_cache[from_spec] = result
        return result


# --------------------------------------------------------------------------- #
# WHERE 表达式求值器（递归下降）
# --------------------------------------------------------------------------- #
class Tokenizer:
    tokens: list[tuple[str, str]]
    pos: int

    def __init__(self, text: str):
        self.tokens = self._tokenize(text)
        self.pos = 0

    @staticmethod
    def _tokenize(text: str) -> list[tuple[str, str]]:
        toks: list[tuple[str, str]] = []
        i = 0
        n = len(text)
        while i < n:
            c = text[i]
            if c.isspace():
                i += 1
                continue
            # 字符串
            if c == '"':
                j = i + 1
                while j < n and text[j] != '"':
                    j += 1
                toks.append(("STR", text[i + 1 : j]))
                i = j + 1
                continue
            # 标识符 / 函数名 / this.xxx / file.xxx
            if c.isalpha() or c == "_":
                j = i
                while j < n and (text[j].isalnum() or text[j] in "._"):
                    j += 1
                word = text[i:j]
                if word in ("AND", "OR", "null", "true", "false"):
                    toks.append(("KW", word))
                else:
                    toks.append(("ID", word))
                i = j
                continue
            # 数字
            if c.isdigit() or (c == "-" and i + 1 < n and text[i + 1].isdigit()):
                j = i + 1
                while j < n and (text[j].isdigit() or text[j] == "."):
                    j += 1
                toks.append(("NUM", text[i:j]))
                i = j
                continue
            # 运算符
            if c in "=!<>":
                if i + 1 < n and text[i + 1] == "=":
                    toks.append(("OP", text[i : i + 2]))
                    i += 2
                    continue
                if c in "<>":
                    toks.append(("OP", c))
                    i += 1
                    continue
                if c == "=":
                    toks.append(("OP", "="))
                    i += 1
                    continue
                if c == "!":
                    # != 被上面吃掉，落到这里是语法异常
                    toks.append(("OP", "!"))
                    i += 1
                    continue
            if c == "(":
                toks.append(("LP", "("))
                i += 1
                continue
            if c == ")":
                toks.append(("RP", ")"))
                i += 1
                continue
            if c == ",":
                toks.append(("COMMA", ","))
                i += 1
                continue
            if c == "+":
                toks.append(("OP", "+"))
                i += 1
                continue
            if c == "-":
                toks.append(("OP", "-"))
                i += 1
                continue
            if c == ".":
                toks.append(("DOT", "."))
                i += 1
                continue
            # 未知字符——记下后跳过
            i += 1
        return toks

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self) -> tuple[str, str] | None:
        t = self.peek()
        if t is not None:
            self.pos += 1
        return t


class WhereEvalError(Exception):
    pass


class WhereEvaluator:
    """递归下降解析 + 求值 WHERE 表达式。

    上下文：current_fm（当前文件的 frontmatter），current_file_key（当前文件标准路径），
    vault_index（用于 file.inlinks/outlinks/mtime）。
    """

    # 类级 AST 缓存：同文本只 tokenize+parse 一次（58 种 WHERE 变体复用）
    _ast_cache: dict[str, object] = {}

    def __init__(self, where_text: str, current_fm: dict, current_key: str, idx: VaultIndex):
        cached = WhereEvaluator._ast_cache.get(where_text)
        if cached is None:
            tk = Tokenizer(where_text)
            self.tk = tk
            self.ast = self._parse_or()
            if self.tk.peek() is not None:
                raise WhereEvalError(f"未消费 token: {self.tk.peek()}")
            WhereEvaluator._ast_cache[where_text] = self.ast
        else:
            self.ast = cached
        self.current_fm = current_fm
        self.current_key = current_key
        self.idx = idx

    # ---- 解析 ----
    def _parse_or(self):
        node = self._parse_and()
        while True:
            t = self.tk.peek()
            if t and t == ("KW", "OR"):
                self.tk.next()
                node = ("OR", node, self._parse_and())
            else:
                break
        return node

    def _parse_and(self):
        node = self._parse_primary()
        while True:
            t = self.tk.peek()
            if t and t == ("KW", "AND"):
                self.tk.next()
                node = ("AND", node, self._parse_primary())
            else:
                break
        return node

    def _parse_primary(self):
        t = self.tk.peek()
        if t is None:
            raise WhereEvalError("意外结尾")
        if t[0] == "LP":
            save = self.tk.pos  # 记住 LP 之前的位置
            self.tk.next()  # 吃 LP
            # 先尝试布尔分组 (a = 0 AND b = 0)
            try:
                node = self._parse_or()
                nt = self.tk.peek()
                if nt and nt[0] == "RP":
                    self.tk.next()
                    return node
            except WhereEvalError:
                pass
            # 回退到 LP 之前：当作值分组的条件 (expr).days > 7
            self.tk.pos = save
            return self._parse_condition()
        # 条件：left op right | contains(...) | length(...) op num | field != null
        return self._parse_condition()

    def _parse_condition(self):
        t = self.tk.peek()
        if t is None:
            raise WhereEvalError("意外结尾（条件）")
        # contains( / length( 开头
        if t[0] == "ID" and t[1] in ("contains", "length"):
            return self._parse_func_or_field()
        if t[0] == "ID" or t[0] == "LP":
            # left 可以是 field/this.x/file.x 或括号分组的值表达式
            left = self._parse_value()
            op_tok = self.tk.next()
            if not op_tok or op_tok[0] != "OP":
                raise WhereEvalError(f"期望运算符，得到 {op_tok}")
            op = op_tok[1]
            if op == "+":
                raise WhereEvalError("算术不在条件层")
            right = self._parse_value()
            return ("CMP", op, left, right)
        if t[0] == "KW" and t[1] == "null":
            raise WhereEvalError("null 不能做左操作数")
        raise WhereEvalError(f"无法解析条件: {t}")

    def _parse_func_or_field(self):
        t = self.tk.next()
        assert t and t[0] == "ID"
        name = t[1]
        nt = self.tk.peek()
        if nt and nt[0] == "LP":
            self.tk.next()
            args = []
            if self.tk.peek() and self.tk.peek()[0] != "RP":
                args.append(self._parse_value())
                while self.tk.peek() and self.tk.peek()[0] == "COMMA":
                    self.tk.next()
                    args.append(self._parse_value())
            rp = self.tk.next()
            if not rp or rp[0] != "RP":
                raise WhereEvalError(f"{name}() 缺右括号")
            if name == "contains":
                if len(args) != 2:
                    raise WhereEvalError("contains 需 2 参数")
                return ("CONTAINS", args[0], args[1])
            if name == "length":
                # length(x) op num
                op_tok = self.tk.next()
                if not op_tok or op_tok[0] != "OP":
                    raise WhereEvalError("length() 后期望运算符")
                right = self._parse_value()
                return ("LENGTHCMP", op_tok[1], args[0], right)
            raise WhereEvalError(f"未知函数 {name}")
        # 普通 ID 后接 op
        left = ("FIELD", name)
        op_tok = self.tk.next()
        if not op_tok or op_tok[0] != "OP":
            raise WhereEvalError(f"期望运算符，得到 {op_tok}")
        right = self._parse_value()
        return ("CMP", op_tok[1], left, right)

    def _parse_value(self):
        """解析一个值，支持后缀属性访问与算术：a.days / a - b / a + b。"""
        node = self._parse_atom()
        while True:
            nt = self.tk.peek()
            if nt and nt[0] == "DOT":
                self.tk.next()
                attr = self.tk.next()
                if not attr or attr[0] != "ID":
                    raise WhereEvalError(". 后期望属性名")
                node = ("ATTR", node, attr[1])
                continue
            if nt and nt[0] == "OP" and nt[1] in ("+", "-"):
                self.tk.next()
                rhs = self._parse_atom()
                node = ("ARITH", nt[1], node, rhs)
                continue
            break
        return node

    def _parse_atom(self):
        """解析原子值：ID(field/this.x/file.x) | STR | NUM | null | date(today)/dur(...) | (expr)"""
        t = self.tk.peek()
        if t is None:
            raise WhereEvalError("意外结尾（值）")
        if t[0] == "LP":
            # 算术/值分组：(date(today) - date(x))
            self.tk.next()
            node = self._parse_value()
            nt = self.tk.next()
            if not nt or nt[0] != "RP":
                raise WhereEvalError("值分组缺右括号")
            return node
        t = self.tk.next()
        if t[0] == "STR":
            return ("LIT", t[1])
        if t[0] == "NUM":
            return ("LIT", t[1])
        if t[0] == "KW":
            if t[1] == "null":
                return ("NULL",)
            if t[1] == "true":
                return ("LIT", True)
            if t[1] == "false":
                return ("LIT", False)
            raise WhereEvalError(f"未预期关键字 {t[1]}")
        if t[0] == "ID":
            name = t[1]
            # date(...) / dur(...)
            nt = self.tk.peek()
            if nt and nt[0] == "LP":
                self.tk.next()
                if name == "date":
                    inner = self._parse_value()
                    rp = self.tk.next()
                    if not rp or rp[0] != "RP":
                        raise WhereEvalError("date() 缺右括号")
                    return ("DATE", inner)
                if name == "dur":
                    # dur(7 days) / dur("7 days") —— 支持 NUM + 可选单位 ID
                    inner_tok = self.tk.peek()
                    if inner_tok and inner_tok[0] == "NUM":
                        self.tk.next()
                        val = inner_tok[1]
                        # 可能有单位 ID
                        nxt = self.tk.peek()
                        if nxt and nxt[0] == "ID":
                            self.tk.next()
                            val = val + " " + nxt[1]
                        rp = self.tk.next()
                        if not rp or rp[0] != "RP":
                            raise WhereEvalError("dur() 缺右括号")
                        return ("DUR", ("LIT", val))
                    inner = self._parse_value()
                    rp = self.tk.next()
                    if not rp or rp[0] != "RP":
                        raise WhereEvalError("dur() 缺右括号")
                    return ("DUR", inner)
                raise WhereEvalError(f"不支持函数 {name}()")
            # this.xxx / file.xxx / rows.xxx
            if name.startswith("this."):
                return ("THIS", name[5:])
            if name.startswith("file."):
                return ("FILE", name[5:])
            if name == "this":
                return ("THIS", "")
            # 普通字段名（候选文件的 frontmatter 字段）
            return ("FIELD", name)
        raise WhereEvalError(f"无法解析值: {t}")

    # ---- 求值 ----
    def eval(self, rec_fm: dict, rec_key: str) -> bool:
        return bool(self._ev(self.ast, rec_fm, rec_key))

    def _get_field(self, node, rec_fm, rec_key):
        """取一个值节点的实际值。返回 (value, is_list)。"""
        tag = node[0]
        if tag == "LIT":
            return node[1], False
        if tag == "NULL":
            return None, False
        if tag == "ATTR":
            inner, _ = self._get_field(node[1], rec_fm, rec_key)
            attr = node[2]
            # .days：date 差 → 天数
            if attr == "days":
                if isinstance(inner, timedelta):
                    return inner.days, False
                if isinstance(inner, (date, datetime)):
                    d = inner if not isinstance(inner, datetime) else inner.date()
                    return (date.today() - d).days, False
                return None, False
            return None, False
        if tag == "ARITH":
            _, op, lnode, rnode = node
            lv, _ = self._get_field(lnode, rec_fm, rec_key)
            rv, _ = self._get_field(rnode, rec_fm, rec_key)
            return self._arith(op, lv, rv), False
        if tag == "THIS":
            # this.field（当前文件 frontmatter）
            fld = node[1]
            v = self.current_fm.get(fld)
            # 当前文件路径（this.file.link）
            if fld == "file.link":
                return self.current_key, False
            return v, isinstance(v, list)
        if tag == "FILE":
            attr = node[1]
            if attr == "name":
                # 用文件 stem
                rec = self.idx.by_path.get(rec_key)
                return rec.stem if rec else rec_key.split("/")[-1], False
            if attr == "link":
                return rec_key, False
            if attr == "mtime":
                rec = self.idx.by_path.get(rec_key)
                return rec.mtime if rec else None, False
            if attr == "ctime":
                rec = self.idx.by_path.get(rec_key)
                return rec.ctime if rec else None, False
            if attr == "outlinks":
                return set(self.idx.outlinks.get(rec_key, set())), True
            if attr == "inlinks":
                return set(self.idx.inlinks.get(rec_key, set())), True
            # file.frontmatter 的其它字段——兜底
            return None, False
        if tag == "FIELD":
            # 候选文件 frontmatter 字段
            v = rec_fm.get(node[1])
            return v, isinstance(v, list)
        if tag == "DATE":
            inner = self._get_field(node[1], rec_fm, rec_key)
            if isinstance(inner, tuple):
                inner = inner[0]
            if node[1][0] == "ID" and node[1][1] == "today":
                return date.today(), False
            if inner is None:
                return None, False
            if isinstance(inner, (date, datetime)):
                return inner, False
            try:
                return datetime.strptime(str(inner)[:10], "%Y-%m-%d").date(), False
            except Exception:
                try:
                    return datetime.strptime(str(inner)[:19], "%Y-%m-%d %H:%M:%S"), False
                except Exception:
                    return None, False
        if tag == "DUR":
            inner = self._get_field(node[1], rec_fm, rec_key)
            if isinstance(inner, tuple):
                inner = inner[0]
            # dur(7 days)
            m = re.match(r"(\d+)\s*days?", str(inner))
            if m:
                return timedelta(days=int(m.group(1))), False
            return None, False
        return None, False

    def _value(self, node, rec_fm, rec_key):
        v, _ = self._get_field(node, rec_fm, rec_key)
        return v

    @staticmethod
    def _arith(op, lv, rv):
        if lv is None or rv is None:
            return None
        # date - date → timedelta
        if isinstance(lv, (date, datetime)) and isinstance(rv, (date, datetime)):
            ld = lv if not isinstance(lv, datetime) else lv.date()
            rd = rv if not isinstance(rv, datetime) else rv.date()
            if op == "-":
                return ld - rd
            if op == "+":
                return ld - rd  # 无意义，兜底
        # date - timedelta → date
        if isinstance(lv, (date, datetime)) and isinstance(rv, timedelta):
            ld = lv if not isinstance(lv, datetime) else lv.date()
            if op == "-":
                return ld - rv
            if op == "+":
                return ld + rv
        if isinstance(lv, timedelta) and isinstance(rv, (date, datetime)):
            rd = rv if not isinstance(rv, datetime) else rv.date()
            if op == "+":
                return lv + rd
        # 数值算术
        ln = lv if isinstance(lv, (int, float)) else WhereEvaluator._coerce_num(lv)
        rn = rv if isinstance(rv, (int, float)) else WhereEvaluator._coerce_num(rv)
        if ln is not None and rn is not None:
            if op == "-":
                return ln - rn
            if op == "+":
                return ln + rn
        return None

    @staticmethod
    def _coerce_num(v):
        if v is None:
            return None
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, (int, float)):
            return v
        s = str(v).strip()
        if s == "":
            return None
        # 形如 "137.48亿" "2267B"
        m = re.match(r"([+-]?\d+(?:\.\d+)?)\s*(亿|B|万|W|M|k)?", s)
        if m:
            base = float(m.group(1))
            unit = m.group(2)
            if unit == "亿":
                return base * 1e8
            if unit == "B":
                return base * 1e8
            if unit == "万" or unit == "W":
                return base * 1e4
            if unit == "M":
                return base * 1e6
            if unit == "k":
                return base * 1e3
            return base
        try:
            return float(s)
        except ValueError:
            return None

    def _ev(self, node, rec_fm, rec_key):
        tag = node[0]
        if tag == "AND":
            return self._ev(node[1], rec_fm, rec_key) and self._ev(node[2], rec_fm, rec_key)
        if tag == "OR":
            return self._ev(node[1], rec_fm, rec_key) or self._ev(node[2], rec_fm, rec_key)
        if tag == "CMP":
            _, op, left, right = node
            lv = self._value(left, rec_fm, rec_key)
            rv = self._value(right, rec_fm, rec_key)
            return self._compare(op, lv, rv)
        if tag == "CONTAINS":
            _, hay, needle = node
            hv = self._value(hay, rec_fm, rec_key)
            nv = self._value(needle, rec_fm, rec_key)
            if hv is None or nv is None:
                return False
            if isinstance(hv, (list, set, tuple)):
                items = [str(x) for x in hv]
            else:
                # 逗号分隔字符串当列表
                items = [x.strip() for x in str(hv).split(",") if x.strip()]
            nv_s = str(nv)
            return nv_s in items or any(nv_s == str(x) for x in items) or (
                # 文件链接包含：标准化比较
                self._norm(nv_s) in {self._norm(x) for x in items}
            )
        if tag == "LENGTHCMP":
            _, op, target, right = node
            tv = self._value(target, rec_fm, rec_key)
            n = 0
            if isinstance(tv, (list, set, tuple)):
                n = len(tv)
            elif tv is not None and str(tv).strip():
                # 逗号分隔字符串
                n = len([x for x in str(tv).split(",") if x.strip()])
            rv = self._value(right, rec_fm, rec_key)
            return self._compare(op, n, self._coerce_num(rv) if rv is not None else None)
        raise WhereEvalError(f"未实现求值节点 {tag}")

    @staticmethod
    def _norm(x):
        x = str(x)
        x = x.split("|")[0].split("#")[0]
        return x[:-3] if x.endswith(".md") else x

    def _compare(self, op, lv, rv):
        if op == "=":
            if lv is None or rv is None:
                return lv is None and rv is None and lv == rv
            return str(lv) == str(rv) or self._norm(str(lv)) == self._norm(str(rv))
        if op == "!=":
            if lv is None or rv is None:
                return not (lv is None and rv is None)
            return str(lv) != str(rv) and self._norm(str(lv)) != self._norm(str(rv))
        # 数值比较
        ln = self._coerce_num(lv)
        rn = self._coerce_num(rv) if rv is not None else None
        # 日期比较：若任一侧是 date/datetime
        if isinstance(lv, (date, datetime)) or isinstance(rv, (date, datetime)):
            ld = self._as_date(lv)
            rd = self._as_date(rv)
            if ld is not None and rd is not None:
                return self._cmp_op(op, ld, rd)
        if ln is not None and rn is not None:
            return self._cmp_op(op, ln, rn)
        # 兜底字符串比较
        if lv is not None and rv is not None:
            return self._cmp_op(op, str(lv), str(rv))
        return False

    @staticmethod
    def _as_date(v):
        if v is None:
            return None
        if isinstance(v, (date, datetime)):
            return v
        s = str(v)[:10]
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None

    @staticmethod
    def _cmp_op(op, a, b):
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        if op == "<=":
            return a <= b
        if op == ">=":
            return a >= b
        if op == "=":
            return a == b
        if op == "!=":
            return a != b
        return False


# --------------------------------------------------------------------------- #
# 查询解析
# --------------------------------------------------------------------------- #
class Query:
    def __init__(self):
        self.without_id = False
        self.columns: list[tuple[str, str | None]] = []  # (field_expr, alias)
        self.from_path: str = ""
        self.where: str = ""
        self.group_by: str = ""
        self.having: str = ""
        self.flatten = False
        self.sort_field: str = ""
        self.sort_dir: str = "ASC"
        self.limit: int | None = None

    @classmethod
    def parse(cls, text: str) -> "Query | None":
        q = cls()
        t = text.strip()
        if not t.upper().startswith("TABLE"):
            return None
        # 按行切分，识别各子句。支持单行紧凑与多行两种写法。
        # 先把 TABLE/WITHOUT ID 头部剥掉，剩余按子句关键字分块。
        body = t[len("TABLE"):].lstrip()
        # WITHOUT ID
        m = re.match(r"WITHOUT\s+ID\b\s*", body, re.IGNORECASE)
        if m:
            q.without_id = True
            body = body[m.end():].lstrip()
        # 找到 FROM 的位置，前面是 columns
        fm = re.search(r'\bFROM\s+"', body, re.IGNORECASE)
        if not fm:
            return None
        cols_str = body[: fm.start()].rstrip()
        q.columns = parse_columns(cols_str)
        body = body[fm.start():]
        # 按"行首子句关键字"切分剩余
        # 子句顺序：FROM "path"  [WHERE ...]  [GROUP BY ... [HAVING ...]]  [FLATTEN ...]  [SORT ...]  [LIMIT ...]
        # 用正则定位各子句起始，取到下一子句前
        clause_pat = re.compile(
            r'\bFROM\s+"[^"]+"'                         # FROM "x"
            r'|\bWHERE\b'
            r'|\bGROUP\s+BY\b'
            r'|\bHAVING\b'
            r'|\bFLATTEN\b'
            r'|\bSORT\b'
            r'|\bLIMIT\b',
            re.IGNORECASE,
        )
        # 找出所有子句起点
        starts = [(m2.start(), m2.group().strip().upper()) for m2 in clause_pat.finditer(body)]
        if not starts:
            return None
        # FROM 必须是第一个
        if not starts[0][1].startswith("FROM"):
            return None
        # 提取 FROM 值
        from_m = re.match(r'FROM\s+"([^"]+)"', body, re.IGNORECASE)
        if not from_m:
            return None
        q.from_path = from_m.group(1)
        # 逐子句切片：从当前子句到下一子句
        for i, (s, name) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(body)
            seg = body[s:end].strip()
            low = name
            if low.startswith("FROM"):
                continue
            if low == "WHERE":
                q.where = seg[len("WHERE"):].strip()
            elif low.startswith("GROUP"):
                # GROUP BY xxx [HAVING yyy]
                gbseg = seg[len("GROUP BY"):].strip()
                hm = re.search(r"\bHAVING\b", gbseg, re.IGNORECASE)
                if hm:
                    q.group_by = gbseg[: hm.start()].strip()
                    q.having = gbseg[hm.end():].strip()
                else:
                    q.group_by = gbseg
            elif low == "HAVING":
                # 单独 HAVING 行（已上面处理，兜底）
                q.having = seg[len("HAVING"):].strip()
            elif low == "FLATTEN":
                q.flatten = True
            elif low == "SORT":
                sm = re.match(r"SORT\s+(\S+)(?:\s+(ASC|DESC))?", seg, re.IGNORECASE)
                if sm:
                    q.sort_field = sm.group(1).rstrip(",")
                    q.sort_dir = (sm.group(2) or "ASC").upper()
            elif low == "LIMIT":
                lm = re.match(r"LIMIT\s+(\d+)", seg, re.IGNORECASE)
                if lm:
                    q.limit = int(lm.group(1))
        return q


def parse_columns(cols_str: str) -> list[tuple[str, str | None]]:
    """解析 TABLE 后的列定义。

    支持：code AS "代码", name AS "名称" / file.link AS "文件" / length(rows) AS "数量"
    / rows.file.link AS "样本" / dateformat(file.mtime,"xx") AS "时间"
    """
    cols: list[tuple[str, str | None]] = []
    # 按逗号切（注意引号内逗号）
    parts: list[str] = []
    buf = ""
    in_q = False
    for ch in cols_str:
        if ch == '"':
            in_q = not in_q
            buf += ch
        elif ch == "," and not in_q:
            if buf.strip():
                parts.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf.strip())
    for p in parts:
        # field AS "alias" / field AS alias / field
        m = re.match(r'^(.*?)\s+AS\s+"([^"]*)"\s*$', p, re.IGNORECASE | re.DOTALL)
        if m:
            cols.append((m.group(1).strip(), m.group(2)))
            continue
        m = re.match(r'^(.*?)\s+AS\s+([^\s,]+)\s*$', p, re.IGNORECASE | re.DOTALL)
        if m:
            cols.append((m.group(1).strip(), m.group(2)))
            continue
        cols.append((p.strip(), None))
    return cols


# --------------------------------------------------------------------------- #
# 表格渲染
# --------------------------------------------------------------------------- #
def render_cell(value: Any, idx: VaultIndex, rec_key: str = "") -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, (list, set, tuple)):
        return ", ".join(str(v) for v in value) or "—"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    s = str(value).strip()
    if s == "" or s == "null":
        return "—"
    return s


def field_value(field_expr: str, rec: FileRecord, idx: VaultIndex, group_key=None, group_rows=None, total=None):
    """对一条记录取 SELECT 字段值。支持 file.xxx / length(rows) / rows.xxx / key / 普通字段 / dateformat。"""
    fe = field_expr.strip()
    low = fe.lower()
    # dateformat(file.mtime, "fmt")
    m = re.match(r'^dateformat\(([^,]+),\s*"([^"]*)"\)\s*$', fe, re.IGNORECASE)
    if m:
        inner = m.group(1).strip()
        fmt = m.group(2)
        v = field_value(inner, rec, idx, group_key=group_key, group_rows=group_rows, total=total)
        dt = None
        if isinstance(v, (date, datetime)):
            dt = v
        elif v is not None:
            s = str(v)
            for pat in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(s[:19] if "%H" in pat else s[:10], pat)
                    break
                except Exception:
                    continue
        if dt is None:
            return "—"
        return dt.strftime(fmt)
    # length(rows)
    if low == "length(rows)":
        if group_rows is not None:
            return len(group_rows)
        return total if total is not None else 0
    # key（GROUP BY 别名）
    if low == "key" or low == "key" and fe == "key":
        return group_key
    if fe == "key":
        return group_key
    # rows.file.link（分组后展开样本）
    if fe.startswith("rows."):
        if group_rows is None:
            return "—"
        sub = fe[len("rows."):]
        links = []
        for r in group_rows:
            rk = r.vault_key
            if sub == "file.link":
                links.append(f"[[{r.vault_key}]]")
            else:
                links.append(render_cell(field_value(sub, r, idx), idx, rk))
        return ", ".join(links) if links else "—"
    # file.link / file.name / file.mtime / file.outlinks / file.inlinks
    if fe.startswith("file."):
        attr = fe[5:]
        rk = rec.vault_key
        if attr == "link":
            return f"[[{rec.vault_key}]]"
        if attr == "name":
            return rec.stem
        if attr == "mtime":
            return rec.mtime
        if attr == "ctime":
            return rec.ctime
        if attr == "outlinks":
            return [f"[[{x}]]" for x in idx.outlinks.get(rk, set())]
        if attr == "inlinks":
            return [f"[[{x}]]" for x in idx.inlinks.get(rk, set())]
        return "—"
    # 普通字段
    v = rec.fm.get(fe)
    return v


def render_table(
    query: Query,
    rows: list[FileRecord],
    idx: VaultIndex,
    grouped: list[tuple[Any, list[FileRecord]]] | None = None,
    total: int | None = None,
) -> str:
    """生成 Markdown 表格。"""
    headers: list[str] = []
    for field, alias in query.columns:
        headers.append(alias if alias else field)
    if not query.without_id and not query.columns:
        headers = ["文件"]
    if not query.without_id:
        # Dataview 默认第一列是 File 链接
        headers = ["文件"] + headers
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")

    def render_row(rec: FileRecord | None, gk=None, grows=None) -> list[str]:
        cells: list[str] = []
        if not query.without_id:
            if rec is not None:
                cells.append(f"[[{rec.vault_key}]]")
            else:
                cells.append("—")
        for field, _alias in query.columns:
            if rec is not None:
                rk = rec.vault_key
                v = field_value(field, rec, idx, group_key=gk, group_rows=grows, total=total)
            else:
                # 无记录（聚合单行）：仍走 field_value 以取 length(rows)=total 等
                v = field_value(field, rows[0] if rows else None, idx, group_key=gk, group_rows=grows, total=total) if rows else (total if field.strip().lower() == "length(rows)" else gk)
            cells.append(render_cell(v, idx, rk if rec else ""))
        return cells

    if grouped is not None:
        for gk, grows in grouped:
            row = render_row(grows[0] if grows else None, gk=gk, grows=grows)
            lines.append("| " + " | ".join(row) + " |")
    else:
        # 聚合单行：SELECT 含 length(rows) 且无 GROUP BY
        is_agg = any(
            f.strip().lower() == "length(rows)" for f, _ in query.columns
        )
        if is_agg and total is not None:
            row = render_row(None)
            lines.append("| " + " | ".join(row) + " |")
        else:
            for rec in rows:
                row = render_row(rec)
                lines.append("| " + " | ".join(row) + " |")
    if len(lines) == 2:  # 只有表头，无数据行
        # 加一个占位空行，避免空表
        lines.append("| " + " | ".join("—" for _ in headers) + " |")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 执行查询
# --------------------------------------------------------------------------- #
def execute(query: Query, current_rec: FileRecord | None, idx: VaultIndex) -> str:
    """执行查询，返回 Markdown 表格字符串。失败抛异常。"""
    candidates = idx.records_from(query.from_path)
    if not candidates and not query.from_path.startswith("10_Reference/investing"):
        # FROM "文件夹" 之类无法解析——视为空
        candidates = []

    current_fm = current_rec.fm if current_rec else {}
    current_key = (
        current_rec.vault_key
        if current_rec
        else ""
    )

    # WHERE 过滤
    filtered: list[FileRecord] = []
    if query.where.strip():
        evaluator = WhereEvaluator(query.where, current_fm, current_key, idx)
        for rec in candidates:
            rk = rec.vault_key
            try:
                if evaluator.eval(rec.fm, rk):
                    filtered.append(rec)
            except WhereEvalError:
                raise
    else:
        filtered = list(candidates)

    # GROUP BY
    if query.group_by:
        gb = query.group_by
        # 去别名 AS
        gb_field = re.sub(r"\s+AS\s+\S+$", "", gb, flags=re.IGNORECASE).strip()
        groups: dict[Any, list[FileRecord]] = defaultdict(list)
        for rec in filtered:
            rk = rec.vault_key
            if gb_field.startswith("file."):
                attr = gb_field[5:]
                if attr == "name":
                    gk = rec.stem
                elif attr == "link":
                    gk = rk
                else:
                    gk = rec.fm.get(attr)
            else:
                gk = rec.fm.get(gb_field)
            groups[gk].append(rec)
        # HAVING length(rows) > N
        grouped_list = list(groups.items())
        if query.having:
            hm = re.match(r"length\(rows\)\s*(>=|>|=|<|<=)\s*(\d+)", query.having)
            if hm:
                op = hm.group(1)
                n = int(hm.group(2))
                cmp = {
                    ">": lambda x: x > n,
                    ">=": lambda x: x >= n,
                    "=": lambda x: x == n,
                    "<": lambda x: x < n,
                    "<=": lambda x: x <= n,
                }[op]
                grouped_list = [(k, rs) for k, rs in grouped_list if cmp(len(rs))]
        # SORT
        if query.sort_field:
            grouped_list = sort_groups(grouped_list, query.sort_field, query.sort_dir)
        # LIMIT（分组场景：限制组数）
        if query.limit is not None:
            grouped_list = grouped_list[: query.limit]
        return render_table(query, [], idx, grouped=grouped_list)

    # 非 GROUP BY：排序 + 限制
    if query.sort_field:
        filtered = sort_records(filtered, query.sort_field, query.sort_dir)
    if query.limit is not None:
        filtered = filtered[: query.limit]
    # total 用于 length(rows) 聚合（无 GROUP BY 场景）
    return render_table(query, filtered, idx, total=len(filtered))


def sort_records(records: list[FileRecord], field: str, direction: str) -> list[FileRecord]:
    reverse = direction.upper() == "DESC"

    def key(rec: FileRecord):
        if field.startswith("file."):
            attr = field[5:]
            if attr == "name":
                v = rec.stem
            elif attr == "mtime":
                v = rec.mtime
            elif attr == "ctime":
                v = rec.ctime
            else:
                v = rec.fm.get(attr)
        else:
            v = rec.fm.get(field)
        return v

    # 区分数值/字符串排序：尝试统一转数值
    def num_key(rec):
        v = key(rec)
        if v is None:
            return (1, 0)  # None 排后
        if isinstance(v, (int, float)):
            return (0, v)
        m = re.match(r"([+-]?\d+(?:\.\d+)?)", str(v))
        if m:
            return (0, float(m.group(1)))
        return (1, str(v))

    try:
        return sorted(records, key=num_key, reverse=reverse)
    except TypeError:
        return sorted(records, key=lambda r: str(key(r)), reverse=reverse)


def sort_groups(groups: list[tuple[Any, list[FileRecord]]], field: str, direction: str):
    reverse = direction.upper() == "DESC"
    field_low = field.lower()

    def key(item):
        gk, rows = item
        if field_low in ("type", "key") or field == "type" or field == "key":
            return str(gk)
        if field_low == "length(rows)" or field_low.startswith("length("):
            return len(rows)
        # 取组内首条记录字段
        if rows:
            rec = rows[0]
            if field.startswith("file."):
                attr = field[5:]
                if attr == "name":
                    return rec.stem
                if attr == "mtime":
                    return rec.mtime
            return rec.fm.get(field)
        return None

    def num_key(item):
        v = key(item)
        if v is None:
            return (1, 0)
        if isinstance(v, (int, float)):
            return (0, v)
        m = re.match(r"([+-]?\d+(?:\.\d+)?)", str(v))
        if m:
            return (0, float(m.group(1)))
        return (1, str(v))

    try:
        return sorted(groups, key=num_key, reverse=reverse)
    except TypeError:
        return sorted(groups, key=lambda x: str(key(x)), reverse=reverse)


# --------------------------------------------------------------------------- #
# 文件处理：替换代码块
# --------------------------------------------------------------------------- #
# 新格式预编译块（可重算）：注释里带 query 原文 base64
#   <!-- dataview-precompiled:<hash> query:<base64> -->
#   | 表格 |
#   <!-- /dataview-precompiled -->
PRECOMPILED_RE = re.compile(
    r"<!-- dataview-precompiled:([a-f0-9]+)(?:(?: query:)([A-Za-z0-9+/=]+))? -->\n(.*?)\n<!-- /dataview-precompiled -->",
    re.DOTALL,
)
# 旧格式预编译块（无 query 标记，不可直接重算）——与 PRECOMPILED_RE 合并匹配
LEGACY_PRECOMPILED_RE = re.compile(
    r"<!-- dataview-precompiled:([a-f0-9]+) -->\n(.*?)\n<!-- /dataview-precompiled -->",
    re.DOTALL,
)
# 裸 dataview 代码块
DATAVIEW_RE = re.compile(r"```dataview\n(.*?)\n```", re.DOTALL)
# 失败标记块
FAILED_RE = re.compile(r"<!-- dataview-failed: [^\n]* -->\n```dataview\n(.*?)\n```", re.DOTALL)
# blockquote 内的 dataview 代码块（每行 > 前缀）
BLOCKQUOTE_DATAVIEW_RE = re.compile(
    r"(>+\s*```dataview\n(?:>.*\n)*?>+\s*```)",
    re.MULTILINE,
)


def _b64_encode(text: str) -> str:
    """base64 编码 query 原文（utf-8）。"""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _b64_decode(s: str) -> str | None:
    """base64 解码，失败返回 None。"""
    try:
        return base64.b64decode(s.encode("ascii")).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return None


def _query_hash(query_text: str) -> str:
    """预编译块 hash——md5(query_text)[:12]，用于块标识 + 旧格式反查。"""
    return hashlib.md5(query_text.encode("utf-8")).hexdigest()[:12]


class QueryHashMap:
    """hash → query 原文 反向映射表。

    旧格式预编译块（无 query 标记）丢失了 query 原文。本表扫描 vault 模板
    和裸 dataview 代码块，建立 md5(query)[:12] → query_text 映射，让旧块
    可升级为新格式（可重算）。
    """

    def __init__(self):
        self._map: dict[str, str] = {}

    def add(self, query_text: str) -> None:
        h = _query_hash(query_text)
        if h not in self._map:
            self._map[h] = query_text

    def lookup(self, hash_str: str) -> str | None:
        return self._map.get(hash_str)

    def build_from_vault(self, root: Path) -> None:
        """扫描模板目录 + 所有裸 dataview 块，填充映射。"""
        # 1. 模板目录
        templates = root / "10_Reference" / "investing" / "templates"
        if templates.is_dir():
            for p in templates.rglob("*.md"):
                try:
                    content = p.read_text(encoding="utf-8")
                except Exception:
                    continue
                for m in DATAVIEW_RE.finditer(content):
                    self.add(m.group(1))
        # 2. 全 vault 裸 dataview 块（含 blockquote 内）
        for p in root.rglob("*.md"):
            if "templates" in p.parts:
                continue
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue
            # 先剥离已预编译块（避免把表格里残留的 dataview 文本误当 query）
            stripped = PRECOMPILED_RE.sub("", content)
            stripped = LEGACY_PRECOMPILED_RE.sub("", stripped)
            stripped = FAILED_RE.sub("", stripped)
            for m in DATAVIEW_RE.finditer(stripped):
                self.add(m.group(1))
            # blockquote 内 dataview 块
            for m in BLOCKQUOTE_DATAVIEW_RE.finditer(stripped):
                raw = m.group(1)
                inner = []
                for ln in raw.split("\n"):
                    s = re.sub(r"^>+\s?", "", ln)
                    inner.append(s)
                body = "\n".join(inner)
                body = re.sub(r"^```dataview\n", "", body)
                body = re.sub(r"\n```$", "", body)
                if body.strip():
                    self.add(body)


# 表头别名 → frontmatter 字段名（用于旧块 query 重建）
ALIAS_TO_FIELD: dict[str, str] = {
    "周期": "period",
    "营收(亿)": "revenue",
    "净利(亿)": "net_profit",
    "ROE%": "roe",
    "毛利率%": "gross_margin",
    "净利率%": "net_margin",
    "EPS": "eps",
    "BVPS": "bvps",
    "名称": "name",
    "行业": "industry",
    "市值": "market_cap",
    "日期": "created",
    "PE(TTM)": "pe_ttm",
    "PB": "pb",
    "PS(TTM)": "ps_ttm",
    "PCF(TTM)": "pcf_ttm",
    "PE分位%": "pe_percentile",
    "PB分位%": "pb_percentile",
    "PEG": "peg",
    "股息率%": "dividend_yield",
    "远期PE": "forward_pe",
    "一致EPS": "consensus_eps",
    "股票代码": "code",
    "报告期": "period",
}


def _parse_header_row(table: str) -> list[str] | None:
    """从表格文本提取表头列名（已去除空/分隔）。"""
    lines = table.strip().split("\n")
    if not lines:
        return None
    header = lines[0]
    cols = [c.strip() for c in header.split("|")]
    # 去掉首尾空
    while cols and cols[0] == "":
        cols.pop(0)
    while cols and cols[-1] == "":
        cols.pop()
    if not cols:
        return None
    # 第二行是分隔（|---|---|），校验
    if len(lines) < 2 or not re.match(r"^\|?[-\s|:]+$", lines[1]):
        return None
    return cols


def reconstruct_query_from_block(
    block_table: str, current_rec: FileRecord, idx: VaultIndex
) -> str | None:
    """从旧预编译块的表格内容重建 query 文本。

    策略：表头列名 → 别名 → 字段；FROM 路径按字段归属推断；WHERE = type+code。
    首列"文件"→ 非 WITHOUT ID（Dataview 默认 file.link 列）。

    FROM 启发式：
    - 字段含 name/industry/market_cap → FROM stocks（所属股票表）
    - 字段含 period/revenue/net_profit/roe/gross_margin/net_margin → FROM 当前目录（趋势表）
    - 字段含 pe_ttm/pb/pe_percentile/pb_percentile/created → FROM 当前目录（估值序列表）
    """
    cols = _parse_header_row(block_table)
    if not cols:
        return None
    fm = current_rec.fm
    file_type = fm.get("type", "")
    cur_dir = ""
    try:
        cur_dir = current_rec.path.resolve().relative_to(VAULT).parent.as_posix()
    except ValueError:
        return None
    # 字段集合
    fields: list[str] = []
    has_file_col = False
    select_cols: list[str] = []
    first = True
    for c in cols:
        if c == "文件":
            if first:
                has_file_col = True
                first = False
                continue
            select_cols.append('file.link AS "文件"')
            first = False
            continue
        first = False
        field = ALIAS_TO_FIELD.get(c, c)
        fields.append(field)
        select_cols.append(f'{field} AS "{c}"')
    # FROM 路径推断
    stock_fields = {"name", "industry", "market_cap"}
    if fields and any(f in stock_fields for f in fields) and not any(
        f in {"revenue", "net_profit", "roe", "pe_ttm", "pb"} for f in fields
    ):
        # 含 name/industry/market_cap 且无财务/估值字段 → FROM stocks
        from_dir = "10_Reference/investing/stocks"
        where_type = "stock"
    else:
        from_dir = cur_dir
        where_type = file_type
    # WHERE
    where_parts = []
    if where_type:
        where_parts.append(f'type = "{where_type}"')
    if fm.get("code"):
        where_parts.append("code = this.code")
    where = " AND ".join(where_parts) if where_parts else ""
    # SORT/LIMIT（按 type 推断）
    if where_type == "metric":
        sort = "SORT period DESC"
        limit = "LIMIT 8"
    elif where_type == "valuation":
        sort = "SORT created DESC"
        limit = "LIMIT 10"
    else:
        # stocks：按 code 排序
        sort = "SORT code ASC"
        limit = ""
    # 拼 query
    parts = ["TABLE"]
    if select_cols:
        parts.append(",\n  ".join(select_cols))
    parts.append(f'FROM "{from_dir}"')
    if where:
        parts.append(f"WHERE {where}")
    if sort:
        parts.append(sort)
    if limit:
        parts.append(limit)
    return "\n".join(parts) + "\n"


def process_file(path: Path, idx: VaultIndex, dry_run: bool, qmap: QueryHashMap | None = None) -> dict:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return {"status": "skip"}
    original = content
    current_rec = FileRecord(path, content)

    stats = {"parsed": 0, "success": 0, "failed": 0, "unchanged": 0, "recomputed": 0}

    def _wrap_block(query_text: str, table: str, blockquote: bool = False) -> str:
        """生成新格式预编译块（带 query base64）。"""
        h = _query_hash(query_text)
        qb64 = _b64_encode(query_text)
        if blockquote:
            lines = [
                f"<!-- dataview-precompiled:{h} query:{qb64} -->",
                *table.split("\n"),
                "<!-- /dataview-precompiled -->",
            ]
            return "\n".join(f"> {ln}" for ln in lines)
        return (
            f"<!-- dataview-precompiled:{h} query:{qb64} -->\n"
            f"{table}\n"
            f"<!-- /dataview-precompiled -->"
        )

    def _handle_query(query_text: str, blockquote: bool = False) -> tuple[str, bool]:
        """执行单个查询，返回 (替换文本, 是否成功)。"""
        stats["parsed"] += 1
        try:
            query = Query.parse(query_text)
            if query is None:
                stats["failed"] += 1
                return (
                    f"<!-- dataview-failed: 无法解析查询类型 -->\n```dataview\n{query_text}\n```",
                    False,
                )
            table = execute(query, current_rec, idx)
            stats["success"] += 1
            return _wrap_block(query_text, table, blockquote=blockquote), True
        except Exception as e:
            stats["failed"] += 1
            if blockquote:
                return _rebuild_blockquote_dataview(query_text), False
            return f"<!-- dataview-failed: {str(e)[:80]} -->\n```dataview\n{query_text}\n```", False

    def _rebuild_blockquote_dataview(query_text: str) -> str:
        lines = query_text.split("\n")
        return "\n".join(["> ```dataview", *[f"> {l}" for l in lines], "> ```"])

    def replace_block(m: re.Match) -> str:
        query_text = m.group(1)
        text, _ok = _handle_query(query_text, blockquote=False)
        return text

    def replace_blockquote_block(m: re.Match) -> str:
        raw = m.group(1)
        inner_lines = []
        for ln in raw.split("\n"):
            stripped = re.sub(r"^>+\s?", "", ln)
            inner_lines.append(stripped)
        body = "\n".join(inner_lines)
        body = re.sub(r"^```dataview\n", "", body)
        body = re.sub(r"\n```$", "", body)
        text, _ok = _handle_query(body, blockquote=True)
        return text

    # --- 可重算：处理已预编译块 ---
    # 新格式块（带 query base64）：解码 query 重算，表格变了才更新
    # 旧格式块（无 query）：hash 反查 qmap → 失败则从表格表头重建 query → 升级为新格式
    def recompute_precompiled(m: re.Match) -> str:
        h = m.group(1)
        qb64 = m.group(2)  # 新格式有；旧格式 None
        old_table = m.group(3) if m.group(3) is not None else ""
        # 取 query 原文：优先 base64 解码 → hash 反查 → 表头重建
        query_text = None
        if qb64:
            query_text = _b64_decode(qb64)
        if query_text is None and qmap is not None:
            query_text = qmap.lookup(h)
        if query_text is None and old_table:
            query_text = reconstruct_query_from_block(old_table, current_rec, idx)
        if query_text is None:
            # 无法重算——保留原块
            return m.group(0)
        stats["parsed"] += 1
        try:
            query = Query.parse(query_text)
            if query is None:
                stats["failed"] += 1
                return m.group(0)
            new_table = execute(query, current_rec, idx)
            stats["success"] += 1
            # 表格未变 → 保留原块；变了 → 写新格式块（带 query base64）
            new_block = _wrap_block(query_text, new_table)
            if new_block == m.group(0):
                stats["unchanged"] += 1
                return m.group(0)
            stats["recomputed"] += 1
            return new_block
        except Exception:
            stats["failed"] += 1
            return m.group(0)

    # blockquote 内预编译块的重算
    bq_precompiled_re = re.compile(
        r"(>+\s*<!-- dataview-precompiled:([a-f0-9]+)(?:(?: query:)([A-Za-z0-9+/=]+))? -->\n(?:>.*\n)*?>+\s*<!-- /dataview-precompiled -->)",
        re.MULTILINE,
    )

    def recompute_bq_precompiled(m: re.Match) -> str:
        raw = m.group(0)
        h = m.group(2)
        qb64 = m.group(3)
        # 提取旧表格（去 > 前缀）
        inner = []
        for ln in raw.split("\n"):
            s = re.sub(r"^>+\s?", "", ln)
            inner.append(s)
        body = "\n".join(inner)
        old_table = re.sub(r"^<!-- dataview-precompiled:[a-f0-9]+(?: query:[A-Za-z0-9+/=]+)? -->\n", "", body)
        old_table = re.sub(r"\n<!-- /dataview-precompiled -->$", "", old_table)
        # 取 query 原文
        query_text = None
        if qb64:
            query_text = _b64_decode(qb64)
        if query_text is None and qmap is not None:
            query_text = qmap.lookup(h)
        if query_text is None and old_table:
            query_text = reconstruct_query_from_block(old_table, current_rec, idx)
        if query_text is None:
            return m.group(0)
        stats["parsed"] += 1
        try:
            query = Query.parse(query_text)
            if query is None:
                stats["failed"] += 1
                return m.group(0)
            new_table = execute(query, current_rec, idx)
            stats["success"] += 1
            new_block = _wrap_block(query_text, new_table, blockquote=True)
            if new_block == m.group(0):
                stats["unchanged"] += 1
                return m.group(0)
            stats["recomputed"] += 1
            return new_block
        except Exception:
            stats["failed"] += 1
            return m.group(0)

    # 1. 先重算 blockquote 内预编译块
    content = bq_precompiled_re.sub(recompute_bq_precompiled, content)
    # 2. 重算普通预编译块
    content = PRECOMPILED_RE.sub(recompute_precompiled, content)
    # 3. 处理 blockquote 内裸 dataview 块
    content = BLOCKQUOTE_DATAVIEW_RE.sub(replace_blockquote_block, content)
    # 4. 处理裸 dataview 块
    content = DATAVIEW_RE.sub(replace_block, content)

    if content == original:
        stats["unchanged"] = stats["parsed"]
        return {"status": "unchanged", **stats}

    if not dry_run:
        path.write_text(content, encoding="utf-8")
    return {"status": "changed", **stats}


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="预编译 Dataview 查询为静态 Markdown 表格")
    ap.add_argument("--dry-run", action="store_true", help="不写文件，仅统计")
    ap.add_argument("--stats-only", action="store_true", help="仅统计不写文件")
    ap.add_argument("--path", default=str(INVESTING), help="处理路径")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    target = Path(args.path)
    print(f"[1/4] 扫描 vault: {target}")
    idx = VaultIndex(target)
    print(f"    索引文件数: {len(idx.records)}")
    print(f"    双链边数: {sum(len(v) for v in idx.outlinks.values())}")

    # 构建 hash → query 反查表（用于旧格式块升级）
    print("[2/4] 构建 query 反查表")
    qmap = QueryHashMap()
    qmap.build_from_vault(VAULT)
    print(f"    query 模板数: {len(qmap._map)}")

    # 收集待处理 .md
    md_files = [p for p in target.rglob("*.md")]
    # 排除 templates
    md_files = [p for p in md_files if "templates" not in p.parts]

    print(f"[3/4] 处理 {len(md_files)} 个文件")
    total = {"parsed": 0, "success": 0, "failed": 0, "changed": 0, "unchanged": 0, "recomputed": 0}
    failed_samples = []
    for i, p in enumerate(sorted(md_files), 1):
        if i % 200 == 0:
            print(f"    进度 {i}/{len(md_files)}")
        r = process_file(p, idx, dry_run=args.dry_run or args.stats_only, qmap=qmap)
        total["parsed"] += r.get("parsed", 0)
        total["success"] += r.get("success", 0)
        total["failed"] += r.get("failed", 0)
        total["recomputed"] += r.get("recomputed", 0)
        if r.get("status") == "changed":
            total["changed"] += 1
        else:
            total["unchanged"] += 1
        if args.verbose and r.get("failed"):
            failed_samples.append((p, r))

    print(f"[4/4] 统计")
    print(f"    解析 dataview 块: {total['parsed']}")
    print(f"    成功替换: {total['success']}")
    print(f"    失败保留: {total['failed']}")
    print(f"    重算更新: {total['recomputed']}")
    print(f"    变更文件: {total['changed']}")
    print(f"    未变文件: {total['unchanged']}")
    if args.dry_run or args.stats_only:
        print("    （dry-run 模式，未写文件）")

    if failed_samples:
        print("\n失败样本（前 10）:")
        for p, r in failed_samples[:10]:
            print(f"  {p.resolve().relative_to(VAULT)}")

    # 验证残留
    remaining = 0
    for p in md_files:
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        # 排除预编译块和失败标记块后的裸 dataview 块
        t2 = PRECOMPILED_RE.sub("", t)
        t2 = FAILED_RE.sub("", t2)
        remaining += len(re.findall(r"```dataview\b", t2))
    print(f"\n验证：残留裸 dataview 块 = {remaining}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
