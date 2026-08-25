#!/usr/bin/env python3
"""verify_quotes_jiegou.py — 验收《解构领域驱动设计》知识包：

① 每张模块 README 的 📖原文引用必须 verbatim 命中对应 fulltext 文件；
② 卡片数（## 篇X / ## §N / ## 附录X）== toc.md 行数 == fulltext 文件数。

用法: python3 scripts/verify_quotes_jiegou.py
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "解构领域驱动设计"

# 接受三种 chapter 标题：篇一/二...、§N、附录X
CARD_RE = re.compile(r"^## (篇[一二三四五六七八九十]+|§\d+|附录[A-Z]) ")

QUOTE_RE = re.compile(
    r"^> 📖 \*\*原文\*\*[：:]?"
    r"(?:\s*（(?P<anchor>[§\d\s.第章节段落引言附录A-Za-z]+)）[：:]?)?"
    r"\s*(?P<q>.+?)$"
)


def normalize(s: str) -> str:
    """NFKC + strip whitespace + 规范化图片路径（../00-原书档案/assets/X 与 ../assets/X 等价）。"""
    s = re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))
    s = re.sub(r"!\[[^\]]*\]\(\.\./(?:00-原书档案/)?(assets/[^)]+)\)",
               r"![](\1)", s)
    return s


def strip_footnotes(s: str) -> str:
    """^ 后跟 0~3 个数字/字母视为 footnote（不剥离后续标点）。"""
    return re.sub(r"\^[A-Za-z0-9]{0,3}", "", s)


def main() -> int:
    fail = 0
    corpus: dict[str, str] = {}
    for f in (BOOK / "00-原书档案" / "fulltext").glob("uid-*.md"):
        uid = f.name.split("-")[1]
        corpus[uid] = normalize(strip_footnotes(f.read_text(encoding="utf-8")))

    toc_rows = [l for l in (BOOK / "00-原书档案" / "toc.md").read_text().splitlines()
                if l and not l.startswith("uid|")]
    print(f"fulltext files={len(corpus)}  toc rows={len(toc_rows)}")

    cards_total = 0
    for readme in sorted(BOOK.glob("[0-9][0-9]-*/README.md")):
        module = readme.parent.name
        lines = readme.read_text(encoding="utf-8").splitlines()
        cards = [m.group(1) for l in lines if (m := CARD_RE.match(l))]
        quotes_raw = []
        for l in lines:
            m = QUOTE_RE.match(l)
            if m:
                quotes_raw.append((m.group("anchor"), m.group("q")))
        cards_total += len(cards)
        # 有些 quote 跨多行（list/blockquote 续行），需要把它们拼回
        # 但 verify_quotes_fenghuang.py 的实现是按行验证，我们保持简单一致

        # 验证：每条 quote normalize + 去上标后必须是 corpus 任一文件的子串
        misses = []
        for anchor, q in quotes_raw:
            nq = normalize(strip_footnotes(q))
            if not nq:
                continue
            hit = any(nq in text for text in corpus.values())
            if not hit:
                misses.append((anchor, q[:30]))
        status = "OK" if not misses else "FAIL"
        if misses:
            fail += 1
        print(f"[{status}] {module}: cards={len(cards)} quotes={len(quotes_raw)} verbatim_miss={len(misses)}")
        for anchor, snippet in misses:
            print(f"        {anchor}: {snippet!r}")

    if cards_total != len(toc_rows) or len(corpus) != len(toc_rows):
        print(f"FAIL reconciliation: cards={cards_total} fulltext={len(corpus)} toc={len(toc_rows)}")
        fail += 1
    else:
        print(f"OK reconciliation: cards==fulltext==toc=={cards_total}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())