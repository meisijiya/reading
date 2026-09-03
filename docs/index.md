# 读书知识库

> 把每一本认真读过的书，蒸馏成可检索、可复用、可演进的标准知识包。

本站收录以**微信读书热门划线**为底层的结构化笔记：每本书单独成目录，问题卡片化，三级证据标记，速查表先行。所有内容均由本地代理通过微信读书 API 拉取并归档，离线可读、增量可加。

## 阅读建议

!!! tip "怎么用这个知识库"

    1. **遇到具体问题**：先翻每本书的 `99-速查表.md` 定位场景关键词，再跳到对应模块读原文证据链。
    2. **想了解一本书在讲什么**：从该书的 `INDEX.md` 进入，看「模块速览」表格就能掌握全貌。
    3. **需要可引用出处**：回 `00-原书档案/hot-highlights.json`，`heat` 字段=标记人数=可信度权重。
    4. **想补充自己的理解**：写入对应书目录下的 `additions/`，命名 `YYYY-MM-DD-主题.md`，与速查表同优先级。

证据标记三档：**📖 原文** = 微信读书热门划线逐字引用 ｜ **🧭 归纳** = 从原文提炼 ｜ **➕ 补充** = 编者依据公开常识补充。

## 已收录

<div class="grid cards" markdown>

- :material-scale-balance:{ .lg .middle } **《轻松破解生活难题：民法典100问》**

    ---

    典叔 · 微信读书 89.7 分 · 2024-07 出版

    7 大编 / 100 个高频法律问题，涵盖总则、物权、合同、人格权、婚姻家庭、继承、侵权责任。从胎儿利益到高空抛物，从彩礼到遗嘱，普通人一辈子可能踩的法律坑全覆盖。

    :material-bookmark-multiple: **模块数**: 7
    :material-format-list-numbered: **问题数**: 100
    :material-thermometer: **覆盖率**: 94/107 章 · 464 条原文划线

    [进入 INDEX](./民法典100问/INDEX.md){ .md-button }
    [速查表](./民法典100问/99-速查表.md){ .md-button }
    [从总则编开始](./民法典100问/01-总则编/README.md){ .md-button }

- :material-robot:{ .lg .middle } **《Vibe Coding：AI 编程时代的认知重构》**

    ---

    张昕东 · 微信读书 71.3 分 · 2025-11 出版

    3 大部分 / 14 个核心问题，从 Karpathy 造词的源起，到 Spec/Vibe 双模式实践、上下文工程方法论、"70% 问题"与 Agentic DevOps 前沿，回答「AI 时代程序员还剩什么价值」这一时代之问。

    :material-bookmark-multiple: **模块数**: 3
    :material-format-list-numbered: **问题数**: 14
    :material-thermometer: **覆盖率**: 14/14 正文章 · 244 条原文划线

    [进入 INDEX](./Vibe%20Coding%EF%BC%9AAI%20%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E7%9A%84%E8%AE%A4%E7%9F%A5%E9%87%8D%E6%9E%84/INDEX.md){ .md-button }
    [速查表](./Vibe%20Coding%EF%BC%9AAI%20%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E7%9A%84%E8%AE%A4%E7%9F%A5%E9%87%8D%E6%9E%84/99-速查表.md){ .md-button }
    [从走近 Vibe Coding 开始](./Vibe%20Coding%EF%BC%9AAI%20%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E7%9A%84%E8%AE%A4%E7%9F%A5%E9%87%8D%E6%9E%84/01-走近VibeCoding/README.md){ .md-button }

- :material-code-braces:{ .lg .middle } **《Claude Code橙皮书：AI编程实战》**

    ---

    花叔 · 本地 epub 一次性落档 · 2025-2026 时效内容

    4 大部分 / 14 个核心章节，从 Claude Code 的独特价值定位、10 分钟起步安装，到 CLAUDE.md / Skill / Hook / MCP 扩展机制与多智能体协作，再到 Chrome 扩展 / 内容创作自动化 / App Store 上架三个完整产品实战，构建 AI 编程时代完整工作流。

    :material-bookmark-multiple: **模块数**: 4
    :material-format-list-numbered: **章节数**: 14
    :material-thermometer: **覆盖率**: 100% epub 落档

    [进入 INDEX](./Claude%20Code橙皮书%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E5%AE%9E%E6%88%98%20(%E8%8A%B1%E5%8F%94)/INDEX.md){ .md-button }
    [速查表](./Claude%20Code橙皮书%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E5%AE%9E%E6%88%98%20(%E8%8A%B1%E5%8F%94)/99-速查表.md){ .md-button }
    [从第一部分开始](./Claude%20Code橙皮书%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E5%AE%9E%E6%88%98%20(%E8%8A%B1%E5%8F%94)/01-第一部分/README.md){ .md-button }

</div>

## 知识包结构

每本书都是同一套模板，方便横向迁移和工具识别：

```text
<书名>/
├── INDEX.md              导航入口：元数据 + 覆盖率声明 + 模块速览
├── 00-原书档案/           机器可读原始数据（book-meta / toc / hot-highlights / fulltext）
├── NN-<模块名>/README.md  每模块一文件，问题卡片化（## Q编号 + 📖原文引用 + 热度人数）
├── 99-速查表.md          场景→规则速查 + 关键期限数字（最高频调用入口）
└── additions/            增量区：新理解、新案例、实践结果（不改原文档案）
```

!!! note "为什么用 `additions/` 而不是改原文"

    知识包的稳定性来自「原文档案只读 + 增量追加」。你今天顿悟的一条规则，应该写在 `additions/2026-08-23-xxx.md` 里，标注「影响速查表第 X 条」即可覆盖旧条目。原书档案保持冻结，方便未来回溯「这条认知是何时加进来的」。

## 数据来源与局限

!!! warning "全文覆盖率不是 100%"

    微信读书 Agent API **不提供正文章节全文接口**。本知识包能稳定拿到 100% 的章节目录与每章按热度排序的热门划线（通常覆盖读者共识最强的核心观点），但非热门段落的原文不在公开接口范围内。

    **升级到 100% 全文**：将账号内导出的全书内容（EPUB/TXT/PDF）放入对应书目录的 `00-原书档案/fulltext/`，更新 `INDEX.md` 即可，目录结构无需变动。

## 贡献约定

!!! example "想加一本新书？"

    1. 在仓库根新建 `<书名>/` 目录
    2. 调微信读书 API 拉 `book-meta` / `chapterinfo` / `bestbookmarks`，存到 `00-原书档案/`
    3. 按模块编号建 `NN-<模块名>/README.md`，每问一张 `## Q编号` 卡片
    4. 写 `99-速查表.md`，场景先行
    5. 在 `INDEX.md` 顶部写「覆盖率声明」与「升级路径」
    6. 提交后 awesome-nav 会自动把新书挂到导航

## 维护者

站点由 [meisijiya](https://github.com/meisijiya) 维护，知识包通过本地代理（[weread-skills](https://github.com/meisijiya/weread-skills)）从微信读书自动构建。每一本书的「覆盖率声明」与「升级路径」都写在各自书的 `INDEX.md` 顶部，欢迎按相同规范追加新书。
