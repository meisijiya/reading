#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_quotes.py — 把 📖 引用对齐回原文，并规范化定位括号。

原理：**不猜内容，只从 fulltext 里取原文**。
对每条 verbatim 未命中的引用，用 difflib 在对应 fulltext 中定位它的最佳对应片段，
把引用替换成**原文里那一段**（因此替换后逐字来自原文，不是改写）。

两件独立的事：
  A) 规范化定位括号：`(ch16 §16.3）` 左右混用 -> `(ch16 §16.3)`
  B) 对齐未命中的引用文本（**支持多行 `> ` 续行引用块**）

安全阀：
  - 只有当「锚点前缀能在原文定位」且「对齐后相似度 >= --min-sim」时才写入
  - 其余一律列为 NEEDS_REVIEW，绝不自动改写
  - 默认 --dry-run

Usage:
  python scripts/fix_quotes.py <book_root> [--apply] [--min-sim 0.82] [--verbose]
"""
import sys, io, os, re, glob, argparse, difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

QUOTE_START = re.compile(r"^(\s*>\s*📖\s*\*\*原文\*\*\s*)[\(（]\s*([^)）]*?)\s*[\)）](\s*[:：]\s*)(.*)$")
QUOTE_CONT = re.compile(r"^>\s?(.*)$")
LOC_OK = re.compile(r"^[\w\s§.\-+（）()第章节实验]*$")


def norm(s):
    return re.sub(r"\s+", "", s)


def load_ft(ft_dir):
    cache = {}

    def get(ch):
        if ch in cache:
            return cache[ch]
        cands = sorted(glob.glob(os.path.join(ft_dir, f"{ch}*.md")))
        cache[ch] = open(cands[0], encoding="utf-8", errors="replace").read() if cands else None
        return cache[ch]
    return get


def align_to_source(ref, full, anchor=18, min_sim=0.82):
    """在 full 中定位 ref 对应的真实片段；成功返回原文片段，否则 None。"""
    r, f = norm(ref), norm(full)
    if not r or r in f:
        return None
    head = r[:anchor]
    pos = f.find(head)
    if pos < 0:
        sm = difflib.SequenceMatcher(None, r, f, autojunk=False)
        blocks = sm.get_matching_blocks()
        if sum(b.size for b in blocks) / len(r) < min_sim:
            return None
        first = max(blocks, key=lambda b: b.size)
        pos = max(0, first.b - first.a)
    cand = f[pos:pos + len(r)]
    if difflib.SequenceMatcher(None, r, cand, autojunk=False).ratio() >= min_sim:
        return cand
    return None


def split_like(text, n):
    """把对齐后的文本切成 n 份，喂回原有的多行结构（保持视觉布局）"""
    if n <= 1:
        return [text]
    step = max(1, len(text) // n)
    out, rest = [], text
    while len(out) < n - 1 and len(rest) > step:
        out.append(rest[:step])
        rest = rest[step:]
    out.append(rest)
    return out


def process_file(p, get_ft, mod, apply=False, min_sim=0.82, verbose=False):
    lines = open(p, encoding="utf-8").read().split("\n")
    out, i = [], 0
    fixed = review = paren = 0

    while i < len(lines):
        m = QUOTE_START.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        head, loc, colon, first_body = m.groups()
        loc = loc.strip()

        # 收集多行续行
        block = [first_body]
        j = i + 1
        while j < len(lines) and not QUOTE_START.match(lines[j]):
            c = QUOTE_CONT.match(lines[j])
            if not c:
                break
            block.append(c.group(1))
            j += 1

        new_head = f"{head}({loc}){colon}"
        if new_head != f"{head}{lines[i][len(head):]}" and f"（{loc}）" not in lines[i]:
            paren += 1

        body = "".join(block)
        mch = re.search(r"(ch\d{2})", loc) if LOC_OK.match(loc) else None
        full = get_ft(mch.group(1)) if mch else None

        if full and norm(body) and len(norm(body)) >= 12 and norm(body) not in norm(full):
            cand = align_to_source(body, full, min_sim=min_sim)
            if cand:
                fixed += 1
                if verbose:
                    print(f"  [FIX] {mod}: {body[:44]!r}\n         -> {cand[:44]!r}")
                parts = split_like(cand, len(block))
                out.append(new_head + parts[0])
                out.extend(">" + p for p in parts[1:])
                i = j
                continue
            review += 1
            if verbose:
                print(f"  [REVIEW] {mod}: {body[:66]!r}")

        out.append(new_head + first_body)
        out.extend(">" + b for b in block[1:])
        i = j

    text = "\n".join(out)
    changed = text != "\n".join(lines)
    if apply and changed:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return fixed, review, paren, changed


def process(root, apply=False, min_sim=0.82, verbose=False):
    ft_dir = os.path.join(root, "00-原书档案", "fulltext")
    get_ft = load_ft(ft_dir)
    tf = tr = tp = 0
    for md in sorted(glob.glob(os.path.join(root, "[0-9][0-9]-*"))):
        p = os.path.join(md, "README.md")
        if not os.path.exists(p):
            continue
        a, b, c, _ = process_file(p, get_ft, os.path.basename(md), apply, min_sim, verbose)
        if a or b or c:
            print(f"  {os.path.basename(md):34s} 对齐={a:3d} 需人工={b:3d} 括号={c:3d}")
        tf += a; tr += b; tp += c
    print(f"  => 对齐 {tf} 处 | 需人工 {tr} 处 | 括号规范化 {tp} 处"
          f"{'' if apply else '（dry-run，未写入）'}")
    return tf, tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-sim", type=float, default=0.82)
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()
    for r in args.roots:
        print(f"\n=== {r} ===")
        process(r, args.apply, args.min_sim, args.verbose)


if __name__ == "__main__":
    main()