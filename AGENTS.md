# 读书知识库项目规则

本项目 = 个人读书知识库。每本书一个目录，内含一份标准知识包。参考实现：《轻松破解生活难题：民法典100问》/。

## 规则一：读书蒸馏（book-distill）

**触发**：用户要求读某本书、做读书笔记、蒸馏/整理知识包。

1. **取数** — 按「规则二」拉全量数据：bookId → 全部章节目录 → 逐章热门划线。完成标准：章节总数与划线条目数均已落盘为 JSON。
2. **通读** — 动笔前完整读完所有原文片段。完成标准：能复述每个问题的核心结论。提炼层只能从原文归纳，禁止凭模型常识编造"书中观点"；不做摘要式压缩，丢上下文等于没读。
3. **建包** — 写入 `<书名>/`，结构固定：

   ```
   <书名>/
   ├── INDEX.md              导航入口：元数据 + 覆盖率声明 + 目录树 + AI检索指南 + 模块速览
   ├── 00-原书档案/           机器可读原始数据：book-meta.json / toc.md / hot-highlights.json / fulltext/
   ├── NN-<模块名>/README.md  每模块一文件；每问一张卡片：## Q编号 题目 + 📖原文引用（含热度人数）
   ├── 99-速查表.md          场景→规则速查 + 关键期限数字（最高频调用入口）
   └── additions/            增量区：README.md（约定+模板）+ 用户后续的新理解/案例/实践
   ```

4. **三级标记** — 全包统一：📖原文＝接口逐字引用｜🧭归纳＝从原文提炼｜➕补充＝编者依据公开常识。归纳与补充永远不冒充原文。
5. **覆盖率声明** — 接口拿不到正文全文时，INDEX.md 顶部写明各层数据来源与完整度，并给升级路径：用户导出全文放入 `00-原书档案/fulltext/` 即完成归档，其余结构不动。

**验收**：问题卡片数 == 目录问题数（逐一对账）；引用条数 == 抓取条数；additions/ 就位。

**增量维护**：用户新内容一律追加到 `additions/YYYY-MM-DD-主题.md`（模板见该目录 README），不改原文档案；与既有规则冲突时在 additions 里写明理由，保留演化历史；AI 检索时 additions 与速查表同优先级，标注了"影响"的条目覆盖速查表对应旧条目。

## 规则二：微信读书抓取（weread-fetch）

**触发**：任何需要微信读书数据的操作（搜书、书目、章节、划线、笔记、进度）。

**鉴权**：每次 bash 调用都是全新 shell，先内联导出再发请求：

```bash
export WEREAD_API_KEY=$(grep -oP 'WEREAD_API_KEY=\K\S+' ~/.bashrc | tail -1)
```

**请求格式**：统一 `POST https://i.weread.qq.com/api/agent/gateway`，Header 带 `Authorization: Bearer $WEREAD_API_KEY`；body 顶层平铺业务参数和 `"skill_version": "1.0.4"`——参数包进 `params/data/body` 会被服务端静默丢弃。

**errcode 陷阱**：成功回包**没有** errcode 字段，失败才有。判断写成 `d.get('errcode') is None or d.get('errcode') == 0`；写反会把成功当失败无限退避重试。

**频率控制**：请求间隔 ≥2s；遇「请求频率超限」按 25s × 尝试次数退避后重试；批量任务每 10 章落盘一次进度实现断点续传；长任务用 `nohup ... > 日志文件 &`，轮询日志文件——工具超时杀得掉前台管道，杀不掉后台进程。

**读书链路端点**（调用陌生端点前先读 weread-skills 技能文档）：

| 端点 | 用途 |
|---|---|
| `/store/search` | 书名 → bookId |
| `/book/info` | 元数据、简介、评分 |
| `/book/chapterinfo` | 完整章节目录（100%可靠） |
| `/book/bestbookmarks` | 每章热门划线 top~20（markText＋heat 标记人数）——唯一原文文本来源 |
| `/book/getprogress` · `/book/bookmarklist` · `/review/list/mine` | 用户个人进度、个人划线、个人想法 |

网关不存在正文章节全文接口；"完整原书"只有用户导出补入 `fulltext/` 一条路。

## 规则三：GitHub Page 同步（github-pages-sync）

**触发**：`push to meisijiya/reading:main`。book-distill 完成、新书目录推上 main 分支即触发，无需任何手动动作。

**机制**：GitHub Actions 在 push 时自动构建并发布 MkDocs Material 站点：

- 触发器：`.github/workflows/mkdocs.yml` 监听 main 分支 push，无需手动触发。
- 构建：MkDocs Material 主题 + `mkdocs gh-deploy`（或 peaceiris/actions-gh-deploy）一键发布到 gh-pages。
- 导航生成：`mkdocs-awesome-nav` 自动扫描仓库根所有 `<书名>/INDEX.md` 并入 nav，**完全不用手改 `mkdocs.yml` 的 nav 段**。
- 入口渲染：`mkdocs-section-index` 把每本书的 INDEX.md 渲染成 section 入口页，点击书名直达知识包首页。
- 透明性：book 目录的增减对 worker 完全透明。建好目录推上去，站点自动长出新书卡片。

**唯一约束**：每本书目录下必须有 `<书名>/INDEX.md`。

`mkdocs-awesome-nav` 靠它定位 section 入口；缺失则 `mkdocs build --strict` 失败，CI 挂掉。Worker 必须严格按规则一的目录模板建包，别自创目录结构、别省略 INDEX.md、别把 INDEX.md 塞到子目录里——任何一项违规都会让 CI 红。

**半自动契约**（实测同步规则）：

由于 `mkdocs-awesome-nav` 3.x 与本仓 Material 主题存在兼容性问题，实际采用手写 nav + docs/ 下 symlink 实现。新增书目录后，worker **必须**同时改两处：

1. `mkdocs.yml` 的 `nav:` 段加一行，例：
   ```yaml
   nav:
     - 首页: index.md
     - 民法典100问: 民法典100问/INDEX.md
     - "Vibe Coding：AI 编程时代的认知重构": "Vibe Coding：AI 编程时代的认知重构/INDEX.md"
     - <新书名>: <新书名>/INDEX.md   # 新增
   ```
2. `docs/` 下建一个 symlink 指向新书目录，例：
   ```bash
   cd docs && ln -s ../<新书名> <新书名>
   ```

漏改任一处，CI 仍会绿（`build --strict` 通过、Pages 部署成功），但站点 nav 不会显示新书——触发"Push 看似成功但站点没更新"陷阱。这两条契约 CI 不会自动检查，靠 worker 自觉。

**验收**：

- GitHub Actions run 显示绿勾。
- 站点首页能看到新书卡片（说明 section 已被识别）。
- 新书目录下 `INDEX.md` 文件实际存在且顶部含元数据块。

任一项不满足，回查 workflow 日志的具体报错行——九成是 "could not find INDEX.md" 类的扫描失败。

**风险**：worker 蒸馏新书忘建 INDEX.md → CI 失败、站点不更新。新人/AI 务必遵守规则一的目录模板，别图省事跳过导航入口这一步。

## 规则四：本地电子书蒸馏（epub-distill）

**触发**：用户提供 epub 文件，要求做读书笔记 / 蒸馏 / 整理知识包（共享规则一目录模板，但数据源是本地 epub 而非微信读书接口）。

1. **取数（epub 来源 + ebooklib 解析）** — Python `ebooklib`：`book = epub.read_epub('x.epub')`；目录递归 `book.toc` 取 NCX level 1 节点（标题为「第N章」/`Chapter N`/`卷N`）；原文用 `chapter.get_content()` 逐节点写 `00-原书档案/fulltext/<uid>.md`（一个 level-1 节点一文件，uid 编号做稳定锚点）。元数据 `book.metadata` 落 `book-meta.json`。epub 无 bestbookmarks 接口——`hot-highlights.json` 与 `fulltext/` 合流，原文即权威。

2. **通读（拿到完整 fulltext 后方可动笔）** — 必须等全部 `fulltext/*.md` 落盘、NCX level 1 节点总数对得上 `book.toc` 顶层数后方可提炼；提炼层只能从原文归纳，禁止凭模型常识编造"书中观点"；不做摘要式压缩，丢上下文等于没读。

3. **建包（沿用规则一目录模板；fulltext 粒度 = NCX level 1 `第N章`）** — 目录结构完全复用规则一：`INDEX.md` + `00-原书档案/`（book-meta.json / toc.md / fulltext/<uid>.md）+ `NN-<模块名>/README.md` 每章一卡 + `99-速查表.md` + `additions/`。fulltext 粒度 = 一个 NCX level 1 章节一个文件，每张卡片对应一个 chapter，sha256 三处一致（原文文件 / 卡片引用块 / 速查表锚点）。

4. **三级标记（📖原文含 §N.M · uid NN 定位 / 🧭归纳 / ➕补充 — 沿用规则一，无热度括号）** — 📖原文＝逐字引用并附 `§N.M`（章节内小节）+ `uid NN`（fulltext 文件编号）双锚点；🧭归纳＝从原文提炼；➕补充＝编者依据公开常识。无热度标记（heat 是 weread 专属，epub 不存在）。

**覆盖率声明（epub 包 = 100%；不存在半覆盖；如未来 weread API 包与 epub 包混站，INDEX.md 必须各自声明）** — epub 包覆盖度天然 100%：`fulltext/` 即原书全部正文。INDEX.md 顶部照规则一样板声明即可。仓库以后若 weread 来源书与 epub 来源书并存，每本书在自己 INDEX.md 内明示数据源（接口 / 本地 epub），不互相冒充。

**验收（path 一致 / 切粒一致 / sha256 三处一致 / 各 NN-部/README 总卡 == toc.md 章节数 / fulltext 抽样 verbatim 命中）** — ① `00-原书档案/book-meta.json` 存在且字段齐；② `fulltext/` 文件数 == `book.toc` 顶层 NCX level 1 节点数；③ sha256 在原文文件、卡片引用块、速查表三处完全一致；④ 各 `NN-部/README.md` 问题卡总数 == `toc.md` 章节数（逐一对账，规则一通行口径）；⑤ 每个 fulltext 文件抽样一句对照原文 verbatim 命中（人工 grep 验）。

**增量维护**：与规则一一致——用户新内容追加到 `additions/YYYY-MM-DD-主题.md`，不改原文档案；与既有规则冲突时在 additions 里写明理由，保留演化历史；AI 检索时 additions 与速查表同优先级，标注了"影响"的条目覆盖速查表对应旧条目。

## 规则五：GitHub Page 内容展示完整（github-pages-complete）

**触发**：用户报"内容看不到/跳不动/看不到完整章节"等 Pages UX 问题；新书发布或重大改动后自检。

**核心约束**（任一遗漏 → 站点 UX 残废）：

1. **nav 段必须展开到 `NN-部/README.md`**（不是只到各书 INDEX.md）。否则侧边栏塌缩成书名一级，用户只能看到第一个模块——这就是用户最初反馈的根因。
2. **`theme.features` 必须含 `navigation.footer`**。否则模块页底部无 Previous/Next，用户读完一个模块无路可走。
3. **INDEX.md 速览表的"模块"列必须用 markdown 链接 `[一 XX](01-XX/README.md)`**，不是纯文本。否则表格内不可点。
4. **epub 来源书的每张卡片"原文出处"必须用 markdown 链接 `[uid-NN-XXX](../00-原书档案/fulltext/uid-NN-XXX.md)`**。`00-原书档案/fulltext/` 已被 mkdocs build 进 site，但卡片不链 = 死入口。
5. **INDEX.md 提及的归档文件路径**（`toc.md` / `book-meta.json` / `hot-highlights.json` / `toc.json`）**用 markdown 链接**，让"AI 检索建议"段落也成可点击入口。
6. **相对路径正确**：模块 README 在 `NN-部/` 子目录，链接归档要 `../00-原书档案/...`；INDEX.md 在书根但被生成到 `INDEX/index.html`，mkdocs 自动加 `../`（不写错就行）。中文文件名里 `"` 和 `"` 是不同字符（U+0022 ≠ U+201C/U+201D），写错会导致 strict build WARNING。
7. **`mkdocs build --strict` 必须零警告通过才允许 push**。有 WARNING = 有死链。

**验收**（push 前必跑）：

```bash
mkdocs build --strict                                    # 零警告
python3 scripts/check_site_links.py                       # 期望 OK=N/N FAIL=0
```

（可选：传本地预览地址做集成测试，如 `python3 scripts/check_site_links.py http://127.0.0.1:8765/reading`。）

**自检目标**：被引用的所有 URL 100% 返回 200；nav 展开、底部 Previous/Next、速览表/卡片/归档文件链接全部可点击；epub 来源书 14 章完整原文从 INDEX 一步直达（不超 2 次跳转）。

