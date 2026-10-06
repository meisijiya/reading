#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clean_fulltext.py — 清洗 fulltext 里会让 mkdocs --strict 报错的形态，并重算 toc.json。

处理三类（都不改正文语义，只改「链接形态」）：
  1) epub 图片死链：epub_extract 生成了 ![alt](../media/x.svg) 但从未导出 media 目录
     -> 转为文字标注 `〔图 …（原书配图）〕`，保留图号信息，去掉死链
  2) PDF 公式编号假链接：`[ π θ ](5.10)` 被 markdown 当成链接
     -> 方括号转义，渲染为字面量
  3) 重算 toc.json 里每个 fulltext 的 sha256 / bytes（文件变了必须同步）

幂等：已清洗过的内容不会再匹配。

Usage:
  python scripts/clean_fulltext.py <book_root> [<book_root> ...] [--dry-run]
"""
import sys, io, os, re, glob, json, hashlib, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ![alt](../media/x.svg) —— alt 里常含图号与标题
IMG_RE = re.compile(r"!\[([^\]]*)\]\((?:\.\./)?media/[^)]+\)")
# 公式编号： [ xxx ](5.10) / [ xxx ](12.3) —— 数字点分编号，不是真链接。
# 必须有 (?<!\\) 守卫，否则重复运行会二次转义（\[ → \\[）。
FORMULA_LINK = re.compile(r"(?<!\\)\[([^\]\n]{1,40})\]\((\d+(?:\.\d+)+)\)")
# PDF 里 Few-shot 示例的教学文本：Entities: [Apple](ORG), [iPhone 15](PRODUCT)
# 以及 Format: [ENTITY](TYPE)。链接目标是纯大写标签，不是 URL/路径，
# 会被 markdown 解析成相对链接 -> 死链。只匹配「大写单词作目标」，正常链接不会命中。
LABEL_LINK = re.compile(r"(?<!\\)\[([^\]\n]{1,40})\]\(([A-Z][A-Z_]{1,20})\)")
# PDF 抽取丢了代码块 ``` 标记，导致 Python 代码里的 [x](**kwargs) / [x](self._workdir / ...)
# 被 markdown 当成链接。锚点高度特异（** 与 self._workdir），不会误伤正常链接。
CODE_LINK = re.compile(r"(?<!\\)\[([^\]\n]{1,60})\]\((\*\*|self\._workdir)")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_text(s):
    n_img = n_fml = 0

    def img(m):
        nonlocal n_img
        n_img += 1
        alt = m.group(1).strip()
        return f"〔{alt} · 原书配图，epub 未随文本导出〕" if alt else "〔原书配图〕"

    def fml(m):
        nonlocal n_fml
        n_fml += 1
        return rf"\[{m.group(1)}\]({m.group(2)})"

    def lbl(m):
        nonlocal n_fml
        n_fml += 1
        return rf"\[{m.group(1)}\]({m.group(2)})"

    def code(m):
        nonlocal n_fml
        n_fml += 1
        return rf"\[{m.group(1)}\]({m.group(2)}"

    s = IMG_RE.sub(img, s)
    s = FORMULA_LINK.sub(fml, s)
    s = LABEL_LINK.sub(lbl, s)
    s = CODE_LINK.sub(code, s)
    return s, n_img, n_fml


def process(root, dry=False):
    ft = os.path.join(root, "00-原书档案", "fulltext")
    if not os.path.isdir(ft):
        print(f"[SKIP] {root}")
        return
    ti = fo = 0
    for p in sorted(glob.glob(os.path.join(ft, "*.md"))):
        s = open(p, encoding="utf-8").read()
        new, ni, nf = clean_text(s)
        if new != s:
            ti += ni
            fo += nf
            if not dry:
                with open(p, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new)
    print(f"  {os.path.basename(root)}: 图片链接→文字 {ti} 处 | 公式假链接转义 {fo} 处"
          f"{'（dry-run）' if dry else ''}")

    # 重算 toc.json
    toc = os.path.join(root, "00-原书档案", "toc.json")
    if os.path.exists(toc):
        data = json.load(open(toc, encoding="utf-8"))
        changed = 0
        for ch in data.get("chapters", []):
            name = ch.get("file") or f"{ch.get('uid')}.md"
            fp = os.path.join(ft, name)
            if not os.path.exists(fp):
                cand = glob.glob(os.path.join(ft, f"{ch.get('uid')}*.md"))
                if not cand:
                    continue
                fp = cand[0]
            ns, nb = sha256_file(fp), os.path.getsize(fp)
            if ch.get("sha256") != ns or ch.get("bytes") != nb:
                ch["sha256"], ch["bytes"], changed = ns, nb, changed + 1
        if changed and not dry:
            with open(toc, "w", encoding="utf-8", newline="\n") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {os.path.basename(root)}: toc.json 同步 {changed} 章 sha256/bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for r in args.roots:
        process(r, args.dry_run)


if __name__ == "__main__":
    main()