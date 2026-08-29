#!/usr/bin/env python3
"""
distill_epub_aiprompt.py — 把「AI Prompt Engineering: The 2026 Guide」epub 蒸馏成
00-原书档案/ 目录（按 AGENTS.md 规则四模板）。

源文件: book/AI Prompt Engineering  The 2026 Guide — ... (Team, AI Prompt Engineering) ...epub

书结构特点:
  - 整本正文落在单个 c63.xhtml (240KB), 按 h1 切粒。
  - NCX navMap 是扁平的 (全 d=0); 不靠深度, 靠 h1 顺序匹配。
  - 识别段:
      "How to Use This Book"        (h2, before Chapter 1)
      "Chapter 1:" ... "Chapter 10:" (10 chapters)
      "Your Prompt Engineering Journey" (h1, transition)
      "Appendix A:" ... "Appendix J:"   (10 appendices)
      "About the Authors"           (h1, closing)
    = 23 uids.

用法:
    python3 scripts/distill_epub_aiprompt.py --src <SOURCE_EPUB> --out <TARGET_DIR>/00-原书档案

产出:
    <out>/epub/<basename>.epub
    <out>/book-meta.json
    <out>/toc.md
    <out>/fulltext/uid-NN-<chapterSlug>.md  (× 23)
    <out>/assets/<sha256[0:16]>.<ext>      (× image count)
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
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Book identity (path-lock)
PATH_LOCK_TITLE = "AI Prompt Engineering : The 2026 Guide — 420+ Battle-Tested Prompts, the 4 C's Framework, and How to Scale Your Business with AI"
PATH_LOCK_CREATOR = "Team, AI Prompt Engineering"

# Pattern of a chapter-tier heading.
#   - Chapter 1, Chapter 2, ..., Chapter 10
#   - Appendix A, Appendix B, ..., Appendix J
#   - How to Use This Book
#   - Your Prompt Engineering Journey
#   - About the Authors
H1_CHAPTER_RE = re.compile(
    r"^Chapter\s+(\d+):\s*(.+?)\s*$"
    r"|^Appendix\s+([A-Z]):\s*(.+?)\s*$"
    r"|^(How to Use This Book|Your Prompt Engineering Journey|About the Authors)\s*$",
    re.IGNORECASE,
)

# Body content xhtml filename (the main book).
MAIN_BODY_XHTML = "OEBPS/c63.xhtml"
TITLE_PAGE_XHTML = "OEBPS/c9.xhtml"  # title page + table of contents


# ---------- utilities ----------

def sha256_of_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify_chapter(label: str, max_len: int = 60) -> str:
    """English title → ASCII slug.

    Examples:
      "Chapter 1: What Is Prompt Engineering?" -> "what-is-prompt-engineering"
      "Appendix A: The 320-Prompt Catalog"     -> "the-320-prompt-catalog"
      "How to Use This Book"                   -> "how-to-use-this-book"
      "About the Authors"                      -> "about-the-authors"
    """
    s = label.strip()
    # Strip leading "Chapter N:" / "Appendix X:"
    s = re.sub(r"^(Chapter\s+\d+:|Appendix\s+[A-Z]:)\s*", "", s, flags=re.IGNORECASE)
    # Normalize curly punctuation to ASCII
    s = (
        s.replace("\u2018", "'").replace("\u2019", "'")  # smart single quotes
         .replace("\u201C", '"').replace("\u201D", '"')  # smart double quotes
         .replace("\u2014", "-").replace("\u2013", "-")  # em/en dash
         .replace("\xa0", " ")                           # NBSP
    )
    # Keep alnum + spaces + dash; drop everything else
    s = re.sub(r"[^A-Za-z0-9 \-]", " ", s)
    # Collapse whitespace → single dash, lowercase
    s = re.sub(r"\s+", "-", s.strip()).strip("-").lower()
    s = re.sub(r"-+", "-", s)
    if not s:
        s = "chapter"
    return s[:max_len]


def get_chapter_meta(label: str) -> Tuple[str, str]:
    """从 h1 label 解析 (chapter_kind, num_or_letter)。

    chapter_kind ∈ {"howto", "chapter", "appendix", "journey", "about"}.
    num_or_letter: howto="", chapter="N", appendix="A", journey="", about="".
    """
    m = H1_CHAPTER_RE.match(label)
    if not m:
        raise ValueError(f"label does not match chapter regex: {label!r}")
    chap_n, _chap_t, app_l, _app_t, special = m.groups()
    if chap_n is not None:
        return ("chapter", chap_n)
    if app_l is not None:
        return ("appendix", app_l)
    if special.lower() == "how to use this book":
        return ("howto", "")
    if special.lower() == "your prompt engineering journey":
        return ("journey", "")
    if special.lower() == "about the authors":
        return ("about", "")
    raise ValueError(f"unmatched label kind: {label!r}")


# ---------- HTML → markdown ----------

def html_to_markdown(html_str: str, img_src_map: Dict[str, str]) -> str:
    """Lightweight HTML→markdown with img-src rewrite.

    Converts h1/h2/h3 → markdown headings; paragraphs → paragraphs; ordered/unordered
    lists → md lists; pre/code blocks → fenced blocks; blockquotes → '> '; em/strong
    preserved; inline images rewritten to ../assets/<hash>.<ext>.
    """
    soup = BeautifulSoup(html_str, "lxml")
    out_lines: List[str] = []

    def flush_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def inline(el) -> str:
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
            txt = "".join(inline(c) for c in el.children).strip()
            txt = re.sub(r"[ \t]+\n", "\n", txt)
            txt = re.sub(r"\n{3,}", "\n\n", txt)
            txt = re.sub(r"(?<!\\)\[([A-Za-z][A-Za-z0-9 _-]*)\](?!\()", r"\\[\1\\]", txt)
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
        elif name == "table":
            rows = el.find_all("tr")
            if not rows:
                return
            grid = []
            for tr in rows:
                cells = tr.find_all(["th", "td"])
                grid.append(["".join(inline(c) for c in td.children).strip() for td in cells])
            # Pad all rows to the same width with empties
            width = max(len(r) for r in grid)
            grid = [r + [""] * (width - len(r)) for r in grid]
            has_header = any(tr.find("th") for tr in rows)
            out_lines.append("")
            for ri, row in enumerate(grid):
                out_lines.append("| " + " | ".join(row) + " |")
                if has_header and ri == 0:
                    out_lines.append("| " + " | ".join("---" for _ in row) + " |")
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

    body = soup.find("body") or soup
    for c in body.children:
        if getattr(c, "name", None):
            handle_block(c)

    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _normalize_img_src(src: str) -> str:
    """Normalize epub img src to a key we can match against zip entries."""
    s = src.strip()
    while s.startswith("/"):
        s = s[1:]
    s = re.sub(r"^(\.\./)+", "", s)
    return s


# ---------- h1-based chapter split (single xhtml body) ----------

def split_xhtml_by_h1(
    xhtml_path_in_epub: str,
    zip_handle: zipfile.ZipFile,
) -> List[Tuple[int, str, str]]:
    """返回 [(chapter_idx, label, html_substring), ...], 按 h1 顺序切粒。

    chapter_idx: 0-based。第一个 chapter 包含 body 开头到第一个 h1 (即 h2 "How to Use
    This Book" 的全部内容)。
    """
    raw = zip_handle.read(xhtml_path_in_epub).decode("utf-8", errors="replace")
    soup = BeautifulSoup(raw, "lxml")
    body = soup.find("body") or soup

    children = [c for c in body.children if getattr(c, "name", None)]

    # 找所有 h1 元素的索引
    h1_indices: List[int] = []
    for i, el in enumerate(children):
        if el.name == "h1":
            label = el.get_text().strip()
            if H1_CHAPTER_RE.match(label):
                h1_indices.append(i)

    if not h1_indices:
        return []

    slices: List[Tuple[int, str, str]] = []
    for bi, start in enumerate(h1_indices):
        end = h1_indices[bi + 1] if bi + 1 < len(h1_indices) else len(children)
        head_label = children[start].get_text().strip()
        # bi=0: from body start (includes "How to Use" h2); bi>=1: from current h1 (incl.).
        # off-by-one risk: must NOT use h1_indices[bi-1]+1, which leaks body of prev chapter.
        prior_start = h1_indices[bi] if bi > 0 else 0
        chapter_html_parts = [str(children[k]) for k in range(prior_start, end)]
        chapter_html = "<div>" + "\n".join(chapter_html_parts) + "</div>"
        slices.append((bi, head_label, chapter_html))
    return slices


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

    # (1) sha256 + size + cp
    file_sha = sha256_of_file(src)
    file_size = src.stat().st_size
    epub_copy = out / "epub" / src.name
    shutil.copy2(src, epub_copy)

    print(f"SOURCE_PATH={src}")
    print(f"FILE_SHA256={file_sha}")
    print(f"FILE_SIZE={file_size}")
    print(f"COPIED_TO={epub_copy}")

    # (2) ebooklib metadata
    from ebooklib import epub as epub_lib

    book = epub_lib.read_epub(str(src))

    def first_meta(qname: str) -> Optional[str]:
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
    date = first_meta("date") or first_meta("pubdate")

    if title != PATH_LOCK_TITLE:
        print(f"ERROR: title mismatch: got {title!r} expected {PATH_LOCK_TITLE!r}", file=sys.stderr)
        return 3
    if creator != PATH_LOCK_CREATOR:
        print(f"ERROR: creator mismatch: got {creator!r} expected {PATH_LOCK_CREATOR!r}", file=sys.stderr)
        return 3

    print(f"TITLE={title}")
    print(f"CREATOR={creator}")

    # (3) extract images
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
                norm = _normalize_img_src(name)
                img_src_map[norm] = f"../assets/{h}.{ext}"

    # (4) split body
    with zipfile.ZipFile(str(src)) as zf:
        if MAIN_BODY_XHTML not in zf.namelist():
            print(f"ERROR: main body xhtml missing: {MAIN_BODY_XHTML}", file=sys.stderr)
            return 4
        slices = split_xhtml_by_h1(MAIN_BODY_XHTML, zf)

    chapter_kind_counts: Dict[str, int] = {}
    for _idx, label, _html in slices:
        kind, _num = get_chapter_meta(label)
        chapter_kind_counts[kind] = chapter_kind_counts.get(kind, 0) + 1

    print(f"CHAPTER_COUNT={len(slices)}")
    for k, v in chapter_kind_counts.items():
        print(f"KIND_{k.upper()}={v}")

    # (5) write fulltext
    chapter_files: List[Path] = []
    toc_rows: List[Dict] = []
    uid_counter = 1

    # Group by "module" (downstream NN-部/), keeps friendly ordering.
    def module_name_for(idx: int, kind: str) -> str:
        # 5 modules:
        #   00-原书档案 is meta (no NN- dir)
        #   01 基础与导读 = howto + chapters 1-3   (4 uids)
        #   02 场景 Prompt 模板库 = chapters 4-8   (5 uids)
        #   03 进阶与商业应用 = chapters 9-10 + journey  (3 uids)
        #   04 参考附录 A-E    = appendices A-E   (5 uids)
        #   05 实战卷 F-J + Authors = appendices F-J + about  (6 uids)
        if kind == "howto" or kind == "chapter" and (idx <= 3):
            return "01-基础与导读"
        if kind == "chapter" and idx <= 8:  # chapters 4-8 → idx 4..8 in 0-based (chapters 4=index 3)
            # idx in chapter count is sequential; we need to track numbering separately.
            # easier: just use chapter number via Kind
            pass
        # Refactor: derive from chapter index in section-of-the-book.
        return ""

    # Simpler: assign module based on the kind+position
    seq_chapter = 0
    seq_appendix = 0
    for idx, (slice_idx, label, html) in enumerate(slices):
        kind, num_or_letter = get_chapter_meta(label)
        seq_chapter += 1 if kind == "chapter" else 0
        seq_appendix += 1 if kind == "appendix" else 0

        if kind == "howto":
            parent_part = "00-全卷-导读"
            chapter_title = label
            chapter_number_str = "00"
        elif kind == "chapter":
            parent_part = _module_for_chapter(int(num_or_letter))
            chapter_title = label  # keep original (e.g., "Chapter 1: What Is Prompt Engineering?")
            chapter_number_str = num_or_letter  # e.g., "1", "2"
        elif kind == "journey":
            parent_part = "03-进阶与商业应用"
            chapter_title = label
            chapter_number_str = "00"
        elif kind == "appendix":
            parent_part = _module_for_appendix(num_or_letter)
            chapter_title = label
            chapter_number_str = num_or_letter
        elif kind == "about":
            parent_part = "05-实战卷-F-J-与作者"
            chapter_title = label
            chapter_number_str = "00"
        else:
            raise ValueError(f"unknown kind: {kind}")

        uid_str = f"{uid_counter:02d}"
        slug = slugify_chapter(label)
        fname = f"uid-{uid_str}-{slug}.md"
        fpath = out / "fulltext" / fname

        md = html_to_markdown(html, img_src_map)
        wc = len(re.sub(r"\s+", "", md))

        # frontmatter
        fm = (
            "---\n"
            f"uid: {uid_str}\n"
            "level: 1\n"
            f"chapterNumber: {chapter_number_str}\n"
            f"chapterKind: {kind}\n"
            f"title: {chapter_title}\n"
            f"wordCount: {wc}\n"
            f"parentPart: {parent_part}\n"
            "---\n\n"
        )
        fpath.write_text(fm + md, encoding="utf-8")
        chapter_files.append(fpath)

        toc_rows.append({
            "uid": uid_str,
            "level": "1",
            "chapterNumber": f"§{chapter_number_str}",
            "chapterKind": kind,
            "title": chapter_title,
            "wordCount": str(wc),
            "parentPart": parent_part,
        })
        uid_counter += 1

    # (6) book-meta.json
    meta: Dict[str, object] = {
        "title": title,
        "creator": creator,
        "sourcePath": str(src),
        "fileSha256": file_sha,
        "fileSize": file_size,
        "mainBodyXhtml": MAIN_BODY_XHTML,
        "spineItemsCount": len(book.spine),
        "chapterCount": len(slices),
        "chapterKindCounts": chapter_kind_counts,
    }
    if identifier is not None:
        meta["identifier"] = identifier
    if language is not None:
        meta["language"] = language
    if generator is not None:
        meta["generator"] = generator
    if date is not None:
        meta["date"] = date

    (out / "book-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # (7) toc.md
    toc_lines = ["uid|level|chapterNumber|chapterKind|title|wordCount|parentPart"]
    for r in toc_rows:
        toc_lines.append(
            f"{r['uid']}|{r['level']}|{r['chapterNumber']}|{r['chapterKind']}|{r['title']}|{r['wordCount']}|{r['parentPart']}"
        )
    (out / "toc.md").write_text("\n".join(toc_lines) + "\n", encoding="utf-8")

    print(f"FULLTEXT_COUNT={len(chapter_files)}")
    print(f"ASSETS_COUNT={len(img_src_map)}")
    print(f"BOOK_META={out / 'book-meta.json'}")
    print(f"TOC={out / 'toc.md'}")
    return 0


def _module_for_chapter(n: int) -> str:
    """Map chapter number → module directory name."""
    if n <= 3:
        return "01-基础与导读"
    if n <= 8:
        return "02-场景-Prompt-模板库"
    if n <= 10:
        return "03-进阶与商业应用"
    raise ValueError(f"chapter number out of range: {n}")


def _module_for_appendix(letter: str) -> str:
    """Map appendix letter A-Z → module directory name."""
    if letter in ("A", "B", "C", "D", "E"):
        return "04-参考附录-A-E"
    if letter in ("F", "G", "H", "I", "J"):
        return "05-实战卷-F-J-与作者"
    raise ValueError(f"appendix letter out of range: {letter}")


if __name__ == "__main__":
    sys.exit(main())
