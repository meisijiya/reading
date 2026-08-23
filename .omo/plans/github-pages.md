---
slug: github-pages
status: awaiting-approval
intent: clear
review_required: false
created: 2026-08-23
---

# Plan: github-pages

## Summary
为读书知识库生成 GitHub Page：MkDocs Material 静态站 + GitHub Actions 自动构建/部署 + CI 扫描根目录所有 `<书名>/` 自动生成 nav。把同步规则写入 `AGENTS.md` 规则三。新书蒸馏完成 push 即自动 page 化，零额外人工。

## Outcome (definition of done)
1. 站点 `https://meisijiya.github.io/reading/` 可访问
2. 首页含两本书入口 + 一句话介绍 + 模块数
3. 每本书有专属 section，能跳到 INDEX.md / 速查表 / 模块 README
4. 新增一个 `<书名>/` 目录 + push → CI 自动部署 → 新书入口出现
5. `AGENTS.md` 含"规则三：GitHub Page 同步"
6. `design.md`（站点视觉与结构设计文档）由 `/frontend` skill 生成并就位

## Decisions (锁定)
| Fork | 决策 |
|---|---|
| 站点生成器 | MkDocs Material（含 pymdownx 扩展） |
| 自动 nav | `mkdocs-awesome-nav` 插件扫 `<书名>/INDEX.md` |
| section 入口 | `mkdocs-section-index` 让 INDEX.md 成为 section page |
| 部署 | GitHub Actions（peaceiris/workflows-mkdocs 成熟模板） |
| 首页形态 | 标准 docs 入口（docs/index.md） |
| 新书触发 | CI 自动扫描，worker 无需改 nav |
| design.md 路径 | 仓库根 `design.md` |
| AGENTS.md 新章节 | 延续"规则一/规则二"，命名为"规则三：GitHub Page 同步（github-pages-sync）" |

## Files to create / modify

| 路径 | 动作 | 说明 |
|---|---|---|
| `mkdocs.yml` | create | Material 配置 + 自动扫描 nav |
| `docs/index.md` | create | 站点首页 |
| `requirements.txt` | create | 锁依赖：mkdocs-material、mkdocs-awesome-nav、mkdocs-section-index |
| `.github/workflows/pages.yml` | create | Actions 工作流 |
| `.gitignore` | create | 排除 site/、__pycache__/、.venv/、.codegraph/、.omo/drafts/ |
| `design.md` | create | 由 `/frontend` skill 在 worker 中生成（站点设计稿） |
| `AGENTS.md` | edit | 追加"规则三"章节 |
| `.codegraph/` · `.omo/run-continuation/` | ignore | 已在 .gitignore 内 |

## Todos

- [x] 1. `.gitignore`: 写仓库级 .gitignore 排除 site/ __pycache__/ .venv/ .codegraph/ .omo/drafts/ 等本地工件 - expect `git status` 干净
- [x] 2. `requirements.txt`: 锁 mkdocs-material[recommended]==9.* + mkdocs-awesome-nav==3.* + mkdocs-section-index==0.3.* + pymdown-extensions - expect `pip install -r` 可重现构建
- [x] 3. `mkdocs.yml`: 写 Material 配置（site_name=读书知识库, theme=material 默认 palette 暗+亮, search/zh, awesome-nav 自动扫根目录 <书名>/INDEX.md, section-index 启用） - expect `mkdocs build --strict` 通过且 nav 含两本书
- [x] 4. `docs/index.md`: 写首页（站点标题+一句话+两本书卡片：封面 URL + 标题 + 作者 + 模块数 + 速查表入口） - expect README 卡片可点入各书 INDEX
- [x] 5. `AGENTS.md`: 在现有"规则二"之后追加"规则三：GitHub Page 同步（github-pages-sync）"（触发时机：book-distill 完成 push；机制：CI 自动扫描 <书名>/INDEX.md 入 nav；唯一约束：每本书必须有 INDEX.md，否则 site 章节缺失） - expect 现有"规则一/规则二"不被改动
- [x] 6. `design.md`: 在 worker session 中调用 `/frontend` skill 产出站点视觉/结构/交互/响应式设计文档（含设计令牌、栅格、组件清单、断点、可访问性） - expect design.md 在仓库根，可直接作为后续前端实现的依据
- [x] 7. `.github/workflows/pages.yml`: 用 peaceiris/actions-gh-pages 或官方 mkdocs gh-deploy 动作，在 push main 时构建并发布到 GitHub Pages - expect Actions run 成功
- [ ] 8. `git init` + 首次 commit + 添加远程 + `git push -u origin main`: 把本地 read/ 目录推到 meisijiya/reading - expect 远程仓库不再为空
- [ ] 9. 远程启用 GitHub Pages: 在 https://github.com/meisijiya/reading/settings/pages 选 Source=GitHub Actions（或 gh CLI 启用） - expect 首次部署可见
- [ ] 10. 验证首页与两本书入口可达（curl 或浏览器） - expect 两本书入口在 nav 出现且点击可达

## Final verification wave

- [ ] F1. 站点可访问性: `curl -I https://meisijiya.github.io/reading/` 返回 200 - evidence: 命令输出截图或返回头
- [ ] F2. 两本书入口存在: 站点首页与 nav 含两本书卡片/链接 - evidence: 浏览器截图 + nav 文本 grep
- [ ] F3. 同步规则可执行: 模拟"加一个测试目录 `tmp-book-test/`（含 dummy INDEX.md）→ commit → push"，CI 自动扫描并部署，验证 tmp-book-test 出现在 nav 后**回滚测试目录** - evidence: Actions run + nav 截图 + 回滚 commit
- [ ] F4. AGENTS.md 规则三可读: cat AGENTS.md 在规则三章节可见触发/机制/约束三段 - evidence: 文件输出节选
- [ ] F5. design.md 在位: design.md 在仓库根，包含视觉/结构/交互/响应式四节 - evidence: ls + wc -l
- [ ] F6. MkDocs strict 构建零警告: `mkdocs build --strict` exit 0 且无 warning - evidence: 本地构建输出

## Risks / Tradeoffs（提前披露）
- **mkdocs-awesome-nav 自动扫描要求每本书目录下有可识别的入口文件**——故 INDEX.md 是强制锚点；若 worker 蒸馏新书忘了 INDEX.md，F3 验证会失败，故 AGENTS.md 规则三明确这点
- **GitHub Pages 启用是一次性手动设置**（gh repo settings 或 web 端）——非文档级改动，由 worker 在 README/CHANGELOG 不修改的情况下做
- **站点主题锁定 Material 默认**——若用户后续要品牌色或自定义字体，需改 mkdocs.yml 的 theme 自定义块（不再本次范围）
- **CI 用 `mkdocs build --strict`**：broken link 会让 build 失败——worker 蒸馏时若 README 引用了不存在的目标文件会被卡住，需在 book-distill 规则里加"无断链"自检（**本次不修改规则一**，仅记录在 Risks 中由用户后续决定）

## Not in scope（明确不做）
- 自定义域名 / DNS 切换
- 全文搜索增强（用 mkdocs-material 自带 search）
- 问题卡片瀑布流首页
- 评论/反馈系统
- 国际化多语言
- PWA / Service Worker
- 修改"规则一（book-distill）"或"规则二（weread-fetch）"

## Reference
- 远程仓库：https://github.com/meisijiya/reading
- 本地工作目录：/home/ljh2923/opencode-project/read
- 参考实现（书结构）：《轻松破解生活难题：民法典100问》/
- Draft：`.omo/drafts/github-pages.md`
- 设计稿：worker 用 `/frontend` skill 产出 `design.md`

## Workflow next action
等待用户显式 "ok" / "开始" / "execute" → 写完后由用户在 worker session 调 `/start-work` 执行