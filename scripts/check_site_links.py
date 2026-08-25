#!/usr/bin/env python3
"""
规则五自检脚本:验证 mkdocs build 产物 site/ 内所有被引用的内部 URL 都返回 200。

用法:
    mkdocs build --strict
    python3 scripts/check_site_links.py [ROOT_URL]

ROOT_URL 默认 https://meisijiya.site/reading (线上);可传 http://127.0.0.1:8765/ 做本地预览检查。

退出码:
    0 = 全部 200/304
    1 = 有 FAIL (脚本同时打印失败清单)
"""
import os
import re
import sys
import urllib.parse
import subprocess

ROOT_URL = sys.argv[1] if len(sys.argv) > 1 else "https://meisijiya.site/reading"
BASE = "site"
host_re = re.compile(r'^https?://')

urls = set()
for root, _, files in os.walk(BASE):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        page_dir = os.path.dirname(path)
        for m in re.finditer(r'href="[^"#][^"]*"|src="[^"#][^"]*"', html):
            ref = m.group(0)
            if ref.startswith('href='):
                ref = ref[6:-1]
            else:
                ref = ref[5:-1]
            if host_re.match(ref) or ref.startswith('mailto:'):
                continue
            target_fs = os.path.normpath(os.path.join(page_dir, urllib.parse.unquote(ref)))
            if not target_fs.startswith(BASE + os.sep) and target_fs != BASE:
                continue
            url_path = '/' + os.path.relpath(target_fs, BASE).replace(os.sep, '/')
            if url_path.endswith('/index.html'):
                url_path = url_path[:-len('/index.html')] + '/'
            elif not url_path.endswith('/') and os.path.isdir(target_fs):
                url_path += '/'
            encoded = '/'.join(urllib.parse.quote(s, safe='') for s in url_path.split('/'))
            urls.add(ROOT_URL.rstrip('/') + encoded)

ok = fail = 0
fails = []
import urllib.request
HEADERS = {"User-Agent": "Mozilla/5.0 check_site_links"}
for u in sorted(urls):
    code = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(u, method='HEAD', headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                code = r.status
            break
        except urllib.error.HTTPError as e:
            code = e.code
            break
        except Exception:
            if attempt == 2:
                code = "ERR:URLError"
    if code in (200, 304):
        ok += 1
    else:
        fail += 1
        fails.append((code, u))

print(f"URL={ROOT_URL}  base={BASE}  total={len(urls)}  OK={ok}  FAIL={fail}")
for code, u in fails:
    print(f"  FAIL {code}: {u}")

sys.exit(0 if fail == 0 else 1)