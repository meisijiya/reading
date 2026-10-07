# 《AI Prompt Engineering: The 2026 Guide》标准知识包

> **一句话**：「AI Prompt Engineering Team」合著的 2026 版提示工程实战手册——以 **4 C's Framework（Clear / Concise / Contextual / Conversational）** 为底层心法，主册 **320 条跨场景模板**（Chat / Writing / Analysis / Coding / Image / Business）+ 附录 **100 条加餐（B1–B100）**，加上 **8 个经典进阶策略 + 12 个 2026 独有技法（XML / Reasoning / Agents / MCP / Caching / Meta-Prompting / Eval / Structured Outputs / Long-Context / Multimodal / Roles / Injection Defense）**，完整覆盖从入门到生产提示工程的全链路。

## 书籍元数据

| 字段 | 值 |
|---|---|
| 标题 | AI Prompt Engineering : The 2026 Guide — 420+ Battle-Tested Prompts, the 4 C's Framework, and How to Scale Your Business with AI |
| 作者 | AI Prompt Engineering Team（合著团队，含工程 / 营销 / 研究 / 设计 / 运营） |
| 出版年 | 2026（identifier `urn:asin:B0GX5HMB1M`；date `2026-04-14`） |
| 语言 | `en`（全文英文；本知识包提炼层为中文，📖原文保英文 verbatim） |
| fileSha256 | `ffd26f17e2ae0d8c1ae11f46e3c0aed4f0d38f6a11c1b71fdbc3a468f5816c6f` |
| fileSize | 403,384 字节（约 394 KB） |
| spineItemsCount | 3 |
| chapterCount | 22（10 章 + 1 收官 + 10 附录 + 1 About） |
| 打开源文件 | `book/AI Prompt Engineering  The 2026 Guide — 420+ ... (Team, AI Prompt Engineering) (z-library.sk, 1lib.sk, z-lib.sk).epub`（本地 epub，未发布到 GitHub Pages） |

> 元数据来源：[`00-原书档案/book-meta.json`](00-原书档案/book-meta.json)（与原书 OPF + c63.xhtml h1 切粒一致）。

## 覆盖率与数据来源声明

本知识包通过 **epub 一次性落档** 构建——`ebooklib` 解析原书 OPF + 整本正文 `OEBPS/c63.xhtml` 按 22 个 h1 节点切粒（Chapter N: × 10 + Your Prompt Engineering Journey × 1 + Appendix A–J × 10 + About the Authors × 1），落盘 `fulltext/`，全部 19 张 `<table>` 转 GFM markdown 保留。提炼层只从原文归纳，禁止凭模型常识编造「书中观点」。

| 层 | 完整度 | 来源 |
|---|---|---|
| 章节目录（22 h1 节点） | ✅ 100% | epub c63.xhtml h1 顺序 + h2 子节 ([`toc.md`](00-原书档案/toc.md)) |
| 原书文本（22 章节正文 + 19 表 + 1 封面图） | ✅ 100% | epub fulltext（`fulltext/uid-NN-题名.md`，约 2.2 万字） |
| 方法提炼（每章卡片 + 速查表） | 由上述原文归纳 + 编者补充公开常识 | 见下方三级标记约定 |

**证据标记约定**（全包统一，**无热度括号**——epub 无 heat 概念）：

- 📖 **原文** = epub fulltext 逐字引用，未改动；附 `§N.M` 章节内 h2 锚点 + `uid NN` fulltext 文件编号。**英文保留**与原文一致。
- 🧭 **归纳** = 编者从原文提炼的结构化结论，**中文输出**。
- ➕ **补充** = 编者依据公开常识补充（非原书内容）。

**升级路径**：N/A（本包覆盖率已 100%，无需再升级；若日后原书修订，重跑 `scripts/distill_epub_aiprompt.py --force` 覆盖 `00-原书档案/fulltext/` 即可）。

## 目录结构与检索指南

```
AI Prompt Engineering: The 2026 Guide/
├── INDEX.md                  ← 本文件：导航入口
├── 00-原书档案/               ← 原始数据（机器可读）
│   ├── book-meta.json            书籍元信息（OPF + 切粒统计）
│   ├── toc.md                    22 章 uid/level/chapterNumber/title/parentPart 表
│   ├── epub/                     原书 epub 归档
│   ├── fulltext/                 ← 22 章完整正文（uid-NN-题名.md，h1 一节点一文件）
│   └── assets/                   原书封面图资源
├── 01-基础与导读/             ← Chapter 1–3：What Is PE / LLMs / 4 C's Framework（基础心法）
├── 02-场景-Prompt-模板库/     ← Chapter 4–8：270 条跨场景模板（Chat / Writing / Analysis / Coding / Image）
├── 03-进阶与商业应用/         ← Chapter 9–10 + Journey：8 进阶策略 + 50 商业模板 + 收官
├── 04-参考附录-A-E/           ← Appendix A–E：420 索引 + 模型版图 + 工具 + 资源 + 检查清单
├── 05-实战卷-F-J-与作者/      ← Appendix F–J + Authors：速查 + 12 专家技法 + 30 天计划 + 词表 + 100 加餐
├── 99-速查表.md               ← 场景→方法速查 + 关键数字（最常调用入口）
└── additions/                 ← 你的新理解/新案例/实践结果追加处
    └── README.md
```

**给 AI 的检索建议**：

1. **小节级精确定位**：按 `§N.M` 锚点 grep 可直接命中某章某 h2——例如 `grep '§3.3' "AI Prompt Engineering: The 2026 Guide/01-基础与导读/README.md"` 命中 4 C's 中"上下文三角"全部引用块。
2. **章节定位**：按 `uid` 编号 grep 命中整章卡片集合——`grep '^uid: 09' "AI Prompt Engineering: The 2026 Guide/00-原书档案/fulltext/"`。
3. **场景速查**：先查 `99-速查表.md` 定位场景/类别 → 再回对应 `NN-部/README.md` 读原文证据链。
4. **公式 & 模型选择**：附录 F（Quick Reference）粘在墙上；附录 G（Expert Techniques 2026）是 12 个独有技法的全集；附录 B（Model Landscape）的 5 行 Model-Picking 是模型选型判据。
5. **420 模板索引**：附录 A 是 uid 1–320 的全索引；附录 J 100 加餐按 B1–B100 编号；详细全文回 `00-原书档案/fulltext/uid-NN-题名.md` 找编号对应的原文段落。
6. **查 frontmatter 元数据**：每张 fulltext 文件顶部 frontmatter 含 `uid / level / chapterNumber / chapterKind / title / wordCount / parentPart`，可与 `toc.md` 表头交叉对账。
7. **回溯原书**：卡片引用的 `§N.M` 锚点可在 `00-原书档案/fulltext/uid-NN-题名.md` 中找到对应 h2 段 verbatim 原文（英文原汁原味）。
8. **引用时严格区分** 📖原文（英文 verbatim）/ 🧭归纳（中文提炼）/ ➕补充（公开常识）三种性质；本包「📖原文」无热度括号（epub 无 heat 字段）。
9. **AI 检索优先级**：`additions/` 与 `99-速查表.md` 同优先级；additions 中标注「影响」的条目覆盖速查表对应旧条目。

## 五大模块速览

| 模块 | 章节 | 主题 |
|---|---|---|
| [一 基础与导读](01-基础与导读/README.md) | Chapter 1–3（3 章，含导读） | 入门：Prompt Engineering 是什么、与谁对话（LLM）、贯穿全书的 **4 C's Framework（Clear / Concise / Contextual / Conversational）** + 完整公式 [Role + Situation + Task + Constraints + Format + Tone] |
| [二 场景 Prompt 模板库](02-场景-Prompt-模板库/README.md) | Chapter 4–8（5 章 · 270 条） | 跨场景模板：Chat 50（对话生命周期）/ Writing 65（5 要素公式 · 6 类）/ Analysis 50（Data+Type+Focus+Format · 7 类）/ Coding 45（Lang+Constraints+Context · 6 类）/ Image 60（Subject+Style+Composition+Lighting+Tech · 6 类） |
| [三 进阶与商业应用](03-进阶与商业应用/README.md) | Chapter 9–10 + Journey（3 章 · 50 条） | 进阶：8 个经典策略（CoT / Self-Consistency / Chaining / Role / Constraints / Iteration / Structured Outputs / Meta-Prompting）+ 50 条商业模板（运营 / 营销销售 / 流程 / 创业 / 自动化 5 块 ROI 公式） |
| [四 参考附录 A–E](04-参考附录-A-E/README.md) | Appendix A–E（5 参考卷） | 参考：420 Prompt 全索引（主册 320 + 加餐 100）/ 2026 模型版图 5 维选型 / 7 大类工具栈 / 5 类学习资源 / 4 张检查清单（Pre / Post / Library / Safety） |
| [五 实战卷 F–J + 作者](05-实战卷-F-J-与作者/README.md) | Appendix F–J + About（6 章） | 实战：**速查粘墙（F）/ 12 个 2026 独有技法（G）/ 30 天落地计划（H）/ 30 词术语表（I）/ 100 加餐（J）/ 作者结语** |

## 完整章节目录（直链完整原文）

> 章节标题直接链到 `00-原书档案/fulltext/uid-NN-*.md` 完整原文页（英文原文）。每章独立可读，无需经过模块页。

| UID | 章节 | 字数 | 所属 | 原文 |
|---|---|---:|---|---|
| §1 | [Chapter 1: What Is Prompt Engineering?](00-原书档案/fulltext/uid-01-what-is-prompt-engineering.md) | 7,177 | 一 基础与导读 | [完整原文](00-原书档案/fulltext/uid-01-what-is-prompt-engineering.md) |
| §2 | [Chapter 2: Understanding Large Language Models](00-原书档案/fulltext/uid-02-understanding-large-language-models.md) | 7,722 | 一 基础与导读 | [完整原文](00-原书档案/fulltext/uid-02-understanding-large-language-models.md) |
| §3 | [Chapter 3: The 4 C's Framework](00-原书档案/fulltext/uid-03-the-4-c-s-framework.md) | 6,679 | 一 基础与导读 | [完整原文](00-原书档案/fulltext/uid-03-the-4-c-s-framework.md) |
| §4 | [Chapter 4: Chat & Conversation Prompts](00-原书档案/fulltext/uid-04-chat-conversation-prompts.md) | 5,680 | 二 场景 Prompt 模板库 | [完整原文](00-原书档案/fulltext/uid-04-chat-conversation-prompts.md) |
| §5 | [Chapter 5: Writing & Content Creation Prompts](00-原书档案/fulltext/uid-05-writing-content-creation-prompts.md) | 11,415 | 二 场景 Prompt 模板库 | [完整原文](00-原书档案/fulltext/uid-05-writing-content-creation-prompts.md) |
| §6 | [Chapter 6: Analysis & Research Prompts](00-原书档案/fulltext/uid-06-analysis-research-prompts.md) | 7,712 | 二 场景 Prompt 模板库 | [完整原文](00-原书档案/fulltext/uid-06-analysis-research-prompts.md) |
| §7 | [Chapter 7: Coding & Technical Prompts](00-原书档案/fulltext/uid-07-coding-technical-prompts.md) | 8,279 | 二 场景 Prompt 模板库 | [完整原文](00-原书档案/fulltext/uid-07-coding-technical-prompts.md) |
| §8 | [Chapter 8: Image Generation Prompts](00-原书档案/fulltext/uid-08-image-generation-prompts.md) | 8,281 | 二 场景 Prompt 模板库 | [完整原文](00-原书档案/fulltext/uid-08-image-generation-prompts.md) |
| §9 | [Chapter 9: Advanced Strategies](00-原书档案/fulltext/uid-09-advanced-strategies.md) | 7,065 | 三 进阶与商业应用 | [完整原文](00-原书档案/fulltext/uid-09-advanced-strategies.md) |
| §10 | [Chapter 10: Business Applications](00-原书档案/fulltext/uid-10-business-applications.md) | 7,969 | 三 进阶与商业应用 | [完整原文](00-原书档案/fulltext/uid-10-business-applications.md) |
| §00 | [Your Prompt Engineering Journey](00-原书档案/fulltext/uid-11-your-prompt-engineering-journey.md) | 429 | 三 进阶与商业应用 | [完整原文](00-原书档案/fulltext/uid-11-your-prompt-engineering-journey.md) |
| §A | [Appendix A: The 320-Prompt Catalog](00-原书档案/fulltext/uid-12-the-320-prompt-catalog.md) | 1,728 | 四 参考附录 A–E | [完整原文](00-原书档案/fulltext/uid-12-the-320-prompt-catalog.md) |
| §B | [Appendix B: Model Landscape 2026](00-原书档案/fulltext/uid-13-model-landscape-2026.md) | 2,246 | 四 参考附录 A–E | [完整原文](00-原书档案/fulltext/uid-13-model-landscape-2026.md) |
| §C | [Appendix C: Prompt Engineering Tools](00-原书档案/fulltext/uid-14-prompt-engineering-tools.md) | 1,566 | 四 参考附录 A–E | [完整原文](00-原书档案/fulltext/uid-14-prompt-engineering-tools.md) |
| §D | [Appendix D: Learning Resources](00-原书档案/fulltext/uid-15-learning-resources.md) | 995 | 四 参考附录 A–E | [完整原文](00-原书档案/fulltext/uid-15-learning-resources.md) |
| §E | [Appendix E: Prompt Engineering Checklists](00-原书档案/fulltext/uid-16-prompt-engineering-checklists.md) | 1,151 | 四 参考附录 A–E | [完整原文](00-原书档案/fulltext/uid-16-prompt-engineering-checklists.md) |
| §F | [Appendix F: Quick Reference Guide](00-原书档案/fulltext/uid-17-quick-reference-guide.md) | 1,096 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-17-quick-reference-guide.md) |
| §G | [Appendix G: Expert Techniques for 2026](00-原书档案/fulltext/uid-18-expert-techniques-for-2026.md) | 6,360 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-18-expert-techniques-for-2026.md) |
| §H | [Appendix H: Your 30-Day Prompt Engineering Plan](00-原书档案/fulltext/uid-19-your-30-day-prompt-engineering-plan.md) | 2,185 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-19-your-30-day-prompt-engineering-plan.md) |
| §I | [Appendix I: Prompt Engineering Glossary](00-原书档案/fulltext/uid-20-prompt-engineering-glossary.md) | 2,250 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-20-prompt-engineering-glossary.md) |
| §J | [Appendix J: 100 Bonus Prompts](00-原书档案/fulltext/uid-21-100-bonus-prompts.md) | 20,639 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-21-100-bonus-prompts.md) |
| About | [About the Authors](00-原书档案/fulltext/uid-22-about-the-authors.md) | 729 | 五 实战卷 F–J + 作者 | [完整原文](00-原书档案/fulltext/uid-22-about-the-authors.md) |

> 新增理解请写入 `additions/`，命名建议：`YYYY-MM-DD-主题.md`
