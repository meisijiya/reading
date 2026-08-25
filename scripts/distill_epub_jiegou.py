#!/usr/bin/env python3
"""distill_epub_jiegou.py — 《解构领域驱动设计》epub → 00-原书档案/。

结构特点（区别于已有三本书）：
- EPUB3 with toc.xhtml (no NCX navMap)
- 38 顶层节点 = 封面/版权/提要/序×4/前言/资源/5 篇扉页/第1-20章/附录A-D
- 章节 xhtml 以 <section class="readerChapterContent"> 包裹，标题用 CSS class
  (secondTitle=章 / thirdTitle=N.M / fourthTitle=N.M.K)
- 类名：content / quotation / quotation-right / imgtitle / bold / italic
- 内嵌章节：篇扉页(009/013/017/024/030) 有实质性引导文字 ~700-1000 字，
  附录(034-037) 也有完整章节量（~37k 字），均纳入 fulltext
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
import warnings
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

CHAPTER_RE = re.compile(r"^第\s*(\d+)\s*章\s*(.+)$")
APPENDIX_RE = re.compile(r"^附录\s*([A-Z])\s*(.+)$")
PART_INTRO_RE = re.compile(r"^第([一二三四五六七八九十]+)\s*篇\s*(.+)$")
TITLE_NORMALIZE = re.compile(r"[\u3000\u2003\u2002]+")  # fullwidth spaces

# (uid, xhtml, kind, label, part)  →  顺序为 fulltext 编号顺序
# kind: "chapter" | "appendix" | "partintro"
PLAN: list[tuple[int, str, str, str, str]] = [
    # 第一篇 开篇 — 篇扉页 + 3 章
    (1, "009.xhtml", "partintro", "第一篇　开篇", "第一篇 开篇"),
    (2, "010.xhtml", "chapter", "第1章　软件复杂度剖析", "第一篇 开篇"),
    (3, "011.xhtml", "chapter", "第2章　领域驱动设计概览", "第一篇 开篇"),
    (4, "012.xhtml", "chapter", "第3章　领域驱动设计统一过程", "第一篇 开篇"),
    # 第二篇 全局分析
    (5, "013.xhtml", "partintro", "第二篇　全局分析", "第二篇 全局分析"),
    (6, "014.xhtml", "chapter", "第4章　问题空间探索", "第二篇 全局分析"),
    (7, "015.xhtml", "chapter", "第5章　价值需求分析", "第二篇 全局分析"),
    (8, "016.xhtml", "chapter", "第6章　业务需求分析", "第二篇 全局分析"),
    # 第三篇 架构映射
    (9, "017.xhtml", "partintro", "第三篇　架构映射", "第三篇 架构映射"),
    (10, "018.xhtml", "chapter", "第7章　同构系统", "第三篇 架构映射"),
    (11, "019.xhtml", "chapter", "第8章　系统上下文", "第三篇 架构映射"),
    (12, "020.xhtml", "chapter", "第9章　限界上下文", "第三篇 架构映射"),
    (13, "021.xhtml", "chapter", "第10章　上下文映射", "第三篇 架构映射"),
    (14, "022.xhtml", "chapter", "第11章　服务契约设计", "第三篇 架构映射"),
    (15, "023.xhtml", "chapter", "第12章　领域驱动架构", "第三篇 架构映射"),
    # 第四篇 领域建模
    (16, "024.xhtml", "partintro", "第四篇　领域建模", "第四篇 领域建模"),
    (17, "025.xhtml", "chapter", "第13章　模型驱动设计", "第四篇 领域建模"),
    (18, "026.xhtml", "chapter", "第14章　领域分析建模", "第四篇 领域建模"),
    (19, "027.xhtml", "chapter", "第15章　领域模型设计要素", "第四篇 领域建模"),
    (20, "028.xhtml", "chapter", "第16章　领域设计建模", "第四篇 领域建模"),
    (21, "029.xhtml", "chapter", "第17章　领域实现建模", "第四篇 领域建模"),
    # 第五篇 融合
    (22, "030.xhtml", "partintro", "第五篇　融合", "第五篇 融合"),
    (23, "031.xhtml", "chapter", "第18章　领域驱动设计的战略考量", "第五篇 融合"),
    (24, "032.xhtml", "chapter", "第19章　领域驱动设计的战术考量", "第五篇 融合"),
    (25, "033.xhtml", "chapter", "第20章　领域驱动设计体系", "第五篇 融合"),
    # 附录 A-D
    (26, "034.xhtml", "appendix", "附录A　领域建模范式", "附录"),
    (27, "035.xhtml", "appendix", "附录B　事件驱动模型", "附录"),
    (28, "036.xhtml", "appendix", "附录C　领域驱动设计魔方", "附录"),
    (29, "037.xhtml", "appendix", "附录D　领域驱动设计统一过程交付物", "附录"),
]


def norm_label(label: str) -> str:
    """第1章　软件复杂度剖析 → 第1章 软件复杂度剖析"""
    return TITLE_NORMALIZE.sub(" ", label.strip())


def slugify(label: str) -> str:
    """中文标题 → 文件名 slug：保留汉字，剔除「第N章」「附录X」，空白转 -。"""
    s = norm_label(label)
    s = re.sub(r"^第[一二三四五六七八九十\d]+\s*章\s+", "", s)
    s = re.sub(r"^附录\s*[A-Z]\s+", "", s)
    s = re.sub(r"^第[一二三四五六七八九十]+\s*篇\s+", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[\\/:*?\"<>|]", "", s)
    return s[:50] if s else "section"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- HTML → markdown ----------

def _norm_img(src: str) -> str:
    s = src.strip()
    s = re.sub(r"^(OEBPS/)+", "", s)
    s = re.sub(r"^(\.\./)+", "", s)
    return s.lstrip("/")


def inline(el, img_map: dict[str, str]) -> str:
    """递归把 inline 内容转 markdown 文本。"""
    if isinstance(el, NavigableString):
        return str(el)
    if not isinstance(el, Tag):
        return ""
    name = el.name
    if name in ("strong", "b"):
        inner = "".join(inline(c, img_map) for c in el.children).strip()
        return f"**{inner}**" if inner else ""
    if name in ("em", "i"):
        inner = "".join(inline(c, img_map) for c in el.children).strip()
        return f"*{inner}*" if inner else ""
    if name == "code":
        return f"`{el.get_text()}`"
    if name == "br":
        return "\n"
    if name == "a":
        href = el.get("href", "")
        inner = "".join(inline(c, img_map) for c in el.children).strip()
        return f"[{inner}]({href})" if href else inner
    if name == "span":
        cls = el.get("class") or []
        if "super" in cls:
            return f"^{el.get_text()}"
        if "sub" in cls:
            return f"~{el.get_text()}"
        return "".join(inline(c, img_map) for c in el.children)
    if name == "img":
        src = el.get("src", "")
        alt = el.get("alt", "")
        new_src = img_map.get(_norm_img(src), src)
        return f"![{alt}]({new_src})"
    return "".join(inline(c, img_map) for c in el.children)


def flush(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def xhtml_to_markdown(soup: BeautifulSoup, img_map: dict[str, str]) -> str:
    sec = soup.find("section", class_="readerChapterContent") or soup.find("section") or soup.find("body") or soup
    lines: list[str] = []
    for el in sec.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6",
         "p", "blockquote", "ul", "ol", "pre", "img"],
        recursive=True,
    ):
        # 跳过嵌套重复：只留最外层
        if el.find_parent(["blockquote", "li"]):
            continue
        cls = el.get("class") or []
        if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            txt = flush(el.get_text())
            if not txt:
                continue
            if "secondTitle" in cls or el.name == "h2":
                lines += ["", f"## {norm_label(txt)}", ""]
            elif "thirdTitle" in cls or el.name == "h3":
                lines += ["", f"### {txt}", ""]
            elif "fourthTitle" in cls or el.name == "h4":
                lines += ["", f"#### {txt}", ""]
            elif "firstTitle" in cls or el.name == "h1":
                lines += ["", f"# {txt}", ""]
            else:
                level = int(el.name[1])
                lines += ["", "#" * level + " " + txt, ""]
            continue
        if el.name == "p":
            # 跳过 reader_footer_note
            if "js_readerFooterNote" in cls or "reader_footer_note" in cls:
                continue
            txt = flush(el.get_text())
            if not txt:
                # 空 p 也可能含 img
                continue
            if "secondTitle" in cls:
                lines += ["", f"## {norm_label(txt)}", ""]
            elif "thirdTitle" in cls:
                lines += ["", f"### {txt}", ""]
            elif "fourthTitle" in cls:
                lines += ["", f"#### {txt}", ""]
            elif "firstTitle" in cls:
                lines += ["", f"# {txt}", ""]
            elif "copyRightTitle" in cls or "contentCR" in cls or "contentCR1" in cls or "contentCR2" in cls:
                lines += ["", txt, ""]
            elif "quotation" in cls:
                lines += ["", f"> {txt}", ""]
            elif "quotation-right" in cls:
                lines += ["", f"> {txt}", ""]
            elif "imgtitle" in cls or "imgdescript" in cls:
                lines += ["", f"*{txt}*", ""]
            elif "author" in cls:
                lines += ["", f"*{txt}*", ""]
            elif "content-b" in cls or "bold" in cls:
                lines += ["", f"**{txt}**", ""]
            else:
                # 普通 content / content-right
                content_txt = "".join(inline(c, img_map) for c in el.children).strip()
                content_txt = re.sub(r"\n{3,}", "\n\n", content_txt)
                if content_txt:
                    lines += ["", content_txt, ""]
        elif el.name == "img":
            src = el.get("src", "")
            alt = el.get("alt", "")
            new_src = img_map.get(_norm_img(src), src)
            lines += ["", f"![{alt}]({new_src})", ""]
        elif el.name == "blockquote":
            inner = el.get_text(" ", strip=True)
            if inner:
                lines += ["", f"> {inner}", ""]
        elif el.name in ("ul", "ol"):
            ordered = el.name == "ol"
            for k, li in enumerate(el.find_all("li", recursive=False), 1):
                t = flush("".join(inline(c, img_map) for c in li.children))
                if t:
                    lines.append((f"{k}. " if ordered else "- ") + t)
            lines.append("")
        elif el.name == "pre":
            code_el = el.find("code")
            txt = (code_el or el).get_text().rstrip()
            lines += ["", "```", txt, "```", ""]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def chapter_meta(uid: int, kind: str, label: str, part: str, xhtml: str, wc: int, slug: str) -> dict:
    m_ch = CHAPTER_RE.match(norm_label(label))
    m_ap = APPENDIX_RE.match(norm_label(label))
    m_pi = PART_INTRO_RE.match(norm_label(label))
    if m_ch:
        num = f"§{int(m_ch.group(1))}"
    elif m_ap:
        num = f"附录{m_ap.group(1)}"
    elif m_pi:
        num = f"篇{m_pi.group(1)}"
    else:
        num = "?"
    return {
        "uid": f"{uid:02d}",
        "kind": kind,
        "chapterNumber": num,
        "title": norm_label(label),
        "wordCount": str(wc),
        "parentPart": part,
        "file": f"uid-{uid:02d}-{slug}.md",
        "sourceXhtml": xhtml,
    }


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

    file_sha = sha256_file(src)
    out.mkdir(parents=True, exist_ok=True)
    (out / "epub").mkdir(exist_ok=True)
    (out / "fulltext").mkdir(exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    shutil.copy2(src, out / "epub" / src.name)

    with zipfile.ZipFile(str(src)) as zf:
        names = zf.namelist()

        # ---- assets：图片按 sha256[0:16] 命名 ----
        img_map: dict[str, str] = {}
        for n in names:
            if n.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp")):
                data = zf.read(n)
                ext = os.path.splitext(n)[1].lstrip(".").lower()
                if ext == "jpeg":
                    ext = "jpg"
                h = hashlib.sha256(data).hexdigest()[:16]
                apath = out / "assets" / f"{h}.{ext}"
                if not apath.exists():
                    apath.write_bytes(data)
                # map 两个 key：相对路径 & zip 内绝对路径
                rel = posixpath.relpath(n, "OEBPS") if n.startswith("OEBPS/") else n
                img_map[rel] = f"../assets/{h}.{ext}"
                img_map[n] = f"../assets/{h}.{ext}"

        # ---- OPF 元数据 ----
        opf_root = ET.fromstring(zf.read("OEBPS/package.opf"))
        DC = "{http://purl.org/dc/elements/1.1/}"
        title = (opf_root.findtext(f".//{DC}title") or "").strip()
        creator = (opf_root.findtext(f".//{DC}creator") or "").strip()
        identifier = (opf_root.findtext(f".//{DC}identifier") or "").strip() or None
        language = (opf_root.findtext(f".//{DC}language") or "").strip() or None
        publisher = (opf_root.findtext(f".//{DC}publisher") or "").strip() or None
        date = (opf_root.findtext(f".//{DC}date") or "").strip() or None
        desc = (opf_root.findtext(f".//{DC}description") or "").strip() or None

        # ---- fulltext ----
        toc_rows: list[dict] = []
        for uid, xhtml, kind, label, part in PLAN:
            xpath = f"OEBPS/{xhtml}"
            assert xpath in names, f"missing {xpath}"
            soup = BeautifulSoup(zf.read(xpath), "lxml")
            md = xhtml_to_markdown(soup, img_map)
            wc = len(re.sub(r"\s+", "", md))
            slug = slugify(label)
            frontmatter = (
                "---\n"
                f"uid: {uid:02d}\n"
                f"kind: {kind}\n"
                f"chapterNumber: {chapter_meta(uid, kind, label, part, xhtml, wc, slug)['chapterNumber']}\n"
                f"title: {norm_label(label)}\n"
                f"wordCount: {wc}\n"
                f"parentPart: {part}\n"
                f"sourceXhtml: {xhtml}\n"
                "---\n\n"
            )
            fpath = out / "fulltext" / f"uid-{uid:02d}-{slug}.md"
            fpath.write_text(frontmatter + md, encoding="utf-8")
            meta = chapter_meta(uid, kind, label, part, xhtml, wc, slug)
            toc_rows.append(meta)
            print(f"  uid={meta['uid']} {meta['chapterNumber']} {meta['title']} ({wc}) -> {meta['file']}")

    # ---- book-meta.json ----
    ncx_chapter_count = sum(1 for r in toc_rows if r["kind"] == "chapter")
    ncx_appendix_count = sum(1 for r in toc_rows if r["kind"] == "appendix")
    ncx_part_intro_count = sum(1 for r in toc_rows if r["kind"] == "partintro")
    part_count = sum(1 for r in toc_rows if r["kind"] == "partintro")
    meta: dict = {
        "title": title,
        "creator": creator,
        "sourcePath": str(src),
        "fileSha256": file_sha,
        "fileSize": src.stat().st_size,
        "epubChapterCount": ncx_chapter_count,
        "epubAppendixCount": ncx_appendix_count,
        "epubPartIntroCount": ncx_part_intro_count,
        "partCount": part_count,
        "tocFormat": "epub3-xhtml",
    }
    if identifier:
        meta["identifier"] = identifier
    if language:
        meta["language"] = language
    if publisher:
        meta["publisher"] = publisher
    if date:
        meta["date"] = date
    if desc:
        meta["description"] = desc
    (out / "book-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ---- toc.md ----
    lines = ["uid|kind|chapterNumber|title|wordCount|parentPart|file"]
    for r in toc_rows:
        lines.append(
            f"{r['uid']}|{r['kind']}|{r['chapterNumber']}|{r['title']}|{r['wordCount']}|{r['parentPart']}|{r['file']}"
        )
    (out / "toc.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nPARTS={part_count} CHAPTERS={ncx_chapter_count} APPENDICES={ncx_appendix_count} PART_INTROS={ncx_part_intro_count}")
    print(f"FULLTEXT_COUNT={len(toc_rows)} ASSETS={len(img_map)}")
    print(f"BOOK_META={out/'book-meta.json'}")
    print(f"TOC={out/'toc.md'}")
    print(f"SHA256={file_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())