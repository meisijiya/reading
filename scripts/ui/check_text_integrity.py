"""门禁 3/3：文本守恒 / 出处谎报 / 编号真伪（攻击测试）。

与 check_evidence.py 刻意**不重叠**。那个脚本只问「标记有没有摘干净」，
从不问相反的方向——stripLeading() 按码元个数跨文本节点盲摘，切点算错
就会把正文字一起吃掉，而这种事故在「标记摘干净了」的前提下完全不可见。

这里换三个角度从源 md 独立对账：
  1. 每条证据的**正文字首**是否仍能在页面上找到（防误吃正文）
  2. 证据最终落在哪条带，是否与它自己的标记一致（防出处谎报）
  3. chip 里的卡号是否逐个等于书自己的编号（防合成假卡号）

用法（必须从仓库根运行）：
    python -m mkdocs build --strict
    python -m http.server 8766 --bind 127.0.0.1 --directory site
    python scripts/ui/check_text_integrity.py
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
# 证据前缀：📖/🧭/➕ + 可选的 **加粗** + 名字 + 可选（全/半角）定位符 + 分隔符
PREFIX = re.compile(
    r"^[>\s]*(?:📖|🧭|➕)\s*(?:\*\*)?\s*[^（(:：\n]{0,12}?\**\s*"
    r"(?:[（(][^）)]*[）)])?\s*[：:]",
    re.M)
MD_NOISE = re.compile(r"[*`>\[\]]+")


def norm(s):
    return MD_NOISE.sub("", s).replace("\u3000", " ").strip()


def squeeze(s):
    """把 md 与页面两侧都压成「连续无空白无管道」的串再比。

    第一版直接拿 md 的原始 40 字去页面里找，表格行必然找不到——md 侧是
    `| 层次 | 表达 |`，页面侧是两个分开的单元格，没有管道也没有换行。
    这种「判别器抓不住它该抓的东西」比判别器红更糟：它会让人以为
    内容丢了。
    """
    return re.sub(r"[\s|`*>#\-\[\]()]+", "", s)


def samples(md: Path):
    """从 md 抽 (标记类型, 卡片标题, 正文字首样本)。

    三个坑，都是这次真踩到的：
      1. 样本必须只取**同一行**。跨行取值会把下一条证据的前缀也拼进来，
         拼出「这里有三个关键细节：📖原文c」这种页面上根本不存在的字符串。
      2. 前缀后正文为空的条目（`> 📖 原文（§2.2.3）：这里有三个关键细节：`
         冒号后本行就没了）单独计数，不混进「丢失」——那是源数据的事实，
         不是渲染把它吃掉了。
      3. `[^\n]{0,24}?` 必须在括号后停下来，否则会在正文里的第一个冒号切点。
    """
    txt = md.read_text(encoding="utf-8")
    heads = [(m.start(), m.group(1)) for m in H2.finditer(txt)]
    out, empty = [], 0
    for i, (pos, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(txt)
        chunk = txt[pos:end]
        for m in re.finditer(r"^[>\s]*(📖|🧭|➕)[^\n]{0,24}?[：:]", chunk, re.M):
            line = chunk[m.end():].split("\n")[0]
            body = squeeze(line)[:14]
            if len(body) < 8:
                empty += 1
                continue
            out.append({"kind": m.group(1), "card": title.strip()[:28], "head": body})
    return out, empty


def locators_in(md: Path):
    """每个 📖 前缀后面跟的定位符，按出现顺序。用于核对标签是否如实。"""
    txt = md.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^[>\s]*📖[^\n（(:：]{0,12}\**\s*[（(]([^）)]*)[）)]", txt, re.M):
        out.append(m.group(1).strip())
    return out


def url_for(rel_md: Path):
    parts = rel_md.as_posix()[:-3].split("/")
    if parts[-1] == "README":
        parts.pop()
    return BASE + "/".join(urllib.parse.quote(p) for p in parts) + "/"


def walk():
    """安全枚举 书/NN-模块/README.md（AI Engineering 是断链 junction）"""
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
            if f.exists() and len(H2.findall(f.read_text(encoding="utf-8"))) >= 2:
                yield book, f


DUMP = r"""() => {
  const squeeze = s => s.replace(/[\s|`*>#\-\[\]()]+/g, '');
  const lanes = [...document.querySelectorAll('.rd-ev')].map(lane => ({
    kind: lane.className.includes('rd-ev--src') ? '📖'
         : lane.className.includes('rd-ev--sum') ? '🧭' : '➕',
    label: lane.querySelector('.rd-ev-label')?.textContent.trim() || '',
    text: squeeze(lane.textContent),
  }));
  const chips = [...document.querySelectorAll('.rd-card-head .rd-chip')].map(c => c.textContent.trim());
  return { lanes, chips, all: squeeze(document.querySelector('.md-typeset').textContent) };
}"""

checked = eaten = 0
empty_md = 0
bad = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    stamp = str(int(time.time()))
    for pat in ("evidence.js", "extra.css"):
        pg.route("**/" + pat, lambda r: r.continue_(url=r.request.url + "?v=" + stamp))

    for book, md in walk():
        pg.goto(url_for(md.relative_to(ROOT)))
        pg.wait_for_function(
            "() => document.querySelector('.md-typeset')?.dataset.rdDone === '1'", timeout=15000)
        got = pg.evaluate(DUMP)
        smp, empt = samples(md)
        empty_md += empt

        # --- 攻击 1：正文字首有没有被吃掉 ---
        # 对**全文**做存在性判断：只要内容还在页面上就没丢。
        # 顺手再判一次「它落在哪条带里」——若标记类型和所在带不一致，
        # 那就是出处谎报，比丢字更严重。
        for s in smp:
            checked += 1
            probe20 = s["head"][:20]
            if probe20 not in got["all"]:
                eaten += 1
                bad.append(f"[{book}] 正文开头丢了: md='{s['head'][:34]}'")
            else:
                # 归属核对：这条证据最终落在哪条带，必须和它自己的标记一致。
                # 第一版只问「是不是落在非原文带」，于是 🧭 样本落进 🧭 带
                # 也被判成问题——那是判别器在问错问题。
                owners = {ln["kind"] for ln in got["lanes"] if s["head"] in ln["text"]}
                if owners and s["kind"] not in owners:
                    bad.append(f"[{book}] {s['kind']} 证据落进了 {sorted(owners)} 带")

        # --- 攻击 2：定位符是否被谎报 ---
        for loc in set(locators_in(md)):
            want = norm(loc)[:12]
            if not any(want in norm(ln["label"]) for ln in got["lanes"]):
                bad.append(f"[{book}] 定位符「{loc}」在页面上找不到对应标签")

        # --- 攻击 3：chip 是不是书自己的编号 ---
        src = md.read_text(encoding="utf-8")
        ids = []
        for m in H2.finditer(src):
            t = m.group(1)
            for pat, f in ((r"^Q(\d+)-(\d+)[\s\u3000]", lambda g: f"Q{g[1]}-{g[2]}"),
                           (r"^§\s*(\d+)", lambda g: f"§{g[1]}"),
                           (r"^Q(\d+)[\s\u3000]", lambda g: f"Q{g[1]}"),
                           (r"[（(]\s*第\s*(\d+)\s*章\s*[）)]", lambda g: f"第{g[1]}章")):
                mm = re.search(pat, t)
                if mm:
                    ids.append(f(mm))
                    break
        # --- 攻击 3：chip 是不是书自己的编号 ---
        # 只有 ≥2 张卡才会做卡片化；单卡页不动是既定设计，不算不一致。
        if len(ids) >= 2:
            if ids != got["chips"]:
                bad.append(f"[{book}] chip 与 md 编号不一致\n      md  ={ids[:8]}\n      页面={got['chips'][:8]}")
    b.close()

print(f"正文开头样本核对 {checked} 条，丢失 {eaten} 条")
print(f"源 md 里前缀后正文为空的证据条：{empty_md} 条（页面同样为空，非渲染丢失）")
print(f"问题 {len(bad)} 条")
for x in bad[:25]:
    print("  FAIL", x)