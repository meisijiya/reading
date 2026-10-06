#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epub_toc_json.py — 从 epub_extract 的 pipe 版 toc.md 补出 toc.json（含每章 sha256），
让 epub 包与 PDF 包（pdf_extract.py）在结构与字段上对齐。"""
import sys, io, os, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = sys.argv[1]
ARC = os.path.join(ROOT, "00-原书档案")
FT = os.path.join(ARC, "fulltext")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = []
with open(os.path.join(ARC, "toc.md"), encoding="utf-8") as f:
    head = next(f).strip()
    assert head.startswith("uid|"), head
    for line in f:
        line = line.strip()
        if not line:
            continue
        uid, kind, chnum, title, words, fname = line.split("|", 5)
        p = os.path.join(FT, fname)
        rows.append({
            "uid": uid.replace("uid-", "ch").split("-")[0] if fname.startswith("uid-") else uid,
            "title": title,
            "kind": kind,
            "pdf_pages": None,
            "file": fname,
            "sha256": sha256_file(p),
            "bytes": os.path.getsize(p),
            "wordCount": int(words),
        })

out = {
    "source": "EPUB (local file)",
    "granularity": "NCX level-1 = 一章一文件",
    "chapters": rows,
}
with open(os.path.join(ARC, "toc.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"toc.json written: {len(rows)} chapters")
for r in rows:
    print(f"  ch{r['uid']}  {r['bytes']:>7,}B  {r['sha256'][:16]}  {r['title']}")