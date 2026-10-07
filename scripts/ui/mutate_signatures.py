"""证伪视觉签名门禁：逐个破坏签名维度，确认对应判据真的会红。

判别器写完不等于判别器有效。本次要证明 8 类判据各自能抓住自己的破坏：

  M1 归纳带左脊 dashed -> solid      抓「虚线签名」
  M2 原文带字族 -> sans              抓「衬线签名」
  M3 归纳带加底色                    抓「无底色签名」
  M4 补充带字号改大                  抓「补充更小」
  M5 补充带点线 -> solid             抓「点线签名」
  M6 原文带去掉淡朱底                抓「有底色签名」
  M7 带内引用边框改回 4px            抓「无双竖线」
  M8 青色令牌改成朱色                抓「两级不撞车」

⚠️ 上一轮 M2/M4 报 SURVIVED 是 harness 自己的错，不是判别器的问题：
   ① `replace(old, new, 1)` 只换第一处，而 `var(--rd-serif)` 在 CSS 里有 3 处，
      改的是令牌定义/别处，不是 `.rd-ev--src p`；
   ② 把新声明「插在块首」，被块内原有的 font-size 覆盖，变异根本没生效。
   所以本版加了三条纪律：
   - 锚点必须唯一（count != 1 直接 SKIP 并报错，不静默跑一个没打中的变异）
   - 写盘后回读，断言「新的在、旧的没了」，落空即报 MUTATION-NOT-APPLIED
   - 报红时把命中的 FAIL 原文打出来——红的原因里必须能看到变异后的实测值
     （expect_value），而不是只看到「有红」。

全程结束后把 CSS 还原、复跑一次确认回到 0 失败，并校验字节级还原。
"""
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CSS = Path("docs/assets/stylesheets/extra.css")
BAK = CSS.with_suffix(".css.mutbak")

# (名称, 锚点, 变异后, 期望命中的判据关键词, 期望出现在红里的实测值)
MUTATIONS = [
    ("M1 归纳带左脊 dashed->solid",
     ".rd-ev--sum { border-left: 3px dashed var(--rd-verdigris); }",
     ".rd-ev--sum { border-left: 3px solid var(--rd-verdigris); }",
     "应为 dashed", "style=solid"),

    ("M2 原文带字族 -> sans",
     ".rd-ev--src p {\n  font-family: var(--rd-serif);",
     ".rd-ev--src p {\n  font-family: var(--rd-sans);",
     "衬线签名失效", None),   # 特殊：红里必须【不含】Serif

    ("M3 归纳带加底色",
     ".rd-ev--sum { border-left: 3px dashed var(--rd-verdigris); }",
     ".rd-ev--sum { border-left: 3px dashed var(--rd-verdigris); background: var(--rd-vermilion-wash); }",
     "设计是无底色", None),

    ("M4 补充带字号改大",
     ".rd-ev--add p {\n  font-size: .8rem;",
     ".rd-ev--add p {\n  font-size: 1.2rem;",
     "未小于原文带", None),   # 特殊：红里两处字号需现场解析比大小

    ("M5 补充带点线 -> solid",
     ".rd-ev--add {\n  border-left: 3px dotted var(--rd-ash);",
     ".rd-ev--add {\n  border-left: 3px solid var(--rd-ash);",
     "应为 dotted", "style=solid"),

    ("M6 原文带去掉淡朱底",
     ".rd-ev--src {\n  border-left-color: var(--rd-vermilion);\n  background: var(--rd-vermilion-wash);",
     ".rd-ev--src {\n  border-left-color: var(--rd-vermilion);\n  background: transparent;",
     "没有淡朱底", "background=0,0,0,0"),

    ("M7 带内引用边框改回 4px",
     ".md-typeset .rd-ev blockquote {\n  border-left: 0;",
     ".md-typeset .rd-ev blockquote {\n  border-left: 4px solid var(--rd-ink-faint);",
     "出现双竖线", "引用边框 4px"),

    ("M8 青色令牌改成朱色",
     "  --rd-verdigris: #2C6B66;",
     "  --rd-verdigris: #B23A2E;",
     "两级签名撞车", None),
]

RX_ADD_SIZE = re.compile(r"补充带字号 ([\d.]+)px 未小于原文带 ([\d.]+)px")


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr


def probe_holds(name, fail_line, expect_value):
    """红的原因里能不能看到变异后的实测值——否则红可能是别的红。"""
    if name.startswith("M2"):
        # 判据本身：字族里【不含】Serif
        m = re.search(r"原文带字族=(.*?)，衬线签名失效", fail_line)
        return (m is not None and "Serif" not in m.group(1),
                f"红里读到的字族={m.group(1) if m else '?'}（应不含 Serif）")
    if name.startswith("M3"):
        m = re.search(r"归纳带有底色 (.*?)，设计是无底色", fail_line)
        return (m is not None and m.group(1) not in ("None", "0,0,0,0"),
                f"红里读到的底色={m.group(1) if m else '?'}")
    if name.startswith("M4"):
        m = RX_ADD_SIZE.search(fail_line)
        if not m:
            return False, "红里没解析出两个字号"
        a, b = float(m.group(1)), float(m.group(2))
        return a >= b, f"红里读到的补充字号={a}px 原文字号={b}px（应不小于）"
    if name.startswith("M8"):
        return ("同色" in fail_line, f"红原文：{fail_line[:110]}")
    return (expect_value in fail_line, f"红里找 {expect_value!r}")


BAK.write_bytes(CSS.read_bytes())
src = CSS.read_text(encoding="utf-8")
results = []

try:
    for name, old, new, expect_key, expect_value in MUTATIONS:
        n = src.count(old)
        if n != 1:
            results.append((name, "ANCHOR-AMBIGUOUS",
                            f"锚点出现 {n} 处（必须唯一），变异没跑，拒绝把 harness 缺陷"
                            f"报成判别器 SURVIVED"))
            continue

        CSS.write_text(src.replace(old, new, 1), encoding="utf-8")

        # 落盘回读：变异必须真的写进去了
        now = CSS.read_text(encoding="utf-8")
        if now == src or old in now or new not in now:
            results.append((name, "MUTATION-NOT-APPLIED",
                            "写盘后回读发现 CSS 未按预期变化，跳过"))
            continue

        sh("python -m mkdocs build --strict")
        out = sh("python scripts/ui/check_signatures.py")
        fails = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
        hit = next((f for f in fails if expect_key in f), None)

        if not fails:
            verdict, detail = "SURVIVED", "门禁 0 失败 —— 判别器没抓住这个破坏"
        elif hit is None:
            verdict, detail = "WRONG-RED", f"红了但没红在期望判据上（共 {len(fails)} 条）"
        else:
            ok, why = probe_holds(name, hit, expect_value)
            verdict = "KILLED" if ok else "RED-BUT-WRONG-VALUE"
            detail = f"命中期望判据，{len(fails)} 条红｜{why}"

        results.append((name, verdict, detail))
        print(f"  [{verdict}] {name} :: {detail}", flush=True)
finally:
    CSS.write_bytes(BAK.read_bytes())
    BAK.unlink()

print("=" * 84)
ok_n = 0
for name, verdict, detail in results:
    flag = "OK " if verdict == "KILLED" else "!! "
    ok_n += verdict == "KILLED"
    print(f"{flag}{verdict:22s} {name}")
    print(f"                     {detail}")
print("=" * 84)
print(f"KILLED {ok_n}/{len(results)}")

# 还原校验：CSS 必须逐字回到变异前（src 是变异前读进来的那份）
print("CSS 已逐字还原" if CSS.read_text(encoding="utf-8") == src else "!! CSS 还原失败")

sh("python -m mkdocs build --strict")
back = sh("python scripts/ui/check_signatures.py")
line = [l for l in back.strip().splitlines() if l.strip()][-1] if back.strip() else ""
print("还原后复跑：", line)