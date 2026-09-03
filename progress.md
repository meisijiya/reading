# progress.md — 知识库当前进度

> 这是仓库的「当前状态板」。每完成一本书、每开一本新书、每遇到一个阻塞，都先更新这里再开干。
> 结构化状态（按 id / status / 字段）见 [`feature_list.json`](feature_list.json)；这里只放人读的进度叙事 + 阻塞 + 下一步。

## 最近一次发布

| 项 | 值 |
|---|---|
| 上次 push | `247a983` — 2026-09-03 |
| 内容 | **清洁大扫除** — 5 个 atomic commit：补 refactor 漏移（AI Prompt Engineering）→ gitignore .omo/run-continuation/ → 入仓旧 notepad → 收 epub_extract.py → 提交 4 个 harness 资产 |
| 站点 | <https://meisijiya.github.io/reading/>（待 push 后 CI 验证） |
| 引用验证 | 上次（fbebc71）78/79 = 98%；本次清洁 0 字节内容变更 |

## 当前活跃任务

无（无正在蒸馏的书；无正在修的卡；无正在等 CI 的 PR）。

## 下一步候选（按优先级）

1. **补 AI Engineering (Chip Huyen) 知识包**（本地有内容但**未进 git**）
   - 阻塞：本地目录 1.2MB 蒸馏成品（6 模块 / 10 § 卡）已写好，但 `git add` 之前没 commit 上去
   - 处理：下次有空时 `git add "AI Engineering (Chip Huyen)"` + 同步 `mkdocs.yml` 的 nav（已有）+ `docs/AI Engineering (Chip Huyen)` symlink + commit + push
   - 风险：symlink 在 Windows 上不能 checkout，本地无法 build 验证；CI 验证就行
2. **push 这次清洁的 5 个 commit**（`247a983` 还在本地）→ CI 跑 mkdocs build 验证
3. **跑一次 `init.sh`**：把当前 8 本已发布书过一遍 Step 1+2 不变量 + Step 3 build，验证 dist 状态健康
4. **过 `_audit_report.md` 旧结论**：11 张无 📖块的卡（Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11）是用户故意保留，不动；如要补 📖 块需走 worker 派发路径

## 已知预存问题（不在本任务 scope）

| 问题 | 状态 | 风险 |
|---|---|---|
| `docs/AI Engineering (Chip Huyen)` 是 broken symlink | 预存在 | mkdocs build 本地会 warning「No such file or directory」；CI/Linux 正常；该书本身未进 git |
| Windows 下 git 对 U+F03A (PUA) 字符路径处理异常 | 预存在 | AI Prompt Engineering 那本书的目录名带 PUA 字符；git add/checkout/reset/mv 在 shell 层都需要绕路（用 Python 走 PUA 字符 literal） |
| `mkdocs build --strict` 在 Windows 本地会因 symlink 失败 | 预存在 | 推 CI 验；本地不强求 |

## 暂停 / 终止条件

- 单本书蒸馏耗时 > 1 小时 → 切成 2-3 个 worker 子任务并行（参考之前 AI Agents in Depth 25 张卡修法）
- verbatim 通过率 < 80% → 停手汇报，让用户决定是补 fulltext 还是修订卡片
- mkdocs build 报 non-strict warning → 不允许 push，先修

## 进度纪要（保留最近 5 条）

- 2026-09-03：仓库清洁大扫除，5 个 atomic commit：`2c63432`(refactor 补移) → `7402670`(.gitignore 收 4) → `436b8a9`(notepad 入仓) → `247a983`(scripts 收 1) → 本次（harness 4 资产入仓）
- 2026-09-03：蒸馏《AI Agents in Depth》+ 12 章 90 卡 + 修 25 张非 verbatim 卡（78/79=98%）+ push `fbebc71`
- 2026-08-30：蒸馏《AI Prompt Engineering: The 2026 Guide》+ 22 章 + push `0f50abd`
- 2026-08-26：蒸馏《解构领域驱动设计》+ 20 章 + push `b807df1`
- 2026-08-25：蒸馏《微服务设计（第2版）》+ 16 章 + push `4133ae1`
