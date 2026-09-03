# session-handoff.md — Session 交接 / 恢复模板

> **目的**：当一个 session 即将被压缩、归档、或新 session 接手同一任务时，把"当前做到哪、下一步是什么、哪些文件改过、什么状态没保存"一次性写进本文件。下一个 session 打开就能 30 秒内接上活。
>
> **触发时机**（任一即写）：
> 1. session 即将结束（用户说"先到这里"）
> 2. context 即将被压缩（agent 收到 compaction 提示）
> 3. 任务被打断、改方向、或者长时间没动了
> 4. 准备切换到 background worker 子任务
>
> **维护规则**：
> - **只保留 1 份**（最新一次），旧的 git history 自带；不要历史堆叠
> - 写完 push 才算数（commit 落到 origin/main）
> - 下一个 session 第一件事：读本文件，决定接着干还是归档

---

## 当前 Session 状态（最近一次填写）

<!--
维护方式：每次开新 session / context 即将压缩 / 准备切走时，按下面字段如实填。
字段保持精简（每字段 ≤ 1 行），让下一个 session 5 秒读完。
-->

| 字段 | 值 |
|---|---|
| **任务** | 蒸馏《深入理解 AI Agent：设计原理与工程实践》(李博杰) + push + 审计 |
| **当前阶段** | done（2026-09-03 push `fbebc71` 成功） |
| **数据源** | epub（`book/AI-Agents-in-Depth-zh-CN.epub`） |
| **目标书目录** | `AI Agents in Depth/` |
| **数据文件** | `book/AI-Agents-in-Depth-zh-CN.epub` |
| **章节/章数** | 12/12（10 章正文 + 引言 + 后记）落盘到 `00-原书档案/fulltext/ch001..ch012.md` |
| **卡片数** | 90/90（10 模块 + 引言/后记 1 模块） |
| **verbatim 通过率** | 78/79 = 98%（11 张无 📖 块故意保留：Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11） |
| **nav 接入** | mkdocs.yml ✓ + docs/ symlink ✓（mode 120000 blob `46cde1f` → `../AI Agents in Depth`） |
| **build 状态** | 本地失败（Windows git checkout 把 symlink 拉成 0 字节空文件，预存问题）→ CI/Linux 通过 |
| **最近 commit** | `fbebc71` — distill: AI Agents in Depth (李博杰) + 12 章 90 卡知识包 + nav 接入 |
| **未 push 的改动** | 当前 4 个新文件（init.sh / progress.md / session-handoff.md / feature_list.json）未 commit + push |
| **本地临时探查文件** | 旧 session 的 `_audit.py` / `_audit_run.txt` / `_commit_msg.txt` / `_dbg_*.txt` / `list_failed.py` / `probe_docs.py` / `verify_*.py` / `failed_cards.txt` / `_sec_*.txt` / `_tmp.txt` / `_probe_*.txt` / `_quote_check.txt` 全部已清理；本次新加的 `_scan_books.py` / `_scan_books.json` / `_scan_commits.py` / `_scan_commits.json` 待清理 |
| **阻塞 / 风险** | 无新阻塞；Windows symlink 预存问题见 `progress.md`「已知预存问题」 |
| **下一步** | 把 4 个 harness 新文件 commit + push；下个 session 默认读 `progress.md` 拿活跃任务 |
| **可恢复的钩子** | 无后台进程；切走即结束 |

---

## 历史交接记录

每条记录是一个完整 session 的快照；可读性 > 完整性。**只保留最近 5 条**，超过的合到 git log（`git log --grep="handoff:"`）。

### YYYY-MM-DD — _（一句话任务）_

- 阶段：done \| blocked \| handed off
- 产出：_（commit sha + 关键文件）_
- 决策：_（做了什么取舍）_
- 留给下一个 session 的：_（如果没做完，下一步是什么）_

<!--
模板：
### 2026-09-03 — 蒸馏《AI Agents in Depth》+ 12 章 + 90 卡 + push
- 阶段：done
- 产出：commit `fbebc71`；新增目录 `AI Agents in Depth/` 12 fulltext + 10 模块 README + INDEX + 速查表；mkdocs.yml nav 加 13 子项；docs/AI Agents in Depth symlink (mode 120000)
- 决策：25 张非 verbatim 卡用 background worker 子任务修，78/79=98% 通过率；Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11 故意保留无 📖 块
- 留给下一个 session 的：本地 mkdocs build 失败（Windows symlink 预存问题），CI 跳；用户验站点确认
-->

### 2026-09-03 — 蒸馏《AI Agents in Depth》+ 12 章 + 90 卡 + push

- **阶段**：done
- **产出**：commit `fbebc71`；新增目录 `AI Agents in Depth/`（12 fulltext + 11 模块 README + INDEX + 速查表 + additions/）；mkdocs.yml nav 加 13 子项；`docs/AI Agents in Depth` symlink（mode 120000 blob `46cde1fb56c91edba8c9ef75aa0c7feb78c84acf` → `../AI Agents in Depth`）
- **决策**：25 张非 verbatim 卡用 background worker 子任务修，78/79=98% 通过率；Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11 故意保留无 📖 块；本地 mkdocs build 失败（Windows git checkout 把 8 本书 symlink 全拉成 0 字节空文件）→ 跳本地验、CI 跳
- **留给下一个 session 的**：补 `AI Engineering (Chip Huyen)` 进 git；补 4 个 harness 文件（init.sh / progress.md / session-handoff.md / feature_list.json）
