#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_local_links.py — 校验 mkdocs 构建产物里的站内链接是否都指向真实文件。

scripts/check_site_links.py 是对**已部署站点**发 HTTP 请求（需先 push）。
本脚本对**本地 site/ 产物**做同样的事，不需要网络，可在 push 前跑。

规则：site/ 里的每个 href（排除外链、锚点、mailto、data:）都必须对应一个存在的
文件或目录。use_directory_urls=true 时 `a/b/` 对应 `site/a/b/index.html`。

Usage:
  python scripts/check_local_links.py [site_dir]
"""
import sys, io, os, re, glob
from urllib.parse import unquote, urlparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SITE = sys.argv[1] if len(sys.argv) > 1 else r"D:\26code\read\site"

HREF = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')
SKIP = ("http://", "https://", "mailto:", "data:", "javascript:", "//", "#")

# 站点挂在子路径下（如 /reading/），产物里的绝对 href 带这个前缀
BASE_PATH = "/reading/"


def resolve(src_dir, raw):
    """把 href 解析成本地文件路径；解析不出来返回 None。"""
    target = unquote(urlparse(raw).path)
    if not target:
        return None
    if target.startswith(BASE_PATH):
        # 站点根绝对路径：从 site/ 根解析
        p = os.path.join(SITE, target[len(BASE_PATH):].replace("/", os.sep))
    elif target.startswith("/"):
        return None          # 站点外的绝对路径，本地无对应物
    else:
        p = os.path.normpath(os.path.join(src_dir, target.replace("/", os.sep)))
    return p


def main():
    files = glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    if not files:
        print(f"[FAIL] {SITE} 下没有 html —— 先跑 mkdocs build")
        return 1

    ok = bad = skipped = 0
    fails = []
    for f in files:
        # 404 页的链接是部署后形态（站点根绝对路径），本地无法解析，不计入
        if os.path.basename(f) == "404.html":
            skipped += 1
            continue
        d = os.path.dirname(f)
        html = open(f, encoding="utf-8", errors="replace").read()
        for raw in HREF.findall(html):
            if raw.startswith(SKIP):
                continue
            p = resolve(d, raw)
            if p is None:
                continue
            if any(os.path.exists(c) for c in (p, os.path.join(p, "index.html"))):
                ok += 1
            else:
                bad += 1
                if len(fails) < 30:
                    fails.append((os.path.relpath(f, SITE), raw))

    print(f"扫描 {len(files) - skipped} 个 html（跳过 {skipped} 个 404）| "
          f"站内链接 OK={ok} FAIL={bad}")
    if fails:
        print("失败样例：")
        for src, raw in fails:
            print(f"  {src}  ->  {raw}")
    print("\n总判定：", "PASS" if bad == 0 else "FAIL")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())