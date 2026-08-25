#!/usr/bin/env python3
"""distill_epub_fenghuang.py — 凤凰架构 epub → 00-原书档案/。

与 distill_epub.py 的差异：本书 epub 每个 §N.M 小节是独立 xhtml，
章级节点只是标题页，所以按 NCX level-1 章 = 自身 + 全部后代节点 src 合并成一个 fulltext 文件。

用法:
    python3 scripts/distill_epub_fenghuang.py --src <EPUB> --out <书包>/00-原书档案
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup

from distill_epub import html_to_markdown, parse_part_label, sha256_of_file, slugify_chapter

NCX_NS = "{http://www.daisy.org/z3986/2005/ncx/}"
PART_RE = re.compile(r"^第[一二三四五六七八九十百千]+部分\s+")
CHAPTER_RE = re.compile(r"^第(\d+)章\s+(.+)$")


def walk_nav(nav: ET.Element, depth: int = 0):
    """yield {depth, label, src, el}，DFS。src 已去 fragment。"""
    for np in nav.findall(f"{NCX_NS}navPoint"):
        lab = np.find(f"{NCX_NS}navLabel/{NCX_NS}text")
        label = (lab.text or "").strip() if lab is not None else ""
        con = np.find(f"{NCX_NS}content")
        src = (con.get("src") if con is not None else "") or ""
        yield {"depth": depth, "label": label, "src": src.split("#", 1)[0], "el": np}
        yield from walk_nav(np, depth + 1)


def norm_title(label: str) -> str:
    """「第1章　服务架构演进史」→「第1章 服务架构演进史」（U+3000 → 空格）。"""
    return re.sub(r"[  ]+", " ", label.strip())


def resolve_zip_path(xhtml_in_zip: str, href: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(xhtml_in_zip), href))


def body_inner_html(zf: zipfile.ZipFile, xhtml: str) -> str:
    soup = BeautifulSoup(zf.read(xhtml).decode("utf-8", errors="replace"), "lxml")
    body = soup.find("body") or soup
    # 去链接留文本：脚注/交叉引用锚点在归档 markdown 里只会变死链
    for a in body.find_all("a"):
        a.unwrap()
    return "".join(str(c) for c in body.children if getattr(c, "name", None))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()
    if not src.is_file():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        return 2
    if out.exists():
        if not args.force:
            print(f"ERROR: out dir exists (use --force): {out}", file=sys.stderr)
            return 2
        shutil.rmtree(out)

    file_sha = sha256_of_file(src)
    out.mkdir(parents=True, exist_ok=True)
    (out / "epub").mkdir(exist_ok=True)
    (out / "fulltext").mkdir(exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    epub_copy = out / "epub" / src.name
    shutil.copy2(src, epub_copy)

    # ---- assets：zip 内图片 → assets/<sha16>.<ext>；key = zip 条目路径 ----
    img_map: dict[str, str] = {}
    with zipfile.ZipFile(str(src)) as zf:
        for name in zf.namelist():
            if name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")):
                data = zf.read(name)
                ext = os.path.splitext(name)[1].lstrip(".").lower()
                if ext == "jpeg":
                    ext = "jpg"
                h = hashlib.sha256(data).hexdigest()[:16]
                apath = out / "assets" / f"{h}.{ext}"
                if not apath.exists():
                    apath.write_bytes(data)
                img_map[name] = f"../assets/{h}.{ext}"

        # ---- NCX 解析 ----
        ncx_path = next(n for n in zf.namelist() if n.endswith("toc.ncx"))
        navmap = ET.fromstring(zf.read(ncx_path)).find(f"{NCX_NS}navMap")
        points = list(walk_nav(navmap))

        chapters: list[dict] = []  # {num,title,part,srcs:[xhtml...]}
        current_part = ""
        part_count = sub_count = front_count = 0
        for p in points:
            if p["depth"] == 0 and PART_RE.match(p["label"]):
                current_part = parse_part_label(p["label"]) or norm_title(p["label"])
                part_count += 1
            elif p["depth"] == 1 and CHAPTER_RE.match(norm_title(p["label"])):
                t = norm_title(p["label"])
                m = CHAPTER_RE.match(t)

                def collect(el, acc):
                    con = el.find(f"{NCX_NS}content")
                    s = (con.get("src") if con is not None else "") or ""
                    s = s.split("#", 1)[0]
                    if s and s not in acc:
                        acc.append(s)
                    for child_np in el.findall(f"{NCX_NS}navPoint"):
                        collect(child_np, acc)

                srcs: list[str] = []
                collect(p["el"], srcs)
                chapters.append({"num": int(m.group(1)), "title": t,
                                 "part": current_part, "srcs": srcs})
            elif p["depth"] >= 1:
                sub_count += 1
            else:
                front_count += 1

        # ---- 逐章合并转 markdown ----
        toc_rows = []
        uid = 0
        for ch in chapters:
            parts_html = []
            for xh in ch["srcs"]:
                inner = body_inner_html(zf, xh)
                soup = BeautifulSoup(f"<div>{inner}</div>", "lxml")
                # img src 按所在 xhtml 目录解析为 assets 路径
                for img in soup.find_all("img"):
                    raw = img.get("src", "")
                    zp = resolve_zip_path(xh, raw)
                    img["src"] = img_map.get(zp, raw)
                parts_html.append(str(soup))
            md = html_to_markdown("<div>" + "\n".join(parts_html) + "</div>", {})
            wc = len(re.sub(r"\s+", "", md))
            uid += 1
            u = f"{uid:02d}"
            fname = f"uid-{u}-{slugify_chapter(ch['title'])}.md"
            fm = ("---\n"
                  f"uid: {u}\nlevel: 1\nchapterNumber: §{ch['num']}\n"
                  f"title: {ch['title']}\nwordCount: {wc}\nparentPart: {ch['part']}\n"
                  "---\n\n")
            (out / "fulltext" / fname).write_text(fm + md, encoding="utf-8")
            toc_rows.append({"uid": u, "chapterNumber": f"§{ch['num']}", "title": ch["title"],
                             "wordCount": str(wc), "parentPart": ch["part"], "file": fname})

    meta = {
        "title": "凤凰架构：构建可靠的大型分布式系统",
        "creator": "周志明",
        "sourcePath": str(src),
        "fileSha256": file_sha,
        "fileSize": src.stat().st_size,
        "ncxChapterCount": len(chapters),
        "ncxSubchapterCount": sub_count,
        "partCount": part_count,
        "frontMatterExcluded": front_count,
    }
    with zipfile.ZipFile(str(src)) as zf:
        from ebooklib import epub as epub_lib
        book = epub_lib.read_epub(str(src))
        for q in ("identifier", "language"):
            rows = book.get_metadata("DC", q)
            if rows:
                meta[q] = rows[0][0]
    (out / "book-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")

    lines = ["uid|chapterNumber|title|wordCount|parentPart|file"]
    lines += [f"{r['uid']}|{r['chapterNumber']}|{r['title']}|{r['wordCount']}|{r['parentPart']}|{r['file']}"
              for r in toc_rows]
    (out / "toc.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"PARTS={part_count} CHAPTERS={len(chapters)} SUBS={sub_count} FRONT={front_count}")
    print(f"FULLTEXT_COUNT={uid} ASSETS={len(img_map)}")
    for r in toc_rows:
        print(f"  {r['uid']} {r['chapterNumber']} {r['title']} ({r['wordCount']}) -> {r['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
