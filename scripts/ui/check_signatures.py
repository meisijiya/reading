"""门禁 4/4：视觉签名是否还成立。

结构有三条门禁守着，**视觉签名却没有**——那正是这个改动的全部意义。
三条签名各自用颜色 / 字族 / 边线三重编码（不依赖颜色单通道）：

  📖 原文 = 衬线 + 朱色实心书脊 + 淡朱底
  🧭 归纳 = 黑体 + 青色虚线 + 无底色
  ➕ 补充 = 更小更淡 + 灰色点线 + 缩进更深

任一条被后续的 CSS 改动破坏（换配色、删 local() 字体栈、把边线改成
虚线统一……），前三条门禁**全绿**——它们只管结构。所以单列这一条。

量的是渲染后的 computed style，不是 CSS 里写的字面值。

用法（必须从仓库根运行）：
    python -m mkdocs build --strict
    python -m http.server 8766 --bind 127.0.0.1 --directory site
    python scripts/ui/check_signatures.py
    # 换预览地址：RD_SITE=http://127.0.0.1:8767/ python scripts/ui/check_signatures.py
"""
import os
import sys
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("docs")
# 预览地址可覆盖：模拟 CI 时用 git worktree 在另一个端口起服务。
# 用法：RD_SITE=http://127.0.0.1:8767/ python scripts/ui/<本脚本>
BASE = os.environ.get("RD_SITE", "http://127.0.0.1:8766/")

PROBE = r"""() => {
  const cs = (sel, prop) => {
    const el = document.querySelector(sel);
    return el ? getComputedStyle(el)[prop] : null;
  };
  const rgbOf = v => v ? v.replace(/rgba?\(([^)]+)\)/, '$1').split(',').map(x => x.trim()).join(',') : null;
  return {
    // 📖 原文：衬线族 + 朱色实心左脊 + 有淡朱底
    srcFamily: cs('.rd-ev--src p', 'fontFamily'),
    srcBorderStyle: cs('.rd-ev--src', 'borderLeftStyle'),
    srcBorderColor: rgbOf(cs('.rd-ev--src', 'borderLeftColor')),
    srcBorderWidth: cs('.rd-ev--src', 'borderLeftWidth'),
    srcBackground: rgbOf(cs('.rd-ev--src', 'backgroundColor')),
    srcLabelColor: rgbOf(cs('.rd-ev--src .rd-ev-label', 'color')),
    // 🧭 归纳：黑体（无衬线）+ 青色虚线 + 透明底
    sumFamily: cs('.rd-ev--sum p', 'fontFamily'),
    sumBorderStyle: cs('.rd-ev--sum', 'borderLeftStyle'),
    sumBorderColor: rgbOf(cs('.rd-ev--sum', 'borderLeftColor')),
    sumBackground: rgbOf(cs('.rd-ev--sum', 'backgroundColor')),
    // ➕ 补充：更小 + 灰点线
    addFamily: cs('.rd-ev--add p', 'fontFamily'),
    addFontSize: cs('.rd-ev--add p', 'fontSize'),
    addBorderStyle: cs('.rd-ev--add', 'borderLeftStyle'),
    addBorderColor: rgbOf(cs('.rd-ev--add', 'borderLeftColor')),
    // 摘要带正文与原文带正文的字号差（补充应更小）
    srcFontSize: cs('.rd-ev--src p', 'fontSize'),
    // 带内不得残留默认灰引用边框（朱色书脊之外多一根竖线）
    innerBorder: cs('.rd-ev blockquote', 'borderLeftWidth'),
    innerPadding: cs('.rd-ev blockquote', 'paddingLeft'),
    counts: {
      src: document.querySelectorAll('.rd-ev--src').length,
      sum: document.querySelectorAll('.rd-ev--sum').length,
      add: document.querySelectorAll('.rd-ev--add').length,
    },
  };
}"""


def find_readme(tail):
    """安全定位 <书>/<模块>/README.md。

    docs/AI Engineering (Chip Huyen) 是指向不存在路径的断链 junction，
    任何递归遍历（Path.rglob/glob）都在遍历阶段抛 FileNotFoundError，
    try/except 救不回来——只能用 os.scandir 逐层下钻。
    """
    cur = ROOT
    for part in tail.split("/"):
        for e in os.scandir(cur):
            if e.name == part:
                cur = Path(e.path)
                break
        else:
            raise SystemExit("找不到目录段: " + part)
    return cur / "README.md"


def url_for(rel_md: Path):
    parts = rel_md.as_posix()[:-3].split("/")
    if parts[-1] == "README":
        parts.pop()
    return BASE + "/".join(urllib.parse.quote(p) for p in parts) + "/"


# 取每本书卡片最多的模块页，每本书都要验到
def sample_pages():
    import re
    H2 = re.compile(r"^##\s+(.*)$", re.M)
    IDS = [re.compile(r"^Q\d+-\d+[\s　]"), re.compile(r"^§\s*\d+"),
           re.compile(r"^Q\d+[\s　]"), re.compile(r"[（(]\s*第\s*\d+\s*章\s*[）)]")]
    out = []
    skipped = []
    for book in sorted(os.listdir(ROOT)):
        bdir = ROOT / book
        # 这里**不能**静默跳过断链：一旦静默，「每本书都验到」这句话就比实际
        # 覆盖更宽，而门禁照样打印一行漂亮的「9 本」。当前已知的跳过项：
        # docs/AI Engineering (Chip Huyen) 是指向仓库根下一个不存在目录的
        # junction —— git 未跟踪其中任何文件、site/ 里也没有产物，跳过它是对的；
        # 但「对的」必须留痕，不能靠沉默。
        if not bdir.exists():
            skipped.append((book, "断链或不可访问（指向不存在的路径）"))
            continue
        if not bdir.is_dir():
            continue        # index.md、assets/ 这类，不是书，不必刷屏
        subs = sorted(os.listdir(bdir))
        best = None
        for sub in subs:
            if not sub[:2].isdigit():
                continue
            f = bdir / sub / "README.md"
            if not f.exists():
                continue
            n = sum(1 for h in H2.findall(f.read_text(encoding="utf-8"))
                    if any(p.search(h) for p in IDS))
            if best is None or n > best[0]:
                best = (n, f)
        if best and best[0] >= 2:
            out.append((book, best[1]))
        elif best:
            # 同样是静默通过的形状：有书目录、有模块 README，却一张卡都对不上，
            # 结果一个都不取样。记下来，别让「覆盖面」只剩一个好看的数字。
            skipped.append((book, f"无卡片型 H2（最多命中 {best[0]} 个）"))
    return out, skipped


pages, skipped = sample_pages()
print(f"待验模块页 {len(pages)} 个 × 浅深两套配色")
for book, why in skipped:
    print(f"  未纳入取样（不计入覆盖）：{book} —— {why}")


fails, checks = [], 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ("default", "slate"):
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        for book, md in pages:
            pg.goto(url_for(md.relative_to(ROOT)))
            pg.wait_for_function(
                "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'", timeout=15000)
            if scheme == "slate":
                pg.eval_on_selector("input#__palette_1", "el => el.click()")
                pg.wait_for_timeout(400)
            g = pg.evaluate(PROBE)
            tag = f"[{scheme}/{book[:14]}]"

            if g["counts"]["src"] == 0:
                check(False, f"{tag} 页面没有原文带，签名无从验证")
                continue

            # 📖 衬线 + 朱色实心书脊
            check(g["srcFamily"] and "Serif" in g["srcFamily"],
                  f"{tag} 原文带字族={g['srcFamily']}，衬线签名失效")
            check(g["srcBorderStyle"] == "solid",
                  f"{tag} 原文带左脊 style={g['srcBorderStyle']}，应为 solid")
            check(g["srcLabelColor"] and g["srcLabelColor"] == g["srcBorderColor"],
                  f"{tag} 原文带标签色 {g['srcLabelColor']} ≠ 书脊色 {g['srcBorderColor']}")
            check(g["srcBackground"] not in (None, "rgba(0,0,0,0)", "0,0,0,0"),
                  f"{tag} 原文带没有淡朱底（background={g['srcBackground']}）")

            # 🧭 无衬线 + 青色虚线 + 无底色（黑体是这条签名的另一半）
            if g["counts"]["sum"]:
                check(g["sumFamily"] and "Serif" not in g["sumFamily"],
                      f"{tag} 归纳带字族={g['sumFamily']}，不该用衬线（会和原文撞签名）")
                check(g["sumBorderStyle"] == "dashed",
                      f"{tag} 归纳带左脊 style={g['sumBorderStyle']}，应为 dashed")
                check(g["sumBorderColor"] and g["sumBorderColor"] != g["srcBorderColor"],
                      f"{tag} 归纳带与原文带同色 {g['sumBorderColor']}，两级签名撞车")
                check(g["sumBackground"] in (None, "rgba(0,0,0,0)", "0,0,0,0"),
                      f"{tag} 归纳带有底色 {g['sumBackground']}，设计是无底色")

            # ➕ 补充：更小 + 点线
            if g["counts"]["add"]:
                check(g["addFontSize"] and g["srcFontSize"]
                      and float(g["addFontSize"][:-2]) < float(g["srcFontSize"][:-2]),
                      f"{tag} 补充带字号 {g['addFontSize']} 未小于原文带 {g['srcFontSize']}")
                check(g["addBorderStyle"] == "dotted",
                      f"{tag} 补充带左脊 style={g['addBorderStyle']}，应为 dotted")
                check(g["addBorderColor"] != g["srcBorderColor"]
                      and g["addBorderColor"] != g["sumBorderColor"],
                      f"{tag} 补充带与其它级同色 {g['addBorderColor']}")

            # 三重编码的第三重：带内不得再挂默认灰引用边框
            check(g["innerBorder"] in (None, "0px"),
                  f"{tag} 证据带内还有引用边框 {g['innerBorder']}，出现双竖线")
        pg.close()
    b.close()

print(f"签名断言 {checks} 条，失败 {len(fails)} 条")
for f in fails[:30]:
    print("  FAIL", f)