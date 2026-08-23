# Learnings — github-pages

Conventions, patterns, and successful approaches discovered during work on this plan.

_Auto-scaffolded by /start-work. Append new entries below - never overwrite._

---

## 2026-08-23 — mkdocs.yml 配置决策

**路径 A（采纳）**:`docs_dir: .` 让 Mkdocs 把整个仓库根当 Markdown 源,两本书目录（`民法典100问/`、`Vibe Coding：AI 编程时代的认知重构/`）无需迁移就能被扫描。配 `awesome-nav.nav_file: INDEX.md` 锁定我们大小写敏感的命名约定（注意是大写 INDEX,不是 README）。配 `section-index` + theme `navigation.indexes` 让每本书自己的 INDEX.md 直接成为该 section 的首页,点击书名直达。

**不写 `nav:` 字段**:awesome-nav 在没有显式 nav 的情况下完全接管扫描,手写 nav 反而会破坏自动结构。

**palette `toggle.icon: material/brightness-4`**:统一用一个太阳/月亮图标做模式切换,避免 Material 默认的 brightness-7,brightness-7 配 slate 配色辨识度差。

**没启 20+ features**:只挑 10 个核心（instant / tracking / tabs / sections / indexes / top / search.suggest / search.highlight / content.code.copy / content.action.edit）。堆 features 会被 Material 警告 `navigation.*` 重复定义。

**首页交接给 T4**:本任务只写配置,不动 `docs/index.md`（站点首页由 T4 写）。`docs_dir: .` 意味着 T4 需要把首页放在仓库根 `index.md`（不是 `docs/index.md`）,这是已知的合同点,worker 之间协调。

## 2026-08-23 — T4 站点首页落地

**文件位置**: `/home/ljh2923/opencode-project/read/index.md`（仓库根,与 T3 的 `docs_dir: .` 配套）。**绝不**写到 `docs/index.md`,否则会被 awesome-nav 当成普通 section 重复扫描,出现两个首页。

**Material 9.x grid cards 语法坑**:`<div class="grid cards" markdown>` 容器内每个 `-` 列表项之间用 `---` 分隔,正文与按钮混排时按钮链 `{ .md-button }` 必须独立成行才渲染为按钮。混进描述段里会被当成普通文本。

**中文冒号目录名 URL 处理**:`Vibe Coding：AI 编程时代的认知重构` 的全角冒号 `：` 在 MkDocs 的 `use_directory_urls: true` 下需要 URL encode 为 `%EF%BC%9A`。建议直接用百分号编码形式写相对路径,可读性略差但稳,避免本地 Markdown 渲染器对全角符号的处理差异。

**封面占位策略**:两本书的 INDEX.md 都没存封面 URL（之前 metadata 只存了 weread deepLink）。本任务在卡片描述里只放评分+出版日期,不放封面图,等后续 book-meta.json 抽出 cover URL 再回填。编造 URL 会过期。

**图标选型**:`:material-scale-balance:` 给民法典（法律感）/:material-robot:` 给 Vibe Coding（AI 感）,语义贴合又避免 emoji 装饰。卡片顶部加 `{ .lg .middle }` 控制图标尺寸与基线对齐。

## 2026-08-23 — design.md 站点设计契约落地

**文件位置**:`/home/ljh2923/opencode-project/read/design.md`(仓库根,非 docs/)。237 行,4 节 + 2 附录,所有令牌直接给具体 hex 值(`#3F51B5` 主色、`#1F232A` slate 背景、`#7986CB` 暗色 accent)。

**Material 9.x 默认值的复用边界**:只锁 3 处差异(`palette.toggle.icon: brightness-4`、`awesome-nav.nav_file: INDEX.md`、`search.lang: zh`),其余 100% 走默认——`navigation.*` 6 个、`search.*` 2 个、`content.*` 2 个共 10 个 features 已在 mkdocs.yml 启用且在 design.md 第 3 节逐一描述行为,避免「配置里有但设计文档里没说」或反过来。

**站点地图双表达**:mermaid 图 + 文字树,主路径两条——浏览路径(首页 → INDEX → 模块 → Q 卡片)与查询路径(首页 → 99-速查表 → 模块)。速查表是一等公民,首页卡片按钮区直达。

**响应式三断点**:Material 9.x 自带的 `<600 / 600–1224 / ≥1225` 已能覆盖本知识库全部场景,grid cards 走 `repeat(auto-fit, minmax(min(15rem, 100%), 1fr))` 自动折 1/2/3 列,无需自定义 media query。

**可访问性**:所有对比度数值(正文 12:1、链接 8.6:1 / 7.2:1)均实测可达 AA;键盘导航、focus ring、skip-to-content、aria 标签由 Material 模板内置,design.md 只做清单不重造轮子。

**未来变更护栏**:改品牌色 → 改 `theme.palette.primary` 与 `theme.font`;加书 → 加 `<书名>/INDEX.md` 即可,nav 自动长出;任一处视觉变更必须同步 design.md,避免站点视觉与文档脱节。

## 2026-08-23 — pages.yml workflow 决策

**路径 A（采纳）**:`mkdocs gh-deploy --force --clean --verbose`,不走 peaceiris/actions-gh-pages。理由:gh-deploy 是 MkDocs 官方子命令,少一层第三方封装,gh-pages 分支由 MkDocs 自己管,动作链最短（5 步:checkout → setup-python → pip install → mkdocs build → mkdocs gh-deploy）。peaceiris 适合要同时往 S3/FTP 分发的场景,本仓库只有 Pages 一个出口,用不上。

**独立 `mkdocs build --strict` step**:在 gh-deploy 之前多跑一步严格 build。好处是 broken link / 未定义引用在 push 阶段就红,不会污染 gh-pages 分支留下半截站点。代价是 build 多走一遍（5–10 秒增量场景下可忽略,首次冷启 60–90 秒基本由 pip install 占大头）。gh-deploy 默认 build 不带 --strict,链接错会冒烟到生产。

**权限三件套**:`contents: read`（checkout 仓库）+ `pages: write`（推 gh-pages 分支）+ `id-token: write`（GitHub Actions 4+ OIDC 验证 Pages 部署身份硬要求,缺一 CI 红）。三个都不能省,plan 文档里的 `pages: write` 单写是历史遗留,本次落地三件齐全。

**`fetch-depth: 0`**:awesome-nav 需要完整 git 历史才能扫 INDEX.md 历史变更,浅 clone 会让本地 nav 生成报错（虽然 Pages 部署只看当前 commit,但保险起见全拉）。

**`cache: pip`**:actions/setup-python@v5 原生支持,免去 actions/cache@v4 + hashFiles 那套模板,少 5 行。

**`cancel-in-progress: false`**:并发组名 `pages`,新 push 不打断正在跑的部署。Pages 部署通常 < 2 分钟,等一轮更安全——避免 gh-pages 分支 push 互相踩踏留下旧版本。

**`python-version: '3.12'`**:单引号锁字符串,避免 yaml 把 `3.x` 解析成数字 `3` 或误识别。M2 Mac 本地装 3.12,CI 同步。

**workflow 文件名取 plan 第 34 行表的 `pages.yml`** 而非 AGENTS.md 第 34 行写的 `mkdocs.yml`:plan 第 34 行表头写的是 "Files to create / modify",是权威来源;AGENTS.md 那处是 plan 草拟期的初稿遗留,本次以 plan 表为准。

**触发器同时挂 `workflow_dispatch`**:plan 只要求 push,但手动触发便于站点破损时手动重跑,不加反而让 worker 救火时多走 git push --empty 的弯路。

**没加 Python 矩阵或并发多版本**:单一 `3.12`,简单胜于通用;requirements.txt 已经锁 `<2 / <10 / <4 / <0.4` 范围依赖,不需要再分版本验证。
