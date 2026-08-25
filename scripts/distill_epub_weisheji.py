#!/usr/bin/env python3
"""distill_epub_weisheji.py — 提取《微服务设计（第2版）》epub → 00-原书档案/。

结构特点（区别于橙皮书/凤凰架构）：
- NCX 扁平（全部 depth 0），一章一个 xhtml（chapter009..chapter026 = 第1..16章）
- 小节标题是成对 <p class="part">：「2.1」单独一段，下一段是标题
- 子小节合并为一段：「2.2.1信息隐藏」
用法: python3 scripts/distill_epub_weisheji.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import warnings
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "book" / "微服务设计（第2版） (【英】萨姆·纽曼) (z-library.sk, 1lib.sk, z-lib.sk).epub"
OUT = ROOT / "微服务设计（第2版）" / "00-原书档案"
PREFIX = "EPUB/"
SEC_RE = re.compile(r"^(\d+\.\d+)$")
SUBSEC_RE = re.compile(r"^(\d+\.\d+\.\d+)\s*(.*)$")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inline(el) -> str:
    if el.name is None:
        return el.string or ""
    if el.name in ("b", "strong"):
        inner = "".join(inline(c) for c in el.children).strip()
        return f"**{inner}**" if inner else ""
    if el.name in ("i", "em"):
        inner = "".join(inline(c) for c in el.children).strip()
        return f"*{inner}*" if inner else ""
    if el.name == "code":
        return f"`{el.get_text()}`"
    if el.name == "br":
        return "\n"
    if el.name == "img":
        src = el.get("src", "")
        alt = el.get("alt", "")
        return f"![{alt}]({IMG_MAP.get(_norm(src), src)})"
    return "".join(inline(c) for c in el.children)


def _norm(src: str) -> str:
    s = re.sub(r"^(EPUB/)+", "", src.strip())
    s = re.sub(r"^(\.\./)+", "", s)
    return s.lstrip("/")


def plain(el) -> str:
    if el.name is None:
        return el.string or ""
    if el.name == "br":
        return "\n"
    return "".join(plain(c) for c in el.children)


def flush(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def chapter_to_markdown(soup) -> str:
    """返回 markdown。"""
    lines: list[str] = []
    body = soup.find("body") or soup
    # 顶层元素拍平收集（div 嵌套穿透）
    blocks = [c for c in body.find_all(["h1", "h2", "h3", "p", "blockquote", "ul", "ol", "pre", "img"], recursive=True)]
    # 过滤嵌套重复：只留最外层
    seen = set()
    tops = []
    for el in blocks:
        anc = el.find_parent(["blockquote", "li"])
        key = id(el)
        if key in seen:
            continue
        tops.append(el)

    chap_emitted = False
    chap_num_pending: str | None = None
    pending_sec_num: str | None = None
    i = 0
    while i < len(tops):
        el = tops[i]
        name = el.name
        if name in ("h1", "h2", "h3"):
            txt = flush(el.get_text())
            if txt:
                if not chap_emitted and re.match(r"^第\d+章$", txt):
                    chap_num_pending = txt  # 等下一个 h2 章题合并
                elif not chap_emitted and chap_num_pending:
                    lines += ["", f"## {chap_num_pending} {txt}", ""]
                    chap_emitted = True
                    chap_num_pending = None
                elif not chap_emitted:
                    lines += ["", f"## {txt}", ""]
                    chap_emitted = True
                else:
                    lines += ["", f"### {txt}", ""]
            i += 1
            continue
        if name == "p":
            raw = flush(plain(el))
            m_sec = SEC_RE.match(raw)
            m_sub = SUBSEC_RE.match(raw)
            if m_sec and i + 1 < len(tops):
                nxt = tops[i + 1]
                ntxt = flush(plain(nxt)) if nxt.name == "p" else ""
                title = ntxt if ntxt and not SEC_RE.match(ntxt) and not SUBSEC_RE.match(ntxt) else ""
                lines += ["", f"### {raw} {title}".rstrip(), ""]
                i += 2 if title else 1
                continue
            if m_sub:
                num, rest = m_sub.group(1), m_sub.group(2).strip()
                lines += ["", f"#### {num} {rest}".rstrip(), ""]
                i += 1
                continue
            txt = "".join(inline(c) for c in el.children).strip()
            txt = re.sub(r"\n{3,}", "\n\n", txt)
            if txt:
                lines += ["", txt, ""]
            i += 1
            continue
        if name == "blockquote":
            for c in el.find_all(["p"], recursive=True):
                t = flush(c.get_text())
                if t:
                    lines.append("> " + t)
            lines.append("")
            i += 1
            continue
        if name in ("ul", "ol"):
            ordered = name == "ol"
            for k, li in enumerate(el.find_all("li", recursive=False), 1):
                t = flush("".join(inline(c) for c in li.children))
                if t:
                    lines.append((f"{k}. " if ordered else "- ") + t)
            lines.append("")
            i += 1
            continue
        if name == "pre":
            code_el = el.find("code")
            lines += ["", f"```\n{(code_el or el).get_text().rstrip()}\n```", ""]
            i += 1
            continue
        if name == "img":
            src = el.get("src", "")
            alt = el.get("alt", "")
            lines += ["", f"![{alt}]({IMG_MAP.get(_norm(src), src)})", ""]
            i += 1
            continue
        i += 1
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> int:
    assert SRC.is_file(), SRC
    if OUT.exists():
        shutil.rmtree(OUT)
    for d in ("epub", "fulltext", "assets"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    file_sha = sha256_file(SRC)
    shutil.copy2(SRC, OUT / "epub" / SRC.name)

    zf = zipfile.ZipFile(SRC)
    names = zf.namelist()

    # ---- assets ----
    global IMG_MAP
    IMG_MAP = {}
    for n in names:
        if n.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")):
            data = zf.read(n)
            ext = Path(n).suffix.lstrip(".").lower()
            ext = {"jpeg": "jpg"}.get(ext, ext)
            key = hashlib.sha256(data).hexdigest()[:16]
            (OUT / "assets" / f"{key}.{ext}").write_bytes(data)
            IMG_MAP[_norm(n)] = f"../assets/{key}.{ext}"

    # ---- NCX labels → chapters ----
    import xml.etree.ElementTree as ET

    ncx_root = ET.fromstring(zf.read("EPUB/toc.ncx"))
    NS = "{http://www.daisy.org/z3986/2005/ncx/}"
    entries = []  # (label, src)
    def walk(el):
        for np in el.findall(NS + "navPoint"):
            lab = np.find(f"{NS}navLabel/{NS}text")
            con = np.find(NS + "content")
            entries.append(((lab.text or "").strip() if lab is not None else "",
                            (con.get("src") if con is not None else "").split("#")[0]))
            walk(np)
    walk(ncx_root.find(NS + "navMap"))

    chapters = [(lab, src) for lab, src in entries if re.match(r"^第\d+章\s+\S", lab)]
    parts = {}  # label like 第N部分
    cur = ""
    for lab, _ in entries:
        if re.match(r"^第[一二三四五六七八九十]+部分", lab):
            cur = re.match(r"^(第[一二三四五六七八九十]+部分)", lab).group(1)
        parts[lab] = cur
    excluded_front = [lab for lab, _ in entries if parts.get(lab, "") == "" and not re.match(r"^第\d+章", lab)]

    # ---- OPF metadata ----
    opf = ET.fromstring(zf.read("EPUB/package.opf"))
    DCMIT = "{http://purl.org/dc/elements/1.1/}"
    meta_el = {}
    for tag in ("title", "creator", "identifier", "language"):
        e = opf.find(f".//{DCMIT}{tag}")
        meta_el[tag] = (e.text or "").strip() if e is not None else None

    # ---- fulltext ----
    toc_rows = []
    for idx, (lab, src) in enumerate(chapters, 1):
        xhtml_key = src if src in names else PREFIX + src
        soup = BeautifulSoup(zf.read(xhtml_key).decode("utf-8", "replace"), "lxml")
        md = chapter_to_markdown(soup)
        wc = len(re.sub(r"\s+", "", md))
        num = int(re.match(r"^第(\d+)章", lab).group(1))
        slug = re.sub(r"^第\d+章\s+", "", lab)
        slug = re.sub(r"[/\\:*?\"<>|\s]", "-", slug)[:50]
        uid = f"{idx:02d}"
        fname = f"uid-{uid}-{slug}.md"
        frontmatter = (
            "---\n"
            f"uid: {uid}\nlevel: 1\n"
            f"chapterNumber: §{num}\n"
            f"title: {lab}\n"
            f"wordCount: {wc}\n"
            f"parentPart: {parts.get(lab, '')}\n"
            "---\n\n"
        )
        (OUT / "fulltext" / fname).write_text(frontmatter + md, encoding="utf-8")
        toc_rows.append({"uid": uid, "num": f"§{num}", "title": lab, "wc": wc,
                         "part": parts.get(lab, ""), "file": fname})

    sub_count = sum(len(re.findall(r"^#### ", (OUT / "fulltext" / r["file"]).read_text(), re.M)) for r in toc_rows)
    sec_count = sum(len(re.findall(r"^### ", (OUT / "fulltext" / r["file"]).read_text(), re.M)) for r in toc_rows)

    meta = {
        "title": meta_el["title"],
        "creator": meta_el["creator"],
        "sourcePath": str(SRC),
        "fileSha256": file_sha,
        "fileSize": SRC.stat().st_size,
        "spineItemsCount": len(names),
        "ncxChapterCount": len(chapters),
        "ncxSectionCount": sec_count,
        "ncxSubsectionCount": sub_count,
        "partCount": len({r['part'] for r in toc_rows}),
        "frontMatterExcluded": len(excluded_front),
        "frontMatterList": excluded_front,
        "identifier": meta_el["identifier"],
        "language": meta_el["language"],
    }
    (OUT / "book-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["uid|chapterNumber|title|wordCount|parentPart|file"]
    for r in toc_rows:
        lines.append(f"{r['uid']}|{r['num']}|{r['title']}|{r['wc']}|{r['part']}|{r['file']}")
    (OUT / "toc.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"chapters={len(chapters)} sections={sec_count} subsections={sub_count} assets={len(IMG_MAP)}")
    print(f"excluded({len(excluded_front)}):", excluded_front)
    print("sha256=", file_sha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
