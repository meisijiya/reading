#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_package.py — 知识包逐卡 verbatim 验证器。

对每个 `NN-*/README.md` 里的每张卡：
  1. 抽出 `> 📖 **原文** (chNN ...)：<引用文本>` 的引用文本与目标章节
     —— 必须支持多行：markdown 引用块里的 `> ` 续行属于同一条引用
  2. 归一化（只去空白，**不做 NFKC**）后在 `00-原书档案/fulltext/chNN.md` 里子串匹配
  3. 报告 PASS / FAIL / WARN，并打印失败卡片供人工修

为什么不做 NFKC：NFKC 会把 `（Pooling）` 正规化成 `(Pooling)`、把 `“”` 压成 `""`，
等于让验证器和被验证对象用同一套「美化」规则，把真实的转写错误自动抹平。
（实测：带 NFKC 的 worker 自检报 100%，不带 NFKC 的独立验证抓出 3 类真实错误。）

正交检查：
  - 卡片总数、每模块卡片数
  - **零引用卡**：一张卡完全没有 📖 原文块（证据缺失）
  - 过短引用：WARN，不算 FAIL（往往是列表项的引导标签）

Usage:
  python scripts/verify_package.py <book_root_dir> [<book_root_dir> ...] [--verbose]
"""
import sys, io, os, re, glob, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

QUOTE_START = re.compile(r"^>\s*📖\s*\*\*原文\*\*\s*[\(（]\s*([^)）]*?)\s*[\)）]\s*[:：]\s*(.*)$")
QUOTE_CONT = re.compile(r"^>\s?(.*)$")
CARD_RE = re.compile(r"^##\s+(Q[\w\-]+)\s+(.*)$", re.M)

MIN_QUOTE_LEN = 12   # 低于此长度记 WARN，不计 FAIL


def norm(s: str) -> str:
    """归一化：只去掉所有空白字符。不做 NFKC —— 见模块 docstring。"""
    return re.sub(r"\s+", "", s)


def extract_quotes(text: str):
    """抽出所有 📖 引用块及其完整内容（含多行续行）。
    返回 [(loc, content), ...]"""
    out = []
    cur = None
    for ln in text.split("\n"):
        m = QUOTE_START.match(ln)
        if m:
            if cur:
                out.append(cur)
            cur = [m.group(1), [m.group(2)]]
            continue
        if cur is not None:
            c = QUOTE_CONT.match(ln)
            if c:
                cur[1].append(c.group(1))
                continue
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return [(loc, "".join(parts)) for loc, parts in out]


def verify_book(root: str, min_rate: float, verbose: bool):
    ft_dir = os.path.join(root, "00-原书档案", "fulltext")
    if not os.path.isdir(ft_dir):
        print(f"[SKIP] {root}: 无 00-原书档案/fulltext")
        return None

    cache = {}

    def fulltext(ch: str):
        """按 chNN 取全文；找不到唯一匹配时返回 None"""
        if ch in cache:
            return cache[ch]
        cands = glob.glob(os.path.join(ft_dir, f"{ch}*.md"))
        if not cands:
            cache[ch] = None
            return None
        txt = norm(open(cands[0], encoding="utf-8", errors="replace").read())
        cache[ch] = txt
        return txt

    modules = sorted(d for d in glob.glob(os.path.join(root, "[0-9][0-9]-*"))
                     if os.path.isdir(d))
    total = passed = failed = 0
    warned = 0
    zero_quote_total = 0
    fails, warns, per_mod = [], [], {}

    for md in modules:
        src = os.path.join(md, "README.md")
        if not os.path.exists(src):
            continue
        text = open(src, encoding="utf-8").read()
        mod = os.path.basename(md)
        cards = list(CARD_RE.finditer(text))

        bounds = []
        for i, m in enumerate(cards):
            start = m.start()
            end = cards[i + 1].start() if i + 1 < len(cards) else len(text)
            bounds.append((m.group(1), m.group(2), text[start:end]))

        m_total = m_pass = 0
        no_quote_cards = []
        for cid, qtitle, block in bounds:
            quotes = extract_quotes(block)
            if not quotes:
                no_quote_cards.append(cid)
            for loc, qtext in quotes:
                m_total += 1
                total += 1
                mch = re.search(r"(ch\d{2})", loc)
                if not mch:
                    failed += 1
                    fails.append((mod, cid, loc, "定位里找不到 chNN", qtext[:60]))
                    continue
                ft = fulltext(mch.group(1))
                if ft is None:
                    failed += 1
                    fails.append((mod, cid, loc, f"fulltext {mch.group(1)} 不存在", qtext[:60]))
                    continue
                frag = norm(qtext)
                if len(frag) < MIN_QUOTE_LEN:
                    warned += 1
                    warns.append((mod, cid, loc, f"引用过短({len(frag)}字)", qtext[:60]))
                    continue
                if frag in ft:
                    m_pass += 1
                    passed += 1
                else:
                    failed += 1
                    fails.append((mod, cid, loc, "verbatim 未命中", qtext[:60]))

        per_mod[mod] = (m_total, m_pass, len(cards))
        zero_quote_total += len(no_quote_cards)
        line = f"  {mod:38s} 卡={len(cards):3d}  引用={m_total:3d}  命中={m_pass:3d}"
        if no_quote_cards:
            line += f"  [无📖 {len(no_quote_cards)}: {' '.join(no_quote_cards[:8])}]"
        print(line)

    denom = passed + failed
    rate = passed / denom if denom else 0.0
    print(f"\n  合计：卡片总数 {sum(v[2] for v in per_mod.values())} | "
          f"📖引用 {total} | PASS {passed} | FAIL {failed} | WARN(过短) {warned} | "
          f"零引用卡 {zero_quote_total} | 命中率 {rate:.1%}")
    if rate < min_rate:
        print(f"  ❌ 命中率 {rate:.1%} < 阈值 {min_rate:.0%}")
    else:
        print(f"  ✅ 命中率 {rate:.1%} ≥ 阈值 {min_rate:.0%}")

    if fails and verbose:
        print(f"\n  失败明细（{len(fails)} 条，前 40）：")
        for f in fails[:40]:
            print(f"    [{f[3]}] {f[0]} {f[1]} {f[2]} :: {f[4]!r}")
    elif fails:
        print(f"  失败 {len(fails)} 条（--verbose 看明细）")
    if verbose and warns:
        print(f"\n  过短引用 WARN（{len(warns)} 条）：")
        for w in warns[:20]:
            print(f"    {w[0]} {w[1]} {w[2]} :: {w[4]!r}")

    return {"total": total, "passed": passed, "failed": failed, "warned": warned,
            "zero_quote": zero_quote_total, "rate": rate,
            "cards": sum(v[2] for v in per_mod.values()), "per_mod": per_mod}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--min-rate", type=float, default=0.95)
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    results = {}
    for root in args.roots:
        print(f"\n=== {root} ===")
        r = verify_book(root, args.min_rate, args.verbose)
        if r:
            results[root] = r

    print("\n" + "=" * 64)
    ok = all(r["rate"] >= args.min_rate for r in results.values())
    for root, r in results.items():
        print(f"{os.path.basename(root):32s} 卡={r['cards']:4d} 引用={r['total']:4d} "
              f"PASS={r['passed']:4d} FAIL={r['failed']:3d} WARN={r['warned']:3d} "
              f"零引用卡={r['zero_quote']:3d}  {r['rate']:.1%}")
    print(f"\n总判定：{'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()