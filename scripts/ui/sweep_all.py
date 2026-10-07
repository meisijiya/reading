"""门禁 2/2：全站不变量扫描。

check_evidence.py 每本书只抽卡片最多的那一页，覆盖面窄。这里把
「带外残留标记 / 空壳证据带 / 原文带混入编者段落 / 段首标记未摘净 /
右栏漏改写 / 卡片数与 md 对不上」六条不变量跑到**每一个**含 ≥2 张卡的
模块页上，任何一页破就打印出来。

用法（必须从仓库根运行）：
    python -m mkdocs build --strict
    python -m http.server 8766 --bind 127.0.0.1 --directory site
    python scripts/ui/sweep_all.py

注意：docs/AI Engineering (Chip Huyen) 是指向不存在路径的断链 junction，
任何递归遍历（Path.rglob/glob）都在遍历阶段抛 FileNotFoundError，
try/except 救不回来，必须用 os.scandir 逐层下钻。
"""
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
# 预览地址可覆盖：模拟 CI 时用 git worktree 在另一个端口起服务。
# 用法：RD_SITE=http://127.0.0.1:8767/ python scripts/ui/<本脚本>
BASE = os.environ.get("RD_SITE", "http://127.0.0.1:8766/")
ROOT = Path("docs")

H2 = re.compile(r"^##\s+(.*)$", re.M)
IDS = [re.compile(r"^Q\d+-\d+[\s　]"), re.compile(r"^§\s*\d+"),
       re.compile(r"^Q\d+[\s　]"), re.compile(r"[（(]\s*第\s*\d+\s*章\s*[）)]")]


def walk_modules():
    """安全枚举所有 书/NN-模块/README.md"""
    out = []
    for book in sorted(os.listdir(ROOT)):
        bdir = ROOT / book
        try:
            subs = sorted(os.listdir(bdir))
        except OSError:
            continue
        for sub in subs:
            if not sub[:2].isdigit():
                continue
            f = bdir / sub / "README.md"
            if not f.exists():
                continue
            n = sum(1 for h in H2.findall(f.read_text(encoding="utf-8"))
                    if any(p.search(h) for p in IDS))
            if n >= 2:
                out.append((f.relative_to(ROOT), n))
    return out


def url_for(rel_md: Path):
    parts = rel_md.as_posix()[:-3].split("/")
    if parts[-1] == "README":
        parts.pop()
    return BASE + "/".join(urllib.parse.quote(p) for p in parts) + "/"


JS = r"""() => {
  const srcViolations = [];
  for (const lane of document.querySelectorAll('.rd-ev--src')) {
    for (const c of lane.children) {
      if (c.classList.contains('rd-ev-label')) continue;
      if (c.tagName === 'P') srcViolations.push(c.textContent.slice(0, 50));
    }
  }
  const stranded = [...document.querySelectorAll('.md-typeset p, .md-typeset blockquote')]
    .filter(n => !n.closest('.rd-ev') && /^[📖🧭➕]/.test(n.textContent.trim()))
    .map(n => n.tagName + ':' + n.textContent.trim().slice(0, 40));
  const unstripped = [...document.querySelectorAll('.rd-ev p')]
    .filter(p => /^[📖🧭➕]/.test(p.textContent.trim()))
    .map(p => p.textContent.slice(0, 40));
  const emptyLanes = [...document.querySelectorAll('.rd-ev')]
    .filter(l => l.children.length <= 1).length;
  const orphanH2 = [...document.querySelectorAll('.rd-card > h2')]
    .filter(h => !h.textContent.trim()).length;
  const tocMissed = [...document.querySelectorAll('.md-nav--secondary')]
    .map(nav => [...nav.querySelectorAll('ul[data-md-component="toc"] > li > a.md-nav__link')]
      .filter(a => !a.querySelector('.rd-toc-id') && /^(Q\d+|§\s*\d+)/.test(a.textContent.trim())).length);
  return {
    cards: document.querySelectorAll('.rd-card').length,
    src: document.querySelectorAll('.rd-ev--src').length,
    sum: document.querySelectorAll('.rd-ev--sum').length,
    add: document.querySelectorAll('.rd-ev--add').length,
    loose: document.querySelectorAll('.rd-ev-loose .rd-ev').length,
    srcViolations, stranded, unstripped, emptyLanes, orphanH2, tocMissed,
  };
}"""

targets = walk_modules()
print(f"含 ≥2 张卡的模块页：{len(targets)} 个")

bad, pages, lanes = [], 0, 0
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    stamp = str(int(time.time()))
    for pat in ("evidence.js", "extra.css"):
        pg.route("**/" + pat, lambda r: r.continue_(url=r.request.url + "?v=" + stamp))
    for rel, n_cards in targets:
        pg.goto(url_for(rel))
        # 等确定性条件，不要固定睡眠：evidence.js 要等 bundle 定义出
        # window.document$（轮询间隔 50ms）才装订订阅，重页面 + 连续压测下
        # 固定 sleep 420ms 会偶发性地「脚本还没跑」，报出一堆假的「卡片数 0」。
        pg.wait_for_function(
            "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'",
            timeout=15000)
        g = pg.evaluate(JS)
        tag = str(rel)
        pages += 1
        lanes += g["src"] + g["sum"] + g["add"] + g["loose"]
        if g["cards"] != n_cards:
            bad.append(f"{tag} 卡片数 {g['cards']} != md 算出的 {n_cards}")
        if g["srcViolations"]:
            bad.append(f"{tag} 原文带混入编者段落 {g['srcViolations'][:1]}")
        if g["stranded"]:
            bad.append(f"{tag} 带外残留标记 {g['stranded'][:1]}")
        if g["unstripped"]:
            bad.append(f"{tag} 段首标记未摘净 {g['unstripped'][:1]}")
        if g["emptyLanes"]:
            bad.append(f"{tag} 空壳证据带 {g['emptyLanes']} 条")
        if g["orphanH2"]:
            bad.append(f"{tag} 卡片标题丢失 {g['orphanH2']} 条")
        if any(g["tocMissed"]):
            bad.append(f"{tag} 右栏漏改写 {g['tocMissed']}")
        if g["loose"] and g["cards"] == 0:
            bad.append(f"{tag} 无卡却有带外证据带（异常）")
    b.close()

print(f"扫了 {pages} 页，共渲染 {lanes} 条证据带")
print(f"违规 {len(bad)} 条")
for x in bad[:40]:
    print("  FAIL", x)