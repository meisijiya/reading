# Learnings — claude-code-orange-book-distill

Conventions, patterns, and successful approaches discovered during work on this plan.

_Auto-scaffolded by /start-work. Append new entries below - never overwrite._

---

## 2026-08-24 — todo 1 (`scripts/distill_epub.py`) 完成

### NCX 切粒细节
- 14 个 level-1 chapter node；全部命中 `^第\d+章\s+\S`（紧跟空格 + 非空白字符 — 关键，避免误中正文里的「第11章将详细介绍…」）。
- 4 个 Part（`第一部分~第四部分`），全部命中 `^第N部分` 正则。
- 119 个 subchapter / appendix / frontmatter 节点被归入 `ncxSubchapterCount`。
- 附录 A-E 与自序/前言/版权 等 level-0 节点未匹配 Part 模式，按 spec 跳过（不计入 chapter 也不计入 part）。
- **Fallback 未触发**（chapter_count = 14 ≫ 3）；模块 grouping 也没退化到 `00-全编`。

### 文件结构事实
- OPF 路径 = `EPUB/content.opf`；NCX 路径 = `EPUB/toc.ncx`，OPF-relative 文件名 = `toc.ncx`，实际 zip 路径 = `EPUB/toc.ncx`（ebooklib `file_name` 是 OPF-relative，zip 内路径多 `EPUB/` 前缀）。
- spine 14 项：chapter_0..chapter_13.xhtml。chapter_0 是封面/toc，chapter_5~8 各装 1 个 part 的多章内容，chapter_9~13 是 5 个附录。
- 每章（level-1 navPoint）的 `<content src>` 都指向所属 part 的同一个 xhtml 文件 → 切章必须在该 xhtml 内按 `^第\d+章\s+\S` 划边界，不能靠 spine 索引。

### 解析陷阱（已修）
- ElementTree 的 `find('ncx:navMap', ns)` 在 `<ncx xmlns="...">` 默认命名空间下返回 None（因为前缀未在 root 声明）。改用 Clark 形式 `{http://.../ncx/}navMap` 才能匹配。
- ebooklib 的 `book.toc` 是 Link 对象列表（chapter href），不是 NCX 文件。NCX 必须从 `book.items` 里按 `media_type == application/x-dtbncx+xml` 找。
- ebooklib OPF metadata 走 `get_metadata('DC', 'title')` / `'OPF'` 两个 namespace；本 epub `generator` 走 OPF。

### HTML 转换陷阱（已修）
- 每个字符被 `<strong>` 包一层 → `inline()` 渲染会变成 `**第****1****章**`。
- 解决：先用 `plain()` 取裸文本，命中 `^第\d+章\s+...` 或 `^\d+\.\d+...` 就改写为 markdown heading（`##` / `###`）；其余正文保留 strong/em 强调。
- `<img src="images/foo.jpg">` → 必须归一化掉 `EPUB/` 和 `../` 前缀才能和 zip 内的 `EPUB/images/foo.jpg` 对齐 → 重写为 `../assets/<sha256[0:16]>.jpg`（fulltext 在 `00-原书档案/fulltext/` 下，assets 同级，`../` 回退一次）。

### 切粒对账
- fulltext 文件数 = 14 == toc.md 数据行数 = 14 == ncxChapterCount。
- sha256 三处一致：`book/<source>.epub` == `00-原书档案/epub/<source>.epub` == `book-meta.json.fileSha256` = `039ef554...d05`。
- wordCount 范围：2960（ch10 避坑指南，最短）~ 12291（ch4 核心工作模式，最长）。
- assets 数：map 76 个条目（不同 src 路径），落盘 75 个文件（两个 src 指向同 sha256 内容，自动去重）。

