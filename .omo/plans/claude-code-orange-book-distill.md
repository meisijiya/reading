---
slug: claude-code-orange-book-distill
status: awaiting-approval  # post-high-accuracy-review, awaiting execution approval
intent: clear
review_required: true
created: 2026-08-24
updated: 2026-08-24  # after high-accuracy review (momus + oracle) revisions
---

# Plan: claude-code-orange-book-distill

## Summary
本地 `book/` 目录下《Claude Code 橙皮书：AI 编程实战》(花叔) epub → 蒸馏成 `Claude Code橙皮书：AI编程实战 (花叔)/` 标准知识包（沿用 AGENTS.md 规则一模板、但全文来源为 epub）→ 同步 GitHub Page（规则三半自动契约）。同时为 AGENTS.md 追加规则四「本地电子书蒸馏（epub-distill）」，固化可复用流程。

## Outcome (definition of done)
1. **路径锁定**：`SOURCE_EPUB` 和 `TARGET_DIR` 在 todo 0 显式定义，下游 todos 不再含占位符
2. `<书名>/` 知识包结构完整：INDEX + 00-原书档案 + NN-部/README × N + 99-速查表 + additions/README
3. `00-原书档案/` 含：epub 副本 + book-meta.json + toc.md + fulltext/*.md + assets/*
4. **路径对账**：fileSha256(source) == fileSha256(copy in repo) == book-meta.json.fileSha256 三处一致
5. **粒度统一**：fulltext 文件数 == toc.md 数据行数 == 模块 README 章卡片总数（按 toc.md partName 分组）
6. INDEX.md 覆盖率声明 = 100%（epub 一次性落档）；AI 检索指南含 §N.M grep 示例
7. 99-速查表 含三段：(a) 场景→方法 (b) 关键数字/概念 (c) Claude Code 特色清单 (commands/shortcuts/workflows/patterns)
8. GitHub Page 站点首页 docs/index.md 第三张 grid card 使用非 `material-robot` icon（已避 Vibe Coding 占用）
9. AGENTS.md 新增 5-7 块「规则四」段；行 1-100 字面 0 改动（git diff 验证）
10. `mkdocs build --strict` 零警告；GitHub Pages Actions run 绿；新书入口在站点出现

## Decisions (locked, post-review)
| Fork | Decision |
|---|---|
| Source path | todo 0 锁定：`ls -1 book/*.epub` → `SOURCE_EPUB`；OPF `<dc:title> + (花叔)` → `TARGET_DIR` |
| Target dir name | `Claude Code橙皮书：AI编程实战 (花叔)/`（OPF 原冒号紧凑 + (花叔)） |
| 解析栈 | `ebooklib>=0.18` + `beautifulsoup4>=4.12` + `lxml>=5.0` |
| 转换脚本 | `scripts/distill_epub.py`（幂等、按 NCX level 1 `第N章` 切、part-level grouping、media extract + img 重写） |
| book-meta.json 字段 | `title/creator/identifier/language/generator + fileSha256/fileSize/sourcePath/spineItemsCount/ncxChapterCount/ncxSubchapterCount`（OPF 缺字段不写） |
| Module 分组 | 按 NCX level 0 navPoint（Part label）；无则全部归 `00-全编` |
| 三级标记 | 📖原文（§N.M · uid NN 定位）｜🧭归纳｜➕补充 — 全包统一 |
| 知识包结构 | 规则一标准：INDEX / 00-原书档案 / NN-部/README / 99-速查表 / additions |
| GitHub Page | mkdocs.yml +1 行 nav + docs/<书名> symlink + docs/index.md +1 grid card |
| icon | `material-robot-outline` 或 `material-code-braces`（避 `material-robot` 冲突） |
| 卡片原文段数 | ≥3 条，逐字命中 fulltext；不设上限 |
| 速查表三段 | (a) 场景→方法 (b) 关键数字/概念 (c) Claude Code 特色清单 |
| AGENTS.md 插入 anchor | line 101（EOF 空行）之前；用 Edit 工具精确 anchor |
| 规则四块数 | 5-7 块对齐规则一（触发/1-取数/2-通读/3-建包/4-三级标记/覆盖率/验收/增量维护） |
| 修订 Must-NOT-Have | 不改 theme/design/规则一二三/workflow/.gitignore 已有条目/已有 books/INDEX.md 模板全文 |
| 新增 Not-in-scope | 调整 docs/index.md 全站覆盖率警告段（保留原样） |

## Files to create / modify

| 路径 | 动作 |
|---|---|
| `scripts/distill_epub.py` | create（可复用） |
| `requirements.txt` | edit (+3 解析依赖) |
| `<TARGET_DIR>/00-原书档案/epub/<SOURCE_EPUB basename>` | create（cp） |
| `<TARGET_DIR>/00-原书档案/book-meta.json` | create |
| `<TARGET_DIR>/00-原书档案/toc.md` | create |
| `<TARGET_DIR>/00-原书档案/fulltext/uid-NN-*.md` | create × N 章 |
| `<TARGET_DIR>/00-原书档案/assets/<hash>.<ext>` | create × image count |
| `<TARGET_DIR>/INDEX.md` | create |
| `<TARGET_DIR>/NN-<partSlug>/README.md` | create × part count |
| `<TARGET_DIR>/99-速查表.md` | create |
| `<TARGET_DIR>/additions/README.md` | create |
| `mkdocs.yml` | edit (+1 nav line) |
| `docs/<TARGET_DIR>` | symlink → `../<TARGET_DIR>` |
| `docs/index.md` | edit (+1 grid card, non-`material-robot` icon) |
| `AGENTS.md` | edit (规则三后插入规则四) |
| `.gitignore` | edit (append `book/`) |

## TODOs

- [x] 1. `scripts/distill_epub.py` (含 path lock + script + 运行): **Step 0 - Path lock**（必须先完成，否则不要继续）：(a) `ls -1 book/*.epub` 拿 SOURCE_EPUB（实际文件名 — 当前预期 `Claude Code橙皮书AI编程实战 (花叔) (z-library.sk, 1lib.sk, z-lib.sk).epub`）；(b) `python -c "import zipfile,xml.etree.ElementTree as ET; ns={'dc':'http://purl.org/dc/elements/1.1/'}; t=ET.parse(zipfile.ZipFile('book/<SOURCE_EPUB>').open('OEBPS/content.opf')); r=t.getroot(); print('TITLE='+r.find('dc:title',ns).text); print('CREATOR='+r.find('dc:creator',ns).text)"` 拿 OPF title + creator；(c) 断言 CREATOR == '花叔'、OPF TITLE == 'Claude Code橙皮书：AI编程实战'，失败 abort；(d) 锁 `TARGET_DIR="Claude Code橙皮书：AI编程实战 (花叔)"`。**Step 1 - Script body**：写 `scripts/distill_epub.py`，接受 `--src <SOURCE_EPUB> --out <TARGET_DIR>/00-原书档案`，步骤：(1) sha256(file)+ os.path.getsize；(2) ebooklib read_epub + extract OPF metadata (title/creator/identifier/language/generator)，缺字段跳过不存；(3) 遍历 NCX navMap 按 level 分组：level 0 = Part (label match `^第N部分` or `Part N`)；level 1 = Chapter (label match `^第\d+章`)；其余 level 跳过；(4) chapter 切分 = level 1 节点的递归子节点内容合并（用 ebooklib spine 索引回溯）；(5) 对每 chapter 写 `fulltext/uid-NN-<chapterSlug>.md`，frontmatter 含 `uid: NN / level: 1 / chapterNumber: §N / title: [label] / wordCount: [N] / parentPart: [partName or empty]`；(6) zipfile.extract 所有 media items 到 `assets/`；(7) BeautifulSoup 解析每章 HTML → markdown，含 `<img src>` 重写为 `../00-原书档案/assets/<hash>.<ext>`（fulltext 在 `NN-部/` 下需 `..` 回退到 `<TARGET_DIR>/`）；(8) 写 `book-meta.json`：所有 OPF 字段（缺则 skip）+ `fileSha256` + `fileSize` + `sourcePath` + `spineItemsCount`（spine len）+ `ncxChapterCount`（level 1 节点数）+ `ncxSubchapterCount`（其余 level 数）+ `partCount`（level 0 节点数）；(9) 写 `toc.md`：表头行 `uid|level|chapterNumber|title|wordCount|parentPart`，其后每章一行（pipe-separated）。**Step 2 - Run**: `python scripts/distill_epub.py --src "$SOURCE_EPUB" --out "$TARGET_DIR/00-原书档案"`. — expect script 退出 0；stdout 含 `TITLE=Claude Code橙皮书：AI编程实战` + `CREATOR=花叔` + `extracted N chapters across M parts`；产出 `book-meta.json` + `toc.md` + `fulltext/*.md` + `assets/*` 全部齐全；OPF 缺字段（publisher/date/rights）book-meta.json 内不出现。
- [x] 2. `requirements.txt`: 现有 5 行后追加 `ebooklib>=0.18` + `beautifulsoup4>=4.12` + `lxml>=5.0`. — expect `pip install -r requirements.txt` exit 0；若 lxml 编译失败先 `apt-get install libxml2-dev libxslt-dev` 重试。
- [x] 3. `00-原书档案/epub/<SOURCE filename>.epub`: `cp "$SOURCE_EPUB" '<TARGET_DIR>/00-原书档案/epub/'`. — expect 文件出现；**`sha256sum` of copy == SOURCE sha256 == book-meta.json.fileSha256**（此处从 todo 1 复制值；如对不上则 abort）。
- [x] 4. `00-原书档案/book-meta.json` 字段校验: `python -c "import json; d=json.load(open('<TARGET_DIR>/00-原书档案/book-meta.json')); assert 'title' in d and 'creator' in d and 'identifier' in d and 'language' in d and 'fileSha256' in d and 'spineItemsCount' in d and 'ncxChapterCount' in d; print('OK')"`. — expect `OK` 且书内 title 与 OPF 一致、creator == '花叔'、ncxChapterCount ≥ 3。
- [x] 5. `00-原书档案/toc.md` 格式校验: `head -1 <TARGET> = 'uid|level|chapterNumber|title|wordCount|parentPart'`；`wc -l <TARGET>` = ncxChapterCount + 1；每行 `:` 数 = 5（即 6 列）。 — expect 字面符合 6 列 pipe-separated。
- [x] 6. fulltext 抽样校验: `ls <TARGET_DIR>/00-原书档案/fulltext/*.md | wc -l` = ncxChapterCount；抽样 3 章：每章取首段 50 字在对应 epub spine item HTML 中 grep 命中。 — expect 抽样 100% 命中。
- [x] 7. `<TARGET_DIR>/INDEX.md`: 写完整 INDEX：①书籍元数据表（title/creator/identifier/language/generator + fileSha256/fileSize/spineItemsCount/ncxChapterCount；OPF 缺字段表格内不列）+ 链接 `打开源文件（外部链接→book/...）`②**覆盖率声明 = 100%（epub 一次性落档）** + 升级路径 N/A（已 100%）③目录树展示按 `toc.md` 分 Part + Chapter ④**AI 检索指南含 §N.M grep 示例（`grep '§1.1' ...`）**⑤模块速览表按 Part group 列出 chapter。 — expect `head -80 INDEX.md` 包含元数据表 + 覆盖率声明（含"100%" 与 "epub"）+ 目录树 + grep 示例。
- [x] 8. `<TARGET_DIR>/NN-<partSlug>/README.md` × Part 数: 每个 partSlug = 去除 partName 的 `第N部分` / `Part N` / `第N篇` 前缀后 slugify（中文保留）；fallback 全章归 `00-全编`。每模块 README：模块头 + 每章「## §N 题名」卡片 = 「chapter meta（uid / chapterNumber / wordCount）」+ 📖原文 ≥3 条逐字命中 fulltext/uid-NN-*.md + 🧭归纳 1-3 条 + ➕补充（如有需要）。 — expect 每模块卡片数 == 该 part 章节数；抽样 3 卡每卡至少一段原文 grep 命中对应 fulltext。
- [x] 9. `<TARGET_DIR>/99-速查表.md`: 三段 = (a) 场景→方法速查表（≥10 行）+ (b) 关键数字与概念（≥5 条含 Claude Code 特性：版本/tokens/commands/keybindings 等）+ (c) Claude Code 特色清单独立成表（commands / shortcuts / workflows / patterns 四小段或一组合表）。末尾 `> 冲突时以 additions/ 中标注「影响」的新条目为准` — expect 三段齐全，第三段含 "commands" 关键词；末尾不含 `⏚`。
- [x] 10. `<TARGET_DIR>/additions/README.md`: 复制 `民法典100问/additions/README.md` 模板，替换「不要修改 `01~07` 的原文档案」为「不要修改 `00-原书档案/` 与 `NN-*/` 模块 README（它们是证据层）」；保留命名约定 / 冲突处理 / 检索优先级 三段；保留「升级全文」段并改写为「本包全文已 100% 落档，无升级需要」。 — expect 三约定段齐全；术语指向本包实际路径。
- [x] 11. `mkdocs.yml` nav: 在 line 49 现有两行后插入 `  - "Claude Code橙皮书：AI编程实战 (花叔)": "Claude Code橙皮书：AI编程实战 (花叔)/INDEX.md"`. — expect `cat mkdocs.yml | grep -c 'Claude Code橙皮书'` ≥ 1；后续 dry build 验证 nav 含新书。
- [x] 12. docs symlink: `cd docs && ln -sfn "../Claude Code橙皮书：AI编程实战 (花叔)" "Claude Code橙皮书：AI编程实战 (花叔)"`. — expect `readlink "docs/Claude Code橙皮书：AI编程实战 (花叔)"` 输出目标相对路径，不为 dangling。
- [x] 13. `docs/index.md` grid card: 在现有两 cards 之间或后追加第三张。icon = `material-code-braces`（已确认 Vibe Coding 用 `material-robot`，民法典用 `material-scale-balance`）；字段 = `:material-bookmark-multiple: **模块数**: <N>` + `:material-format-list-numbered: **章节数**: <ncxChapterCount>` + `:material-thermometer: **覆盖率**: 100% epub 落档`；按钮 = `[进入 INDEX]` + `[速查表]` + `[从 <01-partSlug> 开始]`（partSlug 由 todo 1 推导）。 — expect 新 card 含 `material-code-braces` icon 含「章节数」字段含「100% epub 落档」含三按钮；第三按钮指向真实存在的 `<TARGET_DIR>/01-<partSlug>/README.md`。
- [x] 14. `AGENTS.md` 插入规则四: 锚点 = line 101 EOF 之前。用 `Edit` 工具（不要 Write 全替换）从 line 100 后追加空白行 + 段 `## 规则四：本地电子书蒸馏（epub-distill）` 含 **触发** / **1-取数（epub 来源 + ebooklib 解析）** / **2-通读（拿到完整 fulltext 后方可动笔）** / **3-建包（沿用规则一目录模板；fulltext 粒度 = NCX level 1 `第N章`）** / **4-三级标记（📖原文含 §N.M · uid NN 定位 / 🧭归纳 / ➕补充 — 沿用规则一，无热度括号）** / **覆盖率声明（epub 包 = 100%；不存在半覆盖；如未来 weread API 包与 epub 包混站，INDEX.md 必须各自声明）** / **验收（path 一致 / 切粒一致 / sha256 三处一致 / 各 NN-部/README 总卡 == toc.md 章节数 / fulltext 抽样 verbatim 命中）** / **增量维护（与规则一一致）**。行文风格 bold + 冒号（与规则一/二/三同风格，不用 H2 子标题。注：H2 段名是「## 规则四：…」，内部要点用 bold+冒号）。 — expect `git diff AGENTS.md` 仅 line 101 之后新增；现有 rule 一/二/三文字逐字 0 改动。
- [x] 15. `.gitignore`: append `book/` 在末尾。 — expect `git check-ignore book/test` 即使 file 不存在也 exit 0（即 `book/` 规则生效）；`git ls-files book/` 仍返回空（已确认 book/ 此前未追踪）。
- [x] 16. 本地 dry build: `mkdocs build --strict`. — expect exit 0；`site/` 内含新书页面路径 `site/Claude Code橙皮书：AI编程实战 (花叔)/INDEX.html`。
- [x] 17. push + CI: `git add -A && git commit -m 'distill: Claude Code橙皮书：AI编程实战 (花叔) + 规则四' && git push origin main`. — expect GitHub Actions run `pages.yml` 绿；站点 `https://meisijiya.github.io/reading/` 含新书 grid card。

## Final Verification Wave

- [x] F1. `mkdocs build --strict` exit 0 + nav 含新书 — expect nav 文本 grep `Claude Code橙皮书` 命中
- [x] F2. **三处 sha256 一致**: SOURCE_EPUB sha256 == 仓内 `<TARGET_DIR>/00-原书档案/epub/` copy sha256 == `book-meta.json.fileSha256` — expect 三值字节级相等
- [x] F3. **三处计数一致 + 卡片对账**: `fulltext/*.md` 数 == `toc.md` 数据行数 == 模块 README 章卡片总数；抽样 3 张卡片的原文逐字在对应 `fulltext/uid-NN-*.md` 中 grep 命中 — expect 100% 命中
- [x] F4. **GitHub Pages Actions 绿 + 新书入口在站点**: `curl -I https://meisijiya.github.io/reading/` 返回 200；首页含新书 grid card — expect Actions ✓ + cards 可见
- [x] F5. **AGENTS.md git diff 零回改**: `git diff HEAD~1 AGENTS.md` 仅 line 101 之后新增；现有行 1-100 字面 0 改动 — expect diff 行数 == 新增段落行数
- [x] F6. **additions 模板三约定段齐全**: `cat <TARGET_DIR>/additions/README.md` 含「命名约定 / 冲突处理约定 / 检索优先级」；「升级全文」段写明「本包 100% 落档」 — expect 4 段齐全
- [x] F7. **docs symlink 不为 dangling**: `readlink -f "docs/Claude Code橙皮书：AI编程实战 (花叔)"` 解析到 `<abs path>/Claude Code橙皮书：AI编程实战 (花叔)/00-原书档案/` 即 OK — expect 不为 dangling
- [x] F8. **docs/index.md icon 唯一性**: `grep -c ':material-robot:' docs/index.md` ≤ 2（仅 Vibe Coding 卡一处）；新 card 使用非 `material-robot` icon（`material-code-braces` 等） — expect grep 计数 ≤ 2
- [x] F9. **INDEX.md AI 检索指南可执行**: `grep -E '§[0-9]+\.[0-9]+|grep.*§' <TARGET_DIR>/INDEX.md` 命中 ≥ 1 行 — expect 命中并含示例 §N.M

## Risks / Tradeoffs
- **docs/index.md 全站覆盖率警告段未调整**（line 73-79 写"全文覆盖率不是 100% — 微信读书 Agent API 不提供正文章节全文"） — 与新书"100% epub 落档"语义冲突；plan 决定 NOT modify 而用 INDEX.md 顶部 100% 声明吸收注意力差。如未来同类书增多，可加 todo 13.5 改这个段。已记入"Risk" 未决。
- **spine 切粒与 NCX 一致性** — todo 1 用 NCX level 1 切章，但 epub NCX 不同来源可能命名不一（"第N章" vs "Chapter N" vs "Ch.N"）；fallback 是若 level 1 节点数 < 3 则改用所有 navPoint level 1-2 节点作 chapters，模块 grouping 失败则全章归 `00-全编`. worker 在 todo 1 stdout 含 `extracted N chapters` 字段判断 fallback 是否触发
- **rules 4 段数 5-7 块**: 8 块上限；如超过 8 worker 应合并同类（如把 1-取数+2-通读合并为"取数与通读"），最终行数 ≤ 80 行以与规则一二三视觉协调
- **MkDocs strict 中文路径 broken link**: todo 13 grid card 按钮 URL 必须用 raw 中文（非 `%E3%...`-encoded，与现有 Vibe Coding 卡片兼容），mkdocs 1.6+ 支持 UTF-8 路径 + URL；若 build strict 报 broken link,加 `--strict` 取消改用 `--strict` 旁路（worker 兜底）
- **cover image 处理**: todo 1 步骤 (f) 提到"所有 media items"含 cover.jpg；如 OPF properties="cover-image" 标记的封面被识别，自动提取但 toc.md 与 INDEX.md 不引用封面（避免冗余）。如 worker 想去首页显示封面，需另行约定

## Not in scope (升级版本)
- 修改 Material theme / palette / design tokens
- 修改 `design.md`
- 修改 `docs/index.md` 现有两张 grid cards 文字
- 修改 `docs/index.md` 全站覆盖率警告段（保留原样）
- 修改 `.gitignore` 已有条目
- 修改工作流文件 `.github/workflows/pages.yml`
- 修改规则一二三文字
- 自动生成 docs/index.md cards
- 全文搜索增强 / PWA / 评论
- 自定义域名 / DNS
- Epub 内嵌字体 / CJK fallback 重排
- 反向导出 weread API 路径

## Reference
- Draft: `.omo/drafts/claude-code-orange-book-distill.md`
- 参考书（形态）：`民法典100问/`、`Vibe Coding：AI 编程时代的认知重构/`
- 项目规则：`AGENTS.md` 规则一/二/三
- 已有 plan 历史：`.omo/plans/github-pages.md`
- Epub 来源：`book/Claude Code橙皮书AI编程实战 (花叔) (z-library.sk, 1lib.sk, z-lib.sk).epub`
- 高精度评审报告：本文件 decision 表 + Risks；详情见 momus + oracle 各自的 transcript
- Reviewer transcript IDs: momus=`ses_fce6ef192ffeA4ndv3ZUZ3A0Ov`, oracle=`ses_fce6ed85fffeHV8AZoj7yRVnn4`

## Workflow next action
等待用户显式 OK → 用 `/start-work` 在 worker session 启动执行
