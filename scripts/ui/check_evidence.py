"""门禁 1/2：证据结构化是否正确（浏览器硬断言 + 截图）。

用法（必须从仓库根运行）：
    python -m mkdocs build --strict
    python -m http.server 8766 --bind 127.0.0.1 --directory site
    python scripts/ui/check_evidence.py

期望值全部从源 md 独立算出，不采信页面上 JS 自己声明的数字。
断言原则：只写「能真的抓住那个 bug」的判据。
  - 「有 🧭 就至少渲染出 1 条归纳带」这种页面级 >0 是抓不住的——
    6 本书存在 `> 🧭` 写在引用块里的形态，漏掉全部也不影响 >0 成立。
    改成**逐卡**存在性对账，且加反向断言（md 里没有的标记不许凭空出现）。
  - 「原文带里不能有编者段落」不靠文本正则猜，改成结构判定：
    带**之外**若还有以标记开头的节点，说明分带漏了。
  - 对比度量的是**渲染后**的 computed color，不是 CSS 里的令牌字面值。

覆盖不到的部分：正文有没有被误吃、chip 是不是书自己的编号 ——
那两件事由 scripts/ui/check_text_integrity.py 负责。
"""
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("docs")
SHOT = Path(".scratch/ui/shots")
SHOT.mkdir(parents=True, exist_ok=True)

# 预览地址可覆盖：模拟 CI 时用 git worktree 建一份干净检出，
# 在另一个端口起服务，就能证明这个提交是自足的（而不是靠工作区里的
# 未跟踪文件才构建成功）。用法：RD_SITE=http://127.0.0.1:8767/ python scripts/ui/check_evidence.py
BASE = os.environ.get("RD_SITE", "http://127.0.0.1:8766/")

H2 = re.compile(r"^##\s+(.*)$", re.M)
# 四种真实定位符形态，见 evidence.js 文件头规则 1
ID_PATTERNS = [
    re.compile(r"^Q\d+-\d+[\s　]"),
    re.compile(r"^§\s*\d+"),
    re.compile(r"^Q\d+[\s　]"),
    re.compile(r"[（(]\s*第\s*\d+\s*章\s*[）)]"),
]
M_SRC = re.compile(r"^>\s*📖", re.M)                 # 原文标记（引用块形态）
M_SUM = re.compile(r"^[>\s]*🧭", re.M)              # 归纳标记：段落形态 + 引用块形态
M_ADD = re.compile(r"^[>\s]*➕", re.M)              # 补充标记：同上


def is_card(h):
    return any(p.search(h) for p in ID_PATTERNS)


def expected(md: Path):
    """页面级：卡片数 / 三种标记在全文的出现次数"""
    txt = md.read_text(encoding="utf-8")
    cards = sum(1 for h in H2.findall(txt) if is_card(h))
    return cards, len(M_SRC.findall(txt)), len(M_SUM.findall(txt)), len(M_ADD.findall(txt))


def expected_per_card(md: Path):
    """逐卡：这条卡片的切片里各出现过哪些标记（存在性，不是次数）。

    这是能抓住「引用块形态的 🧭 被整条漏掉」的判据：
    页面级 `sum > 0` 在那种情况下依然是绿的。
    """
    txt = md.read_text(encoding="utf-8")
    marks = [(m.start(), m.group(1)) for m in H2.finditer(txt)]
    out = []
    for i, (pos, title) in enumerate(marks):
        if not is_card(title):
            continue
        end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
        chunk = txt[pos:end]
        out.append({
            "src": bool(M_SRC.search(chunk)),
            "sum": bool(M_SUM.search(chunk)),
            "add": bool(M_ADD.search(chunk)),
        })
    return out


MARK_ANY = re.compile(r"^[>\s]*(?:📖|🧭|➕)", re.M)


def expected_loose(md: Path):
    """卡之外（非卡 h2 小节里）还压着多少带标记的段落。

    解构的「篇N」、AI Prompt 的「§A 附录」、Vibe 的「导读·」都属于这一类，
    它们不是卡，但内容必须同样拿到证据签名。
    """
    txt = md.read_text(encoding="utf-8")
    marks = list(H2.finditer(txt))
    n = 0
    for i, m in enumerate(marks):
        if is_card(m.group(1)):
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(txt)
        n += len(MARK_ANY.findall(txt[m.start():end]))
    return n


def card_head_sections(md: Path):
    """返回所有「非卡 h2 出现在两张卡之间」的小节标题。
    出现这种形态时 restructure 的切片会把下一个非卡 h2 卷进上一张卡。"""
    txt = md.read_text(encoding="utf-8")
    titles = [m.group(1) for m in H2.finditer(txt)]
    bad = []
    seen_card = False
    for t in titles:
        if is_card(t):
            seen_card = True
        elif seen_card:
            bad.append(t)
    return bad


def sample_modules():
    """每本书取 1 个卡片最多的模块页，外加首页 / 速查表 / 档案页"""
    picks = {}
    for book in os.listdir(ROOT):
        bdir = ROOT / book
        try:
            subs = os.listdir(bdir)
        except OSError:
            continue
        best = None
        for sub in subs:
            if not sub[:2].isdigit():
                continue
            f = bdir / sub / "README.md"
            if not f.exists():
                continue
            n = expected(f)[0]
            if best is None or n > best[0]:
                best = (n, f)
        if best and best[0] >= 2:
            picks[book] = best[1]
    return picks


JS_PROBE = r"""
() => {
  // 与 evidence.js 同源的四条定位符，用于独立复核右栏改写有没有漏
  const ID_RX = [/^Q(\d+)-(\d+)[\s\u3000]/, /^§\s*(\d+)/,
                 /^Q(\d+)[\s\u3000]/, /[（(]\s*第\s*(\d+)\s*章\s*[）)]/];
  const hasId = t => ID_RX.some(r => r.test(t));

  // 诚实性不变量：原文带里除标签外，只能出现引用块，不能出现编者白话段落
  const srcViolations = [];
  for (const lane of document.querySelectorAll('.rd-ev--src')) {
    for (const child of lane.children) {
      if (child.classList.contains('rd-ev-label')) continue;
      if (child.tagName === 'P') srcViolations.push(child.textContent.slice(0, 60));
    }
  }

  // 结构化判据：带**之外**若还有以标记开头的节点，说明分带漏了。
  // （旧判据只查带内的段首残留，抓不到「整块留在带外」这个形态。）
  const stranded = [...document.querySelectorAll('.md-typeset p, .md-typeset blockquote')]
    .filter(n => !n.closest('.rd-ev'))
    .filter(n => /^[📖🧭➕]/.test(n.textContent.trim()))
    .map(n => n.tagName + ':' + n.textContent.trim().slice(0, 40));

  const unstripped = [...document.querySelectorAll('.rd-ev p')]
    .filter(p => /^[📖🧭➕]/.test(p.textContent.trim()))
    .map(p => p.textContent.slice(0, 40));

  // 空壳带：只有标签没有内容 —— 意味着第一块证据掉队了
  const emptyLanes = [...document.querySelectorAll('.rd-ev')]
    .filter(l => l.children.length <= 1).length;

  // 逐卡存在的带（只看直接子级，带里的嵌套不算）
  const perCard = [...document.querySelectorAll('.rd-card')].map(c => ({
    src: c.querySelectorAll(':scope > .rd-ev--src').length,
    sum: c.querySelectorAll(':scope > .rd-ev--sum').length,
    add: c.querySelectorAll(':scope > .rd-ev--add').length,
  }));

  // 右栏有两份 DOM 实例（桌面 + 移动抽屉），必须逐份核
  const toc = [...document.querySelectorAll('.md-nav--secondary')].map(nav => {
    const links = [...nav.querySelectorAll('ul[data-md-component="toc"] > li > a.md-nav__link')];
    return {
      links: links.length,
      ids: nav.querySelectorAll('.rd-toc-id').length,
      missed: links.filter(a => !a.querySelector('.rd-toc-id')
        && hasId((a.textContent || '').replace(/\s+/g, ' ').trim())).length,
    };
  });

  const headSticky = getComputedStyle(document.querySelector('.md-typeset thead th') || document.body).position;

  return {
    cards: document.querySelectorAll('.rd-card').length,
    chips: document.querySelectorAll('.rd-card-head .rd-chip').length,
    loose: document.querySelectorAll('.rd-ev-loose .rd-ev').length,
    src: document.querySelectorAll('.rd-ev--src').length,
    sum: document.querySelectorAll('.rd-ev--sum').length,
    add: document.querySelectorAll('.rd-ev--add').length,
    strip: document.querySelectorAll('.rd-idstrip').length,
    srcViolations, stranded, unstripped, emptyLanes, perCard, toc, headSticky,
    serifOk: (() => {
      const p = document.querySelector('.rd-ev--src p, .rd-ev--src blockquote p');
      if (!p) return null;
      return getComputedStyle(p).fontFamily;
    })(),
    // 证据带自带书脊，里面若还挂着 Material 默认的灰引用边框就是双竖线，
    // 且「灰色」混进了三级证据的配色。这条量的是计算值，不是肉眼看图。
    innerBorder: (() => {
      const bq = document.querySelector('.rd-ev blockquote');
      return bq ? getComputedStyle(bq).borderLeftWidth : 'none';
    })(),
    // 在**真实渲染里**量对比度。静态读 CSS 算不出来：继承、透明度、
    // 祖先背景都会改变读者实际看到的颜色。以前浅色下
    // --rd-ink-faint 在 sunken 底上只有 2.88:1，肉眼只当"有点淡"。
    contrast: (() => {
      const lum = (rgb) => {
        const m = rgb.match(/[\d.]+/g).map(Number);
        const f = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(m[0]) + 0.7152 * f(m[1]) + 0.0722 * f(m[2]);
      };
      const ratio = (a, b) => {
        const la = lum(a), lb = lum(b);
        return Math.round(((Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05)) * 100) / 100;
      };
      const probe = (sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        let bg = null, n = el;
        while (n) {
          const c = getComputedStyle(n).backgroundColor;
          if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') { bg = c; break; }
          n = n.parentElement;
        }
        if (!bg) bg = getComputedStyle(document.body).backgroundColor;
        return ratio(getComputedStyle(el).color, bg);
      };
      return {
        meta: probe('.rd-card-meta'),
        srcInfo: probe('.rd-card-head .rd-src'),
        label: probe('.rd-ev-label'),
        addBody: probe('.rd-ev--add p'),
        banner: probe('.rd-archive-banner'),
      };
    })(),
  };
}
"""

def url_for(rel_md: Path):
    """md 路径 → 站点 URL。use_directory_urls 下 README.md 映射到目录本身，
    必须把尾部的 README 段一起去掉，否则会请求 .../README/ 这种不存在的路径。"""
    parts = rel_md.as_posix()[:-3].split("/")
    if parts[-1] == "README":
        parts.pop()
    return BASE + "/".join(urllib.parse.quote(p) for p in parts) + "/"


fails, checks = [], 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    # http.server 不发 Cache-Control，Chromium 会启发式缓存 evidence.js，
    # 改完代码重跑会拿到旧文件。给这两个资源打时间戳穿透缓存。
    stamp = str(int(time.time()))
    for pat in ("evidence.js", "extra.css"):
        pg.route("**/" + pat, lambda r: r.continue_(url=r.request.url + "?v=" + stamp))
    base = "http://127.0.0.1:8766/"
    picks = sorted(sample_modules().items())
    idx = 0

    for book, md in picks:
        url = url_for(md.relative_to(ROOT))
        pg.goto(url)
        pg.wait_for_timeout(900)
        got = pg.evaluate(JS_PROBE)
        exp_cards, exp_src, exp_sum, exp_add = expected(md)
        want = expected_per_card(md)

        tag = f"[{book}]"
        if pg.url.rstrip("/") != url.rstrip("/"):
            fails.append(f"{tag} URL 被重定向到 {pg.url}")
        check(got["cards"] == exp_cards, f"{tag} 卡片数 {got['cards']} != 期望 {exp_cards}")
        check(got["chips"] == exp_cards, f"{tag} chip 数 {got['chips']} != {exp_cards}")
        # 一张卡可能有多条 📖，所以 src 车道数 <= 原文块数；反之必须 > 0
        check(got["src"] > 0, f"{tag} 没有任何原文带")
        check(got["src"] <= exp_src, f"{tag} 原文带数 {got['src']} > 原文块数 {exp_src}")
        check(got["emptyLanes"] == 0, f"{tag} 有 {got['emptyLanes']} 条空壳证据带（只有标签没内容）")
        check(not got["srcViolations"], f"{tag} 原文带混入了编者段落: {got['srcViolations'][:2]}")
        check(not got["stranded"], f"{tag} 带外残留带标记的节点: {got['stranded'][:2]}")
        check(not got["unstripped"], f"{tag} 段首标记未摘净: {got['unstripped'][:2]}")

        # 逐卡对账：md 切片里有哪种标记，卡里就得有哪种带；反向也要成立
        if len(got["perCard"]) == len(want):
            for n, (g, w) in enumerate(zip(got["perCard"], want), 1):
                for kind in ("src", "sum", "add"):
                    check(bool(g[kind]) == w[kind],
                          f"{tag} 第{n}卡 {kind}：md 有={w[kind]}，渲染出 {g[kind]} 条带")
        else:
            check(False, f"{tag} 逐卡对账长度不符 DOM={len(got['perCard'])} md={len(want)}")

        # 右栏两份实例逐份核：漏改的必须是 0，每张卡在每份里各一条
        check(len(got["toc"]) >= 1, f"{tag} 右栏目录实例数 {len(got['toc'])}")
        for n, t in enumerate(got["toc"]):
            check(t["missed"] == 0, f"{tag} 右栏#{n} 有 {t['missed']} 条带卡号却未改写")
            check(t["ids"] == exp_cards,
                  f"{tag} 右栏#{n} 卡号条目 {t['ids']} != 卡片数 {exp_cards}")
        check(got["strip"] == 1, f"{tag} 卡号横条 {got['strip']} 个")
        check(got["innerBorder"] in ("none", "0px"),
              f"{tag} 证据带内的引用块还挂着默认灰边框 {got['innerBorder']}（双竖线）")
        check(got["serifOk"] is not None and "Serif" in got["serifOk"],
              f"{tag} 原文带衬线族={got['serifOk']}，@font-face 可能没生效")

        # 对比度：正文级前景 ≥4.5:1（WCAG AA）。这些是量出来的实测值，
        # 不是从 CSS 里抄的令牌——渲染后的颜色才是读者看到的事实。
        for key, label in (("meta", "卡片元信息"), ("srcInfo", "卡片来源"),
                           ("addBody", "➕补充带正文")):
            v = got["contrast"].get(key)
            if v is not None:
                check(v >= 4.5, f"{tag} {label}对比度 {v}:1 < 4.5:1")
        lab = got["contrast"].get("label")
        if lab is not None:
            check(lab >= 4.5, f"{tag} 证据带标签对比度 {lab}:1 < 4.5:1")

        # 卡外证据：md 里非卡小节还压着标记，页面上就必须有对应的带外证据带
        loose_md = expected_loose(md)
        if loose_md:
            check(got["loose"] > 0,
                  f"{tag} 卡外有 {loose_md} 段带标记证据，但页面上 0 条带外证据带")
        # 非卡 h2 夹在两张卡之间时，切片会把它卷进上一张卡
        mid = card_head_sections(md)
        check(not mid, f"{tag} 非卡小节夹在卡之间，切片会吞掉: {mid}")

        idx += 1

    # 浅色：卡片 / 速查表 / 索引 / 档案 / 首页
    # （上面循环结束时页面停在最后一本书上，这里要自己跳回样本页）
    book, md = picks[0]
    url = url_for(md.relative_to(ROOT))
    pg.goto(url)
    pg.wait_for_function(
        "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'")
    pg.wait_for_timeout(250)
    pg.screenshot(path=str(SHOT / "desktop-card-light.png"), full_page=False)

    book_dir = md.parent.parent
    lk = book_dir / "99-速查表.md"
    for name, out in (("99-速查表", "desktop-lookup.png"), ("INDEX", "desktop-index.png")):
        f = book_dir / f"{name}.md"
        if not f.exists():
            continue
        pg.goto(url_for(f.relative_to(ROOT)))
        pg.wait_for_function(
            "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'")
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(SHOT / out), full_page=False)
        if out == "desktop-lookup.png":
            r = pg.evaluate(JS_PROBE)
            check(r["headSticky"] == "sticky", f"[速查表] 表头 position={r['headSticky']}，不是 sticky")

    ft = sorted(book_dir.glob("00-*/fulltext/*.md"))[0]
    pg.goto(url_for(ft.relative_to(ROOT)))
    pg.wait_for_timeout(700)
    pg.screenshot(path=str(SHOT / "desktop-archive.png"), full_page=False)
    check(pg.locator(".rd-archive-banner").count() == 1, "[档案页] 缺档案横幅")
    ab = pg.evaluate(JS_PROBE)["contrast"]["banner"]
    check(ab is None or ab >= 4.5, f"[档案页] 档案横幅对比度 {ab}:1 < 4.5:1")

    pg.goto(base)
    pg.wait_for_timeout(800)
    pg.screenshot(path=str(SHOT / "desktop-home.png"), full_page=False)
    lit = pg.evaluate("() => document.body.innerText.includes(':material-')")
    check(not lit, "[首页] 仍存在未渲染的 :material- 图标简写")

    # 深色：必须走 Material 真实的 palette 切换（点那个 radio），
    # 直接 setAttribute 改 <html> 是无效的——配色实际挂在 <body> 上。
    # 改错元素的后果是「截了个名字叫 dark 的浅色图」，看起来毫无异常。
    pg.goto(url)
    pg.wait_for_function(
        "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'")
    pg.eval_on_selector("input#__palette_1", "el => el.click()")
    pg.wait_for_timeout(600)
    scheme = pg.evaluate("() => document.body.getAttribute('data-md-color-scheme')")
    check(scheme == "slate", f"[深色] body 的 data-md-color-scheme={scheme}，没切过去")
    hdr = pg.evaluate("() => getComputedStyle(document.querySelector('.md-header')).backgroundColor")
    check(hdr.startswith("rgb(1"), f"[深色] 顶栏背景 {hdr}，没有跟随配色方案")
    pg.screenshot(path=str(SHOT / "desktop-card-dark.png"), full_page=False)
    if lk.exists():
        pg.goto(url_for(lk.relative_to(ROOT)))
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(SHOT / "desktop-lookup-dark.png"), full_page=False)

    # 移动端
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
    for pat in ("evidence.js", "extra.css"):
        m.route("**/" + pat, lambda r: r.continue_(url=r.request.url + "?v=" + stamp))
    m.goto(url)
    m.wait_for_timeout(900)
    m.screenshot(path=str(SHOT / "mobile-card.png"))
    lk = book_dir / "99-速查表.md"
    if lk.exists():
        m.goto(url_for(lk.relative_to(ROOT)))
        m.wait_for_timeout(800)
        m.screenshot(path=str(SHOT / "mobile-lookup.png"))
    b.close()

print(f"断言 {checks} 条，失败 {len(fails)} 条")
for f in fails:
    print("  FAIL", f)