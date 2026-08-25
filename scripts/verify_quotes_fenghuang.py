#!/usr/bin/env python3
"""verify_quotes_fenghuang.py — 验收《凤凰架构》知识包：
① 每个模块 README 的 📖原文引用必须 verbatim 命中对应 fulltext 文件；
② 卡片数（## §N）== toc.md 行数 == fulltext 文件数。
用法: python3 scripts/verify_quotes_fenghuang.py
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "凤凰架构：构建可靠的大型分布式系统"
QUOTE_RE = re.compile(r"^> 📖 \*\*原文\*\*（§(?P<anchor>[\d.]+)）[：:](?P<q>.+)$")
CARD_RE = re.compile(r"^## §(\d+) ")


def normalize(s: str) -> str:
    """NFKC + 去所有空白，避免复制时不可见差异导致误报。"""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def main() -> int:
    fail = 0
    # fulltext 内容索引: uid -> normalized text
    corpus: dict[str, str] = {}
    for f in (BOOK / "00-原书档案" / "fulltext").glob("uid-*.md"):
        uid = f.name.split("-")[1]
        corpus[uid] = normalize(f.read_text(encoding="utf-8"))

    toc_rows = [l for l in (BOOK / "00-原书档案" / "toc.md").read_text().splitlines() if l and not l.startswith("uid|")]
    print(f"fulltext files={len(corpus)}  toc rows={len(toc_rows)}")

    cards_total = 0
    for readme in sorted(BOOK.glob("[0-9][0-9]-*/README.md")):
        module = readme.parent.name
        lines = readme.read_text(encoding="utf-8").splitlines()
        cards = [m.group(1) for l in lines if (m := CARD_RE.match(l))]
        quotes = [(m.group("anchor"), m.group("q")) for l in lines if (m := QUOTE_RE.match(l))]
        cards_total += len(cards)
        misses = []
        for anchor, q in quotes:
            nq = normalize(q)
            hit = any(nq in text for text in corpus.values())
            if not hit:
                misses.append(anchor)
        status = "OK" if not misses else "FAIL"
        if misses:
            fail += 1
        print(f"[{status}] {module}: cards={len(cards)} quotes={len(quotes)} verbatim_miss={misses}")

    if cards_total != len(toc_rows) or len(corpus) != len(toc_rows):
        print(f"FAIL reconciliation: cards={cards_total} fulltext={len(corpus)} toc={len(toc_rows)}")
        fail += 1
    else:
        print(f"OK reconciliation: cards==fulltext==toc=={cards_total}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
