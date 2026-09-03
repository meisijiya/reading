#!/usr/bin/env python3
"""
distill_epub.py — 把一个本地 epub 蒸馏成"00-原书档案/"目录（按 AGENTS.md 规则一/四模板）。

用法:
    python3 scripts/distill_epub.py --src <SOURCE_EPUB> --out <TARGET_DIR>/00-原书档案

产出:
    <out>/epub/<basename>.epub
    <out>/book-meta.json
    <out>/toc.md
    <out>/fulltext/uid-NN-<chapterSlug>.md (× N 章)
    <out>/assets/<sha256[0:16]>.<ext> (× image count)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import warnings
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

NCX_NS = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}
NCX_URI = "http://www.daisy.org/z3986/2005/ncx/"
# 用 Clark notation 查元素，兼容 epub 中「默认命名空间」无前缀的情况
NCX_QN = {
    "navPoint": f"{{{NCX_URI}}}navPoint",
    "navLabel": f"{{{NCX_URI}}}navLabel",
    "navLabel_text": f"{{{NCX_URI}}}text",
    "navMap": f"{{{NCX_URI}}}navMap",
    "content": f"{{{NCX_URI}}}content",
}
PART_RE = re.compile(r"^第[一二三四五六七八九十百千]+部分\b|^Part\s+\d+\b")
CHAPTER_RE = re.compile(r"^第\d+章\s+\S")
SUBSECTION_RE = re.compile(r"^\d+\.\d+")
PATH_LOCK_TITLE = "Claude Code橙皮书：AI编程实战"
PATH_LOCK_CREATOR = "花叔"


# ---------- utilities ----------

def sha256_of_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify_chapter(label: str) -> str:
    """从「第1章 为什么选择Claude Code」生成「1-为什么选择Claude-Code」。

    中文保留，空白转 `-`，剔除「第N章」前缀。
    """
    s = re.sub(r"^第\d+章\s+", "", label.strip())
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[/\\:*?\"<>|]", "", s)
    return s[:60] if s else "chapter"


def parse_part_label(label: str) -> Optional[str]:
    """把「第N部分 xxx」还原成 partName；不匹配返回 None。"""
    m = re.match(r"^(第[一二三四五六七八九十百千\d]+部分)\b\s*(.*)$", label.strip())
    if m:
        return m.group(1).strip()
    m = re.match(r"^(Part\s+\d+)\b\s*(.*)$", label.strip())
    if m:
        return m.group(1).strip()
    return None


# ---------- NCX walking ----------

def ncx_walk(nav: ET.Element):
    """DFS yield (depth, label, src, element)."""
    def _walk(el: ET.Element, depth: int):
        for np in el.findall(NCX_QN["navPoint"]):
            label_el = np.find(f"{NCX_QN['navLabel']}/{NCX_QN['navLabel_text']}")
            label = (label_el.text or "").strip() if label_el is not None else ""
            content = np.find(NCX_QN["content"])
            src = content.get("src", "") if content is not None else ""
            src = src.split("#", 1)[0]  # 去 fragment
            yield depth, label, src, np
            yield from _walk(np, depth + 1)
    yield from _walk(nav, 0)


# ---------- HTML → markdown ----------

def html_to_markdown(html_str: str, img_src_map: Dict[str, str]) -> str:
    """Lightweight HTML→markdown with img-src rewrite.

    This epub wraps every character in <strong>, so chapter/subchapter headings like
    「第1章 ...」「1.1 ...」 are detected by collapsed text and emitted as markdown headings,
    not as `**第****1****章**`. Body strong/em emphasis is preserved.
    """
    soup = BeautifulSoup(html_str, "lxml")
    out_lines: List[str] = []

    def flush_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def inline(el) -> str:
        """递归把 inline 内容转 markdown 文本。"""
        if el.name is None:
            return el.string or ""
        if el.name in ("strong", "b"):
            inner = "".join(inline(c) for c in el.children).strip()
            return f"**{inner}**" if inner else ""
        if el.name in ("em", "i"):
            inner = "".join(inline(c) for c in el.children).strip()
            return f"*{inner}*" if inner else ""
        if el.name == "code":
            return f"`{el.get_text()}`"
        if el.name == "a":
            href = el.get("href", "")
            inner = "".join(inline(c) for c in el.children).strip()
            return f"[{inner}]({href})" if href else inner
        if el.name == "br":
            return "\n"
        if el.name == "img":
            src = el.get("src", "")
            alt = el.get("alt", "")
            new_src = img_src_map.get(_normalize_img_src(src), src)
            return f"![{alt}]({new_src})"
        return "".join(inline(c) for c in el.children)

    def plain(el) -> str:
        """Recursive plain text: strips strong/em/span wrappers, used for heading detection."""
        if el.name is None:
            return el.string or ""
        if el.name == "br":
            return "\n"
        return "".join(plain(c) for c in el.children)

    def handle_block(el):
        name = el.name
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            txt = flush_text(el.get_text())
            if txt:
                out_lines.append("")
                out_lines.append("#" * level + " " + txt)
                out_lines.append("")
        elif name == "p":
            raw_text = flush_text(plain(el))
            m_chap = re.match(r"^第(\d+)章\s+(.+)$", raw_text)
            m_sub = SUBSECTION_RE.match(raw_text)
            if m_chap:
                out_lines.append("")
                out_lines.append(f"## 第{m_chap.group(1)}章 {m_chap.group(2).strip()}")
                out_lines.append("")
            elif m_sub and len(raw_text) <= 60 and "\n" not in raw_text:
                out_lines.append("")
                out_lines.append(f"### {raw_text}")
                out_lines.append("")
            else:
                txt = "".join(inline(c) for c in el.children).strip()
                txt = re.sub(r"[ \t]+\n", "\n", txt)
                txt = re.sub(r"\n{3,}", "\n\n", txt)
                if txt:
                    out_lines.append("")
                    out_lines.append(txt)
                    out_lines.append("")
        elif name == "blockquote":
            out_lines.append("")
            for c in el.find_all(["p", "h1", "h2", "h3", "h4"], recursive=False):
                t = flush_text(c.get_text())
                if t:
                    out_lines.append("> " + t)
            out_lines.append("")
        elif name in ("ul", "ol"):
            ordered = name == "ol"
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                txt = "".join(inline(c) for c in li.children).strip()
                txt = flush_text(txt)
                prefix = f"{i}. " if ordered else "- "
                if txt:
                    out_lines.append(prefix + txt)
            out_lines.append("")
        elif name == "pre":
            code_el = el.find("code")
            code_text = code_el.get_text() if code_el else el.get_text()
            lang = ""
            if code_el and code_el.get("class"):
                for c in code_el.get("class"):
                    if c.startswith("language-"):
                        lang = c[len("language-"):]
                        break
            out_lines.append("")
            out_lines.append(f"```{lang}")
            out_lines.append(code_text.rstrip())
            out_lines.append("```")
            out_lines.append("")
        elif name == "img":
            src = el.get("src", "")
            alt = el.get("alt", "")
            new_src = img_src_map.get(_normalize_img_src(src), src)
            out_lines.append("")
            out_lines.append(f"![{alt}]({new_src})")
            out_lines.append("")
        elif name in ("div", "section", "article"):
            for c in el.children:
                if getattr(c, "name", None):
                    handle_block(c)
        # skip empty / unknown

    body = soup.find("body") or soup
    for c in body.children:
        if getattr(c, "name", None):
            handle_block(c)

    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _normalize_img_src(src: str) -> str:
    """epub 内的 img src 多为 'images/foo.jpg' (相对 xhtml) 或 '../images/foo.jpg' (相对更深层级)。

    规范化：去掉所有 ../、/、以及 zip 内的 EPUB/ 前缀；产出裸 'images/foo.jpg' 形式，与 zip 条目（去 EPUB/）做 key 对齐。
    """
    s = src.strip()
    s = re.sub(r"^(EPUB/)+", "", s)
    s = re.sub(r"^(\.\./)+", "", s)
    while s.startswith("/"):
        s = s[1:]
    return s


# ---------- part-xhtml → chapter split ----------

def split_xhtml_into_chapters(
    xhtml_path_in_epub: str,
    zip_handle: zipfile.ZipFile,
) -> List[Tuple[int, str, str]]:
    """返回 [(chapter_num, chapter_label, html_substring), ...]。

    按「<p>第N章 xxx</p>」切粒；其余 (Part h3 标题、Part intro 段) 被丢弃。
    """
    raw = zip_handle.read(xhtml_path_in_epub).decode("utf-8", errors="replace")
    soup = BeautifulSoup(raw, "lxml")
    body = soup.find("body") or soup

    children = [c for c in body.children if getattr(c, "name", None)]
    boundaries: List[int] = []
    for i, el in enumerate(children):
        text = "".join(el.strings).strip()
        if CHAPTER_RE.match(text):
            boundaries.append(i)

    if not boundaries:
        return []

    # 把每章切成独立 HTML 片段 (单独 soup 再序列化, 避免跨切片)
    results: List[Tuple[int, str, str]] = []
    for bi, start in enumerate(boundaries):
        end = boundaries[bi + 1] if bi + 1 < len(boundaries) else len(children)
        chapter_html_parts = [str(children[k]) for k in range(start, end)]
        chapter_html = "<div>" + "\n".join(chapter_html_parts) + "</div>"
        # 解析 chapter label
        head_text = "".join(children[start].strings).strip()
        m = re.match(r"^第(\d+)章\s+(.+)$", head_text)
        if m:
            num = int(m.group(1))
            label = f"第{num}章 {m.group(2)}"
        else:
            num = -1
            label = head_text
        results.append((num, label, chapter_html))
    return results


# ---------- main ----------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="source .epub")
    ap.add_argument("--out", required=True, help="target dir (will be created)")
    ap.add_argument("--force", action="store_true", help="clean out dir first")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()

    if not src.is_file():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        return 2

    if out.exists():
        if args.force:
            shutil.rmtree(out)
        else:
            print(f"ERROR: out dir exists (use --force to wipe): {out}", file=sys.stderr)
            return 2

    out.mkdir(parents=True, exist_ok=True)
    (out / "epub").mkdir(exist_ok=True)
    (out / "fulltext").mkdir(exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)

    # ---------- (1) sha256 + size + cp ----------
    file_sha = sha256_of_file(src)
    file_size = src.stat().st_size
    epub_copy = out / "epub" / src.name
    shutil.copy2(src, epub_copy)

    print(f"SOURCE_PATH={src}")
    print(f"FILE_SHA256={file_sha}")
    print(f"FILE_SIZE={file_size}")
    print(f"COPIED_TO={epub_copy}")

    # ---------- (2) ebooklib + OPF metadata ----------
    from ebooklib import epub as epub_lib

    book = epub_lib.read_epub(str(src))

    def first_meta(qname: str) -> Optional[str]:
        # ebooklib exposes get_metadata('DC', 'title') etc. and 'OPF' namespace
        for ns in ("DC", "OPF"):
            rows = book.get_metadata(ns, qname)
            if rows:
                return rows[0][0]
        return None

    title = first_meta("title") or ""
    creator = first_meta("creator") or ""
    identifier = first_meta("identifier")
    language = first_meta("language")
    generator = first_meta("generator")

    # Path lock: this script was authored for the orange book; allow override via env if reused later.
    if title != PATH_LOCK_TITLE:
        print(f"ERROR: title mismatch: got {title!r} expected {PATH_LOCK_TITLE!r}", file=sys.stderr)
        return 3
    if creator != PATH_LOCK_CREATOR:
        print(f"ERROR: creator mismatch: got {creator!r} expected {PATH_LOCK_CREATOR!r}", file=sys.stderr)
        return 3

    print(f"TITLE={title}")
    print(f"CREATOR={creator}")

    # ---------- (3)(4) NCX walk ----------
    ncx_path: Optional[str] = None
    for it in book.items:
        if (it.media_type or "").endswith("x-dtbncx+xml") or (it.file_name or "").endswith("toc.ncx"):
            ncx_path = it.file_name
            break

    # Fallback: scan the zip for toc.ncx
    if not ncx_path:
        with zipfile.ZipFile(str(src)) as zf:
            candidates = [n for n in zf.namelist() if n.endswith("toc.ncx")]
        if not candidates:
            print("ERROR: no toc.ncx found", file=sys.stderr)
            return 4
        ncx_path = candidates[0]

    # ebooklib's file_name 是 OPF-relative；epub 实际放在 EPUB/ 子目录里
    with zipfile.ZipFile(str(src)) as zf:
        if ncx_path not in zf.namelist():
            for prefix in ("EPUB/", ""):
                cand = prefix + ncx_path
                if cand in zf.namelist():
                    ncx_path = cand
                    break
            else:
                print(f"ERROR: NCX not found in zip: {ncx_path}", file=sys.stderr)
                return 4
        ncx_xml = zf.read(ncx_path)

    ncx_root = ET.fromstring(ncx_xml)
    nav_map = ncx_root.find(NCX_QN["navMap"])
    if nav_map is None:
        print("ERROR: navMap missing in NCX", file=sys.stderr)
        return 4

    # Collect all navPoints with depth
    nav_points: List[Tuple[int, str, str]] = []
    for depth, label, src_attr, _el in ncx_walk(nav_map):
        nav_points.append((depth, label, src_attr))

    # Identify Part (level 0 matching PART_RE) and Chapter (level 1 matching CHAPTER_RE)
    part_count = 0
    chapter_count = 0
    subchapter_count = 0

    current_part_label: str = ""
    part_to_chapters: Dict[str, List[Tuple[int, str, int]]] = {}  # partLabel -> [(depth, label, idx_in_nav)]
    chapter_nav_indices: List[int] = []  # indices into nav_points that are chapters
    part_nav_indices: List[int] = []

    for idx, (depth, label, _src) in enumerate(nav_points):
        if depth == 0 and PART_RE.match(label):
            part_count += 1
            current_part_label = parse_part_label(label) or label
            part_to_chapters.setdefault(current_part_label, [])
            part_nav_indices.append(idx)
        elif depth == 1 and CHAPTER_RE.match(label):
            chapter_count += 1
            part_to_chapters.setdefault(current_part_label, []).append((depth, label, idx))
            chapter_nav_indices.append(idx)
        else:
            subchapter_count += 1

    # Fallback per spec: 若 level 1 节点数 < 3, 用所有 navPoint level 1-2 节点作 chapters
    fallback_used = False
    if chapter_count < 3:
        fallback_used = True
        print("PART GROUPING FALLBACK: chapter_count < 3, using level 1-2 as chapters")
        part_to_chapters = {"00-全编": []}
        current_part_label = "00-全编"
        for idx, (depth, label, _src) in enumerate(nav_points):
            if depth in (1, 2) and CHAPTER_RE.match(label):
                if label not in [c[1] for c in part_to_chapters["00-全编"]]:
                    part_to_chapters["00-全编"].append((depth, label, idx))
                    chapter_nav_indices.append(idx)
        chapter_count = len(part_to_chapters["00-全编"])

    print(f"NCX_PART_COUNT={part_count}")
    print(f"NCX_CHAPTER_COUNT={chapter_count}")
    print(f"NCX_SUBCHAPTER_COUNT={subchapter_count}")
    print(f"FALLBACK_USED={fallback_used}")

    # ---------- (5)(6)(7) extract media, fulltext, rewrite img ----------
    # Build image src → new asset path mapping
    img_src_map: Dict[str, str] = {}
    with zipfile.ZipFile(str(src)) as zf:
        for name in zf.namelist():
            low = name.lower()
            if low.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp")):
                data = zf.read(name)
                ext = os.path.splitext(name)[1].lstrip(".").lower()
                if ext == "jpeg":
                    ext = "jpg"
                h = sha256_of_bytes(data)[:16]
                asset_path = out / "assets" / f"{h}.{ext}"
                if not asset_path.exists():
                    asset_path.write_bytes(data)
                # map: images/foo.jpg or ../images/foo.jpg → ../assets/<h>.<ext>
                norm = _normalize_img_src(name)
                img_src_map[norm] = f"../assets/{h}.{ext}"

    # Build fulltext files, organized by Part
    spine_items_count = len(book.spine)
    toc_rows: List[Dict] = []  # for toc.md

    # Path of fulltext is <out>/fulltext/uid-NN-*.md
    # Asset rewrite: relative from fulltext to assets = ../assets/<hash>.<ext>

    chapter_files: List[Path] = []
    uid_counter = 1

    # Group chapters by part
    with zipfile.ZipFile(str(src)) as zf:
        for part_label, items in part_to_chapters.items():
            if not items:
                continue
            # group items by source xhtml file (from NCX src)
            by_xhtml: Dict[str, List[Tuple[int, str]]] = {}
            for _depth, label, idx in items:
                src_attr = nav_points[idx][2]
                xhtml_key = src_attr  # typically chapter_5.xhtml etc.
                by_xhtml.setdefault(xhtml_key, []).append((idx, label))
            for xhtml_key, ch_list in by_xhtml.items():
                if xhtml_key not in zf.namelist():
                    # try EPUB/ prefix
                    if "EPUB/" + xhtml_key in zf.namelist():
                        xhtml_key = "EPUB/" + xhtml_key
                    else:
                        print(f"WARN: xhtml missing: {xhtml_key}", file=sys.stderr)
                        continue
                # Get chapter slices
                slices = split_xhtml_into_chapters(xhtml_key, zf)
                # Build label->slice map
                by_label = {lbl: (num, html) for num, lbl, html in slices}
                for _idx, label in ch_list:
                    if label not in by_label:
                        # match by chapter number extracted from label
                        m = re.match(r"^第(\d+)章", label)
                        if not m:
                            print(f"WARN: chapter not found in xhtml: {label}", file=sys.stderr)
                            continue
                        target_num = int(m.group(1))
                        match = next(((n, l, h) for n, l, h in slices if n == target_num), None)
                        if not match:
                            print(f"WARN: chapter#{target_num} not split from {xhtml_key}", file=sys.stderr)
                            continue
                        num, _l, html = match
                    else:
                        num, html = by_label[label]

                    slug = slugify_chapter(label)
                    uid_str = f"{uid_counter:02d}"
                    fname = f"uid-{uid_str}-{slug}.md"
                    fpath = out / "fulltext" / fname

                    md = html_to_markdown(html, img_src_map)
                    wc = len(re.sub(r"\s+", "", md))

                    frontmatter = (
                        "---\n"
                        f"uid: {uid_str}\n"
                        "level: 1\n"
                        f"chapterNumber: §{num}\n"
                        f"title: {label}\n"
                        f"wordCount: {wc}\n"
                        f"parentPart: {part_label or ''}\n"
                        "---\n\n"
                    )
                    fpath.write_text(frontmatter + md, encoding="utf-8")
                    chapter_files.append(fpath)

                    toc_rows.append({
                        "uid": uid_str,
                        "level": "1",
                        "chapterNumber": f"§{num}",
                        "title": label,
                        "wordCount": str(wc),
                        "parentPart": part_label or "",
                    })
                    uid_counter += 1

    # ---------- (8) book-meta.json ----------
    meta: Dict[str, object] = {
        "title": title,
        "creator": creator,
        "sourcePath": str(src),
        "fileSha256": file_sha,
        "fileSize": file_size,
        "spineItemsCount": spine_items_count,
        "ncxChapterCount": chapter_count,
        "ncxSubchapterCount": subchapter_count,
        "partCount": part_count,
    }
    if identifier is not None:
        meta["identifier"] = identifier
    if language is not None:
        meta["language"] = language
    if generator is not None:
        meta["generator"] = generator

    (out / "book-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ---------- (9) toc.md ----------
    toc_lines = ["uid|level|chapterNumber|title|wordCount|parentPart"]
    for r in toc_rows:
        toc_lines.append(
            f"{r['uid']}|{r['level']}|{r['chapterNumber']}|{r['title']}|{r['wordCount']}|{r['parentPart']}"
        )
    (out / "toc.md").write_text("\n".join(toc_lines) + "\n", encoding="utf-8")

    # ---------- summary ----------
    print(f"extracted {chapter_count} chapters across {part_count} parts")
    print(f"FULLTEXT_COUNT={len(chapter_files)}")
    print(f"ASSETS_COUNT={len(img_src_map)}")
    print(f"BOOK_META={out / 'book-meta.json'}")
    print(f"TOC={out / 'toc.md'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
