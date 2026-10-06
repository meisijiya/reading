#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_fulltext.py — 按 AGENTS.md 规则五第 4 条，给每张卡片的「章节」行补 fulltext 链接。

规则五原文：「每张卡片『原文出处』必须用 markdown 链接 …… `00-原书档案/fulltext/` 已被
mkdocs build 进 site，但卡片不链 = 死入口。」

本脚本幂等：已带链接的行原样跳过。改的是链接形态，不动 `§` 编号本体。

Usage:
  python scripts/link_fulltext.py <book_root_dir> [<book_root_dir> ...] [--dry-run]
"""
import sys, io, os, re, glob, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# `- 章节: ch03 §2.1` / `- 章节: ch05 §4.2.2 + §4.2.3 + 实验 4-1` / `- 章节: ch10`
CH_LINE = re.compile(r"^(\s*-\s*章节:\s*.*?)(\s*)$", re.M)
CH_REF = re.compile(r"\b(ch\d{2})\b")
LINKED = re.compile(r"\[原文\]\(")


def process(root: str, dry: bool = False):
    ft_dir = os.path.join(root, "00-原书档案", "fulltext")
    if not os.path.isdir(ft_dir):
        print(f"[SKIP] {root}: 无 fulltext 目录")
        return 0

    # 章节号 -> 实际文件名（ch03 -> ch03.md / uid-03-xxx.md 都兼容）
    def resolve(ch: str):
        direct = os.path.join(ft_dir, f"{ch}.md")
        if os.path.exists(direct):
            return f"{ch}.md"
        cands = sorted(glob.glob(os.path.join(ft_dir, f"{ch}*.md")))
        return os.path.basename(cands[0]) if cands else None

    changed_files = changed_lines = 0
    for md in sorted(glob.glob(os.path.join(root, "[0-9][0-9]-*"))):
        p = os.path.join(md, "README.md")
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read()
        mods = 0

        def repl(m):
            nonlocal mods
            line = m.group(1)
            if LINKED.search(line):
                return m.group(0)          # 已带链接，幂等跳过
            chs = []
            for ch in CH_REF.findall(line):
                if ch not in chs:
                    chs.append(ch)
            if not chs:
                return m.group(0)
            links = []
            for ch in chs:
                fn = resolve(ch)
                if fn:
                    links.append(f"[{ch}](../00-原书档案/fulltext/{fn})")
            if not links:
                return m.group(0)
            mods += 1
            return f"{line}　（原文：{' / '.join(links)}）"

        new = CH_LINE.sub(repl, text)
        if new != text:
            changed_lines += mods
            changed_files += 1
            if not dry:
                with open(p, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new)
            print(f"  {os.path.basename(md):34s} +{mods} 条链接")

    print(f"  => {changed_files} 个文件、{changed_lines} 行"
          f"{'（dry-run，未写入）' if dry else '已更新'}")
    return changed_lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for r in args.roots:
        print(f"\n=== {r} ===")
        process(r, args.dry_run)


if __name__ == "__main__":
    main()