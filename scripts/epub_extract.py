"""Extract an O'Reilly epub into NCX-level-1 fulltext + toc.md + book-meta.json.

Per AGENTS.md 规则四 (epub-distill):
- fulltext granularity = one NCX level-1 node per file
- uid numbering stable (01..NN) for chapter anchor
- title prefix preserves Part / chapter number

Usage:
  python3 scripts/epub_extract.py <epub_path> <book_root_dir>

Example:
  python3 scripts/epub_extract.py \
    "book/AI Engineering (Chip Huyen) (z-library.sk, 1lib.sk, z-lib.sk).epub" \
    "AI Engineering (Chip Huyen)"
"""
import sys, json, hashlib, os, re
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

PREAMBLE = (
    "<!-- EPUB-EXTRACTED -- DO NOT EDIT BY HAND -- regenerated from {src} -->\n"
    "<!-- sha256: {sha} -->\n"
    "<!-- uid: {uid} | part: {part} | chapter: {ch} | title: {title} -->\n\n"
)


def slug(s: str) -> str:
    s = re.sub(r"[^0-9A-Za-z一-鿿]+", "-", s).strip("-")
    return s[:80] or "x"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_l1(book):
    """Return ordered list of NCX level-1 items (Section or Link, plus toc-level Links)."""
    items = []
    for node in book.toc:
        if isinstance(node, tuple):
            sec, _kids = node
            items.append(("section", sec))
        elif isinstance(node, epub.Link):
            items.append(("link", node))
    return items


def href_to_filename(href: str) -> str:
    return href.split("#", 1)[0]


def html_for_href(book, href: str) -> str:
    fname = href_to_filename(href)
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        if item.get_name() == fname or item.file_name.endswith(fname):
            return item.get_content().decode("utf-8", errors="replace")
    return ""


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "nav", "header", "footer"]):
        tag.decompose()

    for h1 in soup.find_all("h1"):
        h1.decompose()

    # Convert headings: h1-h6
    out = []
    body = soup.body or soup
    for el in body.descendants:
        pass

    # Walk top-level elements in body
    main = soup.find("main") or soup.find("article") or soup.body or soup
    if main is None:
        return ""

    def render_inline(node):
        if not hasattr(node, "name") or node.name is None:
            return str(node)
        if node.name in ("strong", "b"):
            return f"**{render_inline_children(node)}**"
        if node.name in ("em", "i"):
            return f"*{render_inline_children(node)}*"
        if node.name == "code":
            return f"`{render_inline_children(node)}`"
        if node.name == "a":
            txt = render_inline_children(node)
            href = node.get("href", "")
            return f"[{txt}]({href})" if href else txt
        if node.name == "br":
            return "\n"
        return render_inline_children(node)

    def render_inline_children(node):
        out = []
        for c in node.children:
            out.append(render_inline(c))
        return "".join(out)

    def render_block(node, depth=0):
        if not hasattr(node, "name") or node.name is None:
            text = str(node).strip()
            if text:
                out.append(text)
            return
        name = node.name
        if name in ("script", "style"):
            return
        if re.match(r"h[1-6]$", name):
            level = int(name[1])
            txt = render_inline(node).strip()
            if txt:
                out.append("\n" + "#" * level + " " + txt + "\n")
            return
        if name == "p":
            txt = render_inline(node).strip()
            if txt:
                out.append("\n" + txt + "\n")
            return
        if name == "pre":
            code = node.find("code")
            lang = ""
            if code and code.get("class"):
                for c in code["class"]:
                    if c.startswith("language-"):
                        lang = c.split("-", 1)[1]
                        break
            inner = code.get_text() if code else node.get_text()
            out.append("\n```" + lang + "\n" + inner.rstrip() + "\n```\n")
            return
        if name == "ul":
            for li in node.find_all("li", recursive=False):
                out.append("- " + render_inline(li).strip())
            out.append("")
            return
        if name == "ol":
            for i, li in enumerate(node.find_all("li", recursive=False), 1):
                out.append(f"{i}. " + render_inline(li).strip())
            out.append("")
            return
        if name == "blockquote":
            inner = "\n".join(render_inline(c).strip() for c in node.children if hasattr(c, "name"))
            out.append("\n> " + inner.replace("\n", "\n> ") + "\n")
            return
        if name == "table":
            rows = node.find_all("tr")
            if rows:
                cells = rows[0].find_all(["th", "td"])
                if cells:
                    out.append("| " + " | ".join(render_inline(c).strip() for c in cells) + " |")
                    out.append("|" + "|".join("---" for _ in cells) + "|")
                for r in rows[1:]:
                    cells = r.find_all(["th", "td"])
                    out.append("| " + " | ".join(render_inline(c).strip() for c in cells) + " |")
                out.append("")
            return
        if name == "img":
            src = node.get("src", "")
            alt = node.get("alt", "")
            if src:
                out.append(f"![{alt}]({src})")
            return
        if name in ("div", "section", "article", "main", "body", "html", "span"):
            for c in node.children:
                render_block(c, depth + 1)
            return
        # fallback
        for c in node.children:
            render_block(c, depth + 1)

    for c in main.children:
        render_block(c)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, root = sys.argv[1], sys.argv[2]
    root_path = Path(root).resolve()
    fulltext_dir = root_path / "00-原书档案" / "fulltext"
    fulltext_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = root_path / "00-原书档案" / "epub"
    archive_dir.mkdir(parents=True, exist_ok=True)

    src_path = Path(src).resolve()
    sha = sha256_file(src_path)
    size = src_path.stat().st_size

    book = epub.read_epub(str(src_path))

    # Metadata
    md = {"http://purl.org/dc/elements/1.1/": {}}
    for ns, items in book.metadata.items():
        for it in items:
            if isinstance(it, dict):
                for k, v in it.items():
                    k_short = k.split("}")[-1]
                    md.setdefault(ns, {})
                    md[ns][k_short] = v

    title = md.get("http://purl.org/dc/elements/1.1/", {}).get("title", src_path.stem)
    creator = md.get("http://purl.org/dc/elements/1.1/", {}).get("creator", "")
    language = md.get("http://purl.org/dc/elements/1.1/", {}).get("language", "")
    publisher = md.get("http://purl.org/dc/elements/1.1/", {}).get("publisher", "")
    date = md.get("http://purl.org/dc/elements/1.1/", {}).get("date", "")
    description = md.get("http://purl.org/dc/elements/1.1/", {}).get("description", "")
    identifier = md.get("http://purl.org/dc/elements/1.1/", {}).get("identifier", "")

    l1 = collect_l1(book)

    # Index chapters → assign uids
    rows = []
    excluded_titles = {"index", "about the author"}
    counter = 1
    for kind, node in l1:
        ttl = node.title.strip()
        if ttl.lower() in excluded_titles:
            continue
        # Chapter number detection
        m = re.match(r"^(\d+)\.\s+(.*)$", ttl)
        if m:
            ch_num = m.group(1)
            ch_title = m.group(2)
            kind_label = "chapter"
        else:
            ch_num = ""
            ch_title = ttl
            kind_label = "preface" if "preface" in ttl.lower() else (
                "epilogue" if "epilogue" in ttl.lower() or "afterword" in ttl.lower() else "frontmatter"
            )
        uid = f"{counter:02d}"
        rows.append({
            "uid": uid,
            "kind": kind_label,
            "chapterNumber": ch_num,
            "title": ttl,
            "chapterTitle": ch_title,
            "href": node.href,
            "wordCount": 0,
        })
        counter += 1

    # Extract content
    for row in rows:
        html = html_for_href(book, row["href"])
        md_text = html_to_markdown(html)
        word_count = len(md_text.split())
        row["wordCount"] = word_count
        file_slug = slug(row["chapterTitle"])
        filename = f"uid-{row['uid']}-{file_slug}.md"
        fulltext_path = fulltext_dir / filename
        preamble = PREAMBLE.format(
            src=src_path.name, sha=sha, uid=row["uid"],
            part=row["kind"], ch=row["chapterNumber"] or "-",
            title=row["title"],
        )
        fulltext_path.write_text(preamble + f"# {row['title']}\n\n" + md_text + "\n", encoding="utf-8")
        row["file"] = filename

    # toc.md (pipe table like 解构领域驱动设计)
    toc_lines = ["uid|kind|chapterNumber|title|wordCount|file"]
    for r in rows:
        toc_lines.append(f"{r['uid']}|{r['kind']}|{r['chapterNumber']}|{r['title']}|{r['wordCount']}|{r['file']}")
    (root_path / "00-原书档案" / "toc.md").write_text("\n".join(toc_lines) + "\n", encoding="utf-8")

    # book-meta.json
    meta = {
        "title": title,
        "creator": creator,
        "sourcePath": str(src_path),
        "fileSha256": sha,
        "fileSize": size,
        "epubChapterCount": sum(1 for r in rows if r["kind"] == "chapter"),
        "epubPrefaceCount": sum(1 for r in rows if r["kind"] == "preface"),
        "epubEpilogueCount": sum(1 for r in rows if r["kind"] == "epilogue"),
        "tocFormat": "epub3-xhtml",
        "identifier": identifier,
        "language": language,
        "publisher": publisher,
        "date": date,
        "description": description,
    }
    (root_path / "00-原书档案" / "book-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Extracted {len(rows)} fulltext files → {fulltext_dir}")
    for r in rows:
        print(f"  {r['uid']}  [{r['kind']:<10}]  {r['title'][:60]:<60}  {r['wordCount']:>6} words  →  {r['file']}")
    print(f"\nbook-meta.json sha256={sha}")


if __name__ == "__main__":
    main()