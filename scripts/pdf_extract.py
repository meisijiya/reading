#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_extract.py — 从带书签的 LaTeX 生成 PDF 抽取全文，按 level-2 章节切粒。
产出：00-原书档案/fulltext/chNN.md + toc.md + toc.json + book-meta.json

设计要点（来自对本 PDF 的实测排版）：
  size 24.8  章标题      size 20.7  "Chapter N"
  size 14.3  小节标题     size 10.9  正文
  y < 30                页眉（H. Roitman — 书名，斜体 10.0）
  y > h-40              页脚页码
  行内 span 按 x 排序 → 表格行可读
  部分页（Roman 部分页）归入其后首章开头
"""
import sys, io, os, re, json, hashlib, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import fitz

PDF = r"D:\26code\read\book\agentic-ai-guide-zh-v1.1.0.pdf"
OUT_ROOT = r"D:\26code\read\docs\智能体AI漫游指南（从基础到系统）\00-原书档案"
FULLTEXT_DIR = os.path.join(OUT_ROOT, "fulltext")

HEADER_Y = 30.0      # 低于此 y 视为页眉
FOOTER_MARGIN = 40.0 # 高于 h-margin 视为页脚
BODY_SIZE_MIN = 9.0  # 低于此字号的 span（如下标 8.0）仍保留但降级


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def is_cjk(ch):
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF) or \
           (0x3000 <= o <= 0x303F) or (0xFF00 <= o <= 0xFFEF)


def join_spans(spans):
    """span 级拼接。同一视觉行的 span 边界常缺空格（Part|I、Transformer|本身），
    但 CJK 与 CJK 之间原书不加空格，因此只在「非 CJK × 非 CJK」处补一个空格。"""
    out = ""
    for s in spans:
        t = s["text"]
        if not t:
            continue
        if out:
            a, b = out[-1], t[0]
            if not a.isspace() and not b.isspace() and not (is_cjk(a) or is_cjk(b)):
                out += " "
        out += t
    return out


def page_lines(page, pno):
    """重建一页的文本流：剔页眉页脚，同一视觉行合并（y 容差 4pt），行内按 x 排序。
    返回 [(y, size, text, is_image)]

    注意：不能直接按 y 排序。同一视觉行内 CJK 与拉丁基线可差 1pt
    （如 y=309.1 的中文标题 与 y=310.1 的 "1.1"），按 y 排会把它们拆散并颠倒顺序。
    """
    h = page.rect.height
    raw = []   # [(y, [spans])]
    images = []  # [y]
    d = page.get_text("dict")
    for b in d["blocks"]:
        if b.get("type") != 0:
            images.append(b["bbox"][1])
            continue
        for ln in b["lines"]:
            y = ln["bbox"][1]
            if y < HEADER_Y or y > h - FOOTER_MARGIN:
                continue
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            if raw and abs(raw[-1][0] - y) < 4.0:
                raw[-1][1].extend(spans)      # 与上一行属同一视觉行
            else:
                raw.append((y, list(spans)))

    out = []
    for y, spans in raw:
        spans = sorted(spans, key=lambda s: s["bbox"][0])
        txt = join_spans(spans).rstrip()
        if not txt.strip():
            continue
        size = spans[0]["size"]   # 行内首个 span 的字号定级
        out.append((y, size, txt, False))
    for y in sorted(images):
        out.append((y, 99.0, "", True))
    out.sort(key=lambda t: round(t[0], 1))
    return out


LINE_GAP = 18.0   # y 间距大于此值视为新段（正文行距约 13.5pt，段距更大）
ROMAN_PART = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)\s+\S")


def render_pages(doc, first, last):
    """把 [first, last] 页渲染成 markdown。

    控制流只用显式 kind 标签，绝不用「渲染后的字符串前缀」来判定类型
    （前导换行会让 startswith 失效，标题会被当成正文）。
    """
    items = []  # (kind, text, y)
    for pno in range(first - 1, min(last, doc.page_count)):
        page = doc[pno]
        for y, size, txt, is_img in page_lines(page, pno + 1):
            if is_img:
                items.append(("image", f"[图片 · 原书 PDF p{pno+1}]", y))
                continue
            t = txt.strip()
            if not t or re.fullmatch(r"\d{1,4}", t):
                continue
            if size >= 19.0 and ROMAN_PART.match(t):
                items.append(("part", t, y))          # 罗马数字开头 = 部分页
            elif size >= 24.0:
                items.append(("chapter", t, y))       # 章标题
            elif size >= 19.0:
                items.append(("chapter", t, y))       # "Chapter N" 标签
            elif size >= 13.5:
                items.append(("section", t, y))       # 小节（1.1 / 1.2.1）
            elif t.startswith(("Figure ", "Table ")):
                items.append(("caption", t, y))
            else:
                items.append(("body", t, y))
        items.append(("body", "\x00PAGEBREAK\x00", None))

    # ---- 标题对合并 ----
    # PDF 里「编号行」与「标题文字行」是两个独立 line，直接输出会让顺序颠倒且无法定位。
    #   ### 1.1  +  ### LLM 工作原理：直觉概览   ->  ### 1.1 LLM 工作原理：直觉概览
    #   # Chapter 1 + # LLM 架构与优化方法        ->  # Chapter 1 · LLM 架构与优化方法
    NUM_ONLY = re.compile(r"\d+(\.\d+)*$")
    LABEL_ONLY = re.compile(r"(Chapter\s+\d+|Part\s+[IVX]+|Part\s+[A-Z])$")
    merged, i = [], 0
    while i < len(items):
        kind, text, y = items[i]
        t = text.strip()
        nxt = items[i + 1] if i + 1 < len(items) else None
        if kind == "section" and NUM_ONLY.match(t) and nxt and nxt[0] == "section":
            merged.append((kind, f"{t} {nxt[1]}".strip(), y))
            i += 2
            continue
        if kind in ("chapter", "part") and LABEL_ONLY.match(t) and nxt and nxt[0] == kind:
            merged.append((kind, f"{t} · {nxt[1]}".strip(), y))
            i += 2
            continue
        merged.append((kind, text, y))
        i += 1
    items = merged

    md = []
    para = []
    caption = []
    prev_y = None

    def flush_body():
        if para:
            md.append("".join(para))
            md.append("")
            para.clear()

    def flush_caption():
        if caption:
            md.append("> " + " ".join(caption))
            md.append("")
            caption.clear()

    for kind, text, y in items:
        if kind == "body":
            flush_caption()
            if text == "\x00PAGEBREAK\x00":
                prev_y = None
                flush_body()
                continue
            if prev_y is not None and y is not None and (y - prev_y) > LINE_GAP:
                flush_body()          # y 间距过大 = 新段
            para.append(text)
            prev_y = y if y is not None else prev_y
        elif kind == "caption":
            flush_body()
            caption.append(text)
        else:
            flush_body()
            flush_caption()
            if kind == "image":
                md.append(f"*（{text}，图形本身未提取）*")
            elif kind == "part":
                md.append(f"## Part · {text}")
            elif kind == "chapter":
                md.append(f"# {text}")
            else:
                md.append(f"### {text}")
            md.append("")

    flush_body()
    flush_caption()
    out = "\n".join(md)
    # PDF 文本层会夹带 NUL 等控制字符（ch09 见过 5 个）。
    # 留着会让 git / mkdocs / read 把 fulltext 当二进制文件，必须在落盘前清掉。
    out = "".join(ch for ch in out if ch >= " " or ch in "\n")
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


def main():
    doc = fitz.open(PDF)
    toc = doc.get_toc()

    # ---- 章边界（level-2），部分页并入其后首章 ----
    l1 = [(p, t) for lv, t, p in toc if lv == 1]
    chaps = [(p, t) for lv, t, p in toc if lv == 2]
    part_before = {}
    for pp, pt in l1:
        part_before.setdefault(pp, pt)

    ranges = []
    for i, (p, t) in enumerate(chaps):
        start = p
        owner = ""
        for pp, pt in l1:
            if pp <= p and pp >= p - 2:      # 紧贴章首页的部分页
                start, owner = pp, pt
        end = chaps[i + 1][0] - 1 if i + 1 < len(chaps) else doc.page_count
        # end 不能超过下一章起点的部分页（若有）
        for pp, pt in l1:
            if p < pp < end:
                end = pp - 1
        ranges.append({"n": i + 1, "title": t, "start": start, "end": end,
                       "part": owner})

    os.makedirs(FULLTEXT_DIR, exist_ok=True)

    entries = []
    # ---- 前置组 ch00：p25 .. ch01.start-1 ----
    front_start = min(p for p, _ in l1)
    front_end = ranges[0]["start"] - 1
    ch0 = render_pages(doc, front_start, front_end)
    p0 = os.path.join(FULLTEXT_DIR, "ch00.md")
    open(p0, "w", encoding="utf-8", newline="\n").write(ch0)
    entries.append({"uid": "ch00", "title": "前置：免责声明 / 关于作者 / 前言 / 引言 / 缩略语表",
                    "pdf_pages": [front_start, front_end], "sha256": sha256_of(p0),
                    "bytes": os.path.getsize(p0), "sections": []})

    # ---- 30 章 ----
    for r in ranges:
        body = render_pages(doc, r["start"], r["end"])
        name = f"ch{r['n']:02d}.md"
        p = os.path.join(FULLTEXT_DIR, name)
        open(p, "w", encoding="utf-8", newline="\n").write(body)
        secs = [t for lv, t, pp in toc
                if lv in (3,) and r["start"] <= pp <= r["end"]]
        entries.append({"uid": f"ch{r['n']:02d}", "title": r["title"],
                        "part": r["part"], "pdf_pages": [r["start"], r["end"]],
                        "sha256": sha256_of(p), "bytes": os.path.getsize(p),
                        "sections": secs})
        print(f"{name}  p{r['start']}-{r['end']}  {len(body):>7,} chars  "
              f"{len(secs):>2} sections  {r['title']}")

    # ---- toc.json ----
    toc_json = {
        "source": "PDF (LaTeX/xdvipdfmx)",
        "pdf": os.path.basename(PDF),
        "page_count": doc.page_count,
        "granularity": "level-2 bookmark (每章一个文件)",
        "chapters": entries,
    }
    with open(os.path.join(OUT_ROOT, "toc.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(toc_json, f, ensure_ascii=False, indent=2)

    # ---- toc.md ----
    lines = ["# 章节目录 · 《智能体 AI 漫游指南：从基础到系统》", "",
             f"> 来源：`{os.path.basename(PDF)}`（{doc.page_count} 页 PDF 书签，level-2 切粒，"
             f"共 {len(entries)} 个 fulltext 文件）", "",
             "| uid | 章节 | PDF 页 | fulltext 字节 | 小节数 | sha256(前16) |",
             "|---|---|---|---|---|---|"]
    for e in entries:
        lines.append(f"| `{e['uid']}` | {e['title']} | p{e['pdf_pages'][0]}-p{e['pdf_pages'][1]} | "
                     f"{e['bytes']:,} | {len(e['sections'])} | `{e['sha256'][:16]}` |")
    with open(os.path.join(OUT_ROOT, "toc.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    # ---- book-meta.json ----
    meta = {
        "title": "智能体 AI 漫游指南：从基础到系统",
        "title_en": "agentic-ai-guide",
        "author": "Haggai Roitman",
        "language": "zh-CN",
        "version": "1.3 (2026)",
        "source": "本地 PDF（用户自备）",
        "pdf_pages": doc.page_count,
        "producer": doc.metadata.get("producer", ""),
        "creation_date": doc.metadata.get("creationDate", ""),
        "chapters": len(entries),
        "granularity": "PDF 书签 level-2 = 章；level-3 = 书内小节（原书编号如 1.2.1）",
        "fulltext_files": len(entries),
        "extract_method": "pymupdf get_text('dict')，按 y 剔页眉(y<30)/页脚(y>h-40)，行内按 x 排序，字号还原标题层级",
    }
    with open(os.path.join(OUT_ROOT, "book-meta.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    total = sum(e["bytes"] for e in entries)
    print(f"\nTOTAL: {len(entries)} files, {total:,} bytes")
    doc.close()


if __name__ == "__main__":
    main()