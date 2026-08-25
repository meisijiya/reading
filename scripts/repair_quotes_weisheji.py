#!/usr/bin/env python3
"""repair_quotes_weisheji.py — 用 difflib 对齐修复未 verbatim 命中的 📖 引文。

算法：引文与语料都在完全归一化空间做 SequenceMatcher 对齐；
匹配率≥60% 且语料区间杂质≤1.35 倍时，把该区间经索引映射回可读原文，
整段替换原引用行——替换文本逐字来自语料。
用法: python3 scripts/repair_quotes_weisheji.py [--dry-run]
"""
from __future__ import annotations

import difflib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "微服务设计（第2版）"
QUOTE_RE = re.compile(r"^(> 📖 \*\*原文\*\*（§[\d.]+）[：:])(.+)$")
FOLD = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "…": "", "—": "-", "－": "-"})


def canon(s: str) -> str:
    return re.sub(r"[\s*`#><]+", "", unicodedata.normalize("NFKC", s).translate(FOLD))


def readable(s: str) -> str:
    """半归一化：保留空白可读版（仅去 markdown 装饰符）。"""
    return unicodedata.normalize("NFKC", s).translate(FOLD).replace("*", "").replace("`", "").replace("#", "").replace(">", "")


def collapse(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def norm_index_map(rd: str) -> tuple[str, list[int]]:
    """返回 (规范化串, 规范化字符 -> rd 下标 的映射)。"""
    cn = []
    idx = []
    for i, c in enumerate(rd):
        if c in " \t\n":
            continue
        cn.append(c)
        idx.append(i)
    return "".join(cn), idx


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = sorted((BOOK / "00-原书档案" / "fulltext").glob("uid-*.md"))
    corpora: dict[str, tuple[str, str, list[int]]] = {}
    for f in files:
        uid = f.name.split("-")[1]
        rd = readable(f.read_text(encoding="utf-8"))
        cn, idx = norm_index_map(rd)
        corpora[uid] = (rd, cn, idx)

    def hits(nnq: str) -> bool:
        return any(nnq in cn for _, cn, _ in corpora.values())

    def align_repair(q: str) -> str | None:
        nq = canon(q)
        if len(nq) < 8:
            return None
        best = None  # (matched, rep_text)
        for _uid, (rd, cn, idx) in corpora.items():
            sm = difflib.SequenceMatcher(None, nq, cn, autojunk=False)
            blocks = [b for b in sm.get_matching_blocks() if b.size > 0]
            if not blocks:
                continue
            matched = sum(b.size for b in blocks)
            if matched < 0.6 * len(nq):
                continue
            j0, j1 = blocks[0].b, blocks[-1].b + blocks[-1].size
            # 冗余容忍：区间比引文多出的语料字符 ≤120 即采纳（拼接句间跳字的情形），超大跨度视为假对齐拒绝
            if (j1 - j0) - matched > 120:
                continue
            rep = collapse(rd[idx[j0]:idx[j1 - 1] + 1])
            if best is None or matched > best[0]:
                best = (matched, rep)
        return best[1] if best else None

    total_fixed = total_dropped = total_kept = 0
    for readme_path in sorted(BOOK.glob("[0-9][0-9]-*/README.md")):
        lines = readme_path.read_text(encoding="utf-8").splitlines()
        out: list[str | None] = []
        fixed = kept = dropped = 0
        for l in lines:
            m = QUOTE_RE.match(l)
            if not m:
                out.append(l)
                continue
            q = m.group(2)
            if hits(canon(q)):
                kept += 1
                out.append(l)
                continue
            rep = align_repair(q)
            if rep and hits(canon(rep)):
                out.append(m.group(1) + rep)
                fixed += 1
            else:
                out.append(None)
                dropped += 1
        final = [l for l in out if l is not None]
        if not dry and (fixed or dropped):
            readme_path.write_text("\n".join(final) + "\n", encoding="utf-8")
        print(f"{readme_path.parent.name}: kept={kept} fixed={fixed} dropped={dropped}")
        total_fixed += fixed
        total_dropped += dropped
        total_kept += kept
    print(f"TOTAL kept={total_kept} fixed={total_fixed} dropped={total_dropped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
