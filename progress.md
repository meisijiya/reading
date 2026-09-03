# progress.md — 知识库当前进度

> 这是仓库的「当前状态板」。每完成一本书、每开一本新书、每遇到一个阻塞，都先更新这里再开干。
> 结构化状态（按 id / status / 字段）见 [`feature_list.json`](feature_list.json)；这里只放人读的进度叙事 + 阻塞 + 下一步。

## 最近一次发布

| 项 | 值 |
|---|---|
| 上次成功 push | `fbebc71` — 2026-09-03 |
| 内容 | 蒸馏《深入理解 AI Agent：设计原理与工程实践》(李博杰) + 12 章 90 卡知识包 + GitHub Pages nav 接入 |
| 站点 | <https://meisijiya.github.io/reading/> |
| 引用验证 | 78/79 = 98% verbatim 通过（11 张无 📖块不参与） |

## 当前活跃任务

无（无正在蒸馏的书；无正在修的卡；无正在等 CI 的 PR）。

## 下一步候选（按优先级）

1. **补 AI Engineering (Chip Huyen) 知识包**（本地有内容但**未进 git**）
   - 阻塞：本地目录 1.2MB 蒸馏成品（6 模块 / 10 § 卡）已写好，但 `git add` 之前没 commit 上去
   - 处理：下次有空时 `git add "AI Engineering (Chip Huyen)"` + 同步 `mkdocs.yml` 的 nav（已有）+ `docs/AI Engineering (Chip Huyen)` symlink + commit + push
   - 风险：symlink 在 Windows 上不能 checkout，本地无法 build 验证；CI 验证就行
2. **跑一次 `init.sh`**：把当前 8 本已发布书过一遍 Step 1+2 不变量 + Step 3 build，验证 dist 状态健康
3. **过 `_audit_report.md` 旧结论**：11 张无 📖块的卡（Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11）是用户故意保留，不动；如要补 📖 块需走 worker 派发路径

## 已知预存问题（不在本任务 scope）

| 问题 | 状态 | 风险 |
|---|---|---|
| `docs/` 下 8 本书 symlink 在 Windows git checkout 下是 0 字节空文件 | 预存在 | 本地 `mkdocs build` 失败；CI/Linux 正常 |
| `.omo/` 文件被改 | 预存在 | 未知；查 `.gitignore` 是否要排除 |
| `AI Engineering (Chip Huyen)/` 在本地但**未进 git** | 预存在 | mkdocs.yml nav 引用了它但远端没有 → 站点有死链 |
| `tmp-book-test/` 已 revert | 已清理 | OK |

## 暂停 / 终止条件

- 单本书蒸馏耗时 > 1 小时 → 切成 2-3 个 worker 子任务并行（参考之前 AI Agents in Depth 25 张卡修法）
- verbatim 通过率 < 80% → 停手汇报，让用户决定是补 fulltext 还是修订卡片
- mkdocs build 报 non-strict warning → 不允许 push，先修

## 进度纪要（保留最近 5 条）

- 2026-09-03：蒸馏《AI Agents in Depth》+ 12 章 90 卡 + 修 25 张非 verbatim 卡（78/79=98%）+ push `fbebc71`
- 2026-08-30：蒸馏《AI Prompt Engineering: The 2026 Guide》+ 22 章 + push `0f50abd`
- 2026-08-26：蒸馏《解构领域驱动设计》+ 20 章 + push `b807df1`
- 2026-08-25：蒸馏《微服务设计（第2版）》+ 16 章 + push `4133ae1`
- 2026-08-25：蒸馏《凤凰架构》+ 16 章 + push `2ce608d`
